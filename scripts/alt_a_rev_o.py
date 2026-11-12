# -*- coding: utf-8 -*-
"""Caderno Alternativo A — REV. R (14 pranchas + FO1 a FO8; a base é a REV. O, mais REV. Q e R).

Cópia da REV. O do caderno principal com a proposta do Caderno Alternativo A,
que é a que está sendo seguida: a parede cozinha/closet desce 0,45 m para o
sul, alinhada à face sul do banheiro (D09, D10 e a parede nova R04, com o
ensaio estrutural E03 antes). Todos os pedidos da REV. O entram iguais:
sala de estar / sala de TV, trilho reto da cortina, pedras, vidro do box e
portas, P02 abrindo para o quarto, banheiro em reforma completa e programação.
A cama do quarto adaptável fica só nas tabelas — não é desenhada.

Nada aqui redesenha folha: os scripts das pranchas e dos fornecedores são os
mesmos da REV. O. Muda a geometria de trabalho (trocada no lugar, para que
todos os módulos a vejam), as tabelas que dependem da área da cozinha e do
closet, e o cabeçalho e o rodapé, que marcam ALTERNATIVO A em todas as folhas.
Na parede nova o ID é R04: na REV. O, R03 passou a ser o forro do banheiro.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base_mainfloor as bm
from base_mainfloor import *      # noqa
from base_mainfloor import esc
import prancha_01_planta as p01
import prancha_02_demolicao as p02
import prancha_03_pisos as p03
import prancha_04_teto as p04
import prancha_05_eletrica as p05
import prancha_06_esquadrias as p06
import prancha_07_banheiro as p07
import prancha_09_medicao as p09
import prancha_10_banheiro_acabamentos as p10
import prancha_11_ar_luz as p11
import prancha_12_riscos as p12
import prancha_13_quarto_claraboia as p13
import prancha_14_programacao as p14
import programacao as pg
import quarto_adaptavel as qa
import fornecedores as fo
from alt_a_parede_cozinha import (ORIG_WALLS, ORIG_ROOMS, ALT_WALLS, ALT_ROOMS,
                                  WALL_REMOVER_1, WALL_REMOVER_2, WALL_NOVA)

REV_ALT = 'ALT. A  ·  REV. O'
TOPO = 'MAXHAUS / MAIN FLOOR  ·  CADERNO ALTERNATIVO A  ·  PAREDE COZINHA/CLOSET 0,45 M AO SUL'


# ---------------------------------------------------------------------------
# geometria de trabalho — trocada no lugar, todos os módulos enxergam
# ---------------------------------------------------------------------------
# drywall sala de TV/quarto (R01) refeita 0,17 m ao norte: o quarto passa de
# 2,54 para 2,71 m livres e a sala de TV perde o mesmo (0,68 m²). A D01 sai
# onde está hoje; só a R01 e a porta P03 mudam de lugar.
DY_R01 = 0.17 * PT_PER_M
Y_R01_ANT = 432.3
Y_R01 = Y_R01_ANT - DY_R01
DRYWALL_ANT = bm.DRYWALL_SALA_QUARTO


def _norte(r):
    return (r[0], r[1] - DY_R01, r[2], r[3] - DY_R01)


DRYWALL_R01 = _norte(DRYWALL_ANT)
PORTA_R01 = _norte(bm.PORTA_NOVA)
ALT_WALLS = [DRYWALL_R01 if w == DRYWALL_ANT else w for w in ALT_WALLS]
for _k, _a in (('sala', 22.32), ('quarto', 14.08)):
    ALT_ROOMS[_k]['poly'] = [(x, Y_R01 if (y == Y_R01_ANT and x >= 415.0) else y)
                             for x, y in ALT_ROOMS[_k]['poly']]
    ALT_ROOMS[_k]['area'] = _a
for _m in (bm, p01, p02, p03, p04, p05, p06, p07, p13, fo):
    if hasattr(_m, 'PORTA_NOVA'):
        _m.PORTA_NOVA = PORTA_R01


def realce_r01(d, cor=K):
    x, y, w_, h_ = d.R(DRYWALL_R01)
    d.rect(x, y, w_, h_, fill='none', stroke=cor, sw=1.3, dash='4 3')


def geometria(proposta=True):
    bm.WALLS[:] = ALT_WALLS if proposta else ORIG_WALLS
    src = ALT_ROOMS if proposta else ORIG_ROOMS
    for k in ('cozinha', 'closet', 'sala', 'quarto'):
        bm.ROOMS[k]['poly'] = list(src[k]['poly'])
        bm.ROOMS[k]['area'] = src[k]['area']


def trocar(d, velho, novo):
    """Troca um texto já desenhado na folha (string exata)."""
    a, b = '>' + esc(velho) + '</text>', '>' + esc(novo) + '</text>'
    n = 0
    for i, s in enumerate(d.o):
        if a in s:
            d.o[i] = s.replace(a, b)
            n += 1
    if not n:
        raise ValueError('texto não encontrado: %r' % velho)


def realce_parede(d):
    for r in (WALL_NOVA, DRYWALL_R01):
        x, y, w_, h_ = d.R(r)
        d.rect(x - 1.5, y - 1.5, w_ + 3, h_ + 3, fill='none', stroke=DEMO, sw=1.1, dash='3 2.5')


# ---------------------------------------------------------------------------
# cabeçalho e rodapé
# ---------------------------------------------------------------------------
def cabecalho_alt(d, titulo, subtitulo, rev, dir1='', dir2=''):
    d.txt(MARGIN, 42, TOPO, 10.0, INK_SOFT, 'bold', ls=1.4)
    d.txt(MARGIN, 78, titulo, 27, INK, 'bold')
    d.txt(MARGIN, 99, subtitulo, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, REV_ALT, 10.0, RED, 'bold', 'end', ls=0.8)
    if dir1:
        d.txt(W - MARGIN, 78, dir1, 10.5, INK, 'bold', 'end')
    if dir2:
        d.txt(W - MARGIN, 99, dir2, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)


def rodape_alt(d, nota1, nota2, prancha, rev):
    d.line(MARGIN, 922, W - MARGIN, 922, RULE, 1.0)
    if nota1:
        d.txt(MARGIN, 940, nota1, 8.3, INK_SOFT)
    if nota2:
        d.txt(MARGIN, 953, nota2, 8.3, INK_SOFT)
    d.txt(MARGIN, 975, 'ESTUDO PRELIMINAR — NÃO LIBERADO PARA EXECUÇÃO   |   CADERNO ALTERNATIVO A   |   '
          + bm.DATA_EMISSAO, 9.0, RED, 'bold', ls=0.5)
    d.txt(W - MARGIN, 975, 'Alt A · %s   ·   %s' % (prancha, REV_ALT), 9.0, INK_SOFT, 'normal', 'end')


PRANCHAS = (p01, p02, p03, p04, p05, p06, p07, p09, p10, p11, p12, p13, p14)
for _m in PRANCHAS:
    _m.cabecalho = cabecalho_alt
    _m.rodape = rodape_alt

# posições de rótulo da cozinha e do closet (a cozinha desce 0,45 m)
ROTULO_ALT = {}


def rotulos_alt(d, areas=True, size=8.8):
    for k, (lx, ly) in ROTULO_ALT.items():
        bm.ROOMS[k]['lx'], bm.ROOMS[k]['ly'] = lx, ly
    return bm.rotulos(d, areas=areas, size=size)


for _m in (p01, p02, p03, p04, p05):
    _m.rotulos = rotulos_alt

# ---------------------------------------------------------------------------
# números que dependem da cozinha e do closet
#   cozinha 8,90 → 9,82 m² · closet 5,30 → 4,38 m² · soma igual (14,20 m²)
#   perímetro ±0,90 m · parede ±0,90 × 2,40 = ±2,16 m² · volume × 2,62
# ---------------------------------------------------------------------------
COZ, CLO = 9.82, 4.38
KC_SUL = my(450.67)


def _subst(lista, chave, nova):
    for i, l in enumerate(lista):
        if l[0] == chave:
            lista[i] = nova
            return
    raise KeyError(chave)


# ---- Prancha 01 -----------------------------------------------------------
_subst(p01.TAB_AMB, 'Cozinha', ('Cozinha', '9,82 m²', '14,6 m', '5,2 × 2,1', '5,2 × 1,4'))
_subst(p01.TAB_AMB, 'Closet', ('Closet', '4,38 m²', '8,4 m', '2,1 × 2,1', '—'))
p01.NOTAS[:] = [
    ['**Alternativo A: a parede cozinha/closet desce 0,45 m para o sul.',
     'Fica alinhada à face sul do banheiro e segue até a parede externa oeste (R04, tracejada em',
     'magenta). A cozinha passa de 8,90 para 9,82 m² e o closet de 5,30 para 4,38 m²; a soma das',
     'duas e a área do MainFloor não mudam. A largura livre comum, 2,04 m, também não.'],
] + [n for n in p01.NOTAS if not n[0].startswith('**Bounding box')]

_REMAP = {430.06: 450.67, 434.63: 455.24}


def _ry(v):
    return _REMAP.get(v, v)


def _cadeia_v(d, cortes, x, off, *a, **k):
    if x < 300:
        cortes = [_ry(v) for v in cortes]
    return bm.cadeia_v(d, cortes, x, off, *a, **k)


def _r01(v):
    return v - DY_R01 if v in (430.06, 434.63) else v


def _cota_v(d, y0, y1, x, off, *a, **k):
    if x < 300:
        y0, y1 = _ry(y0), _ry(y1)
    elif x >= 415.0:
        y0, y1 = _r01(y0), _r01(y1)
    return bm.cota_v(d, y0, y1, x, off, *a, **k)


def _cota_h(d, x0, x1, y, off, *a, **k):
    if x1 <= 345.0 and y == 430.06:
        y = 450.67
    elif x0 >= 415.0:
        y = _r01(y)
    return bm.cota_h(d, x0, x1, y, off, *a, **k)


p01.cadeia_v, p01.cota_v, p01.cota_h = _cadeia_v, _cota_v, _cota_h


def construir_01():
    ROTULO_ALT.clear()
    ROTULO_ALT.update({'cozinha': (300.0, 375.0), 'closet': (297.0, 508.0)})
    d = p01.construir()
    d.set_plan(132, 182, 64.0)
    realce_parede(d)
    bm.cota_v(d, 455.24, 550.38, 343.39, -16, size=6.6, ext=False)     # profundidade do closet
    bm.cota_v(d, 434.63 - DY_R01, 550.38, 599.46, -16, size=6.6, ext=False)   # quarto, 2,71
    return d


# ---- Prancha 02 -----------------------------------------------------------
ALVOS_ALT = [
    ('D09', 281.64, 488.0, 'demo', -10, 3),
    ('D10', 312.50, 432.35, 'demo', 10, -8),
    ('R04', 294.50, 452.96, 'novo', 10, 16),
    ('E03', 326.0, 478.0, 'ensaio', 10, 3),
]
p02.ALVOS = p02.ALVOS + ALVOS_ALT
_l = p02.LINHAS
_l.insert([r[0] for r in _l].index('D05'), ('D09', 'Parede interna do closet — só depois do E03', '2,54 m'))
_l.insert([r[0] for r in _l].index('D05'), ('D10', 'Parede cozinha/closet, trecho existente — só depois do E03', '1,45 m'))
_l.insert([r[0] for r in _l].index('M01'), ('R04', 'Parede nova cozinha/closet, na face sul do banheiro até a oeste', '2,17 m · 2 faces'))
_subst(_l, 'M01', ('M01', 'Desmontar o closet; volta com módulos novos (0,45 m mais raso)', '1 conjunto — inventário'))
_l.append(('E03', 'Ensaio estrutural das paredes cozinha/closet, com engenheiro', 'antes de D09 e D10'))
for _i, _n in enumerate(p02.NOTAS):
    if _n[0].startswith('**Closet:'):
        p02.NOTAS[_i] = [
            '**Alternativo A: a parede cozinha/closet desce 0,45 m (D09, D10 e R04).',
            'Sem projeto estrutural do edifício: o ensaio E03, com engenheiro, vem antes de demolir. Abrir',
            'a D10 com cautela (hidráulica ou gás embutido). O closet fica 0,45 m mais raso: M01 volta com',
            'módulos novos, não os mesmos remontados.']
    elif _n[0].startswith('**Dois ensaios'):
        p02.NOTAS[_i] = [
            '**Ensaios antes de decidir (E01, E02 e E03).',
            'Estanqueidade na hidráulica, isolamento na elétrica e estrutura das paredes cozinha/closet.',
            'Orientação de escopo, não laudo — a decisão final pede um engenheiro na inspeção.']
p02.NOTAS[:] = [n for n in p02.NOTAS if not n[0].startswith('**A laje inteira')]
_tab02 = p02.tabela


def _tabela_compacta(d, x, y, w, cols, linhas, titulo=None, alt=None):
    return _tab02(d, x, y, w, cols, linhas, titulo=titulo, alt=16.6)


p02.tabela = _tabela_compacta


def construir_02():
    geometria(False)
    ROTULO_ALT.clear()
    try:
        d = p02.construir()
        d.set_plan(70, 156, 70.0)
        for r in (WALL_REMOVER_1, WALL_REMOVER_2):
            x, y, w_, h_ = d.R(r)
            d.rect(x, y, w_, h_, fill=DEMO, opacity=0.32)
            d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.4)
        x, y, w_, h_ = d.R(WALL_NOVA)
        d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.4, dash='4 3')
        realce_r01(d)
    finally:
        geometria(True)
    return d


# ---- Pranchas 03 e 04 -----------------------------------------------------
_subst(p03.TAB_A, 'Monolítico',
       ('Monolítico', 'cozinha 7,43 (de 9,82) + closet 4,38 — zona contínua', '11,81 m²'))


def construir_piso(opcao):
    ROTULO_ALT.clear()
    ROTULO_ALT.update({'cozinha': (300.0, 392.0), 'closet': (300.0, 508.0)})
    d = p03.construir(opcao)
    d.set_plan(70, 156, 70.0)
    realce_parede(d)
    return d


# ---- Prancha 05 — teto ----------------------------------------------------
_subst(p04.TAB_LUZ, 'Cozinha', ('Cozinha', '300 lux', '6.138 lm', '3.000 K'))
_subst(p04.TAB_LUZ, 'Closet', ('Closet', '200 lux', '1.825 lm', '3.000 K'))
_subst(p04.TAB_AR, 'Social + cozinha', ('Social + cozinha', '38,72 m²', '23.232 BTU/h', '30.976 BTU/h'))
_subst(p04.TAB_AR, 'Quarto + closet', ('Quarto + closet', '17,78 m²', '10.668 BTU/h', '14.224 BTU/h'))
_subst(p04.TRILHOS, 'TR4', ('TR4', (1.45, 3.90), (1.45, 6.85), 5))   # cozinha 0,45 m mais funda
for _n in p04.NOTAS:
    for _j, _ln in enumerate(_n):
        if _ln.startswith('é com conector T.'):
            _n[_j] = 'é com conector T. No Alternativo A o TR4 ganha 0,45 m e um spot: a cozinha cresce para o sul.'
        if 'coifa 8,9 × 2,62' in _ln:
            _n[_j] = _ln.replace('coifa 8,9 × 2,62 × 12 = 279,8', 'coifa 9,82 × 2,62 × 12 = 308,7')


def construir_teto():
    ROTULO_ALT.clear()
    ROTULO_ALT.update({'cozinha': (277.0, 352.0)})
    d = p04.construir()
    d.set_plan(70, 156, 70.0)
    realce_parede(d)
    return d


# ---- Prancha 06 — elétrica ------------------------------------------------
for _n in p05.NOTAS:
    if _n[0].startswith('**Os pontos T01 a T09'):
        _n.append('No Alternativo A nenhum ponto muda; T12 só ganha folga até a parede nova (de ~0,15 para ~0,60 m).')


def construir_eletrica():
    ROTULO_ALT.clear()
    d = p05.construir()
    d.set_plan(70, 156, 70.0)
    realce_parede(d)
    return d


# ---- Prancha 09 — medição -------------------------------------------------
_subst(p09.TAB_AMB, 'Cozinha', ('Cozinha', '9,82', '25,46', '25,73'))
_subst(p09.TAB_AMB, 'Closet', ('Closet', '4,38', '12,74', '11,48'))
p09.TAB_DEC.insert(0, ('Parede coz./closet', 'Alternativo A', '0,45 m ao sul · cozinha 9,82 · closet 4,38 m² · E03 antes'))

# ---- Prancha 11 — ar e luz ------------------------------------------------
_subst(p11.TAB_TERM, 'Social + cozinha', ('Social + cozinha', '38,72', '23.232', '30.976', 'sala de TV, sala de estar, cozinha e circulação'))
_subst(p11.TAB_TERM, 'Quarto + closet', ('Quarto + closet', '17,78', '10.668', '14.224', 'zona de dormir'))
_subst(p11.TAB_EXA, 'CF01', ('CF01', 'Cozinha isolada — hipótese', '9,82 × 2,62 = 25,73 m³', '× 12', '308,7 m³/h'))
_subst(p11.TAB_LUZ, 'Cozinha', ('Cozinha', '9,82', '300 lux', '6.138 lm', '3.000 K', 'bancada à parte, 500 lux'))
_subst(p11.TAB_LUZ, 'Closet', ('Closet', '4,38', '200 lux', '1.825 lm', '3.000 K', 'luz vertical das roupas'))
for _n in p11.NOTAS:
    for _j, _ln in enumerate(_n):
        _n[_j] = _ln.replace('279,8 m³/h', '308,7 m³/h')

# ---- Prancha 12 — riscos --------------------------------------------------
_i = [r[0] for r in p12.RISCOS].index('E5') + 1
p12.RISCOS[_i:_i] = [
    ('E6', 'Estrutura', 'Paredes cozinha/closet sem projeto estrutural — E03 antes de D09/D10',
     'impasse'),
]
_i = [r[0] for r in p12.RISCOS].index('H4') + 1
p12.RISCOS[_i:_i] = [
    ('H5', 'Hidráulica', 'Tubulação ou gás embutido no trecho da parede antiga (D10)', 'medio'),
]
_i = [r[0] for r in p12.RISCOS].index('A3') + 1
p12.RISCOS[_i:_i] = [
    ('M1', 'Marcenaria', 'Closet 0,45 m mais raso — módulos novos, não os mesmos remontados', 'alto'),
    ('M2', 'Acesso', 'Entrada do closet pelo vão do quarto — confirmar antes de fechar R04', 'medio'),
]
p12.IMPASSES.insert(1, ('E6', 'IMPASSE', 'As paredes da cozinha e do closet',
                        'pedir confirmação ao engenheiro antes de demolir',
                        ['Nenhum projeto estrutural do edifício foi disponibilizado. As duas paredes',
                         'leem como vedação de 0,10 m, sem viga ou pilar aparente no scan — mas o',
                         'scan não enxerga o que está dentro da parede.',
                         'PORTÃO: ensaio E03 (percussão e inspeção do entorno) antes de D09 e D10.']))
for _imp in p12.IMPASSES:
    for _j, _ln in enumerate(_imp[4]):
        _imp[4][_j] = _ln.replace('279,8 m³/h', '308,7 m³/h')
p12.RESOLVIDOS[:] = [r for r in p12.RESOLVIDOS if r[0] != 'D2']
p12.NOTAS[:] = [list(n) for n in p12.NOTAS if not n[0].startswith('**Juntas')]
for _n in p12.NOTAS:
    for _j, _ln in enumerate(_n):
        if _ln.startswith('projetos do edifício. Os ensaios E01 e E02'):
            _n[_j] = 'projetos do edifício. Os ensaios E01, E02 e E03 respondem instalações e paredes; a laje, a'


def construir_riscos():
    d = p12.construir()
    trocar(d, '23 pontos  ·  1 impasse aberto', '%d pontos  ·  2 impasses abertos' % len(p12.RISCOS))
    trocar(d, 'Um impasse aberto e dois em curso, já com dono.', 'Dois impasses abertos e dois em curso, já com dono.')
    trocar(d, 'Nenhum se resolve no desenho: os três pedem campo.', 'Nenhum se resolve no desenho: os quatro pedem campo.')
    return d


# ---- Prancha 13 — quarto adaptável: a cama não é desenhada ----------------
_o, _lc, _p = qa.folgas(qa.CASAL[1], qa.CASAL[2])
_SEM_COTA = {br(_o), br(_lc), br(_p)}


def _sem_cama(*a, **k):
    return None


def _ch13(d, x0, x1, y, off, texto=None, *a, **k):
    if texto in _SEM_COTA:
        return None
    return bm.cota_h(d, x0, x1, y, off, texto, *a, **k)


def _cv13(d, y0, y1, x, off, texto=None, *a, **k):
    if texto in _SEM_COTA:
        return None
    return bm.cota_v(d, y0, y1, x, off, texto, *a, **k)


def construir_quarto():
    orig = qa.desenhar_cama
    qa.desenhar_cama = _sem_cama
    p13.cota_h, p13.cota_v = _ch13, _cv13
    try:
        d = p13.construir()
    finally:
        qa.desenhar_cama = orig
        p13.cota_h, p13.cota_v = bm.cota_h, bm.cota_v
    trocar(d, '1,38 × 1,88 m', '')
    return d


# ---- Prancha 14 / FO8 — programação --------------------------------------
def _celula(nome_ini, fase, texto):
    for nome, _f, cel in pg.LINHAS:
        if nome.startswith(nome_ini):
            cel[fase] = texto
            return
    raise KeyError(nome_ini)


_celula('Empreiteira', 1, 'proteção · ensaios E01, E02 e E03')
_celula('Empreiteira', 2, 'forro, pisos, banheiro e D09/D10')
_celula('Empreiteira', 5, 'R01 · R02 · forro R03 · parede R04')
_celula('Marcenaria', 8, 'closet com módulos novos')
_celula('Marcenaria', 2, 'desmontar M01 · medir o closet novo')
pg.MARCOS[0] = (2, ['Laudos E01/E02 e E03:', 'instalações e paredes', 'cozinha/closet'])


# ---------------------------------------------------------------------------
# FORNECEDORES — FO1 a FO8
# ---------------------------------------------------------------------------
fo.EMISSAO = 'ALT. A  ·  EMISSÃO 02'
fo.ORIGEM = 'extraído do Caderno Alternativo A — REV. O'


def cabeca_fo_alt(d, titulo, disciplina, chamada):
    d.txt(MARGIN, 42, 'MAXHAUS 81I  ·  PACOTE PARA FORNECEDORES  ·  ALTERNATIVO A',
          10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(MARGIN, 78, titulo, 27.0, INK, 'bold')
    d.txt(MARGIN, 99, chamada, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, fo.EMISSAO, 10.0, RED, 'bold', 'end', ls=0.8)
    d.txt(W - MARGIN, 78, disciplina, 10.5, INK, 'bold', 'end')
    d.txt(W - MARGIN, 99, fo.ORIGEM, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)


fo.cabeca_fo = cabeca_fo_alt

# FO1
_t = fo.TAB_DEMO
_t.insert([r[0] for r in _t].index('M01'), ('E03', 'Ensaio estrutural das paredes cozinha/closet, com engenheiro', '2 paredes'))
_t.insert([r[0] for r in _t].index('D08'), ('D09', 'Demolir parede interna do closet — somente após E03', '2,54 m'))
_t.insert([r[0] for r in _t].index('D08'), ('D10', 'Demolir parede cozinha/closet — somente após E03', '1,45 m'))
_t.insert([r[0] for r in _t].index('K01'), ('R04', 'Parede nova cozinha/closet, na face sul do banheiro até a oeste', '2,17 m'))
_subst(_t, 'M01', ('M01', 'Desmontar closet, etiquetar e acondicionar — volta com módulos novos', '1 conjunto'))
fo.SEQ_DEMO[0] = ('1', ['Ensaios antes de qualquer demolição — E01, E02 e E03.',
                        'Resultado por escrito. Sem laudo do E03, D09 e D10 não saem.'], True)
fo.SEQ_DEMO[4] = ('5', ['Vedações — D01, D02, D06, D04, D09 e D10.',
                        'Abrir D10 com cautela: confirmar hidráulica ou gás embutido no trecho.'], False)
fo.SEQ_DEMO[8] = ('9', ['Reconstruções — R01, R02, R03 e R04.',
                        'Marcar R04 antes de levantar: face sul do banheiro, em esquadro com a oeste.',
                        'R01 e R03 fecham só depois da infraestrutura embutida.'], True)


def folha_demolicao_alt():
    geometria(False)
    tab = fo.tabela

    def compacta(d, x, y, w, cols, linhas, titulo=None, alt=None):
        return tab(d, x, y, w, cols, linhas, titulo=titulo, alt=15.4)
    fo.tabela = compacta
    try:
        d = fo.folha_demolicao()
        for r in (WALL_REMOVER_1, WALL_REMOVER_2):
            x, y, w_, h_ = d.R(r)
            d.rect(x, y, w_, h_, fill='none', stroke=DEMO, sw=1.4)
        x, y, w_, h_ = d.R(WALL_NOVA)
        d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.3, dash='4 3')
        realce_r01(d)
    finally:
        fo.tabela = tab
        geometria(True)
    return d


# FO2
fo.SEQ_PISO[-1] = ('7', ['Liberação para marcenaria.',
                         'Closet somente após a cura — e com módulos novos: nesta proposta o',
                         'closet fica 0,45 m mais raso, os módulos antigos não voltam iguais.'], False)

# FO4
_subst(fo.TAB_LUZ_FO, 'TR4', ('TR4', 'Trilho eletrificado — cozinha, eixo 1,45 m, até 6,85 m', '2,95 m  ·  5 spots'))
_subst(fo.TAB_LUZ_FO, '—', ('—', 'Total de trilho e de spots nos seis trechos', '16,25 m  ·  22 spots'))
_subst(fo.TAB_LUX, 'Cozinha', ('Cozinha', '300 lux', '6.138 lm', '3.000 K'))
_subst(fo.TAB_LUX, 'Closet', ('Closet', '200 lux', '1.825 lm', '3.000 K'))

# FO5
_subst(fo.TAB_AR_FO, 'AC01', ('AC01', 'Evaporadora — social + cozinha (38,72 m²)', '1 unidade'))
_subst(fo.TAB_AR_FO, 'AC02', ('AC02', 'Evaporadora — quarto + closet (17,78 m²)', '1 unidade'))
_subst(fo.TAB_BTU, 'Social + cozinha', ('Social + cozinha', '38,72 m²', '23.232 BTU/h', '30.976 BTU/h'))
_subst(fo.TAB_BTU, 'Quarto + closet', ('Quarto + closet', '17,78 m²', '10.668 BTU/h', '14.224 BTU/h'))
_subst(fo.TAB_VAZAO, 'CF01', ('CF01', 'Cozinha — 9,82 m² × 2,62 m × 12 trocas/h', '308,7 m³/h'))
fo.SEQ_AR[1] = (fo.SEQ_AR[1][0], [fo.SEQ_AR[1][1][0].replace('30.240 e 14.960', '30.976 e 14.224')]
                + list(fo.SEQ_AR[1][1][1:]), fo.SEQ_AR[1][2])

# FO7 — a cozinha vai até a parede nova: KC1 cresce 0,45 m
fo.COZ_SUL = KC_SUL
fo.KC1 = (fo.COZ_OESTE, fo.COZ_NORTE + fo.NICHO_GEL, fo.COZ_OESTE + 0.60, fo.COZ_SUL)
_subst(fo.TAB_PEDRA, 'KC1', ('KC1', 'Bancada da cozinha, parede oeste, do nicho da geladeira à parede nova R04 — pedra 2 cm',
                             '%s × 0,60 m' % br(fo._ln(fo.KC1))))
_subst(fo.TAB_PEDRA, 'KC1f', ('KC1f', 'Frontão 10 cm na parede oeste e na lateral da geladeira',
                              '~%s m' % br(fo._ln(fo.KC1) + 0.60)))


# ---------------------------------------------------------------------------
# R01 0,17 m ao norte — números de sala de TV e quarto
#   sala de TV 23,00 → 22,32 m² · quarto 13,40 → 14,08 m² (Δ 0,17 × 3,98 m)
#   perímetro ∓0,34 m · parede ∓0,82 m² · volume × 2,62 · lm = área × 150 / 0,48
#   social + cozinha 38,04 m² · quarto + closet 18,46 m² (600 e 800 BTU/h·m²)
# ---------------------------------------------------------------------------
_subst(p01.TAB_AMB, 'Sala de TV', ('Sala de TV', '22,32 m²', '20,4 m', '5,6 × 4,6', '4,8 × 3,8'))
_subst(p01.TAB_AMB, 'Quarto', ('Quarto', '14,08 m²', '16,5 m', '5,6 × 2,7', '5,6 × 2,3'))
p01.NOTAS.insert(1, [
    '**Alternativo A: a drywall sala de TV/quarto (R01) volta 0,17 m mais ao norte.',
    'O quarto passa de 2,54 para 2,71 m livres (de 13,40 para 14,08 m²) e a sala de TV de 23,00 para',
    '22,32 m². A porta de correr P03 acompanha a parede; o comprimento da drywall não muda.'])
p02.ALVOS[:] = [(a[0], a[1], Y_R01, *a[3:]) if a[0] == 'R01' else a for a in p02.ALVOS]
_subst(p02.LINHAS, 'R01', ('R01', 'Nova drywall sala de TV/quarto, 0,17 m ao norte, com porta de correr',
                          '4,08 m + 1 porta'))
for _n in p02.NOTAS:
    for _j, _ln in enumerate(_n):
        if _ln.startswith('A drywall entre sala de TV e quarto cai e volta (R01)'):
            _n[_j] = 'A drywall sala de TV/quarto cai e volta 0,17 m ao norte (R01), com porta de correr de 1,00 × 2,29 m; a folha'
_subst(p03.TAB_A, 'Cumaru-ferro',
       ('Cumaru-ferro', 'sala de TV 22,32 + quarto 14,08 + sala de estar 5,90 + corredor 2,39', '44,69 m²'))
_subst(p04.TAB_LUZ, 'Sala de TV', ('Sala de TV', '150 lux', '6.975 lm', '2.700 K'))
_subst(p04.TAB_LUZ, 'Quarto', ('Quarto', '150 lux', '4.400 lm', '2.700 K'))
_subst(p04.TAB_AR, 'Social + cozinha', ('Social + cozinha', '38,04 m²', '22.824 BTU/h', '30.432 BTU/h'))
_subst(p04.TAB_AR, 'Quarto + closet', ('Quarto + closet', '18,46 m²', '11.076 BTU/h', '14.768 BTU/h'))
_subst(p05.COMANDOS, 'S05', ('S05', 4.90, 6.98 - 0.17))      # acompanha a face do quarto
_subst(p09.TAB_AMB, 'Sala de TV', ('Sala de TV', '22,32', '28,98', '58,48'))
_subst(p09.TAB_AMB, 'Quarto', ('Quarto', '14,08', '31,12', '36,89'))
p09.TAB_DEC.insert(1, ('Drywall R01', 'Alternativo A', '0,17 m ao norte · quarto 2,71 m livres · 14,08 m²'))
_subst(p11.TAB_TERM, 'Social + cozinha', ('Social + cozinha', '38,04', '22.824', '30.432', 'sala de TV, sala de estar, cozinha e circulação'))
_subst(p11.TAB_TERM, 'Quarto + closet', ('Quarto + closet', '18,46', '11.076', '14.768', 'zona de dormir'))
_subst(p11.TAB_LUZ, 'Sala de TV', ('Sala de TV', '22,32', '150 lux', '6.975 lm', '2.700 K', 'leitura e cenas dimerizáveis'))
_subst(p11.TAB_LUZ, 'Quarto', ('Quarto', '14,08', '150 lux', '4.400 lm', '2.700 K', 'cabeceira independente'))
_subst(fo.TAB_DEMO, 'R01', ('R01', 'Reconstruir drywall sala de TV/quarto 0,17 m ao norte, com vão de porta 1,00 × 2,29 m',
                            '4,08 m + 1 vão'))
_subst(fo.TAB_LUX, 'Sala de TV', ('Sala de TV', '150 lux', '6.975 lm', '2.700 K'))
_subst(fo.TAB_LUX, 'Quarto', ('Quarto', '150 lux', '4.400 lm', '2.700 K'))
_subst(fo.TAB_AR_FO, 'AC01', ('AC01', 'Evaporadora — social + cozinha (38,04 m²)', '1 unidade'))
_subst(fo.TAB_AR_FO, 'AC02', ('AC02', 'Evaporadora — quarto + closet (18,46 m²)', '1 unidade'))
_subst(fo.TAB_BTU, 'Social + cozinha', ('Social + cozinha', '38,04 m²', '22.824 BTU/h', '30.432 BTU/h'))
_subst(fo.TAB_BTU, 'Quarto + closet', ('Quarto + closet', '18,46 m²', '11.076 BTU/h', '14.768 BTU/h'))
fo.SEQ_AR[1] = (fo.SEQ_AR[1][0], [fo.SEQ_AR[1][1][0].replace('30.976 e 14.224', '30.432 e 14.768')]
                + list(fo.SEQ_AR[1][1][1:]), fo.SEQ_AR[1][2])

# ---------------------------------------------------------------------------
# PISO — inversão de materiais (12.11.2026)
#   onde era cumaru-ferro entra monolítico; onde era monolítico entra porcelanato.
#   Opção A: monolítico 44,69 m² (sala de TV, quarto, sala de estar, corredor)
#            + porcelanato 11,81 m² (cozinha 7,43 + closet 4,38), reserva de 10%.
#   Opção B (monolítico integral) não muda.
# ---------------------------------------------------------------------------
PORC = BRANCO
PORC_PASSO = 0.60          # grade ilustrativa — formato a definir


def piso_porcelanato(d, poly_pt, passo=PORC_PASSO, cor=K45, op=0.55, sw=0.45):
    pp = [d.P(a, b) for a, b in poly_pt]
    d.path(path_d(pp), fill=PORC)
    ox, oy = d.org
    S = d.S
    x0, y0, x1, y1 = bbox(pp)
    i = int((x0 - ox) // (passo * S))
    while ox + i * passo * S <= x1:
        xx = ox + i * passo * S
        for (a, b) in spans_at_x(pp, xx):
            d.line(xx, a, xx, b, cor, sw, opacity=op)
        i += 1
    j = int((y0 - oy) // (passo * S))
    while oy + j * passo * S <= y1:
        yy = oy + j * passo * S
        for (a, b) in spans_at_y(pp, yy):
            d.line(a, yy, b, yy, cor, sw, opacity=op)
        j += 1


_PORC_WC = [False]


def _mono_no_lugar_do_cumaru(d, poly_pt, **k):
    """Substitui as réguas de cumaru: o pano vira monolítico, e quando chega o
    corredor (último pano) a zona cozinha + closet já sai em porcelanato."""
    d.path(path_d([d.P(a, b) for a, b in poly_pt]), fill=K07)
    if poly_pt is HALL_A_POLY:
        piso_porcelanato(d, MONO_A_POLY)
        if _PORC_WC[0]:
            piso_porcelanato(d, bm.ROOMS['banheiro']['poly'])


_LEG_PISO = {
    'Cumaru-ferro — piso pronto em réguas': ('fill', K07, 'Monolítico — sala de TV, quarto, sala de estar e corredor'),
    'Piso monolítico — cozinha e closet': ('fill', PORC, 'Porcelanato — cozinha e closet (grade ilustrativa)'),
    'Cumaru-ferro em réguas': ('fill', K07, 'Monolítico'),
    'Monolítico': ('fill', PORC, 'Porcelanato — grade ilustrativa'),
}


def _legenda_piso(orig):
    def f(d, itens, *a, **k):
        return orig(d, [_LEG_PISO.get(t, (tp, c, t)) for (tp, c, t) in itens], *a, **k)
    return f


p03.legenda = _legenda_piso(p03.legenda)
fo.legenda = _legenda_piso(fo.legenda)

p03.TAB_A[:] = [
    ('Monolítico',        'sala de TV 22,32 + quarto 14,08 + sala de estar 5,90 + corredor 2,39', '44,69 m²'),
    ('Sem reserva',       'moldado in loco, sem perda de corte',                     '—'),
    ('Porcelanato',       'cozinha 7,43 (de 9,82) + closet 4,38 — zona contínua',     '11,81 m²'),
    ('+ reserva de 10%',  'cortes, perdas e reposição futura',                       '12,99 m²'),
    ('Banheiro',          'sistema à parte, área molhada, na mesma cota',             '3,80 m²'),
    ('MainFloor',         'total do pavimento',                                      '60,30 m²'),
]
p03.NOTAS_A[:] = [
    ['**Alternativo A: os dois materiais trocam de lugar.',
     'Onde era cumaru-ferro — sala de TV, quarto, sala de estar e corredor — entra o monolítico; onde',
     'era monolítico — cozinha e closet — entra porcelanato. O contorno da zona e a ponta arredondada',
     'não mudam.'],
    ['**O monolítico agora é o pano grande: 44,69 m² pedem projeto de juntas.',
     'Cimentício trabalha em painéis de 3 a 6 m de lado; microcimento reduz as juntas às do substrato',
     'e ao perímetro. Lugares naturais: as soleiras da entrada e do banheiro, a linha da porta de',
     'correr P03 e o encontro com o porcelanato. Pedir a paginação de juntas junto com a proposta.'],
    ['**Porcelanato na cozinha e no closet: formato, cor e rejunte a definir.',
     'A grade de 0,60 m do desenho é ilustrativa. Juntas de assentamento e de movimentação conforme',
     'o fabricante e a NBR 13753; reserva de 10% para cortes e reposição.'],
    ['**Na ponta arredondada o monolítico acompanha e o porcelanato é cortado.',
     'Filete de 0,70 m de raio, canto reto nos demais trechos. O monolítico, moldado in loco, segue a',
     'curva sem esforço; do lado do porcelanato as peças são cortadas em curva (jato d\'água ou serra)',
     'e o perfil de transição curvo fica no encontro.'],
    ['**As duas espessuras se acertam no contrapiso, não na soleira.',
     'Porcelanato com argamassa colante e monolítico somam alturas diferentes: o acerto é no',
     'contrapiso (P06), para os dois se encontrarem rentes, sem degrau.'],
    ['**Sequência sugerida: porcelanato e perfil, depois o monolítico.',
     'O monolítico é aplicado contra o perfil de transição já fixado e cura antes da marcenaria: o',
     'closet (M01) só volta com o piso curado.'],
    p03.NOTAS_A[-1],
]
for _n in p03.NOTAS_B:
    if _n[0].startswith('**Sequência importa mais que no piso em réguas'):
        _n[0] = '**Sequência importa: o monolítico pede cura.'


def construir_piso(opcao):
    ROTULO_ALT.clear()
    ROTULO_ALT.update({'cozinha': (300.0, 392.0), 'closet': (300.0, 508.0)})
    A = (opcao == 'A')
    reguas, mono = p03.piso_reguas, p03.MONO
    if A:
        p03.piso_reguas, p03.MONO = _mono_no_lugar_do_cumaru, 'none'
    try:
        d = p03.construir(opcao)
    finally:
        p03.piso_reguas, p03.MONO = reguas, mono
    if A:
        trocar(d, 'Opção A — cumaru-ferro, cozinha e closet em monolítico',
               'Opção A — monolítico, cozinha e closet em porcelanato')
        trocar(d, 'Piso pronto em réguas nas áreas de estar e dormir; cozinha e closet numa zona monolítica contínua. Cores e desenho de régua ilustrativos.',
               'Monolítico nas áreas de estar e dormir; cozinha e closet numa zona contínua de porcelanato. Cores e paginação ilustrativas.')
    d.set_plan(70, 156, 70.0)
    realce_parede(d)
    return d


# FO2
fo.TAB_PISO_A[:] = [
    ('A1', 'Piso monolítico — sala de TV, quarto, sala de estar e corredor; juntas conforme projeto', '44,69 m²'),
    ('A2', 'Porcelanato — zona contínua cozinha + closet (formato a definir)', '11,81 m²'),
    ('A3', 'Reserva de 10% sobre A2 — cortes, perdas e reposição', '1,18 m²'),
    ('A4', 'Perfil de transição com junta de movimentação, rente nos dois lados', 'a medir em obra'),
    ('A5', 'Ponta arredondada: porcelanato cortado em curva, filete de 0,70 m de raio', '1 trecho'),
]
fo.SEQ_PISO[3] = ('4', ['Aplicação — A ou B, conforme opção contratada.',
                        'A: porcelanato e perfil de transição, depois o monolítico (A1 a A5).',
                        'B: aplicação monolítica contínua com juntas (B1 a B3).'], False)
_planta_piso_orig = fo._planta_piso


def _planta_piso_alt(d, ox, oy, S, opcao, titulo):
    if opcao != 'A':
        return _planta_piso_orig(d, ox, oy, S, opcao, titulo)
    reguas, mono = fo.piso_reguas, fo.MONO
    fo.piso_reguas, fo.MONO = _mono_no_lugar_do_cumaru, 'none'
    try:
        return _planta_piso_orig(d, ox, oy, S, opcao, 'OPÇÃO A  ·  monolítico + porcelanato')
    finally:
        fo.piso_reguas, fo.MONO = reguas, mono


fo._planta_piso = _planta_piso_alt


def folha_piso_alt():
    d = fo.folha_piso()
    trocar(d, 'OPÇÃO A — CUMARU-FERRO COM COZINHA E CLOSET EM MONOLÍTICO',
           'OPÇÃO A — MONOLÍTICO COM COZINHA E CLOSET EM PORCELANATO')
    return d


# riscos, medição e programação
_subst(p12.RISCOS, 'A1', ('A1', 'Acabamento', 'Monolítico de 44,69 a 56,50 m² pede juntas — quantas depende do sistema', 'alto'))
_subst(p12.RISCOS, 'A2', ('A2', 'Acabamento', 'Porcelanato e monolítico rentes: espessuras diferentes, acerto no contrapiso', 'medio'))
_subst(p09.TAB_DEC, 'Piso', ('Piso', 'Duas opções vivas', 'A monolítico + porcelanato · B monolítico integral'))
_celula('Piso da casa', 6, 'opção A (monolítico + porcelanato) ou B (monolítico)')


# ---------------------------------------------------------------------------
# ILUMINAÇÃO — o projeto é da FAS (12.11.2026)
#   trilhos, spots, destaques e fluxos do caderno ficam como referência de
#   posição; valem o projeto, as quantidades e os modelos da FAS. O caderno
#   garante as esperas de alimentação e a zona sem furação da claraboia.
# ---------------------------------------------------------------------------
for _i, _n in enumerate(p04.NOTAS):
    if _n[0].startswith('**Traçado dos trilhos revisado'):
        p04.NOTAS[_i] = [
            '**Projeto de iluminação: FAS.',
            'Trilhos, spots, destaques e fluxos desta folha são referência do estudo, não especificação:',
            'valem o projeto, as quantidades e os modelos da FAS. O caderno garante só as esperas de',
            'alimentação (AL1 a AL3) e a zona sem furação da claraboia — conferir as duas contra o projeto.']
for _n in p11.NOTAS:
    if _n[0].startswith('**Fluxo = área × iluminância'):
        _n[0] = '**Iluminação: o projeto é da FAS — esta conta é só referência.'
        _n.insert(1, 'Fluxo = área × iluminância ÷ (utilização × manutenção).')
_luz = pg.LINHAS[[l[0] for l in pg.LINHAS].index('Iluminação')]
pg.LINHAS[pg.LINHAS.index(_luz)] = ('Iluminação — projeto FAS', _luz[1], {**_luz[2], 4: 'projeto FAS e esperas'})
pg.MARCOS[:] = [(f, ['Luminárias (FAS),', 'tecido da cortina', 'e louças']) if f == 8 else (f, l) for f, l in pg.MARCOS]
_subst(fo.TAB_ELE, 'AL1', ('AL1', 'Alimentação de trilho no teto — posição do projeto FAS (ver FO4)', '6 pontos'))
fo.SEQ_LUZ[0] = ('1', ['Projeto de iluminação da FAS recebido e compatibilizado.',
                       'Trilhos, spots e fluxos desta folha são referência: valem os da FAS.',
                       'Conferir as alimentações AL1 a AL3 (FO3) contra o projeto antes de comprar.'], True)


def construir_teto_fas():
    d = construir_teto()
    trocar(d, 'Distribuição conceitual sobre a laje de concreto. Reservas de posição, não quantidade final de luminárias nem de equipamentos.',
           'Distribuição conceitual sobre a laje de concreto. Iluminação: projeto da FAS — trilhos e luminárias aqui são só reserva de posição.')
    trocar(d, 'ILUMINAÇÃO POR AMBIENTE', 'ILUMINAÇÃO POR AMBIENTE — REFERÊNCIA; VALE O PROJETO FAS')
    return d


def construir_11_fas():
    d = p11.construir()
    trocar(d, 'ILUMINAÇÃO — ALVO POR AMBIENTE', 'ILUMINAÇÃO — ALVO POR AMBIENTE (REFERÊNCIA; VALE O PROJETO FAS)')
    return d


def folha_iluminacao_fas():
    d = fo.folha_iluminacao()
    trocar(d, 'Trilho eletrificado e luminárias sobre a laje aparente. A alimentação é entregue pela elétrica (FO3): aqui é montagem, não fiação.',
           'Projeto de iluminação: FAS. Trilhos e luminárias desta folha são só referência de posição; a alimentação é da elétrica (FO3).')
    trocar(d, 'ESCOPO — TAREFA E QUANTIDADE', 'REFERÊNCIA DO ESTUDO — VALEM QUANTIDADES E MODELOS DO PROJETO FAS')
    trocar(d, 'ALVO POR AMBIENTE — PARA SELEÇÃO DE SPOT', 'ALVO POR AMBIENTE — REFERÊNCIA; VALE O PROJETO FAS')
    return d


# ---------------------------------------------------------------------------
# REV. R (12.11.2026) — incorpora as áreas técnicas da REV. Q (22.10.2026)
#   AT-B  shaft do banho/chuveiro na parede oeste do banheiro (a da bancada),
#         ao longo do box: 0,93 × 0,15 m, profundidade estimada. Prumada.
#   AT-A  aquecedor a gás no closet: nicho ~0,60 × 0,40 m piso-laje na parede
#         de divisa, alinhado ao D09; chaminé sob a laje até a bandeira da J06.
#         Posição no comprimento da parede é esquemática (norte do closet).
#   Áreas líquidas: closet 4,14 m² (4,38 − 0,24), banheiro 3,66 m² (3,80 − 0,14).
# ---------------------------------------------------------------------------
REV_ALT = 'ALT. A  ·  REV. R'
bm.DATA_EMISSAO = '12/11/2026'
fo.DATA = '12.11.2026'
fo.EMISSAO = 'ALT. A  ·  EMISSÃO 04'
fo.ORIGEM = 'extraído do Caderno Alternativo A — REV. R'

AT_B = (347.96, 408.20, 347.96 + 0.15 * PT_PER_M, 450.67)
_XO = 250.26                                    # face interna da parede de divisa
AT_A = (_XO, 455.24, _XO + 0.60 * PT_PER_M, 455.24 + 0.40 * PT_PER_M)
X_CHAMINE = (AT_A[0] + AT_A[2]) / 2.0

AT_TXT = ('AT-B · área técnica do banho/chuveiro: na parede oeste do banheiro (a mesma da bancada), ao longo '
          'de todo o box; 0,93 × 0,15 m. Profundidade estimada (0,15 m, planta original do proprietário) — '
          'confirmar em campo depois do D04. Prumada do condomínio: não demolir. AT-A · aquecimento: '
          'aquecedor a gás no closet, nicho ~0,60 × 0,40 m piso-laje na parede de divisa, alinhado ao D09; '
          'chaminé sob a laje até a bandeira da J06 (posição no comprimento da parede esquemática). '
          'NBR 13103: o closet (~11–14 m³) fica abaixo do volume de referência — nicho fechado em material '
          'incombustível, ventilação permanente para o exterior e chaminé própria. Liberação obrigatória por '
          'instalador credenciado / Comgás antes da infraestrutura. Áreas líquidas com as áreas técnicas: '
          'closet 4,14 m² (era 4,38), banheiro 3,66 m² (−0,14 m² do shaft).')
AT_CURTO = ('AT-B shaft do banho (parede da bancada, todo o box, 0,93 × 0,15 m, estimado) e AT-A aquecedor '
            'no closet (nicho ~0,60 × 0,40 m, NBR 13103 a liberar) — detalhes na Prancha 01 e riscos H6/H7 '
            'na Prancha 12.')
AT_TITULO = 'ÁREAS TÉCNICAS · DA REV. Q (22/10/2026)'


def _quebra(texto, largura, size):
    por_linha = max(20, int(largura / (size * 0.46)))
    linhas, atual = [], ''
    for p in texto.split():
        if atual and len(atual) + 1 + len(p) > por_linha:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + ' ' + p) if atual else p
    if atual:
        linhas.append(atual)
    return linhas


def nota_at(d, x, y, w, texto=AT_CURTO, extra=None, titulo=AT_TITULO, size=7.4, lh=10.2):
    if w < 150 and titulo == AT_TITULO:
        titulo = 'ÁREAS TÉCNICAS · REV. Q'
    corpo = _quebra(texto, w - 16, size)
    if extra:
        corpo += _quebra(extra, w - 16, size)
    h = 22 + len(corpo) * lh + 4
    d.rect(x, y, w, h, fill=BG, stroke=DEMO, sw=0.9)
    d.txt(x + 8, y + 14, titulo, size, DEMO, 'bold', ls=0.4)
    for i, ln in enumerate(corpo):
        d.txt(x + 8, y + 26 + i * lh, ln, size, INK_SOFT)
    return y + h


def desenhar_at(d, size=6.4, rotulos=True, chamine=True, so_b=False):
    x, y, w_, h_ = d.R(AT_B)
    d.rect(x, y, w_, h_, fill=K45, opacity=0.55)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=0.9)
    if rotulos:
        d.txt(x + w_ / 2.0 + 2.2, y + h_ / 2.0, 'AT-B', size, BRANCO, 'bold', 'middle', rot=-90)
    if so_b:
        return
    x, y, w_, h_ = d.R(AT_A)
    d.rect(x, y, w_, h_, fill=AMARELO, stroke=K, sw=1.0)
    d.txt(x + w_ / 2.0, y + h_ / 2.0 + size * 0.35, 'AQ', size, K, 'bold', 'middle')
    if chamine:
        tracejado(d, [(X_CHAMINE, AT_A[3]), (X_CHAMINE, 550.38)], stroke=DEMO, w=1.1,
                  dash=4.0, gap=3.0, halo=False)
    if rotulos:
        d.txt(x + w_ + 3, y + h_ / 2.0 + 2, 'AT-A aquecedor', size, K, 'bold', 'start')
        if chamine and size >= 5.8:
            m = d.P(X_CHAMINE, 515.0)
            d.txt(m[0] + 3, m[1], 'chaminé sob a laje', size - 0.4, DEMO, 'normal', 'start')
            d.txt(m[0] + 3, m[1] + size + 1, 'até a bandeira da J06', size - 0.4, DEMO, 'normal', 'start')


# riscos H6 e H7
_i = [r[0] for r in p12.RISCOS].index('H5') + 1
p12.RISCOS[_i:_i] = [
    ('H6', 'Hidráulica', 'Shaft AT-B do banho: posição e medida estimadas — confirmar após a D04', 'alto'),
    ('H7', 'Gás', 'Aquecedor AT-A no closet só segue com laudo NBR 13103 do instalador credenciado', 'impasse'),
]

# áreas líquidas no piso: o porcelanato não corre sob o nicho AT-A
_subst(p03.TAB_A, 'Porcelanato', ('Porcelanato', 'cozinha 7,43 (de 9,82) + closet 4,14 líquidos (sem o AT-A)', '11,57 m²'))
_subst(p03.TAB_A, '+ reserva de 10%', ('+ reserva de 10%', 'cortes, perdas e reposição futura', '12,73 m²'))
_subst(p03.TAB_A, 'Banheiro', ('Banheiro', 'sistema à parte, na mesma cota — 3,66 líquidos sem o AT-B', '3,80 m²'))
_subst(fo.TAB_PISO_A, 'A2', ('A2', 'Porcelanato — cozinha + closet, sem o nicho AT-A (formato a definir)', '11,57 m²'))
_subst(fo.TAB_PISO_A, 'A3', ('A3', 'Reserva de 10% sobre A2 — cortes, perdas e reposição', '1,16 m²'))
pg.MARCOS[:] = [(4, ['Engenheiro (claraboia)', 'e laudo NBR 13103', 'do aquecedor AT-A']) if f == 4 else (f, l)
                for f, l in pg.MARCOS]


def construir_riscos_r():
    d = p12.construir()
    trocar(d, '23 pontos  ·  1 impasse aberto', '%d pontos  ·  3 impasses abertos' % len(p12.RISCOS))
    trocar(d, 'Um impasse aberto e dois em curso, já com dono.', 'Três impasses abertos e dois em curso, já com dono.')
    trocar(d, 'Nenhum se resolve no desenho: os três pedem campo.', 'Nenhum se resolve no desenho: os cinco pedem campo.')
    if not any(r[0] == 'D1' for r in p12.RISCOS):
        trocar(d, '2 em curso  ·  4 resolvidos até 30.09', '2 em curso  ·  2 resolvidos até 30.09')
    return d


def _com_at(fn, caixa, plano=None, texto=AT_CURTO, extra=None, desenho=True):
    """Envolve uma folha: desenha AT-A/AT-B no plano dado e põe a nota."""
    def f():
        d = fn()
        if desenho:
            for pl in (plano if isinstance(plano, list) else [plano]):
                if pl:
                    d.set_plan(*pl[:3])
                    desenhar_at(d, size=pl[3] if len(pl) > 3 else 6.4, so_b=(len(pl) > 4 and pl[4]))
        if caixa:
            x, y, w = caixa[:3]
            sz = caixa[3] if len(caixa) > 3 else 7.4
            nota_at(d, x, y, w, texto=texto, extra=extra, size=sz, lh=sz * 1.38)
        return d
    return f


def _plano_wc(ox, oy, S):
    return (ox - mx(p07.WC_OE) * S, oy - my(p07.WC_NE) * S, S)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# REV. S (12.11.2026) — correções do cliente
#   · P02 (banheiro) abre para fora em sentido anti-horário: dobradiça no
#     batente norte; por dentro empurra com a direita, por fora puxa com a esquerda
#   · piso em duas propostas: A monolítico integral (com banheiro e box);
#     B porcelanato acetinado no banheiro/box e na cozinha/closet + monolítico
#   · T20: ponto de energia novo acima do vaso sanitário
#   · CT01: 5,72 m de trilho de ponta a ponta, em destaque
# ---------------------------------------------------------------------------
REV_ALT = 'ALT. A  ·  REV. S'
fo.EMISSAO = 'ALT. A  ·  EMISSÃO 05'
fo.ORIGEM = 'extraído do Caderno Alternativo A — REV. S'

# P02 — giro anti-horário (dobradiça norte, folha para fora)
bm.DOOR_BANHO['hinge'] = 'n'
for _i, _e in enumerate(bm.ESQUADRIAS):
    if _e[0] == 'P02':
        bm.ESQUADRIAS[_i] = _e[:6] + ('de abrir — anti-horário, para fora',)
_subst(fo.TAB_PORTAS, 'P02', ('P02', 'Banheiro — folha existente, abre para fora em sentido anti-horário', '0,80 × 2,00 m'))
_subst(fo.TAB_PORTAS, 'P02a', ('P02a', 'Dobradiças no batente norte; fechadura ao sul — empurra com a direita, puxa com a esquerda', '1 conjunto'))
_subst(p07.TAB_RECON_WC, 'P02', ('P02', 'Porta 0,80 × 2,00 m, de abrir para fora — anti-horário, dobradiça norte', '1 vão'))
_subst(p09.TAB_DEC, 'Porta P02', ('Porta P02', 'Anti-horário', 'abre para fora, dobradiça norte; vidro do box em A ou B (FO7)'))
p07.NOTAS[-1] = [
    '**P02 abre para fora, anti-horário (REV. S): dobradiça no batente norte.',
    'Por dentro empurra com a direita; por fora puxa com a esquerda. S04/S08 ficam do lado da dobradiça.']

# T20 — ponto de energia acima do vaso (eixo do vaso a 0,98 m da parede da bancada)
p05.TOMADAS_NOVAS.append(('T20', 3.20, 4.76, 'acima do vaso'))
_subst(p05.LINHAS, 'Tomadas novas', ('Tomadas novas', '11 reservas — T10 a T20', 'não é número normativo nem total final'))
_subst(p05.LINHAS, 'Banheiro', ('Banheiro', 'lavatório (T17) e T20 novo acima do vaso', 'volumes de proteção, DR e cargas'))
_subst(fo.TAB_ELE, 'T10–T19', ('T10–T20', 'Tomadas novas; T18 é espera no teto, T20 acima do vaso', '11 pontos'))
p07.TAB_INST_WC.append(('T20', 'Ponto de energia novo acima do vaso — 2P+T, circuito com DR', '1 ponto'))

# CT01 — de ponta a ponta
_subst(p13.TAB_TRILHO, 'Total do eixo CT01', ('TOTAL — de ponta a ponta', 'do canto noroeste à fachada', '%s m' % br(qa.TRILHO_M)))
_subst(fo.TAB_CORT, 'CT01', ('CT01', 'Trilho de ponta a ponta: descida %s + curva %s + reta %s m' % (
    br(qa.DESCIDA_M), br(qa.CURVA_M), br(qa.RETA_M)), '%s m' % br(qa.TRILHO_M)))


def construir_quarto_s():
    d = construir_quarto()
    trocar(d, '%s m² dentro da cortina  ·  claraboia não furável' % br(qa.AREA_QUARTO),
           'trilho CT01: %s m de ponta a ponta  ·  %s m² dentro da cortina' % (br(qa.TRILHO_M), br(qa.AREA_QUARTO)))
    d.set_plan(p13.OX - p13.X0_M * p13.S, p13.OY - p13.Y0_M * p13.S, p13.S)
    c = d.PM(qa.FACE_OESTE_JANTAR - 0.12, 0.45)
    d.txt(c[0], c[1] + 26, '%s m de trilho' % br(qa.TRILHO_M), 8.0, DEMO, 'bold', 'end')
    d.txt(c[0], c[1] + 37, 'de ponta a ponta', 7.2, DEMO, 'normal', 'end')
    return d


# PISO — duas propostas
#   A  monolítico integral: secos 56,26 (sem AT-A) + banheiro e box 3,66 (sem AT-B) = 59,92 m²
#   B  porcelanato acetinado: cozinha 7,43 + closet 4,14 + banheiro e box 3,66 = 15,23 m²
#      monolítico: sala de TV 22,32 + quarto 14,08 + sala de estar 5,90 + corredor 2,39 = 44,69 m²
p03.TAB_B[:] = [
    ('Monolítico',      'sala de TV, quarto, cozinha, sala de estar, closet e corredor (sem AT-A)', '56,26 m²'),
    ('Banheiro e box',  'mesmo monolítico, sistema para área molhada sobre impermeabilização (sem AT-B)', '3,66 m²'),
    ('Sem reserva',     'aplicação moldada in loco, sem perda de corte',                     '—'),
    ('MainFloor',       'total revestido, líquido das áreas técnicas',                      '59,92 m²'),
]
p03.TAB_A[:] = [
    ('Monolítico',        'sala de TV 22,32 + quarto 14,08 + sala de estar 5,90 + corredor 2,39', '44,69 m²'),
    ('Porcelanato',       'acetinado: cozinha 7,43 + closet 4,14 + banheiro e box 3,66 (líquidos)', '15,23 m²'),
    ('+ reserva de 10%',  'cortes, perdas e reposição futura do porcelanato',                 '16,75 m²'),
    ('MainFloor',         'total revestido, líquido das áreas técnicas',                      '59,92 m²'),
]
p03.NOTAS_B[:] = [
    ['**Opção A: um monolítico só, do hall ao fundo do box.',
     'Sem junta de material entre os ambientes: secos, banheiro e box no mesmo sistema. A única',
     'transição que sobra é a junta da soleira do banheiro, que separa o pano molhado do seco.'],
    ['**No banheiro e no box o monolítico tem de ser sistema de área molhada.',
     'Impermeabilização por baixo, subindo nas paredes do box; caimento até o ralo linear feito no',
     'contrapiso; selador resistente a água e acabamento antiderrapante no box. Pedir ao fornecedor',
     'o sistema e a garantia específicos para box — nem todo cimentício aceita água corrente.'],
    p03.NOTAS_B[1], p03.NOTAS_B[3],
    ['**A base manda no resultado — o monolítico copia o que está embaixo.',
     'Depois de retirar os pisos (D08), todo o contrapiso é lixado, regularizado e nivelado (P06).',
     'Cor, textura e espessura do desenho são ilustrativas: sistema e acabamento a especificar.'],
    ['**Sequência: o monolítico entra depois das paredes prontas e antes da marcenaria.',
     'No banheiro, impermeabilização e caimento antes; o closet (M01) só volta com o piso curado.'],
]
p03.NOTAS_A[:] = [
    ['**Opção B: porcelanato acetinado onde há água e gordura, monolítico no resto.',
     'Porcelanato no banheiro e no box e na zona contínua cozinha + closet; monolítico na sala de TV,',
     'no quarto, na sala de estar e no corredor. O contorno da zona e a ponta arredondada não mudam.'],
    ['**Acetinado no box: conferir o coeficiente de atrito molhado.',
     'Acabamento acetinado varia muito de fabricante para fabricante. No banheiro e no box, exigir na',
     'ficha técnica atrito dinâmico adequado a área molhada (≥ 0,4) — ou usar no box a versão',
     'antiderrapante da mesma linha. Formato, cor e rejunte a definir; a grade de 0,60 m é ilustrativa.'],
    p03.NOTAS_A[1], p03.NOTAS_A[3], p03.NOTAS_A[4], p03.NOTAS_A[5],
]
for _n in p03.NOTAS_A + p03.NOTAS_B:
    for _j, _ln in enumerate(_n):
        _n[_j] = _ln.replace('≥ ', 'mín. ')


def _wc_porcelanato(d, rect_pt, passo=8.0):
    piso_porcelanato(d, bm.ROOMS['banheiro']['poly'])


def construir_piso_s(opcao):
    """A = monolítico integral (desenho da antiga B, com o banheiro no monolítico);
    B = porcelanato + monolítico (desenho da antiga A, com o banheiro em porcelanato)."""
    ROTULO_ALT.clear()
    ROTULO_ALT.update({'cozinha': (300.0, 392.0), 'closet': (300.0, 508.0)})
    salvo = (p03.piso_reguas, p03.MONO, p03.WET, p03.hachura_wc)
    if opcao == 'A':
        p03.WET, p03.hachura_wc = K07, (lambda *a, **k: None)
        base = 'B'
    else:
        p03.piso_reguas, p03.MONO = _mono_no_lugar_do_cumaru, 'none'
        p03.WET, p03.hachura_wc = PORC, _wc_porcelanato
        base = 'A'
    try:
        d = p03.construir(base)
    finally:
        p03.piso_reguas, p03.MONO, p03.WET, p03.hachura_wc = salvo
    if opcao == 'A':
        trocar(d, 'Opção B — monolítico em todo o MainFloor', 'Opção A — monolítico em todo o MainFloor, banheiro incluído')
        trocar(d, 'Sistema único nos cinco ambientes secos, com o banheiro à parte. Cores ilustrativas; nenhum produto, espessura ou acabamento especificado.',
               'Um sistema só nos ambientes secos, no banheiro e no box. Cores ilustrativas; nenhum produto, espessura ou acabamento especificado.')
        trocar(d, 'norte 126°  ·  Prancha 04 de 14', 'norte 126°  ·  Prancha 03 de 14')
        trocar(d, 'piso contínuo — sem junta de material entre ambientes secos', 'piso contínuo — só a junta da soleira do banheiro')
        trocar(d, 'Alt A · Prancha 04 / 14   ·   %s' % REV_ALT, 'Alt A · Prancha 03 / 14   ·   %s' % REV_ALT)
    else:
        trocar(d, 'Opção A — cumaru-ferro, cozinha e closet em monolítico',
               'Opção B — porcelanato acetinado no banheiro, cozinha e closet')
        trocar(d, 'Piso pronto em réguas nas áreas de estar e dormir; cozinha e closet numa zona monolítica contínua. Cores e desenho de régua ilustrativos.',
               'Porcelanato acetinado no banheiro e box e na zona cozinha + closet; monolítico nas áreas de estar e dormir. Cores e paginação ilustrativas.')
        trocar(d, 'norte 126°  ·  Prancha 03 de 14', 'norte 126°  ·  Prancha 04 de 14')
        trocar(d, 'Alt A · Prancha 03 / 14   ·   %s' % REV_ALT, 'Alt A · Prancha 04 / 14   ·   %s' % REV_ALT)
    d.set_plan(70, 156, 70.0)
    realce_parede(d)
    return d


_LEG_PISO.update({
    'Piso monolítico contínuo': ('fill', K07, 'Monolítico contínuo — secos, banheiro e box'),
    'Banheiro — sistema à parte (área molhada)': None,
    'Soleira / junta de transição': ('dash', JOINT, 'Junta na soleira do banheiro'),
    'Piso monolítico — cozinha e closet': ('fill', PORC, 'Porcelanato acetinado — banheiro, box, cozinha e closet'),
    'Banheiro — sistema à parte': None,
    'Monolítico': ('fill', PORC, 'Porcelanato acetinado — grade ilustrativa'),
})


def _legenda_piso_s(orig):
    def f(d, itens, *a, **k):
        novos = []
        for (tp, c, t) in itens:
            m = _LEG_PISO.get(t, (tp, c, t))
            if m:
                novos.append(m)
        return orig(d, novos, *a, **k)
    return f


p03.legenda = _legenda_piso_s(bm.legenda)
fo.legenda = _legenda_piso_s(bm.legenda)

# FO2
fo.TAB_PISO_A[:] = [
    ('A1', 'Monolítico contínuo — sala de TV, quarto, cozinha, sala de estar, closet e corredor', '56,26 m²'),
    ('A2', 'Monolítico no banheiro e no box — sistema de área molhada, antiderrapante no box', '3,66 m²'),
    ('A3', 'Juntas de movimentação conforme projeto; junta na soleira do banheiro', 'a definir'),
    ('A4', 'Sem reserva de corte — aplicação moldada in loco', '—'),
]
fo.TAB_PISO_B[:] = [
    ('B1', 'Monolítico — sala de TV, quarto, sala de estar e corredor; juntas conforme projeto', '44,69 m²'),
    ('B2', 'Porcelanato acetinado — cozinha + closet, sem o nicho AT-A', '11,57 m²'),
    ('B3', 'Porcelanato acetinado — banheiro e box, sem o AT-B; atrito para área molhada', '3,66 m²'),
    ('B4', 'Reserva de 10% sobre B2 + B3 — cortes, perdas e reposição', '1,52 m²'),
    ('B5', 'Perfil de transição monolítico/porcelanato; filete de 0,70 m na ponta', 'a medir em obra'),
]
fo.SEQ_PISO[3] = ('4', ['Aplicação — A ou B, conforme opção contratada.',
                        'A: monolítico contínuo, com o banheiro sobre a impermeabilização (A1 a A4).',
                        'B: porcelanato e perfil de transição, depois o monolítico (B1 a B5).'], False)


def _planta_piso_s(d, ox, oy, S, opcao, titulo):
    salvo = (fo.piso_reguas, fo.MONO, fo.WET)
    try:
        if opcao == 'A':
            fo.WET = K07
            return _planta_piso_orig(d, ox, oy, S, 'B', 'OPÇÃO A  ·  monolítico integral, com banheiro')
        fo.piso_reguas, fo.MONO, fo.WET = _mono_no_lugar_do_cumaru, 'none', 'none'
        _PORC_WC[0] = True
        return _planta_piso_orig(d, ox, oy, S, 'A', 'OPÇÃO B  ·  porcelanato acetinado + monolítico')
    finally:
        _PORC_WC[0] = False
        fo.piso_reguas, fo.MONO, fo.WET = salvo


fo._planta_piso = _planta_piso_s


def folha_piso_s():
    d = fo.folha_piso()
    trocar(d, 'OPÇÃO A — CUMARU-FERRO COM COZINHA E CLOSET EM MONOLÍTICO', 'OPÇÃO A — MONOLÍTICO INTEGRAL, COM BANHEIRO E BOX')
    trocar(d, 'OPÇÃO B — MONOLÍTICO INTEGRAL', 'OPÇÃO B — PORCELANATO ACETINADO NO BANHEIRO, BOX, COZINHA E CLOSET')
    return d


_subst(p12.RISCOS, 'A1', ('A1', 'Acabamento', 'Monolítico de 44,69 a 59,92 m² pede juntas — quantas depende do sistema', 'alto'))
_i = [r[0] for r in p12.RISCOS].index('A3') + 1
p12.RISCOS[:] = [r for r in p12.RISCOS if r[0] not in ('D1', 'D2')]
_i = [r[0] for r in p12.RISCOS].index('A3') + 1
p12.RISCOS[_i:_i] = [('A4', 'Acabamento', 'Opção A: monolítico no box pede sistema e garantia para área molhada', 'alto')]
_subst(p09.TAB_DEC, 'Piso', ('Piso', 'Duas opções vivas', 'A monolítico integral, com banheiro · B porcelanato acetinado + monolítico'))
_celula('Piso da casa', 6, 'opção A (monolítico integral) ou B (porcelanato + monolítico)')

CX = (172, 146, 200)          # nota sobre o recorte vazio acima da escada (plantas a 70)
P70 = (70, 156, 70.0, 6.4)
EXTRA_03 = 'Piso não corre sob AT-A nem AT-B: closet 4,14 m² e banheiro 3,66 m² líquidos.'
EXTRA_03A = 'Piso não corre sob AT-A nem AT-B: monolítico 59,92 m² líquidos, banheiro e box incluídos.'
EXTRA_03B = 'Piso não corre sob AT-A nem AT-B: porcelanato 15,23 m² líquidos (cozinha 7,43, closet 4,14, banheiro 3,66).'
EXTRA_DEMO = 'Demolição: não tocar no AT-B (prumada). No closet, preservar ponto de gás, água fria/quente e saída de exaustão do AT-A.'
EXTRA_AR = 'Ar/exaustão: o aquecedor tem ar de combustão e exaustão próprios — não interligar à exaustão do banheiro nem ao ar-condicionado.'
EXTRA_RISCOS = 'NOVOS RISCOS — H6 (ATENÇÃO): posição/medida do shaft AT-B estimada, confirmar após D04. H7 (IMPASSE): aquecedor a gás no closet só segue com laudo NBR 13103 do instalador credenciado / Comgás.'
EXTRA_13 = 'Quarto: sem mudança de layout; o closet perde ~0,24 m² para o nicho AT-A.'
AT_MINI = 'AT-A aquecedor no closet (nicho ~0,60 × 0,40 m, NBR 13103) e AT-B shaft do banho (0,93 × 0,15 m) — ver FO1 e Prancha 01.'
EXTRA_TETO = 'Teto: a chaminé do AT-A corre sob a laje até a J06 — nenhum trilho, luminária ou evaporadora sobre ela.'
EXTRA_ELE = 'Elétrica: conferir com o fabricante do aquecedor se o AT-A pede ponto de força; nada embutido no AT-B.'

FOLHAS = (
    (_com_at(construir_01, (722, 800, 628), (132, 182, 64.0, 6.2), AT_TXT), 'alt-a-s-prancha-01-planta-cotada', 'Prancha 01: planta baixa cotada'),
    (_com_at(construir_02, CX, P70, extra=EXTRA_DEMO), 'alt-a-s-prancha-02-demolicao', 'Prancha 02: demolição e desmontagem'),
    (_com_at(lambda: construir_piso_s('A'), CX, P70, extra=EXTRA_03A), 'alt-a-s-prancha-03-piso-monolitico-integral', 'Prancha 03: piso monolítico integral'),
    (_com_at(lambda: construir_piso_s('B'), CX, P70, extra=EXTRA_03B), 'alt-a-s-prancha-04-piso-porcelanato-monolitico', 'Prancha 04: piso porcelanato + monolítico'),
    (_com_at(construir_teto_fas, CX, P70, extra=EXTRA_TETO), 'alt-a-s-prancha-05-teto', 'Prancha 05: teto'),
    (_com_at(construir_eletrica, CX, P70, extra=EXTRA_ELE), 'alt-a-s-prancha-06-eletrica', 'Prancha 06: elétrica'),
    (_com_at(p06.construir, (70, 150, 600), desenho=False), 'alt-a-s-prancha-07-esquadrias', 'Prancha 07: esquadrias'),
    (_com_at(p07.construir, (70, 818, 345), [_plano_wc(190, 222.0, 118.0) + (7.0, True)]), 'alt-a-s-prancha-08-banheiro', 'Prancha 08: banheiro'),
    (_com_at(p09.construir, (722, 820, 628), desenho=False), 'alt-a-s-prancha-09-medicao', 'Prancha 09: medição e decisões'),
    (_com_at(p10.construir, (70, 640, 600), desenho=False), 'alt-a-s-prancha-10-banheiro-acabamentos', 'Prancha 10: banheiro, acabamentos'),
    (_com_at(construir_11_fas, (755, 450, 590), desenho=False), 'alt-a-s-prancha-11-ar-luz', 'Prancha 11: ar, exaustão e iluminação'),
    (_com_at(construir_riscos_r, None, desenho=False), 'alt-a-s-prancha-12-riscos', 'Prancha 12: riscos'),
    (_com_at(construir_quarto_s, (66, 660, 138), desenho=False, extra=EXTRA_13), 'alt-a-s-prancha-13-quarto-claraboia', 'Prancha 13: quarto adaptável e claraboia'),
    (_com_at(p14.construir, None, desenho=False), 'alt-a-s-prancha-14-programacao', 'Prancha 14: programação da obra'),
)
FOLHAS_FO = (
    (_com_at(folha_demolicao_alt, (165, 138, 180, 7.0), (70, 156, 63.0, 6.0), extra=EXTRA_DEMO), 'alt-a-s-fornecedor-01-demolicao', 'FO1: demolição e preparo'),
    (_com_at(folha_piso_s, (1130 - 340, 820, 560), [(70, 200, 40.0, 5.0), (414, 200, 40.0, 5.0)], extra=EXTRA_03), 'alt-a-s-fornecedor-02-piso', 'FO2: piso'),
    (_com_at(fo.folha_eletrica, (165, 138, 180, 7.0), (70, 156, 63.0, 6.0), extra=EXTRA_ELE), 'alt-a-s-fornecedor-03-eletrica', 'FO3: elétrica'),
    (_com_at(folha_iluminacao_fas, (162, 136, 143, 6.6), (70, 156, 54.0, 5.6), AT_MINI, EXTRA_TETO), 'alt-a-s-fornecedor-04-iluminacao', 'FO4: iluminação'),
    (_com_at(fo.folha_ar, (160, 134, 125, 6.3), (70, 156, 49.0, 5.4), AT_MINI, EXTRA_AR), 'alt-a-s-fornecedor-05-ar', 'FO5: ar-condicionado e exaustão'),
    (_com_at(fo.folha_cortina, (722, 760, 628), desenho=False), 'alt-a-s-fornecedor-06-cortina-claraboia', 'FO6: cortina e claraboia'),
    (_com_at(fo.folha_pedras_vidro_portas, (722, 820, 628), desenho=False), 'alt-a-s-fornecedor-07-pedras-vidro-portas', 'FO7: pedras, vidro do box e portas'),
    (_com_at(fo.folha_programacao, None, desenho=False), 'alt-a-s-fornecedor-08-programacao', 'FO8: programação da obra'),
)

if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    so = set(sys.argv[1:])
    geometria(True)
    for grupo, caderno, titulo_cad in (
            (FOLHAS, 'caderno-alternativo-a-rev-s-A3.pdf',
             'MaxHaus MainFloor — Caderno Alternativo A, REV. S (A3)'),
            (FOLHAS_FO, 'caderno-fornecedores-alternativo-a-rev-s-A3.pdf',
             'MaxHaus 81I — pacote para fornecedores, Alternativo A, REV. S (A3)')):
        saidas = []
        for fn, nome, titulo in grupo:
            if so and not any(s in nome for s in so):
                continue
            caminho = salvar(fn(), pasta, nome)
            exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                            'MaxHaus MainFloor — Alternativo A, REV. S — ' + titulo)
            exportar_png(caminho, os.path.join(pasta, nome + '.png'))
            saidas.append(caminho)
        if not so:
            exportar_pdf_a3(saidas, os.path.join(pasta, caderno), titulo_cad)
        print('ok %d folhas' % len(saidas))
    geometria(False)
