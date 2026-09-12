# -*- coding: utf-8 -*-
"""Prancha 03 — Piso monolítico (REV. F).

A comparação cumaru × monolítico saiu: o cliente fechou o piso em monolítico.
Sobra um sistema único em todos os ambientes secos e o banheiro à parte — sem
junta de material no meio da planta, e por isso sem a ponta em curva da cozinha,
que só existia para resolver o encontro entre madeira e monolítico.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. J'
PRANCHA = 'Prancha 03 / 06'

# contorno único do piso seco (faces internas, pt) — o monolítico é uma peça só,
# então o desenho não pode mostrar a costura entre os polígonos de ambiente
CONTORNO_SECO = [(448.4,126.7),(601.7,126.7),(601.7,552.7),(248.0,552.7),
                 (248.0,284.8),(277.8,284.8),(277.8,211.2),(448.4,211.2)]

AREA_MONO = 56.50
AREA_WC = 3.80
AREA_TOTAL = 60.30

# soleiras / juntas de transição (retângulos em pt do scan)
SOLEIRA_WC = (413.33, 351.00, 417.90, 387.30)      # porta do banheiro
SOLEIRA_ENTRADA = (275.52, 220.10, 280.09, 259.20)  # limite do apartamento

TAB_AREAS = [
    ('Sala',              'monolítico contínuo',                    '23,00 m²'),
    ('Quarto',            'monolítico contínuo',                    '13,40 m²'),
    ('Cozinha',           'monolítico contínuo',                     '8,90 m²'),
    ('Jantar',            'monolítico contínuo',                     '5,90 m²'),
    ('Closet',            'monolítico contínuo',                     '5,30 m²'),
    ('Monolítico — total','cinco ambientes, sem junta de material',  '56,50 m²'),
    ('Banheiro',          'sistema à parte, área molhada',           '3,80 m²'),
    ('MainFloor',         'total do pavimento',                     '60,30 m²'),
]

NOTAS = [
    ['**Um sistema só, sem junta de material entre os ambientes secos.',
     'Com o cumaru fora, a ponta em curva da cozinha perde a função: ela existia apenas para',
     'resolver o encontro entre a madeira e o monolítico. O piso corre contínuo da entrada ao',
     'quarto; as únicas transições são a soleira do banheiro — agora sem degrau — e a da entrada.'],
    ['**Juntas de movimentação são projeto, não improviso de obra.',
     'Monolítico contínuo em 56,50 m² trabalha: prever juntas conforme o sistema escolhido,',
     'nos vãos de porta e nos encontros com a estrutura. Posição e desenho entram no executivo,',
     'junto com o fornecedor — uma trinca num piso sem junta não tem remendo invisível.'],
    ['**A base manda no resultado — o monolítico copia o que está embaixo.',
     'Depois de retirar os pisos (D08), todo o contrapiso é lixado, regularizado e nivelado (P06),',
     'com conferência de aderência, umidade e fissuras. Espessura, sistema e acabamento ainda não',
     'estão especificados: cor e textura do desenho são ilustrativas.'],
    ['**O banheiro fica fora do monolítico, mas na mesma cota.',
     'Sistema próprio, com impermeabilização, caimento e acabamento antiderrapante — só que nivelado',
     'com o piso seco (P05): a soleira passa a ser junta de material, não degrau. Sem degrau, a',
     'contenção de água é resolvida dentro do box, com ralo linear e fecho de vidro. A',
     'impermeabilização sobe também na parede nova do fundo do box (R02).'],
    ['**Encontro com a parede.',
     'Rodapé embutido, negativo ou pintura direta mudam o preparo das paredes e o corte do',
     'piso: definir antes de a empreiteira fechar o preparo para pintura.'],
    ['**Sequência importa mais que no piso em réguas.',
     'O monolítico entra depois das paredes prontas e antes da marcenaria: o closet (M01) só volta',
     'depois do piso curado. Prever tempo de cura e proteção da superfície até o fim da obra.'],
    ['**Sem reserva de corte.',
     'Aplicação moldada in loco não tem perda de régua, mas isso não é margem zero: prever',
     'retrabalho de textura e acerto de bordas. Os degraus da escada estão fora da conta;',
     'o piso sob a escada permanece.'],
]


def hachura_wc(d, rect_pt, passo=8.0):
    """45° clipado no retângulo do banheiro."""
    x0, y0, x1, y1 = rect_pt
    ax, ay = d.P(x0, y0)
    bx, by = d.P(x1, y1)
    w_, h_ = bx - ax, by - ay
    t = -h_
    while t <= w_:
        px0 = ax + max(0.0, t)
        py0 = ay + h_ - (px0 - (ax + t))
        px1 = min(ax + w_, ax + t + h_)
        py1 = ay + h_ - (px1 - (ax + t))
        if px1 > px0:
            d.line(px0, py0, px1, py1, WET_LINE, 0.6, opacity=0.85)
        t += passo


def soleira(d, rect_pt, rotulo=None):
    x0, y0, x1, y1 = rect_pt
    vertical = (x1 - x0) < (y1 - y0)
    if vertical:
        xm = (x0 + x1) / 2.0
        tracejado(d, [(xm, y0), (xm, y1)])
    else:
        ym = (y0 + y1) / 2.0
        tracejado(d, [(x0, ym), (x1, ym)])


def construir():
    d = folha_nova()
    cabecalho(d, 'Piso monolítico',
              'Sistema único em todo o MainFloor, com o banheiro à parte. Cores ilustrativas; nenhum produto, espessura ou acabamento especificado.',
              REV, 'proposta de cumaru encerrada',
              'piso contínuo — sem junta de material entre ambientes secos')

    S = 70.0
    d.set_plan(70, 156, S)
    d.path(path_d([d.P(px, py) for px, py in CONTORNO_SECO]), fill=MONO)
    # banheiro: sistema à parte
    pp = [d.P(px, py) for px, py in ROOMS['banheiro']['poly']]
    d.path(path_d(pp), fill=WET)
    hachura_wc(d, (345.7, 327.9, 415.6, 453.0))
    d.path(path_d(pp), fill='none', stroke=K, sw=1.0)

    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    soleira(d, SOLEIRA_WC)
    soleira(d, SOLEIRA_ENTRADA)

    for k, lx, ly in (('jantar', 520.0, 152.0), ('sala', 500.0, 300.0),
                      ('cozinha', 300.0, 360.0), ('closet', 300.0, 500.0),
                      ('quarto', 520.0, 500.0), ('banheiro', 380.6, 400.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    # respiro atrás do rótulo do banheiro, que cai sobre a hachura
    bx, by = d.P(ROOMS['banheiro']['lx'], ROOMS['banheiro']['ly'])
    d.rect(bx - 33, by - 9, 66, 24, fill=WET, opacity=0.95)
    rotulos(d, areas=True, size=8.4)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('fill', MONO, 'Piso monolítico contínuo'),
                ('fill', WET, 'Banheiro — sistema à parte (área molhada)'),
                ('dash', JOINT, 'Soleira / junta de transição')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.36, 'start'), ('Sistema', 0.38, 'start'),
                  ('Área', 0.26, 'end')],
                 TAB_AREAS, titulo='QUADRO DE ÁREAS')
    paragrafos(d, cx, fim + 34, cw, NOTAS, size=8.4, lh=12.4, gap=7.0)

    rodape(d,
           'Revestimento contínuo: toda a área de piso é revestida, inclusive sob móveis e equipamentos — nenhum recorte de mobiliário foi descontado. Áreas conforme o scan de 02.09.2026.',
           'Estudo preliminar de superfície: não substitui especificação de sistema, projeto de juntas nem memorial de aplicação do fornecedor.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-03-piso-monolitico')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-03-piso-monolitico-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 03: piso monolítico')
    exportar_png(caminho, os.path.join(pasta, 'prancha-03-piso-monolitico.png'))
    print('ok prancha 03')
