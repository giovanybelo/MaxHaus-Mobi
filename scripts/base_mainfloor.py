# -*- coding: utf-8 -*-
"""
Base gráfica do caderno MaxHaus MainFloor.

Geometria extraída do levantamento "MaxHaus_Mainfloor.pdf" (scan de 02.09.2026,
pág. 2): paredes, aberturas e polígonos de ambiente foram lidos do vetor
original em pontos PDF e convertidos para metros pela escala 45,66 pt/m,
conferida contra as cotas gerais do pavimento (7,85 m x 9,43 m).

Dois estados convivem no caderno:
  ESTADO EXISTENTE (Prancha 02) — o fundo do box é um pano de vidro chão-teto,
  ponta a ponta (o scan o leu como vão) e a drywall entre sala e quarto não tem
  porta.
  ESTADO PROPOSTO (Pranchas 03, 04 e 05) — o pano de vidro sai e entra uma
  parede fechando o box; a drywall é refeita com uma porta de 1,00 x 2,30 m;
  a porta do banheiro passa a abrir para o lado do quarto.

Demais decisões do cliente embutidas na base:
  · o teto é laje de concreto aparente — não há forro, salvo no banheiro;
  · a área da piscina do pavimento superior está centrada em (6,13 / 3,14) m,
    medida do canto noroeste, e condiciona luz, ar e furação da laje.

Todas as pranchas do caderno fecham em A3 deitado (420 x 297 mm).
"""
import math
import os

# ---------------------------------------------------------------------------
# 1. GEOMETRIA (pontos PDF do scan)
# ---------------------------------------------------------------------------
ORIGIN_X, ORIGIN_Y = 245.7, 124.38
PT_PER_M = 45.66
BUILDING_W, BUILDING_H = 7.85, 9.43

def mx(v): return (v - ORIGIN_X) / PT_PER_M
def my(v): return (v - ORIGIN_Y) / PT_PER_M
def px_(m_): return m_ * PT_PER_M + ORIGIN_X      # metro -> pt (eixo x)
def py_(m_): return m_ * PT_PER_M + ORIGIN_Y      # metro -> pt (eixo y)

ROOMS = {
    'jantar': dict(label='JANTAR', area=5.90, lx=525.0, ly=165.0,
        poly=[(448.4,126.7),(601.7,126.7),(601.7,211.2),(448.4,211.2)]),
    'sala': dict(label='SALA', area=23.00, lx=508.0, ly=285.0,
        poly=[(345.7,211.2),(601.7,211.2),(601.7,432.3),(415.6,432.3),
              (415.6,327.9),(345.7,327.9)]),
    'cozinha': dict(label='COZINHA', area=8.90, lx=297.0, ly=368.0,
        poly=[(277.8,211.2),(345.7,211.2),(345.7,432.3),(248.0,432.3),
              (248.0,284.8),(277.8,284.8)]),
    'banheiro': dict(label='BANHEIRO', area=3.80, lx=380.6, ly=360.0,
        poly=[(345.7,327.9),(415.6,327.9),(415.6,453.0),(345.7,453.0)]),
    'closet': dict(label='CLOSET', area=5.30, lx=314.0, ly=498.0,
        poly=[(248.0,432.3),(345.7,432.3),(345.7,552.7),(248.0,552.7)]),
    'quarto': dict(label='QUARTO', area=13.40, lx=505.0, ly=500.0,
        poly=[(415.6,432.3),(601.7,432.3),(601.7,552.7),(345.7,552.7),
              (345.7,453.0),(415.6,453.0)]),
}
ROOM_ORDER = ['jantar','sala','cozinha','closet','quarto','banheiro']

WALLS = [
    (446.11,124.38,604.03,128.94), (275.52,208.91,450.68,213.47),
    (275.52,208.91,280.09,287.11), (245.70,282.54,280.09,287.11),
    (279.36,430.06,345.67,434.63), (345.67,550.38,604.03,554.94),
    (343.39,432.34,347.96,455.24), (343.39,325.65,347.96,432.34),
    (415.61,430.06,601.74,434.63),
    (413.33,325.65,417.90,432.34), (599.46,432.34,604.03,554.94),
    (279.36,430.06,283.92,545.96), (245.70,550.38,345.67,554.94),
    (343.39,513.42,347.96,552.66), (446.11,124.38,450.68,213.47),
    (413.33,432.34,417.90,455.24), (599.46,124.38,604.03,432.34),
    (245.70,282.54,250.26,554.94), (343.39,325.65,417.90,330.22),
]
# fundo do box no estado existente: pano de vidro chão-teto, ponta a ponta.
# Será derrubado e substituído por parede (PAREDE_FUNDO_BOX).
VIDRO_BOX = (343.39, 450.67, 417.90, 455.24)
PAREDE_FUNDO_BOX = (343.39, 450.67, 417.90, 455.24)
# drywall sala/quarto: demolida e refeita, agora com porta
DRYWALL_SALA_QUARTO = (415.61, 430.06, 601.74, 434.63)
PORTA_NOVA = (416.90, 430.06, 462.50, 434.63)      # 1,00 x 2,30 m
PORTA_ENTRADA_H = 2.30                              # altura de referência
# parede do jantar / sob a escada: revestimento retirado e preparo para pintura
PAREDE_ESCADA_JANTAR = (446.11, 124.38, 450.68, 213.47)
PAREDE_SOB_ESCADA = (321.40, 208.91, 459.40, 213.47)

DOOR_ENTRADA = dict(rect=(275.52,220.10,280.09,259.20), hinge='n', leaf='e')
DOOR_BANHO   = dict(rect=(413.33,351.00,417.90,387.30), hinge='s', leaf='e')
JANELAS = [
    (599.46,142.50,604.03,193.20), (599.46,215.00,604.03,300.80),
    (599.46,348.00,604.03,394.40), (599.46,455.70,604.03,509.80),
    (251.40,550.38,342.00,554.94), (354.00,550.38,408.10,554.94),
]
ESCADA = dict(rect=(321.40,213.47,459.40,251.70), degraus=11)

# --- elementos existentes lidos do scan (para alvos de demolição) -----------
BANCADA_WC   = (347.96, 352.00, 366.00, 380.00)   # bancada + espelho (parede oeste)
BOX_WC       = (347.96, 408.20, 413.33, 450.67)   # box do banheiro
VIDRO_BOX_INT= (347.96, 408.20, 413.33, 411.00)   # vidro interno do box (manter)
CANTO_ALEMAO = (450.68, 128.94, 599.46, 145.00)   # banco de canto do jantar

# --- ponta em curva da cozinha (prancha de pisos) ---------------------------
CURVA_CX, CURVA_CY = 277.8, 325.65
CURVA_RX, CURVA_RY = 67.90, 66.45
PORTA_QUINA = (277.8, 259.20)
CURVA_FIM   = (345.7, 325.65)

def arco_pts(n=28, invertido=False):
    pts = []
    for i in range(n + 1):
        th = math.radians(90.0 * (1.0 - i / float(n)))
        pts.append((CURVA_CX + CURVA_RX * math.cos(th),
                    CURVA_CY - CURVA_RY * math.sin(th)))
    return list(reversed(pts)) if invertido else pts

# --- área da piscina do pavimento superior ---------------------------------
# 1,92 x 3,00 m, centrada no cruzamento marcado pelo cliente (6,13 / 3,14 m).
PISCINA_CX, PISCINA_CY = 6.13, 3.14
PISCINA_W, PISCINA_H = 1.92, 3.00
AREA_PISCINA = (px_(PISCINA_CX - PISCINA_W / 2), py_(PISCINA_CY - PISCINA_H / 2),
                px_(PISCINA_CX + PISCINA_W / 2), py_(PISCINA_CY + PISCINA_H / 2))
AREA_PISCINA_M2 = PISCINA_W * PISCINA_H
AREA_TETO = AREA_PISCINA          # compatibilidade
AREA_TETO_M2 = AREA_PISCINA_M2

# ---------------------------------------------------------------------------
# 2. PALETA
# ---------------------------------------------------------------------------
BG        = '#faf8f4'
INK       = '#22303c'
INK_SOFT  = '#6b7480'
RULE      = '#cbc8c0'
WALL      = '#5b6472'
GHOST     = '#9aa2ab'
GLASS     = '#7fb0c4'
WOOD      = '#c98a4b'
WOOD_LINE = '#9c6530'
MONO      = '#dcd9d2'
MONO_LINE = '#b9b5ab'
WET       = '#d7e7ef'
WET_LINE  = '#6f9bb0'
JOINT     = '#1f2c38'
RED       = '#b23a2f'
DEMO      = '#c2443a'
KEEP      = '#2e7d6b'
NEW       = '#1f6f9c'
EXIST     = '#8a8f96'
AIR       = '#4c8fa8'

# ---------------------------------------------------------------------------
# 3. FOLHA A3 E PRIMITIVAS
# ---------------------------------------------------------------------------
W, H = 1400, 990                      # proporção A3 deitado
FONT = "'IBM Plex Sans', Helvetica, Arial, sans-serif"
MARGIN = 48

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def br(v, casas=2):
    return (('%.' + str(casas) + 'f') % v).replace('.', ',')

class Draw(object):
    def __init__(self):
        self.o = []
        self.org = (0.0, 0.0)
        self.S = 55.0
    # --- primitivas ---------------------------------------------------------
    def add(self, s): self.o.append(s)
    def txt(self, x, y, t, size=10, fill=INK, weight='normal', anchor='start', ls=None):
        a = ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" fill="%s" '
             'font-weight="%s" text-anchor="%s"' % (x, y, FONT, size, fill, weight, anchor))
        if ls: a += ' letter-spacing="%.2f"' % ls
        self.add(a + '>' + esc(t) + '</text>')
    def line(self, x1, y1, x2, y2, stroke, w=1.0, opacity=None, cap=None):
        a = ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"'
             % (x1, y1, x2, y2, stroke, w))
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        if cap: a += ' stroke-linecap="%s"' % cap
        self.add(a + '/>')
    def rect(self, x, y, w_, h_, fill='none', stroke=None, sw=1.0, opacity=None, dash=None):
        a = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"' % (x, y, w_, h_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    def circle(self, x, y, r, fill='none', stroke=None, sw=1.0, opacity=None):
        a = '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"' % (x, y, r, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    def path(self, d_, fill='none', stroke=None, sw=1.0, opacity=None, dash=None):
        a = '<path d="%s" fill="%s"' % (d_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    # --- transformação planta ----------------------------------------------
    def set_plan(self, ox, oy, S):
        self.org = (ox, oy); self.S = S
    def P(self, x_pt, y_pt):
        return (self.org[0] + mx(x_pt) * self.S, self.org[1] + my(y_pt) * self.S)
    def PM(self, x_m, y_m):
        return (self.org[0] + x_m * self.S, self.org[1] + y_m * self.S)
    def R(self, r):
        a = self.P(r[0], r[1]); b = self.P(r[2], r[3])
        return (a[0], a[1], b[0] - a[0], b[1] - a[1])

def path_d(pp, close=True):
    d = ['%s%.2f %.2f' % ('M' if i == 0 else 'L', p[0], p[1]) for i, p in enumerate(pp)]
    return ' '.join(d) + (' Z' if close else '')

def bbox(pp):
    xs = [p[0] for p in pp]; ys = [p[1] for p in pp]
    return min(xs), min(ys), max(xs), max(ys)

def _spans(v):
    v.sort()
    return [(v[i], v[i + 1]) for i in range(0, len(v) - 1, 2)]

def spans_at_y(pp, y):
    xs = []
    n = len(pp)
    for i in range(n):
        x1, y1 = pp[i]; x2, y2 = pp[(i + 1) % n]
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return _spans(xs)

def spans_at_x(pp, x):
    ys = []
    n = len(pp)
    for i in range(n):
        x1, y1 = pp[i]; x2, y2 = pp[(i + 1) % n]
        if (x1 <= x < x2) or (x2 <= x < x1):
            ys.append(y1 + (x - x1) * (y2 - y1) / (x2 - x1))
    return _spans(ys)

# ---------------------------------------------------------------------------
# 4. DESENHO DA PLANTA
# ---------------------------------------------------------------------------
def fundo_ambientes(d, cor=MONO, opacity=1.0):
    for k in ROOM_ORDER:
        d.path(path_d([d.P(x, y) for x, y in ROOMS[k]['poly']]), fill=cor, opacity=opacity)

def paredes(d, estado='novo'):
    """estado='existente' mantém o fundo do box em vidro; 'novo' o fecha em parede."""
    for r in WALLS:
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=WALL)
    if estado == 'novo':
        x, y, w_, h_ = d.R(PAREDE_FUNDO_BOX)
        d.rect(x, y, w_, h_, fill=WALL)

def vidro_box(d, rotulo=True):
    """Pano de vidro chão-teto no fundo do box, ponta a ponta."""
    x, y, w_, h_ = d.R(VIDRO_BOX)
    d.rect(x - 0.3, y - 0.3, w_ + 0.6, h_ + 0.6, fill=BG)
    d.rect(x, y, w_, h_, fill='#e8f2f6', stroke=GLASS, sw=0.9)
    ym = y + h_ / 2.0
    d.line(x, ym, x + w_, ym, GLASS, 1.6)
    for t in (0.18, 0.5, 0.82):
        d.line(x + w_ * t, y, x + w_ * t, y + h_, GLASS, 0.7)

def vao(d, r):
    x, y, w_, h_ = d.R(r)
    d.rect(x - 0.3, y - 0.3, w_ + 0.6, h_ + 0.6, fill=BG)

def porta_horizontal(d, rect, hinge='w', swing='s'):
    """Porta em parede horizontal: dobradiça a oeste/leste, abrindo para norte/sul."""
    vao(d, rect)
    x, y, w_, h_ = d.R(rect)
    leaf = w_
    hx = x if hinge == 'w' else x + w_
    hy = y + h_ if swing == 's' else y
    ex = hx + (leaf if hinge == 'w' else -leaf)
    ty = hy + (leaf if swing == 's' else -leaf)
    d.line(hx, hy, hx, ty, WALL, 1.4)
    flag = 1 if (hinge == 'w') == (swing == 'n') else 0
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 %d %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>' % (hx, ty, leaf, leaf, flag, ex, hy, WALL))


def porta(d, door):
    vao(d, door['rect'])
    x, y, w_, h_ = d.R(door['rect'])
    leaf = h_
    hx = x + w_ if door['leaf'] == 'e' else x
    hy = y if door['hinge'] == 'n' else y + h_
    ex = hx + (leaf if door['leaf'] == 'e' else -leaf)
    ty = hy + (leaf if door['hinge'] == 'n' else -leaf)
    d.line(hx, hy, ex, hy, WALL, 1.4)
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 %d %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>'
          % (ex, hy, leaf, leaf, 1 if door['hinge'] == 'n' else 0, hx, ty, WALL))

def janelas(d):
    for r in JANELAS:
        vao(d, r)
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill='none', stroke=WALL, sw=0.9)
        if w_ > h_:
            d.line(x, y + h_ / 2, x + w_, y + h_ / 2, WALL, 0.9)
        else:
            d.line(x + w_ / 2, y, x + w_ / 2, y + h_, WALL, 0.9)

def escada(d, rotulo=True):
    x, y, w_, h_ = d.R(ESCADA['rect'])
    d.rect(x, y, w_, h_, fill='none', stroke=WALL, sw=0.9, opacity=0.85)
    n = ESCADA['degraus']
    for i in range(1, n):
        xx = x + w_ * i / float(n)
        d.line(xx, y, xx, y + h_, WALL, 0.7, opacity=0.6)
    if rotulo:
        d.txt(x + w_ / 2, y + h_ / 2 + 3, 'ESCADA', 6.6, INK_SOFT, 'bold', 'middle', ls=0.8)

def rotulos(d, areas=True, size=8.8):
    for k in ROOM_ORDER:
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], size, INK, 'bold', 'middle', ls=0.9)
        if areas:
            d.txt(lx, ly + 10, br(r['area']) + ' m²', size - 1.1, INK_SOFT, 'normal', 'middle')

def tracejado(d, pts_pt, stroke=JOINT, w=1.7, dash=6.0, gap=4.2, halo=True):
    pp = [d.P(x, y) for x, y in pts_pt]
    if halo:
        d.path(path_d(pp, close=False), stroke=BG, sw=w + 1.7, opacity=0.9)
    resto, on = 0.0, True
    for i in range(len(pp) - 1):
        (ax, ay), (bx, by) = pp[i], pp[i + 1]
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-9: continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0.0
        while t < L:
            passo = (dash if on else gap) - resto
            t2 = min(t + passo, L)
            if on:
                d.line(ax + ux * t, ay + uy * t, ax + ux * t2, ay + uy * t2, stroke, w, cap='butt')
            if t2 - t >= passo - 1e-9:
                on = not on; resto = 0.0
            else:
                resto += t2 - t
            t = t2

def escala(d, y):
    ox = d.org[0]
    S = d.S
    for i in range(2):
        d.rect(ox + i * S, y, S, 5, fill=(INK if i % 2 == 0 else BG), stroke=INK, sw=0.8)
    for i in range(3):
        d.txt(ox + i * S, y + 16, str(i), 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(ox + 2 * S + 13, y + 16, 'm   (base do scan)', 7.2, INK_SOFT)

def planta_base(d, estado='novo', fundo=True, com_rotulos=True, areas=True):
    if fundo:
        fundo_ambientes(d, MONO, 0.55)
    paredes(d, estado)
    janelas(d)
    if estado == 'existente':
        vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    if estado == 'novo':
        porta_horizontal(d, PORTA_NOVA, hinge='w', swing='s')
    escada(d)
    if com_rotulos:
        rotulos(d, areas=areas)

# ---------------------------------------------------------------------------
# 5. BLOCOS DA FOLHA
# ---------------------------------------------------------------------------
def cabecalho(d, titulo, subtitulo, rev, dir1='', dir2=''):
    d.txt(MARGIN, 42, 'MAXHAUS / MAIN FLOOR', 10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(MARGIN, 78, titulo, 27, INK, 'bold')
    d.txt(MARGIN, 99, subtitulo, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, rev, 10.0, RED, 'bold', 'end', ls=0.8)
    if dir1: d.txt(W - MARGIN, 78, dir1, 10.5, INK, 'bold', 'end')
    if dir2: d.txt(W - MARGIN, 99, dir2, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)

def rodape(d, nota1, nota2, prancha, rev):
    d.line(MARGIN, 922, W - MARGIN, 922, RULE, 1.0)
    if nota1: d.txt(MARGIN, 940, nota1, 8.3, INK_SOFT)
    if nota2: d.txt(MARGIN, 953, nota2, 8.3, INK_SOFT)
    d.txt(MARGIN, 975, 'ESTUDO PRELIMINAR — NÃO LIBERADO PARA EXECUÇÃO   |   11/09/2026',
          9.0, RED, 'bold', ls=0.5)
    d.txt(W - MARGIN, 975, '%s   ·   %s' % (prancha, rev), 9.0, INK_SOFT, 'normal', 'end')

def legenda(d, itens, x, y, largura=None, col=1):
    """itens: (tipo, cor, texto). tipo: 'fill' | 'line' | 'dash' | 'dot' | 'ghost'."""
    cx, cy = x, y
    for (tipo, cor, texto) in itens:
        passo = 30 + len(texto) * 4.9
        if col == 1 and largura and cx > x and (cx + passo - 30) > (x + largura):
            cx, cy = x, cy + 17      # quebra de linha da legenda
        if tipo == 'fill':
            d.rect(cx, cy - 8, 15, 10, fill=cor, stroke=MONO_LINE, sw=0.7)
        elif tipo == 'ghost':
            d.rect(cx, cy - 8, 15, 10, fill='none', stroke=cor, sw=0.9, dash='3 2.5')
        elif tipo == 'line':
            d.line(cx, cy - 3, cx + 15, cy - 3, cor, 2.2)
        elif tipo == 'dash':
            for i in range(3):
                d.line(cx + i * 6, cy - 3, cx + i * 6 + 4, cy - 3, cor, 1.8, cap='butt')
        elif tipo == 'dot':
            d.circle(cx + 7, cy - 3, 4.2, fill='none', stroke=cor, sw=1.4)
        elif tipo == 'dotf':
            d.circle(cx + 7, cy - 3, 4.2, fill=cor, stroke=cor, sw=1.0)
        d.txt(cx + 22, cy, texto, 8.8, INK)
        if col == 1:
            cx += passo
        else:
            cy += 16
    return (cx, cy)

def tabela(d, x, y, largura, colunas, linhas, titulo=None, zebra=True):
    """colunas: [(rotulo, largura_relativa, alinhamento)]"""
    if titulo:
        d.txt(x, y - 9, titulo, 8.0, INK_SOFT, 'bold', ls=1.2)
    larguras = [c[1] for c in colunas]
    total = float(sum(larguras))
    xs, acc = [], 0.0
    for lw in larguras:
        xs.append(x + acc / total * largura)
        acc += lw
    d.rect(x, y, largura, 20, fill='#eceae4')
    for i, (rot, lw, al) in enumerate(colunas):
        tx = xs[i] + 8 if al == 'start' else (xs[i] + (xs[i + 1] - xs[i] if i + 1 < len(xs) else largura - (xs[i] - x)) - 8)
        d.txt(tx, y + 13.5, rot, 8.2, INK_SOFT, 'bold', al, ls=0.6)
    ry = y + 20
    for n, linha in enumerate(linhas):
        alt = 22 if not isinstance(linha, tuple) or len(linha) < 4 else linha[3]
        if zebra and n % 2 == 1:
            d.rect(x, ry, largura, 22, fill='#f2f0ea')
        for i, (rot, lw, al) in enumerate(colunas):
            val = linha[i] if i < len(linha) else ''
            tx = xs[i] + 8 if al == 'start' else (xs[i] + (xs[i + 1] - xs[i] if i + 1 < len(xs) else largura - (xs[i] - x)) - 8)
            peso = 'bold' if i == 0 else 'normal'
            cor = INK if i == 0 else INK_SOFT
            d.txt(tx, ry + 14.5, val, 8.6, cor, peso, al)
        d.line(x, ry + 22, x + largura, ry + 22, RULE, 0.6, opacity=0.8)
        ry += 22
    return ry

def paragrafos(d, x, y, largura, blocos, size=8.6, lh=13.0, gap=9.0):
    """blocos: lista de listas de linhas já quebradas."""
    yy = y
    for bloco in blocos:
        for ln in bloco:
            if ln.startswith('**'):
                d.txt(x, yy, ln[2:], size, INK, 'bold')
            else:
                d.txt(x, yy, ln, size, INK_SOFT)
            yy += lh
        yy += gap
    return yy

# ---------------------------------------------------------------------------
# 6. SAÍDA
# ---------------------------------------------------------------------------
def svg(d):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            % (W, H, W, H)) + '\n'.join(d.o) + '\n</svg>'

def folha_nova():
    d = Draw()
    d.rect(0, 0, W, H, fill=BG)
    return d

def salvar(d, pasta, nome_base):
    if not os.path.isdir(pasta):
        os.makedirs(pasta)
    caminho_svg = os.path.join(pasta, nome_base + '.svg')
    with open(caminho_svg, 'w') as f:
        f.write(svg(d))
    return caminho_svg

def exportar_pdf_a3(svgs, pdf_path, titulo):
    """Fecha uma ou mais folhas em A3 deitado (420 x 297 mm)."""
    import pymupdf
    folha = pymupdf.paper_rect('a3-l')
    saida = pymupdf.open()
    for caminho in svgs:
        src = pymupdf.open(caminho)
        doc = pymupdf.open('pdf', src.convert_to_pdf())
        pagina = saida.new_page(width=folha.width, height=folha.height)
        pagina.show_pdf_page(pagina.rect, doc, 0)
    saida.set_metadata({'title': titulo,
                        'subject': 'Estudo preliminar — A3, 420 x 297 mm',
                        'keywords': 'MaxHaus, MainFloor, estudo preliminar'})
    saida.save(pdf_path)
    return pdf_path

def exportar_png(svg_path, png_path, dpi=170):
    import pymupdf
    pymupdf.open(svg_path)[0].get_pixmap(dpi=dpi).save(png_path)
    return png_path
