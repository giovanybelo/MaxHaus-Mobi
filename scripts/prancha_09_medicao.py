# -*- coding: utf-8 -*-
"""Prancha 09 — Base de medição e decisões.

Refaz, na identidade do caderno, a folha de base de medição recebida em
11.09.2026. A geometria continua a do scan; o que muda é a altura de
referência, agora separada em laje (2,62) e forro do banheiro (2,42).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'
PRANCHA = 'Prancha 09 / 12'

TAB_AMB = [
    ('Sala',     '23,00', '29,80', '60,26'),
    ('Quarto',   '13,40', '30,30', '35,11'),
    ('Cozinha',  '8,90',  '23,30', '23,32'),
    ('Jantar',   '5,90',  '15,20', '15,46'),
    ('Closet',   '5,30',  '14,90', '13,89'),
    ('Banheiro', '3,80',  '16,70', '9,20'),
    ('Soma por ambiente', '60,30', '130,20', '157,24'),
]

TAB_CONF = [
    ('Área útil', '60,30 m²', '60,2 m² no relatório', 'arredondamento por ambiente'),
    ('Área de parede', '130,20 m²', '130,4 m² no relatório', 'mesma diferença, mantida'),
    ('Malha do OBJ', '63,13 m²', 'inclui área sob paredes', 'geometria, não área útil'),
    ('Pé-direito na laje', '2,62 m', 'medição do cliente 12.09', 'vale em todo o pavimento'),
    ('Altura sob o forro', '2,42 m', 'só no banheiro', 'o scan lia 2,40 m'),
    ('Plenum do forro', '0,20 m', 'liberado pela D07', 'fora do banheiro'),
]

TAB_DEC = [
    ('Escopo', 'Somente MainFloor', 'o pavimento superior entra como referência de piscina'),
    ('Piso', 'Duas opções vivas', 'A cumaru + monolítico · B monolítico integral'),
    ('Altura', 'Resolvida', '2,62 na laje, 2,42 sob o forro do banheiro'),
    ('Norte', 'Medido', '126°, do scan do pavimento superior'),
    ('Tomadas', 'Permanecem', 'posição existente, sem remanejamento'),
    ('Ar', 'Somente Electrolux', 'condensadora existente a conferir'),
]

NOTAS = [
    ['**Estas quantidades são de estudo, rastreáveis ao scan de 02.09.2026.',
     'Não use a área comercial do duplex para comprar material do MainFloor: ela inclui o',
     'pavimento superior, paredes e projeções que não existem nesta obra. A referência é a',
     'coluna de piso útil, 60,30 m².'],
    ['**A diferença entre 60,30 e os 60,2 m² do relatório é arredondamento por ambiente,',
     'e a de 130,20 contra 130,4 m² é a mesma coisa no outro sentido. A planilha conserva a',
     'diferença em vez de forçar o fechamento — é honesto e é pequeno demais para mudar compra.'],
    ['**A malha de piso do modelo OBJ soma 63,13 m² porque mede o plano cheio,',
     'incluindo a área sob as paredes. Serve para a representação geométrica e para o 3D; não',
     'substitui a área útil. Quem comprar piso pela malha compra 2,83 m² a mais.'],
    ['**A altura deixou de ser hipótese.',
     'O scan lia 2,40 m porque mediu sob o forro. A medição de campo de 12.09 fechou 2,62 m da',
     'laje ao piso. As duas convivem: 2,62 m vale no pavimento inteiro depois da D07, e 2,42 m',
     'vale dentro do banheiro, único ambiente que mantém forro. Revestimento, vazão e volume do',
     'banheiro se calculam com 2,42 — usar 2,62 lá dentro superestima em 7%.'],
    ['**O que esta emissão ainda não resolve:',
     'instalação embutida, estrutura, quadro elétrico, drenos e saídas externas não foram',
     'localizados em campo. As plantas vêm de levantamento digital, sem vistoria. O responsável',
     'técnico valida demolição, instalações e impermeabilização com o condomínio e com os',
     'projetos do edifício antes da obra.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Base de medição e decisões',
              'Quantidades de estudo rastreáveis ao scan de 02.09.2026. É esta a base de compra do MainFloor — não a área comercial do duplex.',
              REV, '60,30 m² úteis  ·  130,20 m² de parede',
              '2,62 m na laje  ·  2,42 m sob o forro do banheiro')

    cx, cw = MARGIN, 620
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.34, 'start'), ('Piso útil m²', 0.22, 'end'),
                  ('Parede no scan m²', 0.24, 'end'), ('Volume m³', 0.20, 'end')],
                 TAB_AMB, titulo='ÁREAS POR AMBIENTE — LEVANTAMENTO POR SCAN', alt=20)
    fim = tabela(d, cx, fim + 40, cw,
                 [('Grandeza', 0.28, 'start'), ('Adotado', 0.18, 'end'),
                  ('Origem', 0.30, 'end'), ('Condição', 0.24, 'end')],
                 TAB_CONF, titulo='CONFERÊNCIA DE BASES — O QUE ENTRA NA CONTA', alt=20)
    fim = tabela(d, cx, fim + 40, cw,
                 [('Tema', 0.20, 'start'), ('Estado', 0.24, 'start'),
                  ('Leitura', 0.56, 'start')],
                 TAB_DEC, titulo='DECISÕES FECHADAS ATÉ A REV. M', alt=20)

    d.line(700, 140, 700, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 732, W - MARGIN - 732
    paragrafos(d, cx2, 168, cw2, NOTAS, size=8.6, lh=12.6, gap=8.0)

    rodape(d,
           'Volume por ambiente calculado com 2,62 m, exceto o banheiro, com 2,42 m sob o forro. Área de parede conforme o relatório do scan, sem desconto de vão.',
           'Estudo preliminar sobre levantamento digital, sem vistoria. Conferir em campo antes de mobilizar equipe, cortar material ou fechar medição.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-09-medicao')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-09-medicao-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 09: base de medição e decisões')
    exportar_png(caminho, os.path.join(pasta, 'prancha-09-medicao.png'))
    print('ok prancha 09')
