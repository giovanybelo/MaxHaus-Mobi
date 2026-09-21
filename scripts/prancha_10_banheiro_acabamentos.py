# -*- coding: utf-8 -*-
"""Prancha 10 — Banheiro: louças, metais e revestimentos.

Refaz a folha de quantitativos do banheiro recebida em 11.09.2026, com a
correção que muda o resultado: o banheiro mantém forro, então o revestimento
sobe até 2,42 m e não até 2,62 m.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'
PRANCHA = 'Prancha 10 / 12'

H_REV = 2.42          # altura de revestimento: até o forro
LARG_BOX, PROF_BOX = 1.432, 0.930
PERIM, PISO = 8.139, 3.80
RUN_BOX = LARG_BOX + 2 * PROF_BOX
RUN_OUT = PERIM - RUN_BOX
VAO_PORTA = 0.80 * 2.00

TAB_PREM = [
    ('Perímetro interno', '8,14 m', 'faces com revestimento retirado', 'scan · confere com 8,10 do CSV'),
    ('Altura de revestimento', '2,42 m', 'até o forro, que permanece', 'CORRIGIDO — não 2,62'),
    ('Largura do box', '1,43 m', 'toda a largura do banheiro', 'scan · 1,40 arredondado no CSV'),
    ('Profundidade do box', '0,93 m', 'do vidro K01 à parede R02', 'scan · 0,90 arredondado no CSV'),
    ('Paredes revestidas do box', '3', 'fundo R02 e duas laterais', 'a frente é o vidro K01'),
    ('Vão da porta', '0,80 × 2,00 m', 'descontado das paredes', 'modelo lia 0,81 × 2,03 — conferir'),
    ('Piso do banheiro', '3,80 m²', 'medido 3,78; tabelas em 3,80', 'diferença mantida'),
    ('Perda de corte', '10%', 'fração sobre o líquido', 'sem paginação definida'),
    ('Nichos e retornos', '0,00 m²', 'nenhum cotado até aqui', 'somar quando definidos'),
]

TAB_SUP = [
    ('Piso do box', '1,43 × 0,93', '1,33', '0,13', '1,46'),
    ('Piso fora do box', '3,80 − 1,33', '2,47', '0,25', '2,72'),
    ('Paredes do box', '(1,43 + 2 × 0,93) × 2,42', '7,97', '0,80', '8,77'),
    ('Outras paredes', '4,85 × 2,42 − 1,60', '10,13', '1,01', '11,14'),
    ('Total', 'pisos + todas as paredes', '21,90', '2,19', '24,09'),
]

TAB_ANTES = [
    ('Total anterior', '23,38 m²', '25,72 m²', 'revestia até 2,62 m'),
    ('Total corrigido', '21,90 m²', '24,09 m²', 'reveste até 2,42 m'),
    ('Diferença', '−1,48 m²', '−1,63 m²', '6,3% a menos de material'),
]

TAB_LOUCA = [
    ('Bacia sanitária', '1 un.', 'Substituir / definir', 'Saída, eixo e distância da parede'),
    ('Cuba / lavatório', '1 un.', 'Definir', 'Recorte, bancada e sifão compatíveis'),
    ('Misturador / torneira', '1 un.', 'Definir', 'Pressão e água quente não levantadas'),
    ('Chuveiro', '1 conj.', 'Definir', 'Vazão, pressão, aquecimento e comando'),
    ('Registros de isolamento', 'a levantar', 'Levantar', 'Identificar os existentes e a alimentação'),
    ('Ralo linear do box', '1 un.', 'Verificar', 'Não deslocar sem conferir laje e esgoto'),
    ('Box de vidro — K01', '1 conj.', 'Manter e proteger', 'Medir vão só após os revestimentos'),
    ('Ducha higiênica', 'opcional', 'Não escolhida', 'Fora do total de compra'),
]

NOTAS = [
    ['**A correção que muda a compra: o banheiro é o único ambiente que mantém forro.',
     'A altura livre lá dentro é 2,42 m, não os 2,62 m da laje. Revestir até 2,62 m mede parede',
     'que não existe — acima do forro. O total cai de 23,38 para 21,90 m² líquidos, e de 25,72',
     'para 24,09 m² com a perda de 10%.'],
    ['**O box é uma parcela do banheiro, não um adicional.',
     'Suas três paredes revestidas ocupam 3,29 m dos 8,14 m de perímetro; as outras paredes são',
     'os 4,85 m restantes. Somar box e perímetro cheio contaria a mesma parede duas vezes.'],
    ['**O total é acabamento futuro, não área a demolir.',
     'A demolição do banheiro mede 3,80 m² de piso mais as paredes revestidas existentes, que só',
     'se conhecem em campo. Os 21,90 m² acima são o que volta, não o que sai.'],
    ['**Impermeabilização é sistema à parte do revestimento.',
     'Rodapé virado, ralo, cantos, passagens e ensaio de estanqueidade entram antes de assentar',
     'qualquer peça, e a quantidade de produto depende do sistema escolhido. Não está embutida',
     'nos m² desta folha.'],
    ['**O que ainda não está aqui:',
     'nichos, retornos, peças especiais, soleira, recorte do ralo, juntas e paginação. Arredondar',
     'por caixa só depois da paginação do produto escolhido. A medida do vidro do box se tira',
     'com os revestimentos já assentados, nunca antes.'],
]


def diagrama_box(d, x, y, esc=92.0):
    """Esquema dimensional do banheiro, com o box destacado."""
    d.txt(x, y - 12, 'ESQUEMA DIMENSIONAL — PLANTA', 8.0, INK_SOFT, 'bold', ls=1.2)
    w = LARG_BOX * esc
    h_seca = (2.638 - PROF_BOX) * esc
    h_box = PROF_BOX * esc
    # área seca
    d.rect(x, y, w, h_seca, fill=BG, stroke=K, sw=1.6)
    d.txt(x + w / 2.0, y + h_seca / 2.0 - 4, 'ÁREA SECA', 7.4, INK, 'bold', 'middle', ls=0.6)
    d.txt(x + w / 2.0, y + h_seca / 2.0 + 8, '2,47 m²', 7.0, INK_SOFT, 'normal', 'middle')
    # box
    d.rect(x, y + h_seca, w, h_box, fill=WET, stroke=K, sw=1.6)
    d.txt(x + w / 2.0, y + h_seca + h_box / 2.0 - 4, 'BOX  1,43 × 0,93', 7.4, INK,
          'bold', 'middle', ls=0.4)
    d.txt(x + w / 2.0, y + h_seca + h_box / 2.0 + 8, '1,33 m²', 7.0, INK_SOFT, 'normal', 'middle')
    # vidro K01 na divisa
    d.line(x, y + h_seca, x + w, y + h_seca, CIANO, 4.0)
    d.txt(x + w + 8, y + h_seca + 3, 'K01', 6.8, K, 'bold', 'start', ls=0.3)
    # parede nova R02 no fundo
    d.line(x, y + h_seca + h_box, x + w, y + h_seca + h_box, DEMO, 3.0)
    d.txt(x + w + 8, y + h_seca + h_box + 3, 'R02', 6.8, DEMO, 'bold', 'start', ls=0.3)
    # cotas
    d.txt(x + w / 2.0, y + h_seca + h_box + 22, '1,43 m', 7.2, DIM_TXT, 'normal', 'middle')
    d.txt(x - 10, y + (h_seca + h_box) / 2.0, '2,64 m', 7.2, DIM_TXT, 'normal', 'middle', rot=-90.0)
    d.txt(x + w + 40, y + 16, 'altura de', 7.0, INK_SOFT, 'normal', 'start')
    d.txt(x + w + 40, y + 27, 'revestimento', 7.0, INK_SOFT, 'normal', 'start')
    d.txt(x + w + 40, y + 40, '2,42 m', 9.0, DEMO, 'bold', 'start', ls=0.4)
    d.txt(x + w + 40, y + 52, 'até o forro', 6.8, INK_SOFT, 'normal', 'start')
    return y + h_seca + h_box + 34


def construir():
    d = folha_nova()
    cabecalho(d, 'Banheiro: louças, metais e revestimentos',
              'Quantitativo de acabamento sobre o layout existente. Pontos hidráulicos mantidos como hipótese até confirmar água, esgoto, aquecimento e interferência na laje.',
              REV, '21,90 m² líquidos  ·  24,09 m² com 10%',
              'revestimento até 2,42 m — o forro fica')

    cx, cw = MARGIN, 640
    fim = tabela(d, cx, 158, cw,
                 [('Premissa', 0.28, 'start'), ('Valor', 0.18, 'start'),
                  ('O que é', 0.28, 'start'), ('Fonte / condição', 0.26, 'end')],
                 TAB_PREM, titulo='PREMISSAS DO CÁLCULO', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('Superfície', 0.24, 'start'), ('Conta', 0.30, 'start'),
                  ('Líquido m²', 0.16, 'end'), ('Perda m²', 0.14, 'end'),
                  ('Compra m²', 0.16, 'end')],
                 TAB_SUP, titulo='SUPERFÍCIES — SEM DUPLA CONTAGEM', alt=19)
    fim = tabela(d, cx, fim + 38, cw,
                 [('Emissão', 0.28, 'start'), ('Líquido', 0.20, 'end'),
                  ('Com 10%', 0.20, 'end'), ('Por quê', 0.32, 'end')],
                 TAB_ANTES, titulo='O QUE MUDOU DESDE A FOLHA DE 11.09', alt=19)

    d.line(716, 140, 716, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 748, W - MARGIN - 748
    fim2 = tabela(d, cx2, 158, cw2,
                  [('Louça / metal', 0.30, 'start'), ('Quantidade', 0.16, 'start'),
                   ('Tratamento', 0.22, 'start'), ('Verificar antes de selecionar', 0.32, 'end')],
                  TAB_LOUCA, titulo='LOUÇAS E METAIS', alt=19)
    fim2 = paragrafos(d, cx2, fim2 + 30, cw2, NOTAS, size=8.3, lh=11.9, gap=6.2)

    diagrama_box(d, cx2 + 150, fim2 + 30, esc=90.0)

    rodape(d,
           'Geometria interna do scan de 02.09.2026 nas faces de revestimento retirado: 1,432 × 2,638 m. O CSV arredonda box e perímetro; esta folha usa o medido e mostra os dois.',
           'Quantidade de acabamento, não de demolição. Impermeabilização, soleira, juntas e paginação são serviços à parte. Arredondar por caixa só após a paginação do produto.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-10-banheiro-acabamentos')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-10-banheiro-acabamentos-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 10: banheiro, louças, metais e revestimentos')
    exportar_png(caminho, os.path.join(pasta, 'prancha-10-banheiro-acabamentos.png'))
    print('ok prancha 10')
