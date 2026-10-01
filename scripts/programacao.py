# -*- coding: utf-8 -*-
"""Programação da obra — quem entra quando (REV. O).

Quadro de fases × fornecedores. Não há durações: cada contratada preenche as
suas no cronograma. O que esta folha fixa é a ordem — em que fase cada
fornecedor entra, quando volta e qual decisão precisa estar fechada antes de
a fase começar. Usado pela Prancha 14 e pela folha FO8 dos fornecedores.
"""
from base_mainfloor import (K, K04, K12, K45, K70, INK, INK_SOFT, RULE, BG, DEMO,
                            AMARELO, AMARELO40, CIANO, CIANO18, BRANCO)

FASES = [
    ('1', 'Ensaios e', 'proteção'),
    ('2', 'Demolição', ''),
    ('3', 'Preparo de', 'superfícies'),
    ('4', 'Infraestrutura', ''),
    ('5', 'Reconstruções', ''),
    ('6', 'Piso e', 'revestimentos'),
    ('7', 'Pintura', ''),
    ('8', 'Acabamentos e', 'equipamentos'),
    ('9', '2027/28', 'claraboia'),
]

# (fornecedor, folha, {fase: texto})
LINHAS = [
    ('Empreiteira — demolição e obra civil', 'FO1',
     {1: 'proteção · ensaios E01/E02', 2: 'forro 100%, pisos e banheiro inteiro',
      3: 'laje P03 e paredes P01–P04', 5: 'drywall R01 · box R02 · forro R03',
      6: 'contrapiso P06 · cota P05'}),
    ('Hidráulica do banheiro', '—',
     {1: 'ensaio de estanqueidade E01', 4: 'pontos novos: cuba, bacia, ducha, ralo',
      8: 'louças e metais'}),
    ('Elétrica', 'FO3',
     {1: 'isolamento E02', 4: 'eletrodutos, quadro, esperas AL e T18',
      8: 'tomadas, comandos e testes'}),
    ('Ar-condicionado e exaustão', 'FO5',
     {4: 'frigorígena, dreno e duto do EX01', 8: 'evaporadoras e exaustor'}),
    ('Iluminação', 'FO4',
     {5: 'embutidos no forro novo R03', 8: 'trilhos e luminárias'}),
    ('Banheiro — impermeabilização e revestimento', 'FO2',
     {5: 'impermeabilização e caimento C1–C2', 6: 'piso e paredes até 2,40 m'}),
    ('Piso da casa', 'FO2',
     {6: 'opção A (cumaru + monolítico) ou B (monolítico)'}),
    ('Pintura', '—',
     {7: 'laje, paredes e forro R03'}),
    ('Marmoraria — bancadas KC1, KC2, WB1', 'FO7',
     {6: 'gabarito com paredes revestidas', 8: 'assentar pedras e frontões'}),
    ('Vidraçaria — box', 'FO7',
     {5: 'se B: perfis na parede R02', 6: 'medir vão revestido', 8: 'instalar K01 (A) ou VB1 (B)'}),
    ('Portas P02 e P03', 'FO7',
     {5: 'vão de 1,00 m na drywall R01', 8: 'trilho P03 · giro novo da P02'}),
    ('Cortina e claraboia', 'FO6',
     {3: 'apoios no concreto confirmados', 4: 'espera T18 e comando S10',
      5: 'apoios e perfil PF1', 8: 'trilho CT01 e cortina CT02'}),
    ('Marcenaria — closet', 'FO1',
     {2: 'desmontar e etiquetar M01', 8: 'remontar M01'}),
    ('Fechamento elétrico da claraboia', 'FO6',
     {9: 'FC01 e FC02 na espera T18'}),
]

# decisões que têm de estar fechadas ANTES de a fase começar: (fase, texto)
MARCOS = [
    (2, ['Laudo de E01/E02:', 'troca ou não da', 'hidráulica e elétrica']),
    (4, ['Engenheiro: onde o', 'concreto da claraboia', 'admite apoio']),
    (5, ['Box A (K01) ou', 'B (VB1 de 2,00 m)']),
    (6, ['Piso A ou B · cuba,', 'cooktop e metais']),
    (8, ['Luminárias, tecido', 'da cortina e louças']),
]


def _quebra(texto, n):
    linhas, atual = [], ''
    for p in texto.split():
        if atual and len(atual) + 1 + len(p) > n:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + ' ' + p).strip()
    if atual:
        linhas.append(atual)
    return linhas


def desenhar(d, x, y, largura, alt=34.0):
    """Desenha o quadro a partir de (x, y). Devolve o y final."""
    col_nome, col_folha = 236.0, 40.0
    nf = len(FASES)
    cw = (largura - col_nome - col_folha) / nf
    x0f = x + col_nome + col_folha

    # cabeçalho das fases
    d.rect(x, y, largura, 34, fill=K12)
    d.txt(x + 8, y + 21, 'FORNECEDOR', 8.0, INK_SOFT, 'bold', ls=0.8)
    d.txt(x + col_nome + col_folha / 2, y + 21, 'FOLHA', 7.2, INK_SOFT, 'bold', 'middle', ls=0.4)
    for i, (num, l1, l2) in enumerate(FASES):
        cx = x0f + i * cw
        d.txt(cx + 8, y + 14, num, 9.0, K, 'bold')
        d.txt(cx + 20, y + 14, l1, 7.4, INK, 'bold')
        if l2:
            d.txt(cx + 20, y + 25, l2, 7.4, INK, 'bold')
    yy = y + 34

    # linhas
    for n, (nome, folha, celulas) in enumerate(LINHAS):
        if n % 2 == 1:
            d.rect(x, yy, largura, alt, fill=K04)
        nl = _quebra(nome, 38)
        for j, ln in enumerate(nl[:2]):
            d.txt(x + 8, yy + alt / 2 + 3 - (len(nl[:2]) - 1) * 5 + j * 10, ln, 8.0, INK, 'bold')
        d.txt(x + col_nome + col_folha / 2, yy + alt / 2 + 3, folha, 7.6, INK_SOFT, 'bold', 'middle')
        primeira = min(celulas)
        for f, texto in sorted(celulas.items()):
            cx = x0f + (f - 1) * cw
            futuro = (f == 9)
            cor = AMARELO40 if f == primeira else CIANO18
            if futuro:
                d.rect(cx + 3, yy + 4, cw - 6, alt - 8, fill='none', stroke=K45, sw=0.9, dash='4 3')
            else:
                d.rect(cx + 3, yy + 4, cw - 6, alt - 8, fill=cor, stroke=K, sw=0.7)
            tl = _quebra(texto, int((cw - 12) / 3.25))[:2]
            for j, ln in enumerate(tl):
                d.txt(cx + 8, yy + alt / 2 + 2.5 - (len(tl) - 1) * 4.6 + j * 9.2, ln, 6.6, K, 'normal')
        d.line(x, yy + alt, x + largura, yy + alt, RULE, 0.6, opacity=0.8)
        yy += alt

    # divisórias das fases
    for i in range(nf + 1):
        xx = x0f + i * cw
        d.line(xx, y, xx, yy, RULE, 0.6, opacity=0.9)
    d.line(x0f - col_folha, y, x0f - col_folha, yy, RULE, 0.6, opacity=0.9)

    # decisões que liberam a fase
    ym = yy + 22
    d.txt(x + 8, ym + 4, 'DECISÕES QUE LIBERAM A FASE', 8.0, INK_SOFT, 'bold', ls=1.0)
    d.txt(x + 8, ym + 16, 'fechadas antes de a fase começar', 7.2, INK_SOFT)
    for (f, linhas) in MARCOS:
        xx = x0f + (f - 1) * cw
        d.line(xx, yy, xx, ym - 6, DEMO, 1.4)
        d.path('M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z'
               % (xx, ym - 6, xx + 6, ym, xx, ym + 6, xx - 6, ym), fill=DEMO, stroke=DEMO, sw=0.8)
        for j, ln in enumerate(linhas):
            d.txt(xx + 10, ym + 3 + j * 9.6, ln, 7.0, K if j == 0 else INK_SOFT,
                  'bold' if j == 0 else 'normal')
    return ym + 36


def legenda_programacao(d, x, y):
    itens = [(AMARELO40, K, None, 'Entrada do fornecedor'),
             (CIANO18, K, None, 'Retorno à obra'),
             ('none', K45, '4 3', '2027/28 — fora desta obra'),
             (DEMO, DEMO, None, 'Decisão que libera a fase')]
    cx = x
    for fill, st, dash, txt in itens:
        if fill == DEMO:
            d.path('M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z'
                   % (cx + 7, y - 9, cx + 13, y - 3, cx + 7, y + 3, cx + 1, y - 3), fill=DEMO, stroke=DEMO, sw=0.8)
        else:
            d.rect(cx, y - 8, 16, 10, fill=fill, stroke=st, sw=0.8, dash=dash)
        d.txt(cx + 22, y, txt, 8.6, INK)
        cx += 34 + len(txt) * 4.9
