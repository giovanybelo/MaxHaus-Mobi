# -*- coding: utf-8 -*-
"""Prancha 01 — Planta baixa cotada (REV. H).

Cruza o levantamento por scan (Polycam, captura 02.09.2026) com as decisões já
fechadas no caderno: é a folha de referência dimensional do MainFloor, no estado
proposto, com cotas, cadeias, norte e quadro de ambientes.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. I'
PRANCHA = 'Prancha 01 / 06'

TAB_AMB = [(n, '%s m²' % br(a), '%s m' % br(per, 1), bb, ins)
           for (n, a, per, bb, ins, _w) in AMBIENTES_SCAN] + \
          [('MainFloor', '60,30 m²', '78,1 m', '7,85 × 9,43', '—')]

NOTAS = [
    ['**Como esta planta foi levantada.',
     'Scan 3D Polycam, captura de 02.09.2026, relatório exportado em 07.09.2026. Paredes, vãos e',
     'polígonos de ambiente foram lidos do vetor do arquivo em pontos PDF e convertidos pela escala',
     '45,66 pt/m, conferida duas vezes contra as cotas gerais: 358,33 pt / 7,85 m e 430,56 pt / 9,43 m.',
     'O próprio relatório avisa que são estimativas — nenhuma cota aqui substitui medição em campo.'],
    ['**Pé-direito 2,40 m, medido com o forro — e o forro vai sair.',
     'Os seis ambientes dão 2,40 m e o volume fecha em 144,51 m³. Com a retirada total do forro (D07),',
     'a altura livre passa a ser a face inferior da laje, que o scan não mede: levantar o plenum logo',
     'na demolição. Isso decide a folga da porta de correr de 2,30 m e a altura de trilhos e',
     'evaporadoras. A porta de entrada existente já tem 2,30 m — o vão de 2,30 cabe.'],
    ['**Espessuras e níveis.',
     'Todas as paredes lidas no scan têm 0,10 m. A nova drywall (R01) repete a espessura, salvo se o',
     'trilho da porta de correr for embutido em cassete — aí a parede engrossa. Cota de nível ±0,00 =',
     'piso acabado atual; com a troca de piso o nível final muda e precisa ser amarrado ao hall.'],
    ['**Diferença entre as áreas do relatório.',
     'Área externa 64,70 m² (inclui paredes), área útil 60,20 m² pelo relatório e 60,30 m² pela soma',
     'dos seis ambientes — a diferença é arredondamento. O caderno usa 60,30 m². Área de parede',
     '130,40 m², área de janela 12,70 m², perímetro somado dos ambientes 78,10 m.'],
    ['**Bounding box não é o ambiente.',
     'As dimensões do relatório vêm em duas leituras: o menor retângulo que contém o ambiente (B) e o',
     'maior retângulo inscrito (I). Em planta irregular — sala e cozinha — as duas divergem bastante:',
     'usar a inscrita para conferir mobiliário e a cotada em planta para obra.'],
    ['**O norte foi medido, não arbitrado: 126° do topo da folha.',
     'O relatório do pavimento superior — mesma captura — traz rosa dos ventos e GPS; o do MainFloor',
     'não traz nenhum dos dois. As duas plantas estão desenhadas com 180° de diferença, confirmado por',
     'dois elementos que os pavimentos compartilham: a caixa da escada e a área da piscina, que só cai',
     'no terraço de cima com essa rotação. A pétala N do Upfloor marca −53,97°; somados 180°, dá 126°.'],
    ['**As duas fachadas envidraçadas dão para NOROESTE e NORDESTE.',
     'Noroeste: jantar (J01), sala (J02 e J03) e uma janela do quarto (J04) — é a face que toma o sol',
     'de tarde, o mais quente. Nordeste: a outra janela do quarto (J05) e o closet (J06), sol de manhã.',
     'As outras duas faces são divisa, a sudeste e a sudoeste. Coordenadas do levantamento:',
     '23°36\'46,8"S  46°44\'15,8"O, altitude 822 m.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Planta baixa cotada — estado proposto',
              'Folha de referência dimensional. Cotas em metros, sobre o levantamento por scan de 02.09.2026; conferir em campo antes de qualquer medição.',
              REV, 'norte 126° — medido pela rosa do pavimento superior',
              'paredes 0,10 m  ·  nível ±0,00 = piso acabado atual')

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
                      ('cozinha', 300.0, 360.0), ('closet', 297.0, 500.0),
                      ('quarto', 505.0, 505.0), ('banheiro', 380.6, 372.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=True, size=8.2)

    # ---------------- cotas externas ----------------
    cadeia_h(d, [245.70, 343.39, 347.96, 604.03], 554.94, 24)
    cota_h(d, 245.70, 604.03, 554.94, 48, '7,85', size=8.0)
    cadeia_v(d, [124.38, 208.91, 282.54, 430.06, 434.63, 554.94], 245.70, -24)
    cota_v(d, 124.38, 554.94, 245.70, -48, '9,43', size=8.0)
    cadeia_h(d, [446.11, 450.68, 599.46, 604.03], 124.38, -24)
    cota_h(d, 446.11, 604.03, 124.38, -48, '3,46', size=8.0)
    # fachada leste: posição dos vãos
    cadeia_v(d, [124.38, 142.50, 193.20, 215.00, 300.80, 348.00, 394.40,
                 455.70, 509.80, 554.94], 604.03, 24, size=6.2)
    cota_v(d, 124.38, 554.94, 604.03, 48, '9,43', size=8.0)

    # ---------------- cotas internas ----------------
    cota_h(d, 347.96, 413.33, 330.22, 15, size=6.4, ext=False)     # banheiro
    cota_v(d, 330.22, 450.67, 413.33, -15, size=6.4, ext=False)
    cota_h(d, 250.26, 343.39, 550.38, -16, size=6.6, ext=False)    # closet
    cota_h(d, 347.96, 599.46, 550.38, -16, size=6.6, ext=False)    # quarto
    cota_h(d, 417.90, 599.46, 430.06, -16, size=6.6, ext=False)    # sala
    cota_v(d, 213.47, 430.06, 599.46, -16, size=6.6, ext=False)
    cota_h(d, 250.26, 343.39, 430.06, -16, size=6.6, ext=False)    # cozinha
    cota_v(d, 213.47, 430.06, 275.52, 16, size=6.6, ext=False)

    # ---------------- norte + nível ----------------
    norte(d, 214, 218, 19)
    nx, ny = d.P(470.0, 372.0)
    d.add('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="none" stroke="%s" stroke-width="1.1"/>'
          % (nx, ny, nx - 5, ny - 8, nx + 5, ny - 8, INK))
    d.line(nx - 16, ny - 8, nx + 16, ny - 8, INK, 1.1)
    d.txt(nx + 20, ny - 4, '±0,00', 7.4, INK, 'bold', 'start', ls=0.3)
    d.txt(nx + 20, ny + 5, 'piso acabado atual', 6.6, INK_SOFT, 'normal', 'start')

    escala(d, 182 + BUILDING_H * S + 74)
    legenda(d, [('fill', K07, 'Área útil — 60,30 m²'),
                ('line', DIM, 'Linha de cota (m)'),
                ('ghost', WALL, 'Vão de esquadria — ver Prancha 06')],
            70, 182 + BUILDING_H * S + 108, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.24, 'start'), ('Área', 0.15, 'end'),
                  ('Perímetro', 0.17, 'end'), ('Bounding box', 0.22, 'end'),
                  ('Inscrita', 0.22, 'end')],
                 TAB_AMB, titulo='QUADRO DE AMBIENTES — LEVANTAMENTO (m, m²)')
    paragrafos(d, cx, fim + 30, cw, NOTAS, size=8.4, lh=12.4, gap=7.0)

    rodape(d,
           'Cotas extraídas do modelo do scan e arredondadas ao centímetro. O relatório do levantamento declara que os valores são estimativas: conferir em campo antes de fabricar esquadria, marcenaria ou bancada.',
           'Planta de estudo preliminar. Não é planta executiva liberada: faltam projeto estrutural, hidráulica, elétrico executivo e aprovação do condomínio.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-01-planta-cotada')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-01-planta-cotada-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 01: planta baixa cotada')
    exportar_png(caminho, os.path.join(pasta, 'prancha-01-planta-cotada.png'))
    print('ok prancha 01')
