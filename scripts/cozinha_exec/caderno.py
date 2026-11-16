# -*- coding: utf-8 -*-
"""Caderno de paginação do piso da cozinha + closet — folhas CP-01 a CP-06 (emissão C1).

Gera cozinha/piso-C1/Cozinha_Caderno_Piso_C1_A3.pdf e uma folha PDF por código.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coz import *          # noqa
import coz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA = os.path.join(RAIZ, 'cozinha', 'piso-C1')
OX, OY, N = 200.0, 190.0, 30          # planta padrão 1:30
CX = 640.0                            # coluna de texto
CW = W - MARGIN - CX

TIPO = {'inteira': 'inteira', 'reta': 'corte reto', 'curva': 'corte curvo (arco R 700)',
        'recorte': 'recorte em L (degrau)', 'faixa': 'faixa de ajuste, sob a KC1'}
COR = {'inteira': BRANCO, 'reta': K04, 'curva': CIANO18, 'recorte': CIANO18, 'faixa': AMARELO40}
PEC = pecas()
PLANO, ORIGEM, N_PLACAS = placas(PEC)
A_ZONA = area(zona()) / 1e6
A_PECAS = sum(p[3] for p in PEC) / 1e6
K10 = 1.10
N_COMPRA = int(math.ceil(N_PLACAS * K10 / 2.0) * 2)       # caixas de 2 placas
RETO, ARCO, PERIM = comprimentos()


def _cota_txt(f, P, x0, x1, y_mm, off, txt, size=6.6):
    a, b = P(x0, y_mm), P(x1, y_mm)
    f.cota_h(a[0], b[0], a[1] + off, txt, size)


def _cota_txt_v(f, P, y0, y1, x_mm, off, txt, size=6.6, lado=-1):
    a, b = P(x_mm, y0), P(x_mm, y1)
    f.cota_v(a[0] + off, a[1], b[1], txt, size, lado=lado)


def _legenda_padrao(f, y=890, extra=()):
    f.legenda(OX - 120, y, [('line', DEMO, 'Transição com o monolítico (perfil)'),
                            ('dash', DEMO, 'R04 e AT-A: construídos depois, sobre o piso')] + list(extra))


# ---------------------------------------------------------------------------------------
def cp01():
    f = Folha('CP-01', 'Planta de referência: zona contínua cozinha + closet',
              'Opção B do Caderno Alternativo A (prancha 04): porcelanato acetinado. A drywall nova R04 sobe depois, sobre o piso pronto.', '1:30')
    P, s = f.planta(OX, OY, N, marcenaria=True, demolidas=True)
    f.cadeia_v(P, [DEG_Y, KC1[1], R04[1], R04[3], AT_A[3], COMP], 0, -30)
    _cota_txt_v(f, P, 0, COMP, 0, -62, '%d' % COMP)
    f.cadeia_v(P, [0, RAIO, WC_Y0, PASSAGEM[0], PASSAGEM[1], COMP], LARG + 520, 16, lado=1)
    f.cadeia_h(P, [0, DEG_X, FC[0], LARG], -420, -12)
    _cota_txt(f, P, 0, LARG, COMP + 100, 26, '%d (face a face)' % LARG)
    c = P(FC[0] + 330, 330)
    f.t(c[0] - 6, c[1] + 26, 'R 700', 6.6, DEMO, True, 'middle')
    c = P(1000, 4700)
    f.t(c[0], c[1], 'CLOSET', 8.0, K, True, 'middle')
    c = P(1300, 1800)
    f.t(c[0], c[1], 'COZINHA', 8.0, K, True, 'middle')
    c = P(1200, PAREDES_DEMOLIDAS[0][1])
    f.t(c[0], c[1] - 3, 'parede demolida', 6.0, K45, False, 'middle')
    c = P(1000, COMP + 100)
    f.t(c[0], c[1] + 8, 'J06', 6.4, K70, True, 'middle')
    _legenda_padrao(f, 885, [('fill', K12, 'Faixa de parede demolida')])
    y = f.tab(CX, 150, CW, [('Item', 0.26, 'start'), ('Medida (mm)', 0.22, 'start'), ('De onde vem', 0.52, 'start')], [
        ('Zona de porcelanato', '%d × %d' % (LARG, COMP), 'da face oeste (divisa) à face do banheiro; da transição norte à parede sul do closet'),
        ('Área da zona', '%s m²' % br(A_ZONA), 'cozinha + closet + faixa sob a R04 + nicho AT-A, menos o filete e o degrau'),
        ('Ponta arredondada', 'R 700', 'prancha 04: canto reto com filete; aqui tangente à face do banheiro'),
        ('Degrau da geladeira', '%d × %d' % (DEG_X, DEG_Y), 'parede do corredor de entrada; a zona recua 51 mm'),
        ('R04 · drywall nova', 'y %d a %d' % (R04[1], R04[3]), 'Alternativo A: na face sul do banheiro, até a parede oeste'),
        ('AT-A · nicho do aquecedor', '600 × 400', 'REV. R: canto noroeste do closet; nicho construído depois'),
        ('Passagem closet / quarto', '%d' % (PASSAGEM[1] - PASSAGEM[0]), 'transição reta na face da parede'),
        ('KC1 · bancada', '%d × 600' % (KC1[3] - KC1[1]), 'FO7: do nicho da geladeira (920) até a R04'),
        ('Cooktop e coifa CF01', 'eixo a %d' % CF_Y, 'CF01 da prancha de teto (6,20 m na base); ver CP-05'),
        ('Pé-direito', '%d' % LAJE, 'laje aparente, sem forro'),
    ], titulo='MEDIDAS DE REFERÊNCIA')
    f.par(CX, y + 24, CW, [
        ('Uma zona só, da entrada até o fundo do closet.', 'A R04 (parede nova cozinha/closet) e o nicho do aquecedor AT-A são '
         'construídos depois do piso. O porcelanato corre contínuo por baixo dos dois, sem junta nem soleira na linha da parede. '
         'Se um dia a parede mudar de lugar, o piso fica.'),
        ('Sob móveis também.', 'O piso passa sob a geladeira, a bancada KC1 e o closet M01: nenhum recorte de mobiliário foi descontado.'),
        ('Faixa das paredes demolidas.', 'Onde saem a parede antiga cozinha/closet e a parede interna do closet, recompor o contrapiso '
         'na mesma cota e com a mesma cura antes de assentar. Placa de 1 m não perdoa contrapiso torto.'),
        ('A ponta arredondada.', 'Na prancha 04 o filete de 0,70 m nasce no eixo da parede. Aqui ele foi alinhado à face da parede '
         'do banheiro (5 cm para dentro), para a transição seguir reta até a parede, sem dente. O monolítico acompanha.'),
        ('Conferir em obra.', 'A largura de %d mm vem do scan. Ela decide a faixa de ajuste da CP-02: medir de parede a parede em '
         'três pontos (norte, meio e closet) antes de comprar.' % LARG),
    ], size=8.2, lh=11.6, gap=6)
    return f


# ---------------------------------------------------------------------------------------
def _desenha_pecas(f, P, rotulos=True):
    d = f.d
    for pid, r, pol, a, tipo, env in PEC:
        d.path(bm.path_d([P(*p) for p in pol]), fill=COR[tipo], stroke=K, sw=0.8)
        if not rotulos:
            continue
        if tipo == 'faixa':
            c = P(-100, (r[1] + r[3]) / 2)
            f.t(c[0] - 6, c[1] + 2, pid, 6.4, K, True, 'end')
            continue
        c = P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + (220 if tipo == 'curva' else 0))
        f.t(c[0], c[1], pid, 10.0, K, True, 'middle')
        f.t(c[0], c[1] + 11, '%d × %d' % (round(env[0]), round(env[1])), 6.4, K70, False, 'middle')


def cp02():
    f = Folha('CP-02', 'Paginação: Confete 100 × 100, malha alinhada à face leste',
              'Junta de 2 mm, folga de 3 mm no perímetro. Fiadas a partir da entrada; o corte fica no fundo do closet; a faixa de ajuste, sob a bancada.', '1:30')
    P, s = f.planta(OX, OY, N, piso=K04, r04=False, at_a=False)
    d = f.d
    _desenha_pecas(f, P)
    for r_ in (R04, AT_A):
        a, b = P(r_[0], r_[1]), P(r_[2], r_[3])
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill='none', stroke=DEMO, sw=1.0, dash='5 3')
    # linhas mestras
    xm = colunas()[-1][0] - JUNTA / 2
    ym = fiadas()[0][1] + JUNTA / 2
    a, b = P(xm, -420), P(xm, COMP + 100)
    d.path('M%.1f %.1f L%.1f %.1f' % (a[0], a[1], b[0], b[1]), stroke=DEMO, sw=0.9, dash='10 3 2 3')
    a, b = P(-100, ym), P(LARG + 520, ym)
    d.path('M%.1f %.1f L%.1f %.1f' % (a[0], a[1], b[0], b[1]), stroke=DEMO, sw=0.9, dash='10 3 2 3')
    c = P(xm, ym)
    d.circle(c[0], c[1], 4.5, fill=AMARELO, stroke=K, sw=1.0)
    f.t(c[0] + 8, c[1] - 6, 'M · ponto de partida', 6.6, DEMO, True)
    # cotas da malha
    cols = colunas()
    _cota_txt(f, P, 0, cols[1][0] - JUNTA / 2, -420, -12, '30+3', 6.0)
    _cota_txt(f, P, cols[1][0] - JUNTA / 2, xm, -420, -12, '1000 + junta')
    _cota_txt(f, P, xm, LARG, -420, -12, '1000 + 3 de folga')
    _cota_txt(f, P, xm, LARG, ym + 260, 0, '%d até a face' % round(LARG - xm), 6.2)
    ys = [0] + [r[1] + JUNTA / 2 for r in fiadas()[:-1]] + [COMP]
    f.cadeia_v(P, ys, LARG + 520, 16)
    _cota_txt_v(f, P, 0, ym, LARG + 520, 44, '%d até a transição' % round(ym), 6.2, lado=1)
    f.legenda(OX - 120, 885, [('fill', BRANCO, 'Inteira'), ('fill', K04, 'Corte reto'), ('fill', CIANO18, 'Corte curvo / em L'),
                              ('fill', AMARELO40, 'Faixa de ajuste (30 mm)'), ('dash', DEMO, 'R04 e AT-A depois')])
    linhas = []
    for pid, r, pol, a, tipo, env in PEC:
        orig = ORIGEM.get(pid) or [p for p, q, _ in PLANO if q == pid][0]
        linhas.append((pid, '%d × %d' % (round(env[0]), round(env[1])), TIPO[tipo], orig + (' (sobra)' if pid in ORIGEM else '')))
    y = f.tab(CX, 150, CW, [('Peça', 0.10, 'start'), ('Largura × comprimento (mm)', 0.30, 'start'), ('Tipo', 0.38, 'start'), ('Placa', 0.22, 'start')],
              linhas, titulo='PEÇAS — ENVELOPE (mm), DE NORTE PARA SUL', alt=14.5, size=7.4)
    n_int = sum(1 for p in PEC if p[4] == 'inteira')
    f.par(CX, y + 22, CW, [
        ('Por que alinhar a malha à face leste.', 'São %d mm de parede a parede. Centralizar daria dois cortes de 515 mm por fiada, '
         'que não saem dois de uma placa: 18 placas. Alinhando a leste, ficam duas colunas inteiras e uma faixa de 30 mm a oeste, '
         'escondida sob a KC1 e o closet, tirada das sobras da fiada F: %d placas. A junta central cai a 1004 mm da face do banheiro.' % (LARG, N_PLACAS)),
        ('Ponto de partida M.', 'Fixar primeiro o perfil de transição (CP-04). Marcar no contrapiso a linha da junta entre as colunas 2 e 3 '
         '(a 1004 da face leste) e a junta entre as fiadas A e B (a 1004 da transição). Assentar B3 no canto do ponto M e seguir para sul e oeste; '
         'a fiada A (curva e degrau) e as faixas entram por último, já com as medidas de obra.'),
        ('Resultado.', '%d peças: %d inteiras, %d cortadas e %d faixas. Nenhum corte menor que meia placa no piso visível.' %
         (len(PEC), n_int, len(PEC) - n_int - 6, 6)),
    ], size=8.2, lh=11.6, gap=6)
    return f


# ---------------------------------------------------------------------------------------
def cp03():
    f = Folha('CP-03', 'Plano de corte e gabarito da peça curva',
              'Uma placa por peça larga; as seis faixas saem das sobras de F2 e F3. A curva sai por ordenadas, já descontada a folga de 3 mm.', 'indicada')
    d = f.d
    # placas
    lado, gap, x0, y0 = 92.0, 22.0, 70.0, 165.0
    f.t(x0, y0 - 14, 'PLACAS 1000 × 1000 — O QUE SAI DE CADA UMA (1:110)', 7.4, INK_SOFT, True, ls=1.0)
    por_placa = {}
    for p, q, sob in PLANO:
        por_placa.setdefault(p, []).append(q)
    for q, p in ORIGEM.items():
        por_placa.setdefault(p, []).append(q)
    peca = {p[0]: p for p in PEC}
    for k, (pl, ids) in enumerate(sorted(por_placa.items())):
        cx_, cy_ = x0 + (k % 4) * (lado + gap), y0 + (k // 4) * (lado + 34)
        d.rect(cx_, cy_, lado, lado, fill=BRANCO, stroke=K, sw=0.9)
        sc = lado / PECA
        yy = 0.0
        for q in ids:
            pid, r, pol, a, tipo, env = peca[q]
            if tipo == 'faixa':
                h = env[0] * sc
                d.rect(cx_, cy_ + yy, env[1] * sc, h, fill=AMARELO40, stroke=K, sw=0.5)
                yy += h + CORTE * sc
            else:
                pts = [(cx_ + (x - r[0]) * sc, cy_ + (y - r[1]) * sc) for x, y in pol]
                d.path(bm.path_d(pts), fill=COR[tipo], stroke=K, sw=0.7)
                yy += env[1] * sc + CORTE * sc
        larg = [q for q in ids if peca[q][4] != 'faixa']
        f.t(cx_ + lado / 2, cy_ + 40, ' + '.join(larg), 8.4, K, True, 'middle')
        fx = [q for q in ids if peca[q][4] == 'faixa']
        if fx:
            f.t(cx_ + lado / 2, cy_ + lado - 2, 'faixas ' + ', '.join(fx), 5.8, K, True, 'middle')
        f.t(cx_, cy_ + lado + 11, pl, 7.2, INK_SOFT, True)
    yb = y0 + 3 * (lado + 34) + 6
    f.par(70, yb, 470, [
        ('Ordem de corte.', 'Cortar primeiro F2 e F3 (800 mm) e tirar das sobras de 197 mm as seis faixas de 30 mm. '
         'B2 a E3 entram inteiras. A2 e A3 só depois de fixar o perfil e medir a curva e o degrau em obra.'),
        ('Reserva.', '%d placas no projeto; com 10%% de perda, comprar %d (%d caixas de 2), do mesmo lote do banheiro.' %
         (N_PLACAS, N_COMPRA, N_COMPRA // 2)),
    ], size=8.2, lh=11.6)
    # gabarito da peça curva A3, 1:10
    pid, r, ords = ordenadas()
    s10 = MM / 10.0
    gx, gy = CX + 30, 178.0
    f.t(CX, gy - 26, 'GABARITO DA PEÇA %s — ESCALA 1:10, ORDENADAS EM mm A PARTIR DA BORDA NORTE' % pid, 7.4, INK_SOFT, True, ls=1.0)
    pol = peca[pid][2]
    d.rect(gx, gy, PECA * s10, PECA * s10, fill='none', stroke=K45, sw=0.6, dash='3 2')
    d.path(bm.path_d([(gx + (x - r[0]) * s10, gy + (y - r[1]) * s10) for x, y in pol]), fill=CIANO18, stroke=K, sw=1.0)
    for u, v in ords:
        if v <= 0.5 and u > 1:
            continue
        a = (gx + u * s10, gy)
        b = (gx + u * s10, gy + v * s10)
        d.line(a[0], a[1], b[0], b[1], DEMO, 0.7)
        d.circle(b[0], b[1], 1.8, fill=DEMO)
    for u, v in ords:
        if u not in (975.0, 990.0):
            f.t(gx + u * s10, gy - 6, '%d' % round(u), 5.8, K70, False, 'middle')
        if v > 0.5:
            f.t(gx + u * s10 + 3, gy + v * s10 + 10, '%d' % round(v), 6.4, DEMO, True, 'start' if u < 980 else 'end')
    f.t(gx + PECA * s10 / 2, gy + PECA * s10 * 0.62, pid, 16, K, True, 'middle')
    f.t(gx + PECA * s10 / 2, gy + PECA * s10 * 0.62 + 16, 'borda norte = transição  ·  leste à direita', 7.0, K70, False, 'middle')
    yt = gy + PECA * s10 + 30
    f.tab(CX, yt, CW, [('Da borda oeste da placa (mm)', 0.5, 'start'), ('Até a curva, a partir da borda norte (mm)', 0.5, 'end')],
          [('%d' % round(u), '%d' % round(v)) for u, v in ords if u >= 300], titulo='ORDENADAS DO ARCO R 697 (700 MENOS A FOLGA)', alt=13.0, size=7.2)
    return f


# ---------------------------------------------------------------------------------------
def _camadas(f, x, y, titulo, camadas, rotulos, dy_tit=-40):
    """Corte esquemático: retângulos (x, y, larg, alt, cor, tracejado) e chamadas."""
    d = f.d
    f.t(x, y + dy_tit, titulo, 7.4, INK_SOFT, True, ls=1.0)
    for (cx0, cy0, cw, ch, cor, dash) in camadas:
        d.rect(x + cx0, y + cy0, cw, ch, fill=cor, stroke=K, sw=0.7, dash=dash)
    for (px, py, tx, ty, txt) in rotulos:
        lx = tx if tx >= px else tx + larg_txt(txt, 6.6) / bm.ESCALA_FONTE * 0.9 + 4
        d.line(x + px, y + py, x + lx, y + ty, K70, 0.5)
        d.circle(x + px, y + py, 1.6, fill=K)
        f.t(x + tx + (4 if tx >= px else 0), y + ty + 3, txt, 6.6, INK, False, 'start')


def cp04():
    f = Folha('CP-04', 'Transições, drywall R04 sobre o piso e sequência',
              'Cortes esquemáticos, sem escala. O acerto de altura entre porcelanato e monolítico é no contrapiso, não na soleira.', 'sem escala')
    X = 70.0
    _camadas(f, X, 210.0, '1 · TRANSIÇÃO PORCELANATO / MONOLÍTICO (NORTE, ARCO E PASSAGEM DO CLOSET)', [
        (0, 60, 480, 40, K12, None), (0, 30, 250, 30, K20, None), (0, 22, 250, 8, K45, None), (0, 10, 245, 12, BRANCO, None),
        (247, 6, 8, 24, DEMO, None), (257, 40, 223, 20, K20, None), (257, 10, 223, 30, K07, None),
    ], [(100, 16, 20, -14, 'porcelanato Confete 9 mm'), (251, 8, 200, -28, 'perfil de transição, fixado antes'),
        (380, 25, 340, -14, 'monolítico, contra o perfil'), (60, 26, 20, 118, 'argamassa AC-III, dupla colagem'),
        (180, 45, 200, 118, 'contrapiso acertado: os dois rentes'), (440, 80, 420, 132, 'laje')], dy_tit=-48)
    _camadas(f, X, 480.0, '2 · R04 LEVANTADA DEPOIS: GUIA SOBRE O PORCELANATO', [
        (0, 60, 480, 40, K12, None), (0, 30, 480, 30, K20, None), (0, 22, 480, 8, K45, None), (0, 10, 480, 12, BRANCO, None),
        (195, 4, 90, 6, AMARELO40, None), (205, -60, 70, 64, BRANCO, None),
        (185, -60, 12, 70, K07, None), (283, -60, 12, 70, K07, None),
        (170, -4, 15, 14, K20, None), (295, -4, 15, 14, K20, None),
    ], [(191, -40, 20, -78, 'placa de gesso, dos dois lados'), (240, -30, 330, -78, 'guia e montantes 70 mm'),
        (177, 2, 20, -20, 'rodapé dos dois lados'), (240, 7, 330, -20, 'banda acústica sob a guia'),
        (100, 16, 20, 118, 'porcelanato contínuo, sem junta sob a parede'),
        (240, 20, 270, 118, 'bucha em furo de broca diamantada, fora das juntas')], dy_tit=-100)
    _camadas(f, X, 715.0, '3 · PERÍMETRO: FOLGA DE 3 mm COM SELANTE, SOB O RODAPÉ', [
        (0, 60, 480, 40, K12, None), (0, 30, 400, 30, K20, None), (0, 22, 400, 8, K45, None), (0, 10, 396, 12, BRANCO, None),
        (396, 10, 4, 12, AMARELO, None), (400, -80, 60, 140, K45, None), (385, -6, 15, 16, K20, None),
    ], [(392, 2, 300, -40, 'rodapé'), (430, -40, 330, -70, 'parede'), (398, 16, 380, 118, 'folga 3 mm + selante PU'),
        (200, 16, 20, 132, 'sob a KC1 e o closet o rodapé é da marcenaria; a faixa de 30 mm fica escondida')], dy_tit=-100)
    PAR04 = [
        ('Juntas de movimentação.', 'A zona tem %s m² e o lado maior %s m: abaixo dos limites da NBR 13753 para área interna, '
         'não pede junta intermediária. Ficam só a folga do perímetro e as transições.' % (br(A_ZONA), br(COMP / 1000.0))),
        ('Proteção.', 'Do rejunte até a entrega: papelão ondulado e lona sobre todo o piso. A R04, o AT-A, a marcenaria e o '
         'duto da coifa sobem com o piso protegido.'),
    ]
    yp = f.passos(CX, 160, CW, [
        ('Duto da coifa e elétrica do teto.', 'DU2 e CF01 (CP-05) fixados sob a laje antes do piso: escada e furação de laje não '
                                              'combinam com porcelanato novo. Os pontos da R04 descem pela laje, não pelo piso.', True),
        ('Demolição e contrapiso.', 'Sair as duas paredes antigas, recompor o contrapiso nas faixas e acertar a cota com o monolítico (P06).', False),
        ('Medição de obra.', 'Largura em três pontos, comprimento, degrau e o arco. Se a largura mudar, refazer a faixa de ajuste.', True),
        ('Perfil de transição.', 'Reto no norte e na passagem do closet; flexível no arco de 700. Fixado e nivelado antes das placas.', False),
        ('Assentamento.', 'Do ponto M (CP-02) para sul e oeste, dupla colagem, niveladores de placa. Fiada A, curva, degrau e faixas por último.', False),
        ('Rejunte e cura.', 'Rejunte acrílico na cor do Confete; selante no perímetro. 7 dias sem carga pesada.', False),
        ('Monolítico.', 'Aplicado contra o perfil já fixado (corredor, sala de TV, quarto).', False),
        ('R04 e AT-A sobre o piso.', 'Guia com banda acústica, fixada por bucha. O nicho AT-A em material incombustível, com a liberação do instalador credenciado.', True),
        ('Marcenaria.', 'KC1, geladeira e closet M01 só com o piso curado e protegido.', False),
    ])
    f.par(CX, yp + 24, CW, PAR04, size=8.2, lh=11.6)
    return f


# ---------------------------------------------------------------------------------------
def cp05():
    f = Folha('CP-05', 'Fogão e coifa: posição e exaustão',
              'Cooktop na bancada KC1, sob a CF01. Duto próprio até a fachada do closet, afastado da chaminé do aquecedor. Nada é ligado à chaminé.', '1:30')
    P, s = f.planta(OX, OY, N, marcenaria=True, rotulos=True)
    d = f.d
    # coifa em planta
    a, b = P(0, CF_Y - COIFA_L / 2), P(500, CF_Y + COIFA_L / 2)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=CIANO35, stroke=K, sw=1.0, opacity=0.8)
    f.t((a[0] + b[0]) / 2, b[1] - 6, 'CF01', 6.8, K, True, 'middle')
    # duto e chaminé
    d.path(bm.path_d([P(*p) for p in DUTO], close=False), stroke=CIANO, sw=4.0)
    d.path(bm.path_d([P(*p) for p in DUTO], close=False), stroke=K, sw=0.6, dash='6 3')
    a, b = P(X_CHAMINE, AT_A[3]), P(X_CHAMINE, COMP)
    d.path('M%.1f %.1f L%.1f %.1f' % (a[0], a[1], b[0], b[1]), stroke=DEMO, sw=1.3, dash='4 3')
    c = P(X_DUTO, 4600)
    f.t(c[0] + 6, c[1], 'DU2 Ø150', 6.8, K, True, 'start')
    f.t(c[0] + 6, c[1] + 9, 'sob a laje', 6.0, K70, False, 'start')
    c = P(X_CHAMINE, 5000)
    f.t(c[0] - 4, c[1], 'chaminé AT-A', 6.0, DEMO, True, 'end')
    c = P(X_DUTO, R04[1])
    d.circle(c[0], c[1] + 5, 5.5, fill=AMARELO, stroke=K, sw=0.9)
    f.t(c[0] + 9, c[1] + 24, 'travessia da R04: luva', 6.0, K, True)
    f.cadeia_h(P, [X_CHAMINE, X_DUTO], COMP + 100, 26)
    f.t(P(X_DUTO, COMP)[0] + 8, P(X_DUTO, COMP)[1] + 33, 'entre terminais, na bandeira da J06', 6.0, K70, False, 'start')
    f.cadeia_v(P, [KC1[1], COOK[1], COOK[3], R04[1]], 0, -30)
    f.legenda(OX - 120, 885, [('line', CIANO, 'Duto DU2 da coifa'), ('dash', DEMO, 'Chaminé do aquecedor (não tocar)'), ('fill', CIANO35, 'Coifa CF01')])
    # vista da parede oeste (KC1), 1:30
    vx, vy, sv = 560.0, 170.0, s
    zb = vy + LAJE * sv

    def V(u, z):
        return (vx + (R04[1] - u) * sv, zb - z * sv)      # olhando para oeste: norte à direita

    f.t(vx, vy - 14, 'VISTA DA PAREDE OESTE (BANCADA KC1), 1:30', 7.4, INK_SOFT, True, ls=1.0)
    a, b = V(R04[1], LAJE), V(0, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K04, stroke=K, sw=0.8)
    for (u0, z0, u1, z1, cor, txt) in ((DEG_Y, 0, GEL[3], 1800, 'none', 'geladeira'), (KC1[1], 0, KC1[3], TOPO_BANC, K12, ''),
                                       (COOK[1], TOPO_BANC, COOK[3], TOPO_BANC + 30, K45, ''),
                                       (CUBA[1], TOPO_BANC - 200, CUBA[3], TOPO_BANC, 'none', 'cuba')):
        p0, p1 = V(u1, z1), V(u0, z0)
        d.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=cor, stroke=K, sw=0.8, dash='4 2' if cor == 'none' else None)
        if txt:
            f.t((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, txt, 6.4, K70, False, 'middle')
    zc = TOPO_BANC + 700
    p0, p1 = V(CF_Y - COIFA_L / 2, zc + 120), V(CF_Y + COIFA_L / 2, zc)
    d.path(bm.path_d([V(CF_Y - COIFA_L / 2, zc), V(CF_Y + COIFA_L / 2, zc), V(CF_Y + 150, zc + 250), V(CF_Y - 150, zc + 250)]),
           fill=CIANO35, stroke=K, sw=0.9)
    p0, p1 = V(CF_Y + 150, LAJE), V(CF_Y - 150, zc + 250)
    d.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=CIANO18, stroke=K, sw=0.8)
    p0 = V(CF_Y, LAJE - 110)
    d.circle(p0[0], p0[1], 75 * sv, fill='none', stroke=CIANO, sw=1.6)
    f.t(p0[0] + 12, p0[1] + 3, 'DU2 Ø150: sai para leste, depois sul', 6.2, K, True)
    f.cota_v(V(CF_Y - COIFA_L / 2 - 120, 0)[0], V(0, TOPO_BANC)[1], V(0, zc)[1], '650–750', 6.4, lado=1)
    f.cota_v(V(-80, 0)[0], V(0, 0)[1], V(0, TOPO_BANC)[1], '%d' % TOPO_BANC, 6.4, lado=1)
    f.cota_v(V(-80, 0)[0], V(0, TOPO_BANC)[1], V(0, LAJE)[1], '%d' % (LAJE - TOPO_BANC), 6.4, lado=1)
    f.cota_h(V(CF_Y + COIFA_L / 2, 0)[0], V(CF_Y - COIFA_L / 2, 0)[0], V(0, zc)[1] - 4, '%d' % COIFA_L, 6.4)
    f.cota_h(V(R04[1], 0)[0], V(COOK[3], 0)[0], V(0, 0)[1] + 14, '%d' % (R04[1] - COOK[3]), 6.4)
    f.t(V(R04[1], 0)[0] - 4, V(0, 1300)[1], 'R04 (sul)', 6.6, DEMO, True, 'end')
    f.t(V(0, 0)[0] + 4, V(0, 1300)[1], 'norte', 6.6, K70, True)
    f.t(V(CF_Y, 0)[0], V(0, TOPO_BANC)[1] + 12, 'cooktop 60', 6.2, K70, False, 'middle')
    # critérios
    q_cap = COIFA_L / 1000 * 0.50 * 0.30 * 3600
    q_vol = 9.82 * 2.62 * 12
    v150 = 400 / 3600 / (math.pi * 0.075 ** 2)
    v125 = 400 / 3600 / (math.pi * 0.0625 ** 2)
    l_duto = (X_DUTO - 300 + COMP - CF_Y) / 1000 + 0.6
    yt = f.tab(560, 520, W - MARGIN - 560, [('Critério', 0.30, 'start'), ('Valor', 0.22, 'start'), ('Base', 0.48, 'start')], [
        ('Vazão por captura', '~%d m³/h' % round(q_cap, -1), 'coifa de %d × 500 mm, 0,30 m/s na face de captura' % COIFA_L),
        ('Vazão por trocas', '%s m³/h' % br(q_vol, 1), 'cozinha 9,82 m² × 2,62 m × 12 trocas/h (FO5, Prancha 11)'),
        ('Selecionar', 'mín. 400 m³/h efetivos', 'na curva do fabricante, já com a perda do duto abaixo'),
        ('Duto DU2', 'Ø150 rígido, metálico', '400 m³/h a %s m/s; em Ø125 seriam %s m/s (ruído)' % (br(v150, 1), br(v125, 1))),
        ('Rota', '~%s m, 3 curvas' % br(l_duto, 1), 'sobe, vai para leste até o meio do closet, segue para sul até a J06'),
        ('Terminal', 'bandeira da J06', 'grelha com tela e válvula antirretorno; a %d mm da chaminé do AT-A' % (X_DUTO - X_CHAMINE)),
        ('Altura da coifa', '650 a 750 sobre o cooktop', 'vale o manual do modelo escolhido (indução)'),
        ('Elétrica', 'ponto a ~2,20 m', 'atrás da chaminé da coifa, circuito dedicado (IN3)'),
    ], titulo='EXAUSTÃO — CRITÉRIOS DE PROJETO (A VALIDAR COM O FORNECEDOR)', alt=14.5, size=7.4)
    f.par(1000, 160, W - MARGIN - 1000, [
        ('A rota não pode seguir a parede oeste.', 'A chaminé do aquecedor (AT-A) já corre sob a laje em x = 300, até a J06. '
         'Por isso o DU2 sobe na coifa, desvia %d mm para leste e só então segue para o sul.' % (X_DUTO - 300)),
        ('Coifa e aquecedor: risco real.', 'Coifa com duto tira ar do apartamento. Se o aquecedor não for de câmara estanque, '
         'a depressão pode puxar gás de combustão para dentro do closet. Confirmar o tipo com o instalador credenciado e prever '
         'entrada de ar de compensação se ele pedir. Nunca ligar coifa à chaminé.'),
        ('Condomínio.', 'O terminal na fachada precisa de autorização. Se for negado, a saída é coifa depuradora (filtro de carvão, sem duto), '
         'que não tira calor nem umidade.'),
        ('Antes de fechar.', 'Perguntar à construtora se a unidade tem prumada ou ponto de exaustão de coifa previsto: se existir, é a rota preferida.'),
    ], size=8.0, lh=11.2, gap=5)
    return f


# ---------------------------------------------------------------------------------------
def cp06():
    f = Folha('CP-06', 'Lista de compra e pendências',
              'Tudo com 10% de perda. Quantidades sobre as medidas desta emissão: refazer depois da medição de obra.')
    x1, w1 = MARGIN + 22, 640.0
    arg = A_ZONA * 8.0 * K10
    rej = A_ZONA * (PECA + PECA) / (PECA * PECA) * 9.0 * JUNTA * 1.7
    y = f.tab(x1, 150, w1, [('Material', 0.40, 'start'), ('Líquido', 0.15, 'end'), ('+10%', 0.15, 'end'), ('Compra', 0.30, 'end')], [
        ('Porcelanato Confete 100 × 100 (5041209)', '%s m²' % br(A_ZONA), '%s m²' % br(A_ZONA * K10),
         '%d placas · %d caixas' % (N_COMPRA, N_COMPRA // 2)),
        ('Argamassa AC-III, dupla colagem (~8 kg/m²)', '%d kg' % round(A_ZONA * 8), '%d kg' % round(arg), '%d sacos de 20 kg' % math.ceil(arg / 20)),
        ('Rejunte acrílico, cor do Confete (junta 2 mm)', '%s kg' % br(rej), '%s kg' % br(rej * K10), '1 kg'),
        ('Perfil de transição reto', '%s m' % br(RETO), '%s m' % br(RETO * K10), '1 barra de 3 m'),
        ('Perfil de transição flexível (arco R 700)', '%s m' % br(ARCO), '%s m' % br(ARCO * K10), '1 peça de 1,5 m'),
        ('Selante PU no perímetro (folga 3 mm)', '%s m' % br(PERIM), '%s m' % br(PERIM * K10), '2 tubos'),
        ('Nivelador de placas (clipes + cunhas)', '~%d clipes' % (len(PEC) * 4), '—', '1 kit de 100'),
        ('Proteção: papelão ondulado + lona', '%s m²' % br(A_ZONA), '%s m²' % br(A_ZONA * K10), '14 m²'),
    ], titulo='PISO — PORCELANATO E ASSENTAMENTO')
    y = f.tab(x1, y + 34, w1, [('Item', 0.55, 'start'), ('Quantidade', 0.45, 'end')], [
        ('Coifa de parede, 75 cm, mín. 400 m³/h efetivos (indução)', '1 unidade'),
        ('Duto rígido metálico Ø150', '~%s m: 2 barras de 3 m' % br((X_DUTO - 300 + COMP - CF_Y) / 1000 + 0.6, 1)),
        ('Curva 90° Ø150', '3 unidades'),
        ('Válvula antirretorno Ø150', '1 unidade'),
        ('Terminal de fachada Ø150 com tela', '1 unidade (bandeira da J06)'),
        ('Suportes de laje, abraçadeiras e fita aluminizada', '1 conjunto'),
        ('Luva incombustível na travessia da R04', '1 unidade'),
    ], titulo='EXAUSTÃO DA COIFA — DU2 E CF01')
    f.tab(x1 + w1 + 30, 150, W - MARGIN - (x1 + w1 + 30), [('#', 0.07, 'start'), ('Pendência', 0.63, 'start'), ('Quem', 0.30, 'start')], [
        ('1', 'Confirmar o Confete 100 × 100 também na cozinha e no closet', 'cliente'),
        ('2', 'Comprar junto com o banheiro: %d + 6 = %d placas, mesmo lote' % (N_COMPRA, N_COMPRA + 6), 'cliente / loja'),
        ('3', 'Medir a largura em três pontos: decide a faixa de 30 mm', 'obra'),
        ('4', 'Modelo e posição do cooktop e da cuba na KC1', 'marcenaria'),
        ('5', 'Tipo do aquecedor: câmara estanque ou não', 'instalador gás'),
        ('6', 'Terminal da coifa na fachada (J06)', 'condomínio'),
        ('7', 'Prumada ou ponto de coifa previsto no prédio?', 'construtora'),
        ('8', 'Vigas sob a laje na rota do DU2', 'obra'),
        ('9', 'Acabamento dos perfis igual ao do banheiro', 'cliente'),
    ], titulo='PENDÊNCIAS', alt=16.0, size=7.4)
    f.par(x1, y + 26, w1, [
        ('Por que %d placas.' % N_COMPRA, '%d placas saem no plano de corte da CP-03 (área de %s m²). Com 10%% são %s; '
         'arredondando para caixas de 2, ficam %d placas: sobra uma de reserva para reposição.' %
         (N_PLACAS, br(A_ZONA), br(N_PLACAS * K10, 1), N_COMPRA)),
        ('O nicho AT-A e a faixa da R04 estão incluídos.', 'Os dois são construídos depois, sobre o piso: o porcelanato é contínuo. '
         'Sem eles, a área cairia 0,24 + 0,20 m², sem mudar o número de placas.'),
    ], size=8.2, lh=11.6)
    return f


FOLHAS = [cp01, cp02, cp03, cp04, cp05, cp06]


if __name__ == '__main__':
    so = set(a for a in sys.argv[1:] if not a.startswith('--'))
    svgs = []
    for fn in FOLHAS:
        fo = fn()
        if so and not any(s_ in fo.cod for s_ in so):
            continue
        cam = fo.salvar(PASTA)
        exportar_pdf_a3([cam], os.path.join(PASTA, fo.cod + '-A3.pdf'), 'MaxHaus 81 — Cozinha — ' + fo.cod)
        if '--png' in sys.argv:
            exportar_png(cam, os.path.join(PASTA, fo.cod + '.png'), dpi=110)
        svgs.append(cam)
    if not so:
        exportar_pdf_a3(svgs, os.path.join(PASTA, 'Cozinha_Caderno_Piso_C1_A3.pdf'),
                        'MaxHaus 81 — Cozinha e closet — Caderno de paginação do piso C1 (A3)')
    print(len(svgs), 'folhas')
