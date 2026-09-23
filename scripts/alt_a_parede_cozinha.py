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
import prancha_02_demolicao as p02
import prancha_03_pisos as p03
import prancha_04_teto as p04t
import prancha_05_eletrica as p05e
import prancha_06_esquadrias as p06e
import prancha_11_ar_luz as p11

REV = 'ALT. A'
PRANCHA_N = 11

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
# ALT-02 — demolição (planta geral, estado existente + escopo desta alteração)
# ---------------------------------------------------------------------------
ALVOS_ALT_EXTRA = [
    ('D09', 281.64, 488.0, 'demo', -10, 3),
    ('D10', 312.50, 432.35, 'demo', 10, -8),
    ('R03', 294.50, 452.96, 'novo', 10, 16),
]
LINHAS_ALT_EXTRA = [
    ('D09', 'Parede interna do closet — sem função estrutural aparente (Alt A)', '2,54 m'),
    ('D10', 'Parede cozinha/closet — trecho existente (Alt A)', '1,45 m'),
    ('R03', 'Parede nova, alinhada à face sul do banheiro (Alt A)', '2,17 m'),
]


def construir_02_demolicao():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Demolição e desmontagem', 'Diagrama de escopo sobre o modelo de trabalho — REV. M mais os alvos desta proposta (D09, D10, R03).',
               2, 'estado existente: o que sai, o que se prepara', 'inclui o escopo do Caderno Alternativo A')

    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='existente')
    janelas(d)
    vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    for r in (DRYWALL_SALA_QUARTO, BOX_WC, BANCADA_WC, CANTO_ALEMAO, VIDRO_BOX):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=DEMO, opacity=0.22)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
    for r in (PAREDE_ESCADA_JANTAR, PAREDE_SOB_ESCADA):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=PREP, opacity=0.55)
        d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.0, dash='4 3')
    x, y, w_, h_ = d.R(PORTA_NOVA)
    d.rect(x, y - 1.5, w_, h_ + 3, fill='none', stroke=KEEP, sw=1.4, dash='4 3')
    # alvo desta proposta: as duas paredes cozinha/closet, contorno cheio
    for r in (WALL_REMOVER_1, WALL_REMOVER_2):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=DEMO, opacity=0.32)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.4)
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.4, dash='4 3')

    for k in ROOM_ORDER:
        pp = [d.P(px, py) for px, py in ROOMS[k]['poly']]
        x0, y0, x1, y1 = bbox(pp)
        yy = y0
        while yy <= y1:
            for (a, b) in spans_at_y(pp, yy):
                d.line(a, yy, b, yy, DEMO, 0.45, opacity=0.10)
            yy += 7.0
    rotulos(d, areas=False, size=8.4)

    for (ident, xp, yp, tipo, dx, dy) in p02.ALVOS + ALVOS_ALT_EXTRA:
        cx, cy = d.P(xp, yp)
        cor, miolo = p02.COR_TRACO[tipo], p02.COR_MIOLO[tipo]
        if tipo == 'ensaio':
            d.rect(cx - 5.6, cy - 5.6, 11.2, 11.2, fill=BG, stroke=cor, sw=1.5)
            d.line(cx - 2.6, cy, cx + 2.6, cy, cor, 1.1)
            d.line(cx, cy - 2.6, cx, cy + 2.6, cor, 1.1)
        else:
            d.circle(cx, cy, 6.4, fill=BG, stroke=cor, sw=1.5)
            d.circle(cx, cy, 3.0, fill=miolo, stroke=cor, sw=0.7)
        anchor = 'start' if dx > 0 else 'end'
        d.txt(cx + dx, cy + dy, ident, 8.0, cor, 'bold', anchor, ls=0.4)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dot', DEMO, 'Demolir / retirar'),
                ('fill', AMARELO, 'Preparo de superfície — pronto para pintura'),
                ('dot', K, 'Reconstruir / manter'),
                ('fill', CIANO, 'Desmontar e remontar'),
                ('line', GLASS, 'Pano de vidro existente'),
                ('fill', BRANCO, 'Ensaio de verificação — antes de decidir')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('ID', 0.11, 'start'), ('Serviço', 0.56, 'start'),
                  ('Quantidade preliminar', 0.33, 'end')],
                 p02.LINHAS + LINHAS_ALT_EXTRA,
                 titulo='ESCOPO DE DEMOLIÇÃO, PREPARO E VERIFICAÇÃO', alt=17)
    paragrafos(d, cx, fim + 18, cw,
               [['**Esta folha soma dois escopos.',
                 'A base é o escopo de demolição já previsto na REV. M (D01 a D08, P01 a P06,',
                 'R01, R02, M01, K01, E01, E02). D09, D10 e R03 são exclusivos desta proposta',
                 'alternativa — a parede cozinha/closet, contorno cheio em magenta, e a parede',
                 'nova, tracejada, alinhada à face sul do banheiro.']] + p02.NOTAS,
               size=8.0, lh=11.2, gap=5.0)

    rodape_alt(d,
               'Quantidades preliminares sobre o modelo do scan (02.09.2026): servem para orientar visita e proposta, não para fechar medição.',
               'Nenhum alvo foi verificado em campo. D09/D10/R03 pedem o mesmo ensaio estrutural (E03) descrito na Alt A · 04.',
               'Alt A · 02 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-03 — planta de escopo (detalhe, estado atual + demolição + parede nova)
# ---------------------------------------------------------------------------
def construir_03_escopo():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Escopo da alteração', 'Detalhe cozinha · closet · banheiro, no estado atual, com o que sai e o que entra.',
               3, '1 parede nova · 2 trechos demolidos', 'deslocamento de 0,45 m para o sul')

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
               'Não é planta executiva. Confirmar em campo antes de qualquer demolição — ver Alt A · 04 desta série.',
               'Alt A · 03 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-01 — planta proposta cotada (peça equivalente à Prancha 01)
# ---------------------------------------------------------------------------
def construir_01_planta():
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Planta proposta cotada', 'MainFloor completo, com a parede cozinha/closet na posição nova. Demais ambientes sem alteração.',
               1, 'cozinha 9,82 m²  ·  closet 4,38 m²', 'mesma base do scan — REV. M')

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
               'Alt A · 01 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-04 — demolição e construção (sequência de obra desta alteração)
# ---------------------------------------------------------------------------
def construir_04_sequencia():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Demolição e construção desta alteração', 'Sequência de execução — orientação de escopo, não laudo.',
               4, '7 passos  ·  2 paradas', 'ver Alt A · 11 para os riscos')

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
               'Alt A · 04 / %d' % PRANCHA_N)
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
# ALT-05 / ALT-06 — piso (opção A cumaru + monolítico, opção B monolítico total)
# ---------------------------------------------------------------------------
TAB_PISO_A_ALT = [
    ('Cumaru-ferro',      'sala 23,00 + quarto 13,40 + jantar 5,90 + corredor 2,39', '44,69 m²'),
    ('+ reserva de 10%',  'cortes, perdas e reposição futura',                       '49,16 m²'),
    ('Monolítico',        'cozinha 7,43 (de 9,82) + closet 4,38 — zona contínua',    '11,81 m²'),
    ('Banheiro',          'sistema à parte, área molhada, na mesma cota',             '3,80 m²'),
    ('MainFloor',         'total do pavimento',                                      '60,30 m²'),
]


def construir_piso(opcao='A'):
    A = (opcao == 'A')
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    if A:
        cabeca_alt(d, 'Piso — opção A, cumaru-ferro + monolítico', 'Piso pronto em réguas nas áreas de estar e dormir; cozinha e closet numa zona monolítica contínua — sem mudança nesta zona.',
                   5, 'norte 126°  ·  Alt A · 05', 'ponta arredondada: canto reto com filete de 0,70 m')
    else:
        cabeca_alt(d, 'Piso — opção B, monolítico em todo o MainFloor', 'Sistema único nos cinco ambientes secos, com o banheiro à parte — contorno externo sem mudança nesta proposta.',
                   6, 'norte 126°  ·  Alt A · 06', 'piso contínuo — sem junta de material entre ambientes secos')

    S = 70.0
    d.set_plan(70, 156, S)

    if A:
        for k in ('sala', 'quarto', 'jantar'):
            piso_reguas(d, ROOMS[k]['poly'])
        piso_reguas(d, HALL_A_POLY)
        pm = [d.P(a, b) for a, b in MONO_A_POLY]
        d.path(path_d(pm), fill=MONO)
        d.path(path_d(pm), fill='none', stroke=K, sw=0.9)
    else:
        d.path(path_d([d.P(a, b) for a, b in p03.CONTORNO_SECO]), fill=MONO)

    pp = [d.P(px, py) for px, py in ROOMS['banheiro']['poly']]
    d.path(path_d(pp), fill=WET)
    p03.hachura_wc(d, (345.7, 327.9, 415.6, 453.0))
    d.path(path_d(pp), fill='none', stroke=K, sw=1.0)

    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    p03.soleira(d, p03.SOLEIRA_WC)
    p03.soleira(d, p03.SOLEIRA_ENTRADA)
    if A:
        tracejado(d, [(280.09, 284.8), (313.74, 284.8)] + filete_pts()
                     + [(345.7, 325.65)])
        tracejado(d, [(345.7, 453.0), (345.7, 513.42)])
        qx, qy = d.P(*PONTA_MONO)
        d.circle(qx, qy, 3.0, fill=K)
        d.line(qx, qy, qx + 46, qy - 36, K, 0.8)
        d.txt(qx + 50, qy - 40, 'PONTA ARREDONDADA', 7.4, K, 'bold', 'start', ls=0.4)
        d.txt(qx + 50, qy - 31, 'canto reto com filete de', 7.0, INK_SOFT, 'normal', 'start')
        d.txt(qx + 50, qy - 22, '0,70 m de raio', 7.0, INK_SOFT, 'normal', 'start')

    # realce leve na parede nova
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x - 1.5, y - 1.5, w_ + 3, h_ + 3, fill='none', stroke=DEMO, sw=1.1, dash='3 2.5')

    for k, lx, ly in (('jantar', 520.0, 152.0), ('sala', 500.0, 300.0),
                      ('cozinha', 300.0, 370.0), ('closet', 300.0, 505.0),
                      ('quarto', 520.0, 500.0), ('banheiro', 380.6, 400.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    bx, by = d.P(ROOMS['banheiro']['lx'], ROOMS['banheiro']['ly'])
    d.rect(bx - 33, by - 9, 66, 24, fill=WET, opacity=0.95)
    rotulos(d, areas=True, size=8.4)

    escala(d, 156 + BUILDING_H * S + 26)
    if A:
        itens = [('line', K, 'Cumaru-ferro — piso pronto em réguas'),
                 ('fill', MONO, 'Piso monolítico — cozinha e closet'),
                 ('fill', WET, 'Banheiro — sistema à parte'),
                 ('ghost', DEMO, 'Parede nova, nesta proposta'),
                 ('dash', JOINT, 'Junta / soleira de transição')]
    else:
        itens = [('fill', MONO, 'Piso monolítico contínuo'),
                 ('fill', WET, 'Banheiro — sistema à parte (área molhada)'),
                 ('ghost', DEMO, 'Parede nova, nesta proposta'),
                 ('dash', JOINT, 'Soleira / junta de transição')]
    legenda(d, itens, 70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Sistema', 0.22, 'start'), ('Onde', 0.56, 'start'), ('Área', 0.22, 'end')],
                 TAB_PISO_A_ALT if A else p03.TAB_B, titulo='QUADRO DE ÁREAS')
    nota_alt = (['**Nesta proposta, só a divisão interna cozinha/closet se move.',
                 'A zona monolítica inteira (cozinha + closet) já era desenhada como um único',
                 'pano contínuo, de parede a parede — 11,81 m², sem mudança. O que muda é',
                 'apenas quanto desse pano cada ambiente soma: cozinha passa de 6,51 para',
                 '7,43 m² dentro da zona; closet cai de 5,30 para 4,38 m². Nenhum corte de',
                 'piso novo é criado por esta alteração.'] if A else
                ['**O contorno do monolítico contínuo não muda nesta proposta.',
                 'A parede que se move é 100% interna a essa zona — o contorno externo dos',
                 'cinco ambientes secos (56,50 m²) é o mesmo da REV. M.'])
    paragrafos(d, cx, fim + 30, cw, [nota_alt] + (p03.NOTAS_A if A else p03.NOTAS_B),
               size=8.0, lh=11.4, gap=5.5)

    rodape_alt(d,
               'Revestimento contínuo: toda a área de piso é revestida, inclusive sob móveis e equipamentos — nenhum recorte de mobiliário foi descontado. Áreas conforme o scan de 02.09.2026.',
               'Estudo preliminar de superfície: não substitui especificação de sistema, projeto de juntas nem memorial de aplicação do fornecedor.',
               'Alt A · %s / %d' % ('05' if A else '06', PRANCHA_N))
    return d


# ---------------------------------------------------------------------------
# ALT-07 — teto: laje aparente, iluminação e ar-condicionado
# ---------------------------------------------------------------------------
def construir_07_teto():
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Teto: laje aparente, iluminação e ar-condicionado', 'Distribuição conceitual sobre a laje de concreto — sem mudança de posição nesta proposta; só a parede cozinha/closet se move.',
               7, 'sem forro — tudo aplicado na laje', 'piscina do pavimento superior sobre a sala')

    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    pp = [d.P(px, py) for px, py in ROOMS['banheiro']['poly']]
    d.path(path_d(pp), fill=WET, opacity=0.6)
    d.path(path_d(pp), fill='none', stroke=WET_LINE, sw=0.9, dash='3 2.5')

    x, y, w_, h_ = d.R(AREA_PISCINA)
    d.rect(x, y, w_, h_, fill=AMARELO, opacity=0.30)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.2, dash='6 4')
    t = -h_
    while t <= w_:
        x0 = x + max(0.0, t); y0 = y + h_ - (x0 - (x + t))
        x1 = min(x + w_, x + t + h_); y1 = y + h_ - (x1 - (x + t))
        if x1 > x0:
            d.line(x0, y0, x1, y1, K, 0.5, opacity=0.22)
        t += 13
    cxp, cyp = d.PM(PISCINA_CX, PISCINA_CY)
    d.line(cxp - 11, cyp, cxp + 11, cyp, K, 1.0)
    d.line(cxp, cyp - 11, cxp, cyp + 11, K, 1.0)
    d.circle(cxp, cyp, 3.4, fill='none', stroke=K, sw=1.0)
    d.txt(x + w_ / 2, y + h_ / 2 - 40, 'ÁREA DA PISCINA', 7.6, K, 'bold', 'middle', ls=0.5)
    d.txt(x + w_ / 2, y + h_ / 2 - 29, 'pavimento superior', 7.2, K70, 'normal', 'middle')
    d.txt(x + w_ / 2, y + h_ / 2 + 34, '1,92 × 3,00 m  ·  5,76 m²', 7.2, K70, 'normal', 'middle')
    d.txt(x + w_ / 2, y + h_ / 2 + 45, 'centro em 6,13 / 3,14 m', 7.0, K70, 'normal', 'middle')

    # realce leve na parede nova
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x - 1.5, y - 1.5, w_ + 3, h_ + 3, fill='none', stroke=DEMO, sw=1.1, dash='3 2.5')

    for k, lx, ly in (('jantar', 520.0, 142.0), ('sala', 470.0, 300.0),
                      ('cozinha', 300.0, 340.0), ('closet', 277.6, 508.0),
                      ('quarto', 520.0, 442.0), ('banheiro', 380.6, 430.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=False, size=8.4)

    for (ident, p0, p1, n) in p04t.TRILHOS:
        a = d.PM(*p0); b = d.PM(*p1)
        d.line(a[0], a[1], b[0], b[1], BG, 5.0)
        d.line(a[0], a[1], b[0], b[1], INK, 2.6, cap='round')
        for i in range(n):
            t_ = (i + 0.5) / float(n)
            cx = a[0] + (b[0] - a[0]) * t_
            cy = a[1] + (b[1] - a[1]) * t_
            d.circle(cx, cy, 4.0, fill=BG, stroke=INK, sw=1.2)
            d.circle(cx, cy, 1.5, fill=INK)
        vertical = abs(b[0] - a[0]) < 1
        if ident in p04t.ROTULO_ACIMA:
            d.txt(a[0], a[1] - 12, ident, 7.2, INK, 'bold', 'start', ls=0.4)
        elif vertical:
            d.txt(a[0] + 9, a[1] - 6, ident, 7.2, INK, 'bold', 'start', ls=0.4)
        else:
            d.txt(a[0] - 9, a[1] + 3, ident, 7.2, INK, 'bold', 'end', ls=0.4)

    for (ident, xm, ym, nome) in p04t.DESTAQUES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 10.5, fill=AMARELO, stroke=K, sw=1.8)
        d.circle(cx, cy, 3.4, fill=NEW)
        d.txt(cx, cy + 22, ident + ' · ' + nome, 7.4, NEW, 'bold', 'middle', ls=0.3)

    for (xm, ym) in p04t.EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.0, fill=BG, stroke=WET_LINE, sw=1.3)

    for (ident, xm, ym, nome) in p04t.EXISTENTES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.6, fill='none', stroke=EXIST, sw=1.3)
        d.line(cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2, EXIST, 1.0)

    for (ident, xm, ym, nome) in p04t.MAQUINAS:
        cx, cy = d.PM(xm, ym)
        if ident.startswith('AC'):
            d.rect(cx - 18, cy - 6, 36, 12, fill=CIANO35, stroke=K, sw=1.2)
            d.txt(cx, cy + 3.4, ident, 7.0, K, 'bold', 'middle', ls=0.3)
        else:
            d.circle(cx, cy, 6.0, fill=CIANO35, stroke=K, sw=1.2)
            d.line(cx - 3, cy, cx + 3, cy, K, 1.0)
            d.line(cx, cy - 3, cx, cy + 3, K, 1.0)
            d.txt(cx + 10, cy + 3, ident, 7.0, K, 'bold', 'start', ls=0.3)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('line', INK, 'Trilho eletrificado + spots de sobrepor'),
                ('fill', AMARELO, 'Luminária de destaque (corpo maior)'),
                ('dot', EXIST, 'Ponto existente — confirmar'),
                ('dot', WET_LINE, 'Embutido no forro do banheiro'),
                ('fill', CIANO35, 'Ar-condicionado / exaustão'),
                ('ghost', DEMO, 'Parede nova, nesta proposta')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.34, 'start'), ('Alvo geral', 0.22, 'end'),
                  ('Fluxo inicial', 0.22, 'end'), ('Temperatura de cor', 0.22, 'end')],
                 p04t.TAB_LUZ, titulo='ILUMINAÇÃO POR AMBIENTE')
    fim = tabela(d, cx, fim + 34, cw,
                 [('Zona', 0.34, 'start'), ('Área', 0.22, 'end'),
                  ('Base sombra', 0.22, 'end'), ('Base sol', 0.22, 'end')],
                 p04t.TAB_AR, titulo='AR-CONDICIONADO — REGRA SIMPLIFICADA 600/800 BTU/h POR m²')
    paragrafos(d, cx, fim + 24,
               cw, [['**Nada aqui se move.',
                     'Trilhos, luminárias de destaque, pontos existentes e máquinas ficam nas',
                     'mesmas posições da REV. M — nenhum está no trecho de laje que a cozinha',
                     'ganha (faixa sul, ver Alt A · 03). Ganho: essa faixa fica sem trilho',
                     'próprio; ao aprovar a proposta, avaliar estender o TR4 ou somar um',
                     'spot para cobrir os 0,92 m² adicionais de teto da cozinha.']] + p04t.NOTAS,
               size=8.0, lh=11.4, gap=5.5)

    rodape_alt(d,
               'Fluxo = área × lux ÷ (0,60 × 0,80). Fatores de utilização e manutenção são hipóteses; a laje aparente escura reduz o fator de utilização e deve ser reavaliada.',
               'Carga térmica não é carga final — ver Alt A · 10 para a base recalculada com as áreas desta proposta.',
               'Alt A · 07 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-08 — elétrica: tomadas, comandos e quadro
# ---------------------------------------------------------------------------
def construir_08_eletrica():
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Tomadas, comandos e quadro', 'Reservas de localização — sem mudança nesta proposta; T12 é a única posição que a alteração afeta, e só na folga até a parede.',
               8, 'quadro junto à porta de entrada', 'T12 ganha folga até a parede nova')

    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    # realce leve na parede nova
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x - 1.5, y - 1.5, w_ + 3, h_ + 3, fill='none', stroke=DEMO, sw=1.1, dash='3 2.5')

    for k, lx, ly in (('jantar', 520.0, 145.0), ('sala', 500.0, 300.0),
                      ('cozinha', 310.0, 350.0), ('closet', 300.0, 508.0),
                      ('quarto', 500.0, 480.0), ('banheiro', 380.6, 428.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=False, size=8.4)

    for (ident, xm, ym) in p05e.TOMADAS_EXIST:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.6, fill=BG, stroke=EXIST, sw=1.5)
        d.circle(cx, cy, 1.8, fill=EXIST)
        d.txt(cx, cy - 9, ident, 6.6, EXIST, 'bold', 'middle', ls=0.3)

    for (ident, xm, ym, uso) in p05e.TOMADAS_NOVAS:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.6, fill=CIANO, stroke=K, sw=1.3)
        d.circle(cx, cy, 1.8, fill=NEW)
        d.txt(cx, cy - 9, ident, 6.6, K, 'bold', 'middle', ls=0.3)
        if ident == 'T12':
            wx, wy = d.P(*WALL_NOVA[:2])
            d.circle(cx, cy, 11.0, fill='none', stroke=DEMO, sw=1.3)
            d.line(cx, cy + 11.0, cx, wy, DEMO, 1.0, opacity=0.7)
            d.txt(cx + 10, cy + 22, 'folga sobe de ~0,15 p/ ~0,60 m', 6.8, DEMO, 'bold', 'start', ls=0.2)

    for (ident, xm, ym) in p05e.COMANDOS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 5.2, cy - 5.2, 10.4, 10.4, fill=BG, stroke=INK, sw=1.3)
        d.line(cx - 2.4, cy + 2.4, cx + 2.4, cy - 2.4, INK, 1.2)
        if ident in p05e.ROTULO_LESTE:
            d.txt(cx + 8.5, cy + 2.4, ident, 6.6, INK, 'bold', 'start', ls=0.3)
        else:
            d.txt(cx, cy - 9, ident, 6.6, INK, 'bold', 'middle', ls=0.3)

    cx, cy = d.PM(*p05e.QUADRO)
    d.rect(cx - 10, cy - 7, 20, 14, fill=MAGENTA18, stroke=DEMO, sw=1.8)
    for i in range(3):
        d.line(cx - 6 + i * 6, cy - 4, cx - 6 + i * 6, cy + 4, DEMO, 1.1)
    d.txt(cx, cy + 20, 'QUADRO DE ENERGIA', 7.6, DEMO, 'bold', 'middle', ls=0.4)
    d.txt(cx, cy + 30, 'posição indicada pelo cliente', 7.0, INK_SOFT, 'normal', 'middle')

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dotf', EXIST, 'Tomada existente'),
                ('fill', CIANO, 'Tomada nova (reserva)'),
                ('fill', BRANCO, 'Comando / interruptor'),
                ('fill', MAGENTA18, 'Quadro de energia'),
                ('ghost', DEMO, 'Parede nova, nesta proposta')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('Grupo', 0.24, 'start'), ('Reservas', 0.40, 'start'),
                  ('Revisão necessária', 0.36, 'end')],
                 p05e.LINHAS, titulo='RESERVAS DE INFRAESTRUTURA ELÉTRICA')
    paragrafos(d, cx2, fim + 20, cw,
               [['**Nenhum ponto muda de posição nesta proposta.',
                 'Todas as reservas — existentes e novas — seguem exatamente onde estão na',
                 'REV. M. O único efeito da parede nova é sobre T12 (tomada de forno/lava-',
                 'louças): a folga até a parede sobe de aproximadamente 0,15 m para 0,60 m,',
                 'o que facilita a instalação, não a obriga a mudar de lugar.']] + p05e.NOTAS,
               size=8.0, lh=11.2, gap=5.0)

    rodape_alt(d,
               'Posições aproximadas sobre o modelo do scan. Quadro e trajetos existentes não estão identificados no levantamento: confirmar em campo antes de qualquer medição.',
               'Este desenho é reserva de localização — não substitui projeto elétrico com memorial, diagrama unifilar e dimensionamento.',
               'Alt A · 08 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-09 — esquadrias e dados do levantamento
# ---------------------------------------------------------------------------
def construir_09_esquadrias():
    usar(ALT_WALLS, ALT_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Quadro de esquadrias e dados do levantamento', 'Idêntico à REV. M — nenhuma esquadria muda de vão nesta proposta. J06, a janela do closet, é a que fica mais perto da alteração.',
               9, 'seis janelas · três portas', 'nenhuma esquadria afetada por esta proposta')

    cols = (192, 382, 572)
    linhas_y = (322, 522, 722)
    for i, item in enumerate(ESQUADRIAS):
        p06e.desenha_esquadria(d, cols[i % 3], linhas_y[i // 3], item)

    d.rect(70, 778, p06e.ESC, 5, fill=K, stroke=K, sw=0.8)
    d.rect(70 + p06e.ESC, 778, p06e.ESC, 5, fill=BRANCO, stroke=K, sw=0.8)
    d.txt(70, 796, '0', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + p06e.ESC, 796, '1', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + 2 * p06e.ESC, 796, '2', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + 2 * p06e.ESC + 13, 796, 'm   (elevação das esquadrias)', 7.2, INK_SOFT)
    legenda(d, [('fill', CIANO18, 'Janela'), ('fill', BRANCO, 'Porta'),
                ('line', K, 'Nível do piso acabado')],
            70, 828, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Dado', 0.42, 'start'), ('Valor', 0.22, 'end'), ('Observação', 0.36, 'end')],
                 p06e.TAB_DADOS, titulo='DADOS DO LEVANTAMENTO')
    fim = tabela(d, cx, fim + 30, cw,
                 [('Ambiente', 0.16, 'start'), ('Itens reconhecidos pelo scan (m)', 0.84, 'start')],
                 p06e.TAB_INV, titulo='INVENTÁRIO DO SCAN — NÃO É ESPECIFICAÇÃO', alt=17)
    paragrafos(d, cx, fim + 22,
               cw, [['**Por que esta folha é igual à da REV. M.',
                     'A alteração desliza uma parede interna 0,45 m — nenhuma esquadria muda',
                     'de largura, altura ou posição. J06 (a janela do closet) é a mais próxima:',
                     'fica na parede sul, que esta proposta não toca, então seu vão de 2,00 ×',
                     '2,15 m permanece igual. O que muda é a profundidade do ambiente atrás',
                     'dela, não o vão em si.']] + p06e.NOTAS,
               size=8.0, lh=11.4, gap=5.5)

    rodape_alt(d,
               'Larguras do relatório do scan (captura 02.09.2026); alturas de janela e porta conforme medição do cliente em 12.09.2026. Vão livre; marco, contramarco e acabamento não estão medidos.',
               'Quadro de referência de estudo preliminar — não é lista de compra nem pedido de fabricação.',
               'Alt A · 09 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-10 — ar, exaustão e iluminação: base de cálculo (recalculada)
# ---------------------------------------------------------------------------
TAB_TERM_ALT = [
    ('Social + cozinha',   '38,72 m²', '23.232 BTU/h', '30.976 BTU/h'),
    ('Quarto + closet',    '17,78 m²', '10.668 BTU/h', '14.224 BTU/h'),
    ('Total sem banheiro', '56,50 m²', '33.900 BTU/h', '45.200 BTU/h'),
]
TAB_EXA_ALT = [
    ('EX01', 'Banheiro', '3,80 × 2,40 = 9,12 m³', '× 10', '91,2 m³/h'),
    ('CF01', 'Cozinha isolada — hipótese', '9,82 × 2,62 = 25,73 m³', '× 12', '308,7 m³/h'),
]
TAB_LUZ_ALT = [
    ('Sala',     '23,00', '150 lux', '7.188 lm', '2.700 K', 'leitura e cenas dimerizáveis'),
    ('Quarto',   '13,40', '150 lux', '4.188 lm', '2.700 K', 'cabeceira independente'),
    ('Cozinha',  '9,82',  '300 lux', '6.138 lm', '3.000 K', 'bancada à parte, 500 lux'),
    ('Jantar',   '5,90',  '150 lux', '1.844 lm', '2.700 K', 'pendente sobre a mesa'),
    ('Closet',   '4,38',  '200 lux', '1.825 lm', '3.000 K', 'luz vertical das roupas'),
    ('Banheiro', '3,80',  '200 lux', '1.583 lm', '3.000 K', 'espelho frontal e balizamento'),
]


def construir_10_ar_luz():
    d = folha_nova()
    cabeca_alt(d, 'Ar, exaustão e iluminação: base de cálculo', 'Mesma planilha da REV. M, recalculada com as áreas desta proposta — cozinha e closet trocam 0,92 m² entre si.',
               10, '45.200 BTU/h na base sol — total sem mudança', 'cozinha ganha carga, closet perde, na mesma proporção')

    cx, cw = MARGIN, 648
    fim = tabela(d, cx, 158, cw,
                 [('Premissa', 0.30, 'start'), ('Valor', 0.24, 'start'),
                  ('Condição', 0.46, 'start')],
                 p11.TAB_PREM, titulo='PREMISSAS — O QUE A CONTA ASSUME', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('Zona térmica', 0.26, 'start'), ('Área m²', 0.13, 'end'),
                  ('Base sombra', 0.16, 'end'), ('Base sol', 0.15, 'end'),
                  ('Atende', 0.30, 'end')],
                 TAB_TERM_ALT, titulo='CARGA TÉRMICA — SELECIONAR PELA BASE SOL (RECALCULADA)', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('ID', 0.09, 'start'), ('Ambiente', 0.28, 'start'),
                  ('Volume', 0.27, 'start'), ('Trocas', 0.13, 'end'),
                  ('Vazão', 0.23, 'end')],
                 TAB_EXA_ALT, titulo='EXAUSTÃO — VAZÃO A VALIDAR COM PERDA DE CARGA (RECALCULADA)', alt=19)
    tabela(d, cx, fim + 38, cw,
           [('Ambiente', 0.20, 'start'), ('Área m²', 0.12, 'end'),
            ('Alvo', 0.13, 'end'), ('Fluxo', 0.14, 'end'),
            ('CCT', 0.13, 'end'), ('Camada adicional', 0.28, 'end')],
           TAB_LUZ_ALT, titulo='ILUMINAÇÃO — ALVO POR AMBIENTE (RECALCULADA)', alt=19)

    d.line(724, 140, 724, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 756, W - MARGIN - 756
    paragrafos(d, cx2, 168, cw2,
               [['**Só a divisão entre as duas zonas de dormir/social muda — os totais não.',
                 'Cozinha entra na zona "social + cozinha"; closet entra em "quarto + closet".',
                 'Cozinha ganha 0,92 m² e puxa a zona social de 37,80 para 38,72 m²; closet',
                 'perde a mesma faixa e a zona de dormir cai de 18,70 para 17,78 m². A soma',
                 'das duas zonas (56,50 m²) e a carga total (45.200 BTU/h na base sol) não',
                 'mudam — é a mesma casca redistribuída.'],
                ['**A vazão da coifa (CF01) sobe com a área da cozinha.',
                 'Cozinha isolada, hipótese que só vale com ela fechada: 9,82 × 2,62 m =',
                 '25,73 m³, × 12 renovações/hora = 308,7 m³/h — 28,9 m³/h a mais que os',
                 '279,8 m³/h da REV. M. Segue sem seleção de coifa: isso é vazão de',
                 'referência, não captura sobre o fogão.'],
                ['**Iluminação: cozinha sobe, closet desce, na mesma proporção da área.',
                 'Fluxo inicial da cozinha vai de 5.563 para 6.138 lm; do closet, de 2.208',
                 'para 1.825 lm. Alvo de lux e temperatura de cor não mudam — só a área',
                 'que multiplica o alvo.']] + list(p11.NOTAS),
               size=8.0, lh=11.4, gap=6.0)

    rodape_alt(d,
               'Regra 600/800 BTU/h por m² conforme orientação simplificada de fabricante; renovações por hora conforme prática corrente de ventilação. Nenhuma das duas substitui cálculo.',
               'Alvos de iluminância são proposta de projeto. Confirmar curva pressão × vazão do duto e fotometria da luminária antes de comprar.',
               'Alt A · 10 / %d' % PRANCHA_N)
    return d


# ---------------------------------------------------------------------------
# ALT-11 — quadro comparativo e riscos
# ---------------------------------------------------------------------------
def construir_11_riscos():
    usar(ORIG_WALLS, ORIG_ROOMS)
    d = folha_nova()
    cabeca_alt(d, 'Quadro comparativo e riscos', 'O que muda, o que não muda, e o que precisa de confirmação antes da obra.',
               11, '4 pontos catalogados  ·  1 impasse', 'orientação de escopo, não laudo')

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
               'Alt A · 11 / %d' % PRANCHA_N)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminhos = []
    FOLHAS = (
        (construir_01_planta,               'alt-a-01-planta'),
        (construir_02_demolicao,            'alt-a-02-demolicao'),
        (construir_03_escopo,               'alt-a-03-escopo'),
        (construir_04_sequencia,            'alt-a-04-sequencia'),
        (lambda: construir_piso('A'),       'alt-a-05-piso-cumaru'),
        (lambda: construir_piso('B'),       'alt-a-06-piso-monolitico'),
        (construir_07_teto,                 'alt-a-07-teto'),
        (construir_08_eletrica,             'alt-a-08-eletrica'),
        (construir_09_esquadrias,           'alt-a-09-esquadrias'),
        (construir_10_ar_luz,               'alt-a-10-ar-luz'),
        (construir_11_riscos,               'alt-a-11-riscos'),
    )
    for fn, nome in FOLHAS:
        caminho = salvar(fn(), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus MainFloor — Caderno Alternativo A: ' + nome)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
        caminhos.append(caminho)
    exportar_pdf_a3(caminhos, os.path.join(pasta, 'caderno-alternativo-a-A3.pdf'),
                    'MaxHaus MainFloor — Caderno Alternativo A: parede cozinha/closet, caderno completo')
    print('ok caderno alternativo a: %d folhas + pacote' % len(FOLHAS))
