# -*- coding: utf-8 -*-
"""Prancha 07 — Quadro de esquadrias e dados do levantamento (REV. K)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. L'
PRANCHA = 'Prancha 07 / 07'

ESC = 55.0          # px por metro no desenho das esquadrias

TAB_DADOS = [
    ('Área útil (soma dos ambientes)', '60,30 m²', 'relatório arredonda para 60,20'),
    ('Área externa do pavimento',      '64,70 m²', 'inclui espessura de paredes'),
    ('Área de parede',                '130,40 m²', 'sem vãos'),
    ('Área de esquadria',              '14,77 m²', 'seis janelas, vão — scan dava 12,70'),
    ('Volume',                        '144,51 m³', 'com forro; ~158 m³ na laje aparente'),
    ('Perímetro somado dos ambientes', '78,10 m',  'não é perímetro do pavimento'),
    ('Pé-direito — laje',               '2,62 m',  'depois de retirar o forro (D07)'),
    ('Pé-direito — forro atual',        '2,42 m',  'plenum de 0,20 m'),
    ('Captura / exportação',   '02.09 / 07.09.2026', 'scan 3D Polycam'),
    ('Coordenadas',   '23°36\'46,8"S  46°44\'15,8"O', 'altitude 822 m — do scan superior'),
    ('Norte',                            '126°', 'do topo da folha, sentido horário'),
]

TAB_INV = [
    ('Sala',     'sofá 2,60 × 1,60 · mesa de centro 1,60 × 1,00 · 3 cadeiras · armário 2,50 × 0,40 · escada 0,80 × 3,00'),
    ('Quarto',   'cama 1,50 × 2,00 · bancada 3,00 × 0,50 · mesa 0,50 × 0,50 · cadeira'),
    ('Cozinha',  'armário 1,60 × 0,60 · cuba 0,70 × 0,60 · geladeira 0,90 × 0,80 (h 1,80) · forno · cooktop · lava-louças'),
    ('Jantar',   'armário de canto 2,50 × 0,40 — o canto alemão, item D05 da demolição'),
    ('Closet',   'marcenaria não discriminada pelo scan — inventariar módulo a módulo antes de desmontar (M01)'),
    ('Banheiro', 'bancada 1,70 × 0,40 · box 0,90 × 1,40 (h 2,10) · cuba 0,60 × 0,50 · bacia 0,40 × 0,70'),
]

NOTAS = [
    ['**Todas na mesma escala. Largura × altura de vão livre, não de marco.',
     'Peitoril, sentido de abertura e material não estão medidos: as três informações precisam de',
     'visita. Nenhuma esquadria deste caderno está liberada para fabricação.'],
    ['**As alturas das janelas vieram do cliente, não do scan.',
     'Cinco têm 1,63 m. A do closet (J06) vai do piso ao teto: 2,42 m de altura livre menos 0,15 m de',
     'apoio no topo e 0,10 m de peitoril, dando 2,00 × 2,17 m — e é o único peitoril medido até agora.',
     'As duas do quarto ficam idênticas, e a área de esquadria sobe de 12,70 para 14,77 m².'],
    ['**P03 é a única esquadria nova.',
     'Porta de correr de 1,00 × 2,29 m na drywall reconstruída, com a folha estacionando no 1,00 m',
     'de parede a leste do vão, pela face da sala. P02 mantém a folha existente de 0,80 × 2,00 m e',
     'só inverte o giro. P01, a porta de entrada, mede 1,00 × 2,29 m e não é alterada.'],
    ['**O inventário do scan serve para escopo, não para especificação.',
     'É o que o algoritmo reconheceu no dia da captura. Há erro evidente — uma "mesa lateral" de',
     '6,60 × 2,00 m que é a projeção da escada — e há ausência: o closet inteiro não foi',
     'discriminado. Use a lista para conferir o que sai, o que se desmonta e o que volta.'],
    ['**O que este caderno ainda não tem, e que um executivo exige:',
     'projeto estrutural para a furação da laje e a área da piscina; hidráulica e esgoto do banheiro',
     'e da cozinha; elétrico executivo com diagrama unifilar e cálculo de demanda; projeto de',
     'juntas do piso monolítico; detalhamento de marcenaria; e aprovação do condomínio.'],
]


def desenha_esquadria(d, x, ybase, item):
    ident, tipo, amb, larg, alt, area, sit = item
    w_, h_ = larg * ESC, alt * ESC
    x0 = x - w_ / 2.0
    y0 = ybase - h_
    porta = tipo.startswith('Porta')
    d.rect(x0, y0, w_, h_, fill=BRANCO if porta else CIANO18, stroke=K, sw=1.4)
    if porta:
        if 'correr' in tipo:
            d.line(x0 + w_ * 0.5, y0 + 4, x0 + w_ * 0.5, ybase - 4, K, 0.8, opacity=0.6)
            d.line(x0 + 6, ybase - h_ / 2, x0 + w_ - 6, ybase - h_ / 2, K, 1.0)
            d.add('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>'
                  % (x0 + w_ - 6, ybase - h_ / 2, x0 + w_ - 11, ybase - h_ / 2 - 2.6,
                     x0 + w_ - 11, ybase - h_ / 2 + 2.6, K))
        else:
            d.line(x0 + w_ * 0.82, ybase - h_ * 0.45, x0 + w_ * 0.82, ybase - h_ * 0.45, K, 1.0)
            d.circle(x0 + w_ * 0.84, ybase - h_ * 0.45, 2.0, fill=K)
    else:
        d.line(x0, ybase - h_ * 0.5, x0 + w_, ybase - h_ * 0.5, K, 0.8, opacity=0.55)
    d.line(x0 - 8, ybase, x0 + w_ + 8, ybase, K, 1.1)          # linha de piso
    d.txt(x, y0 - 10, ident, 10.0, K, 'bold', 'middle', ls=0.6)
    d.txt(x, ybase + 14, '%s × %s m' % (br(larg), br(alt)), 8.4, K, 'normal', 'middle')
    d.txt(x, ybase + 25, '%s · %s' % (tipo, amb), 7.6, INK_SOFT, 'normal', 'middle')
    d.txt(x, ybase + 35, sit, 7.4, DEMO if sit != 'manter' else INK_SOFT,
          'bold' if sit != 'manter' else 'normal', 'middle')


def construir():
    d = folha_nova()
    cabecalho(d, 'Quadro de esquadrias e dados do levantamento',
              'Todas as esquadrias na mesma escala. Alturas conforme medição do cliente; larguras do scan. Vão livre, não marco: conferir antes de fabricar.',
              REV, 'seis janelas · três portas',
              'peitoril, sentido de abertura e material a levantar')

    cols = (192, 382, 572)
    linhas_y = (322, 522, 722)
    for i, item in enumerate(ESQUADRIAS):
        desenha_esquadria(d, cols[i % 3], linhas_y[i // 3], item)

    # escala das esquadrias
    d.rect(70, 778, ESC, 5, fill=K, stroke=K, sw=0.8)
    d.rect(70 + ESC, 778, ESC, 5, fill=BRANCO, stroke=K, sw=0.8)
    d.txt(70, 796, '0', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + ESC, 796, '1', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + 2 * ESC, 796, '2', 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(70 + 2 * ESC + 13, 796, 'm   (elevação das esquadrias)', 7.2, INK_SOFT)
    legenda(d, [('fill', CIANO18, 'Janela'), ('fill', BRANCO, 'Porta'),
                ('line', K, 'Nível do piso acabado')],
            70, 828, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Dado', 0.42, 'start'), ('Valor', 0.22, 'end'), ('Observação', 0.36, 'end')],
                 TAB_DADOS, titulo='DADOS DO LEVANTAMENTO')
    fim = tabela(d, cx, fim + 36, cw,
                 [('Ambiente', 0.16, 'start'), ('Itens reconhecidos pelo scan (m)', 0.84, 'start')],
                 TAB_INV, titulo='INVENTÁRIO DO SCAN — NÃO É ESPECIFICAÇÃO')
    paragrafos(d, cx, fim + 28, cw, NOTAS, size=8.4, lh=12.4, gap=6.5)

    rodape(d,
           'Larguras do relatório do scan (captura 02.09.2026); alturas de janela e porta conforme medição do cliente em 12.09.2026. Vão livre; marco, contramarco e acabamento não estão medidos.',
           'Quadro de referência de estudo preliminar — não é lista de compra nem pedido de fabricação.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-07-esquadrias')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-07-esquadrias-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 07: esquadrias e levantamento')
    exportar_png(caminho, os.path.join(pasta, 'prancha-07-esquadrias.png'))
    print('ok prancha 06')
