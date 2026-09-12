# -*- coding: utf-8 -*-
"""Enxuga os PDFs A3: o "subset" do MuPDF embute a fonte inteira (654 glifos)
quando as pranchas usam pouco mais de cem. Aqui os glifos não usados são
esvaziados, mantendo os GIDs no lugar — nada no resto do PDF precisa mudar.
"""
import io, os, re, sys
import pymupdf
from fontTools.cffLib import CFFFontSet
from fontTools.misc.psCharStrings import T2CharString
from fontTools.pens.t2CharStringPen import T2CharStringPen

RE_FONTE = re.compile(rb'/(F\d+)\s+[\d.]+\s+Tf')
RE_HEX = re.compile(rb'<([0-9A-Fa-f]+)>')


def gids_usados(doc):
    """GIDs efetivamente desenhados, por nome de recurso de fonte (/F0, /F1)."""
    uso = {}
    for x in range(1, doc.xref_length()):
        sub = doc.xref_get_key(x, 'Subtype')
        if not sub or sub[1] != '/Form':
            continue
        try:
            fluxo = doc.xref_stream(x)
        except Exception:
            continue
        if not fluxo:
            continue
        atual = None
        pos = 0
        for m in re.finditer(rb'/(F\d+)\s+[\d.]+\s+Tf|<([0-9A-Fa-f]+)>', fluxo):
            if m.group(1):
                atual = m.group(1).decode()
            elif atual:
                h = m.group(2)
                for i in range(0, len(h) - 3, 4):
                    uso.setdefault(atual, set()).add(int(h[i:i + 4], 16))
    return uso


def mapa_recurso_para_cff(doc):
    """/F0 -> xref do fluxo CFF correspondente."""
    mapa = {}
    for x in range(1, doc.xref_length()):
        sub = doc.xref_get_key(x, 'Subtype')
        if not sub or sub[1] != '/Form':
            continue
        rec = doc.xref_get_key(x, 'Resources/Font')
        if not rec or rec[0] == 'null':
            continue
        for nome in re.findall(r'/(F\d+)\s+(\d+)\s+0\s+R', rec[1]):
            f_nome, f_xref = nome[0], int(nome[1])
            desc = doc.xref_get_key(f_xref, 'DescendantFonts')
            if not desc or desc[0] == 'null':
                continue
            cid_xref = int(re.search(r'(\d+)\s+0\s+R', desc[1]).group(1))
            fd = doc.xref_get_key(cid_xref, 'FontDescriptor')
            fd_xref = int(re.search(r'(\d+)\s+0\s+R', fd[1]).group(1))
            ff = doc.xref_get_key(fd_xref, 'FontFile3')
            ff_xref = int(re.search(r'(\d+)\s+0\s+R', ff[1]).group(1))
            mapa[f_nome] = ff_xref
    return mapa


def esvazia(raw, manter):
    """Reescreve o CFF: só os glifos usados sobrevivem, já sem sub-rotinas.

    Os GIDs continuam nas mesmas posições, então o /W, o Identity-H e o
    conteúdo das páginas não precisam de nenhum ajuste.
    """
    cff = CFFFontSet()
    cff.decompile(io.BytesIO(raw), None)
    td = cff[cff.fontNames[0]]
    cs = td.CharStrings
    ordem = td.getGlyphOrder()
    vazio = T2CharString(bytecode=b'\x0e')          # endchar

    def private_de(gid):
        if hasattr(td, 'FDArray'):
            return td.FDArray[td.FDSelect[gid]].Private
        return td.Private

    n = 0
    for gid, nome in enumerate(ordem):
        if gid not in manter:
            cs[nome] = vazio
            n += 1
            continue
        # redesenha o glifo sem chamadas de sub-rotina
        antigo = cs[nome]
        try:
            largura = antigo.width
        except Exception:
            largura = None
        priv = private_de(gid)
        pen = T2CharStringPen(largura, cs)
        try:
            antigo.draw(pen)
            cs[nome] = pen.getCharString(private=priv)
        except Exception:
            pass                                     # mantém o original

    # sem sub-rotinas, os índices podem ir embora
    for priv in ([td.FDArray[i].Private for i in range(len(td.FDArray))]
                 if hasattr(td, 'FDArray') else [td.Private]):
        if hasattr(priv, 'Subrs'):
            priv.Subrs.items = []
            del priv.rawDict['Subrs']
            del priv.Subrs
    cff.GlobalSubrs.items = []

    class _Fake(object):
        recalcBBoxes = False
        isTTF = False
        def __getitem__(self, k):
            raise KeyError(k)
    buf = io.BytesIO()
    cff.compile(buf, _Fake(), isCFF2=False)
    return buf.getvalue(), n, len(ordem)


def enxugar(src, dst, verboso=False):
    doc = pymupdf.open(src)
    uso = gids_usados(doc)
    mapa = mapa_recurso_para_cff(doc)
    for f_nome, ff_xref in mapa.items():
        manter = uso.get(f_nome, set()) | {0}
        raw = doc.xref_stream(ff_xref)
        novo, zerados, total = esvazia(raw, manter)
        doc.update_stream(ff_xref, novo, compress=True)
        doc.xref_set_key(ff_xref, 'Length1', str(len(novo)))
        if verboso:
            print('   %s: %d de %d glifos mantidos, CFF %d -> %d'
                  % (f_nome, total - zerados, total, len(raw), len(novo)))
    doc.subset_fonts()
    doc.save(dst, garbage=4, deflate=True, deflate_fonts=True, clean=True)
    return os.path.getsize(src), os.path.getsize(dst)


if __name__ == '__main__':
    for caminho in sys.argv[1:]:
        base, ext = os.path.splitext(caminho)
        saida = base + '-leve' + ext
        a, b = enxugar(caminho, saida, verboso=True)
        print('%-40s %7d -> %7d  (-%d%%)'
              % (os.path.basename(caminho), a, b, round(100 - 100.0 * b / a)))
