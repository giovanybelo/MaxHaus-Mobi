# -*- coding: utf-8 -*-
"""Desenho das elevações (P1–P6, nicho, bancada) e da planta do banheiro."""
import math
from lib import *
import calc_r1 as CR

def fm(v, d=0):
    """mm em pt-BR"""
    s = ('%.' + str(d) + 'f') % v
    if d: s = s.rstrip('0').rstrip('.')
    s = s.replace('.', ',')
    if d == 0 and abs(v) >= 1000:
        s = '{:,}'.format(int(round(v))).replace(',', '.')
    return s

def tile_fill(q):
    if q['col'] == 'N':
        return NUAGE if q['kind'] == 'f' else NUAGE_CUT
    return BLEU if q['kind'] == 'f' else BLEU_CUT

def draw_wall(c, ox, oy, sc, sid, chains='full', idx=True, nome=None, tag=None, name_dy=None, tags=True, axis=True, vchain=True):
    """Elevação: (ox, oy) é o canto inferior esquerdo; sc em pt/mm."""
    w = CR.WALLS[sid]; W = w['W']; H = CR.H_ROOM; HT = CR.H_TILE
    p, xs, pcs = CR.wall_pieces(sid)
    X = lambda v: ox + v * sc
    Y = lambda v: oy + v * sc
    # faixa acima do revestimento
    rect(c, X(0), Y(HT), W * sc, (H - HT) * sc, white, None)
    hatch(c, X(0), Y(HT), W * sc, (H - HT) * sc, 3, K45, 0.3)
    rect(c, X(0), Y(0), W * sc, HT * sc, JUNTA, None)
    for q in pcs:
        rect(c, X(q['x0']), Y(q['y0']), (q['x1'] - q['x0']) * sc, (q['y1'] - q['y0']) * sc, tile_fill(q), JUNTA, 0.25)
    for (hx0, hx1, hy0, hy1, hn) in w['hole']:
        rect(c, X(hx0), Y(hy0), (hx1 - hx0) * sc, (hy1 - hy0) * sc, white, K, 0.8)
        hatch(c, X(hx0), Y(hy0), (hx1 - hx0) * sc, (hy1 - hy0) * sc, 5, K20, 0.35)
        lab = 'NICHO 1000 × 400 × 118' if hn == 'nicho' else 'PORTA · vão 800 × 1.990'
        cx = X((hx0 + hx1) / 2); cy = Y((hy0 + hy1) / 2)
        rect(c, cx - 52, cy - 8, 104, 14, white, None)
        txt(c, cx, cy - 4, lab, 6.8, 'S-B', K, 'c')
    rect(c, X(0), Y(0), W * sc, H * sc, None, K, 1.0)
    line(c, X(0), Y(HT), X(W), Y(HT), 0.9, K)
    if tags:
        for q in pcs:
            if q['col'] == 'N' and (q['x1'] - q['x0']) * sc > 9:
                txt(c, X((q['x0'] + q['x1']) / 2), Y((q['y0'] + q['y1']) / 2) - 2, q['tag'][-2:], 5.2, 'S-B', BLEU, 'c')
    if axis and sid != 'P6':
        line(c, X(W / 2), Y(0) - 7, X(W / 2), Y(H) + 7, 0.8, MAGENTA, (5, 1.6, 1, 1.6))
    if chains:
        y1 = Y(H) + 12
        if chains == 'full' and sid != 'P6':
            cc = p['c']
            dimh(c, X(0), X(cc), y1, fm(cc, 1), 6.2)
            dimh(c, X(cc), X(W - cc), y1, '%d inteiras · módulo 77' % p['n'], 6.2)
            dimh(c, X(W - cc), X(W), y1, fm(cc, 1), 6.2)
            dimh(c, X(0), X(W), y1 + 15, fm(W) + ' mm', 7.0, bold=True)
            txt(c, X(W / 2), y1 + 27, 'EIXO', 6.2, 'S-B', MAGENTA, 'c', ls=0.8)
        else:
            dimh(c, X(0), X(W), y1, fm(W) + ' mm', 7.0, bold=True)
        xl = X(0) - 14
        if vchain: dimv(c, xl, Y(0), Y(HT), '15 fiadas inteiras · ' + fm(HT) + ' mm', 6.2)
        if vchain:
            dimv(c, xl, Y(HT), Y(H), '', 6.2)
            txt(c, xl - 4, Y(HT) + (H - HT) * sc / 2 - 2, '38', 5.6, 'S', K70, 'r')
            dimv(c, xl - 15, Y(0), Y(H), fm(H) + ' mm', 7.0, bold=True)
    if idx:
        for ri, (y0, y1_, t) in enumerate(CR.ROWS):
            if ri % 2 == 0 or sc > 0.12:
                txt(c, X(W) + 4, Y((y0 + y1_) / 2) - 2, 'F%d' % (ri + 1), 5.6, 'S', K70)
        colw = CR.A * sc
        step = 1 if colw >= 14 else (2 if colw >= 8 else 5)
        for ci, (x0, x1, t) in enumerate(xs):
            n_ = ci + 1
            if step == 1 or n_ % step == 0 or n_ in (1, len(xs)):
                txt(c, X((x0 + x1) / 2), Y(0) - 9, 'C%d' % n_, 5.4, 'S', K70, 'c')
    dy = name_dy if name_dy is not None else (50 if chains == 'full' else 28)
    if nome: txt(c, X(0), Y(H) + dy, nome, 11, 'S-B')
    if tag: txt(c, X(0), Y(H) + dy - 11, tag, 7.0, 'S', K70)
    return p, xs, pcs

def legend_tiles(c, x, y, size=7.6, extra=True):
    items = [(BLEU, 'Bleu Nuit inteira'), (BLEU_CUT, 'Bleu Nuit cortada'), (NUAGE, 'Nuage inteira (acento)'), (NUAGE_CUT, 'Nuage cortada')]
    for col, lab in items:
        rect(c, x, y - 1, 11, 8, col, K, 0.4)
        txt(c, x + 15, y, lab, size); x += 15 + pdfmetrics.stringWidth(lab, 'S', size) + 14
    if extra:
        rect(c, x, y - 1, 11, 8, white, K, 0.4); hatch(c, x, y - 1, 11, 8, 3)
        txt(c, x + 15, y, 'vão / faixa sem revestimento', size); x += 15 + pdfmetrics.stringWidth('vão / faixa sem revestimento', 'S', size) + 14
        line(c, x, y + 3, x + 11, y + 3, 0.8, MAGENTA, (4, 1.6, 1, 1.6)); txt(c, x + 15, y, 'eixo', size)
    return x

# ---------------------------------------------------------------- planta
PL_W, PL_L = 1423.0, 2583.0
def draw_plan(c, ox, oy, sc, mode='demo', labels=True):
    """Planta com o norte (P5) no topo. ox, oy = canto superior esquerdo interno; y cresce para baixo."""
    X = lambda v: ox + v * sc
    Y = lambda v: oy - v * sc
    t = 100
    rect(c, X(-t), Y(PL_L + t), (PL_W + 2 * t) * sc, (PL_L + 2 * t) * sc, HexColor('#3a3a3a'), None)
    rect(c, X(0), Y(PL_L), PL_W * sc, PL_L * sc, HexColor('#f4f2ee'), None)
    # box
    rect(c, X(150), Y(PL_L), (PL_W - 150) * sc, (PL_L - 1706) * sc, CIANO18, None)
    # área técnica
    rect(c, X(0), Y(PL_L), 152 * sc, (PL_L - 1706) * sc, HexColor('#bdbdbd'), K, 0.5)
    txt(c, X(76), Y(2150), 'área técnica', 6.0, 'S-I', K, 'c', rot=90)
    # vidro do box
    line(c, X(152), Y(1706), X(PL_W), Y(1706), 2.4, HexColor('#00a8c6'))
    # bancada
    rect(c, X(10), Y(1670), 530 * sc, 1650 * sc, NUAGE, K, 0.6)
    txt(c, X(275), Y(845), 'BANCADA', 8, 'S-B', K, 'c', rot=90)
    txt(c, X(275) + 10, Y(845), '1650 × 530 · tampo a 840', 6.2, 'S', K70, 'c', rot=90)
    # vaso (posição de referência)
    rect(c, X(580), Y(180), 360 * sc, 180 * sc, white, K, 0.6)
    c.saveState(); c.setStrokeColor(K); c.setFillColor(white); c.setLineWidth(0.6)
    c.ellipse(X(580), Y(650), X(940), Y(190), stroke=1, fill=1); c.restoreState()
    txt(c, X(760), Y(430), 'VASO', 7.2, 'S-B', K, 'c')
    # porta (P4, leste)
    rect(c, X(PL_W), Y(1246), t * sc, 801 * sc, white, None)
    line(c, X(PL_W), Y(445), X(PL_W + t), Y(445), 0.6, K); line(c, X(PL_W), Y(1246), X(PL_W + t), Y(1246), 0.6, K)
    c.saveState(); c.setStrokeColor(K45); c.setLineWidth(0.6); c.setDash([3, 2])
    c.arc(X(PL_W + t) - 800 * sc, Y(445) - 800 * sc, X(PL_W + t) + 800 * sc, Y(445) + 800 * sc, -90, 90); c.restoreState()
    txt(c, X(PL_W + t) + 6, Y(845), 'PORTA', 7.4, 'S-B', K, 'l')
    txt(c, X(PL_W + t) + 6, Y(845) - 9, 'vão 800 · giro a conferir', 6.0, 'S', K70, 'l')
    # rótulos de parede
    if labels:
        txt(c, X(PL_W / 2), Y(-t) + 6, 'P5 · Norte · vaso', 7.6, 'S-B', K, 'c')
        txt(c, X(PL_W / 2), Y(PL_L + t) - 12, 'P1 · Sul · fundo do box', 7.6, 'S-B', K, 'c')
        txt(c, X(-t) - 8, Y(850), 'P3 · Oeste · bancada', 7.6, 'S-B', K, 'c', rot=90)
        txt(c, X(-t) - 8, Y(2150), 'P2', 7.6, 'S-B', K, 'c', rot=90)
        txt(c, X(160), Y(1690), 'P6', 6.6, 'S-B', MAGENTA, 'l')
        txt(c, X(PL_W + t) + 22, Y(1900), 'P4 · Leste · porta', 7.6, 'S-B', K, 'c', rot=-90)
        txt(c, X(1150), Y(2450), 'BOX', 8, 'S-B', K70, 'c')
    # ralos
    r1c = HexColor('#2b2b2b') if mode == 'agua' else HexColor('#7a7a7a')
    rect(c, X(177), Y(2497), 90 * sc, 720 * sc, r1c, None)
    rect(c, X(1108), Y(335), 100 * sc, 100 * sc, r1c, None)
    if mode == 'agua':
        txt(c, X(272), Y(2140), 'R1 · ralo linear 720 × 90', 6.6, 'S-B', K, 'l', rot=90)
        txt(c, X(1158), Y(335) - 9, 'R2 · 100 × 100', 6.6, 'S-B', K, 'c')
        # caimento
        line(c, X(1200), Y(2200), X(330), Y(2200), 0.9, HexColor('#00a8c6'))
        c.saveState(); c.setFillColor(HexColor('#00a8c6')); p = c.beginPath()
        p.moveTo(X(330), Y(2200)); p.lineTo(X(330) + 6, Y(2200) + 3); p.lineTo(X(330) + 6, Y(2200) - 3); p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()
        txt(c, X(800), Y(2200) + 4, 'caimento 1–2 % para R1', 6.2, 'S', K, 'c')
        # água quente
        red = HexColor('#b4432f')
        line(c, X(99), Y(1950), X(99), Y(930), 1.4, red, (5, 3))
        line(c, X(99), Y(930), X(300), Y(930), 1.4, red, (5, 3))
        txt(c, X(99) + 4, Y(1300), 'AQ · derivação a confirmar', 6.2, 'S-B', red, 'l', rot=90)
    if mode == 'luz':
        y_ = HexColor('#b07f20')
        for (x_, yy, lab, r) in ((696, 625, 'L1', 90), (960, 2165, 'L2', 50), (656, 2165, 'CH', 100)):
            c.saveState(); c.setStrokeColor(y_ if lab != 'CH' else K45); c.setFillColor(white); c.setLineWidth(1.0)
            c.circle(X(x_), Y(yy), r * sc, stroke=1, fill=1); c.restoreState()
            txt(c, X(x_), Y(yy) - 2.5, lab, 6.6, 'S-B', K, 'c')
        line(c, X(24), Y(20), X(24), Y(1670), 2.6, y_)
        txt(c, X(24) + 6, Y(1300), 'L3 · perfil linear 1650 mm sobre o espelho (parede P3)', 6.2, 'S-B', y_, 'l', rot=90)
    if mode == 'demo':
        hatch(c, X(0), Y(PL_L), PL_W * sc, PL_L * sc, 9, MAGENTA, 0.25)
    # cotas
    dimh(c, X(0), X(PL_W), Y(-t) + 22, '1.423 mm', 7.0, bold=True)
    dimh(c, X(152), X(PL_W), Y(PL_L + t) - 26, 'box 1.271', 6.4, above=False)
    dimv(c, X(-t) - 26, Y(PL_L), Y(0), '2.583 mm', 7.0, bold=True)
    dimv(c, X(-t) - 40, Y(1706), Y(0), '1.706', 6.4)
    dimv(c, X(-t) - 40, Y(PL_L), Y(1706), '877', 6.4)
