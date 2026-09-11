# -*- coding: utf-8 -*-
"""
Prancha 03 — MaxHaus MainFloor | Cumaru ou monolítico (REV. B)

Geometria extraída do levantamento "MaxHaus_Mainfloor.pdf" (scan, pág. 2):
paredes, aberturas e polígonos de ambiente foram lidos do vetor original em
pontos PDF e convertidos para metros pela escala 45,66 pt/m — conferida contra
as cotas gerais do pavimento (7,85 m x 9,43 m).

REV. B (11.09.2026)
  · cozinha e closet passam a monolítico também na proposta de cumaru;
    a extensão da cozinha termina na soleira da porta de entrada;
  · banheiro sai do monolítico nas duas opções (sistema à parte, área molhada);
  · piso desenhado contínuo: nenhum recorte de mobiliário é descontado.

Saída: pranchas/prancha-03-cumaru-ou-monolitico.svg
"""
import os

# ---------------------------------------------------------------------------
# 1. BASE DO SCAN — unidades em pontos PDF da pág. 2 do levantamento
# ---------------------------------------------------------------------------
ORIGIN_X, ORIGIN_Y = 245.7, 124.38    # canto externo noroeste do pavimento
PT_PER_M = 45.66                       # 358,33 pt / 7,85 m = 430,56 pt / 9,43 m
BUILDING_W, BUILDING_H = 7.85, 9.43

def mx(v): return (v - ORIGIN_X) / PT_PER_M
def my(v): return (v - ORIGIN_Y) / PT_PER_M

# --- ambientes: polígono (contorno) + retângulos (preenchimento/hachura) ----
ROOMS = {
    'jantar': dict(
        label='JANTAR', area=5.90, lx=525.0, ly=165.0,
        poly=[(448.4,126.7),(601.7,126.7),(601.7,211.2),(448.4,211.2)],
        rects=[(448.4,126.7,601.7,211.2)]),
    'sala': dict(
        label='SALA', area=23.00, lx=508.0, ly=285.0,
        poly=[(345.7,211.2),(601.7,211.2),(601.7,432.3),(415.6,432.3),
              (415.6,327.9),(345.7,327.9)],
        rects=[(345.7,211.2,601.7,327.9),(415.6,327.9,601.7,432.3)]),
    'cozinha': dict(
        label='COZINHA', area=8.90, lx=297.0, ly=360.0,
        poly=[(277.8,211.2),(345.7,211.2),(345.7,432.3),(248.0,432.3),
              (248.0,284.8),(277.8,284.8)],
        rects=[(277.8,211.2,345.7,284.8),(248.0,284.8,345.7,432.3)]),
    'banheiro': dict(
        label='BANHEIRO', area=3.80, lx=380.6, ly=392.0,
        poly=[(345.7,327.9),(415.6,327.9),(415.6,453.0),(345.7,453.0)],
        rects=[(345.7,327.9,415.6,453.0)]),
    'closet': dict(
        label='CLOSET', area=5.30, lx=314.0, ly=498.0,
        poly=[(248.0,432.3),(345.7,432.3),(345.7,552.7),(248.0,552.7)],
        rects=[(248.0,432.3,345.7,552.7)]),
    'quarto': dict(
        label='QUARTO', area=13.40, lx=505.0, ly=500.0,
        poly=[(415.6,432.3),(601.7,432.3),(601.7,552.7),(345.7,552.7),
              (345.7,453.0),(415.6,453.0)],
        rects=[(415.6,432.3,601.7,552.7),(345.7,453.0,415.6,552.7)]),
}
ROOM_ORDER = ['jantar','sala','cozinha','closet','quarto','banheiro']

WALLS = [
    (446.11,124.38,604.03,128.94), (275.52,208.91,450.68,213.47),
    (275.52,208.91,280.09,287.11), (245.70,282.54,280.09,287.11),
    (279.36,430.06,345.67,434.63), (415.61,430.06,601.74,434.63),
    (343.39,450.67,417.90,455.24), (345.67,550.38,604.03,554.94),
    (343.39,432.34,347.96,455.24), (343.39,325.65,347.96,432.34),
    (413.33,325.65,417.90,432.34), (599.46,432.34,604.03,554.94),
    (279.36,430.06,283.92,545.96), (245.70,550.38,345.67,554.94),
    (343.39,513.42,347.96,552.66), (446.11,124.38,450.68,213.47),
    (413.33,432.34,417.90,455.24), (599.46,124.38,604.03,432.34),
    (245.70,282.54,250.26,554.94), (343.39,325.65,417.90,330.22),
]

DOOR_ENTRADA = dict(rect=(275.52,220.10,280.09,259.20), hinge='n', leaf='e')
DOOR_BANHO   = dict(rect=(413.33,351.00,417.90,387.30), hinge='n', leaf='e')
PASSAGENS = [(361.90,450.67,412.30,455.24)]
JANELAS = [
    (599.46,142.50,604.03,193.20), (599.46,215.00,604.03,300.80),
    (599.46,348.00,604.03,394.40), (599.46,455.70,604.03,509.80),
    (251.40,550.38,342.00,554.94), (354.00,550.38,408.10,554.94),
]
ESCADA = dict(rect=(321.40,213.47,459.40,251.70), degraus=11)

# juntas de transição em vãos livres (sem parede separando acabamentos)
TRANSICOES_A = [
    ((345.70,211.20),(345.70,325.65)),   # extensão da cozinha  ↔  hall / sala
    ((345.70,455.24),(345.70,513.42)),   # closet               ↔  quarto
]
TRANSICOES_BANHO = [
    ((415.60,351.00),(415.60,387.30)),   # soleira da porta do banheiro
    ((361.90,452.95),(412.30,452.95)),   # soleira do vão banheiro ↔ quarto
]

# ---------------------------------------------------------------------------
# 2. PALETA
# ---------------------------------------------------------------------------
BG        = '#faf8f4'
INK       = '#22303c'
INK_SOFT  = '#6b7480'
RULE      = '#cbc8c0'
WALL      = '#5b6472'
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
W, H = 1400, 1090
S = 55.0                                   # px por metro
PLAN_W, PLAN_H = BUILDING_W * S, BUILDING_H * S
PANEL_W = 630
PANEL_X = {'A': 48, 'B': 722}
PLAN_TOP = 238
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
    def line(self, x1, y1, x2, y2, stroke, w=1.0, dash=None, opacity=None, cap=None):
        a = ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"'
             % (x1, y1, x2, y2, stroke, w))
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        if cap: a += ' stroke-linecap="%s"' % cap
        self.add(a + '/>')
    def rect(self, x, y, w_, h_, fill='none', stroke=None, sw=1.0, opacity=None):
        a = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"' % (x, y, w_, h_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')

def plan_origin(panel):
    """panel pode ser 'A'/'B' (prancha completa) ou uma origem (x, y) em px."""
    if isinstance(panel, tuple):
        return panel
    return (PANEL_X[panel] + (PANEL_W - PLAN_W) / 2.0, PLAN_TOP)

def P(panel, x_pt, y_pt):
    ox, oy = plan_origin(panel)
    return (ox + mx(x_pt) * S, oy + my(y_pt) * S)

def path_of(panel, poly):
    d = []
    for i, (x, y) in enumerate(poly):
        px, py = P(panel, x, y)
        d.append('%s%.2f %.2f' % ('M' if i == 0 else 'L', px, py))
    return ' '.join(d) + ' Z'

def px_rects(panel, rects):
    out = []
    for (x0, y0, x1, y1) in rects:
        a = P(panel, x0, y0); b = P(panel, x1, y1)
        out.append((a[0], a[1], b[0], b[1]))
    return out

def clip_segment(seg, box):
    """Liang-Barsky: recorta o segmento ao retângulo; devolve None se fora."""
    x0, y0, x1, y1 = seg
    xmin, ymin, xmax, ymax = box
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if abs(p) < 1e-9:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1: return None
            if r > t0: t0 = r
        else:
            if r < t0: return None
            if r < t1: t1 = r
    return (x0 + t0 * dx, y0 + t0 * dy, x0 + t1 * dx, y0 + t1 * dy)

# ---------------------------------------------------------------------------
# 4. ACABAMENTOS
# ---------------------------------------------------------------------------
def fill_base(d, panel, room, color):
    for (a, b, c, e) in px_rects(panel, room['rects']):
        d.rect(a - 0.2, b - 0.2, c - a + 0.4, e - b + 0.4, fill=color)

def fill_cumaru(d, panel, room):
    """Taboado de cumaru: réguas de 19 cm com juntas de topo desencontradas."""
    fill_base(d, panel, room, WOOD)
    plank = 0.22 * S
    joint = 3.00 * S
    for box in px_rects(panel, room['rects']):
        x0, y0, x1, y1 = box
        n, yy = 0, y0
        while yy <= y1 + plank:
            s = clip_segment((x0, yy, x1, yy), box)
            if s:
                d.line(s[0], s[1], s[2], s[3], WOOD_LINE, 0.5, opacity=0.26)
            xx = x0 + (n % 3) * joint / 3.0 + 0.30 * S
            while xx <= x1:
                s = clip_segment((xx, yy, xx, yy + plank), box)
                if s:
                    d.line(s[0], s[1], s[2], s[3], WOOD_LINE, 0.5, opacity=0.22)
                xx += joint
            yy += plank; n += 1

def fill_mono(d, panel, room):
    fill_base(d, panel, room, MONO)

def fill_wet(d, panel, room):
    """Banheiro — sistema à parte: hachura fina a 45°."""
    fill_base(d, panel, room, WET)
    step = 0.115 * S
    for box in px_rects(panel, room['rects']):
        x0, y0, x1, y1 = box
        span = (x1 - x0) + (y1 - y0)
        t = -span
        while t <= span:
            s = clip_segment((x0 + t, y1, x0 + t + (y1 - y0), y0), box)
            if s:
                d.line(s[0], s[1], s[2], s[3], WET_LINE, 0.6, opacity=0.85)
            t += step

FILLERS = {'cumaru': fill_cumaru, 'mono': fill_mono, 'wet': fill_wet}

# ---------------------------------------------------------------------------
# 5. ELEMENTOS DE PLANTA
# ---------------------------------------------------------------------------
def draw_walls(d, panel):
    for (x0, y0, x1, y1) in WALLS:
        a = P(panel, x0, y0); b = P(panel, x1, y1)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=WALL)

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
    d.txt((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0 + 3, 'ESCADA', 7.0, INK_SOFT, 'bold', 'middle', ls=0.8)

def draw_juntas(d, panel, segs):
    """Junta/soleira: tracejado montado segmento a segmento."""
    dash, gap_ = 6.0, 4.2
    for (p0, p1) in segs:
        a = P(panel, p0[0], p0[1]); b = P(panel, p1[0], p1[1])
        d.line(a[0], a[1], b[0], b[1], BG, 3.4, opacity=0.9)
        L = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if L < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        t = 0.0
        while t < L:
            t2 = min(t + dash, L)
            d.line(a[0] + ux * t, a[1] + uy * t, a[0] + ux * t2, a[1] + uy * t2,
                   JOINT, 1.7, cap='butt')
            t = t2 + gap_

def draw_soleira_entrada(d, panel):
    r = DOOR_ENTRADA['rect']
    a = P(panel, r[0], r[1]); b = P(panel, r[2], r[3])
    d.line(b[0], a[1], b[0], b[1], JOINT, 2.6)

def draw_labels(d, panel):
    for key in ROOM_ORDER:
        r = ROOMS[key]
        lx, ly = P(panel, r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 9.2, INK, 'bold', 'middle', ls=0.9)
        d.txt(lx, ly + 11, br(r['area']) + ' m²', 8.2, INK_SOFT, 'normal', 'middle')

def draw_scalebar(d, panel, y):
    ox, _ = plan_origin(panel)
    for i in range(2):
        d.rect(ox + i * S, y, S, 5, fill=(INK if i % 2 == 0 else BG), stroke=INK, sw=0.8)
    for i in range(3):
        d.txt(ox + i * S, y + 17, str(i), 7.5, INK_SOFT, 'normal', 'middle')
    d.txt(ox + 2 * S + 14, y + 17, 'm   (base do scan)', 7.5, INK_SOFT)

# ---------------------------------------------------------------------------
# 6. BLOCOS DE TEXTO
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
        d.txt(x, y + i * 13.5, ln, 8.6, INK_SOFT)

# ---------------------------------------------------------------------------
# 7. PAINEL
# ---------------------------------------------------------------------------
def draw_panel(d, panel, titulo, subtitulo, finishes, transicoes, callout=False):
    x = PANEL_X[panel]
    d.txt(x, 214, titulo, 13.5, INK, 'bold')
    d.txt(x + PANEL_W, 214, subtitulo, 9.0, INK_SOFT, 'normal', 'end')

    for key in ROOM_ORDER:
        FILLERS[finishes[key]](d, panel, ROOMS[key])
    draw_juntas(d, panel, transicoes)
    draw_walls(d, panel)
    draw_windows(d, panel)
    for r in PASSAGENS:
        gap(d, panel, r)
    draw_door(d, panel, DOOR_ENTRADA)
    draw_door(d, panel, DOOR_BANHO)
    draw_soleira_entrada(d, panel)
    draw_juntas(d, panel, TRANSICOES_BANHO)      # soleiras do banheiro, sobre os vãos
    draw_escada(d, panel)
    draw_labels(d, panel)

    if callout:
        ox, oy = plan_origin(panel)
        tx, ty = ox + 2, oy + 0.80 * S
        dx, dy = P(panel, 277.8, 239.6)
        d.line(tx + 4, ty + 12, tx + 4, dy, JOINT, 0.9, dash='3 2.5')
        d.line(tx + 4, dy, dx - 1, dy, JOINT, 0.9, dash='3 2.5')
        d.add('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (dx, dy, JOINT))
        d.txt(tx, ty, 'PORTA DE ENTRADA', 8.2, JOINT, 'bold', ls=0.6)
        d.txt(tx, ty + 10, 'a extensão da cozinha termina aqui', 8.0, INK_SOFT)

    draw_scalebar(d, panel, 782)

# ---------------------------------------------------------------------------
# 7b. PLANTA ISOLADA  (SVG por opção, para a versão HTML)
# ---------------------------------------------------------------------------
PAD_L, PAD_T, PAD_R, PAD_B = 14.0, 12.0, 14.0, 56.0

def plan_svg(finishes, transicoes, callout=False):
    d = Draw()
    org = (PAD_L, PAD_T)
    w = PLAN_W + PAD_L + PAD_R
    h = PLAN_H + PAD_T + PAD_B
    d.rect(0, 0, w, h, fill=BG)

    for key in ROOM_ORDER:
        FILLERS[finishes[key]](d, org, ROOMS[key])
    draw_juntas(d, org, transicoes)
    draw_walls(d, org)
    draw_windows(d, org)
    for r in PASSAGENS:
        gap(d, org, r)
    draw_door(d, org, DOOR_ENTRADA)
    draw_door(d, org, DOOR_BANHO)
    draw_soleira_entrada(d, org)
    draw_juntas(d, org, TRANSICOES_BANHO)
    draw_escada(d, org)
    draw_labels(d, org)

    if callout:
        tx, ty = org[0] + 2, org[1] + 0.80 * S
        dx, dy = P(org, 277.8, 239.6)
        d.line(tx + 4, ty + 12, tx + 4, dy, JOINT, 0.9)
        d.line(tx + 4, dy, dx - 1, dy, JOINT, 0.9)
        d.add('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (dx, dy, JOINT))
        d.txt(tx, ty, 'PORTA DE ENTRADA', 8.2, JOINT, 'bold', ls=0.6)
        d.txt(tx, ty + 10, 'a extensão da cozinha termina aqui', 8.0, INK_SOFT)

    draw_scalebar(d, org, PLAN_H + PAD_T + 20)

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" '
            'role="img" aria-label="Planta do MainFloor com os acabamentos de piso">\n'
            % (w, h)) + '\n'.join(d.o) + '\n</svg>'

FINISHES_A = {'sala':'cumaru','quarto':'cumaru','jantar':'cumaru',
              'cozinha':'mono','closet':'mono','banheiro':'wet'}
FINISHES_B = {'sala':'mono','quarto':'mono','jantar':'mono',
              'cozinha':'mono','closet':'mono','banheiro':'wet'}

# ---------------------------------------------------------------------------
# 8. PRANCHA
# ---------------------------------------------------------------------------
def build():
    d = Draw()
    d.rect(0, 0, W, H, fill=BG)

    d.txt(48, 48, 'MAXHAUS / MAIN FLOOR', 10.5, INK_SOFT, 'bold', ls=1.6)
    d.txt(48, 86, 'Cumaru ou monolítico', 30, INK, 'bold')
    d.txt(48, 108, 'Comparação gráfica em planta. Cores ilustrativas; nenhum produto ou espessura está especificado.',
          10.0, INK_SOFT)
    d.txt(W - 48, 48, 'REV. B   |   11.09.2026', 10.5, RED, 'bold', 'end', ls=0.8)
    d.txt(W - 48, 86, 'cozinha e closet em monolítico', 11.0, INK, 'bold', 'end')
    d.txt(W - 48, 108, 'banheiro fora do monolítico nas duas opções', 10.0, INK_SOFT, 'normal', 'end')

    d.line(48, 126, W - 48, 126, RULE, 1.0)

    ly = 152
    items = [(WOOD, WOOD_LINE, 'Cumaru em réguas'),
             (MONO, MONO_LINE, 'Piso monolítico'),
             (WET, WET_LINE, 'Banheiro — sistema à parte (área molhada)')]
    cx = 48
    for fill, stroke, t in items:
        d.rect(cx, ly - 9, 16, 11, fill=fill, stroke=stroke, sw=0.8)
        d.txt(cx + 23, ly, t, 9.2, INK)
        cx += 32 + len(t) * 5.0
    d.line(cx, ly - 3.5, cx + 18, ly - 3.5, JOINT, 1.7, dash='5 3.5')
    d.txt(cx + 25, ly, 'Junta / soleira de transição entre acabamentos', 9.2, INK)
    d.line(48, 172, W - 48, 172, RULE, 1.0)
    d.line(PANEL_X['B'] - 22, 192, PANEL_X['B'] - 22, 1008, RULE, 0.8, opacity=0.8)

    draw_panel(d, 'A', 'A / Cumaru nas áreas secas', 'cozinha e closet em monolítico',
               finishes=FINISHES_A, transicoes=TRANSICOES_A, callout=True)

    draw_table(d, 'A', 828, [
        ('Cumaru',        'sala 23,00  +  quarto 13,40  +  jantar 5,90', '42,30', (WOOD, WOOD_LINE)),
        ('+ reserva 10%', 'cortes, perdas e reposição futura',           '46,53', (BG, WOOD_LINE)),
        ('Monolítico',    'cozinha 8,90  +  closet 5,30',                '14,20', (MONO, MONO_LINE)),
        ('Banheiro',      'sistema à parte (área molhada)',              '3,80',  (WET, WET_LINE)),
    ], '60,30')

    draw_notes(d, 'A', 964, [
        'Cumaru só nas áreas secas de convívio: 42,30 m² líquidos; com reserva de 10% para cortes e reposição, 46,53 m².',
        'Cozinha e closet recebem o mesmo monolítico da opção B (14,20 m²). A extensão da cozinha sobe pelo corredor e',
        'termina na soleira da porta de entrada — do hall/escada em diante o piso é cumaru.',
    ])

    draw_panel(d, 'B', 'B / Monolítico no MainFloor', 'banheiro em sistema à parte',
               finishes=FINISHES_B, transicoes=[], callout=False)

    draw_table(d, 'B', 828, [
        ('Monolítico',  'sala, jantar, quarto, cozinha e closet',        '56,50', (MONO, MONO_LINE)),
        ('Banheiro',    'sistema à parte (área molhada)',                '3,80',  (WET, WET_LINE)),
        ('Sem reserva', 'aplicação moldada in loco, sem perda de corte', '—',     (BG, RULE)),
        None,
    ], '60,30')

    draw_notes(d, 'B', 964, [
        'Monolítico contínuo em 56,50 m² de base horizontal (60,30 m² do pavimento menos os 3,80 m² do banheiro).',
        'Degraus excluídos; o piso acessível sob a escada permanece. Juntas de dilatação e de transição a definir no executivo.',
        'No banheiro, especificar sistema compatível com água, impermeabilização e acabamento antiderrapante.',
    ])

    d.line(48, 1024, W - 48, 1024, RULE, 1.0)
    d.txt(48, 1044, 'Revestimento contínuo: toda a área de piso é revestida, inclusive sob móveis e equipamentos — nenhum recorte de mobiliário foi descontado.',
          8.6, INK_SOFT)
    d.txt(48, 1058, 'Áreas conforme levantamento MaxHaus MainFloor (scan de 02.09.2026); a escada é o único elemento deduzido, conforme nota da opção B.',
          8.6, INK_SOFT)
    d.txt(48, 1080, 'ESTUDO PRELIMINAR — NÃO LIBERADO PARA EXECUÇÃO   |   11/09/2026', 9.0, RED, 'bold', ls=0.5)
    d.txt(W - 48, 1080, 'Prancha 03 / 08   ·   REV. B', 9.0, INK_SOFT, 'normal', 'end')

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            % (W, H, W, H)) + '\n'.join(d.o) + '\n</svg>'

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, 'pranchas')
    if not os.path.isdir(out):
        os.makedirs(out)
    for nome, conteudo in (
            ('prancha-03-cumaru-ou-monolitico.svg', build()),
            ('planta-opcao-a.svg', plan_svg(FINISHES_A, TRANSICOES_A, callout=True)),
            ('planta-opcao-b.svg', plan_svg(FINISHES_B, [], callout=False))):
        with open(os.path.join(out, nome), 'w') as f:
            f.write(conteudo)
        print('ok', nome, len(conteudo))
