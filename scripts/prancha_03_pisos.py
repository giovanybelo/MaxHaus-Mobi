# -*- coding: utf-8 -*-
"""Pranchas 03 e 04 — as duas propostas de piso (REV. K).

Opção A  cumaru-ferro, piso pronto em réguas, com a cozinha em monolítico.
Opção B  monolítico em todos os ambientes secos.

Uma folha para cada, na mesma escala e com o mesmo quadro de áreas, para
comparar lado a lado sem trocar de desenho.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'

AREA_CUMARU = 44.69          # sala + quarto + jantar + corredor
AREA_CUMARU_RESERVA = 49.16  # + 10% de corte e reposição
AREA_MONO_B = 56.50
AREA_WC = 3.80

SOLEIRA_WC = (413.33, 351.00, 417.90, 387.30)
SOLEIRA_ENTRADA = (275.52, 220.10, 280.09, 265.76)

CONTORNO_SECO = [(448.4,126.7),(601.7,126.7),(601.7,552.7),(248.0,552.7),
                 (248.0,284.8),(277.8,284.8),(277.8,211.2),(448.4,211.2)]

TAB_A = [
    ('Cumaru-ferro',      'sala 23,00 + quarto 13,40 + jantar 5,90 + corredor 2,39', '44,69 m²'),
    ('+ reserva de 10%',  'cortes, perdas e reposição futura',                       '49,16 m²'),
    ('Monolítico',        'cozinha 6,51 (de 8,90) + closet 5,30 — zona contínua',    '11,81 m²'),
    ('Banheiro',          'sistema à parte, área molhada, na mesma cota',             '3,80 m²'),
    ('MainFloor',         'total do pavimento',                                      '60,30 m²'),
]

TAB_B = [
    ('Monolítico',   'sala, quarto, cozinha, jantar e closet — sem junta de material', '56,50 m²'),
    ('Sem reserva',  'aplicação moldada in loco, sem perda de corte',                   '—'),
    ('Banheiro',     'sistema à parte, área molhada, na mesma cota',                    '3,80 m²'),
    ('MainFloor',    'total do pavimento',                                             '60,30 m²'),
]

NOTAS_A = [
    ['**A zona monolítica da opção A quase não tem problema de junta.',
     'São 11,81 m² num pano estreito: cabe em um ou dois painéis, e a junta de material com o',
     'cumaru já resolve a maior parte do movimento. O desenho de juntas vira questão de verdade',
     'só na opção B, com 56,50 m² contínuos — ver a Prancha 04.'],
    ['**Cozinha e closet formam uma zona monolítica só.',
     'A zona é um retângulo contínuo, da parede oeste até a linha da sala e do degrau até a fachada',
     'sul, passando pela abertura entre cozinha e closet. O corredor da entrada e a escada ficam em',
     'cumaru; o monolítico cobre a cozinha de trabalho e o closet.'],
    ['**A ponta é canto reto com filete de 0,70 m de raio.',
     'Não é mais um arco achatado atravessando a cozinha: o limite corre reto pela linha do degrau,',
     'vira reto na linha da sala, e só a quina que aparece no corredor é arredondada. Um quarto de',
     'círculo tangente aos dois lados — geometria que o marceneiro e o aplicador sabem replicar com',
     'um compasso, e que o perfil de transição consegue acompanhar.'],
    ['**A junta é o detalhe mais caro desta opção.',
     'Perfil de transição com junta de movimentação, reto nos trechos retos e curvo só no filete.',
     'E as duas espessuras têm de ser niveladas no contrapiso para se encontrarem rentes: régua',
     'pronta com manta e monolítico somam alturas diferentes, e é no contrapiso que se acerta a',
     'diferença, não na soleira.'],
    ['**Cumaru-ferro é madeira densa — o que é virtude e é risco.',
     'Dureza e resistência altas, e por isso mesmo muito sensível a umidade e a base torta. Exige',
     'contrapiso seco, plano e nivelado (P06), aclimatação das réguas no ambiente antes de assentar',
     'e folga de dilatação em todo o perímetro, escondida no rodapé. Piso pronto reduz obra, mas',
     'não dispensa nenhuma dessas três condições.'],
    ['**O desenho das réguas é hipótese, não especificação.',
     'Réguas de 0,22 m correndo norte-sul, paralelas ao lado maior do pavimento, com topos a cada',
     '3,00 m defasados de um terço. Largura, comprimento e sentido de assentamento são decisão de',
     'projeto: o sentido muda a leitura do espaço e a percepção do desnível do contrapiso.'],
    ['**O banheiro fica fora dos dois sistemas, mas na mesma cota.',
     'Sistema próprio, com impermeabilização, caimento e acabamento antiderrapante, nivelado com o',
     'piso seco (P05): a soleira é junta de material, não degrau. Sem degrau, ralo linear e fecho de',
     'vidro assumem a contenção de água.'],
]

NOTAS_B = [
    ['**Um sistema só, sem junta de material entre os ambientes secos.',
     'O piso corre contínuo da entrada ao quarto. Não há curva porque não há encontro de materiais:',
     'a ponta em curva da cozinha só existe na opção A. As únicas transições são a soleira do',
     'banheiro — sem degrau — e a da porta de entrada.'],
    ['**Contínuo não quer dizer sem junta — e quantas juntas depende do sistema.',
     'Cimentício (cimento queimado, concreto polido, autonivelante aparente) retrai ao curar e',
     'acompanha o movimento da laje: trabalha em painéis de 3 a 6 m de lado, próximos do quadrado,',
     'o que dá de 4 a 8 juntas nos 56,50 m². Microcimento de 2 a 3 mm, com tela e primer, reduz as',
     'juntas às do substrato e à dessolidarização de perímetro. Resina epóxi ou poliuretano fecha',
     'contínuo de verdade, mas tem cara de resina e não de concreto.'],
    ['**Três juntas são obrigatórias em qualquer sistema.',
     'Sobre junta estrutural ou linha de viga, porque ali a laje se move e o acabamento trinca se',
     'for contínuo. No perímetro, para o pano poder trabalhar sem romper no canto — fica escondida',
     'no rodapé. E na parada de concretagem, onde a aplicação do dia terminou.',
     'A boa notícia: a casa já tem lugares naturais para elas — a soleira da entrada, a do banheiro',
     'e a linha da porta de correr entre sala e quarto.'],
    ['**Peça a paginação de juntas junto com a proposta, antes de assinar.',
     'Quem desenha as juntas escolhe onde a trinca vai aparecer; quem não desenha deixa o material',
     'escolher. Fornecedor que promete 56,50 m² sem nenhuma junta ou está propondo resina, ou não',
     'vai entregar o que prometeu — trinca em piso monolítico não tem remendo invisível.'],
    ['**A base manda no resultado — o monolítico copia o que está embaixo.',
     'Depois de retirar os pisos (D08), todo o contrapiso é lixado, regularizado e nivelado (P06),',
     'com conferência de aderência, umidade e fissuras. Espessura, sistema e acabamento ainda não',
     'estão especificados: cor e textura do desenho são ilustrativas.'],
    ['**O banheiro fica fora do monolítico, mas na mesma cota.',
     'Sistema próprio, com impermeabilização, caimento e acabamento antiderrapante, nivelado com o',
     'piso seco (P05). Sem degrau, ralo linear e fecho de vidro assumem a contenção de água, e a',
     'impermeabilização sobe também na parede nova do fundo do box (R02).'],
    ['**Sequência importa mais que no piso em réguas.',
     'O monolítico entra depois das paredes prontas e antes da marcenaria: o closet (M01) só volta',
     'depois do piso curado. Prever tempo de cura e proteção da superfície até o fim da obra.'],
]


def hachura_wc(d, rect_pt, passo=8.0):
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


def soleira(d, rect_pt):
    x0, y0, x1, y1 = rect_pt
    if (x1 - x0) < (y1 - y0):
        xm = (x0 + x1) / 2.0
        tracejado(d, [(xm, y0), (xm, y1)])
    else:
        ym = (y0 + y1) / 2.0
        tracejado(d, [(x0, ym), (x1, ym)])


def construir(opcao='A'):
    A = (opcao == 'A')
    d = folha_nova()
    if A:
        cabecalho(d, 'Opção A — cumaru-ferro, cozinha e closet em monolítico',
                  'Piso pronto em réguas nas áreas de estar e dormir; cozinha e closet numa zona monolítica contínua. Cores e desenho de régua ilustrativos.',
                  REV, 'norte 126°  ·  Prancha 03 de 07',
                  'ponta arredondada: canto reto com filete de 0,70 m')
    else:
        cabecalho(d, 'Opção B — monolítico em todo o MainFloor',
                  'Sistema único nos cinco ambientes secos, com o banheiro à parte. Cores ilustrativas; nenhum produto, espessura ou acabamento especificado.',
                  REV, 'norte 126°  ·  Prancha 04 de 07',
                  'piso contínuo — sem junta de material entre ambientes secos')

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
        d.path(path_d([d.P(a, b) for a, b in CONTORNO_SECO]), fill=MONO)

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
    if A:
        # junta só onde os dois pisos realmente se encontram — não sobre parede
        tracejado(d, [(280.09, 284.8), (313.74, 284.8)] + filete_pts()
                     + [(345.7, 325.65)])
        tracejado(d, [(345.7, 453.0), (345.7, 513.42)])
        qx, qy = d.P(*PONTA_MONO)
        d.circle(qx, qy, 3.0, fill=K)
        d.line(qx, qy, qx + 46, qy - 36, K, 0.8)
        d.txt(qx + 50, qy - 40, 'PONTA ARREDONDADA', 7.4, K, 'bold', 'start', ls=0.4)
        d.txt(qx + 50, qy - 31, 'canto reto com filete de', 7.0, INK_SOFT, 'normal', 'start')
        d.txt(qx + 50, qy - 22, '0,70 m de raio', 7.0, INK_SOFT, 'normal', 'start')

    for k, lx, ly in (('jantar', 520.0, 152.0), ('sala', 500.0, 300.0),
                      ('cozinha', 300.0, 380.0), ('closet', 300.0, 500.0),
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
                 ('dash', JOINT, 'Junta / soleira de transição')]
    else:
        itens = [('fill', MONO, 'Piso monolítico contínuo'),
                 ('fill', WET, 'Banheiro — sistema à parte (área molhada)'),
                 ('dash', JOINT, 'Soleira / junta de transição')]
    legenda(d, itens, 70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Sistema', 0.22, 'start'), ('Onde', 0.56, 'start'), ('Área', 0.22, 'end')],
                 TAB_A if A else TAB_B, titulo='QUADRO DE ÁREAS')
    paragrafos(d, cx, fim + 30, cw, NOTAS_A if A else NOTAS_B,
               size=8.4, lh=12.0, gap=6.0)

    rodape(d,
           'Revestimento contínuo: toda a área de piso é revestida, inclusive sob móveis e equipamentos — nenhum recorte de mobiliário foi descontado. Áreas conforme o scan de 02.09.2026.',
           'Estudo preliminar de superfície: não substitui especificação de sistema, projeto de juntas nem memorial de aplicação do fornecedor.',
           'Prancha %s / 12' % ('03' if A else '04'), REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    for opc, nome, titulo in (('A', 'prancha-03-piso-cumaru', 'Prancha 03: piso em cumaru-ferro'),
                              ('B', 'prancha-04-piso-monolitico', 'Prancha 04: piso monolítico')):
        caminho = salvar(construir(opc), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus MainFloor — ' + titulo)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
    print('ok pranchas 03 e 04')
