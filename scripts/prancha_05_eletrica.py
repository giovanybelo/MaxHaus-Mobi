# -*- coding: utf-8 -*-
"""Prancha 05 — Tomadas, comandos e quadro (REV. C)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. F'
PRANCHA = 'Prancha 05 / 08'

# --- pontos existentes marcados pelo cliente (metros) -----------------------
TOMADAS_EXIST = [
    ('T01', 7.62, 2.46), ('T02', 7.62, 4.51), ('T03', 7.62, 5.90),
    ('T04', 7.55, 9.15), ('T05', 2.02, 4.75), ('T06', 2.02, 5.25),
    ('T07', 2.45, 7.62), ('T08', 0.22, 5.70), ('T09', 0.22, 6.05),
]
# --- reservas novas ---------------------------------------------------------
TOMADAS_NOVAS = [
    ('T10', 0.60, 3.95, 'geladeira'),
    ('T11', 0.30, 4.75, 'bancada'),
    ('T12', 0.30, 6.55, 'forno / lava-louças'),
    ('T13', 5.05, 9.20, 'cabeceira'),
    ('T14', 6.95, 9.20, 'cabeceira'),
    ('T15', 3.40, 9.20, 'office'),
    ('T16', 6.60, 0.30, 'jantar'),
    ('T17', 3.45, 4.78, 'lavatório'),
]
# --- comandos ---------------------------------------------------------------
COMANDOS = [
    ('S01', 0.90, 3.05), ('S02', 4.17, 2.30), ('S03', 2.35, 4.60),
    ('S04', 3.92, 4.88), ('S05', 4.05, 7.35),
    ('S06', 5.05, 9.05), ('S07', 6.95, 9.05),
    ('S08', 3.92, 4.62),      # luz da sala, na quina do box voltada para a escada
]
# comandos com o id ao lado, para não empilhar rótulo sobre símbolo
ROTULO_LESTE = {'S04', 'S08'}

QUADRO = (1.35, 2.35)

LINHAS = [
    ('Quadro elétrico', 'junto à porta de entrada, na extensão da cozinha',
     'tensão, fases, demanda, proteção e espaços'),
    ('Tomadas existentes', '9 posições levantadas pelo cliente', 'confirmar altura, caixa e circuito'),
    ('Tomadas novas', '8 reservas — T10 a T17', 'não é número normativo nem total final'),
    ('Comandos', '8 posições — S01 a S08, duas na cabeceira', 'lado da porta, marcenaria e cenas'),
    ('Cozinha', 'geladeira, forno, lava-louças, coifa e bancada', 'pontos dedicados, circuito exclusivo'),
    ('Ar-condicionado', 'alimentação conforme manual da unidade', 'quem alimenta varia com o sistema'),
    ('Banheiro', 'ponto junto ao lavatório a validar', 'volumes de proteção, DR e cargas'),
]

NOTAS = [
    ['**O quadro de energia foi localizado pelo cliente: fica junto à porta de entrada,',
     'no início da extensão da cozinha. Confirmar espaço livre, altura e a circulação da porta',
     'antes de fixar. Todo o resto do traçado sai dele.'],
    ['**Sem forro, os trajetos ficam aparentes.',
     'A distribuição no teto passa a ser perfilado ou eletrocalha pintada, acompanhando os trilhos',
     'de luz da Prancha 04; as descidas para tomadas e comandos correm embutidas na parede.',
     'Isso vira desenho: definir caminhos e separações antes de medir eletrodutos e cabos.'],
    ['**Alturas de intenção, sempre conferidas com mobiliário e acabamento:',
     'tomadas gerais 0,30 m; comandos 1,10 m; pontos de bancada em torno de 1,15 m.',
     'As marcações não autorizam instalação em parede sem localizar estrutura e tubulações.'],
    ['**Os pontos T01 a T09 são os existentes que você marcou em planta.',
     'Estão desenhados na posição aproximada do levantamento: servem para decidir o que se aproveita',
     'e o que se remaneja, não para medir. T10 a T17 são reservas novas do estudo.'],
    ['**Comandos revisados nesta folha.',
     'O comando que caía dentro do box saiu; o que ficava junto à porta do quarto passou a S05,',
     'agora ao lado da porta nova da drywall. S06 e S07 são os dois novos comandos da cabeceira,',
     'um de cada lado da cama, em paralelo com as luminárias P02 e P03 da Prancha 04.'],
    ['**O que cada comando aciona — leitura de folha, não diagrama de circuito:',
     'S01 entrada e cozinha (TR4 e coifa, junto ao quadro) · S02 jantar (TR1 e P01) · S03 arandelas',
     'do espelho, junto à bancada · S04 banheiro, na quina do box · S05 quarto, ao lado da porta',
     'nova (TR5, P02 e P03) · S06 e S07 cabeceira, em paralelo com o S05 · S08 sala (TR2 e TR3).'],
    ['**S08 é o novo comando da luz da sala.',
     'Fica na quina do box voltada para a escada, encostado no S04 do banheiro: é o primeiro',
     'anteparo de quem entra na sala vindo da escada ou da cozinha. Os dois ocupam a faixa de',
     'parede de 0,45 m entre a quina e o batente — cabe, mas é a folga exata de duas placas 4×2:',
     'confirmar em obra antes de fechar a caixa. Se a sala for acender também pelo outro extremo,',
     'S08 precisa de paralelo junto à porta nova da drywall, em conjunto com o S05.'],
    ['**Circuitos, seções, disjuntores, aterramento, DR, demanda e proteção contra surtos',
     'ficam a cargo do projeto elétrico após o levantamento. Não usar estas reservas como projeto',
     'para o eletricista executar.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Tomadas, comandos e quadro',
              'Reservas de localização, sem circuitos executivos. Posições existentes conforme marcação do cliente sobre o estudo anterior.',
              REV, 'quadro junto à porta de entrada',
              'trajetos aparentes: não há forro')

    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, '#edeae3')
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_horizontal(d, PORTA_NOVA, hinge='w', swing='s')
    escada(d)
    for k, lx, ly in (('jantar', 520.0, 145.0), ('sala', 500.0, 300.0),
                      ('cozinha', 310.0, 350.0), ('closet', 300.0, 505.0),
                      ('quarto', 500.0, 480.0), ('banheiro', 380.6, 428.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=False, size=8.4)

    # tomadas existentes
    for (ident, xm, ym) in TOMADAS_EXIST:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.6, fill=BG, stroke=EXIST, sw=1.5)
        d.circle(cx, cy, 1.8, fill=EXIST)
        d.txt(cx, cy - 9, ident, 6.6, EXIST, 'bold', 'middle', ls=0.3)

    # tomadas novas
    for (ident, xm, ym, uso) in TOMADAS_NOVAS:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.6, fill='#e6f0f6', stroke=NEW, sw=1.5)
        d.circle(cx, cy, 1.8, fill=NEW)
        d.txt(cx, cy - 9, ident, 6.6, NEW, 'bold', 'middle', ls=0.3)

    # comandos
    for (ident, xm, ym) in COMANDOS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 5.2, cy - 5.2, 10.4, 10.4, fill=BG, stroke=INK, sw=1.3)
        d.line(cx - 2.4, cy + 2.4, cx + 2.4, cy - 2.4, INK, 1.2)
        if ident in ROTULO_LESTE:
            d.txt(cx + 8.5, cy + 2.4, ident, 6.6, INK, 'bold', 'start', ls=0.3)
        else:
            d.txt(cx, cy - 9, ident, 6.6, INK, 'bold', 'middle', ls=0.3)

    # quadro de energia
    cx, cy = d.PM(*QUADRO)
    d.rect(cx - 10, cy - 7, 20, 14, fill='#fdeceb', stroke=DEMO, sw=1.8)
    for i in range(3):
        d.line(cx - 6 + i * 6, cy - 4, cx - 6 + i * 6, cy + 4, DEMO, 1.1)
    d.txt(cx, cy + 20, 'QUADRO DE ENERGIA', 7.6, DEMO, 'bold', 'middle', ls=0.4)
    d.txt(cx, cy + 30, 'posição indicada pelo cliente', 7.0, INK_SOFT, 'normal', 'middle')

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dotf', EXIST, 'Tomada existente'),
                ('dotf', NEW, 'Tomada nova (reserva)'),
                ('fill', '#f0eee8', 'Comando / interruptor'),
                ('fill', '#fdeceb', 'Quadro de energia')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('Grupo', 0.24, 'start'), ('Reservas', 0.40, 'start'),
                  ('Revisão necessária', 0.36, 'end')],
                 LINHAS, titulo='RESERVAS DE INFRAESTRUTURA ELÉTRICA')
    paragrafos(d, cx2, fim + 30, cw, NOTAS, size=8.4, lh=12.4, gap=8.5)

    rodape(d,
           'Posições aproximadas sobre o modelo do scan. Quadro e trajetos existentes não estão identificados no levantamento: confirmar em campo antes de qualquer medição.',
           'Este desenho é reserva de localização — não substitui projeto elétrico com memorial, diagrama unifilar e dimensionamento.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-05-eletrica')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-05-eletrica-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 05: tomadas, comandos e quadro')
    exportar_png(caminho, os.path.join(pasta, 'prancha-05-eletrica.png'))
    print('ok prancha 05')
