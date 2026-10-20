# -*- coding: utf-8 -*-
import math
import engine as E

H_BANHEIRO = 240.0
ROW_J = 0.30                       # junta entre fiadas (uniforme nas 4 paredes: as fiadas fecham nos cantos)

# Opções de peça (formato real, ficha Portobello da linha de mesmo formato)
OPTS = {
    'A': dict(k='A', nome='Opção A', fmt='15,5 × 15,5 cm', a=15.5, b=15.5, ppb=36, m2box=0.87, jmed=0.30),
    'B': dict(k='B', nome='Opção B', fmt='7,5 × 15,5 cm', a=7.5, b=15.5, ppb=26, m2box=0.30, jmed=0.30),
}

# Paredes (vistas de dentro). Coordenadas x a partir do canto ESQUERDO da vista, y a partir do piso acabado.
WALLS = {
    'NORTE': dict(W=143.0, H=240.0, vista='olhando para o norte (esquerda = oeste)'),
    'LESTE': dict(W=264.0, H=240.0, vista='olhando para o leste (esquerda = norte)',
                  door=(45.5, 125.5, 0.0, 200.0), k01=171.1, box=(171.1, 264.0)),
    'SUL':   dict(W=143.0, H=240.0, vista='olhando para o sul (esquerda = leste)', box=(0.0, 143.0), r02=True),
    'OESTE': dict(W=264.0, H=240.0, vista='olhando para o oeste (esquerda = sul)',
                  k01=92.9, box=(0.0, 92.9), bancada=(154.9, 216.2)),
}
ORDEM = ['NORTE', 'LESTE', 'SUL', 'OESTE']       # sentido horário, visto de dentro
L2 = dict(W=358.0, H=260.0, vista='parede Leste de 358 × 260 cm (a confirmar)')

def ov(p, o):
    """Interseção de dois retângulos (x0,x1,y0,y1) -> retângulo ou None"""
    x0 = max(p[0], o[0]); x1 = min(p[1], o[1]); y0 = max(p[2], o[2]); y1 = min(p[3], o[3])
    if x1 - x0 > 1e-6 and y1 - y0 > 1e-6: return (x0, x1, y0, y1)
    return None

def plan(W, H, opt):
    hp = E.plan_axis(W, opt['a'], 0.25, 0.35)
    vp = E.plan_axis(H, opt['b'], ROW_J, ROW_J)
    return hp, vp

def wall_pieces(w, opt):
    """Lista de peças da parede com tipo, após o recorte do vão."""
    W, H = w['W'], w['H']
    hp, vp = plan(W, H, opt)
    xs = E.spans(W, opt['a'], hp); ys = E.spans(H, opt['b'], vp)
    door = w.get('door')
    pcs = []
    for ci, (x0, x1, tx) in enumerate(xs):
        for ri, (y0, y1, ty) in enumerate(ys):
            p = (x0, x1, y0, y1)
            rem = False; part = None
            if door:
                o = ov(p, door)
                if o:
                    area_o = (o[1]-o[0])*(o[3]-o[2]); area_p = (x1-x0)*(y1-y0)
                    full_h = o[2] <= y0 + 1e-6 and o[3] >= y1 - 1e-6
                    full_w = o[0] <= x0 + 1e-6 and o[1] >= x1 - 1e-6
                    if area_o > area_p - 1e-6: rem = True
                    elif full_h and (x1 - x0) - (o[1] - o[0]) < 1.0: rem = True      # lasca menor que 1 cm não existe
                    elif full_w and (y1 - y0) - (o[3] - o[2]) < 1.0: rem = True
                    else: part = o
            pcs.append(dict(ci=ci, ri=ri, x0=x0, x1=x1, y0=y0, y1=y1, tx=tx, ty=ty, rem=rem, part=part))
    return hp, vp, xs, ys, pcs

def quant(w, opt):
    hp, vp, xs, ys, pcs = wall_pieces(w, opt)
    a = opt['a']
    pair = (2 * hp['c'] + E.KERF) <= a + 1e-6          # as duas pontas saem de uma mesma peça cortada ao meio
    grid = [p for p in pcs if not p['rem']]
    full = [p for p in grid if p['tx'] == 'f' and p['ty'] == 'f' and not p['part']]
    cut = [p for p in grid if p not in full]
    nrows = len(ys)
    # peças físicas
    phys = len(grid)
    pares = 0
    if pair:
        for ri in range(nrows):
            l = [p for p in grid if p['ri'] == ri and p['ci'] == 0]
            r = [p for p in grid if p['ri'] == ri and p['ci'] == len(xs) - 1]
            if l and r: pares += 1
        phys -= pares
    # operações de corte
    ops = 0
    for p in cut:
        n = (1 if p['tx'] == 'c' else 0) + (1 if p['ty'] == 'c' else 0)
        if p['part']:
            o = p['part']
            if o[0] > p['x0'] + 1e-6 or o[1] < p['x1'] - 1e-6: n += 1
            if o[2] > p['y0'] + 1e-6 or o[3] < p['y1'] - 1e-6: n += 1
        ops += max(n, 1)
    if pair:
        ops -= pares            # um corte separa as duas pontas
    nx = len(xs); ny = len(ys)
    rem = [p for p in pcs if p['rem']]
    return dict(hp=hp, vp=vp, xs=xs, ys=ys, nx=nx, ny=ny, grid=len(grid), full=len(full), cut=len(cut),
                phys=phys, pares=pares, ops=ops, removed=len(rem), pair=pair,
                area=w['W'] * w['H'] / 1e4 - (((w['door'][1]-w['door'][0])*(w['door'][3]-w['door'][2]))/1e4 if w.get('door') else 0))

def buy(phys, opt, reserve=0.10):
    need = math.ceil(phys * (1 + reserve))
    caixas = math.ceil(need / opt['ppb'])
    return need, caixas, caixas * opt['ppb'], caixas * opt['m2box']

def total(opt, reserve=0.10):
    rows = {}
    tp = tf = tc = to = 0
    for nm in ORDEM:
        q = quant(WALLS[nm], opt); rows[nm] = q
        tp += q['phys']; tf += q['full']; tc += q['cut']; to += q['ops']
    need, cx, pcs_c, m2c = buy(tp, opt, reserve)
    area = sum(rows[n]['area'] for n in ORDEM)
    return dict(rows=rows, phys=tp, full=tf, cut=tc, ops=to, need=need, caixas=cx, pcs_comprados=pcs_c, m2_comprado=m2c, area=area)

def jamb_info(opt):
    """Cortes que o vão da porta (Leste) produz nas colunas e nas fiadas."""
    w = WALLS['LESTE']; hp, vp, xs, ys, pcs = wall_pieces(w, opt)
    x0d, x1d, _, y1d = w['door']
    res = {}
    # coluna que contém a aresta esquerda e a direita
    for nome, xd in (('esq', x0d), ('dir', x1d)):
        for ci, (a0, a1, t) in enumerate(xs):
            if a0 - 1e-6 <= xd <= a1 + 1e-6:
                res[nome] = dict(ci=ci + 1, a0=a0, a1=a1, xd=xd,
                                 fora=(xd - a0) if nome == 'esq' else (a1 - xd),
                                 junta_d=min(abs(xd - a0), abs(xd - a1)))
                break
        else:
            # caiu numa junta
            for ci in range(len(xs) - 1):
                if xs[ci][1] < xd < xs[ci + 1][0]:
                    res[nome] = dict(ci=ci + 1, a0=xs[ci][1], a1=xs[ci + 1][0], xd=xd, fora=0.0, junta_d=0.0, naJunta=True)
    for ri, (b0, b1, t) in enumerate(ys):
        if b0 - 1e-6 <= y1d <= b1 + 1e-6:
            res['topo'] = dict(ri=ri + 1, b0=b0, b1=b1, fora=b1 - y1d)
    return res

def k01_info(opt):
    out = {}
    for nm in ('LESTE', 'OESTE'):
        w = WALLS[nm]; hp, vp, xs, ys, pcs = wall_pieces(w, opt)
        xk = w['k01']; best = None
        for ci, (a0, a1, t) in enumerate(xs):
            if a0 <= xk <= a1: best = ('peça', ci + 1, min(xk - a0, a1 - xk))
        if best is None:
            for ci in range(len(xs) - 1):
                if xs[ci][1] < xk < xs[ci + 1][0]: best = ('junta', ci + 1, 0.0)
        # distância à junta mais próxima
        d = min(min(abs(xk - s[0]), abs(xk - s[1])) for s in xs)
        out[nm] = (best, d)
    return out

if __name__ == '__main__':
    for k, o in OPTS.items():
        t = total(o)
        print('\n==', o['nome'], o['fmt'])
        for nm in ORDEM:
            q = t['rows'][nm]
            print(f"{nm:6s} cols {q['nx']:2d} (n={q['hp']['n']}, c={q['hp']['c']:.2f}, j={q['hp']['j']*10:.2f}mm, {q['hp']['mode']}) rows {q['ny']} (c={q['vp']['c']:.2f}) "
                  f"grid {q['grid']} inteiras {q['full']} cortadas {q['cut']} fis {q['phys']} par {q['pares']} ops {q['ops']} rem {q['removed']} area {q['area']:.2f}")
        print('TOTAL físicas', t['phys'], 'inteiras', t['full'], 'cortadas', t['cut'], 'cortes', t['ops'], '+10% =', t['need'], 'caixas', t['caixas'], 'pcs', t['pcs_comprados'], 'm2', round(t['m2_comprado'], 2), 'area líq', round(t['area'], 2))
        print('vão:', jamb_info(o)); print('K01:', k01_info(o))
    # L2
    for k, o in OPTS.items():
        hp, vp = plan(L2['W'], L2['H'], o)
        print('L2', k, hp, vp)
