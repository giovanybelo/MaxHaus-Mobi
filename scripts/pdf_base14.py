# -*- coding: utf-8 -*-
"""Troca as fontes embutidas dos PDFs A3 pelas Times padrão do PDF (base-14).

O MuPDF embute Times-Roman e Times-Bold como CID/Identity-H. Qualquer leitor de
PDF já traz essas duas fontes, com as mesmas métricas: basta referenciá-las,
sem embutir. O texto é recodificado de GID para WinAnsi pelo ToUnicode do
próprio arquivo. O desenho não muda; o arquivo cai para uma fração.
"""
import os
import re
import sys

import pymupdf

RE_HEX = re.compile(rb'<([0-9A-Fa-f]+)>')
TROCAS = {'−': '–', '‑': '-', ' ': ' '}


def _cmap(texto):
    m = {}
    for bloco in re.findall(r'beginbfrange(.*?)endbfrange', texto, re.S):
        for a, b, dst in re.findall(r'<(\w+)>\s*<(\w+)>\s*<(\w+)>', bloco):
            a, b, u = int(a, 16), int(b, 16), int(dst, 16)
            for i in range(b - a + 1):
                m[a + i] = chr(u + i)
    for bloco in re.findall(r'beginbfchar(.*?)endbfchar', texto, re.S):
        for a, dst in re.findall(r'<(\w+)>\s*<(\w+)>', bloco):
            m[int(a, 16)] = chr(int(dst, 16))
    return m


def converter(src, dst):
    doc = pymupdf.open(src)
    fontes = {}
    for x in range(1, doc.xref_length()):
        if doc.xref_get_key(x, 'Type')[1] != '/Font':
            continue
        if doc.xref_get_key(x, 'Subtype')[1] != '/Type0':
            continue
        base = doc.xref_get_key(x, 'BaseFont')[1].split('+')[-1]
        tu = int(doc.xref_get_key(x, 'ToUnicode')[1].split()[0])
        fontes[x] = (base, _cmap(doc.xref_stream(tu).decode('latin-1')))
    if not fontes:
        doc.save(dst, garbage=4, deflate=True, use_objstms=1)
        return
    mapa = next(iter(fontes.values()))[1]
    if any(f[1] != mapa for f in fontes.values()):
        raise ValueError('ToUnicode diferente entre fontes: %s' % src)
    faltas = set()

    def recodifica(m):
        h = m.group(1)
        if len(h) % 4:
            return m.group(0)
        out = []
        for i in range(0, len(h), 4):
            ch = mapa.get(int(h[i:i + 4], 16), '?')
            ch = TROCAS.get(ch, ch)
            try:
                out.append(ch.encode('cp1252'))
            except UnicodeEncodeError:
                faltas.add(ch)
                out.append(b'?')
        return b'<' + b''.join(out).hex().encode() + b'>'

    for x in range(1, doc.xref_length()):
        if doc.xref_get_key(x, 'Subtype')[1] != '/Form':
            continue
        fluxo = doc.xref_stream(x)
        if not fluxo or b'Tf' not in fluxo:
            continue
        partes = re.split(rb'(BT.*?ET)', fluxo, flags=re.S)
        novo = b''.join(RE_HEX.sub(recodifica, p) if p.startswith(b'BT') else p
                        for p in partes)
        doc.update_stream(x, novo, compress=True)
    for x, (base, _) in fontes.items():
        doc.update_object(x, '<</Type/Font/Subtype/Type1/BaseFont/%s'
                             '/Encoding/WinAnsiEncoding>>' % base)
    if faltas:
        raise ValueError('sem equivalente WinAnsi em %s: %r' % (src, sorted(faltas)))
    doc.save(dst, garbage=4, deflate=True, clean=True, use_objstms=1)


if __name__ == '__main__':
    destino = sys.argv[1]
    os.makedirs(destino, exist_ok=True)
    for src in sys.argv[2:]:
        dst = os.path.join(destino, os.path.basename(src))
        converter(src, dst)
        print('%-48s %7d -> %6d' % (os.path.basename(src), os.path.getsize(src),
                                     os.path.getsize(dst)))
