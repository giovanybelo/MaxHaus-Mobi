# -*- coding: utf-8 -*-
"""Prancha 02 — Demolição e desmontagem (REV. C)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. C'
PRANCHA = 'Prancha 02 / 08'

# --- alvos: (id, x_pt, y_pt, tipo, dx_rotulo, dy_rotulo) --------------------
ALVOS = [
    ('D01', 508.7, 432.3, 'demo',  10, -6),
    ('D02', 380.6, 430.0, 'demo',  10,  4),
    ('D03', 366.0, 340.0, 'demo', -10,  3),
    ('D04', 345.7, 368.0, 'demo', -10,  3),
    ('D05', 525.0, 137.0, 'demo',  10,  3),
    ('D06', 448.4, 152.0, 'demo', -10,  3),
    ('D07', 324.0, 211.2, 'demo',  -9, -7),
    ('D08', 448.4, 195.0, 'demo',  10,  3),
    ('D09', 545.0, 300.0, 'demo',  10,  3),
    ('D10', 520.0, 520.0, 'demo',  10,  3),
    ('M01', 300.0, 520.0, 'desm',  10,  3),
    ('K01', 380.6, 409.0, 'keep',  10, -5),
    ('K02', 380.6, 453.0, 'keep',  10, 10),
]
COR = {'demo': DEMO, 'desm': NEW, 'keep': KEEP}

LINHAS = [
    ('D01', 'Drywall entre sala e quarto', '1 trecho — 4,08 m'),
    ('D02', 'Box do banheiro: fechamento e base', '1 conjunto — vidro preservado'),
    ('D03', 'Piso do banheiro', '3,80 m²'),
    ('D04', 'Parede atrás do espelho e da bancada', '1 trecho — 2,64 m a conferir'),
    ('D05', 'Canto alemão do jantar', '1 conjunto — inventário por módulo'),
    ('D06', 'Espelho de parede do jantar', '1 peça — não confundir com a fachada'),
    ('D07', 'Parede da escada', 'trecho a confirmar em obra'),
    ('D08', 'Parede entre a escada e o jantar', '1 trecho — 1,95 m'),
    ('D09', 'Forro: retirar 100%', '60,30 m² menos a área marcada de 5,76 m²'),
    ('D10', 'Retirar pisos do MainFloor', '60,30 m² úteis, sem dupla contagem'),
    ('M01', 'Desmontar e remontar closet', '1 conjunto — inventário por módulo'),
    ('K01', 'Vidro do box — MANTER', '1 peça'),
    ('K02', 'Pano de vidro chão-teto do box — MANTER', '1,63 m, ponta a ponta'),
]

NOTAS = [
    ['**Sem forro. O teto do MainFloor passa a ser a laje de concreto aparente:',
     'a retirada do forro é total, não parcial. Só o banheiro admite forro, para abrigar',
     'a exaustão e a luminária embutida. Toda a iluminação e o ar-condicionado dos demais',
     'ambientes serão aplicados na laje — ver Prancha 04.'],
    ['**O fundo do box não é parede: é um pano de vidro chão-teto, ponta a ponta.',
     'O scan leu esse pano como vão. A correção vale para todas as pranchas do caderno.',
     'O vidro permanece; o que sai é o fechamento do box, o revestimento e o piso.'],
    ['**Drywall: não somar as duas faces como área de parede demolida.',
     'Aberturas, montantes, instalações internas e encontros exigem conferência. O desenho',
     'marca apenas o trecho entre sala e quarto.'],
    ['**Closet: etiquetar módulos e ferragens, fotografar, acondicionar e proteger.',
     'A área de 5,30 m² é do ambiente, não é área de marcenaria.'],
    ['**Escada: dois alvos distintos.',
     'A parede entre a escada e o jantar (D08) está identificada no scan. A parede da escada',
     '(D07) precisa ser apontada presencialmente antes de entrar em orçamento.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Demolição e desmontagem',
              'Diagrama de escopo sobre o modelo de trabalho. Conferir os alvos presencialmente antes de mobilizar a demolidora.',
              REV, 'sem forro: laje de concreto aparente',
              'fundo do box é pano de vidro chão-teto')

    # ---------------- planta ----------------
    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, '#eeebe4')
    paredes(d, ghost_drywall=False)
    janelas(d)
    vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    escada(d)

    # elementos a demolir, realçados
    for r in (DRYWALL_SALA_QUARTO, PAREDE_ESCADA_JANTAR, BOX_WC, BANCADA_WC, CANTO_ALEMAO):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=DEMO, opacity=0.22)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
    # parede da escada (alvo a confirmar)
    x, y, w_, h_ = d.R((321.40, 208.91, 328.00, 251.70))
    d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
    # piso a retirar: varredura leve sobre todo o pavimento
    for k in ROOM_ORDER:
        pp = [d.P(px, py) for px, py in ROOMS[k]['poly']]
        x0, y0, x1, y1 = bbox(pp)
        yy = y0
        while yy <= y1:
            for (a, b) in spans_at_y(pp, yy):
                d.line(a, yy, b, yy, DEMO, 0.45, opacity=0.16)
            yy += 7.0
    rotulos(d, areas=False, size=8.4)

    # marcadores
    for (ident, xp, yp, tipo, dx, dy) in ALVOS:
        cx, cy = d.P(xp, yp)
        cor = COR[tipo]
        d.circle(cx, cy, 6.4, fill=BG, stroke=cor, sw=1.5)
        d.circle(cx, cy, 2.0, fill=cor)
        anchor = 'start' if dx > 0 else 'end'
        d.txt(cx + dx, cy + dy, ident, 8.0, cor, 'bold', anchor, ls=0.4)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dot', DEMO, 'Demolir / retirar'),
                ('dot', NEW, 'Desmontar e remontar'),
                ('dot', KEEP, 'Manter'),
                ('fill', '#e4b8b4', 'Elemento a demolir'),
                ('line', GLASS, 'Pano de vidro chão-teto')],
            70, 156 + BUILDING_H * S + 64)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    # ---------------- coluna direita ----------------
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('ID', 0.11, 'start'), ('Serviço', 0.56, 'start'),
                  ('Quantidade preliminar', 0.33, 'end')],
                 LINHAS, titulo='ESCOPO DE DEMOLIÇÃO E DESMONTAGEM')
    paragrafos(d, cx, fim + 30, cw, NOTAS)

    rodape(d,
           'Quantidades preliminares sobre o modelo do scan (02.09.2026): servem para orientar visita e proposta, não para fechar medição.',
           'Nenhum alvo foi verificado em campo. Instalações embutidas, estrutura e vedações devem ser identificadas antes do início dos serviços.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-02-demolicao')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-02-demolicao-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 02: demolição e desmontagem')
    exportar_png(caminho, os.path.join(pasta, 'prancha-02-demolicao.png'))
    print('ok prancha 02')
