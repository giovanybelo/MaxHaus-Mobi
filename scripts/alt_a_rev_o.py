# -*- coding: utf-8 -*-
"""Caderno Alternativo A — REV. O completa (14 pranchas + FO1 a FO8).

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
    'O quarto passa de 2,54 para 2,71 m livres (13,40 → 14,08 m²) e a sala de TV de 23,00 para',
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
FOLHAS = (
    (construir_01,                 'alt-a-o-prancha-01-planta-cotada',      'Prancha 01: planta baixa cotada'),
    (construir_02,                 'alt-a-o-prancha-02-demolicao',          'Prancha 02: demolição e desmontagem'),
    (lambda: construir_piso('A'),  'alt-a-o-prancha-03-piso-cumaru',        'Prancha 03: piso em cumaru-ferro'),
    (lambda: construir_piso('B'),  'alt-a-o-prancha-04-piso-monolitico',    'Prancha 04: piso monolítico'),
    (construir_teto,               'alt-a-o-prancha-05-teto',               'Prancha 05: teto'),
    (construir_eletrica,           'alt-a-o-prancha-06-eletrica',           'Prancha 06: elétrica'),
    (p06.construir,                'alt-a-o-prancha-07-esquadrias',         'Prancha 07: esquadrias'),
    (p07.construir,                'alt-a-o-prancha-08-banheiro',           'Prancha 08: banheiro'),
    (p09.construir,                'alt-a-o-prancha-09-medicao',            'Prancha 09: medição e decisões'),
    (p10.construir,                'alt-a-o-prancha-10-banheiro-acabamentos', 'Prancha 10: banheiro, acabamentos'),
    (p11.construir,                'alt-a-o-prancha-11-ar-luz',             'Prancha 11: ar, exaustão e iluminação'),
    (construir_riscos,             'alt-a-o-prancha-12-riscos',             'Prancha 12: riscos'),
    (construir_quarto,             'alt-a-o-prancha-13-quarto-claraboia',   'Prancha 13: quarto adaptável e claraboia'),
    (p14.construir,                'alt-a-o-prancha-14-programacao',        'Prancha 14: programação da obra'),
)
FOLHAS_FO = (
    (folha_demolicao_alt,          'alt-a-o-fornecedor-01-demolicao',       'FO1: demolição e preparo'),
    (fo.folha_piso,                'alt-a-o-fornecedor-02-piso',            'FO2: piso'),
    (fo.folha_eletrica,            'alt-a-o-fornecedor-03-eletrica',        'FO3: elétrica'),
    (fo.folha_iluminacao,          'alt-a-o-fornecedor-04-iluminacao',      'FO4: iluminação'),
    (fo.folha_ar,                  'alt-a-o-fornecedor-05-ar',              'FO5: ar-condicionado e exaustão'),
    (fo.folha_cortina,             'alt-a-o-fornecedor-06-cortina-claraboia', 'FO6: cortina e claraboia'),
    (fo.folha_pedras_vidro_portas, 'alt-a-o-fornecedor-07-pedras-vidro-portas', 'FO7: pedras, vidro do box e portas'),
    (fo.folha_programacao,         'alt-a-o-fornecedor-08-programacao',     'FO8: programação da obra'),
)


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    so = set(sys.argv[1:])
    geometria(True)
    for grupo, caderno, titulo_cad in (
            (FOLHAS, 'caderno-alternativo-a-rev-o-A3.pdf',
             'MaxHaus MainFloor — Caderno Alternativo A, REV. O (A3)'),
            (FOLHAS_FO, 'caderno-fornecedores-alternativo-a-rev-o-A3.pdf',
             'MaxHaus 81I — pacote para fornecedores, Alternativo A, REV. O (A3)')):
        saidas = []
        for fn, nome, titulo in grupo:
            if so and not any(s in nome for s in so):
                continue
            caminho = salvar(fn(), pasta, nome)
            exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                            'MaxHaus MainFloor — Alternativo A, REV. O — ' + titulo)
            exportar_png(caminho, os.path.join(pasta, nome + '.png'))
            saidas.append(caminho)
        if not so:
            exportar_pdf_a3(saidas, os.path.join(pasta, caderno), titulo_cad)
        print('ok %d folhas' % len(saidas))
    geometria(False)
