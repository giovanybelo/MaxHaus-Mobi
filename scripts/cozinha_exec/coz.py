# -*- coding: utf-8 -*-
"""Cozinha + closet — geometria e paginação do piso (emissão C1, 16.11.2026).

Base: Caderno Alternativo A, REV. W, prancha 04, opção B (porcelanato acetinado no
banheiro, cozinha e closet). O porcelanato é o mesmo do banheiro: Confete 100 × 100.

Medidas em milímetros, faces de parede, origem no canto noroeste da zona:
  x = 0 na face interna da parede oeste (divisa), crescendo para leste;
  y = 0 na linha de transição com o monolítico do corredor, crescendo para sul.
Valores lidos de base_mainfloor.py (scan de 02.09.2026, 45,66 pt/m) e do
Alternativo A (parede nova R04 na face sul do banheiro).

A parede nova cozinha/closet (R04, drywall) é levantada DEPOIS do piso: o
porcelanato é uma zona única, contínua, da transição norte até a parede sul do
closet, passando por baixo da R04 e do nicho do aquecedor (AT-A).
"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(SCRIPTS, 'banheiro_exec'))
sys.path.insert(0, SCRIPTS)
import lib as wc                                   # noqa: E402  (Folha do banheiro)
import base_mainfloor as bm                        # noqa: E402
from base_mainfloor import (salvar, exportar_pdf_a3, exportar_png, W, H, MARGIN, BG, K, K70, K45,  # noqa: E402,F401
                            K20, K12, K07, K04, INK, INK_SOFT, RULE, DEMO, CIANO, CIANO18, CIANO35,
                            AMARELO, AMARELO40, BRANCO, br, folha_nova)
from lib import quebra, larg_txt, MM               # noqa: E402,F401

EMISSAO = 'C1  ·  16/11/2026'
CAD = 'CADERNO DE PAGINAÇÃO DO PISO'


def _m(xpt):
    return (xpt - 250.26) / bm.PT_PER_M * 1000.0


def _n(ypt):
    return (ypt - 284.8) / bm.PT_PER_M * 1000.0


# --- geometria (mm) -------------------------------------------------------------
LARG = round(_m(343.39))            # 2040 · face oeste → face da parede do banheiro / closet
COMP = round(_n(550.38))            # 5816 · transição norte → face da parede sul do closet
DEG_X, DEG_Y = round(_m(280.09)), round(_n(287.11))   # 653, 51 · degrau da parede no nicho da geladeira
RAIO = 700.0                        # ponta arredondada (filete de 0,70 m), tangente à face leste
FC = (LARG - RAIO, RAIO)            # centro do filete
WC_Y0 = round(_n(323.74))           # 853 · começa a parede do banheiro, na face leste
R04 = (0.0, round(_n(450.67)), LARG, round(_n(455.24)))       # 3633 → 3733 · drywall nova
PASSAGEM = (R04[3], round(_n(513.42)))                         # 3733 → 5007 · closet ↔ quarto
AT_A = (0.0, R04[3], 600.0, R04[3] + 400.0)                    # nicho do aquecedor
J06 = (round(_m(251.40)), round(_m(342.00)))                   # janela do closet, na parede sul
PAREDES_DEMOLIDAS = [(round(_m(279.36)), round(_n(430.06)), LARG, round(_n(434.63))),
                     (round(_m(279.36)), round(_n(430.06)), round(_m(283.92)), round(_n(545.96)))]
LAJE = 2620.0

# cozinha — referência de marcenaria (FO7) e da coifa CF01 (prancha 04 de teto)
GEL = (0.0, DEG_Y, 800.0, DEG_Y + 900.0)
KC1 = (0.0, DEG_Y + 920.0, 600.0, R04[1])          # bancada, do nicho da geladeira à R04
CF_Y = round(6200 + _n(124.38))    # 2687 · eixo da coifa CF01 (6,20 m na base)
COOK = (40.0, CF_Y - 295.0, 560.0, CF_Y + 295.0)   # cooktop de 60 cm (590 × 520), eixo na CF01
CUBA = (100.0, 1350.0, 500.0, 1850.0)               # cuba de referência
COIFA_L = 750.0                                     # coifa de parede, largura recomendada
TOPO_BANC = 900.0
X_CHAMINE = 300.0                                   # chaminé do aquecedor (AT-A), sob a laje
X_DUTO = 1400.0                                     # duto da coifa, sob a laje, no meio do closet
DUTO = [(300.0, CF_Y), (X_DUTO, CF_Y), (X_DUTO, COMP)]

# --- porcelanato ------------------------------------------------------------------
PECA, JUNTA, FOLGA, CORTE = 1000.0, 2.0, 3.0, 3.0   # placa, junta, folga no perímetro, disco
MOD = PECA + JUNTA


def zona():
    """Contorno da zona contínua, já com a folga de 3 mm no arco."""
    r = RAIO - FOLGA
    pts = [(0.0, DEG_Y + FOLGA), (DEG_X + FOLGA, DEG_Y + FOLGA), (DEG_X + FOLGA, 0.0), (FC[0], 0.0), (FC[0], FOLGA)]
    for i in range(1, 40):
        th = math.pi / 2 * i / 40
        pts.append((FC[0] + r * math.sin(th), FC[1] - r * math.cos(th)))
    pts += [(LARG - FOLGA, FC[1]), (LARG, FC[1]), (LARG, COMP), (0.0, COMP)]
    return pts


def area(pts):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2.0


def _corta(pts, dentro, cruza):
    out = []
    for i, p in enumerate(pts):
        q = pts[i - 1]
        if dentro(p):
            if not dentro(q):
                out.append(cruza(q, p))
            out.append(p)
        elif dentro(q):
            out.append(cruza(q, p))
    return out


def recorte(pts, x0, y0, x1, y1):
    """Sutherland–Hodgman: zona (côncava) recortada pelo retângulo da peça (convexo)."""
    def cx(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / (b[0] - a[0]))

    def cy(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / (b[1] - a[1]), yc)
    for dentro, cruza in ((lambda p: p[0] >= x0, cx(x0)), (lambda p: p[0] <= x1, cx(x1)),
                          (lambda p: p[1] >= y0, cy(y0)), (lambda p: p[1] <= y1, cy(y1))):
        if not pts:
            break
        pts = _corta(pts, dentro, cruza)
    return pts


def colunas():
    """Malha alinhada à face leste (lado visível, junto ao banheiro): duas placas inteiras
    e a faixa de ajuste a oeste, escondida sob a bancada KC1."""
    cols, x = [], LARG - FOLGA
    while x - PECA >= FOLGA:
        cols.append((x - PECA, x))
        x -= MOD
    if x - FOLGA > 1:
        cols.append((FOLGA, x))
    return list(reversed(cols))


def fiadas():
    """Fiadas a partir da transição norte (entrada): inteiras, e o corte no fundo do closet."""
    rows, y = [], FOLGA
    while y + PECA <= COMP - FOLGA:
        rows.append((y, y + PECA))
        y += MOD
    if COMP - FOLGA - y > 1:
        rows.append((y, COMP - FOLGA))
    return rows


def _no_arco(p):
    return p[0] > FC[0] + 1 and p[1] < FC[1] - 1 and abs(math.hypot(p[0] - FC[0], p[1] - FC[1]) - (RAIO - FOLGA)) < 0.5


def pecas():
    """[(id, (x0, y0, x1, y1), poligono, area_mm2, tipo, (larg, comp))]"""
    Z = zona()
    out = []
    for i, (y0, y1) in enumerate(fiadas()):
        for j, (x0, x1) in enumerate(colunas()):
            pol = recorte(list(Z), x0, y0, x1, y1)
            a = area(pol) if len(pol) > 2 else 0.0
            if a < 100:
                continue
            xs, ys = [p[0] for p in pol], [p[1] for p in pol]
            env = (max(xs) - min(xs), max(ys) - min(ys))
            cheia = abs(a - PECA * PECA) < 5
            if cheia:
                tipo = 'inteira'
            elif env[0] < 100:
                tipo = 'faixa'
            elif any(_no_arco(p) for p in pol):
                tipo = 'curva'
            elif abs(a - env[0] * env[1]) > 5:
                tipo = 'recorte'
            else:
                tipo = 'reta'
            out.append(('%s%d' % ('ABCDEFGH'[i], j + 1), (x0, y0, x1, y1), pol, a, tipo, env))
    return out


def placas(lista=None):
    """Plano de corte: cada peça de largura >= 500 sai de uma placa; as faixas saem das
    sobras das peças cortadas no comprimento. Devolve ([(placa, peça, sobra)], faixas→origem, n)."""
    lista = lista or pecas()
    plano, sobras, n = [], [], 0
    for pid, r, pol, a, tipo, env in lista:
        if env[0] >= 500:
            n += 1
            sob = PECA - env[1] - CORTE
            plano.append(('P%02d' % n, pid, sob))
            if sob >= 30:
                sobras.append(['P%02d' % n, sob])
    origem = {}
    for pid, r, pol, a, tipo, env in lista:
        if env[0] >= 500:
            continue
        for s in sorted(sobras, key=lambda s_: -s_[1]):
            if s[1] >= env[0]:
                origem[pid] = s[0]
                s[1] -= env[0] + CORTE
                break
        else:
            n += 1
            origem[pid] = 'P%02d' % n
            plano.append(('P%02d' % n, pid, PECA - env[0] - CORTE))
    return plano, origem, n


def ordenadas():
    """Peça curva: distância da borda norte da placa até o arco, ao longo da largura."""
    for pid, r, pol, a, tipo, env in pecas():
        if tipo == 'curva':
            x0, y0, x1, y1 = r
            xs = [0.0, FC[0] - x0] + [v for v in range(400, 1000, 100)] + [950.0, 975.0, 990.0, x1 - x0]
            out = []
            for u in xs:
                x = x0 + u
                yy = y0 if x <= FC[0] else FC[1] - math.sqrt(max(0.0, (RAIO - FOLGA) ** 2 - (x - FC[0]) ** 2))
                out.append((u, max(0.0, yy - y0)))
            return pid, r, out
    return None


def comprimentos():
    """Perfis de transição (m): reto (norte + abertura junto ao banheiro + passagem do closet) e arco."""
    reto = (FC[0] - DEG_X) + (WC_Y0 - RAIO) + (PASSAGEM[1] - PASSAGEM[0])
    arco = math.pi / 2 * RAIO
    perim = (COMP - DEG_Y) + LARG + DEG_X + DEG_Y + (PASSAGEM[0] - WC_Y0) + (COMP - PASSAGEM[1])
    return reto / 1000.0, arco / 1000.0, perim / 1000.0


# --- folha ------------------------------------------------------------------------------
class Folha(wc.Folha):
    """Folha A3 com o cabeçalho do caderno da cozinha (reaproveita texto e tabelas do banheiro)."""

    def __init__(self, cod, titulo, sub='', escala='sem escala'):
        self.d = folha_nova()
        self.cod = cod
        d = self.d
        self.t(MARGIN, 42, 'MAXHAUS 81  ·  COZINHA E CLOSET  ·  ' + CAD, 9.0, INK_SOFT, True, ls=1.4)
        self.t(MARGIN, 76, titulo, 24, INK, True)
        if sub:
            self.t(MARGIN, 97, sub, 9.0, INK_SOFT)
        self.t(W - MARGIN, 42, EMISSAO, 9.0, DEMO, True, 'end', ls=0.8)
        self.t(W - MARGIN, 78, cod, 22, INK, True, 'end')
        self.t(W - MARGIN, 97, 'escala ' + escala + '  ·  A3, imprimir a 100%', 8.4, INK_SOFT, False, 'end')
        d.line(MARGIN, 112, W - MARGIN, 112, RULE, 1.0)
        d.line(MARGIN, 928, W - MARGIN, 928, RULE, 1.0)
        self.t(MARGIN, 944, 'Cotas em mm, em faces de parede, sobre o scan de 02/09/2026 e o Caderno Alternativo A, REV. W, prancha 04 (opção B). '
               'Medir a zona em obra, depois da demolição e do contrapiso, antes de cortar qualquer placa.', 7.6, INK_SOFT)
        self.t(MARGIN, 956, 'Orientação de escopo, não laudo: instalações de gás e exaustão, estrutura e liberação do condomínio pedem responsável técnico em obra.', 7.6, INK_SOFT)
        self.t(MARGIN, 975, 'MAXHAUS 81  ·  JOÃO BALDINATO 109  ·  COZINHA E CLOSET  ·  ' + CAD, 8.4, DEMO, True, ls=0.5)
        self.t(W - MARGIN, 975, cod + '   ·   ' + EMISSAO, 8.4, INK_SOFT, False, 'end')

    def cadeia_v(self, P, ys, x_mm, off, size=6.6, lado=-1):
        for a, b in zip(ys, ys[1:]):
            pa, pb = P(x_mm, a), P(x_mm, b)
            self.cota_v(pa[0] + off, pa[1], pb[1], '%d' % round(b - a), size, lado=lado)

    def planta(self, ox, oy, N, piso=BRANCO, r04=True, at_a=True, marcenaria=False, rotulos=True, demolidas=False):
        """Casca da zona em 1:N; (ox, oy) = origem (face oeste × transição norte)."""
        d = self.d
        s = MM / N

        def P(x, y):
            return (ox + x * s, oy + y * s)

        def R(x0, y0, x1, y1, **k):
            a, b = P(x0, y0), P(x1, y1)
            d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], **k)

        # monolítico em volta (corredor, sala de TV, quarto)
        R(DEG_X, -420, LARG + 520, WC_Y0, fill=K07)
        R(LARG, PASSAGEM[0], LARG + 520, COMP, fill=K07)
        d.path(bm.path_d([P(*p) for p in zona()]), fill=piso, stroke=K, sw=0.5)
        if demolidas:
            for (x0, y0, x1, y1) in PAREDES_DEMOLIDAS:
                R(x0, y0, x1, y1, fill=K12, stroke=K45, sw=0.5, dash='3 2')
        # paredes
        for (x0, y0, x1, y1) in [(-100, -49, 0, COMP + 100), (-100, -49, DEG_X, DEG_Y),
                                 (DEG_X - 100, -420, DEG_X, DEG_Y), (-100, COMP, LARG + 520, COMP + 100),
                                 (LARG, WC_Y0, LARG + 100, PASSAGEM[0]), (LARG, WC_Y0, LARG + 520, WC_Y0 + 100),
                                 (LARG, PASSAGEM[1], LARG + 100, COMP)]:
            R(x0, y0, x1, y1, fill=K)
        R(J06[0], COMP + 30, J06[1], COMP + 70, fill=BRANCO, stroke=K45, sw=0.6)
        # transição com o monolítico
        trans = [P(DEG_X, 0), P(FC[0], 0)] + [P(FC[0] + RAIO * math.sin(math.pi / 2 * i / 30),
                                                FC[1] - RAIO * math.cos(math.pi / 2 * i / 30)) for i in range(31)] + [P(LARG, WC_Y0)]
        d.path(bm.path_d(trans, close=False), stroke=DEMO, sw=2.2)
        a, b = P(LARG, PASSAGEM[0]), P(LARG, PASSAGEM[1])
        d.line(a[0], a[1], b[0], b[1], DEMO, 2.2)
        if marcenaria:
            for r_, nome in ((GEL, 'geladeira'), (KC1, 'KC1 bancada'), (COOK, 'cooktop'), (CUBA, 'cuba')):
                R(*r_, fill='none', stroke=K45, sw=0.7, dash='4 2')
            for r_, nome in ((GEL, 'geladeira'), (KC1, 'bancada KC1'), (COOK, 'cooktop'), (CUBA, 'cuba')):
                c = P((r_[0] + r_[2]) / 2, (r_[1] + r_[3]) / 2 + (0 if nome != 'bancada KC1' else -280))
                self.t(c[0], c[1] + 2, nome, 6.2, K70, False, 'middle', rot=-90 if nome == 'bancada KC1' else None)
        if r04:
            R(*R04, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
            c = P(40, R04[1])
            self.t(c[0], c[1] - 3, 'R04 · drywall depois, sobre o piso', 6.4, DEMO, True)
        if at_a:
            R(*AT_A, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
            c = P(AT_A[2] / 2, (AT_A[1] + AT_A[3]) / 2)
            self.t(c[0], c[1] + 2, 'AT-A', 6.6, DEMO, True, 'middle')
        if rotulos:
            for (x, y, t) in ((LARG + 260, -200, 'CORREDOR'), (LARG + 260, 420, 'SALA DE TV'), (LARG + 330, 2300, 'BANHEIRO'),
                              (LARG + 270, 4400, 'QUARTO'), (FC[0] - 300, -230, 'monolítico')):
                c = P(x, y)
                self.t(c[0], c[1], t, 6.6, K70, t != 'monolítico', 'middle')
        return P, s
