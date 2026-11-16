# -*- coding: utf-8 -*-
"""Executivo do banheiro — geometria, paginação e desenho (emissão E4, 16.11.2026: pares Nuage; E1 a E3 superadas).

Medidas em milímetros, faces ACABADAS, origem no canto interno noroeste do
banheiro: x cresce para leste, y para sul, z para cima a partir do piso pronto.

Fontes das medidas
  · cliente, em obra, 14.11.2026: parede da porta por fora 880 + 800 + 1200 =
    2880; vão da porta 800 × 2150; área técnica do chuveiro 800 × 250; bancada
    1600 × 400 com saia de 100; gabinete 880 de altura × 1600 × 400; espelho
    1600 × 900; topo da bancada a 980; box com 920 de fundo.
  · modelo R95 (12.11.2026): largura acabada 1420; forro e topo do revestimento
    a 2500; nicho a +1100, com 400 de altura (de parede a parede: cliente, 14/11);
    ralo linear 720 × 90; vaso com eixo a 980
    da parede da bancada; toalheiro 550 × 370; Bleu Nuit 155 × 155, junta 2.
  · FAS, pedido 22804 e folha F02: D1 Halo 7 W e D2 Tiny 5,8 W IP.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pymupdf
import base_mainfloor as bm
from base_mainfloor import (folha_nova, salvar, exportar_pdf_a3, exportar_png, esc,
                            W, H, MARGIN, BG, K, K70, K45, K20, K12, K07, K04,
                            INK, INK_SOFT, RULE, DEMO, CIANO, CIANO18, AMARELO,
                            AMARELO40, BRANCO, br)

EMISSAO = 'E4  ·  16/11/2026'
MM = 1.0 / 0.3                      # unidades da folha por mm de papel (A3 = 1400 × 990)

# --- geometria ---------------------------------------------------------------
LARG, COMP = 1420.0, 2680.0         # x, y
PAREDE = 100.0
BOX_Y = COMP - 920.0                # 1760: linha do vidro do box
AT = (0.0, COMP - 800.0, 250.0, COMP)            # área técnica do chuveiro
BANC = (0.0, BOX_Y - 1600.0, 400.0, BOX_Y)       # bancada / gabinete / espelho
PORTA = (880.0 - PAREDE, 880.0 - PAREDE + 800.0)  # 780 → 1580, na parede leste
PORTA_H = 2150.0
FORRO = 2500.0
LAJE = 2620.0
TOPO_BANC, GABINETE_H, SAIA = 980.0, 880.0, 100.0
ESP_BASE, ESP_H = 1340.0, 900.0      # espelho: base proposta 360 acima do tampo
VASO_X = 980.0
R1 = (312.0, 1903.0, 402.0, 2623.0)             # ralo linear 720 × 90
R2 = (1230.0, 250.0, 1330.0, 350.0)             # ralo ao lado do vaso, grelha 100 × 100
CUBA_Y = (BANC[1] + BANC[3]) / 2.0              # 960
Q_Y, F_Y = CUBA_Y + 100.0, CUBA_Y - 100.0       # quente ao sul (esquerda de quem usa)
Z_COMANDO, Z_BICA = 1245.0, 1250.0
CH = (653.0, 2208.0)                            # eixo do chuveiro
D1 = (910.0, 880.0)                             # FAS D1 Halo — luz geral
D2 = (957.0, 2261.0)                            # FAS D2 Tiny IP — box
EX = (1150.0, 1480.0)
NICHO_PROF = 118.0                              # profundidade do nicho (R95)
NICHO = (0.0, LARG - 250.0, 1100.0, 1500.0)     # na P1, de parede a parede: u0, u1, z0, z1
TOALHEIRO = (VASO_X - 275.0, VASO_X + 275.0, 989.0, 1359.0)   # na P5

PECA, JUNTA = 155.0, 2.0
MOD = PECA + JUNTA

# acentos Nuage 75 x 155: sempre em par, ocupando uma célula inteira da malha (75 + 5 + 75 = 155)
NUAGE_L, NUAGE_J = 75.0, 5.0
NUAGE_COR = AMARELO40
ACENTO_DENS = 10          # 1 par a cada ~10 peças inteiras elegíveis

# bancada revestida com Bleu Nuit (cliente, 15/11): tampo, saia e lateral norte
TAMPO_U = (AT[1] - BANC[3], AT[1] - BANC[1])     # 120 → 1720, na coordenada da P3 (u a partir do box)
P3_E0 = 59.0                                     # primeiro corte da malha da P3


# --- paginação -----------------------------------------------------------------
def colunas(larg, quina=False, e0=None):
    """Colunas (u0, u1, inteira) com eixo central e pontas iguais (>= 40% da peça)."""
    if quina:   # retorno estreito: peça inteira na quina externa, corte no canto
        return [(0.0, PECA, True), (PECA + JUNTA, larg - JUNTA, False)]
    if e0 is not None:   # malha deslocada: primeiro corte e0, o último é o que sobrar
        cols, u = [(0.0, e0, False)], e0 + JUNTA
        while u + PECA <= larg - JUNTA:
            cols.append((u, u + PECA, True))
            u += MOD
        if larg - u > 1.0:
            cols.append((u, larg, False))
        return cols
    n = int((larg - JUNTA) // MOD)
    while n > 0:
        e = (larg - n * PECA - (n + 1) * JUNTA) / 2.0
        if e >= 0.4 * PECA or abs(e) < 0.5:
            break
        n -= 1
    cols, u = [], 0.0
    if e > 0.5:
        cols.append((0.0, e, False))
        u = e + JUNTA
    else:
        u = JUNTA
    for _ in range(n):
        cols.append((u, u + PECA, True))
        u += MOD
    if e > 0.5:
        cols.append((u, larg, False))
    return cols


def fiadas(topo=FORRO):
    rows, z = [], 0.0
    while z + PECA <= topo + 0.01:
        rows.append((z, z + PECA, True))
        z += MOD
    if topo - z > 5:
        rows.append((z, topo, False))
    return rows


def _menos(r, h):
    a, b, c, d = r
    x, y, z, w = h
    ix, iy, iz, iw = max(a, x), min(b, y), max(c, z), min(d, w)
    if iy <= ix + 1e-6 or iw <= iz + 1e-6:
        return [r]
    out = [(a, ix, c, d), (iy, b, c, d), (ix, iy, c, iz), (ix, iy, iw, d)]
    return [q for q in out if q[1] - q[0] > 1.0 and q[3] - q[2] > 1.0]


class Parede:
    def __init__(self, pid, nome, larg, furos=(), quina=False, vista='', e0=None, evitar=()):
        self.evitar = list(evitar)
        self.id, self.nome, self.larg, self.furos, self.vista = pid, nome, larg, list(furos), vista
        self.cols, self.rows = colunas(larg, quina, e0), fiadas()
        self.pecas = []          # (num, fi, ci, [frags], inteira)
        n = 0
        for fi, (z0, z1, rf) in enumerate(self.rows):
            for ci, (u0, u1, cf) in enumerate(self.cols):
                fr = [(u0, u1, z0, z1)]
                for h in self.furos:
                    fr = [q for r in fr for q in _menos(r, h[:4])]
                if not fr:
                    continue
                n += 1
                cheia = rf and cf and len(fr) == 1 and fr[0] == (u0, u1, z0, z1)
                self.pecas.append((n, fi, ci, fr, cheia))
        self.acentos = self._acentos()

    def _acentos(self):
        """Pares Nuage espalhados: só em peças inteiras (fora da fiada cortada do topo), no máximo um por fiada,
        sem encostar em outro par (nem na diagonal) e sem repetir a coluna a menos de 4 fiadas."""
        import random
        ult = len(self.rows) - 1
        cand = [(n, fi, ci) for (n, fi, ci, fr, cheia) in self.pecas if cheia and fi < ult
                and not any(_menos(fr[0], e) != [fr[0]] for e in self.evitar)]
        alvo = int(round(len(cand) / float(ACENTO_DENS)))
        rnd = random.Random('nuage-' + self.id)
        rnd.shuffle(cand)
        ok = []
        for n, fi, ci in cand:
            if len(ok) >= alvo:
                break
            if any(f == fi or (abs(f - fi) <= 1 and abs(c - ci) <= 1) or (c == ci and abs(f - fi) <= 3) for _, f, c in ok):
                continue
            ok.append((n, fi, ci))
        return {n for n, _, _ in ok}

    @property
    def n_bleu(self):
        return len(self.pecas) - len(self.acentos)

    @property
    def n_nuage(self):
        return 2 * len(self.acentos)

    @property
    def area(self):
        return sum((b - a) * (d - c) for p in self.pecas for (a, b, c, d) in p[3]) / 1e6

    @property
    def inteiras(self):       # Bleu Nuit inteiras (as células dos pares Nuage não contam)
        return sum(1 for p in self.pecas if p[4] and p[0] not in self.acentos)


PAREDES = [
    Parede('P5', 'Parede do vaso e do toalheiro (norte)', LARG, vista='de frente para o norte · esquerda = bancada',
           evitar=[TOALHEIRO]),
    Parede('P4', 'Parede da porta (leste)', COMP,
           furos=[(PORTA[0], PORTA[1], 0.0, PORTA_H, 'PORTA  800 × 2150')],
           vista='de frente para o leste · esquerda = parede do vaso'),
    Parede('P1', 'Fundo do box e nicho (sul)', LARG - AT[2],
           furos=[NICHO + ('NICHO DE PAREDE A PAREDE  1170 × 400',)],
           vista='de frente para o sul · esquerda = parede da porta'),
    Parede('P2', 'Face da área técnica dentro do box', AT[3] - AT[1],
           vista='de frente para o oeste · esquerda = fundo do box'),
    Parede('P6', 'Retorno da área técnica', AT[2], quina=True,
           vista='de frente para o sul · esquerda = quina externa'),
    Parede('P3', 'Parede da bancada e do espelho (oeste)', AT[1],
           furos=[(AT[1] - BANC[3], AT[1] - BANC[1], 0.0, TOPO_BANC, 'GABINETE E BANCADA'),
                  (AT[1] - BANC[3], AT[1] - BANC[1], ESP_BASE, ESP_BASE + ESP_H, 'ESPELHO  1600 × 900')],
           vista='de frente para o oeste · esquerda = box', e0=59.0),
]
PAR = {p.id: p for p in PAREDES}


# --- texto -------------------------------------------------------------------------
def larg_txt(t, size, bold=False):
    return pymupdf.get_text_length(t, fontname='hebo' if bold else 'helv', fontsize=size)


def quebra(t, w, size, bold=False):
    out, cur = [], ''
    for p in t.split():
        if cur and larg_txt(cur + ' ' + p, size, bold) > w * 0.955:
            out.append(cur)
            cur = p
        else:
            cur = (cur + ' ' + p) if cur else p
    if cur:
        out.append(cur)
    return out


class Folha:
    """Folha A3 com cabeçalho e rodapé do executivo do banheiro."""

    def __init__(self, caderno, cod, titulo, sub='', escala='sem escala'):
        self.d = folha_nova()
        self.cod = cod
        d = self.d
        self.t(MARGIN, 42, 'MAXHAUS 81  ·  BANHEIRO  ·  ' + caderno, 9.0, INK_SOFT, True, ls=1.4)
        self.t(MARGIN, 76, titulo, 24, INK, True)
        if sub:
            self.t(MARGIN, 97, sub, 9.0, INK_SOFT)
        self.t(W - MARGIN, 42, EMISSAO, 9.0, DEMO, True, 'end', ls=0.8)
        self.t(W - MARGIN, 78, cod, 22, INK, True, 'end')
        self.t(W - MARGIN, 97, 'escala ' + escala + '  ·  A3, imprimir a 100%', 8.4, INK_SOFT, False, 'end')
        d.line(MARGIN, 112, W - MARGIN, 112, RULE, 1.0)
        d.line(MARGIN, 928, W - MARGIN, 928, RULE, 1.0)
        self.t(MARGIN, 944, 'Cotas em mm, em faces acabadas; nível ±0 = piso pronto. Medidas de 14/11/2026 informadas pelo cliente + modelo R95. '
               'Conferir em obra depois da demolição e antes de cortar qualquer peça.', 7.6, INK_SOFT)
        self.t(MARGIN, 956, 'Orientação de escopo, não laudo: instalações, estrutura e impermeabilização pedem responsável técnico em obra.', 7.6, INK_SOFT)
        self.t(MARGIN, 975, 'MAXHAUS 81  ·  JOÃO BALDINATO 109  ·  BANHEIRO  ·  ' + caderno, 8.4, DEMO, True, ls=0.5)
        self.t(W - MARGIN, 975, cod + '   ·   ' + EMISSAO, 8.4, INK_SOFT, False, 'end')

    # texto em corpo real (a base reduz 10%)
    def t(self, x, y, s, size=8.0, cor=INK, bold=False, anchor='start', ls=None, rot=None):
        self.d.txt(x, y, s, size / bm.ESCALA_FONTE, cor, 'bold' if bold else 'normal', anchor, ls, rot)

    def par(self, x, y, w, blocos, size=8.4, lh=12.0, gap=7.0):
        """blocos: (titulo, texto) — quebra automática. Devolve o y final."""
        for tit, txt in blocos:
            if tit:
                for ln in quebra(tit, w, size, True):
                    self.t(x, y, ln, size, INK, True)
                    y += lh
            for ln in quebra(txt, w, size):
                self.t(x, y, ln, size, INK_SOFT)
                y += lh
            y += gap
        return y

    def tab(self, x, y, w, cols, linhas, titulo=None, alt=17.0, size=7.8):
        """cols: (rótulo, fração, alinhamento). Células longas quebram em duas linhas."""
        d = self.d
        if titulo:
            self.t(x, y - 8, titulo, 7.4, INK_SOFT, True, ls=1.0)
        d.rect(x, y, w, alt, fill=K12)
        xs, acc = [], x
        for (_, f, _) in cols:
            xs.append(acc)
            acc += f * w
        for (rot, f, al), xx in zip(cols, xs):
            cw = f * w
            self.t(xx + (6 if al == 'start' else cw - 6), y + alt * 0.66, rot, size - 0.4, INK_SOFT, True, al)
        y += alt
        for i, ln in enumerate(linhas):
            cel = []
            for (rot, f, al), v in zip(cols, ln):
                cel.append(quebra(str(v), f * w - 12, size) or [''])
            n = max(len(c) for c in cel)
            hh = alt + (n - 1) * (size + 2.4)
            if i % 2:
                d.rect(x, y, w, hh, fill=K04)
            for j, ((rot, f, al), xx, c) in enumerate(zip(cols, xs, cel)):
                cw = f * w
                for k, s in enumerate(c):
                    self.t(xx + (6 if al == 'start' else cw - 6), y + alt * 0.66 + k * (size + 2.4), s, size,
                           INK if j == 0 else INK_SOFT, j == 0, al)
            y += hh
            d.line(x, y, x + w, y, K20, 0.5)
        return y

    def passos(self, x, y, w, itens, size=8.4, lh=12.0):
        """itens: (titulo, texto, portão?) numerados."""
        d = self.d
        for i, (tit, txt, portao) in enumerate(itens, 1):
            d.circle(x + 8, y - 3, 8, fill=AMARELO if portao else BG, stroke=K, sw=1.0)
            self.t(x + 8, y, str(i), 7.4, K, True, 'middle')
            self.t(x + 24, y, tit, size, INK, True)
            y += lh
            for ln in quebra(txt, w - 24, size):
                self.t(x + 24, y, ln, size, INK_SOFT)
                y += lh
            y += 5
        return y

    def cota_h(self, x0, x1, y, rot, size=7.0, cor=K70):
        d = self.d
        d.line(x0, y, x1, y, cor, 0.6)
        for x in (x0, x1):
            d.line(x - 2.5, y + 2.5, x + 2.5, y - 2.5, cor, 0.8)
            d.line(x, y - 4, x, y + 4, cor, 0.4)
        self.t((x0 + x1) / 2.0, y - 3.5, rot, size, cor, False, 'middle')

    def cota_v(self, x, y0, y1, rot, size=7.0, cor=K70, lado=-1):
        d = self.d
        d.line(x, y0, x, y1, cor, 0.6)
        for y in (y0, y1):
            d.line(x - 2.5, y + 2.5, x + 2.5, y - 2.5, cor, 0.8)
            d.line(x - 4, y, x + 4, y, cor, 0.4)
        self.t(x + lado * 4.0, (y0 + y1) / 2.0, rot, size, cor, False, 'middle', rot=-90)

    def cadeia_h(self, P, xs, y_mm, off, size=6.6):
        for a, b in zip(xs, xs[1:]):
            pa, pb = P(a, y_mm), P(b, y_mm)
            self.cota_h(pa[0], pb[0], pa[1] + off, '%d' % round(b - a), size)

    def cadeia_v(self, P, ys, x_mm, off, size=6.6):
        for a, b in zip(ys, ys[1:]):
            pa, pb = P(x_mm, a), P(x_mm, b)
            self.cota_v(pa[0] + off, pa[1], pb[1], '%d' % round(b - a), size)

    def legenda(self, x, y, itens):
        d = self.d
        for tipo, cor, txt in itens:
            if tipo == 'fill':
                d.rect(x, y - 8, 14, 10, fill=cor, stroke=K45, sw=0.6)
            elif tipo == 'line':
                d.line(x, y - 3, x + 14, y - 3, cor, 2.2)
            elif tipo == 'dash':
                d.path('M%.1f %.1f L%.1f %.1f' % (x, y - 3, x + 14, y - 3), stroke=cor, sw=1.6, dash='4 3')
            elif tipo == 'dot':
                d.circle(x + 7, y - 3, 4.5, fill=cor, stroke=K, sw=0.9)
            self.t(x + 20, y, txt, 7.8, INK)
            x += 44 + larg_txt(txt, 7.8) * 1.05
        return x

    # ---- planta ----------------------------------------------------------------
    def planta(self, ox, oy, N, objetos=True, box_cor=CIANO18, piso=K04, rotulos=True, porta=True):
        """Desenha a casca do banheiro em 1:N. (ox, oy) = canto interno noroeste.
        Devolve P(x_mm, y_mm) -> ponto da folha e s (unidades por mm)."""
        d = self.d
        s = MM / N

        def P(x, y):
            return (ox + x * s, oy + y * s)

        def R(x0, y0, x1, y1, **k):
            a, b = P(x0, y0), P(x1, y1)
            d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], **k)

        t = PAREDE
        R(-t, -t, LARG + t, COMP + t, fill=K)
        R(0, 0, LARG, COMP, fill=piso)
        if box_cor:
            R(0, BOX_Y, LARG, COMP, fill=box_cor)
        R(*AT, fill=K20, stroke=K, sw=0.8)
        c = P((AT[0] + AT[2]) / 2.0, (AT[1] + AT[3]) / 2.0)
        if rotulos:
            self.t(c[0] + 2.5, c[1], 'AT-B', 6.6, K, True, 'middle', rot=-90)
        # vão da porta
        R(LARG, PORTA[0], LARG + t, PORTA[1], fill=BG)
        a, b = P(LARG, PORTA[0]), P(LARG + t, PORTA[0])
        d.line(a[0], a[1], b[0], b[1], K, 0.8)
        a, b = P(LARG, PORTA[1]), P(LARG + t, PORTA[1])
        d.line(a[0], a[1], b[0], b[1], K, 0.8)
        if porta:   # folha aberta para fora, dobradiça norte, giro anti-horário
            h = P(LARG + t, PORTA[0])
            r = 800 * s
            d.line(h[0], h[1], h[0] + r, h[1], K, 1.6)
            d.path('M%.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f' % (h[0] + r, h[1], r, r, h[0], h[1] + r),
                   stroke=K45, sw=0.7, dash='4 3')
            if rotulos:
                self.t(h[0] + r * 0.45, h[1] + r * 0.45, 'P02', 7.4, K, True, 'middle')
        # vidro do box
        a, b = P(0, BOX_Y), P(LARG, BOX_Y)
        d.line(a[0], a[1], b[0], b[1], CIANO, 2.6)
        if objetos:
            R(*BANC, fill=BRANCO, stroke=K, sw=1.0)
            c = P(BANC[2] / 2.0, CUBA_Y)
            d.rect(c[0] - 150 * s, c[1] - 210 * s, 300 * s, 420 * s, fill=BG, stroke=K45, sw=0.7)
            if rotulos:
                self.t(c[0] + 2.5, P(0, BANC[1] + 260)[1], 'B01', 7.0, K, True, 'middle', rot=-90)
            # vaso
            R(VASO_X - 200, 0, VASO_X + 200, 180, fill=BRANCO, stroke=K, sw=0.9)
            c = P(VASO_X, 440)
            d.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="0.9"/>'
                  % (c[0], c[1], 180 * s, 260 * s, BRANCO, K))
            if rotulos:
                self.t(c[0], c[1] + 3, 'VASO', 6.6, K, True, 'middle')
        if rotulos:
            c = P(LARG * 0.62, (BOX_Y + COMP) / 2.0 + 250)
            self.t(c[0], c[1], 'BOX', 8.0, INK, True, 'middle', ls=0.8)
        return P, s

    def ralos(self, P, s, rot=True):
        d = self.d
        a, b = P(R1[0], R1[1]), P(R1[2], R1[3])
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K45, stroke=K, sw=0.8)
        a2, b2 = P(R2[0], R2[1]), P(R2[2], R2[3])
        d.rect(a2[0], a2[1], b2[0] - a2[0], b2[1] - a2[1], fill=K45, stroke=K, sw=0.8)
        if rot:
            self.t(b[0] + 5, (a[1] + b[1]) / 2.0, 'R1', 7.0, K, True)
            self.t(a2[0] + (b2[0] - a2[0]) / 2.0, b2[1] + 10, 'R2', 7.0, K, True, 'middle')

    def ids_paredes(self, P):
        for pid, x, y, an, rot in (('P5', LARG / 2, -PAREDE - 70, 'middle', None),
                                   ('P1', (AT[2] + LARG) / 2, COMP + PAREDE + 130, 'middle', None),
                                   ('P4', LARG + PAREDE + 90, 2250, 'start', None),
                                   ('P3', -PAREDE - 90, 900, 'end', None),
                                   ('P2', AT[2] + 45, 2330, 'start', None),
                                   ('P6', 125, AT[1] - 40, 'middle', None)):
            c = P(x, y)
            self.t(c[0], c[1], pid, 8.4, DEMO, True, an)

    # ---- elevação paginada --------------------------------------------------------
    def elevacao(self, ox, oy, N, par, modo='linhas', indices=True):
        """Desenha a parede `par` em 1:N. (ox, oy) = canto inferior esquerdo (piso).
        modo 'linhas': peças em branco, cortes com a medida; 'numeros': só o número."""
        d = self.d
        s = MM / N

        def P(u, z):
            return (ox + u * s, oy - z * s)

        a, b = P(0, FORRO), P(par.larg, 0)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke='none')
        for h in par.furos:
            p0, p1 = P(h[0], h[3]), P(h[1], h[2])
            d.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=K07, stroke=K45, sw=0.6)
            lin = quebra(h[4], (p1[0] - p0[0]) - 8, 7.0, True)
            for i, ln in enumerate(lin):
                self.t((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0 + 3 + (i - (len(lin) - 1) / 2.0) * 9.5, ln, 7.0, K70, True, 'middle')
        fs = 6.0 if N <= 15 else 5.2
        for (n, fi, ci, frags, cheia) in par.pecas:
            if n in par.acentos:      # par Nuage 75 + 5 + 75
                u0, u1, z0, z1 = frags[0]
                for a_ in (u0, u1 - NUAGE_L):
                    p0, p1 = P(a_, z1), P(a_ + NUAGE_L, z0)
                    d.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=NUAGE_COR, stroke=K, sw=0.55)
                p0, p1 = P(u0, z1), P(u1, z0)
                cx, cy = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0 + fs * 0.36
                if modo == 'numeros':
                    self.t(cx, cy, str(n), fs, K, False, 'middle')
                else:
                    self.t(cx, cy, 'N', fs, K, True, 'middle')
                continue
            for (u0, u1, z0, z1) in frags:
                p0, p1 = P(u0, z1), P(u1, z0)
                w_, h_ = p1[0] - p0[0], p1[1] - p0[1]
                d.rect(p0[0], p0[1], w_, h_, fill=BRANCO, stroke=K, sw=0.55 if modo == 'numeros' else 0.45)
            # rótulo no maior fragmento
            u0, u1, z0, z1 = max(frags, key=lambda q: (q[1] - q[0]) * (q[3] - q[2]))
            p0, p1 = P(u0, z1), P(u1, z0)
            w_, h_ = p1[0] - p0[0], p1[1] - p0[1]
            cx, cy = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0 + fs * 0.36
            if modo == 'numeros':
                if w_ > larg_txt(str(n), fs) + 1.5 and h_ > fs:
                    self.t(cx, cy, str(n), fs, K, False, 'middle')
            elif not cheia:
                lw, lz = round(u1 - u0), round(z1 - z0)
                rot = ('%d' % lw) if lz == 155 else ('%d' % lz) if lw == 155 else '%d×%d' % (lw, lz)
                if w_ > larg_txt(rot, fs - 0.6) + 1.0 and h_ > fs:
                    self.t(cx, cy, rot, fs - 0.6, DEMO, False, 'middle')
                elif h_ > larg_txt(rot, fs - 0.6) + 1.0 and w_ > fs:
                    self.t(cx + fs * 0.3, cy - fs * 0.3, rot, fs - 0.6, DEMO, False, 'middle', rot=-90)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill='none', stroke=K, sw=1.2)
        d.line(a[0] - 6, b[1], b[0] + 6, b[1], K, 1.6)          # piso
        if indices:
            for ci, (u0, u1, cf) in enumerate(par.cols):
                c = P((u0 + u1) / 2.0, 0)
                self.t(c[0], c[1] + 9, 'C%d' % (ci + 1), 5.0, K70, False, 'middle')
            for fi, (z0, z1, rf) in enumerate(par.rows):
                c = P(par.larg, (z0 + z1) / 2.0)
                self.t(c[0] + 4, c[1] + 2, 'F%d' % (fi + 1), 5.0, K70)
        return P, s

    def salvar(self, pasta):
        return salvar(self.d, pasta, self.cod)
