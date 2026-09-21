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
ORIGEM = 'extraído do caderno de estudo REV. M'

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
    sequencia(d, cx, fim + 30, cw, 'ORDEM DE EXECUÇÃO', SEQ_DEMO, size=8.4, lh=12.1)
    rodape_fo(d, 'FOLHA FO1 / 5', 'Demolição')
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
    rodape_fo(d, 'FOLHA FO2 / 5', 'Piso')
    return d


# ---------------------------------------------------------------------------
# BASE COMUM DAS FOLHAS DE INSTALAÇÃO (FO3, FO4 e FO5)
# ---------------------------------------------------------------------------
from prancha_05_eletrica import (TOMADAS_EXIST, TOMADAS_NOVAS, COMANDOS, QUADRO,
                                 ROTULO_LESTE)
from prancha_04_teto import TRILHOS, DESTAQUES, EMBUTIDOS_WC, MAQUINAS

S_INST = 63.0


def planta_inst(d, rotulos_extra=(), escala_folha=None):
    """Casca da planta usada pelas três folhas de instalação."""
    d.set_plan(70, 156, escala_folha or S_INST)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 206, 15, nota=None)
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
    for (txt, xm, ym, size) in rotulos_extra:
        cx, cy = d.PM(xm, ym)
        d.txt(cx, cy, txt, size, INK_SOFT, 'normal', 'middle')


def ponto_alim(d, xm, ym, ident, lado='n'):
    """Caixa de alimentação que a elétrica entrega para outra disciplina."""
    cx, cy = d.PM(xm, ym)
    d.rect(cx - 4.6, cy - 4.6, 9.2, 9.2, fill=AMARELO, stroke=K, sw=1.2)
    if lado == 'n':
        d.txt(cx, cy - 8.5, ident, 6.2, K, 'bold', 'middle', ls=0.3)
    elif lado == 'e':
        d.txt(cx + 7.5, cy + 2.2, ident, 6.2, K, 'bold', 'start', ls=0.3)
    elif lado == 'o':
        d.txt(cx - 7.5, cy + 2.2, ident, 6.2, K, 'bold', 'end', ls=0.3)
    else:
        d.txt(cx, cy + 13, ident, 6.2, K, 'bold', 'middle', ls=0.3)


def zona_piscina(d, rotulo=True):
    """Projeção da piscina do pavimento superior: laje sem furação."""
    x0, y0 = d.P(AREA_PISCINA[0], AREA_PISCINA[1])
    x1, y1 = d.P(AREA_PISCINA[2], AREA_PISCINA[3])
    d.rect(x0, y0, x1 - x0, y1 - y0, fill=AMARELO40, stroke=DEMO, sw=1.4,
           dash='5 3')
    if rotulo:
        d.txt((x0 + x1) / 2.0, (y0 + y1) / 2.0 - 4, 'PISCINA ACIMA', 6.8, DEMO,
              'bold', 'middle', ls=0.5)
        d.txt((x0 + x1) / 2.0, (y0 + y1) / 2.0 + 7, 'não furar a laje', 6.4,
              DEMO, 'normal', 'middle')


# ---------------------------------------------------------------------------
# FO3 — ELÉTRICA (força, comando e quadro)
# ---------------------------------------------------------------------------
TAB_ELE = [
    ('QD',  'Quadro de distribuição: avaliar, dimensionar e substituir',       '1 conjunto'),
    ('T01–T09', 'Tomadas existentes: conferir caixa, altura e circuito',       '9 pontos'),
    ('T10–T17', 'Tomadas novas',                                               '8 pontos'),
    ('S01–S08', 'Comandos / interruptores, com paralelos na cabeceira',        '8 pontos'),
    ('IN1', 'Infraestrutura embutida em parede — antes de fechar a drywall R01', '4,08 m'),
    ('IN2', 'Infraestrutura aparente no teto: perfilado ou eletrocalha pintada', 'a medir'),
    ('IN3', 'Circuitos dedicados: geladeira, forno, cooktop, lava-louças, coifa', '5 circuitos'),
    ('AL1', 'Alimentação de trilho no teto — entregar caixa (ver FO4)',        '6 pontos'),
    ('AL2', 'Alimentação de destaque — P02 e P03 no eixo do TR5 (ver FO4)',    '3 pontos'),
    ('AL3', 'Alimentação de embutido no forro do banheiro (ver FO4)',          '2 pontos'),
    ('AL4', 'Alimentação de evaporadora — entregar caixa (ver FO5)',           '2 pontos'),
    ('AL5', 'Alimentação de exaustor e de coifa (ver FO5)',                    '2 pontos'),
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
           'Somente após o preparo da laje (P03), alinhada aos trilhos da FO4.'], False),
    ('6', ['Descidas, caixas e passagem de cabos.',
           'Concluir antes do piso.'], True),
    ('7', ['Entrega das alimentações — AL1 a AL5.',
           'Caixa no ponto, cabo passado e circuito identificado, para a iluminação',
           '(FO4) e o ar-condicionado (FO5) instalarem sem abrir parede ou laje.'], True),
    ('8', ['Quadro, proteção e aterramento — QD, PR e AT.'], False),
    ('9', ['Ensaios — EN.',
           'Continuidade, isolamento, DR e aterramento, com laudo por escrito.'], False),
    ('10', ['Ligação final e acabamento de placas.',
            'Somente após a pintura concluída.'], False),
]


def folha_eletrica():
    d = folha_nova()
    cabeca_fo(d, 'Elétrica', 'FO3 — ELÉTRICA',
              'Força, comando e quadro. Iluminação na FO4 e ar-condicionado na FO5: aqui entram só as caixas de alimentação.')

    planta_inst(d)

    # alimentações a entregar para as outras disciplinas
    for (ident, p0, p1, n) in TRILHOS:
        ponto_alim(d, p0[0], p0[1], ident, 'e' if abs(p1[0] - p0[0]) < 1 else 'n')
    for (ident, xm, ym, nome) in DESTAQUES:
        ponto_alim(d, xm, ym, ident, 's')
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 2.0, fill=K)
    for (xm, ym) in EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 3.4, cy - 3.4, 6.8, 6.8, fill=AMARELO, stroke=K, sw=1.0)
    for (ident, xm, ym, nome) in MAQUINAS:
        ponto_alim(d, xm, ym, ident, 'e')

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
    for (ident, xm, ym) in COMANDOS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 5.2, cy - 5.2, 10.4, 10.4, fill=BG, stroke=K, sw=1.3)
        d.line(cx - 2.4, cy + 2.4, cx + 2.4, cy - 2.4, K, 1.2)
        if ident == 'S03':
            d.txt(cx + 8.0, cy + 2.2, ident, 6.4, K, 'bold', 'start', ls=0.3)
        elif ident in ROTULO_LESTE:
            d.txt(cx + 8.5, cy + 2.4, ident, 6.4, K, 'bold', 'start', ls=0.3)
        else:
            d.txt(cx, cy - 9, ident, 6.4, K, 'bold', 'middle', ls=0.3)
    cx, cy = d.PM(*QUADRO)
    d.rect(cx - 10, cy - 7, 20, 14, fill=MAGENTA18, stroke=DEMO, sw=1.8)
    for i in range(3):
        d.line(cx - 6 + i * 6, cy - 4, cx - 6 + i * 6, cy + 4, DEMO, 1.1)
    d.txt(cx, cy + 19, 'QD', 7.6, DEMO, 'bold', 'middle', ls=0.4)

    escala(d, 156 + BUILDING_H * S_INST + 26)
    legenda(d, [('dotf', K45, 'Tomada existente'), ('fill', CIANO, 'Tomada nova'),
                ('fill', BRANCO, 'Comando'), ('fill', AMARELO, 'Caixa de alimentação a entregar'),
                ('fill', MAGENTA18, 'Quadro')],
            70, 156 + BUILDING_H * S_INST + 62, largura=600)
    regua_fases(d, 70, 862, 600, (1, 4))

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('ID', 0.16, 'start'), ('Tarefa', 0.62, 'start'), ('Quantidade', 0.22, 'end')],
                 TAB_ELE, titulo='ESCOPO — TAREFA E QUANTIDADE', alt=19)
    sequencia(d, cx2, fim + 32, cw, 'ORDEM DE EXECUÇÃO', SEQ_ELE, size=8.4, lh=12.2)
    rodape_fo(d, 'FOLHA FO3 / 5', 'Elétrica')
    return d


# ---------------------------------------------------------------------------
# FO4 — ILUMINAÇÃO
# ---------------------------------------------------------------------------
TAB_LUZ_FO = [
    ('TR1', 'Trilho eletrificado — jantar, 4,75 a 7,50 m', '2,75 m  ·  4 spots'),
    ('TR2', 'Trilho eletrificado — sala, eixo 4,55 m', '2,10 m  ·  3 spots'),
    ('TR3', 'Trilho eletrificado — sala, 4,20 a 7,50 m', '3,30 m  ·  4 spots'),
    ('TR4', 'Trilho eletrificado — cozinha, eixo 1,45 m', '2,50 m  ·  4 spots'),
    ('TR5', 'Trilho eletrificado — quarto, eixo 8,28 m', '3,65 m  ·  3 spots'),
    ('TR6', 'Trilho eletrificado — closet, eixo 1,45 m', '1,50 m  ·  3 spots'),
    ('—',   'Total de trilho e de spots nos seis trechos', '15,80 m  ·  21 spots'),
    ('P01', 'Luminária de destaque — jantar, pendente ou plafon', '1 peça'),
    ('P02', 'Luminária de destaque — cama, no eixo do TR5', '1 peça'),
    ('P03', 'Luminária de destaque — office, no eixo do TR5', '1 peça'),
    ('EM',  'Embutido no forro do banheiro — único ambiente com forro', '2 peças'),
    ('CT',  'Conector, emenda e terminação de trilho', 'a definir'),
    ('FX',  'Fixação direta na laje de concreto aparente — bucha e parafuso', 'a medir'),
]

TAB_LUX = [
    ('Sala',     '150 lux', '7.188 lm', '2.700 K'),
    ('Quarto',   '150 lux', '4.188 lm', '2.700 K'),
    ('Cozinha',  '300 lux', '5.563 lm', '3.000 K'),
    ('Jantar',   '150 lux', '1.844 lm', '2.700 K'),
    ('Closet',   '200 lux', '2.208 lm', '3.000 K'),
    ('Banheiro', '200 lux', '1.583 lm', '3.000 K'),
]

SEQ_LUZ = [
    ('1', ['Recebimento das alimentações da elétrica — AL1, AL2 e AL3.',
           'Caixa no ponto, cabo passado e circuito identificado (FO3, passo 7).',
           'Conferir posição de cada uma antes de comprar trilho.'], True),
    ('2', ['Conferência da laje preparada — P03.',
           'A laje é o teto acabado, a 2,62 m do piso: tudo é fixado nela, à vista.',
           'Sem forro fora do banheiro, portanto nada de embutido.'], True),
    ('3', ['Marcação dos eixos no teto.',
           'Alinhar cada trecho às vigas e ao perfilado da elétrica. Trilho não cruza',
           'trilho: se dois trechos tiverem de se encontrar, é com conector T.'], True),
    ('4', ['Zona sem furação — piscina do pavimento superior.',
           'Retângulo de 1,92 × 3,00 m sobre a sala, centrado em 6,13 / 3,14 m do canto',
           'noroeste. Nenhuma fixação, furo ou passagem dentro dele.'], True),
    ('5', ['Pintura concluída antes de instalar.',
           'Trilho, spot e luminária entram depois da pintura da laje e das paredes.'], False),
    ('6', ['Montagem de trilho e spots — TR1 a TR6.'], False),
    ('7', ['Luminárias de destaque — P01, P02 e P03.',
           'P02 e P03 correm no eixo do TR5 e podem sair do próprio trilho, com',
           'adaptador, dispensando saída nova na laje.'], False),
    ('8', ['Embutidos do banheiro — EM.'], False),
    ('9', ['Ajuste de foco e entrega.',
           'Apontar spot por spot com o mobiliário no lugar; conferir cena por comando.'], False),
]


def folha_iluminacao():
    d = folha_nova()
    cabeca_fo(d, 'Iluminação', 'FO4 — ILUMINAÇÃO',
              'Trilho eletrificado e luminárias sobre a laje aparente. A alimentação é entregue pela elétrica (FO3): aqui é montagem, não fiação.')

    S = 54.0
    planta_inst(d, escala_folha=S)
    zona_piscina(d)

    for (ident, p0, p1, n) in TRILHOS:
        a = d.PM(*p0); b = d.PM(*p1)
        d.line(a[0], a[1], b[0], b[1], BG, 5.0)
        d.line(a[0], a[1], b[0], b[1], K, 2.0, cap='round')
        vertical = abs(b[0] - a[0]) < 1
        for i in range(n):
            t = (i + 0.5) / float(n)
            sx = a[0] + (b[0] - a[0]) * t
            sy = a[1] + (b[1] - a[1]) * t
            d.circle(sx, sy, 3.2, fill=BRANCO, stroke=K, sw=1.0)
        d.circle(a[0], a[1], 4.8, fill=AMARELO, stroke=K, sw=1.2)
        if vertical:
            d.txt(a[0] + 8.5, a[1] - 6.5, ident, 6.8, K, 'bold', 'start', ls=0.3)
        else:
            d.txt(a[0], a[1] - 10.5, ident, 6.8, K, 'bold', 'start', ls=0.3)
    for (ident, xm, ym, nome) in DESTAQUES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 8.0, fill=AMARELO, stroke=K, sw=1.5)
        d.circle(cx, cy, 2.4, fill=K)
        d.txt(cx, cy + 18, ident, 7.0, K, 'bold', 'middle', ls=0.3)
    for (xm, ym) in EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 3.8, fill=BG, stroke=K, sw=1.1)
    cx, cy = d.PM(2.95, 4.85)
    d.txt(cx, cy - 10, 'EM', 6.2, K, 'bold', 'middle', ls=0.3)
    for (ident, xm, ym) in COMANDOS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 4.0, cy - 4.0, 8.0, 8.0, fill=BG, stroke=K45, sw=1.0)
        d.line(cx - 1.8, cy + 1.8, cx + 1.8, cy - 1.8, K45, 1.0)

    base = 156 + BUILDING_H * S
    escala(d, base + 26)
    legenda(d, [('line', K, 'Trilho eletrificado'), ('dot', K, 'Spot no trilho'),
                ('fill', AMARELO, 'Alimentação entregue pela elétrica'),
                ('ghost', DEMO, 'Laje sem furação — piscina acima'),
                ('ghost', K45, 'Comando (referência, escopo da FO3)')],
            70, base + 62, largura=600)
    tabela(d, 70, base + 120, 600,
           [('Ambiente', 0.34, 'start'), ('Nível', 0.22, 'end'),
            ('Fluxo alvo', 0.22, 'end'), ('Temperatura', 0.22, 'end')],
           TAB_LUX, titulo='ALVO POR AMBIENTE — PARA SELEÇÃO DE SPOT', alt=18)

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('ID', 0.11, 'start'), ('Tarefa', 0.63, 'start'), ('Quantidade', 0.26, 'end')],
                 TAB_LUZ_FO, titulo='ESCOPO — TAREFA E QUANTIDADE', alt=19)
    fim = sequencia(d, cx2, fim + 32, cw, 'ORDEM DE EXECUÇÃO', SEQ_LUZ, size=8.4, lh=12.0)
    regua_fases(d, cx2, fim + 40, cw, (8,))
    rodape_fo(d, 'FOLHA FO4 / 5', 'Iluminação')
    return d


# ---------------------------------------------------------------------------
# FO5 — AR-CONDICIONADO, EXAUSTÃO E COIFA
# ---------------------------------------------------------------------------
TAB_AR_FO = [
    ('AC01', 'Evaporadora — social + cozinha (37,80 m²)', '1 unidade'),
    ('AC02', 'Evaporadora — quarto + closet (18,70 m²)', '1 unidade'),
    ('CD',   'Condensadora: conferir modelo existente e capacidade real', '1 unidade'),
    ('FG',   'Linha frigorígena aparente, em calha, isolada', 'a medir'),
    ('DR',   'Dreno aparente, com caimento contínuo até ponto de descarte', 'a medir'),
    ('IE',   'Interligação elétrica entre condensadora e evaporadoras', '2 linhas'),
    ('SU',   'Suporte de evaporadora fixado na laje ou na parede', '2 conjuntos'),
    ('EX01', 'Exaustor do banheiro — único ambiente com forro', '1 unidade'),
    ('DU1',  'Duto e rota de descarte do exaustor do banheiro', 'a definir'),
    ('CF01', 'Coifa da cozinha — alimentação e fixação', '1 unidade'),
    ('DU2',  'Duto e rota de descarte da coifa, independente do banheiro', 'a definir'),
    ('VF',   'Vedação e acabamento das passagens de parede e de laje', 'a medir'),
    ('CG',   'Carga de gás, vácuo e teste de estanqueidade da linha', '1 conjunto'),
]

TAB_BTU = [
    ('Social + cozinha',   '37,80 m²', '22.680 BTU/h', '30.240 BTU/h'),
    ('Quarto + closet',    '18,70 m²', '11.220 BTU/h', '14.960 BTU/h'),
    ('Total sem banheiro', '56,50 m²', '33.900 BTU/h', '45.200 BTU/h'),
]

TAB_VAZAO = [
    ('EX01', 'Banheiro — 3,80 m² × 2,42 m × 10 trocas/h', '92,0 m³/h'),
    ('CF01', 'Cozinha — 8,90 m² × 2,62 m × 12 trocas/h', '279,8 m³/h'),
]

SEQ_AR = [
    ('1', ['Conferência da condensadora existente.',
           'Modelo, capacidade e número de evaporadoras que admite. Não assumir que',
           'a atual aceita duas: se não aceitar, entra no orçamento.'], True),
    ('2', ['Seleção pela coluna base sol — 30.240 e 14.960 BTU/h, somente Electrolux.',
           'A fachada envidraçada é noroeste e pega o sol da tarde. Marca igual não',
           'garante compatibilidade: conferir o par no catálogo antes de comprar.'], True),
    ('3', ['Não há forro para dutar, fora do banheiro.',
           'Evaporadora hi-wall ou cassete aparente; frigorígena, dreno e interligação',
           'aparentes, em calha, alinhados às vigas e ao perfilado da elétrica.'], False),
    ('4', ['Zona sem furação — piscina do pavimento superior.',
           'Retângulo de 1,92 × 3,00 m sobre a sala. Nem equipamento, nem suporte,',
           'nem tubulação dentro dele.'], True),
    ('5', ['Posição definitiva do AC01 em obra.',
           'A posição em planta é reserva: confirmar apoio acima do limite sala/jantar',
           'e altura livre na faixa de 2,62 m antes de fixar.'], True),
    ('6', ['Infraestrutura: passagens, calha, frigorígena e dreno — FG, DR, IE.',
           'Executar após o preparo da laje (P03) e antes da pintura.'], False),
    ('7', ['Exaustão — EX01 e CF01, com rotas próprias.',
           'Uma rota não serve às duas. Validar vazão com a perda de carga do duto e',
           'a rota de descarte com o condomínio antes de furar fachada.'], True),
    ('8', ['Recebimento da alimentação elétrica — AL4 e AL5.',
           'Caixa no ponto e circuito identificado, entregues pela FO3, passo 7.'], False),
    ('9', ['Montagem, vácuo, carga e teste — CG.',
           'Equipamento entra após a pintura. Entregar com teste de estanqueidade,',
           'medição de temperatura e nota de garantia por escrito.'], False),
]


def folha_ar():
    d = folha_nova()
    cabeca_fo(d, 'Ar-condicionado e exaustão', 'FO5 — AR',
              'Evaporadoras, exaustor e coifa sobre laje aparente, sem forro para dutar. Somente Electrolux. A alimentação é entregue pela elétrica (FO3).')

    S = 49.0
    planta_inst(d, escala_folha=S)
    zona_piscina(d)

    for (ident, xm, ym, nome) in MAQUINAS:
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 19, cy - 8, 38, 16, fill=CIANO35, stroke=K, sw=1.4)
        d.txt(cx + 3, cy + 3.6, ident, 7.4, K, 'bold', 'middle', ls=0.4)
        d.rect(cx - 18, cy - 4.2, 8.4, 8.4, fill=AMARELO, stroke=K, sw=1.0)

    base = 156 + BUILDING_H * S
    escala(d, base + 26)
    legenda(d, [('fill', CIANO35, 'Evaporadora, exaustor e coifa'),
                ('fill', AMARELO, 'Alimentação entregue pela elétrica'),
                ('ghost', DEMO, 'Laje sem furação — piscina acima')],
            70, base + 62, largura=600)
    fim = tabela(d, 70, base + 120, 600,
                 [('Zona', 0.34, 'start'), ('Área', 0.20, 'end'),
                  ('Base sombra', 0.23, 'end'), ('Base sol', 0.23, 'end')],
                 TAB_BTU, titulo='CARGA TÉRMICA — 600 / 800 BTU/h POR m², SELECIONAR PELA BASE SOL',
                 alt=18)
    tabela(d, 70, fim + 42, 600,
           [('ID', 0.11, 'start'), ('Cálculo de referência', 0.67, 'start'),
            ('Vazão', 0.22, 'end')],
           TAB_VAZAO, titulo='EXAUSTÃO — VAZÃO A VALIDAR COM PERDA DE CARGA DO DUTO', alt=18)

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx2, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx2, 160, cw,
                 [('ID', 0.11, 'start'), ('Tarefa', 0.67, 'start'), ('Quantidade', 0.22, 'end')],
                 TAB_AR_FO, titulo='ESCOPO — TAREFA E QUANTIDADE', alt=19)
    fim = sequencia(d, cx2, fim + 32, cw, 'ORDEM DE EXECUÇÃO', SEQ_AR, size=8.4, lh=12.0)
    regua_fases(d, cx2, fim + 40, cw, (4, 8))
    rodape_fo(d, 'FOLHA FO5 / 5', 'Ar-condicionado')
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    saidas = []
    for fn, nome, titulo in ((folha_demolicao,  'fornecedor-01-demolicao',  'FO1: demolição e preparo'),
                             (folha_piso,       'fornecedor-02-piso',       'FO2: piso'),
                             (folha_eletrica,   'fornecedor-03-eletrica',   'FO3: elétrica'),
                             (folha_iluminacao, 'fornecedor-04-iluminacao', 'FO4: iluminação'),
                             (folha_ar,         'fornecedor-05-ar',         'FO5: ar-condicionado e exaustão')):
        caminho = salvar(fn(), pasta, nome)
        exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                        'MaxHaus 81I — fornecedores — ' + titulo)
        exportar_png(caminho, os.path.join(pasta, nome + '.png'))
        saidas.append(caminho)
    exportar_pdf_a3(saidas, os.path.join(pasta, 'caderno-fornecedores-A3.pdf'),
                    'MaxHaus 81I — pacote para fornecedores (A3)')
    print('ok fornecedores: 5 folhas + pacote')
