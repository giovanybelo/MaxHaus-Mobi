# -*- coding: utf-8 -*-
"""Paginação R1 do banheiro MaxHaus (Gouache 75 × 155 mm, junta 2 mm).

Regras (em ordem de prioridade):
  1. Máximo de peças inteiras: fiadas inteiras desde o piso; o revestimento termina
     na última fiada inteira (2353 mm), sem fiada cortada no topo.
  2. Colunas simétricas no eixo de cada parede, com o maior número de peças inteiras
     em que o corte de ponta ainda tem pelo menos 40% da peça.
  3. Vãos existentes (nicho, porta) são preservados e recortados da malha, sem deslocá-la.
  4. Retorno estreito (P6, 150 mm): peça inteira na quina externa, corte no canto interno.
  5. Compra: área revestida × 1,10, arredondada para caixa fechada; conferida contra
     o número de peças físicas (cada peça cortada consome uma peça).
Unidades: mm.
"""
import json, math, os

A, B = 75.0, 155.0          # peça em pé: largura × altura
J = 2.0                     # junta
KERF = 2.0                  # perda do disco
MINF = 0.40                 # corte mínimo de ponta
H_TILE = 15 * B + 14 * J    # 2353: 15 fiadas inteiras
H_ROOM = 2391.0             # altura da superfície no modelo R47
PIECE_M2 = A * B / 1e6      # 0,011625
BOX_PCS, BOX_M2 = 26, 0.30
RESERVA = 0.10

HERE = os.path.dirname(os.path.abspath(__file__))
R0 = json.load(open(os.path.join(HERE, 'dados', 'r0.json')))

# ---------------------------------------------------------------- eixos
def cols_sym(W, a=A, j=J, minf=MINF):
    """Maior n de peças inteiras com pontas simétricas >= minf·a."""
    for n in range(int(W // a) + 1, 0, -1):
        c = (W - n * a - (n + 1) * j) / 2
        if minf * a <= c < a:
            return dict(n=n, c=c, j=j)
    raise ValueError(W)

def spans_sym(W, p, a=A, j=J):
    c = p['c']; out = [(0.0, c, 'c')]
    x = c + j
    for _ in range(p['n']):
        out.append((x, x + a, 'f')); x += a + j
    out.append((W - c, W, 'c'))
    return out

def spans_from(L, a, j, start_full_at_zero=True):
    """Peças inteiras a partir de 0 e uma sobra cortada no fim (se houver)."""
    out = []; x = 0.0
    while x + a <= L + 1e-6:
        out.append((x, x + a, 'f')); x += a + j
    if L - x > 1.0:
        out.append((x, L, 'c'))
    return out

ROWS = [(k * (B + J), k * (B + J) + B, 'f') for k in range(15)]   # 0 → 2353

# ---------------------------------------------------------------- superfícies
WALLS = {
    'P1': dict(nome='Fundo do box / nicho', W=1275.0, face='Sul', hole=[(59.1, 1060.7, 1091.0, 1491.0, 'nicho')]),
    'P2': dict(nome='Lateral do box / área técnica', W=877.0, face='Oeste (box)', hole=[]),
    'P3': dict(nome='Parede da bancada e espelho', W=1706.0, face='Oeste', hole=[]),
    'P4': dict(nome='Parede da porta', W=2583.0, face='Leste', hole=[(1337.0, 2137.0, 0.0, 1990.0, 'porta')]),
    'P5': dict(nome='Parede do vaso sanitário', W=1427.0, face='Norte', hole=[]),
    'P6': dict(nome='Retorno da área técnica', W=150.0, face='Norte (retorno)', hole=[], quina='direita'),
}
ORDEM = ['P5', 'P4', 'P1', 'P2', 'P6', 'P3']      # volta ao redor do banheiro

def wall_cols(sid):
    w = WALLS[sid]
    if sid == 'P6':
        # quina externa à direita: peça inteira encostada nela, corte no canto interno
        W = w['W']; c = W - A - J
        return dict(n=1, c=c, j=J, asym=True), [(0.0, c, 'c'), (c + J, W, 'f')]
    p = cols_sym(w['W']); return p, spans_sym(w['W'], p)

def ov(p, o):
    x0 = max(p[0], o[0]); x1 = min(p[1], o[1]); y0 = max(p[2], o[2]); y1 = min(p[3], o[3])
    return (x0, x1, y0, y1) if (x1 - x0 > 1e-6 and y1 - y0 > 1e-6) else None

def remainder(p, o):
    """Retângulo que sobra de p tirando o (quando o corte é reto). None = sumiu; 'L' = recorte em L."""
    full_h = o[2] <= p[2] + 1e-6 and o[3] >= p[3] - 1e-6
    full_w = o[0] <= p[0] + 1e-6 and o[1] >= p[1] - 1e-6
    if full_h and full_w: return None
    if full_h:
        if o[0] <= p[0] + 1e-6: r = (o[1], p[1], p[2], p[3])
        else: r = (p[0], o[0], p[2], p[3])
    elif full_w:
        if o[2] <= p[2] + 1e-6: r = (p[0], p[1], o[3], p[3])
        else: r = (p[0], p[1], p[2], o[2])
    else:
        return 'L'
    if (r[1] - r[0]) < 10 or (r[3] - r[2]) < 10:   # lasca menor que 1 cm não existe
        return None
    return r

def wall_pieces(sid):
    w = WALLS[sid]; p, xs = wall_cols(sid)
    pcs = []
    for ci, (x0, x1, tx) in enumerate(xs):
        for ri, (y0, y1, ty) in enumerate(ROWS):
            pr = (x0, x1, y0, y1); geo = pr; kind = 'f' if tx == 'f' else 'c'
            why = None if tx == 'f' else 'ponta'
            gone = False
            for (hx0, hx1, hy0, hy1, hn) in w['hole']:
                o = ov(pr, (hx0, hx1, hy0, hy1))
                if not o: continue
                r = remainder(pr, o)
                if r is None: gone = True
                elif r == 'L': kind = 'c'; why = 'recorte em L (%s)' % hn
                else: geo = r; kind = 'c'; why = hn
            if gone: continue
            pcs.append(dict(ci=ci, ri=ri, x0=geo[0], x1=geo[1], y0=geo[2], y1=geo[3], kind=kind, why=why,
                            grid=pr, col='B'))
    # acentos Nuage: posição do R0 levada para a peça inteira mais próxima
    used = set()
    for (u, v) in R0[sid]['nuage'] if sid in R0 else []:
        cand = [q for q in pcs if q['kind'] == 'f' and (q['ci'], q['ri']) not in used]
        q = min(cand, key=lambda q: ((q['x0'] + q['x1']) / 2 - u) ** 2 + ((q['y0'] + q['y1']) / 2 - v) ** 2)
        q['col'] = 'N'; used.add((q['ci'], q['ri']))
    n = 0
    for q in sorted([q for q in pcs if q['col'] == 'N'], key=lambda q: (-q['ri'], q['ci'])):
        n += 1; q['tag'] = '%s-%02d' % (sid, n)
    return p, xs, pcs

def wall_area(sid):
    w = WALLS[sid]
    a = w['W'] * H_TILE
    for (hx0, hx1, hy0, hy1, hn) in w['hole']:
        a -= (hx1 - hx0) * (min(hy1, H_TILE) - hy0)
    return a / 1e6

# ---------------------------------------------------------------- nicho (1000 × 400 × 118, preservado)
NICHO = dict(u0=59.1, u1=1060.7, v0=1091.0, v1=1491.0, prof=118.0)
T_LAYER = 11.0      # peça 9 mm + argamassa

def nicho_surfaces():
    """Fundo alinhado às 13 colunas e às fiadas da parede; laterais, base e teto com peça em pé."""
    out = {}
    # N1 fundo: 13 colunas (as da parede, 61 → 1060) × fiadas 8 e 9 inteiras + fiada 10 cortada
    v0 = NICHO['v0'] + T_LAYER; v1 = NICHO['v1'] - T_LAYER
    rows = []
    for (y0, y1, t) in ROWS:
        a0 = max(y0, v0); a1 = min(y1, v1)
        if a1 - a0 > 10:
            rows.append((a0, a1, 'f' if (a1 - a0) > B - 1 else 'c'))
    out['N1'] = dict(nome='Nicho / fundo', W=1000.0, H=400.0, cols=13, rows=rows,
                     full=13 * sum(1 for r in rows if r[2] == 'f'), cut=13 * sum(1 for r in rows if r[2] == 'c'))
    # N2/N3 laterais 118 × 400: 1 coluna inteira + 1 corte de 41 mm, mesmas fiadas
    cl = NICHO['prof'] - A - J
    nr = len(rows); nf = sum(1 for r in rows if r[2] == 'f')
    for k, nm in (('N2', 'Nicho / lateral esquerda'), ('N3', 'Nicho / lateral direita')):
        out[k] = dict(nome=nm, W=118.0, H=400.0, cols=2, rows=rows, corte_col=cl,
                      full=nf, cut=nr * 2 - nf)
    # N4/N5 base e teto 1000 × 118: 13 peças em pé cortadas a 118 mm de comprimento
    for k, nm in (('N4', 'Nicho / base'), ('N5', 'Nicho / teto')):
        out[k] = dict(nome=nm, W=1000.0, H=118.0, cols=13, full=0, cut=13)
    area = (1.0 * 0.4 + 2 * 0.118 * 0.4 + 2 * 1.0 * 0.118)
    nuage = 2                                   # acentos do R0 no fundo
    return out, area, nuage

# ---------------------------------------------------------------- bancada (Nuage, peça deitada)
BANC = dict(L=1650.0, P=530.0, borda=75.0)
def bancada():
    lx = spans_from(BANC['L'], B, J)          # 10 inteiras + corte de 80 na ponta norte
    py = spans_from(BANC['P'], A, J)          # 6 fiadas inteiras a partir da frente + corte de 68 junto à parede
    b1_full = sum(1 for x in lx if x[2] == 'f') * sum(1 for y in py if y[2] == 'f')
    b1_tot = len(lx) * len(py)
    ends = spans_from(BANC['P'], B, J)        # bordas laterais: 3 inteiras + corte de 59 junto à parede
    s = dict(
        B1=dict(nome='Bancada / tampo', W=1650, H=530, xs=lx, ys=py, full=b1_full, cut=b1_tot - b1_full, area=1.650 * 0.530),
        B2=dict(nome='Bancada / borda frontal', W=1650, H=75, xs=lx, full=sum(1 for x in lx if x[2] == 'f'),
                cut=sum(1 for x in lx if x[2] == 'c'), area=1.650 * 0.075),
        B3=dict(nome='Bancada / borda sul', W=530, H=75, xs=ends, full=sum(1 for x in ends if x[2] == 'f'),
                cut=sum(1 for x in ends if x[2] == 'c'), area=0.530 * 0.075),
        B4=dict(nome='Bancada / borda norte', W=530, H=75, xs=ends, full=sum(1 for x in ends if x[2] == 'f'),
                cut=sum(1 for x in ends if x[2] == 'c'), area=0.530 * 0.075),
    )
    return s

# ---------------------------------------------------------------- totais
def totals():
    rows = []
    tw = dict(B_pcs=0, N_pcs=0, full=0, cut=0, area=0.0)
    for sid in ORDEM:
        p, xs, pcs = wall_pieces(sid)
        nb = sum(1 for q in pcs if q['col'] == 'B'); nn = sum(1 for q in pcs if q['col'] == 'N')
        full = sum(1 for q in pcs if q['kind'] == 'f'); cut = len(pcs) - full
        ar = wall_area(sid)
        rows.append(dict(id=sid, nome=WALLS[sid]['nome'], W=WALLS[sid]['W'], H=H_TILE, area=ar, nb=nb, nn=nn, full=full, cut=cut,
                         n=p['n'], c=p['c'], area_n=nn * PIECE_M2))
    ns, narea, nn = nicho_surfaces()
    for k in ('N1', 'N2', 'N3', 'N4', 'N5'):
        s = ns[k]; tot = s['full'] + s['cut']
        nnk = nn if k == 'N1' else 0
        ar = s['W'] * s['H'] / 1e6
        rows.append(dict(id=k, nome=s['nome'], W=s['W'], H=s['H'], area=ar, nb=tot - nnk, nn=nnk, full=s['full'], cut=s['cut'],
                         n=None, c=None, area_n=nnk * PIECE_M2))
    bs = bancada()
    for k in ('B1', 'B2', 'B3', 'B4'):
        s = bs[k]; tot = s['full'] + s['cut']
        rows.append(dict(id=k, nome=s['nome'], W=s['W'], H=s['H'], area=s['area'], nb=0, nn=tot, full=s['full'], cut=s['cut'],
                         n=None, c=None, area_n=s['area']))
    res = {}
    for col in ('B', 'N'):
        if col == 'B':
            area = sum(r['area'] - r['area_n'] for r in rows)
            pcs = sum(r['nb'] for r in rows)
        else:
            area = sum(r['area_n'] for r in rows)
            pcs = sum(r['nn'] for r in rows)
        m2 = area * (1 + RESERVA)
        cx = math.ceil(m2 / BOX_M2 - 1e-9)
        res[col] = dict(area=area, m2_compra=m2, caixas=cx, pcs_compradas=cx * BOX_PCS, pcs_fisicas=pcs,
                        folga=cx * BOX_PCS / pcs - 1)
    return rows, res

if __name__ == '__main__':
    rows, res = totals()
    for r in rows:
        extra = '' if r['n'] is None else ' n=%d c=%.1f (%d%%)' % (r['n'], r['c'], round(r['c'] / A * 100))
        print('%-3s %-30s %6.0f × %5.0f área %.4f  Bleu %4d Nuage %3d  inteiras %4d cortadas %3d%s' %
              (r['id'], r['nome'], r['W'], r['H'], r['area'], r['nb'], r['nn'], r['full'], r['cut'], extra))
    for k, v in res.items():
        print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items()})
    print('soma área', round(sum(r['area'] for r in rows), 3), 'peças', sum(r['nb'] + r['nn'] for r in rows),
          'inteiras', sum(r['full'] for r in rows), 'cortadas', sum(r['cut'] for r in rows))
