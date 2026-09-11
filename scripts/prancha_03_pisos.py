# -*- coding: utf-8 -*-
"""
Prancha 03 — MaxHaus MainFloor | Cumaru ou monolítico (REV. C)

Geometria extraída do levantamento "MaxHaus_Mainfloor.pdf" (scan, pág. 2):
paredes, aberturas e polígonos de ambiente foram lidos do vetor original em
pontos PDF e convertidos para metros pela escala 45,66 pt/m — conferida contra
as cotas gerais do pavimento (7,85 m x 9,43 m).

REV. B  cozinha e closet monolíticos também na proposta de cumaru; banheiro
        fora do monolítico; piso desenhado contínuo, sem recorte de mobiliário.
REV. C  · a cozinha vai até a quina da porta de entrada e a ponta do monolítico
          é resolvida em curva (arco de raio 1,49 m tangente à parede oeste);
        · parede do box do banheiro fechada — a abertura sul do scan era o
          vidro do box, não um vão;
        · parede de drywall entre sala e quarto retirada (indicada em fantasma).

Saídas: pranchas/prancha-03-cumaru-ou-monolitico.svg  (prancha completa)
        pranchas/planta-opcao-a.svg, planta-opcao-b.svg  (plantas isoladas)
"""
import math
import os

# ---------------------------------------------------------------------------
# 1. BASE DO SCAN — unidades em pontos PDF da pág. 2 do levantamento
# ---------------------------------------------------------------------------
ORIGIN_X, ORIGIN_Y = 245.7, 124.38    # canto externo noroeste do pavimento
PT_PER_M = 45.66                       # 358,33 pt / 7,85 m = 430,56 pt / 9,43 m
BUILDING_W, BUILDING_H = 7.85, 9.43

def mx(v): return (v - ORIGIN_X) / PT_PER_M
def my(v): return (v - ORIGIN_Y) / PT_PER_M

# --- ambientes (faces internas, em pt) --------------------------------------
ROOMS = {
    'jantar': dict(
        label='JANTAR', area=5.90, lx=525.0, ly=165.0,
        poly=[(448.4,126.7),(601.7,126.7),(601.7,211.2),(448.4,211.2)]),
    'sala': dict(
        label='SALA', area=23.00, lx=508.0, ly=285.0,
        poly=[(345.7,211.2),(601.7,211.2),(601.7,432.3),(415.6,432.3),
              (415.6,327.9),(345.7,327.9)]),
    'cozinha': dict(
        label='COZINHA', area=8.90, lx=297.0, ly=368.0,
        poly=[(277.8,211.2),(345.7,211.2),(345.7,432.3),(248.0,432.3),
              (248.0,284.8),(277.8,284.8)]),
    'banheiro': dict(
        label='BANHEIRO', area=3.80, lx=380.6, ly=392.0,
        poly=[(345.7,327.9),(415.6,327.9),(415.6,453.0),(345.7,453.0)]),
    'closet': dict(
        label='CLOSET', area=5.30, lx=314.0, ly=498.0,
        poly=[(248.0,432.3),(345.7,432.3),(345.7,552.7),(248.0,552.7)]),
    'quarto': dict(
        label='QUARTO', area=13.40, lx=505.0, ly=500.0,
        poly=[(415.6,432.3),(601.7,432.3),(601.7,552.7),(345.7,552.7),
              (345.7,453.0),(415.6,453.0)]),
}
ROOM_ORDER = ['jantar','sala','cozinha','closet','quarto','banheiro']

# --- REV. C: ponta em curva da cozinha --------------------------------------
# A ponta do monolítico encosta na quina sul do vão da porta de entrada
# (277,8 / 259,2) e gira em arco até a cabeça da parede da cozinha (345,7 /
# 325,65). Centro do arco em (277,8 / 325,65): rx = 67,9 pt e ry = 66,45 pt,
# ou seja um raio de ~1,49 m, tangente horizontal na porta e vertical na parede.
CURVA_CX, CURVA_CY = 277.8, 325.65
CURVA_RX, CURVA_RY = 67.90, 40.85
QUINA_DEGRAU = (277.8, 284.80)         # quina do degrau da parede — onde fica a geladeira
PORTA_QUINA = QUINA_DEGRAU             # compatibilidade
CURVA_FIM   = (345.7, 325.65)          # cabeça da parede cozinha / banheiro

def arco_pts(n=28, invertido=False):
    """Arco da ponta da cozinha, do ângulo 90° (porta) a 0° (parede)."""
    pts = []
    for i in range(n + 1):
        th = math.radians(90.0 * (1.0 - i / float(n)))
        pts.append((CURVA_CX + CURVA_RX * math.cos(th),
                    CURVA_CY - CURVA_RY * math.sin(th)))
    return list(reversed(pts)) if invertido else pts

COZ_MONO_POLY = ([(248.0,432.3),(248.0,284.8)] + arco_pts() + [(345.7,432.3)])
COZ_HALL_POLY = ([(277.8,211.2),(345.7,211.2),(345.7,325.65)]
                 + arco_pts(invertido=True))

# área do hall que sai do ambiente Cozinha e passa ao cumaru (m²)
_A_COZ_PT = 67.9 * 73.6 + 97.7 * 147.5
_A_HALL_PT = 67.9 * 73.6 + (67.9 * 40.85 - math.pi * CURVA_RX * CURVA_RY / 4.0)
AREA_HALL = round(ROOMS['cozinha']['area'] * _A_HALL_PT / _A_COZ_PT, 2)   # 1,94
AREA_COZ_MONO = round(ROOMS['cozinha']['area'] - AREA_HALL, 2)            # 6,96

# --- paredes ----------------------------------------------------------------
WALLS = [
    (446.11,124.38,604.03,128.94), (275.52,208.91,450.68,213.47),
    (275.52,208.91,280.09,287.11), (245.70,282.54,280.09,287.11),
    (279.36,430.06,345.67,434.63),
    (345.67,550.38,604.03,554.94), (343.39,450.67,417.90,455.24),
    (415.61,430.06,601.74,434.63),
    (343.39,432.34,347.96,455.24), (343.39,325.65,347.96,432.34),
    (413.33,325.65,417.90,432.34), (599.46,432.34,604.03,554.94),
    (279.36,430.06,283.92,545.96), (245.70,550.38,345.67,554.94),
    (343.39,513.42,347.96,552.66), (446.11,124.38,450.68,213.47),
    (413.33,432.34,417.90,455.24), (599.46,124.38,604.03,432.34),
    (245.70,282.54,250.26,554.94), (343.39,325.65,417.90,330.22),
]
# REV. C — drywall entre sala e quarto: retirada, indicada em fantasma
GHOST_WALLS = []
PORTA_NOVA = (416.90, 430.06, 462.50, 434.63)      # porta nova de 1,00 x 2,30 m
AREA_DRYWALL = 0.40                     # faixa de piso liberada, ~0,10 x 4,08 m

DOOR_ENTRADA = dict(rect=(275.52,220.10,280.09,259.20), hinge='n', leaf='e')
DOOR_BANHO   = dict(rect=(413.33,351.00,417.90,387.30), hinge='s', leaf='e')
JANELAS = [
    (599.46,142.50,604.03,193.20), (599.46,215.00,604.03,300.80),
    (599.46,348.00,604.03,394.40), (599.46,455.70,604.03,509.80),
    (251.40,550.38,342.00,554.94), (354.00,550.38,408.10,554.94),
]
ESCADA = dict(rect=(321.40,213.47,459.40,251.70), degraus=11)

TRANSICOES_A = [[(345.70,455.24),(345.70,513.42)]]      # closet ↔ quarto
TRANSICOES_BANHO = [[(415.60,351.00),(415.60,387.30)]]  # soleira da porta do WC

# ---------------------------------------------------------------------------
# 2. PALETA
# ---------------------------------------------------------------------------
BG        = '#faf8f4'
INK       = '#22303c'
INK_SOFT  = '#6b7480'
RULE      = '#cbc8c0'
WALL      = '#5b6472'
GHOST     = '#9aa2ab'
WOOD      = '#c98a4b'
WOOD_LINE = '#9c6530'
MONO      = '#dcd9d2'
MONO_LINE = '#b9b5ab'
WET       = '#d7e7ef'
WET_LINE  = '#6f9bb0'
JOINT     = '#1f2c38'
RED       = '#b23a2f'

# ---------------------------------------------------------------------------
# 3. INFRAESTRUTURA DE DESENHO
# ---------------------------------------------------------------------------
W, H = 1400, 990          # proporção A3 deitado (1:1,4142) — exporta em 420x297 mm
S = 48.0                                   # px por metro
PLAN_W, PLAN_H = BUILDING_W * S, BUILDING_H * S
PANEL_W = 630
PANEL_X = {'A': 48, 'B': 722}
PLAN_TOP = 212
FONT = "'IBM Plex Sans', Helvetica, Arial, sans-serif"

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def br(v):
    return ('%.2f' % v).replace('.', ',')

class Draw(object):
    def __init__(self):
        self.o = []
    def add(self, s):
        self.o.append(s)
    def txt(self, x, y, t, size=10, fill=INK, weight='normal', anchor='start', ls=None):
        a = ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" fill="%s" '
             'font-weight="%s" text-anchor="%s"' % (x, y, FONT, size, fill, weight, anchor))
        if ls:
            a += ' letter-spacing="%.2f"' % ls
        self.add(a + '>' + esc(t) + '</text>')
    def line(self, x1, y1, x2, y2, stroke, w=1.0, opacity=None, cap=None):
        a = ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"'
             % (x1, y1, x2, y2, stroke, w))
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        if cap: a += ' stroke-linecap="%s"' % cap
        self.add(a + '/>')
    def rect(self, x, y, w_, h_, fill='none', stroke=None, sw=1.0, opacity=None):
        a = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"' % (x, y, w_, h_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    def path(self, d_, fill='none', stroke=None, sw=1.0, opacity=None, dash=None):
        a = '<path d="%s" fill="%s"' % (d_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')

def plan_origin(panel):
    """panel: 'A'/'B' na prancha completa, ou uma origem (x, y) em px."""
    if isinstance(panel, tuple):
        return panel
    return (PANEL_X[panel] + (PANEL_W - PLAN_W) / 2.0, PLAN_TOP)

def P(panel, x_pt, y_pt):
    ox, oy = plan_origin(panel)
    return (ox + mx(x_pt) * S, oy + my(y_pt) * S)

def to_px(panel, poly):
    return [P(panel, x, y) for x, y in poly]

def path_d(pp, close=True):
    d = ['%s%.2f %.2f' % ('M' if i == 0 else 'L', p[0], p[1]) for i, p in enumerate(pp)]
    return ' '.join(d) + (' Z' if close else '')

# --- recorte analítico das hachuras contra o polígono da zona ---------------
def _spans(pairs):
    pairs.sort()
    return [(pairs[i], pairs[i + 1]) for i in range(0, len(pairs) - 1, 2)]

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

def bbox(pp):
    xs = [p[0] for p in pp]; ys = [p[1] for p in pp]
    return min(xs), min(ys), max(xs), max(ys)

# ---------------------------------------------------------------------------
# 4. ACABAMENTOS
#    A malha das hachuras parte da origem da planta, não de cada ambiente:
#    o piso é contínuo, então as réguas correm alinhadas de um cômodo a outro.
# ---------------------------------------------------------------------------
PLANK = 0.22       # largura da régua de cumaru (m)
JOINT_SPACING = 3.00   # junta de topo (m)

def fill_cumaru(d, panel, poly, smooth=None):
    pp = to_px(panel, poly)
    ox, oy = plan_origin(panel)
    d.path(smooth or path_d(pp), fill=WOOD)
    plank, joint = PLANK * S, JOINT_SPACING * S
    x0, y0, x1, y1 = bbox(pp)
    k0 = int(math.floor((y0 - oy) / plank))
    k1 = int(math.ceil((y1 - oy) / plank))
    for k in range(k0, k1 + 1):
        yy = oy + k * plank
        for (a, b) in spans_at_y(pp, yy):
            d.line(a, yy, b, yy, WOOD_LINE, 0.5, opacity=0.26)
        j0 = int(math.floor((x0 - ox) / joint)) - 1
        j1 = int(math.ceil((x1 - ox) / joint)) + 1
        for j in range(j0, j1 + 1):
            xx = ox + j * joint + (k % 3) * joint / 3.0
            if xx < x0 - 1 or xx > x1 + 1:
                continue
            for (ya, yb) in spans_at_x(pp, xx):
                a, b = max(ya, yy), min(yb, yy + plank)
                if b > a:
                    d.line(xx, a, xx, b, WOOD_LINE, 0.5, opacity=0.22)

def fill_mono(d, panel, poly, smooth=None):
    d.path(smooth or path_d(to_px(panel, poly)), fill=MONO)

def fill_wet(d, panel, poly, smooth=None):
    """Banheiro — sistema à parte: hachura fina a 45°."""
    pp = to_px(panel, poly)
    d.path(smooth or path_d(pp), fill=WET)
    x0, y0, x1, y1 = bbox(pp)
    step = 0.115 * S
    # retas a 45°: y = -x + c  →  varre c
    c0, c1 = x0 + y0, x1 + y1
    c = math.floor(c0 / step) * step
    while c <= c1 + step:
        seg = _clip45(pp, c, x0, y0, x1, y1)
        for (ax, ay, bx, by) in seg:
            d.line(ax, ay, bx, by, WET_LINE, 0.6, opacity=0.85)
        c += step

def _clip45(pp, c, x0, y0, x1, y1):
    """Recorta a reta x + y = c ao polígono (usado só em zonas retangulares)."""
    ax, ay = max(x0, c - y1), min(y1, c - x0)
    bx, by = min(x1, c - y0), max(y0, c - x1)
    if ax > bx:
        return []
    return [(ax, ay, bx, by)]

FILLERS = {'cumaru': fill_cumaru, 'mono': fill_mono, 'wet': fill_wet}

# ---------------------------------------------------------------------------
# 5. ELEMENTOS DE PLANTA
# ---------------------------------------------------------------------------
def draw_walls(d, panel):
    for (x0, y0, x1, y1) in WALLS:
        a = P(panel, x0, y0); b = P(panel, x1, y1)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=WALL)

def draw_ghost_walls(d, panel):
    for (x0, y0, x1, y1) in GHOST_WALLS:
        a = P(panel, x0, y0); b = P(panel, x1, y1)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill='none',
               stroke=GHOST, sw=0.9, opacity=0.9)
        d.add('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" '
              'stroke-width="0.9" stroke-dasharray="4 3" opacity="0.9"/>'
              % (a[0], a[1], b[0] - a[0], b[1] - a[1], GHOST))

def gap(d, panel, r):
    a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
    d.rect(a[0] - 0.3, a[1] - 0.3, b[0] - a[0] + 0.6, b[1] - a[1] + 0.6, fill=BG)

def draw_door(d, panel, door):
    r = door['rect']
    gap(d, panel, r)
    a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
    leaf = b[1] - a[1]
    hx = b[0] if door['leaf'] == 'e' else a[0]
    hy = a[1] if door['hinge'] == 'n' else b[1]
    ex = hx + (leaf if door['leaf'] == 'e' else -leaf)
    ty = hy + (leaf if door['hinge'] == 'n' else -leaf)
    d.line(hx, hy, ex, hy, WALL, 1.4)
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 %d %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>'
          % (ex, hy, leaf, leaf, 1 if door['hinge'] == 'n' else 0, hx, ty, WALL))

def draw_porta_nova(d, panel):
    """Porta nova de 1,00 x 2,30 m na drywall refeita, abrindo para o quarto."""
    gap(d, panel, PORTA_NOVA)
    a = P(panel, PORTA_NOVA[0], PORTA_NOVA[1]); b = P(panel, PORTA_NOVA[2], PORTA_NOVA[3])
    leaf = b[0] - a[0]
    hx, hy = a[0], b[1]
    d.line(hx, hy, hx, hy + leaf, WALL, 1.4)
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 0 %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>' % (hx, hy + leaf, leaf, leaf, hx + leaf, hy, WALL))


def draw_windows(d, panel):
    for r in JANELAS:
        gap(d, panel, r)
        a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill='none', stroke=WALL, sw=0.9)
        if (b[0] - a[0]) > (b[1] - a[1]):
            ym = (a[1] + b[1]) / 2.0
            d.line(a[0], ym, b[0], ym, WALL, 0.9)
        else:
            xm = (a[0] + b[0]) / 2.0
            d.line(xm, a[1], xm, b[1], WALL, 0.9)

def draw_escada(d, panel):
    r = ESCADA['rect']
    a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill='none', stroke=WALL, sw=0.9, opacity=0.85)
    n = ESCADA['degraus']
    for i in range(1, n):
        xx = a[0] + (b[0] - a[0]) * i / float(n)
        d.line(xx, a[1], xx, b[1], WALL, 0.7, opacity=0.6)
    d.txt((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0 + 3, 'ESCADA', 6.4, INK_SOFT, 'bold', 'middle', ls=0.8)

def dashed_polyline(d, panel, pts, stroke=JOINT, w=1.7, dash=6.0, gap_=4.2, halo=True):
    """Tracejado montado segmento a segmento (não depende do renderizador)."""
    pp = to_px(panel, pts)
    if halo:
        d.path(path_d(pp, close=False), stroke=BG, sw=w + 1.7, opacity=0.9)
    resto = 0.0
    desenhando = True
    for i in range(len(pp) - 1):
        (ax, ay), (bx, by) = pp[i], pp[i + 1]
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-9:
            continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0.0
        while t < L:
            passo = (dash if desenhando else gap_) - resto
            t2 = min(t + passo, L)
            if desenhando:
                d.line(ax + ux * t, ay + uy * t, ax + ux * t2, ay + uy * t2, stroke, w, cap='butt')
            if t2 - t >= passo - 1e-9:
                desenhando = not desenhando
                resto = 0.0
            else:
                resto += t2 - t
            t = t2

def draw_soleira_entrada(d, panel):
    r = DOOR_ENTRADA['rect']
    a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
    d.line(b[0], a[1], b[0], b[1], JOINT, 2.6)

def draw_labels(d, panel):
    for key in ROOM_ORDER:
        r = ROOMS[key]
        lx, ly = P(panel, r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 8.6, INK, 'bold', 'middle', ls=0.9)
        d.txt(lx, ly + 10, br(r['area']) + ' m²', 7.6, INK_SOFT, 'normal', 'middle')

def draw_scalebar(d, panel, y):
    ox, _ = plan_origin(panel)
    for i in range(2):
        d.rect(ox + i * S, y, S, 5, fill=(INK if i % 2 == 0 else BG), stroke=INK, sw=0.8)
    for i in range(3):
        d.txt(ox + i * S, y + 16, str(i), 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(ox + 2 * S + 13, y + 16, 'm   (base do scan)', 7.2, INK_SOFT)

# ---------------------------------------------------------------------------
# 6. ZONAS DE ACABAMENTO POR OPÇÃO
# ---------------------------------------------------------------------------
def smooth_mono_curva(panel):
    p = to_px(panel, [(248.0,432.3),(248.0,284.8)])
    f = P(panel, *CURVA_FIM)
    g = P(panel, 345.7, 432.3)
    rx, ry = CURVA_RX / PT_PER_M * S, CURVA_RY / PT_PER_M * S
    return (path_d(p, close=False)
            + ' A %.2f %.2f 0 0 1 %.2f %.2f L %.2f %.2f Z' % (rx, ry, f[0], f[1], g[0], g[1]))

def smooth_hall_curva(panel):
    p = to_px(panel, [(277.8,211.2),(345.7,211.2),(345.7,325.65)])
    f = P(panel, *PORTA_QUINA)
    rx, ry = CURVA_RX / PT_PER_M * S, CURVA_RY / PT_PER_M * S
    return (path_d(p, close=False)
            + ' A %.2f %.2f 0 0 0 %.2f %.2f Z' % (rx, ry, f[0], f[1]))

def zonas(opcao, panel):
    """Lista de (polígono_pt, acabamento, path_suave)."""
    z = []
    if opcao == 'A':
        for k in ('jantar', 'sala', 'quarto'):
            z.append((ROOMS[k]['poly'], 'cumaru', None))
        z.append((COZ_HALL_POLY, 'cumaru', smooth_hall_curva(panel)))
        z.append((COZ_MONO_POLY, 'mono', smooth_mono_curva(panel)))
        z.append((ROOMS['closet']['poly'], 'mono', None))
    else:
        for k in ('jantar', 'sala', 'quarto', 'cozinha', 'closet'):
            z.append((ROOMS[k]['poly'], 'mono', None))
    z.append((ROOMS['banheiro']['poly'], 'wet', None))
    return z

def juntas(opcao, panel):
    j = list(TRANSICOES_BANHO)
    if opcao == 'A':
        j = TRANSICOES_A + [[PORTA_QUINA] + arco_pts()] + j
    return j

# ---------------------------------------------------------------------------
# 7. DESENHO DA PLANTA
# ---------------------------------------------------------------------------
def draw_plan(d, panel, opcao, callout=False):
    for (poly, kind, smooth) in zonas(opcao, panel):
        FILLERS[kind](d, panel, poly, smooth)
    if opcao == 'A':
        for seg in juntas(opcao, panel)[:2]:
            dashed_polyline(d, panel, seg)
    draw_ghost_walls(d, panel)
    draw_walls(d, panel)
    draw_windows(d, panel)
    draw_door(d, panel, DOOR_ENTRADA)
    draw_door(d, panel, DOOR_BANHO)
    draw_porta_nova(d, panel)
    draw_soleira_entrada(d, panel)
    for seg in TRANSICOES_BANHO:
        dashed_polyline(d, panel, seg)
    draw_escada(d, panel)
    draw_labels(d, panel)
    if callout:
        ox, oy = plan_origin(panel)
        tx, ty = ox + 2, oy + 0.72 * S
        dx, dy = P(panel, *PORTA_QUINA)
        d.line(tx + 4, ty + 22, tx + 4, dy, JOINT, 0.9)
        d.line(tx + 4, dy, dx - 1, dy, JOINT, 0.9)
        d.add('<circle cx="%.1f" cy="%.1f" r="2.8" fill="%s"/>' % (dx, dy, JOINT))
        d.txt(tx, ty, 'QUINA DO DEGRAU DA PAREDE', 7.8, JOINT, 'bold', ls=0.6)
        d.txt(tx, ty + 9.5, 'logo abaixo da porta, onde fica a geladeira:', 7.6, INK_SOFT)
        d.txt(tx, ty + 18, 'a ponta do monolítico nasce aqui, em curva', 7.6, INK_SOFT)

# ---------------------------------------------------------------------------
# 7b. PLANTA ISOLADA (SVG por opção, para a versão HTML)
# ---------------------------------------------------------------------------
PAD_L, PAD_T, PAD_R, PAD_B = 14.0, 12.0, 14.0, 56.0

def plan_svg(opcao, callout=False):
    d = Draw()
    org = (PAD_L, PAD_T)
    w = PLAN_W + PAD_L + PAD_R
    h = PLAN_H + PAD_T + PAD_B
    d.rect(0, 0, w, h, fill=BG)
    draw_plan(d, org, opcao, callout=callout)
    draw_scalebar(d, org, PLAN_H + PAD_T + 20)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" '
            'role="img" aria-label="Planta do MainFloor com os acabamentos de piso">\n'
            % (w, h)) + '\n'.join(d.o) + '\n</svg>'

# ---------------------------------------------------------------------------
# 8. PRANCHA COMPLETA
# ---------------------------------------------------------------------------
def draw_table(d, panel, y, rows, total):
    x = PANEL_X[panel]
    d.txt(x, y - 8, 'QUADRO DE ÁREAS   (m²)', 8.0, INK_SOFT, 'bold', ls=1.2)
    d.line(x, y, x + PANEL_W, y, RULE, 0.9)
    ry = y + 18
    for row in rows:
        if row is None:
            ry += 22; continue
        nome, det, val, cor = row
        d.rect(x, ry - 8, 9, 9, fill=cor[0], stroke=cor[1], sw=0.7)
        d.txt(x + 16, ry, nome, 9.0, INK, 'bold')
        d.txt(x + 152, ry, det, 8.6, INK_SOFT)
        d.txt(x + PANEL_W, ry, val, 9.4, INK, 'bold', 'end')
        d.line(x, ry + 7, x + PANEL_W, ry + 7, RULE, 0.6, opacity=0.7)
        ry += 22
    d.txt(x + 16, ry + 3, 'TOTAL DO PAVIMENTO', 9.0, INK, 'bold', ls=0.4)
    d.txt(x + PANEL_W, ry + 3, total, 9.4, INK, 'bold', 'end')

def draw_notes(d, panel, y, lines):
    x = PANEL_X[panel]
    for i, ln in enumerate(lines):
        d.txt(x, y + i * 13.0, ln, 8.3, INK_SOFT)

def draw_panel(d, panel, titulo, subtitulo, opcao, callout=False):
    x = PANEL_X[panel]
    d.txt(x, 192, titulo, 12.8, INK, 'bold')
    d.txt(x + PANEL_W, 192, subtitulo, 8.8, INK_SOFT, 'normal', 'end')
    draw_plan(d, panel, opcao, callout=callout)
    draw_scalebar(d, panel, 686)

def build():
    d = Draw()
    d.rect(0, 0, W, H, fill=BG)

    d.txt(48, 42, 'MAXHAUS / MAIN FLOOR', 10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(48, 78, 'Cumaru ou monolítico', 27, INK, 'bold')
    d.txt(48, 99, 'Comparação gráfica em planta. Cores ilustrativas; nenhum produto ou espessura está especificado.',
          9.6, INK_SOFT)
    d.txt(W - 48, 42, 'REV. D   |   11.09.2026', 10.0, RED, 'bold', 'end', ls=0.8)
    d.txt(W - 48, 78, 'ponta da cozinha em curva na quina do degrau', 10.5, INK, 'bold', 'end')
    d.txt(W - 48, 99, 'fundo do box fechado em parede  ·  drywall refeita com porta',
          9.6, INK_SOFT, 'normal', 'end')
    d.line(48, 116, W - 48, 116, RULE, 1.0)

    ly = 140
    cx = 48
    for fill, stroke, t in ((WOOD, WOOD_LINE, 'Cumaru em réguas'),
                            (MONO, MONO_LINE, 'Piso monolítico'),
                            (WET, WET_LINE, 'Banheiro — sistema à parte (área molhada)')):
        d.rect(cx, ly - 9, 16, 11, fill=fill, stroke=stroke, sw=0.8)
        d.txt(cx + 23, ly, t, 9.2, INK)
        cx += 32 + len(t) * 5.0
    for i in range(3):
        d.line(cx + i * 9, ly - 3.5, cx + i * 9 + 6, ly - 3.5, JOINT, 1.7, cap='butt')
    d.txt(cx + 32, ly, 'Junta / soleira de transição', 9.2, INK)
    cx += 32 + len('Junta / soleira de transição') * 5.0 + 10
    d.line(48, 158, W - 48, 158, RULE, 1.0)
    d.line(PANEL_X['B'] - 22, 176, PANEL_X['B'] - 22, 908, RULE, 0.8, opacity=0.8)

    draw_panel(d, 'A', 'A / Cumaru nas áreas secas', 'cozinha e closet em monolítico',
               'A', callout=True)
    draw_table(d, 'A', 738, [
        ('Cumaru',        'sala 23,00 + quarto 13,40 + jantar 5,90 + hall 2,56', '44,86', (WOOD, WOOD_LINE)),
        ('+ reserva 10%', 'cortes, perdas e reposição futura',                   '49,35', (BG, WOOD_LINE)),
        ('Monolítico',    'cozinha 6,34 (de 8,90) + closet 5,30',                '11,64', (MONO, MONO_LINE)),
        ('Banheiro',      'sistema à parte (área molhada)',                      '3,80',  (WET, WET_LINE)),
    ], '60,30')
    draw_notes(d, 'A', 872, [
        'A ponta do monolítico nasce na quina do degrau da parede — logo abaixo da porta de entrada, onde fica a geladeira —',
        'e gira em curva (1,49 × 0,89 m) até a parede do banheiro. O corredor da entrada e a escada, 2,56 m² que o scan conta',
        'como cozinha, ficam em cumaru: por isso a cozinha entra no quadro com 6,34 m². Cumaru 44,86 m²; 49,35 m² com reserva.',
    ])

    draw_panel(d, 'B', 'B / Monolítico no MainFloor', 'banheiro em sistema à parte', 'B')
    draw_table(d, 'B', 738, [
        ('Monolítico',  'sala, jantar, quarto, cozinha e closet',        '56,50', (MONO, MONO_LINE)),
        ('Banheiro',    'sistema à parte (área molhada)',                '3,80',  (WET, WET_LINE)),
        ('Sem reserva', 'aplicação moldada in loco, sem perda de corte', '—',     (BG, RULE)),
        None,
    ], '60,30')
    draw_notes(d, 'B', 872, [
        'Monolítico contínuo em 56,50 m² de base horizontal (60,30 m² do pavimento menos os 3,80 m² do banheiro) — sem',
        'junta de material entre os ambientes secos. Degraus excluídos; o piso acessível sob a escada permanece. Juntas de',
        'dilatação a definir no executivo. No banheiro, especificar sistema com impermeabilização e acabamento antiderrapante.',
    ])

    d.line(48, 922, W - 48, 922, RULE, 1.0)
    d.txt(48, 940, 'Revestimento contínuo: toda a área de piso é revestida, inclusive sob móveis e equipamentos — nenhum recorte de mobiliário foi descontado. '
                    'O fundo do box aparece já fechado em parede (ver Prancha 02).',
          8.3, INK_SOFT)
    d.txt(48, 953, 'A drywall entre sala e quarto é demolida e refeita no mesmo eixo, agora com uma porta de 1,00 × 2,30 m: as áreas de piso não mudam. '
                    'Áreas conforme o scan de 02.09.2026.',
          8.3, INK_SOFT)
    d.txt(48, 975, 'ESTUDO PRELIMINAR — NÃO LIBERADO PARA EXECUÇÃO   |   11/09/2026', 9.0, RED, 'bold', ls=0.5)
    d.txt(W - 48, 975, 'Prancha 03 / 08   ·   REV. D', 9.0, INK_SOFT, 'normal', 'end')

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            % (W, H, W, H)) + '\n'.join(d.o) + '\n</svg>'

def exportar_a3(svg_path, pdf_path):
    """Fecha a prancha em uma folha A3 deitada (420 x 297 mm)."""
    import pymupdf
    src = pymupdf.open(svg_path)
    doc = pymupdf.open('pdf', src.convert_to_pdf())
    folha = pymupdf.paper_rect('a3-l')          # 1190,55 x 841,89 pt
    saida = pymupdf.open()
    pagina = saida.new_page(width=folha.width, height=folha.height)
    pagina.show_pdf_page(pagina.rect, doc, 0)
    saida.set_metadata({
        'title': 'MaxHaus MainFloor — Prancha 03: cumaru ou monolítico (REV. C)',
        'subject': 'Estudo preliminar de pisos — A3, 420 x 297 mm',
        'keywords': 'MaxHaus, MainFloor, piso, cumaru, monolítico, prancha 03, rev C',
    })
    saida.save(pdf_path)
    print('ok', os.path.basename(pdf_path), '%.0f x %.0f mm'
          % (folha.width / 72.0 * 25.4, folha.height / 72.0 * 25.4))


def exportar_png(svg_path, png_path, dpi=170):
    import pymupdf
    pix = pymupdf.open(svg_path)[0].get_pixmap(dpi=dpi)
    pix.save(png_path)
    print('ok', os.path.basename(png_path), '%dx%d' % (pix.width, pix.height))


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, 'pranchas')
    if not os.path.isdir(out):
        os.makedirs(out)
    print('hall %s m² · cozinha monolítica %s m²' % (br(AREA_HALL), br(AREA_COZ_MONO)))
    svg_prancha = os.path.join(out, 'prancha-03-cumaru-ou-monolitico.svg')
    for nome, conteudo in (
            ('prancha-03-cumaru-ou-monolitico.svg', build()),
            ('planta-opcao-a.svg', plan_svg('A', callout=True)),
            ('planta-opcao-b.svg', plan_svg('B'))):
        with open(os.path.join(out, nome), 'w') as f:
            f.write(conteudo)
        print('ok', nome, len(conteudo))
    exportar_a3(svg_prancha, os.path.join(out, 'prancha-03-cumaru-ou-monolitico-A3.pdf'))
    exportar_png(svg_prancha, os.path.join(out, 'prancha-03-cumaru-ou-monolitico.png'))
