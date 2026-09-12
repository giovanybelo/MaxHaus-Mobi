# -*- coding: utf-8 -*-
"""Pacote para fornecedores — três mapas independentes, A3 deitado.

FO1  Demolição e preparo
FO2  Piso
FO3  Elétrica

Cada folha é autossuficiente e sai como PDF próprio: especificação de tarefa,
quantidade e sequência de execução. Sem justificativa de projeto, sem
comparação de materiais e sem observação dirigida ao cliente.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

EMISSAO = 'EMISSÃO 01'
DATA = '12.09.2026'
ORIGEM = 'extraído do caderno de estudo REV. L'

# ---------------------------------------------------------------------------
# FASES GERAIS DA OBRA — a mesma régua nas três folhas
# ---------------------------------------------------------------------------
FASES = ['Ensaios e proteção', 'Demolição', 'Preparo de superfícies',
         'Infraestrutura', 'Reconstruções', 'Piso', 'Pintura',
         'Marcenaria e luminárias']


def regua_fases(d, x, y, largura, ativas):
    d.txt(x, y - 10, 'SEQUÊNCIA GERAL DA OBRA', 8.0, INK_SOFT, 'bold', ls=1.2)
    n = len(FASES)
    w = largura / float(n)
    for i, nome in enumerate(FASES):
        xx = x + i * w
        ativo = (i + 1) in ativas
        d.rect(xx, y, w - 3, 26, fill=AMARELO if ativo else K04,
               stroke=K, sw=1.0 if ativo else 0.5)
        d.txt(xx + 6, y + 11, str(i + 1), 8.4, K, 'bold' if ativo else 'normal')
        palavras = nome.split()
        if len(palavras) > 2:
            d.txt(xx + 16, y + 10, ' '.join(palavras[:2]), 6.8, K if ativo else INK_SOFT,
                  'bold' if ativo else 'normal')
            d.txt(xx + 16, y + 19, ' '.join(palavras[2:]), 6.8, K if ativo else INK_SOFT,
                  'bold' if ativo else 'normal')
        else:
            d.txt(xx + 16, y + 15, nome, 6.8, K if ativo else INK_SOFT,
                  'bold' if ativo else 'normal')


def sequencia(d, x, y, largura, titulo, passos, size=8.5, lh=12.6):
    d.txt(x, y, titulo, 8.0, INK_SOFT, 'bold', ls=1.2)
    yy = y + 18
    for i, (num, texto, gate) in enumerate(passos):
        d.circle(x + 7, yy - 3, 7.5, fill=AMARELO if gate else BRANCO, stroke=K, sw=1.0)
        d.txt(x + 7, yy, num, 7.4, K, 'bold', 'middle')
        linhas = texto if isinstance(texto, list) else [texto]
        for j, ln in enumerate(linhas):
            d.txt(x + 22, yy + j * lh, ln, size,
                  K if (j == 0) else INK_SOFT, 'bold' if (j == 0 and gate) else 'normal')
        yy += lh * len(linhas) + 6.0
    return yy


def rodape_fo(d, folha, disciplina):
    d.line(MARGIN, 930, W - MARGIN, 930, RULE, 1.0)
    d.txt(MARGIN, 948,
          'Quantidades preliminares sobre levantamento por scan de 02.09.2026. Conferir medidas e alvos em campo antes de mobilizar equipe, cortar material ou fechar medição.',
          8.3, INK_SOFT)
    d.txt(MARGIN, 961,
          'Durações e prazos não estão definidos: preencher no cronograma da contratada. Alterações de escopo somente por escrito.',
          8.3, INK_SOFT)
    d.txt(MARGIN, 978, 'MAXHAUS 81I  ·  JOÃO BALDINATO 109  ·  %s  ·  %s' % (disciplina.upper(), DATA),
          9.0, RED, 'bold', ls=0.5)
    d.txt(W - MARGIN, 978, '%s   ·   %s' % (folha, EMISSAO), 9.0, INK_SOFT, 'normal', 'end')


def cabeca_fo(d, titulo, disciplina, chamada):
    d.txt(MARGIN, 42, 'MAXHAUS 81I  ·  PACOTE PARA FORNECEDORES', 10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(MARGIN, 78, titulo, 27.0, INK, 'bold')
    d.txt(MARGIN, 99, chamada, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, EMISSAO, 10.0, RED, 'bold', 'end', ls=0.8)
    d.txt(W - MARGIN, 78, disciplina, 10.5, INK, 'bold', 'end')
    d.txt(W - MARGIN, 99, ORIGEM, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)


# ---------------------------------------------------------------------------
# FO1 — DEMOLIÇÃO E PREPARO
# ---------------------------------------------------------------------------
TAB_DEMO = [
    ('E01', 'Ensaio de estanqueidade (pressão) na hidráulica', '1 ensaio'),
    ('E02', 'Medição de resistência de isolamento na elétrica', '1 ensaio'),
    ('M01', 'Desmontar closet, etiquetar módulos e ferragens, acondicionar', '1 conjunto'),
    ('D05', 'Retirar canto alemão do jantar', '1 conjunto'),
    ('D07', 'Retirar forro — 100%', '60,30 m²'),
    ('D01', 'Demolir drywall entre sala e quarto', '4,08 m'),
    ('D02', 'Demolir fechamento e base do box do banheiro', '1 conjunto'),
    ('D06', 'Demolir pano de vidro chão-teto do fundo do box', '1,63 m'),
    ('D04', 'Demolir parede atrás do espelho e da bancada do banheiro', '2,64 m a conferir'),
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
    ('K01', 'Vidro do box — MANTER e proteger', '1 peça'),
]

SEQ_DEMO = [
    ('1', ['Ensaios antes de qualquer demolição — E01 e E02.',
           'Resultado por escrito antes de abrir parede ou piso.'], True),
    ('2', ['Proteção e canteiro.',
           'Proteger K01, esquadrias, prumadas e caixilhos. Isolar acessos e prever',
           'remoção de entulho e horário de condomínio.'], False),
    ('3', ['Desmontagem — M01 e D05.',
           'Closet etiquetado e acondicionado; canto alemão do jantar.'], False),
    ('4', ['Forro — D07, 100%.',
           'Libera a laje e revela a altura livre real.'], False),
    ('5', ['Vedações — D01, D02, D06 e D04.'], False),
    ('6', ['Pisos e base — D08 e D03.',
           'Banheiro desce até a laje.'], False),
    ('7', ['Revestimentos de parede — P01, P02 e P04.'], False),
    ('8', ['Laje — P03.',
           'Restauro, descascamento e limpeza.'], False),
    ('9', ['Reconstruções — R01 e R02.',
           'R01 fecha somente após a infraestrutura elétrica embutida.'], True),
    ('10', ['Contrapiso e nível — P06 e P05.',
            'Última etapa desta disciplina. Entregar plano, nivelado, seco e limpo,',
            'em cota única, para liberar o piso.'], True),
]


def folha_demolicao():
    d = folha_nova()
    cabeca_fo(d, 'Demolição e preparo', 'FO1 — DEMOLIÇÃO',
              'Escopo de retirada, preparo de superfícies e reconstruções. Planta no estado existente.')

    S = 63.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='existente')
    janelas(d)
    vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    escada(d)
    norte(d, 140, 206, 15, nota=None)

    for r in (DRYWALL_SALA_QUARTO, BOX_WC, BANCADA_WC, CANTO_ALEMAO, VIDRO_BOX):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=DEMO, opacity=0.22)
        d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.1, dash='5 3')
    for r in (PAREDE_ESCADA_JANTAR, PAREDE_SOB_ESCADA):
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=AMARELO, opacity=0.55)
        d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.0, dash='4 3')
    x, y, w_, h_ = d.R(PORTA_NOVA)
    d.rect(x, y - 1.5, w_, h_ + 3, fill='none', stroke=K, sw=1.4, dash='4 3')
    for k in ROOM_ORDER:
        pp = [d.P(px, py) for px, py in ROOMS[k]['poly']]
        x0, y0, x1, y1 = bbox(pp)
        yy = y0
        while yy <= y1:
            for (a, b) in spans_at_y(pp, yy):
                d.line(a, yy, b, yy, DEMO, 0.45, opacity=0.10)
            yy += 7.0

    from prancha_02_demolicao import ALVOS, COR_TRACO, COR_MIOLO
    for k, lx, ly in (('jantar', 520.0, 152.0), ('sala', 500.0, 300.0),
                      ('cozinha', 300.0, 360.0), ('closet', 300.0, 500.0),
                      ('quarto', 520.0, 500.0), ('banheiro', 380.6, 400.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=False, size=8.4)
    for (ident, xp, yp, tipo, dx, dy) in ALVOS:
        cx, cy = d.P(xp, yp)
        cor, miolo = COR_TRACO[tipo], COR_MIOLO[tipo]
        if tipo == 'ensaio':
            d.rect(cx - 5.6, cy - 5.6, 11.2, 11.2, fill=BG, stroke=cor, sw=1.5)
            d.line(cx - 2.6, cy, cx + 2.6, cy, cor, 1.1)
            d.line(cx, cy - 2.6, cx, cy + 2.6, cor, 1.1)
        else:
            d.circle(cx, cy, 6.4, fill=BG, stroke=cor, sw=1.5)
            d.circle(cx, cy, 3.0, fill=miolo, stroke=cor, sw=0.7)
        d.txt(cx + dx, cy + dy, ident, 8.0, cor, 'bold',
              'start' if dx > 0 else 'end', ls=0.4)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dot', DEMO, 'Demolir / retirar'),
                ('fill', AMARELO, 'Preparo de superfície'),
                ('dot', K, 'Reconstruir / manter'),
                ('fill', CIANO, 'Desmontar e remontar'),
                ('fill', BRANCO, 'Ensaio de verificação')],
            70, 156 + BUILDING_H * S + 62, largura=600)
    regua_fases(d, 70, 862, 600, (1, 2, 3, 5))

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('ID', 0.07, 'start'), ('Tarefa', 0.71, 'start'),
                  ('Quantidade', 0.22, 'end')],
                 TAB_DEMO, titulo='ESCOPO — TAREFA E QUANTIDADE', alt=19)
    sequencia(d, cx, fim + 34, cw, 'ORDEM DE EXECUÇÃO', SEQ_DEMO)
    rodape_fo(d, 'FOLHA FO1 / 3', 'Demolição')
    return d


# ---------------------------------------------------------------------------
# FO2 — PISO
# ---------------------------------------------------------------------------
TAB_PISO_A = [
    ('A1', 'Cumaru-ferro, piso pronto em réguas — sala, quarto, jantar e corredor', '44,69 m²'),
    ('A2', 'Reserva de 10% sobre A1 — cortes, perdas e reposição', '4,47 m²'),
    ('A3', 'Piso monolítico — zona contínua cozinha + closet', '11,81 m²'),
    ('A4', 'Perfil de transição com junta de movimentação', 'a medir em obra'),
    ('A5', 'Filete curvo de 0,70 m de raio na ponta da zona monolítica', '1 peça'),
]
TAB_PISO_B = [
    ('B1', 'Piso monolítico contínuo — sala, quarto, cozinha, jantar e closet', '56,50 m²'),
    ('B2', 'Juntas de movimentação conforme projeto do fornecedor', 'a definir'),
    ('B3', 'Sem reserva de corte — aplicação moldada in loco', '—'),
]
TAB_PISO_C = [
    ('C1', 'Banheiro: sistema de área molhada, impermeabilização e caimento', '3,80 m²'),
    ('C2', 'Ralo linear e fecho de vidro — contenção sem degrau', '1 conjunto'),
    ('C3', 'Soleira do banheiro: junta de material, sem degrau', '1,00 m'),
    ('C4', 'Soleira da porta de entrada', '1,00 m'),
]

SEQ_PISO = [
    ('1', ['Recebimento do contrapiso.',
           'Conferir por escrito: plano, nivelado, seco e limpo, em cota única (P06).',
           'Medir umidade antes de assentar ou aplicar. Não iniciar sem esse aceite.'], True),
    ('2', ['Marcação da cota de piso acabado.',
           'Cota única para todo o pavimento, amarrada ao nível do hall.'], True),
    ('3', ['Banheiro — C1 e C2.',
           'Impermeabilização, caimento e ralo antes do piso das áreas secas.'], False),
    ('4', ['Aplicação — A ou B, conforme opção contratada.',
           'A: réguas + zona monolítica + perfil de transição (A1 a A5).',
           'B: aplicação monolítica contínua com juntas (B1 a B3).'], False),
    ('5', ['Soleiras — C3 e C4.'], False),
    ('6', ['Cura e proteção.',
           'Proteger a superfície até o fim da obra. Trânsito de obra somente sobre',
           'proteção. Informar o prazo de cura antes do início.'], True),
    ('7', ['Liberação para marcenaria.',
           'Remontagem do closet (M01) e demais marcenarias somente após a cura.'], False),
]


def _planta_piso(d, ox, oy, S, opcao, titulo):
    d.set_plan(ox, oy, S)
    A = (opcao == 'A')
    if A:
        for k in ('sala', 'quarto', 'jantar'):
            piso_reguas(d, ROOMS[k]['poly'], op=0.30, sw=0.4)
        piso_reguas(d, HALL_A_POLY, op=0.30, sw=0.4)
        pm = [d.P(a, b) for a, b in MONO_A_POLY]
        d.path(path_d(pm), fill=MONO)
        d.path(path_d(pm), fill='none', stroke=K, sw=0.9)
    else:
        d.path(path_d([d.P(a, b) for a, b in
                       [(448.4,126.7),(601.7,126.7),(601.7,552.7),(248.0,552.7),
                        (248.0,284.8),(277.8,284.8),(277.8,211.2),(448.4,211.2)]]), fill=MONO)
    pp = [d.P(px, py) for px, py in ROOMS['banheiro']['poly']]
    d.path(path_d(pp), fill=WET)
    d.path(path_d(pp), fill='none', stroke=K, sw=0.9)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    escada(d, rotulo=False)
    if A:
        tracejado(d, [(280.09, 284.8), (313.74, 284.8)] + filete_pts() + [(345.7, 325.65)],
                  dash=4.0, gap=3.0, halo=False)
        tracejado(d, [(345.7, 453.0), (345.7, 513.42)], dash=4.0, gap=3.0, halo=False)
    for k, lx, ly in (('jantar', 520.0, 160.0), ('sala', 500.0, 330.0),
                      ('cozinha', 300.0, 340.0), ('closet', 312.0, 515.0),
                      ('quarto', 520.0, 480.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    for k in ('jantar', 'sala', 'cozinha', 'closet', 'quarto'):
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 7.2, INK, 'bold', 'middle', ls=0.8)
    d.txt(ox, oy - 14, titulo, 11.5, K, 'bold')


def folha_piso():
    d = folha_nova()
    cabeca_fo(d, 'Piso', 'FO2 — PISO',
              'Duas opções para orçamento, na mesma escala. Quantidades por sistema; banheiro em sistema à parte nas duas.')

    S = 40.0
    _planta_piso(d, 70, 200, S, 'A', 'OPÇÃO A  ·  cumaru-ferro + monolítico')
    _planta_piso(d, 414, 200, S, 'B', 'OPÇÃO B  ·  monolítico integral')

    base_y = 200 + BUILDING_H * S + 22
    d.set_plan(70, 200, S)
    escala(d, base_y)
    legenda(d, [('line', K, 'Cumaru-ferro em réguas'), ('fill', MONO, 'Monolítico'),
                ('fill', WET, 'Banheiro — sistema à parte'), ('dash', JOINT, 'Junta / soleira')],
            70, base_y + 36, largura=658)

    fim = tabela(d, 70, 684, 658,
                 [('ID', 0.07, 'start'), ('Tarefa', 0.71, 'start'), ('Quantidade', 0.22, 'end')],
                 TAB_PISO_A, titulo='OPÇÃO A — CUMARU-FERRO COM COZINHA E CLOSET EM MONOLÍTICO',
                 alt=18)
    tabela(d, 70, fim + 42, 658,
           [('ID', 0.07, 'start'), ('Tarefa', 0.71, 'start'), ('Quantidade', 0.22, 'end')],
           TAB_PISO_B, titulo='OPÇÃO B — MONOLÍTICO INTEGRAL', alt=18)

    d.line(760, 140, 760, 916, RULE, 0.8, opacity=0.8)
    cx, cw = 792, W - MARGIN - 792
    fim2 = sequencia(d, cx, 160, cw, 'ORDEM DE EXECUÇÃO', SEQ_PISO)
    fim2 = tabela(d, cx, fim2 + 44, cw,
                  [('ID', 0.07, 'start'), ('Tarefa', 0.71, 'start'), ('Quantidade', 0.22, 'end')],
                  TAB_PISO_C, titulo='NAS DUAS OPÇÕES — BANHEIRO E SOLEIRAS', alt=18)
    regua_fases(d, cx, fim2 + 58, cw, (6,))
    rodape_fo(d, 'FOLHA FO2 / 3', 'Piso')
    return d


# ---------------------------------------------------------------------------
# FO3 — ELÉTRICA
# ---------------------------------------------------------------------------
from prancha_05_eletrica import TOMADAS_EXIST, TOMADAS_NOVAS, COMANDOS, QUADRO
from prancha_04_teto import TRILHOS, DESTAQUES, EMBUTIDOS_WC, MAQUINAS

TAB_ELE = [
    ('QD',  'Quadro de distribuição: avaliar, dimensionar e substituir',       '1 conjunto'),
    ('T01–T09', 'Tomadas existentes: conferir caixa, altura e circuito',       '9 pontos'),
    ('T10–T17', 'Tomadas novas',                                               '8 pontos'),
    ('S01–S08', 'Comandos / interruptores, com paralelos na cabeceira',        '8 pontos'),
    ('TR1–TR6', 'Pontos de alimentação de trilho eletrificado no teto',        '6 pontos'),
    ('P01–P03', 'Pontos de luminária de destaque — jantar, cama e office',     '3 pontos'),
    ('EM',  'Embutidos no forro do banheiro',                                  '2 pontos'),
    ('AC',  'Alimentação de evaporadoras AC01 e AC02',                         '2 pontos'),
    ('EX',  'Alimentação de exaustor do banheiro e coifa da cozinha',          '2 pontos'),
    ('IN1', 'Infraestrutura embutida em parede — antes de fechar a drywall R01', '4,08 m'),
    ('IN2', 'Infraestrutura aparente no teto: perfilado ou eletrocalha pintada', 'a medir'),
    ('IN3', 'Circuitos dedicados: geladeira, forno, cooktop, lava-louças, coifa', '5 circuitos'),
    ('PR',  'Proteção: disjuntores, DR e DPS conforme projeto elétrico',       '1 conjunto'),
    ('AT',  'Aterramento e equipotencialização',                               '1 conjunto'),
    ('EN',  'Ensaios: continuidade, isolamento, DR e aterramento',             '1 conjunto'),
]

SEQ_ELE = [
    ('1', ['Levantamento e ensaio — E02.',
           'Identificar quadro, prumadas e circuitos existentes. Medir isolamento.'], True),
    ('2', ['Estudo de demanda e projeto executivo.',
           'Diagrama unifilar, seções, proteção e quadro dimensionado antes de comprar',
           'material. Considerar 2 a 3 evaporadoras, forno, cooktop e lava-louças.'], True),
    ('3', ['Marcação de pontos em obra.',
           'Conferir com marcenaria e mobiliário antes de abrir caixa. Faixa de 1,00 m',
           'a leste do vão da porta de correr é reservada: nada de caixa ali.'], True),
    ('4', ['Infraestrutura embutida — IN1.',
           'Concluir antes de fechar a drywall R01.'], True),
    ('5', ['Infraestrutura aparente no teto — IN2.',
           'Somente após o preparo da laje (P03), alinhada aos trilhos e vigas.'], False),
    ('6', ['Descidas, caixas e passagem de cabos.',
           'Concluir antes do piso.'], True),
    ('7', ['Quadro, proteção e aterramento — QD, PR e AT.'], False),
    ('8', ['Ensaios — EN.',
           'Continuidade, isolamento, DR e aterramento, com laudo por escrito.'], False),
    ('9', ['Luminárias, trilhos e acabamentos.',
           'Somente após a pintura concluída.'], False),
]


def folha_eletrica():
    d = folha_nova()
    cabeca_fo(d, 'Elétrica', 'FO3 — ELÉTRICA',
              'Pontos de força, comando e teto num único mapa. Posições de referência: conferir em obra antes de abrir caixa.')

    S = 63.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 206, 15, nota=None)

    # trilhos: linha + ponto de alimentação
    for (ident, p0, p1, n) in TRILHOS:
        a = d.PM(*p0); b = d.PM(*p1)
        d.line(a[0], a[1], b[0], b[1], BG, 5.0)
        d.line(a[0], a[1], b[0], b[1], K, 2.0, cap='round')
        d.circle(a[0], a[1], 5.0, fill=AMARELO, stroke=K, sw=1.2)
        vertical = abs(b[0] - a[0]) < 1
        if vertical:
            d.txt(a[0] + 9, a[1] - 7, ident, 7.0, K, 'bold', 'start', ls=0.3)
        else:
            d.txt(a[0], a[1] - 11, ident, 7.0, K, 'bold', 'start', ls=0.3)
    for (ident, xm, ym, nome) in DESTAQUES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 8.5, fill=AMARELO, stroke=K, sw=1.5)
        d.circle(cx, cy, 2.6, fill=K)
        d.txt(cx, cy + 19, ident, 7.2, K, 'bold', 'middle', ls=0.3)
    for (xm, ym) in EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.0, fill=BG, stroke=K, sw=1.1)
    for (ident, xm, ym, nome) in MAQUINAS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 16, cy - 6, 32, 12, fill=CIANO35, stroke=K, sw=1.1)
        d.txt(cx, cy + 3.4, ident, 6.8, K, 'bold', 'middle', ls=0.3)
    for (ident, xm, ym) in TOMADAS_EXIST:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.4, fill=BG, stroke=K45, sw=1.5)
        d.circle(cx, cy, 1.8, fill=K45)
        d.txt(cx, cy - 9, ident, 6.4, K45, 'bold', 'middle', ls=0.3)
    for (ident, xm, ym, uso) in TOMADAS_NOVAS:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.4, fill=CIANO, stroke=K, sw=1.3)
        d.circle(cx, cy, 1.8, fill=K)
        d.txt(cx, cy - 9, ident, 6.4, K, 'bold', 'middle', ls=0.3)
    from prancha_05_eletrica import ROTULO_LESTE
    for (ident, xm, ym) in COMANDOS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 5.2, cy - 5.2, 10.4, 10.4, fill=BG, stroke=K, sw=1.3)
        d.line(cx - 2.4, cy + 2.4, cx + 2.4, cy - 2.4, K, 1.2)
        if ident == 'S03':
            d.txt(cx - 8.5, cy + 2.4, ident, 6.4, K, 'bold', 'end', ls=0.3)
        elif ident in ROTULO_LESTE:
            d.txt(cx + 8.5, cy + 2.4, ident, 6.4, K, 'bold', 'start', ls=0.3)
        else:
            d.txt(cx, cy - 9, ident, 6.4, K, 'bold', 'middle', ls=0.3)
    cx, cy = d.PM(*QUADRO)
    d.rect(cx - 10, cy - 7, 20, 14, fill=MAGENTA18, stroke=DEMO, sw=1.8)
    for i in range(3):
        d.line(cx - 6 + i * 6, cy - 4, cx - 6 + i * 6, cy + 4, DEMO, 1.1)
    d.txt(cx, cy + 19, 'QD', 7.6, DEMO, 'bold', 'middle', ls=0.4)

    for k, lx, ly in (('jantar', 520.0, 152.0), ('sala', 470.0, 300.0),
                      ('cozinha', 280.0, 352.0), ('quarto', 520.0, 470.0),
                      ('banheiro', 380.6, 430.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    for k in ROOM_ORDER:
        if k == 'closet':
            continue
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], 8.2, INK, 'bold', 'middle', ls=0.9)
    lx, ly = d.P(329.0, 498.0)
    d.txt(lx, ly, 'CLOSET', 6.8, INK, 'bold', 'middle', ls=0.6)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('dotf', K45, 'Tomada existente'), ('fill', CIANO, 'Tomada nova'),
                ('fill', BRANCO, 'Comando'), ('line', K, 'Trilho'),
                ('fill', AMARELO, 'Alimentação de teto'), ('fill', CIANO35, 'AC / exaustão'),
                ('fill', MAGENTA18, 'Quadro')],
            70, 156 + BUILDING_H * S + 62, largura=600)
    regua_fases(d, 70, 862, 600, (4, 8))

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('ID', 0.16, 'start'), ('Tarefa', 0.62, 'start'), ('Quantidade', 0.22, 'end')],
                 TAB_ELE, titulo='ESCOPO — TAREFA E QUANTIDADE', alt=19)
    sequencia(d, cx2, fim + 34, cw, 'ORDEM DE EXECUÇÃO', SEQ_ELE)
    rodape_fo(d, 'FOLHA FO3 / 3', 'Elétrica')
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    saidas = []
    for fn, nome, titulo in ((folha_demolicao, 'fornecedor-01-demolicao', 'FO1: demolição e preparo'),
                             (folha_piso,      'fornecedor-02-piso',      'FO2: piso'),
                             (folha_eletrica,  'fornecedor-03-eletrica',  'FO3: elétrica')):
        caminho = salvar(fn(), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus 81I — fornecedores — ' + titulo)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
        saidas.append(caminho)
    exportar_pdf_a3(saidas, os.path.join(pasta, 'caderno-fornecedores-A3.pdf'),
                    'MaxHaus 81I — pacote para fornecedores (A3)')
    print('ok fornecedores: 3 folhas + pacote')
