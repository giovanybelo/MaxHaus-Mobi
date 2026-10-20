# -*- coding: utf-8 -*-
from lib import *
import engine as E
import calc as C
from draw import *
from sheets_a import TOTAL, A, B, TA, TB, pct

SC25 = 1.1339      # 1:25 em pt por cm
SC20 = 1.4173      # 1:20

def eixo_txt(hp):
    n = hp['n']
    if n % 2 == 1:
        return 'peça inteira C%d centrada no eixo' % (1 + (n + 1) // 2)
    return 'junta do eixo entre C%d e C%d' % (1 + n // 2, 2 + n // 2)

def marks_blocks(c, x, y, w, nm, opt, size=8.2):
    wl = C.WALLS[nm]
    hp, vp, xs, ys, _ = C.wall_pieces(wl, opt)
    mx = [f(a0, 1) for (a0, a1, t) in xs if t == 'f']
    my = [f(y0, 1) for (y0, y1, t) in ys if t == 'f']
    y = para(c, x, y, w, 'Início de cada peça inteira, em cm a partir do canto esquerdo:', size, font='S-B')
    y = para(c, x, y - 1, w, ' · '.join(mx), size) - 4
    y = para(c, x, y, w, 'Início de cada fiada inteira, em cm a partir do piso acabado:', size, font='S-B')
    y = para(c, x, y - 1, w, ' · '.join(my), size) - 4
    return y

def legenda_padrao(c, x, y, size=7.8):
    return legend(c, x, y, [('full', 'peça inteira'), ('cut', 'peça com corte'), ('wet', 'zona do box'), ('door', 'vão P02'),
                            ('k01', 'vidro K01'), ('axis', 'eixo da parede')], size, 16)

def resumo_table(c, x, y, opt, T, size=8.4):
    head = ['Parede', 'Malha (colunas × fiadas)', 'Inteiras na linha', 'Corte das pontas', 'Fiada piso · topo', 'Peças inteiras', 'Peças com corte', 'Peças físicas', 'Cortes']
    rows = []
    for nm in C.ORDEM:
        q = T['rows'][nm]; hp = q['hp']; vp = q['vp']
        j = '' if abs(hp['j'] - 0.3) < 1e-6 else ' (junta %s mm)' % fx(hp['j'] * 10, 1)
        rows.append([nm, '%d × %d' % (q['nx'], q['ny']), str(hp['n']), '%s cm · %s%s' % (fx(hp['c'], 2), pct(hp['c'], opt['a']), j),
                     '%s · %s cm' % (fx(vp['c'], 2), fx(vp['c'], 2)), str(q['full']), str(q['cut']), str(q['phys']), str(q['ops'])])
    rows.append({'cells': ['Total', '', '', '', '', str(T['full']), str(T['cut']), str(T['phys']), str(T['ops'])], 'bold': True, 'fill': K08})
    return table(c, x, y, [62, 90, 62, 132, 88, 58, 64, 62, 48], head, rows, size=size, pad=3.6,
                 aligns=['l', 'c', 'c', 'l', 'l', 'r', 'r', 'r', 'r'], bold_first=True, hsize=size - 0.4)

def s_plan(c, opt, nf):
    T = TA if opt['k'] == 'A' else TB
    header(c, '%s · %s · planificação das quatro paredes' % (opt['nome'], opt['fmt']),
           'As quatro paredes abertas em sequência, vistas de dentro, escala 1:25. As fiadas atravessam os cantos na mesma altura. '
           'Cada parede tem o eixo no centro e o mesmo corte nas duas pontas.', nf, TOTAL)
    ox = MG + 64; oy = 392
    x = ox
    for nm in C.ORDEM:
        w = C.WALLS[nm]
        draw_wall(c, x, oy, SC25, w, opt, chains='min', idx_rows=(nm == 'OESTE'), idx_cols=False, vchain=(nm == 'NORTE'),
                  nome='%s · %s × %s' % (nm, f(w['W'], 0), f(w['H'], 0)), tag=w['vista'], name_dy=48)
        x += w['W'] * SC25
    # cantos
    x = ox
    for nm in C.ORDEM[:-1]:
        x += C.WALLS[nm]['W'] * SC25
        line(c, x, oy - 10, x, oy + 240 * SC25 + 6, 1.6, K)
        txt(c, x, oy - 19, 'canto', 6.4, 'S-I', K70, 'c')
    legenda_padrao(c, ox, oy - 38)
    y = oy - 62
    yb = resumo_table(c, MG, y, opt, T)
    # notas
    xn = MG + 740; wn = PW - MG - xn
    yn = section(c, xn, y + 6, 'Leitura', wn)
    hpN = T['rows']['NORTE']['hp']; hpL = T['rows']['LESTE']['hp']
    notas = [
        ('Mesma malha, espelhada.', 'Norte e Sul usam a mesma régua (%s), e Leste e Oeste também (%s).' % (eixo_txt(hpN), eixo_txt(hpL))),
        ('Fiadas contínuas.', '%d fiadas inteiras e cortes de %s cm no piso e no forro, nas quatro paredes: a junta horizontal não quebra no canto.' %
         (T['rows']['NORTE']['vp']['n'], fx(T['rows']['NORTE']['vp']['c'], 2))),
        ('Fiada de piso e de topo.', 'Cortar 3 a 5 mm menores que o desenhado, para a junta de movimentação contra piso e forro. Medir a cota real antes (Prancha 15).'),
    ]
    for h, b in notas:
        yn = rich(c, xn, yn, wn, h, b, 9.0, 5)
    footer(c, nf, TOTAL)

def vao_notes(opt):
    ji = C.jamb_info(opt); ki = C.k01_info(opt)
    a = opt['a']
    out = []
    e = ji['esq']; d = ji['dir']
    if e['fora'] < 1.0:
        out.append(('Batente esquerdo do P02 (45,5 cm).', 'Cai na junta entre C%d e C%d, a %s cm dela. O batente cobre a folga de cerca de 5 mm entre peça e madeira. Nenhum corte estreito.' %
                    (e['ci'] - 1, e['ci'], fx(e['fora'], 2))))
    else:
        s = 'Corta a coluna C%d e sobra uma faixa de %s cm (%s da peça).' % (e['ci'], fx(e['fora'], 2), pct(e['fora'], a))
        out.append(('Batente esquerdo do P02 (45,5 cm).', s + (' É estreita: confirmar a posição do batente instalado antes de cortar.' if e['fora'] / a < 0.40 else '')))
    if d['fora'] < 1.0:
        out.append(('Batente direito do P02 (125,5 cm).', 'Cai na junta entre C%d e C%d.' % (d['ci'] - 1, d['ci'])))
    else:
        s = 'Corta a coluna C%d e sobra uma faixa de %s cm (%s da peça).' % (d['ci'], fx(d['fora'], 2), pct(d['fora'], a))
        out.append(('Batente direito do P02 (125,5 cm).', s + (' No limite de 1/3: conferir o batente instalado antes de cortar.' if d['fora'] / a < 0.40 else '')))
    t = ji['topo']
    out.append(('Cabeça do vão (2,00 m).', 'Corta a fiada F%d e sobra %s cm (%s da peça) acima do vão. O canto direito pede um recorte em L pequeno.' % (t['ri'], fx(t['fora'], 2), pct(t['fora'], opt['b']))))
    kl, ko = ki['LESTE'], ki['OESTE']
    if kl[1] < 1.0:
        out.append(('Vidro K01.', 'Nas duas paredes o vidro cai a %s cm de uma junta vertical: perfil e junta ficam alinhados.' % fx(max(kl[1], ko[1]), 2)))
    else:
        out.append(('Vidro K01.', 'Cai a %s cm da junta mais próxima, no meio de uma peça. O perfil do vidro (opção B de K01) assenta sobre a peça, não na junta.' % fx(min(kl[1], ko[1]), 1)))
    return out

def s_elev_ns(c, opt, nf):
    T = TA if opt['k'] == 'A' else TB
    header(c, '%s · elevações Norte e Sul' % opt['nome'],
           'Peça %s cm, escala 1:20, vistas de dentro. As duas paredes têm a mesma malha. A Sul é a parede nova R02, no fundo do box.' % opt['fmt'],
           nf, TOTAL)
    oy = 300
    xN = MG + 84
    xS = xN + 143 * SC20 + 118
    tN = 'olhando para o norte · esquerda = oeste'; tS = 'olhando para o sul · esquerda = leste'
    draw_wall(c, xN, oy, SC20, C.WALLS['NORTE'], opt, nome='NORTE · 143 × 240', tag=tN, name_dy=64)
    draw_wall(c, xS, oy, SC20, C.WALLS['SUL'], opt, nome='SUL · 143 × 240', tag=tS, name_dy=64)
    legenda_padrao(c, xN - 30, oy - 30, 7.4)
    # marcas
    xm = xN - 30; wm = 560
    y = oy - 54
    y = section(c, xm, y, 'Régua de modulação · Norte e Sul', wm)
    y = marks_blocks(c, xm, y, wm, 'NORTE', opt, 8.6)
    # painel direito
    xr = 760; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Leitura das paredes', wr)
    q = T['rows']['NORTE']; hp = q['hp']; vp = q['vp']
    textos = [
        ('Eixo e pontas.', 'Eixo a %s cm do canto. %d peças inteiras por fiada, %s. Pontas de %s cm (%s da peça) nos dois lados%s.' %
         (f(143 / 2, 1), hp['n'], eixo_txt(hp), fx(hp['c'], 2), pct(hp['c'], opt['a']), '; as duas saem da mesma peça cortada ao meio' if q['pair'] else '')),
        ('Fiadas.', '%d fiadas inteiras entre duas de %s cm (piso e forro). Mesma altura das paredes Leste e Oeste.' % (vp['n'], fx(vp['c'], 2))),
        ('NORTE.', 'Parede lisa, sem ponto elétrico ou hidráulico. Os embutidos EM ficam no forro.'),
        ('SUL (R02).', 'Parede nova do fundo do box, toda molhada: a impermeabilização precisa subir antes do revestimento (altura a decidir, Prancha 16). Pontos do chuveiro e dos registros: centro da peça ou junta.'),
        ('Cantos.', 'Canto interno com junta de movimentação selada, sem rejunte rígido. Peças de ponta de uma parede encostam na da vizinha com 3 a 5 mm de folga.'),
    ]
    for h, b in textos:
        yr = rich(c, xr, yr, wr, h, b, 9.0, 5)
    yr -= 18
    yr = section(c, xr, yr, 'Quantidade por parede', wr)
    rows = []
    for nm in ('NORTE', 'SUL'):
        qq = T['rows'][nm]
        rows.append([nm, '%d × %d' % (qq['nx'], qq['ny']), str(qq['full']), str(qq['cut']), str(qq['phys']), str(qq['ops'])])
    table(c, xr, yr, [64, 70, 58, 68, 74, wr - 334], ['Parede', 'Malha', 'Inteiras', 'Com corte', 'Físicas', 'Cortes'], rows,
          size=8.6, pad=3.6, aligns=['l', 'c', 'r', 'r', 'r', 'r'], bold_first=True)
    footer(c, nf, TOTAL)

def s_elev_lo(c, opt, nf):
    T = TA if opt['k'] == 'A' else TB
    header(c, '%s · elevações Leste e Oeste' % opt['nome'],
           'Peça %s cm, escala 1:25, vistas de dentro. A malha é a mesma nas duas paredes. A Leste leva a porta P02; as duas levam o vidro K01 e a zona do box.' % opt['fmt'],
           nf, TOTAL)
    sc = SC25
    oy = 376
    xL = MG + 84
    xO = xL + 264 * sc + 112
    draw_wall(c, xL, oy, sc, C.WALLS['LESTE'], opt, nome='LESTE · 264 × 240', tag='olhando para o leste · esquerda = norte', name_dy=60)
    draw_wall(c, xO, oy, sc, C.WALLS['OESTE'], opt, nome='OESTE · 264 × 240', tag='olhando para o oeste · esquerda = sul', name_dy=60)
    legenda_padrao(c, xL - 30, oy - 30, 7.6)
    wl = xO + 264 * sc - (xL - 30)
    y = oy - 54
    yy = section(c, xL - 30, y, 'Régua de modulação · Leste e Oeste', wl)
    yb = marks_blocks(c, xL - 30, yy, wl, 'LESTE', opt, 8.8)
    y3 = yb - 14
    wcol = (wl - 28) / 2
    x2 = xL - 30; x3 = x2 + wcol + 28
    notes = vao_notes(opt)
    cy = section(c, x2, y3, 'Vão da porta P02 (Leste)', wcol)
    for h, b in notes[:3]:
        cy = rich(c, x2, cy, wcol, h, b, 9.0, 5)
    cz = section(c, x3, y3, 'Vidro K01 e bancada', wcol)
    for h, b in notes[3:]:
        cz = rich(c, x3, cz, wcol, h, b, 9.0, 5)
    cz = rich(c, x3, cz, wcol, 'Bancada (Oeste).', 'Desenhada só como referência, de 154,9 a 216,2 cm. O revestimento corre por trás dela. Altura do espelho e da bancada ainda a definir.', 9.0, 5)
    # painel direito
    xr = 906; wr = PW - MG - xr
    q = T['rows']['LESTE']; hp = q['hp']; vp = q['vp']
    yr = section(c, xr, PH - 130, 'Malha', wr)
    for h, b in [
        ('Eixo e pontas.', 'Eixo a 132 cm do canto. %d inteiras por fiada, %s. Pontas de %s cm (%s)%s.' %
         (hp['n'], eixo_txt(hp), fx(hp['c'], 2), pct(hp['c'], opt['a']),
          ', iguais nas duas paredes' + ('; junta de %s mm entre colunas, para fechar a meia peça' % fx(hp['j'] * 10, 2) if hp['mode'] == 'meia' else ''))),
        ('Fiadas.', '%d inteiras e cortes de %s cm no piso e no forro, iguais às paredes Norte e Sul.' % (vp['n'], fx(vp['c'], 2))),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 9.0, 5)
    yr -= 14
    yr = section(c, xr, yr, 'Quantidade', wr)
    rows = []
    for nm in ('LESTE', 'OESTE'):
        qq = T['rows'][nm]
        rows.append([nm, '%d × %d' % (qq['nx'], qq['ny']), str(qq['full']), str(qq['cut']), str(qq['phys']), str(qq['ops'])])
    yr = table(c, xr, yr, [48, 44, 36, 40, 36, wr - 204], ['Parede', 'Malha', 'Int.', 'Corte', 'Fís.', 'Cortes'], rows,
               size=8.2, pad=3.2, aligns=['l', 'c', 'r', 'r', 'r', 'r'], bold_first=True, hsize=7.8)
    para(c, xr, yr - 6, wr, 'A Leste perde %d peças da malha dentro do vão de 1,60 m².' % T['rows']['LESTE']['removed'], 8.8, 11.4, 'S', K70)
    footer(c, nf, TOTAL)

def s_l2(c, nf):
    header(c, 'Parede Leste 358 × 260 cm · a confirmar',
           'Esta parede aparece só no arquivo "Leste · 15×15" e não casa com o banheiro (Leste com 264 × 240 cm). A paginação está pronta nas duas opções, '
           'mas fica FORA do total do banheiro até alguém dizer que parede é esta.', nf, TOTAL)
    oy = 322; sc = SC25
    xA = MG + 70
    xB = xA + 358 * sc + 104
    wl2 = dict(C.L2)
    draw_wall(c, xA, oy, sc, wl2, A, nome='OPÇÃO A · 15,5 × 15,5', tag='358 × 260 cm · escala 1:25', name_dy=50)
    draw_wall(c, xB, oy, sc, wl2, B, nome='OPÇÃO B · 7,5 × 15,5', tag='358 × 260 cm · escala 1:25', name_dy=50)
    legend(c, xA - 20, oy - 28, [('full', 'peça inteira'), ('cut', 'peça com corte'), ('axis', 'eixo da parede')], 7.8, 16)
    y = oy - 52
    qa = C.quant(wl2, A); qb = C.quant(wl2, B)
    na, ca, _, _ = C.buy(qa['phys'], A); nb, cb, _, _ = C.buy(qb['phys'], B)
    rows = []
    for nm, o, q, ne, cx in (('A · 15,5 × 15,5', A, qa, na, ca), ('B · 7,5 × 15,5', B, qb, nb, cb)):
        hp, vp = q['hp'], q['vp']
        rows.append([nm, '%d inteiras · corte %s cm (%s)%s' % (hp['n'], fx(hp['c'], 2), pct(hp['c'], o['a']), '' if hp['mode'] != 'meia' else ' · junta %s mm' % fx(hp['j'] * 10, 2)),
                     '%d inteiras · corte %s cm (%s)' % (vp['n'], fx(vp['c'], 2), pct(vp['c'], o['b'])),
                     str(q['full']), str(q['cut']), str(q['phys']), str(ne), str(cx)])
    yb = table(c, MG, y, [110, 210, 190, 64, 74, 70, 80, 50], ['Opção', 'Colunas', 'Fiadas', 'Inteiras', 'Com corte', 'Físicas', '+10%', 'Caixas'], rows,
               size=8.6, pad=4, aligns=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r'], bold_first=True)
    xr = MG + 900; wr = PW - MG - xr
    # notas
    yn = yb - 24
    wn = 520
    yn = section(c, MG, yn, 'O que precisa ser respondido', wn)
    for h, b in [
        ('Que parede é esta?', 'A Leste do banheiro tem 2,64 m. Os 3,58 m podem ser a parede da casa vista de fora, outro ambiente ou um erro de digitação (2,64 + 0,93 = 3,57).'),
        ('Altura de 2,60 m.', 'Combina com o pé-direito sem forro (2,62 m), não com o banheiro (2,40 m). Se é outro ambiente, o forro e a cota do piso mudam as fiadas.'),
        ('Se for o banheiro.', 'As duas paredes Leste do desenho não podem coexistir. Vale a medida de obra.'),
    ]:
        yn = rich(c, MG, yn, wn, h, b, 9.0, 5)
    yn2 = section(c, MG + wn + 40, yb - 24, 'Como a malha foi calculada', 470)
    for h, b in [
        ('Pontas iguais.', 'A: 21 inteiras por fiada, corte de 12,95 cm (84%). B: 45 inteiras, meia peça de 3,65 cm, junta de 2,87 mm entre colunas.'),
        ('Fiadas.', '15 inteiras e cortes de 11,35 cm (73%) no piso e no topo. Se a altura for 2,40 m, valem as fiadas do banheiro (9,25 cm).'),
    ]:
        yn2 = rich(c, MG + wn + 40, yn2, 470, h, b, 9.0, 5)
    footer(c, nf, TOTAL, 'Parede fora do total do banheiro até a confirmação. Peças e caixas desta folha não entram no quantitativo da Prancha 12.')

SHEETS = [
    lambda c: s_plan(c, A, 5), lambda c: s_elev_ns(c, A, 6), lambda c: s_elev_lo(c, A, 7),
    lambda c: s_plan(c, B, 8), lambda c: s_elev_ns(c, B, 9), lambda c: s_elev_lo(c, B, 10),
    lambda c: s_l2(c, 11),
]
