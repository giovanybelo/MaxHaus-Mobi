# -*- coding: utf-8 -*-
"""Pacote para fornecedores — Caderno Alternativo A (parede cozinha/closet).

As mesmas cinco folhas do pacote da REV. M (fornecedores.py), com a parede
cozinha/closet na posição da proposta alternativa e as quantidades que dependem
dela recalculadas. Os desenhos e as tabelas são os do pacote principal,
reaproveitados por troca dos dados de módulo — só o que muda é redefinido aqui.

Cabeçalho e rodapé marcam ALTERNATIVO A em todas as folhas: o fornecedor não
pode confundir este pacote com o da REV. M.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base_mainfloor as bm
from base_mainfloor import *      # noqa
import fornecedores as fo
import prancha_02_demolicao as p02
from alt_a_parede_cozinha import (ORIG_WALLS, ORIG_ROOMS, ALT_WALLS, ALT_ROOMS,
                                  WALL_REMOVER_1, WALL_REMOVER_2, WALL_NOVA,
                                  ALVOS_ALT_EXTRA, usar)

fo.EMISSAO = 'ALT. A  ·  EMISSÃO 01'
fo.DATA = '23.09.2026'
fo.ORIGEM = 'extraído do Caderno Alternativo A'

CHAMADAS = {
    'FO1 — DEMOLIÇÃO': 'Escopo de retirada, preparo e reconstruções, com a parede cozinha/closet da proposta alternativa (D09, D10, R03). Planta no estado existente.',
    'FO2 — PISO': 'Duas opções para orçamento, na mesma escala. A parede cozinha/closet muda de lugar, mas as áreas por sistema são as mesmas da REV. M.',
    'FO3 — ELÉTRICA': 'Força, comando e quadro — pontos nas mesmas posições da REV. M. Iluminação na FO4 e ar-condicionado na FO5.',
    'FO4 — ILUMINAÇÃO': 'Trilho e luminárias sobre a laje aparente, nas mesmas posições da REV. M. Alvo de fluxo recalculado para cozinha e closet.',
    'FO5 — AR': 'Evaporadoras, exaustor e coifa sobre laje aparente. Somente Electrolux. Cargas por zona e vazão da coifa recalculadas.',
}


def cabeca_fo_alt(d, titulo, disciplina, chamada):
    d.txt(MARGIN, 42, 'MAXHAUS 81I  ·  PACOTE PARA FORNECEDORES  ·  ALTERNATIVO A',
          10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(MARGIN, 78, titulo, 27.0, INK, 'bold')
    d.txt(MARGIN, 99, CHAMADAS.get(disciplina, chamada), 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, fo.EMISSAO, 10.0, RED, 'bold', 'end', ls=0.8)
    d.txt(W - MARGIN, 78, disciplina, 10.5, INK, 'bold', 'end')
    d.txt(W - MARGIN, 99, fo.ORIGEM, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)


fo.cabeca_fo = cabeca_fo_alt

# ---------------------------------------------------------------------------
# FO1 — demolição: entra o ensaio estrutural e a parede cozinha/closet
# ---------------------------------------------------------------------------
fo.TAB_DEMO = [
    ('E01', 'Ensaio de estanqueidade (pressão) na hidráulica', '1 ensaio'),
    ('E02', 'Medição de resistência de isolamento na elétrica', '1 ensaio'),
    ('E03', 'Ensaio estrutural das paredes cozinha/closet, com engenheiro', '2 paredes'),
    ('M01', 'Desmontar closet, etiquetar módulos e ferragens, acondicionar', '1 conjunto'),
    ('D05', 'Retirar canto alemão do jantar', '1 conjunto'),
    ('D07', 'Retirar forro — 100%', '60,30 m²'),
    ('D01', 'Demolir drywall entre sala e quarto', '4,08 m'),
    ('D02', 'Demolir fechamento e base do box do banheiro', '1 conjunto'),
    ('D06', 'Demolir pano de vidro chão-teto do fundo do box', '1,63 m'),
    ('D04', 'Demolir parede atrás do espelho e da bancada do banheiro', '2,64 m a conferir'),
    ('D09', 'Demolir parede interna do closet — somente após E03', '2,54 m'),
    ('D10', 'Demolir parede cozinha/closet — somente após E03', '1,45 m'),
    ('D08', 'Retirar pisos do MainFloor', '60,30 m²'),
    ('D03', 'Retirar piso, base e rebaixo do banheiro até a laje', '3,80 m²'),
    ('P01', 'Parede do jantar: retirar espelho e revestimento', '1,95 m'),
    ('P02', 'Parede sob a escada: retirar revestimento', 'a confirmar'),
    ('P04', 'Demais paredes com revestimento retirado', 'mapear em obra'),
    ('P03', 'Laje: restaurar, descascar, limpar e preparar', '60,30 m²'),
    ('P06', 'Regularizar e lixar todo o contrapiso — plano e nivelado', '60,30 m²'),
    ('P05', 'Nivelar o banheiro na cota do piso da casa', 'cota única'),
    ('R01', 'Reconstruir drywall sala/quarto com vão de porta 1,00 × 2,29 m', '4,08 m + 1 vão'),
    ('R02', 'Construir parede de fechamento do fundo do box', '1,63 m'),
    ('R03', 'Parede nova cozinha/closet, na face sul do banheiro até a oeste', '2,17 m'),
    ('K01', 'Vidro do box — MANTER e proteger', '1 peça'),
]

fo.SEQ_DEMO = [
    ('1', ['Ensaios antes de qualquer demolição — E01, E02 e E03.',
           'Resultado por escrito. Sem laudo do E03, D09 e D10 não saem.'], True),
    ('2', ['Proteção e canteiro.',
           'Proteger K01, esquadrias, prumadas e caixilhos; entulho e horário do condomínio.'], False),
    ('3', ['Desmontagem — M01 e D05.'], False),
    ('4', ['Forro — D07, 100%.'], False),
    ('5', ['Vedações — D01, D02, D06, D04, D09 e D10.',
           'Abrir D10 com cautela: confirmar hidráulica ou gás embutido no trecho.'], False),
    ('6', ['Pisos e base — D08 e D03. Banheiro desce até a laje.'], False),
    ('7', ['Revestimentos de parede — P01, P02 e P04. Laje — P03.'], False),
    ('8', ['Marcação da parede nova R03 antes de levantar.',
           'Alinhada à face sul do banheiro, em esquadro com a parede oeste.'], True),
    ('9', ['Reconstruções — R01, R02 e R03.',
           'R01 fecha somente após a infraestrutura elétrica embutida.'], True),
    ('10', ['Contrapiso e nível — P06 e P05.',
            'Entregar plano, nivelado, seco e limpo, em cota única, para liberar o piso.'], True),
]


def folha_demolicao_alt():
    usar(ORIG_WALLS, ORIG_ROOMS)
    alvos_orig = p02.ALVOS
    p02.ALVOS = alvos_orig + ALVOS_ALT_EXTRA
    alt_orig = fo.tabela

    def tabela_compacta(d, x, y, w, cols, linhas, titulo=None, alt=None):
        return alt_orig(d, x, y, w, cols, linhas, titulo=titulo, alt=16.2)
    fo.tabela = tabela_compacta
    try:
        d = fo.folha_demolicao()
    finally:
        p02.ALVOS = alvos_orig
        fo.tabela = alt_orig
    # a planta ainda está no plano da FO1 (70, 156, 63): marca a parede que sai
    # e a posição da nova sobre o estado existente
    for r in (WALL_REMOVER_1, WALL_REMOVER_2):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.4)
    x, y, w_, h_ = d.R(WALL_NOVA)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.3, dash='4 3')
    return d


# ---------------------------------------------------------------------------
# FO2 — piso: áreas por sistema iguais; só a remontagem do closet muda
# ---------------------------------------------------------------------------
fo.SEQ_PISO = list(fo.SEQ_PISO[:-1]) + [
    ('7', ['Liberação para marcenaria.',
           'Marcenaria do closet somente após a cura — e com módulos novos: o closet',
           'fica 0,45 m mais raso nesta proposta, os módulos antigos não voltam iguais.'], False),
]


def folha_piso_alt():
    usar(ALT_WALLS, ALT_ROOMS)
    return fo.folha_piso()


# ---------------------------------------------------------------------------
# FO3 — elétrica: sem mudança de ponto
# ---------------------------------------------------------------------------
def folha_eletrica_alt():
    usar(ALT_WALLS, ALT_ROOMS)
    return fo.folha_eletrica()


# ---------------------------------------------------------------------------
# FO4 — iluminação: fluxo alvo de cozinha e closet recalculado
# ---------------------------------------------------------------------------
fo.TAB_LUX = [
    ('Sala',     '150 lux', '7.188 lm', '2.700 K'),
    ('Quarto',   '150 lux', '4.188 lm', '2.700 K'),
    ('Cozinha',  '300 lux', '6.138 lm', '3.000 K'),
    ('Jantar',   '150 lux', '1.844 lm', '2.700 K'),
    ('Closet',   '200 lux', '1.825 lm', '3.000 K'),
    ('Banheiro', '200 lux', '1.583 lm', '3.000 K'),
]


def folha_iluminacao_alt():
    usar(ALT_WALLS, ALT_ROOMS)
    return fo.folha_iluminacao()


# ---------------------------------------------------------------------------
# FO5 — ar: cargas por zona e vazão da coifa recalculadas
# ---------------------------------------------------------------------------
fo.TAB_AR_FO = [
    ('AC01', 'Evaporadora — social + cozinha (38,72 m²)', '1 unidade'),
    ('AC02', 'Evaporadora — quarto + closet (17,78 m²)', '1 unidade'),
] + list(fo.TAB_AR_FO[2:])

fo.TAB_BTU = [
    ('Social + cozinha',   '38,72 m²', '23.232 BTU/h', '30.976 BTU/h'),
    ('Quarto + closet',    '17,78 m²', '10.668 BTU/h', '14.224 BTU/h'),
    ('Total sem banheiro', '56,50 m²', '33.900 BTU/h', '45.200 BTU/h'),
]

fo.TAB_VAZAO = [
    ('EX01', 'Banheiro — 3,80 m² × 2,40 m × 10 trocas/h', '91,2 m³/h'),
    ('CF01', 'Cozinha — 9,82 m² × 2,62 m × 12 trocas/h', '308,7 m³/h'),
]

fo.SEQ_AR = [fo.SEQ_AR[0]] + [
    ('2', ['Seleção pela coluna base sol — 30.976 e 14.224 BTU/h, somente Electrolux.',
           'A fachada envidraçada é noroeste e pega o sol da tarde. Marca igual não',
           'garante compatibilidade: conferir o par no catálogo antes de comprar.'], True),
] + list(fo.SEQ_AR[2:])


def folha_ar_alt():
    usar(ALT_WALLS, ALT_ROOMS)
    return fo.folha_ar()


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    saidas = []
    for fn, nome, titulo in (
            (folha_demolicao_alt,  'alt-a-fornecedor-01-demolicao',  'FO1: demolição e preparo'),
            (folha_piso_alt,       'alt-a-fornecedor-02-piso',       'FO2: piso'),
            (folha_eletrica_alt,   'alt-a-fornecedor-03-eletrica',   'FO3: elétrica'),
            (folha_iluminacao_alt, 'alt-a-fornecedor-04-iluminacao', 'FO4: iluminação'),
            (folha_ar_alt,         'alt-a-fornecedor-05-ar',         'FO5: ar-condicionado e exaustão')):
        caminho = salvar(fn(), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus 81I — fornecedores, Alternativo A — ' + titulo)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
        saidas.append(caminho)
    usar(ORIG_WALLS, ORIG_ROOMS)
    exportar_pdf_a3(saidas, os.path.join(pasta, 'caderno-fornecedores-alternativo-a-A3.pdf'),
                    'MaxHaus 81I — pacote para fornecedores, Alternativo A (A3)')
    print('ok fornecedores alternativo a: 5 folhas + pacote')
