# -*- coding: utf-8 -*-
"""Prancha 11 — Ar, exaustão e iluminação: base de cálculo.

Refaz a planilha de pré-dimensionamento recebida em 11.09.2026. A conta de
exaustão do banheiro muda: o ambiente mantém forro, logo o volume é calculado
com 2,40 m.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'
PRANCHA = 'Prancha 11 / 12'

TAB_PREM = [
    ('Fator de sombra', '600 BTU/h por m²', 'regra simplificada — não é cálculo térmico'),
    ('Fator de sol', '800 BTU/h por m²', 'fachada envidraçada a noroeste, sol de tarde'),
    ('Pé-direito de estudo', '2,62 m', 'laje aparente, fora do banheiro'),
    ('Altura do banheiro', '2,40 m', 'sob o forro, que permanece'),
    ('Renovações — banheiro', '10 por hora', 'ventilação volumétrica preliminar'),
    ('Renovações — cozinha', '12 por hora', 'hipótese de cozinha isolada'),
    ('Fator de utilização', '0,60', 'iluminação — refletâncias e geometria'),
    ('Fator de manutenção', '0,80', 'iluminação — depreciação e sujidade'),
    ('Pessoas e equipamentos', 'não inventariados', 'entram no cálculo térmico, não nesta base'),
]

TAB_TERM = [
    ('Social + cozinha', '37,80', '22.680', '30.240', 'sala, jantar, cozinha e circulação'),
    ('Quarto + closet', '18,70', '11.220', '14.960', 'zona de dormir'),
    ('Total sem banheiro', '56,50', '33.900', '45.200', 'seleção pela coluna base sol'),
]

TAB_EXA = [
    ('EX01', 'Banheiro', '3,80 × 2,40 = 9,12 m³', '× 10', '91,2 m³/h'),
    ('CF01', 'Cozinha isolada — hipótese', '8,90 × 2,62 = 23,32 m³', '× 12', '279,8 m³/h'),
]

TAB_LUZ = [
    ('Sala',     '23,00', '150 lux', '7.188 lm', '2.700 K', 'leitura e cenas dimerizáveis'),
    ('Quarto',   '13,40', '150 lux', '4.188 lm', '2.700 K', 'cabeceira independente'),
    ('Cozinha',  '8,90',  '300 lux', '5.563 lm', '3.000 K', 'bancada à parte, 500 lux'),
    ('Jantar',   '5,90',  '150 lux', '1.844 lm', '2.700 K', 'pendente sobre a mesa'),
    ('Closet',   '5,30',  '200 lux', '2.208 lm', '3.000 K', 'luz vertical das roupas'),
    ('Banheiro', '3,80',  '200 lux', '1.583 lm', '3.000 K', 'espelho frontal e balizamento'),
]

NOTAS = [
    ['**Correção desde a folha de 11.09: a exaustão do banheiro cai de 99,6 para 91,2 m³/h.',
     'O volume se calcula com 2,40 m, a altura sob o forro que permanece, e não com os 2,62 m',
     'da laje. A cozinha segue em 2,62 m porque lá a laje é o teto acabado.'],
    ['**A regra 600/800 BTU/h por m² não é cálculo térmico.',
     'Ela não conta pessoas, equipamentos, a claraboia, a piscina sobre a sala, a escada aberta',
     'nem a troca entre pavimentos. Serve para dimensionar a conversa com o fornecedor e conferir',
     'se a condensadora existente tem alguma chance de atender. A seleção final pede cálculo.'],
    ['**A escada aberta é a maior incerteza desta base.',
     'Os dois pavimentos trocam ar livremente, então a carga do MainFloor sozinho é otimista.',
     'Dimensionar pela coluna base sol é a margem que resta — e ainda assim pode faltar.'],
    ['**A vazão da cozinha isolada não é seleção de coifa.',
     'A cozinha é integrada à sala; 279,8 m³/h só valeria com ela fechada. Coifa se seleciona por',
     'captura sobre o fogão, com o diâmetro e a altura do manual, e percurso próprio até uma saída',
     'permitida. Banheiro e cozinha não dividem rota.'],
    ['**Fluxo = área × iluminância ÷ (utilização × manutenção).',
     'Com 0,60 e 0,80, o divisor é 0,48. Os alvos em lux são proposta de conforto, não declaração',
     'normativa, e o número de luminárias depende do fluxo útil e da fotometria de cada modelo —',
     'não do lúmen nominal da caixa.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Ar, exaustão e iluminação: base de cálculo',
              'Pré-dimensionamento de estudo. Não define compra, compatibilidade de equipamento, circuitos, cabos, disjuntores nem perfurações.',
              REV, '45.200 BTU/h na base sol',
              'exaustão do banheiro corrigida para 91,2 m³/h')

    cx, cw = MARGIN, 648
    fim = tabela(d, cx, 158, cw,
                 [('Premissa', 0.30, 'start'), ('Valor', 0.24, 'start'),
                  ('Condição', 0.46, 'start')],
                 TAB_PREM, titulo='PREMISSAS — O QUE A CONTA ASSUME', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('Zona térmica', 0.26, 'start'), ('Área m²', 0.13, 'end'),
                  ('Base sombra', 0.16, 'end'), ('Base sol', 0.15, 'end'),
                  ('Atende', 0.30, 'end')],
                 TAB_TERM, titulo='CARGA TÉRMICA — SELECIONAR PELA BASE SOL', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('ID', 0.09, 'start'), ('Ambiente', 0.28, 'start'),
                  ('Volume', 0.27, 'start'), ('Trocas', 0.13, 'end'),
                  ('Vazão', 0.23, 'end')],
                 TAB_EXA, titulo='EXAUSTÃO — VAZÃO A VALIDAR COM PERDA DE CARGA', alt=19)
    tabela(d, cx, fim + 38, cw,
           [('Ambiente', 0.20, 'start'), ('Área m²', 0.12, 'end'),
            ('Alvo', 0.13, 'end'), ('Fluxo', 0.14, 'end'),
            ('CCT', 0.13, 'end'), ('Camada adicional', 0.28, 'end')],
           TAB_LUZ, titulo='ILUMINAÇÃO — ALVO POR AMBIENTE', alt=19)

    d.line(724, 140, 724, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 756, W - MARGIN - 756
    paragrafos(d, cx2, 168, cw2, NOTAS, size=8.5, lh=12.4, gap=8.0)

    rodape(d,
           'Regra 600/800 BTU/h por m² conforme orientação simplificada de fabricante; renovações por hora conforme prática corrente de ventilação. Nenhuma das duas substitui cálculo.',
           'Alvos de iluminância são proposta de projeto. Confirmar curva pressão × vazão do duto e fotometria da luminária antes de comprar.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-11-ar-luz')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-11-ar-luz-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 11: ar, exaustão e iluminação')
    exportar_png(caminho, os.path.join(pasta, 'prancha-11-ar-luz.png'))
    print('ok prancha 11')
