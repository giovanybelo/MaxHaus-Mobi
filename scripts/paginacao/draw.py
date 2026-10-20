# -*- coding: utf-8 -*-
"""Desenho de paredes (elevações) e esquemas."""
from lib import *
import engine as E
import calc as C

def marks_x(xs):
    return [a0 for (a0, a1, t) in xs if t == 'f']

def draw_wall(c, ox, oy, sc, w, opt, chains='full', idx_rows=True, idx_cols=True, vchain=True, nome=None, tag=None, fill_box=True, name_dy=None):
    """Elevação da parede em (ox, oy) = canto inferior esquerdo; sc = pt por cm."""
    W, H = w['W'], w['H']
    hp, vp = C.plan(W, H, opt)
    xs = E.spans(W, opt['a'], hp); ys = E.spans(H, opt['b'], vp)
    X = lambda v: ox + v * sc
    Y = lambda v: oy + v * sc
    box = w.get('box'); door = w.get('door')
    rect(c, X(0), Y(0), W * sc, H * sc, GROUT, None)
    c.saveState()
    if door:
        p = c.beginPath()
        p.rect(X(0) - 6, Y(0) - 6, W * sc + 12, H * sc + 12)
        p.rect(X(door[0]), Y(door[2]), (door[1] - door[0]) * sc, (door[3] - door[2]) * sc)
        c.clipPath(p, stroke=0, fill=0, fillMode=0)
    for (x0, x1, tx) in xs:
        for (y0, y1, ty) in ys:
            pr = (x0, x1, y0, y1)
            cut = (tx == 'c' or ty == 'c')
            if door and C.ov(pr, door): cut = True
            cx = (x0 + x1) / 2
            inbox = fill_box and box and box[0] <= cx <= box[1]
            fill = AMARELO45 if cut else (CIANO18 if inbox else white)
            rect(c, X(x0), Y(y0), (x1 - x0) * sc, (y1 - y0) * sc, fill, K, 0.22)
    c.restoreState()
    if door:
        dx0, dx1, dy0, dy1 = door
        rect(c, X(dx0), Y(dy0), (dx1 - dx0) * sc, (dy1 - dy0) * sc, white, K, 0.9)
        hatch(c, X(dx0), Y(dy0), (dx1 - dx0) * sc, (dy1 - dy0) * sc, 5, K45, 0.35)
        txt(c, X((dx0 + dx1) / 2), Y(dy1 / 2), 'P02', 8, 'S-B', K, 'c')
        txt(c, X((dx0 + dx1) / 2), Y(dy1 / 2) - 10, 'vão 0,80 × 2,00', 6.4, 'S', K70, 'c')
    rect(c, X(0), Y(0), W * sc, H * sc, None, K, 1.1)
    # vidro K01
    if w.get('k01') is not None:
        xk = w['k01']
        rect(c, X(xk) - 1.4, Y(0), 2.8, H * sc, CIANO, K, 0.5)
    # bancada (indicativa)
    if w.get('bancada'):
        b0, b1 = w['bancada']
        rect(c, X(b0), Y(0), (b1 - b0) * sc, 90 * sc, None, K70, 0.7, (3, 2))
        txt(c, X((b0 + b1) / 2), Y(45), 'bancada', 6.4, 'S-I', K70, 'c')
        txt(c, X((b0 + b1) / 2), Y(45) - 8, '(indicativa)', 6.0, 'S-I', K70, 'c')
    # eixo central
    line(c, X(W / 2), Y(0) - 7, X(W / 2), Y(H) + 7, 0.8, MAGENTA, (5, 1.6, 1, 1.6))
    if chains:
        cc = hp['c']
        y1 = Y(H) + 12
        if chains == 'full':
            dimh(c, X(0), X(cc), y1, fx(cc, 2), 6.4)
            dimh(c, X(cc), X(W - cc), y1, '%d inteiras · módulo %s' % (hp['n'], fx(opt['a'] + hp['j'], 2)), 6.4)
            dimh(c, X(W - cc), X(W), y1, fx(cc, 2), 6.4)
            dimh(c, X(0), X(W), y1 + 15, f(W, 1) + ' cm', 7.2, bold=True)
            txt(c, X(W / 2), y1 + 27, 'EIXO', 6.4, 'S-B', MAGENTA, 'c', ls=0.8)
        else:
            dimh(c, X(0), X(W), y1, f(W, 1) + ' cm', 7.0, bold=True)
            txt(c, X(W / 2), y1 + 12, 'EIXO', 6.0, 'S-B', MAGENTA, 'c', ls=0.8)
        if vchain:
            cv = vp['c']; xl = X(0) - 14
            if chains == 'full':
                dimv(c, xl, Y(0), Y(cv), fx(cv, 2), 6.4)
                dimv(c, xl, Y(cv), Y(H - cv), '%d fiadas · módulo %s' % (vp['n'], fx(opt['b'] + vp['j'], 2)), 6.4)
                dimv(c, xl, Y(H - cv), Y(H), fx(cv, 2), 6.4)
                dimv(c, xl - 15, Y(0), Y(H), f(H, 1) + ' cm', 7.2, bold=True)
            else:
                dimv(c, xl, Y(0), Y(cv), fx(cv, 2), 6.0)
                dimv(c, xl, Y(cv), Y(H - cv), '%d fiadas' % vp['n'], 6.0)
                dimv(c, xl, Y(H - cv), Y(H), fx(cv, 2), 6.0)
        if w.get('k01') is not None:
            txt(c, X(w['k01']), Y(H) + 3, 'K01', 6.6, 'S-B', K, 'c')
    if idx_rows:
        for ri, (y0, y1_, t) in enumerate(ys):
            txt(c, X(W) + 4, Y((y0 + y1_) / 2) - 2.2, 'F%d' % (ri + 1), 5.8, 'S', K70)
    if idx_cols:
        colw = opt['a'] * sc
        step = 1 if colw >= 14 else (2 if colw >= 9 else 5)
        for ci, (x0, x1, t) in enumerate(xs):
            n_ = ci + 1
            if step == 1 or n_ % step == 0 or n_ == 1 or n_ == len(xs):
                txt(c, X((x0 + x1) / 2), Y(0) - 9, 'C%d' % n_, 5.6, 'S', K70, 'c')
    dy = name_dy if name_dy is not None else (48 if chains == 'full' else 26)
    if nome:
        txt(c, X(0), Y(H) + dy, nome, 11, 'S-B')
    if tag:
        txt(c, X(0), Y(H) + dy - 11, tag, 7.0, 'S', K70)
    return dict(hp=hp, vp=vp, xs=xs, ys=ys)

def marks_text(xs, ys, vp, opt, hp):
    mx = [f(a0, 1) for (a0, a1, t) in xs if t == 'f']
    my = [f(y0, 1) for (y0, y1, t) in ys if t == 'f']
    return mx, my

def schematic_axis(c, x, y, wpt, hpt, W, a, hp, label, opt_color=True):
    """Esquema de uma linha de peças (corte simétrico) em escala horizontal."""
    sc = wpt / W
    xs = E.spans(W, a, hp)
    for (x0, x1, t) in xs:
        rect(c, x + x0 * sc, y, (x1 - x0) * sc, hpt, AMARELO45 if t == 'c' else white, K, 0.4)
    line(c, x + W * sc / 2, y - 6, x + W * sc / 2, y + hpt + 6, 0.8, MAGENTA, (4, 1.5, 1, 1.5))
    txt(c, x, y + hpt + 12, label, 7.6, 'S-B')
