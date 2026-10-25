# -*- coding: utf-8 -*-
from lib import *
import calc_r1 as CR
from draw_r1 import *
from s_r1a import TOTAL, RT, R0S, SC20, SC10, fm

def cut_groups(pcs):
    g = {}
    for q in pcs:
        if q['kind'] != 'c': continue
        why = q['why'] or 'ponta'
        key = (why, round(q['x1'] - q['x0'], 1), round(q['y1'] - q['y0'], 1))
        g[key] = g.get(key, 0) + 1
    rows = []
    for (why, w, h), n in sorted(g.items(), key=lambda kv: -kv[1]):
        nome = {'ponta': 'Ponta', 'nicho': 'Contorno do nicho', 'porta': 'Contorno da porta'}.get(why, why.capitalize())
        rows.append([nome, '%s × %s' % (fm(w, 1), fm(h, 1)), str(n)])
    return rows

def marks_block(c, x, y, w, sid, xs):
    mx = [fm(a0, 1) for (a0, a1, t) in xs if t == 'f']
    y = para(c, x, y, w, 'Início de cada coluna inteira, em mm a partir do canto esquerdo da prancha:', 8.4, font='S-B')
    y = para(c, x, y - 1, w, ' · '.join(mx), 8.2) - 4
    y = para(c, x, y, w, 'Início de cada fiada, em mm a partir do piso acabado (iguais em todas as paredes):', 8.4, font='S-B')
    y = para(c, x, y - 1, w, ' · '.join(fm(y0) for (y0, y1, t) in CR.ROWS) + ' · topo 2.353', 8.2) - 4
    return y

def wall_sheet(c, n, sid, titulo, sub, notes, extra=None, ox=None):
    header(c, titulo, sub, n, TOTAL)
    w = CR.WALLS[sid]; sc = SC20
    ox = ox or MG + 90; oy = 300
    p, xs, pcs = draw_wall(c, ox, oy, sc, sid, nome='%s · %s' % (sid, w['nome']), tag='escala 1:20 · %s × 2.391 mm · U = 0 no canto esquerdo, como no R0' % fm(w['W']), name_dy=58)
    legend_tiles(c, ox - 40, oy - 30, 7.4)
    y = marks_block(c, ox - 40, oy - 52, max(w['W'] * sc + 140, 420), sid, xs)
    xr = max(ox + w['W'] * sc + 90, 560); wr = PW - MG - xr
    if extra:
        yr = extra(c, xr, PH - 130, wr)
    else:
        yr = PH - 130
    yr = section(c, xr, yr, 'Leitura', wr)
    for h, b in notes:
        yr = rich(c, xr, yr, wr, h, b, 9.0, 5)
    yr -= 12
    r = RT[sid]
    cw = (wr - 20) / 2
    ys = section(c, xr, yr, 'Quantidade', cw)
    rows = [['Área revestida', fm(r['area'], 2) + ' m²'], ['Peças Bleu Nuit', str(r['nb'])], ['Peças Nuage (acentos)', str(r['nn'])],
            ['Inteiras', str(r['full'])], ['Cortadas', str(r['cut'])]]
    table(c, xr, ys, [cw - 70, 70], None, rows, size=8.6, pad=3.2, aligns=['l', 'r'], bold_first=True, zebra=False)
    yc = section(c, xr + cw + 20, yr, 'Peças cortadas (L × A mm)', cw)
    table(c, xr + cw + 20, yc, [cw - 120, 80, 40], ['Corte', 'Medida', 'Qtd'], cut_groups(pcs), size=8.2, pad=3.0, aligns=['l', 'r', 'r'], hsize=8.0)
    footer(c, n, TOTAL)

# ---------------------------------------------------------------- nicho
def draw_nicho(c, x, y, wr):
    sc = SC10
    ns, area, nn = CR.nicho_surfaces()
    y = section(c, x, y, 'Nicho · N1 a N5 · escala 1:10 (mantido 1000 × 400 × 118 mm)', wr)
    rows = [(a0 - CR.NICHO['v0'], a1 - CR.NICHO['v0'], t) for (a0, a1, t) in ns['N1']['rows']]
    # N1
    by = y - 30 - 400 * sc
    bx = x + 40 * sc + 46
    def frame(xx, yy, w_, h_, lab):
        rect(c, xx, yy, w_ * sc, h_ * sc, JUNTA, K, 0.8)
        txt(c, xx, yy + h_ * sc + 4, lab, 7.6, 'S-B')
    frame(bx, by, 1000, 400, 'N1 · fundo')
    acc = {(0, 1), (4, 1)}
    for k in range(13):
        x0 = 1.9 + 77 * k
        for ri, (a0, a1, t) in enumerate(rows):
            nua = (k, ri) in acc
            full = (t == 'f')
            col = (NUAGE if full else NUAGE_CUT) if nua else (BLEU if full else BLEU_CUT)
            rect(c, bx + x0 * sc, by + a0 * sc, 75 * sc, (a1 - a0) * sc, col, JUNTA, 0.25)
    dimh(c, bx, bx + 1000 * sc, by - 10, '1.000', 6.4, above=False)
    for (a0, a1, t) in rows:
        txt(c, bx + 1000 * sc + 4, by + (a0 + a1) / 2 * sc - 2, fm(a1 - a0), 6.0, 'S', K70)
    # N2 / N3
    lx = bx + 1000 * sc + 34
    for k, lab in ((0, 'N2 · lateral esq.'), (1, 'N3 · lateral dir.')):
        xx = lx + k * (118 * sc + 26)
        frame(xx, by, 118, 400, lab)
        for (a0, a1, t) in rows:
            rect(c, xx, by + a0 * sc, 75 * sc, (a1 - a0) * sc, BLEU if t == 'f' else BLEU_CUT, JUNTA, 0.25)
            rect(c, xx + 77 * sc, by + a0 * sc, 41 * sc, (a1 - a0) * sc, BLEU_CUT, JUNTA, 0.25)
        txt(c, xx + 37 * sc, by - 9, 'frente', 5.8, 'S-I', K70, 'c')
    # N4 / N5
    y2 = by - 40 - 118 * sc
    for k, lab in ((0, 'N4 · base (caimento para fora)'), (1, 'N5 · teto')):
        yy = y2 - k * (118 * sc + 26)
        frame(bx, yy, 1000, 118, lab)
        for j in range(13):
            rect(c, bx + (1.9 + 77 * j) * sc, yy, 75 * sc, 118 * sc, BLEU_CUT, JUNTA, 0.25)
    return y2 - (118 * sc + 26) - 14

NOTES_P1 = [
    ('Eixo e pontas.', '15 colunas inteiras e pontas de 59 mm (79%) nos dois lados.'),
    ('Nicho.', 'Os lados do nicho (59 e 1.061 mm) caem exatamente nas juntas: nenhuma peça cortada na vertical em volta dele. Embaixo, a fiada F7 é aparada 6 mm (149 mm); em cima, a F10 sobra com 77 mm (50%).'),
    ('Dentro do nicho.', 'O fundo segue as 13 colunas e as fiadas da parede. Laterais com uma peça inteira na frente e corte de 41 mm junto ao fundo. Base e teto com peças de 118 mm. Base com caimento para fora e impermeabilização contínua.'),
    ('Acentos.', '8 Nuage na parede e 2 no fundo do nicho, sempre em peça inteira.'),
]
NOTES_P2 = [
    ('Eixo e pontas.', '10 colunas inteiras e pontas de 52,5 mm (70%) nos dois lados.'),
    ('Box.', 'Parede inteira dentro do box: impermeabilização até 2.400 mm antes de revestir. Pontos de chuveiro e registros no centro de uma peça ou exatamente na junta.'),
    ('Acentos.', '7 Nuage, em peça inteira.'),
]
NOTES_P3 = [
    ('Eixo e pontas.', '21 colunas inteiras e pontas de 43,5 mm (58%) nos dois lados, como o R0 já fazia; muda só a fiada do topo.'),
    ('Bancada.', 'Revestimento contínuo atrás do gabinete e do espelho, sem desconto de área. Tampo a 840 (fiada F6), base da borda frontal a 765 (F5), espelho a partir de 1.140 (F8).'),
    ('Pontos.', 'Bases do misturador, tomada e comando do L3: marcar sobre a malha antes de assentar; furo no centro da peça ou na junta.'),
    ('Acentos.', '12 Nuage, em peça inteira.'),
]
NOTES_P4 = [
    ('Eixo e pontas.', '32 colunas inteiras e pontas de 58,5 mm (78%) nos dois lados.'),
    ('Porta.', 'O batente do lado direito (2.137 mm) cai a 2,5 mm de uma junta: a guarnição cobre a folga. O do lado esquerdo (1.337 mm) corta a coluna C18 com 44,5 mm (59%).'),
    ('Verga.', 'A cabeça do vão a 1.990 mm corta a fiada F13 e deixa 49 mm acima da porta. Se a verga puder subir para 2.041 mm (junta da F13), o recorte some.'),
    ('Acentos.', '16 Nuage, em peça inteira.'),
]
NOTES_P5 = [
    ('Eixo e pontas.', '17 colunas inteiras e pontas de 58 mm (77%) nos dois lados.'),
    ('Vaso.', 'Vaso com caixa acoplada reaproveitado: engate e registro conferidos antes de assentar; ponto de alimentação no centro de uma peça ou na junta.'),
    ('Acentos.', '11 Nuage, em peça inteira.'),
]

def s09(c):
    wall_sheet(c, 9, 'P1', 'P1 · fundo do box e nicho', 'Parede do fundo do box com o nicho existente. Elevação 1:20 e detalhes do nicho 1:10.', NOTES_P1,
               extra=lambda c, x, y, w: draw_nicho(c, x, y, w))

def s10(c):
    header(c, 'P2 · lateral do box e P6 · retorno', 'As duas faces da área técnica. Elevações 1:20.', 10, TOTAL)
    sc = SC20; oy = 300
    ox = MG + 90
    p, xs, pcs = draw_wall(c, ox, oy, sc, 'P2', nome='P2 · Lateral do box / área técnica', tag='escala 1:20 · 877 × 2.391 mm', name_dy=58)
    ox6 = ox + 877 * sc + 90
    draw_wall(c, ox6, oy, sc, 'P6', chains='min', nome='P6 · Retorno', tag='150 × 2.391 mm', name_dy=58, axis=False)
    txt(c, ox6 + 150 * sc + 2, oy + 2391 * sc + 4, 'quina', 6.4, 'S-B', MAGENTA, 'l')
    legend_tiles(c, ox - 40, oy - 30, 7.4)
    marks_block(c, ox - 40, oy - 52, 430, 'P2', xs)
    xr = ox6 + 150 * sc + 70; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Leitura', wr)
    for h, b in NOTES_P2 + [('P6 · retorno.', 'Face de 150 mm entre a bancada (P3) e o box. Uma coluna inteira encostada na quina externa, com perfil de canto, e corte de 73 mm (97%) no canto interno com a P3. Sem acentos.')]:
        yr = rich(c, xr, yr, wr, h, b, 9.0, 5)
    yr -= 12
    cw = (wr - 20) / 2
    for k, sid in enumerate(('P2', 'P6')):
        r = RT[sid]; xx = xr + k * (cw + 20)
        ys = section(c, xx, yr, 'Quantidade · ' + sid, cw)
        table(c, xx, ys, [cw - 60, 60], None, [['Área', fm(r['area'], 2) + ' m²'], ['Bleu', str(r['nb'])], ['Nuage', str(r['nn'])],
                                               ['Inteiras', str(r['full'])], ['Cortadas', str(r['cut'])]], size=8.6, pad=3.2, aligns=['l', 'r'], bold_first=True, zebra=False)
    footer(c, 10, TOTAL)

def s11(c):
    wall_sheet(c, 11, 'P3', 'P3 · parede da bancada', 'Parede oeste com bancada, gabinete, espelho e perfil L3. Elevação 1:20.', NOTES_P3)

def s12(c):
    wall_sheet(c, 12, 'P4', 'P4 · parede da porta', 'Parede leste, de 2.583 mm, com o vão da porta preservado. Elevação 1:20.', NOTES_P4)

def s13(c):
    wall_sheet(c, 13, 'P5', 'P5 · parede do vaso', 'Parede norte, atrás do vaso. Elevação 1:20.', NOTES_P5)

def s14(c):
    header(c, 'Bancada · tampo e bordas', 'Tampo e bordas em Nuage, peça deitada (155 mm no sentido do comprimento). Escala 1:10, vista de cima e de frente.', 14, TOTAL)
    bs = CR.bancada(); sc = SC10
    ox = MG + 60; oy = 420
    b1 = bs['B1']
    def strip(xx, yy, xs_, h, lab, ys_=None):
        if ys_ is None: ys_ = [(0, h, 'f')]
        rect(c, xx, yy, xs_[-1][1] * sc, ys_[-1][1] * sc, JUNTA, K, 0.8)
        for (x0, x1, tx) in xs_:
            for (y0, y1, ty) in ys_:
                full = tx == 'f' and ty == 'f'
                rect(c, xx + x0 * sc, yy + y0 * sc, (x1 - x0) * sc, (y1 - y0) * sc, NUAGE if full else NUAGE_CUT, JUNTA, 0.3)
        txt(c, xx, yy + ys_[-1][1] * sc + 5, lab, 8.4, 'S-B')
    strip(ox, oy, b1['xs'], 530, 'B1 · tampo 1650 × 530 · frente embaixo, parede em cima', b1['ys'])
    txt(c, ox - 6, oy + 2, 'frente', 6.4, 'S-I', K70, 'r'); txt(c, ox - 6, oy + 530 * sc - 8, 'parede', 6.4, 'S-I', K70, 'r')
    txt(c, ox, oy - 12, 'sul', 6.4, 'S-I', K70, 'l'); txt(c, ox + 1650 * sc, oy - 12, 'norte', 6.4, 'S-I', K70, 'r')
    dimh(c, ox, ox + 1650 * sc, oy + 530 * sc + 22, '1.650 mm · 10 inteiras + corte de 80 mm na ponta norte', 7.0)
    dimv(c, ox + 1650 * sc + 18, oy, oy + 530 * sc, '530 · 6 fiadas + 68', 6.6, left=False)
    strip(ox, oy - 80, bs['B2']['xs'], 75, 'B2 · borda frontal 1650 × 75 (juntas alinhadas ao tampo)')
    strip(ox, oy - 160, bs['B3']['xs'], 75, 'B3 · borda sul 530 × 75 · frente à esquerda')
    strip(ox + 530 * sc + 60, oy - 160, bs['B4']['xs'], 75, 'B4 · borda norte 530 × 75 · frente à esquerda')
    xr = 700; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Leitura', wr)
    for h, b in [
        ('Tampo.', '10 peças inteiras por fiada e um corte de 80 mm (52%) na ponta norte, junto à parede P5, a menos vista. Seis fiadas inteiras a partir da frente e corte de 68 mm (91%) junto à parede.'),
        ('Bordas.', 'A borda frontal repete as colunas do tampo, com o mesmo corte de 80 mm no fim. Bordas sul e norte com três peças inteiras a partir da quina frontal e corte de 59 mm junto à parede.'),
        ('Quinas.', 'Encontro tampo/borda a 45° só depois de ensaio de corte com o fabricante; senão, peça sobreposta com perfil.'),
        ('Furos.', 'Cuba de apoio e bica só com o gabarito real das peças.'),
        ('Uso horizontal.', 'Gouache é revestimento de parede. O tampo depende de aprovação do fabricante e de base impermeável.'),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 9.2, 6)
    yr -= 12
    yr = section(c, xr, yr, 'Quantidade', wr)
    rows = []
    for k in ('B1', 'B2', 'B3', 'B4'):
        s = bs[k]; rows.append([k, s['nome'], fm(s['area'], 4), str(s['full']), str(s['cut']), str(s['full'] + s['cut'])])
    rows.append({'cells': ['Total', '', fm(sum(bs[k]['area'] for k in bs), 4), str(sum(bs[k]['full'] for k in bs)), str(sum(bs[k]['cut'] for k in bs)),
                           str(sum(bs[k]['full'] + bs[k]['cut'] for k in bs))], 'bold': True, 'fill': K08})
    table(c, xr, yr, [36, 150, 70, 60, 60, wr - 376], ['', 'Superfície', 'Área m²', 'Inteiras', 'Cortadas', 'Peças'], rows, size=8.6, pad=3.4,
          aligns=['l', 'l', 'r', 'r', 'r', 'r'], bold_first=True)
    footer(c, 14, TOTAL)

SHEETS = [s09, s10, s11, s12, s13, s14]
