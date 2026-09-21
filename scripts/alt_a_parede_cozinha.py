# -*- coding: utf-8 -*-
"""Caderno Alternativo A — parede cozinha/closet.

Proposta paralela ao caderno REV. M: não substitui a REV. M, é uma variante de
estudo sobre o mesmo levantamento. Mexe em uma única parede interna.

A ALTERAÇÃO
  A parede que hoje separa cozinha e closet (0,10 m, sem carga aparente — não
  há projeto estrutural do edifício disponível para confirmar) desliza 0,45 m
  para o sul, alinhando-se com a parede sul do banheiro e se estendendo até a
  parede externa oeste. Um trecho de parede interna, hoje dentro do closet
  (2,54 m, sem função estrutural aparente), é removido — não sobra em lugar
  nenhum na proposta.

O que isso muda: cozinha ganha 0,92 m² de profundidade (8,90 → 9,82 m²);
closet perde a mesma faixa (5,30 → 4,38 m²). A soma das duas áreas não muda
(14,20 m²) — é a mesma casca, só a parede interna se move.

Geometria conferida por calibração de pixel sobre a Prancha 01 (REV. M) e por
leitura direta das coordenadas do scan em base_mainfloor.py — não por régua a
olho. Ver notas de cada prancha para o que ainda precisa ser confirmado em
campo antes de liberar para obra (estrutura, hidráulica e o acesso do closet).
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base_mainfloor as bm
from base_mainfloor import *      # noqa
from base_mainfloor import _tick

REV = 'ALT. A'
PRANCHA_N = 4

# ---------------------------------------------------------------------------
# GEOMETRIA — o que muda
# ---------------------------------------------------------------------------
WALL_REMOVER_1 = (279.36, 430.06, 345.67, 434.63)   # parede antiga cozinha/closet
WALL_REMOVER_2 = (279.36, 430.06, 283.92, 545.96)   # parede interna do closet
WALL_NOVA = (245.70, 450.67, 343.39, 455.24)        # segue a parede sul do banheiro

ORIG_WALLS = list(bm.WALLS)
ORIG_ROOMS = copy.deepcopy(bm.ROOMS)

ALT_WALLS = [w for w in ORIG_WALLS if w not in (WALL_REMOVER_1, WALL_REMOVER_2)] + [WALL_NOVA]

ALT_ROOMS = copy.deepcopy(ORIG_ROOMS)
ALT_ROOMS['cozinha']['poly'] = [(277.8, 211.2), (345.7, 211.2), (345.7, 450.67),
                                 (248.0, 450.67), (248.0, 284.8), (277.8, 284.8)]
ALT_ROOMS['cozinha']['area'] = 9.82
ALT_ROOMS['closet']['poly'] = [(248.0, 455.24), (345.7, 455.24), (345.7, 552.7), (248.0, 552.7)]
ALT_ROOMS['closet']['area'] = 4.38

# subconjunto local de paredes/janelas para a folha 01 (zoom cozinha/closet/
# banheiro): o MuPDF não recorta por clip-path em SVG, então a única forma
# segura de ampliar sem sangrar sobre o quadro à direita é desenhar só o
# trecho relevante, não a planta inteira em escala grande. Paredes que
# cruzam para fora da região (x > 420 pt) são truncadas na borda.
LOCAL_WALLS_01 = [
    (275.52, 208.91, 420.00, 213.47),   # norte da cozinha, truncada
    (275.52, 208.91, 280.09, 287.11),
    (245.70, 282.54, 280.09, 287.11),
    WALL_REMOVER_1,
    (345.67, 550.38, 420.00, 554.94),   # sul, truncada
    (343.39, 432.34, 347.96, 455.24),
    (343.39, 325.65, 347.96, 432.34),
    (413.33, 325.65, 417.90, 432.34),
    WALL_REMOVER_2,
    (245.70, 550.38, 345.67, 554.94),
    (343.39, 513.42, 347.96, 552.66),
    (413.33, 432.34, 417.90, 455.24),
    (245.70, 282.54, 250.26, 554.94),   # externa oeste
    (343.39, 325.65, 417.90, 330.22),
]
ORIG_JANELAS = list(bm.JANELAS)
LOCAL_JANELAS_01 = [r for r in ORIG_JANELAS if max(r[0], r[2]) <= 420.0]

DESLOCAMENTO_M = 0.451   # deslocamento da parede para o sul
AREA_TRANSFERIDA = 0.92  # m², cozinha ganha / closet perde
LARGURA_COMUM = 2.04     # m, largura interna comum às duas salas

TAB_AREAS = [
    ('Cozinha', '8,90 m²', '9,82 m²', '+0,92 m²'),
    ('Closet', '5,30 m²', '4,38 m²', '−0,92 m²'),
    ('Soma das duas', '14,20 m²', '14,20 m²', 'sem variação'),
    ('MainFloor — total', '60,30 m²', '60,30 m²', 'sem variação'),
]

TAB_DEMO_ALT = [
    ('E03', 'Ensaio: confirmar natureza da parede (estrutural ou não) antes de qualquer corte', '2 paredes'),
    ('D09', 'Demolir parede interna do closet — sem função estrutural aparente', '2,54 m'),
    ('D10', 'Demolir parede cozinha/closet — trecho existente', '1,45 m'),
    ('P07', 'Preparar as duas faces do corte para receber a parede nova', '4,08 m²'),
]
TAB_CONST_ALT = [
    ('R03', 'Construir parede nova, alinhada à parede sul do banheiro', '2,17 m'),
    ('R04', 'Estender a parede nova até a parede externa oeste', 'inclui em R03'),
    ('P08', 'Revestir e pintar as duas faces da parede nova', '4,34 m²'),
    ('T12*', 'Reavaliar posição de T12 (tomada forno/lava-louças) — folga aumenta', '1 ponto'),
]

SEQ_ALT = [
    ('1', ['Ensaio estrutural — E03.',
           'Confirmar com engenheiro que as duas paredes não têm função estrutural',
           'antes de qualquer demolição. Não há projeto estrutural do edifício',
           'disponível nesta emissão — orientação de escopo, não laudo.'], True),
    ('2', ['Verificar interferências ocultas.',
           'A parede antiga corre junto à cozinha: confirmar se há hidráulica ou',
           'gás embutidos no trecho antes de abrir. Nenhum ponto elétrico documentado',
           'nesta faixa além de T12, que fica mais afastado com a mudança.'], True),
    ('3', ['Demolição — D09 e D10.',
           'A parede interna do closet (D09) e o trecho cozinha/closet (D10).'], False),
    ('4', ['PARADA — Marcação da nova parede antes de levantar.',
           'Conferir o alinhamento com a face sul do banheiro e o esquadro contra',
           'a parede externa oeste. Uma vez levantada, o erro custa desmontar.'], True),
    ('5', ['Construção — R03.',
           'Mesma espessura das demais paredes internas, 0,10 m. Confirmar material',
           '(drywall ou alvenaria) pelo que for encontrado nas paredes vizinhas.'], False),
    ('6', ['Revestimento e pintura — P08, nas duas faces.'], False),
    ('7', ['Entrega com nível e esquadro conferidos.',
           'Não iniciar armário novo do closet (M01) sem essa conferência.'], False),
]

RISCOS_ALT = [
    ('R1', 'Estrutura', 'impasse',
     'Natureza da parede não confirmada',
     'em análise — pedir confirmação ao engenheiro antes de demolir',
     ['Nenhum projeto estrutural do edifício foi disponibilizado nesta emissão.',
      'As duas paredes leem como alvenaria de vedação de 0,10 m, sem viga ou pilar',
      'aparente no scan — mas o scan não enxerga o que está dentro da parede.',
      'PORTÃO: ensaio E03 (percussão + inspeção visual do entorno) antes do D09/D10.']),
    ('R2', 'Marcenaria', 'alto',
     'Armário do closet perde profundidade',
     'M01 precisa de módulo novo, não o mesmo remontado',
     ['A profundidade útil do closet cai de 2,58 para 2,13 m. Armários e cabideiros',
      'projetados para a medida antiga não cabem mais. M01 (desmontar, etiquetar e',
      'acondicionar) segue igual, mas a remontagem exige projeto de marcenaria novo,',
      'não a simples devolução dos módulos existentes.']),
    ('R3', 'Hidráulica/gás', 'medio',
     'Interferência oculta na parede antiga',
     'confirmar em campo antes da demolição',
     ['Nenhum ponto hidráulico ou de gás está documentado nesta faixa da cozinha,',
      'mas o levantamento é por scan óptico — não enxerga tubulação embutida.',
      'Abrir com cautela e ter um hidráulico de prontidão no primeiro corte.']),
    ('R4', 'Acesso', 'acompanhar',
     'Entrada do closet não está no escopo desta alteração',
     'confirmar em campo',
     ['O levantamento não registra porta no closet. O acesso hoje parece vir do',
      'quarto, num vão de cerca de 1,27 m na divisa closet/quarto, que esta',
      'alteração não toca. Confirmar em campo que esse vão realmente é a entrada',
      'antes de fechar a parede nova — se não for, o closet fica sem acesso.']),
]

COR_GRAU = {'impasse': DEMO, 'alto': AMARELO, 'medio': BRANCO, 'acompanhar': K12}
NOME_GRAU = {'impasse': 'IMPASSE', 'alto': 'ATENÇÃO', 'medio': 'ACOMPANHAR', 'acompanhar': 'ACOMPANHAR'}


def usar(walls, rooms):
    bm.WALLS = walls
    bm.ROOMS = rooms


def cabeca_alt(d, titulo, chamada, num, dir1='', dir2=''):
    d.txt(MARGIN, 42, 'MAXHAUS 81I  ·  CADERNO ALTERNATIVO A  ·  PAREDE COZINHA/CLOSET',
          10.0, INK_SOFT, 'bold', ls=1.4)
    d.txt(MARGIN, 78, titulo, 25.0, INK, 'bold')
    d.txt(MARGIN, 99, chamada, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, REV, 10.0, RED, 'bold', 'end', ls=0.8)
    if dir1:
        d.txt(W - MARGIN, 78, dir1, 10.5, INK, 'bold', 'end')
    if dir2:
        d.txt(W - MARGIN, 99, dir2, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)


def rodape_alt(d, nota1, nota2, folha):
    d.line(MARGIN, 922, W - MARGIN, 922, RULE, 1.0)
    d.txt(MARGIN, 940, nota1, 8.3, INK_SOFT)
    d.txt(MARGIN, 953, nota2, 8.3, INK_SOFT)
    d.txt(MARGIN, 975, 'PROPOSTA DE ESTUDO — PARALELA À REV. M, NÃO A SUBSTITUI   |   21/09/2026',
          9.0, RED, 'bold', ls=0.5)
    d.txt(W - MARGIN, 975, '%s   ·   %s' % (folha, REV), 9.0, INK_SOFT, 'normal', 'end')


def registro_riscos(d, x, y, largura):
    d.txt(x, y - 10, 'REGISTRO DE RISCO — ESTA ALTERAÇÃO', 8.0, INK_SOFT, 'bold', ls=1.2)
    yy = y
    for (ident, disc, grau, titulo, dono, linhas) in RISCOS_ALT:
        aberto = (grau == 'impasse')
        cor_borda = DEMO if aberto else K20
        alt = 44 + len(linhas) * 11.4
        d.rect(x, yy, largura, alt, fill=MAGENTA18 if aberto else K04, stroke=cor_borda,
               sw=1.4 if aberto else 0.8)
        d.rect(x, yy, 30, 18, fill=DEMO if aberto else K45)
        d.txt(x + 15, yy + 13, ident, 8.0, BRANCO, 'bold', 'middle', ls=0.3)
        d.txt(x + 40, yy + 13, '%s  ·  %s' % (disc, titulo), 8.8, K, 'bold')
        sw_ = 74.0
        d.rect(x + largura - sw_ - 8, yy + 4, sw_, 13, fill=COR_GRAU[grau], stroke=K,
               sw=1.2 if aberto else 0.7)
        d.txt(x + largura - sw_ / 2.0 - 8, yy + 13.3, NOME_GRAU[grau], 6.4,
              BRANCO if aberto else K, 'bold', 'middle', ls=0.4)
        d.txt(x + 12, yy + 28, dono, 7.4, INK_SOFT, 'normal')
        y2 = yy + 40
        for ln in linhas:
            forte = ln.startswith('PORTÃO:')
            d.txt(x + 12, y2, ln, 7.9, DEMO if forte else INK, 'bold' if forte else 'normal')
            y2 += 11.4
        yy += alt + 12
    return yy


# ---------------------------------------------------------------------------
# ALT-01 — planta de escopo (detalhe, estado atual + demolição + parede nova)
# ---------------------------------------------------------------------------
def construir_01():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Escopo da alteração', 'Detalhe cozinha · closet · banheiro, no estado atual, com o que sai e o que entra.',
               1, '1 parede nova · 2 trechos demolidos', 'deslocamento de 0,45 m para o sul')

    # detalhe ampliado (zoom na área cozinha/closet/banheiro): o MuPDF não
    # respeita clip-path em SVG, então o recorte é geométrico — desenha-se só
    # o subconjunto de paredes/janelas/ambientes desta esquina, não a planta
    # inteira em escala grande (o que sangraria sobre o quadro à direita).
    S = 85.0
    ox, oy = 170.0, -7.3
    d.set_plan(ox, oy, S)

    for k in ('cozinha', 'banheiro', 'closet'):
        d.path(path_d([d.P(x, y) for x, y in ROOMS[k]['poly']]), fill=K07)

    bm.WALLS = LOCAL_WALLS_01
    paredes(d, estado='novo')
    bm.WALLS = ORIG_WALLS

    bm.JANELAS = LOCAL_JANELAS_01
    janelas(d)
    bm.JANELAS = ORIG_JANELAS
    porta(d, DOOR_BANHO)

    for k, lx, ly in (('cozinha', 300.0, 350.0), ('banheiro', 380.6, 385.0),
                      ('closet', 297.0, 500.0), ('quarto', 470.0, 500.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    for k in ('cozinha', 'banheiro', 'closet'):
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 9.0, INK, 'bold', 'middle', ls=0.8)
        d.txt(lx, ly + 11, br(r['area']) + ' m²', 7.6, INK_SOFT, 'normal', 'middle')

    # demolição: hachura magenta sobre as duas paredes a remover
    for rect in (WALL_REMOVER_1, WALL_REMOVER_2):
        x, y, w_, h_ = d.R(rect)
        d.rect(x, y, w_, h_, fill=DEMO)
        cx, cy = x + w_ / 2.0, y + h_ / 2.0
        rr = max(w_, h_) / 2.0 + 3
        d.line(cx - rr, cy - rr, cx + rr, cy + rr, DEMO, 2.2)
        d.line(cx - rr, cy + rr, cx + rr, cy - rr, DEMO, 2.2)

    # parede nova: cheia em preto, com textura de "nova"
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x, y, w_, h_, fill=WALL, stroke=K, sw=0.5)
    for i in range(int(w_ / 10)):
        xx = x + 6 + i * 10
        if xx < x + w_ - 4:
            d.line(xx, y + 1.5, xx, y + h_ - 1.5, BG, 1.0, opacity=0.55)

    # callouts — ancorados à direita das paredes para caber dentro do recorte
    p0 = d.P(*WALL_NOVA[:2])
    d.txt(p0[0] + 10, p0[1] - 14, 'PAREDE NOVA — segue a face sul do banheiro', 7.6, K, 'bold', 'start', ls=0.2)
    d.txt(p0[0] + 10, p0[1] - 4, 'até a parede externa oeste', 7.0, INK_SOFT, 'normal', 'start')

    rx, ry = d.R(WALL_REMOVER_2)[:2]
    rx2, ry2 = d.R(WALL_REMOVER_1)[:2]
    d.txt(rx + 8, ry - 22, 'D09  parede interna do closet — REMOVER', 7.2, DEMO, 'bold', 'start', ls=0.2)
    d.txt(rx2 + 8, ry2 - 8, 'D10  parede cozinha/closet — REMOVER', 7.2, DEMO, 'bold', 'start', ls=0.2)

    # cota do deslocamento
    xco = d.P(343.39, 0)[0] + 26
    ya = d.P(0, 430.06)[1]
    yb = d.P(0, 450.67)[1]
    d.line(xco, ya, xco, yb, DEMO, 1.4)
    _tick(d, xco, ya, True)
    _tick(d, xco, yb, True)
    d.txt(xco + 6, (ya + yb) / 2.0 + 3, '0,45', 8.0, DEMO, 'bold', 'start')

    bottom_y = d.P(0, 554.94)[1]      # face sul do edifício — base visível da planta
    escala(d, bottom_y + 30)
    legenda(d, [('fill', DEMO, 'Demolir (D09, D10)'), ('fill', WALL, 'Parede nova (R03)'),
                ('ghost', K45, 'Mantido')],
            int(ox), bottom_y + 62, largura=500)

    # thumbnail de contexto — planta inteira, pequena, no canto
    d2_ox, d2_oy, d2_S = 70, 176, 16.0
    d.set_plan(d2_ox, d2_oy, d2_S)
    d.rect(d2_ox - 4, d2_oy - 4, BUILDING_W * d2_S + 8, BUILDING_H * d2_S + 8, fill=BG, stroke=K20, sw=0.8)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    zx0, zy0 = d.P(245.70, 280.0)
    zx1, zy1 = d.P(420.0, 555.0)
    d.rect(zx0, zy0, zx1 - zx0, zy1 - zy0, fill='none', stroke=DEMO, sw=1.6)
    d.txt(d2_ox, d2_oy - 10, 'ONDE FICA', 7.0, INK_SOFT, 'bold', ls=0.8)

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('ID', 0.11, 'start'), ('O que sai', 0.65, 'start'), ('Quantidade', 0.24, 'end')],
                 TAB_DEMO_ALT, titulo='DEMOLIÇÃO', alt=24)
    fim = tabela(d, cx, fim + 30, cw,
                 [('ID', 0.11, 'start'), ('O que entra', 0.65, 'start'), ('Quantidade', 0.24, 'end')],
                 TAB_CONST_ALT, titulo='CONSTRUÇÃO', alt=24)
    paragrafos(d, cx, fim + 30, cw,
               [['**A leitura desta folha.',
                 'A planta é o estado ATUAL, com a demolição marcada em magenta e a parede nova',
                 'desenhada cheia, em preto, sobreposta na posição final. O deslocamento é',
                 'exato: 0,45 m para o sul, medido face a face das duas paredes.'],
                ['**Por que esta parede e não outra.',
                 'A parede nova reaproveita o alinhamento que já existe — a face sul do',
                 'banheiro — em vez de criar uma cota nova. Isso simplifica a execução: um',
                 'só traço reto, do banheiro até a fachada, sem escora.']],
               size=8.5, lh=12.2, gap=8.0)

    rodape_alt(d,
               'Geometria conferida por calibração de pixel sobre a Prancha 01 (REV. M) e pelas coordenadas do scan de 02.09.2026.',
               'Não é planta executiva. Confirmar em campo antes de qualquer demolição — ver Prancha 03 desta série.',
               'Alt A · 01 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-02 — planta proposta cotada (peça equivalente à Prancha 01)
# ---------------------------------------------------------------------------
def construir_02():
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Planta proposta cotada', 'MainFloor completo, com a parede cozinha/closet na posição nova. Demais ambientes sem alteração.',
               2, 'cozinha 9,82 m²  ·  closet 4,38 m²', 'mesma base do scan — REV. M')

    S = 64.0
    d.set_plan(132, 182, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)

    for k, lx, ly in (('jantar', 525.0, 158.0), ('sala', 505.0, 290.0),
                      ('cozinha', 300.0, 375.0), ('closet', 297.0, 508.0),
                      ('quarto', 505.0, 505.0), ('banheiro', 380.6, 372.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=True, size=8.2)

    # realce leve na parede nova, para achar de imediato
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x - 1.5, y - 1.5, w_ + 3, h_ + 3, fill='none', stroke=DEMO, sw=1.1, dash='3 2.5')

    cadeia_h(d, [245.70, 343.39, 347.96, 604.03], 554.94, 24)
    cota_h(d, 245.70, 604.03, 554.94, 48, '7,85', size=8.0)
    cadeia_v(d, [124.38, 208.91, 282.54, 450.67, 455.24, 554.94], 245.70, -24)
    cota_v(d, 124.38, 554.94, 245.70, -48, '9,43', size=8.0)
    cadeia_h(d, [446.11, 450.68, 599.46, 604.03], 124.38, -24)
    cota_h(d, 446.11, 604.03, 124.38, -48, '3,46', size=8.0)

    cota_h(d, 347.96, 413.33, 330.22, 15, size=6.4, ext=False)      # banheiro
    cota_v(d, 330.22, 450.67, 413.33, -15, size=6.4, ext=False)
    cota_h(d, 250.26, 343.39, 552.66, -16, size=6.6, ext=False)     # closet (nova)
    cota_v(d, 455.24, 552.66, 250.26, -16, size=6.6, ext=False)
    cota_h(d, 347.96, 599.46, 550.38, -16, size=6.6, ext=False)     # quarto
    cota_h(d, 417.90, 599.46, 430.06, -16, size=6.6, ext=False)     # sala
    cota_h(d, 250.26, 343.39, 430.06, -16, size=6.6, ext=False)     # cozinha (nova)
    cota_v(d, 213.47, 450.67, 250.26, 16, size=6.6, ext=False)

    norte(d, 214, 218, 19)

    escala(d, 182 + BUILDING_H * S + 74)
    legenda(d, [('fill', K07, 'Área útil — 60,30 m²'),
                ('ghost', DEMO, 'Parede nova, nesta proposta'),
                ('line', DIM, 'Linha de cota (m)')],
            70, 182 + BUILDING_H * S + 108, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.30, 'start'), ('Área atual', 0.22, 'end'),
                  ('Área nesta proposta', 0.26, 'end'), ('Diferença', 0.22, 'end')],
                 TAB_AREAS, titulo='COMPARATIVO DE ÁREAS', alt=22)
    paragrafos(d, cx, fim + 30, cw,
               [['**Só duas salas mudam de área.',
                 'Sala, quarto, jantar e banheiro seguem exatamente como na REV. M — mesmas',
                 'cotas, mesmas esquadrias, mesma numeração de portas e janelas.'],
                ['**A largura interna comum não muda.',
                 'Cozinha e closet continuam com 2,04 m de largura livre — a mesma parede',
                 'externa oeste e a mesma parede do banheiro/quarto os limitam dos dois lados.',
                 'Só a parede que os separa entre si é que se move.'],
                ['**J06, a janela do closet, não é afetada.',
                 'Fica na parede sul (fachada), que esta alteração não toca. A profundidade',
                 'do closet diminui pelo lado norte — o vão da janela permanece o mesmo.']],
               size=8.5, lh=12.3, gap=8.0)

    rodape_alt(d,
               'Cotas extraídas do modelo do scan e arredondadas ao centímetro, com a parede cozinha/closet na posição desta proposta.',
               'Planta de estudo. Substitui a Prancha 01 apenas nesta proposta alternativa — a REV. M segue como está.',
               'Alt A · 02 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-03 — demolição e construção (sequência de obra)
# ---------------------------------------------------------------------------
def construir_03():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Demolição e construção', 'Sequência de execução desta alteração — orientação de escopo, não laudo.',
               3, '7 passos  ·  2 paradas', 'ver Prancha 04 para os riscos')

    S = 85.0
    ox, oy = 170.0, -7.3
    d.set_plan(ox, oy, S)

    for k in ('cozinha', 'banheiro', 'closet'):
        d.path(path_d([d.P(x, y) for x, y in ROOMS[k]['poly']]), fill=K07)

    bm.WALLS = LOCAL_WALLS_01
    paredes(d, estado='novo')
    bm.WALLS = ORIG_WALLS

    bm.JANELAS = LOCAL_JANELAS_01
    janelas(d)
    bm.JANELAS = ORIG_JANELAS
    porta(d, DOOR_BANHO)

    for k, lx, ly in (('cozinha', 300.0, 350.0), ('banheiro', 380.6, 385.0),
                      ('closet', 297.0, 500.0), ('quarto', 470.0, 500.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    for k in ('cozinha', 'banheiro', 'closet'):
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 9.0, INK, 'bold', 'middle', ls=0.8)

    for rect, ident in ((WALL_REMOVER_1, 'D10'), (WALL_REMOVER_2, 'D09')):
        x, y, w_, h_ = d.R(rect)
        d.rect(x, y, w_, h_, fill=DEMO)
        d.circle(x + w_ / 2.0, y + h_ / 2.0, 9, fill=BRANCO, stroke=DEMO, sw=1.4)
        d.txt(x + w_ / 2.0, y + h_ / 2.0 + 3, ident, 7.4, DEMO, 'bold', 'middle')

    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.6, dash='5 3')
    d.circle(x + w_ / 2.0, y + h_ / 2.0, 9, fill=BRANCO, stroke=K, sw=1.4)
    d.txt(x + w_ / 2.0, y + h_ / 2.0 + 3, 'R03', 7.4, K, 'bold', 'middle')

    bottom_y = d.P(0, 554.94)[1]
    escala(d, bottom_y + 30)
    legenda(d, [('fill', DEMO, 'Demolir'), ('ghost', K, 'Construir')],
            int(ox), bottom_y + 62, largura=400)

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = sequencia_alt(d, cx, 160, cw, 'ORDEM DE EXECUÇÃO', SEQ_ALT)
    paragrafos(d, cx, fim + 26, cw,
               [['**Nada aqui é laudo estrutural.',
                 'Sem acesso ao projeto estrutural do edifício, a leitura desta alteração é',
                 'visual, sobre o scan. O ensaio E03 é o que transforma essa leitura em',
                 'decisão segura — não pular esse passo por parecer óbvio.']],
               size=8.6, lh=12.4, gap=8.0)

    rodape_alt(d,
               'Sequência de estudo, sem cronograma. Prazos e mão de obra a definir com a contratada.',
               'Passos em amarelo (PARADA) não seguem sem aceite por escrito ou confirmação de engenheiro.',
               'Alt A · 03 / %d' % PRANCHA_N)
    return d


def sequencia_alt(d, x, y, largura, titulo, passos, size=8.4, lh=12.2):
    d.txt(x, y, titulo, 8.0, INK_SOFT, 'bold', ls=1.2)
    yy = y + 18
    for (num, texto, gate) in passos:
        d.circle(x + 7, yy - 3, 7.5, fill=AMARELO if gate else BRANCO, stroke=K, sw=1.0)
        d.txt(x + 7, yy, num, 7.4, K, 'bold', 'middle')
        linhas = texto if isinstance(texto, list) else [texto]
        for j, ln in enumerate(linhas):
            forte = ln.startswith('PARADA')
            d.txt(x + 22, yy + j * lh, ln, size, K if (j == 0 or forte) else INK_SOFT,
                  'bold' if (j == 0 and gate) or forte else 'normal')
        yy += lh * len(linhas) + 7.0
    return yy


# ---------------------------------------------------------------------------
# ALT-04 — quadro comparativo e riscos
# ---------------------------------------------------------------------------
def construir_04():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Quadro comparativo e riscos', 'O que muda, o que não muda, e o que precisa de confirmação antes da obra.',
               4, '4 pontos catalogados  ·  1 impasse', 'orientação de escopo, não laudo')

    cx, cw = MARGIN, 660
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.28, 'start'), ('Área atual', 0.20, 'end'),
                  ('Área proposta', 0.22, 'end'), ('Diferença', 0.30, 'end')],
                 TAB_AREAS, titulo='ÁREAS — ANTES E DEPOIS', alt=22)

    tab_dim = [
        ('Largura interna (comum)', '2,04 m', '2,04 m', 'sem variação'),
        ('Profundidade da cozinha', '3,18 m', '3,63 m', '+0,45 m'),
        ('Profundidade do closet', '2,59 m', '2,13 m', '−0,45 m'),
        ('Posição da parede', '—', '0,45 m ao sul', 'alinhada ao banheiro'),
    ]
    fim = tabela(d, cx, fim + 34, cw,
                 [('Grandeza', 0.34, 'start'), ('Atual', 0.20, 'end'),
                  ('Proposta', 0.20, 'end'), ('Leitura', 0.26, 'end')],
                 tab_dim, titulo='DIMENSÕES — FACE A FACE', alt=22)

    fim = registro_riscos(d, cx, fim + 34, cw)

    d.line(716, 140, 716, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 748, W - MARGIN - 748
    paragrafos(d, cx2, 160, cw2,
               [['**O que não muda.',
                 'Sala, quarto, jantar, banheiro: mesmas cotas, mesmas esquadrias, mesma',
                 'numeração de portas e janelas da REV. M. Nenhuma instalação elétrica',
                 'documentada precisa ser remanejada — T12 só ganha mais folga.'],
                ['**O que muda.',
                 'Uma parede interna se desloca 0,45 m para o sul, alinhando-se com a',
                 'parede do banheiro. Cozinha ganha 0,92 m² de profundidade; closet perde',
                 'a mesma faixa. A soma das duas áreas — e a área total do MainFloor —',
                 'não muda: é a mesma casca, com a parede interna numa posição nova.'],
                ['**Por que a área total do MainFloor não muda.',
                 'A parede que se move é 100% interna, entre dois ambientes que já',
                 'pertenciam ao apartamento. Não há ganho nem perda de área contra a',
                 'fachada, a caixa de escada ou qualquer parede externa.'],
                ['**O que esta proposta não resolve.',
                 'Não inclui projeto de marcenaria novo para o closet (a profundidade',
                 'menor pede módulos redesenhados, não os mesmos remontados — ver R2).',
                 'Não confirma a natureza estrutural das paredes (ver R1, o único',
                 'impasse aberto desta proposta) nem o acesso do closet pelo quarto',
                 '(ver R4) — os dois pedem confirmação em campo antes da obra.'],
                ['**Como isto se encaixa no caderno REV. M.',
                 'Esta é uma proposta PARALELA — um estudo de opção, não uma revisão.',
                 'Se aprovada, as folhas equivalentes da REV. M (Prancha 01, Prancha 02,',
                 'Prancha 09 e o pacote de fornecedores) precisam ser atualizadas para',
                 'incorporar esta alteração — o que não foi feito nesta emissão.']],
               size=8.5, lh=12.2, gap=8.0)

    rodape_alt(d,
               'Análise sobre o levantamento digital de 02.09.2026 e sobre a REV. M do caderno principal. Sem vistoria, sem ensaio e sem acesso aos projetos do edifício.',
               'Orientação de escopo, não laudo. A decisão final sobre estrutura pede engenheiro responsável em inspeção.',
               'Alt A · 04 / %d' % PRANCHA_N)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminhos = []
    for fn, nome in ((construir_01, 'alt-a-01-escopo'),
                     (construir_02, 'alt-a-02-planta-proposta'),
                     (construir_03, 'alt-a-03-obra'),
                     (construir_04, 'alt-a-04-riscos')):
        caminho = salvar(fn(), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus MainFloor — Caderno Alternativo A: ' + nome)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
        caminhos.append(caminho)
    exportar_pdf_a3(caminhos, os.path.join(pasta, 'caderno-alternativo-a-A3.pdf'),
                    'MaxHaus MainFloor — Caderno Alternativo A: parede cozinha/closet')
    print('ok caderno alternativo a: 4 folhas + pacote')
