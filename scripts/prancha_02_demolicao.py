# -*- coding: utf-8 -*-
"""Prancha 02 — Demolição e desmontagem (REV. C)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. D'
PRANCHA = 'Prancha 02 / 08'

# --- alvos: (id, x_pt, y_pt, tipo, dx_rotulo, dy_rotulo) --------------------
ALVOS = [
    ('D01', 508.7, 432.3, 'demo',  10, -6),
    ('D02', 380.6, 425.0, 'demo',  10,  4),
    ('D03', 366.0, 340.0, 'demo', -10,  3),
    ('D04', 345.7, 368.0, 'demo', -10,  3),
    ('D05', 525.0, 137.0, 'demo',  10,  3),
    ('D06', 380.6, 453.0, 'demo',  10, 11),
    ('D07', 545.0, 300.0, 'demo',  10,  3),
    ('D08', 520.0, 520.0, 'demo',  10,  3),
    ('P01', 448.4, 170.0, 'prep', -10,  3),
    ('P02', 380.0, 211.2, 'prep',   0, -8),
    ('R01', 555.0, 432.3, 'novo',  10, -6),
    ('R02', 353.0, 453.0, 'novo', -10, 11),
    ('M01', 300.0, 520.0, 'desm',  10,  3),
    ('K01', 380.6, 409.0, 'keep',  10, -5),
]
PREP = '#9a6b1f'
COR = {'demo': DEMO, 'desm': NEW, 'keep': KEEP, 'prep': PREP, 'novo': KEEP}

LINHAS = [
    ('D01', 'Drywall entre sala e quarto', '1 trecho — 4,08 m'),
    ('D02', 'Box do banheiro: fechamento e base', '1 conjunto'),
    ('D03', 'Piso do banheiro', '3,80 m²'),
    ('D04', 'Parede atrás do espelho e da bancada', '1 trecho — 2,64 m a conferir'),
    ('D05', 'Canto alemão do jantar', '1 conjunto — inventário por módulo'),
    ('D06', 'Pano de vidro chão-teto do fundo do box', '1,63 m, ponta a ponta'),
    ('D07', 'Forro: retirar 100%', '60,30 m² — teto passa a laje aparente'),
    ('D08', 'Retirar pisos do MainFloor', '60,30 m² úteis, sem dupla contagem'),
    ('P01', 'Parede do jantar: retirar espelho e revestimento', '1 trecho — 1,95 m, preparo p/ pintura'),
    ('P02', 'Parede sob a escada: retirar revestimento', 'trecho a confirmar — preparo p/ pintura'),
    ('R01', 'Nova drywall sala/quarto, com porta 1,00 × 2,30 m', '4,08 m + 1 porta'),
    ('R02', 'Nova parede de fechamento do box', '1,63 m, no lugar do vidro'),
    ('M01', 'Desmontar e remontar closet', '1 conjunto — inventário por módulo'),
    ('K01', 'Vidro do box — MANTER', '1 peça'),
]

NOTAS = [
    ['**Esta planta mostra o estado existente.',
     'O fundo do box aparece como o pano de vidro chão-teto que existe hoje (D06) e a drywall',
     'ainda sem porta. O estado proposto — parede fechando o box e drywall nova com porta —',
     'está desenhado nas Pranchas 03, 04 e 05.'],
    ['**Demolir para refazer, não só demolir.',
     'A drywall entre sala e quarto cai e é reconstruída (R01), agora com uma porta de',
     '1,00 × 2,30 m, na mesma altura da porta de entrada. O pano de vidro do fundo do box cai',
     'e vira parede (R02). Orçar demolição e reconstrução como serviços separados.'],
    ['**Banheiro: reforma integral.',
     'Saem piso, revestimentos, fechamento do box e a parede atrás do espelho e da bancada.',
     'O vidro do box (K01) segue marcado para manter conforme definição anterior — confirmar',
     'se a reforma integral o preserva.'],
    ['**Jantar e sob a escada: preparo, não demolição.',
     'Nessas duas paredes saem o espelho e os revestimentos e a superfície é preparada para',
     'pintura. A parede fica. O trecho sob a escada precisa ser apontado presencialmente.'],
    ['**Sem forro: a retirada é total, não parcial.',
     'O teto do MainFloor passa a ser a laje de concreto aparente. Só o banheiro admite forro,',
     'para abrigar a exaustão e a luminária. Ver Prancha 04.'],
    ['**Closet: etiquetar módulos e ferragens, fotografar, acondicionar e proteger.',
     'A área de 5,30 m² é do ambiente, não é área de marcenaria.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Demolição e desmontagem',
              'Diagrama de escopo sobre o modelo de trabalho. Conferir os alvos presencialmente antes de mobilizar a demolidora.',
              REV, 'estado existente: o que sai, o que se prepara',
              'demolir e reconstruir são serviços separados')

    # ---------------- planta ----------------
    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, '#eeebe4')
    paredes(d, estado='existente')
    janelas(d)
    vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    escada(d)

    # elementos a demolir, realçados
    for r in (DRYWALL_SALA_QUARTO, BOX_WC, BANCADA_WC, CANTO_ALEMAO, VIDRO_BOX):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=DEMO, opacity=0.22)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
    # paredes de preparo para pintura
    for r in (PAREDE_ESCADA_JANTAR, PAREDE_SOB_ESCADA):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=PREP, opacity=0.28)
        d.rect(x, y, w_, h_, fill='none', stroke=PREP, sw=1.1, dash='4 3')
    # porta nova na drywall reconstruída
    x, y, w_, h_ = d.R(PORTA_NOVA)
    d.rect(x, y - 1.5, w_, h_ + 3, fill='none', stroke=KEEP, sw=1.4, dash='4 3')
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
                ('dot', PREP, 'Retirar revestimento e preparar para pintura'),
                ('dot', KEEP, 'Reconstruir / manter'),
                ('dot', NEW, 'Desmontar e remontar'),
                ('line', GLASS, 'Pano de vidro existente')],
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
