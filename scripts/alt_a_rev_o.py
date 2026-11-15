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
# parede sala de TV/quarto: NÃO é demolida (cliente, 15.11.2026). Fica na posição
# original, que é 0,42 m ao norte do que o scan leu: a face norte coincide com a
# linha da cota de 3,98 m da REV. T. O quarto fica com 2,96 m livres e a sala de
# TV com 4,32 m. Só o vão da porta P03 é aberto (D01) e requadrado (R01).
DY_R01 = 0.42 * PT_PER_M
Y_R01_ANT = 432.3
Y_R01 = Y_R01_ANT - DY_R01
DRYWALL_ANT = bm.DRYWALL_SALA_QUARTO


def _norte(r):
    return (r[0], r[1] - DY_R01, r[2], r[3] - DY_R01)


DRYWALL_R01 = _norte(DRYWALL_ANT)
PORTA_R01 = _norte(bm.PORTA_NOVA)
ALT_WALLS = [DRYWALL_R01 if w == DRYWALL_ANT else w for w in ALT_WALLS]
for _k, _a in (('sala', 21.33), ('quarto', 15.07)):
    ALT_ROOMS[_k]['poly'] = [(x, Y_R01 if (y == Y_R01_ANT and x >= 415.0) else y)
                             for x, y in ALT_ROOMS[_k]['poly']]
    ALT_ROOMS[_k]['area'] = _a
for _m in (bm, p01, p02, p03, p04, p05, p06, p07, p13, fo):
    if hasattr(_m, 'PORTA_NOVA'):
        _m.PORTA_NOVA = PORTA_R01
    if hasattr(_m, 'DRYWALL_SALA_QUARTO'):
        _m.DRYWALL_SALA_QUARTO = PORTA_R01      # da parede só sai o vão da porta
# o estado existente também mostra a parede no lugar real
ORIG_WALLS[:] = [DRYWALL_R01 if w == DRYWALL_ANT else w for w in ORIG_WALLS]
for _k, _a in (('sala', 21.33), ('quarto', 15.07)):
    ORIG_ROOMS[_k]['poly'] = [(x, Y_R01 if (y == Y_R01_ANT and x >= 415.0) else y)
                              for x, y in ORIG_ROOMS[_k]['poly']]
    ORIG_ROOMS[_k]['area'] = _a


def realce_r01(d, cor=K):
    """A parede sala de TV/quarto é mantida: nada a realçar além do vão da porta."""
    return


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
    for r in (WALL_NOVA,):
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
    bm.cota_v(d, 434.63 - DY_R01, 550.38, 599.46, -16, size=6.6, ext=False)   # quarto, 2,96
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
                        'R03 fecha só depois da infraestrutura embutida; R01 é só o requadro do vão da P03.'], True)


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
# parede sala de TV/quarto 0,42 m ao norte do scan — números de sala de TV e quarto
#   sala de TV 23,00 → 21,33 m² · quarto 13,40 → 15,07 m² (Δ 0,42 × 3,98 m)
#   perímetro ∓0,84 m · parede ∓2,03 m² · volume × 2,62 · lm = área × 150 / 0,48
#   social + cozinha 37,05 m² · quarto + closet 19,45 m² (600 e 800 BTU/h·m²)
# ---------------------------------------------------------------------------
_subst(p01.TAB_AMB, 'Sala de TV', ('Sala de TV', '21,33 m²', '19,9 m', '5,6 × 4,4', '4,8 × 3,6'))
_subst(p01.TAB_AMB, 'Quarto', ('Quarto', '15,07 m²', '17,0 m', '5,6 × 3,0', '5,6 × 2,5'))
p01.NOTAS.insert(1, [
    '**Parede sala de TV/quarto: mantida, sem demolição (cliente, 15.11.2026).',
    'Fica na posição original, 0,42 m ao norte da leitura do scan. O quarto tem 2,96 m livres (15,07 m²) e a',
    'sala de TV 4,32 m (21,33 m²). Só o vão da porta de correr P03 é aberto. Conferir a posição em obra.'])
_XP03 = (PORTA_R01[0] + PORTA_R01[2]) / 2.0
p02.ALVOS[:] = [('D01', _XP03, Y_R01, 'demo', 0, -9) if a[0] == 'D01' else
                ('R01', _XP03 + 14.0, Y_R01, 'novo', 10, 11) if a[0] == 'R01' else a for a in p02.ALVOS]
_subst(p02.LINHAS, 'D01', ('D01', 'Abrir vão de porta na parede sala de TV/quarto (parede mantida)', '1 vão — 1,00 × 2,29 m'))
_subst(fo.TAB_DEMO, 'D01', ('D01', 'Abrir vão de porta 1,00 × 2,29 m na parede sala de TV/quarto; a parede fica', '1 vão'))
_subst(p02.LINHAS, 'R01', ('R01', 'Parede sala de TV/quarto mantida: requadrar o vão e instalar a porta de correr P03',
                          '1 vão + 1 porta'))
for _n in p02.NOTAS:
    for _j, _ln in enumerate(_n):
        if _ln.startswith('A drywall entre sala de TV e quarto cai e volta (R01)'):
            _n[_j] = 'A parede sala de TV/quarto fica onde está: só se abre o vão da porta de correr de 1,00 × 2,29 m (D01, R01); a folha'
_subst(p03.TAB_A, 'Cumaru-ferro',
       ('Cumaru-ferro', 'sala de TV 21,33 + quarto 15,07 + sala de estar 5,90 + corredor 2,39', '44,69 m²'))
_subst(p04.TAB_LUZ, 'Sala de TV', ('Sala de TV', '150 lux', '6.665 lm', '2.700 K'))
_subst(p04.TAB_LUZ, 'Quarto', ('Quarto', '150 lux', '4.710 lm', '2.700 K'))
_subst(p04.TAB_AR, 'Social + cozinha', ('Social + cozinha', '37,05 m²', '22.230 BTU/h', '29.640 BTU/h'))
_subst(p04.TAB_AR, 'Quarto + closet', ('Quarto + closet', '19,45 m²', '11.670 BTU/h', '15.560 BTU/h'))
_subst(p05.COMANDOS, 'S05', ('S05', 4.90, 6.98 - 0.42))      # acompanha a face do quarto
_subst(p09.TAB_AMB, 'Sala de TV', ('Sala de TV', '21,33', '27,77', '55,88'))
_subst(p09.TAB_AMB, 'Quarto', ('Quarto', '15,07', '32,33', '39,48'))
p09.TAB_DEC.insert(1, ('Parede sala de TV/quarto', 'cliente, 15.11.2026', 'mantida, sem demolição · quarto 2,96 m livres · 15,07 m²'))
_subst(p11.TAB_TERM, 'Social + cozinha', ('Social + cozinha', '37,05', '22.230', '29.640', 'sala de TV, sala de estar, cozinha e circulação'))
_subst(p11.TAB_TERM, 'Quarto + closet', ('Quarto + closet', '19,45', '11.670', '15.560', 'zona de dormir'))
_subst(p11.TAB_LUZ, 'Sala de TV', ('Sala de TV', '21,33', '150 lux', '6.665 lm', '2.700 K', 'leitura e cenas dimerizáveis'))
_subst(p11.TAB_LUZ, 'Quarto', ('Quarto', '15,07', '150 lux', '4.710 lm', '2.700 K', 'cabeceira independente'))
_subst(fo.TAB_DEMO, 'R01', ('R01', 'Parede sala de TV/quarto mantida: requadrar o vão de 1,00 × 2,29 m para a porta de correr P03',
                            '1 vão'))
_subst(fo.TAB_LUX, 'Sala de TV', ('Sala de TV', '150 lux', '6.665 lm', '2.700 K'))
_subst(fo.TAB_LUX, 'Quarto', ('Quarto', '150 lux', '4.710 lm', '2.700 K'))
_subst(fo.TAB_AR_FO, 'AC01', ('AC01', 'Evaporadora — social + cozinha (37,05 m²)', '1 unidade'))
_subst(fo.TAB_AR_FO, 'AC02', ('AC02', 'Evaporadora — quarto + closet (19,45 m²)', '1 unidade'))
_subst(fo.TAB_BTU, 'Social + cozinha', ('Social + cozinha', '37,05 m²', '22.230 BTU/h', '29.640 BTU/h'))
_subst(fo.TAB_BTU, 'Quarto + closet', ('Quarto + closet', '19,45 m²', '11.670 BTU/h', '15.560 BTU/h'))
fo.SEQ_AR[1] = (fo.SEQ_AR[1][0], [fo.SEQ_AR[1][1][0].replace('30.976 e 14.224', '29.640 e 15.560')]
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
    ('Monolítico',        'sala de TV 21,33 + quarto 15,07 + sala de estar 5,90 + corredor 2,39', '44,69 m²'),
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


def nota_at(d, x, y, w, texto=None, extra=None, titulo=None, size=7.4, lh=10.2):
    texto = AT_CURTO if texto is None else texto
    if titulo is None:
        titulo = AT_TITULO if w >= 150 else 'BANHEIRO · OBRA 14/11'
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


def _com_at(fn, caixa, plano=None, texto=None, extra=None, desenho=True):
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
#      monolítico: sala de TV 21,33 + quarto 15,07 + sala de estar 5,90 + corredor 2,39 = 44,69 m²
p03.TAB_B[:] = [
    ('Monolítico',      'sala de TV, quarto, cozinha, sala de estar, closet e corredor (sem AT-A)', '56,26 m²'),
    ('Banheiro e box',  'mesmo monolítico, sistema para área molhada sobre impermeabilização (sem AT-B)', '3,66 m²'),
    ('Sem reserva',     'aplicação moldada in loco, sem perda de corte',                     '—'),
    ('MainFloor',       'total revestido, líquido das áreas técnicas',                      '59,92 m²'),
]
p03.TAB_A[:] = [
    ('Monolítico',        'sala de TV 21,33 + quarto 15,07 + sala de estar 5,90 + corredor 2,39', '44,69 m²'),
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

# ---------------------------------------------------------------------------
# REV. T (14.11.2026) — banheiro remedido em obra pelo cliente
#   · parede da porta, por fora: 0,88 + 0,80 (vão, 2,15 m de altura) + 1,20 = 2,88 m
#     (a geometria está em base_mainfloor; por dentro o banheiro tem 2,68 m)
#   · AT-B (shaft do chuveiro): 0,80 × 0,25 m, no canto sudoeste do box
#   · bancada 1,60 × 0,40 m com saia de 10 cm, sobre o gabinete de 0,88 m (topo 0,98 m)
#   · espelho 1,60 × 0,90 m · T20 é o ponto do toalheiro, acima do vaso
#   · tipografia: família Helvetica em todas as folhas
#   As áreas dos quadros continuam as do scan: a diferença de 4 cm no comprimento
#   (~0,06 m²) fica para a medição depois da demolição.
# ---------------------------------------------------------------------------
for _n in p01.NOTAS:
    for _j, _ln in enumerate(_n):
        if 'A nova drywall (R01) repete a espessura' in _ln:
            _n[_j] = _ln.replace('A nova drywall (R01) repete a espessura', 'A parede sala de TV/quarto é mantida com a espessura atual')
bm.ESQUADRIAS[:] = [e[:-1] + ('nova, na parede sala de TV/quarto (mantida)',) if e[0] == 'P03' else e for e in bm.ESQUADRIAS] if hasattr(bm, 'ESQUADRIAS') else []
# REV. U (15.11.2026) — parede sala de TV/quarto mantida, na posição original (ver topo)
REV_ALT = 'ALT. A  ·  REV. U'
bm.DATA_EMISSAO = '15/11/2026'
fo.DATA = '15.11.2026'
fo.EMISSAO = 'ALT. A  ·  EMISSÃO 07'
fo.ORIGEM = 'extraído do Caderno Alternativo A — REV. U'

AT_B = (347.96, 450.67 - 0.80 * PT_PER_M, 347.96 + 0.25 * PT_PER_M, 450.67)
AT_TITULO = 'BANHEIRO · MEDIDO EM OBRA (14/11/2026)'
AT_CURTO = ('Parede da porta, por fora: 0,88 m + vão de 0,80 × 2,15 m + 1,20 m = 2,88 m. AT-B (shaft do '
            'chuveiro) 0,80 × 0,25 m. AT-A aquecedor no closet (~0,60 × 0,40 m, NBR 13103 a liberar). '
            'Detalhes no Executivo do Banheiro.')
AT_MINI = 'AT-A aquecedor no closet (~0,60 × 0,40 m, NBR 13103) e AT-B shaft do chuveiro (0,80 × 0,25 m). Ver FO1 e Prancha 01.'
AT_TXT = ('Banheiro remedido em 14/11/2026. Parede da porta, pela face externa, de norte a sul: 0,88 m de parede, '
          'vão de 0,80 m com 2,15 m de altura e 1,20 m de parede; total 2,88 m (o scan dava 2,84 m). Por dentro: '
          '1,43 × 2,68 m. AT-B · área técnica do chuveiro, no canto sudoeste do box: 0,80 m ao longo da parede da '
          'bancada por 0,25 m de profundidade; o box continua com 0,92 m. Prumada do condomínio: não demolir. '
          'Bancada 1,60 × 0,40 m com saia de 10 cm sobre o gabinete de 0,88 m (topo a 0,98 m); espelho 1,60 × 0,90 m. '
          'AT-A · aquecedor a gás no closet, nicho ~0,60 × 0,40 m piso-laje na parede de divisa, chaminé sob a laje '
          'até a bandeira da J06 (posição esquemática); NBR 13103: liberação por instalador credenciado / Comgás. '
          'As áreas do quadro seguem o scan: os 4 cm a mais no comprimento (~0,06 m²) entram depois da medição pós-demolição.')

_subst(p12.RISCOS, 'H6', ('H6', 'Hidráulica', 'Shaft AT-B: 0,80 × 0,25 m medido em 14/11; posição dentro do box a confirmar após a D04', 'alto'))
_subst(fo.TAB_PORTAS, 'P02', ('P02', 'Banheiro — abre para fora em sentido anti-horário; vão a 0,88 m do canto norte', '0,80 × 2,15 m'))
_subst(p07.TAB_RECON_WC, 'P02', ('P02', 'Porta 0,80 × 2,15 m, de abrir para fora — anti-horário, dobradiça norte', '1 vão'))
p05.TOMADAS_NOVAS[:] = [t for t in p05.TOMADAS_NOVAS if t[0] != 'T20'] + [('T20', 3.22, 4.62, 'toalheiro, acima do vaso')]
_subst(p05.LINHAS, 'Banheiro', ('Banheiro', 'lavatório (T17) e T20: toalheiro, acima do vaso', 'volumes de proteção, DR e cargas'))
_subst(fo.TAB_ELE, 'T10–T20', ('T10–T20', 'Tomadas novas; T18 é espera no teto, T20 é o toalheiro acima do vaso', '11 pontos'))
_subst(p07.TAB_INST_WC, 'T20', ('T20', 'Ponto 127 V do toalheiro térmico, acima do vaso — circuito com DR', '1 ponto'))

# áreas líquidas com o AT-B de 0,80 × 0,25 (0,20 m²): banheiro 3,60 m²
_subst(p03.TAB_B, 'Monolítico', ('Monolítico', 'sala de TV, quarto, cozinha, sala de estar, closet e corredor (sem AT-A)', '56,26 m²'))
_subst(p03.TAB_B, 'Banheiro e box', ('Banheiro e box', 'mesmo monolítico, sistema para área molhada sobre impermeabilização (sem AT-B)', '3,60 m²'))
_subst(p03.TAB_B, 'MainFloor', ('MainFloor', 'total revestido, líquido das áreas técnicas', '59,86 m²'))
_subst(p03.TAB_A, 'Porcelanato', ('Porcelanato', 'cozinha 7,43 + closet 4,14 + banheiro e box 3,60 (líquidos) — no banheiro: Confete', '15,17 m²'))
_subst(p03.TAB_A, '+ reserva de 10%', ('+ reserva de 10%', 'cortes, perdas e reposição futura do porcelanato', '16,69 m²'))
_subst(p03.TAB_A, 'MainFloor', ('MainFloor', 'total revestido, líquido das áreas técnicas', '59,86 m²'))
_subst(fo.TAB_PISO_A, 'A2', ('A2', 'Monolítico no banheiro e no box — sistema de área molhada, antiderrapante no box', '3,60 m²'))
_subst(fo.TAB_PISO_B, 'B3', ('B3', 'Porcelanato Confete 100 × 100 — banheiro e box, sem o AT-B; ver executivo do banheiro', '3,60 m²'))
_subst(p12.RISCOS, 'A1', ('A1', 'Acabamento', 'Monolítico de 44,69 a 59,86 m² pede juntas — quantas depende do sistema', 'alto'))
EXTRA_03 = 'Piso não corre sob AT-A nem AT-B: closet 4,14 m² e banheiro 3,60 m² líquidos.'
EXTRA_03A = 'Piso não corre sob AT-A nem AT-B: monolítico 59,86 m² líquidos, banheiro e box incluídos.'
EXTRA_03B = 'Piso não corre sob AT-A nem AT-B: porcelanato 15,17 m² líquidos (cozinha 7,43, closet 4,14, banheiro 3,60).'
EXTRA_WC = 'Folha anterior às medidas de 14/11: quantidades e detalhes do banheiro valem pelo Executivo do Banheiro.'

CX = (172, 146, 200)          # nota sobre o recorte vazio acima da escada (plantas a 70)
P70 = (70, 156, 70.0, 6.4)
EXTRA_DEMO = 'Demolição: não tocar no AT-B (prumada). No closet, preservar ponto de gás, água fria/quente e saída de exaustão do AT-A.'
EXTRA_AR = 'Ar/exaustão: o aquecedor tem ar de combustão e exaustão próprios — não interligar à exaustão do banheiro nem ao ar-condicionado.'
EXTRA_RISCOS = 'NOVOS RISCOS — H6 (ATENÇÃO): posição/medida do shaft AT-B estimada, confirmar após D04. H7 (IMPASSE): aquecedor a gás no closet só segue com laudo NBR 13103 do instalador credenciado / Comgás.'
EXTRA_13 = 'Quarto: sem mudança de layout; o closet perde ~0,24 m² para o nicho AT-A.'
EXTRA_TETO = 'Teto: a chaminé do AT-A corre sob a laje até a J06 — nenhum trilho, luminária ou evaporadora sobre ela.'
EXTRA_ELE = 'Elétrica: conferir com o fabricante do aquecedor se o AT-A pede ponto de força; nada embutido no AT-B.'

# ---------------------------------------------------------------------------
# REV. V (15.11.2026) — respostas do cliente às divergências da revisão
#   · forro do banheiro a 2,50 m (como no Executivo); exaustor 3,80 × 2,50 × 10 = 95,0 m³/h
#   · revestimento do banheiro = Executivo E3: paredes 14,93 + nicho 0,84 + bancada 0,84 m²
#   · elétrica: só troca de fiação; pontos mantidos; único ponto novo é o T20 (toalheiro)
#   · porta P03: vão existente ampliado, porta de abrir 0,90 × 2,10 m para o quarto,
#     sentido horário, a 0,15 m da parede do banheiro
# ---------------------------------------------------------------------------
REV_ALT = 'ALT. A  ·  REV. V'
fo.EMISSAO = 'ALT. A  ·  EMISSÃO 08'
fo.ORIGEM = 'extraído do Caderno Alternativo A — REV. V'


def _varrer(obj, pares):
    """Troca trechos de texto dentro de listas/tuplas aninhadas (dados das folhas)."""
    if isinstance(obj, str):
        for a, b in pares:
            obj = obj.replace(a, b)
        return obj
    if isinstance(obj, tuple):
        return tuple(_varrer(o, pares) for o in obj)
    if isinstance(obj, list):
        obj[:] = [_varrer(o, pares) for o in obj]
        return obj
    if isinstance(obj, dict):
        for k in list(obj):
            obj[k] = _varrer(obj[k], pares)
        return obj
    return obj


def _paragrafo(notas, inicio, novo):
    for i, n in enumerate(notas):
        if n and n[0].startswith(inicio):
            notas[i] = novo
            return
    raise ValueError('parágrafo não encontrado: %r' % inicio)


# ---- porta P03 de abrir --------------------------------------------------
X_BANHO_LESTE = 417.90
P03_VAO = (X_BANHO_LESTE + 0.15 * PT_PER_M, DRYWALL_R01[1], X_BANHO_LESTE + 1.13 * PT_PER_M, DRYWALL_R01[3])
PORTA_R01 = (P03_VAO[0] + 0.04 * PT_PER_M, DRYWALL_R01[1], P03_VAO[0] + 0.94 * PT_PER_M, DRYWALL_R01[3])


def _porta_p03(d, rect, lado='n', sentido='e'):
    bm.porta_horizontal(d, rect, hinge='w', swing='s')      # abre para o quarto, horário


import alt_a_parede_cozinha as _apc
for _m in (bm, p01, p02, p03, p04, p05, p06, p07, p13, fo, _apc):
    if hasattr(_m, 'PORTA_NOVA'):
        _m.PORTA_NOVA = PORTA_R01
    if hasattr(_m, 'DRYWALL_SALA_QUARTO'):
        _m.DRYWALL_SALA_QUARTO = PORTA_R01
    if hasattr(_m, 'porta_correr_horizontal'):
        _m.porta_correr_horizontal = _porta_p03
bm.ESQUADRIAS[:] = [('P03', 'Porta de abrir', 'Quarto', 0.90, 2.10, 1.89, 'vão existente ampliado; abre para o quarto, horário')
                    if e[0] == 'P03' else e for e in bm.ESQUADRIAS]
_XP03 = (PORTA_R01[0] + PORTA_R01[2]) / 2.0
p02.ALVOS[:] = [('D01', _XP03, Y_R01, 'demo', 0, -9) if a[0] == 'D01' else
                ('R01', _XP03 + 14.0, Y_R01, 'novo', 10, 11) if a[0] == 'R01' else a for a in p02.ALVOS]
_subst(p02.LINHAS, 'D01', ('D01', 'Ampliar o vão existente da porta sala de TV/quarto (parede mantida)', '1 vão — ~0,98 × 2,14 m'))
_subst(p02.LINHAS, 'R01', ('R01', 'Requadrar o vão e instalar a P03: porta de abrir 0,90 × 2,10 m, para o quarto', '1 vão + 1 porta'))
_subst(fo.TAB_DEMO, 'D01', ('D01', 'Ampliar o vão existente sala de TV/quarto para ~0,98 × 2,14 m, a 0,15 m do banheiro', '1 vão'))
_subst(fo.TAB_DEMO, 'R01', ('R01', 'Requadrar o vão para a porta P03 de abrir, 0,90 × 2,10 m', '1 vão'))
for _n in p02.NOTAS:
    for _j, _ln in enumerate(_n):
        if _ln.startswith('A parede sala de TV/quarto fica onde está'):
            assert 'O vidro do fundo do box' in _n[_j + 1], _n[_j + 1]
            _n[_j] = 'A parede sala de TV/quarto fica onde está: o vão existente é ampliado para a porta P03 de abrir,'
            _n[_j + 1] = '0,90 × 2,10 m, a 0,15 m do banheiro (D01, R01). O vidro do fundo do box cai e vira parede (R02).'
_paragrafo(p06.NOTAS, '**P03 é a única esquadria nova.', [
    '**P03 é a única porta nova (REV. V).',
    'Porta de abrir de 0,90 × 2,10 m, no vão existente ampliado da parede sala de TV/quarto, a 0,15 m',
    'da parede do banheiro. Abre para o quarto, em sentido horário, com a dobradiça do lado do banheiro.',
    'P02, do banheiro, 0,80 × 2,15 m, abre para fora, anti-horário. P01, a entrada, não muda.'])
_paragrafo(p01.NOTAS, '**Pé-direito: 2,40 m com o forro atual', [
    '**Pé-direito: 2,40 m com o forro atual, 2,62 m na laje.',
    'Alturas informadas pelo cliente; o relatório do scan mede 2,40 m com forro, o que confere. Com',
    'a retirada total do forro (D07) ganham-se os 0,22 m de plenum; só o banheiro recebe forro novo,',
    'a 2,50 m. O volume passa de 144,51 m³ para cerca de 158 m³ com a laje aparente.'])
_paragrafo(p01.NOTAS, '**Espessuras e níveis', [
    '**Espessuras e níveis: uma cota única para o pavimento.',
    'Todas as paredes lidas no scan têm 0,10 m. A parede sala de TV/quarto fica com a espessura atual;',
    'só o vão da P03 é ampliado. O banheiro passa a nascer na mesma cota do piso seco (P05), sem',
    'degrau de soleira, e todo o contrapiso é lixado e nivelado (P06): ±0,00 é o piso acabado atual,',
    'e o nível final precisa ser amarrado ao hall.'])
_varrer(p01.NOTAS, [('Só o vão da porta de correr P03 é aberto. Conferir a posição em obra.',
                     'O vão da P03 é ampliado para porta de abrir de 0,90 × 2,10 m.')])
_subst(fo.TAB_PORTAS, 'P03', ('P03', 'Quarto / sala de TV — de abrir, para o quarto, sentido horário; dobradiça do lado '
                                     'do banheiro; vão a 0,15 m da parede dele', 'folha 0,90 × 2,10 m'))
fo.SEQ_FO7[-1] = ('6', ['Portas — P02 com giro invertido e P03 nova, de abrir.',
                        'Vão da P03 ampliado antes do revestimento; folha depois da pintura.'], False)
_subst(p12.RISCOS, 'L4', ('L4', 'Elétrica', 'Eletroduto existente obstruído na troca da fiação — decidir antes de abrir parede', 'medio'))

# ---- forro do banheiro a 2,50 m ------------------------------------------
p07.PE_DIREITO_FORRO = 2.50
_subst(p09.TAB_AMB, 'Banheiro', ('Banheiro', '3,80', '16,70', '9,50'))
p09.TAB_DEC[0:0] = [
    ('Forro do banheiro', 'REV. V', '2,50 m, forro novo, como no Executivo'),
    ('Elétrica', 'REV. V', 'troca de fiação; só o T20 é ponto novo'),
    ('Porta P03', 'REV. V', 'de abrir, 0,90 × 2,10 m, para o quarto'),
    ('Bancada do banheiro', 'REV. V', 'balcão atual revestido em Bleu Nuit'),
]
for _m in (p11,):
    for _nome in ('TAB_PREM',):
        _subst(getattr(_m, _nome), 'Altura do banheiro', ('Altura do banheiro', '2,50 m', 'sob o forro novo'))

# ---- prancha 10: resumo do Executivo E3 -----------------------------------
p10.TAB_PREM[:] = [
    ('Medidas', 'interno 1,42 × 2,68 m', 'medidas de obra de 14/11', 'Executivo E3'),
    ('Altura de revestimento', '2,50 m', 'até o forro novo', 'REV. V — não 2,40'),
    ('Box', '1,42 × 0,92 m', 'AT-B de 0,80 × 0,25 no canto', 'cliente, 14/11'),
    ('Porta P02', '0,80 × 2,15 m', 'descontada; guarnição de 50 mm', 'cliente, 14/11'),
    ('Sem revestimento', 'gabinete e espelho', 'P3 só na faixa e acima do espelho', 'BE-17'),
    ('Nicho', '1,17 × 0,40 m', 'de parede a parede, base a +1,10', 'cliente, 14 e 15/11'),
    ('Bancada B01', '1,60 × 0,40 + saia', 'balcão atual revestido', 'cliente, 15/11'),
    ('Perda', '10%', 'sobre as peças contadas na malha', 'conta conservadora'),
]
p10.TAB_SUP[:] = [
    ('Paredes P1 a P6', 'malha 155 × 155, 745 peças', '14,93', '1,49', '16,42'),
    ('Nicho', 'fundo, base, teto e pontas, 46 peças', '0,84', '0,08', '0,92'),
    ('Bancada B01', 'tampo, saia e lateral, 47 peças', '0,84', '0,08', '0,92'),
    ('Bleu Nuit — total', '838 peças + 10% = 922 · 26 caixas', '16,61', '1,66', '18,27'),
    ('Piso Confete', '100 × 100 em placas, 12 recortes', '3,82', '—', '6 placas'),
]
p10.TAB_ANTES[:] = [
    ('REV. U (até 2,40 m)', '21,73 m²', '23,90 m²', 'perímetro cheio, sem paginação'),
    ('REV. V = Executivo E3', '20,43 m²', '22,09 m²', 'malha real, nicho e bancada'),
    ('Diferença', '−1,30 m²', '−1,81 m²', 'gabinete e espelho sem azulejo'),
]
p10.TAB_LOUCA[:] = [
    ('Bacia sanitária', '1 un.', 'Reinstalar', 'anel e engate novos; eixo a 0,98 m'),
    ('Cuba de apoio', '1 un.', 'Definir modelo', 'borda a +1,14 m com tampo a +0,98'),
    ('Misturador da pia', '1 un.', 'Novo, com água quente', 'comandos a +1,245; bica a +1,25'),
    ('Chuveiro', '1 conj.', 'Manter / definir', 'água quente da coluna no AT-B'),
    ('Ralo linear do box', '1 un.', 'Novo, 720 × 90', 'caimento −10 / −25 mm'),
    ('Ralo R2, junto ao vaso', '1 un.', 'Grelha oculta 100 × 100', 'prolongador a medir'),
    ('Toalheiro elétrico', '1 un.', 'Aiello Unique Solo', 'ponto novo T20, atrás do vaso'),
    ('Box de vidro — K01', '1 conj.', 'Manter e proteger', 'medir o vão só após revestir'),
]
p10.NOTAS[:] = [
    ['**Esta folha resume o Executivo do Banheiro E3.',
     'Quantidades, paginação e detalhes valem pelos cadernos Executivo e Técnico E3.',
     'Aqui ficam só os totais, para o orçamento geral.'],
    ['**Forro novo a 2,50 m.',
     'O revestimento vai até o forro novo. Da laje (2,62 m) sobram 0,12 m para as luminárias',
     'da FAS, que pedem no mínimo 0,10 m.'],
    ['**Por que o total caiu, mesmo com o forro mais alto.',
     'A conta antiga revestia o perímetro inteiro. Na malha real não há azulejo atrás do gabinete e',
     'do espelho, e porta e nicho saem da área; entram o interior do nicho e a bancada revestida.'],
    ['**Impermeabilização é sistema à parte.',
     'Piso, box até o forro, rodapé e nicho: cerca de 12 m², com ensaio de 72 horas antes de assentar.'],
    ['**Rejunte.',
     'Paredes e piso com acrílico Quartzolit: 5 dias antes de molhar. Tampo da bancada com epóxi.'],
]

# ---- elétrica: troca de fiação, só o T20 é novo ----------------------------
p05.TOMADAS_NOVAS[:] = [('T20', 3.22, 4.62, 'toalheiro, atrás do vaso')]
p05.COMANDOS[:] = []
p05.LINHAS[:] = [
    ('Regra desta obra', 'trocar toda a fiação; manter todos os pontos', 'nenhuma saída nova, exceto o T20'),
    ('Quadro elétrico', 'existente, junto à porta de entrada', 'avaliar proteção: DR e DPS'),
    ('Tomadas existentes', 'T01 a T09, posições do cliente', 'trocar espelhos; módulo se gasto'),
    ('Comandos existentes', 'posições atuais, fora do scan', 'trocar espelhos e os comandos indicados'),
    ('Ponto novo', 'T20 — toalheiro elétrico, atrás do vaso', 'único; circuito com DR'),
    ('Banheiro', 'bancada, luz e exaustor nos pontos atuais', 'volumes de proteção e DR'),
    ('Iluminação FAS e ar', 'alimentar a partir dos pontos existentes', 'ponto novo só com aprovação'),
    ('Claraboia', 'espera T18 cancelada', 'o motor de 2027/28 leva ponto próprio'),
]
p05.NOTAS[:] = [
    ['**O quadro de energia fica junto à porta de entrada (posição do cliente).',
     'Com a porta de entrada medindo 1,00 m de vão, a folha passa sobre o quadro: confirmar espaço',
     'livre e altura antes de trocar a proteção — todo o traçado sai dali.'],
    ['**Regra desta obra: troca de fiação, sem saídas novas.',
     'Toda a fiação é trocada pelos eletrodutos existentes. Tomadas e comandos ficam onde estão:',
     'nas tomadas trocam-se os espelhos; nos interruptores, os espelhos e os comandos que o cliente',
     'indicar. O único ponto novo é o T20, do toalheiro elétrico, atrás do vaso.'],
    ['**Eletroduto obstruído é decisão, não improviso.',
     'Se um trecho não aceitar o cabo novo, parar e decidir com o cliente antes de abrir parede ou',
     'de passar cabo aparente.'],
    ['**Iluminação FAS e ar-condicionado: conferir a alimentação.',
     'Trilhos, destaques e evaporadoras das Pranchas 05 e 11 precisam de energia no teto. Se o projeto',
     'da FAS ou o manual da Electrolux pedir ponto que não existe, é exceção a aprovar pelo cliente.'],
    ['**Claraboia e quarto adaptável: sem pontos novos.',
     'A espera T18 e os comandos S09/S10 saem desta obra. O quarto adaptável usa as tomadas',
     'existentes T01 e T02; o motor do fechamento, em 2027/28, leva ponto e eletroduto próprios.'],
    p05.NOTAS[-1]]
fo.ESPERA_CLARABOIA = False
fo.TAB_ELE[:] = [
    ('QD', 'Quadro existente: avaliar; proteção DR e DPS conforme projeto', '1 conjunto'),
    ('FI', 'Troca de toda a fiação pelos eletrodutos existentes', 'todos os circuitos'),
    ('T01–T09', 'Tomadas existentes: manter posição; trocar espelho (e módulo, se gasto)', '9 pontos'),
    ('SX', 'Comandos existentes: manter posição; trocar espelhos e os comandos indicados', 'a levantar'),
    ('T20', 'Ponto novo do toalheiro elétrico, atrás do vaso — o único ponto novo', '1 ponto'),
    ('IN2', 'Infraestrutura aparente no teto para a iluminação FAS (perfilado pintado)', 'a medir'),
    ('AL1', 'Trilhos e destaques FAS: alimentar de ponto existente; ponto novo só com aprovação', 'a confirmar'),
    ('AL3', 'Luz do banheiro no forro novo (D1, D2): circuito existente', '2 pontos'),
    ('AL4', 'Evaporadoras Electrolux: idem AL1', 'a confirmar'),
    ('AL5', 'Exaustor do banheiro e coifa: pontos existentes', '2 pontos'),
    ('PR', 'Proteção: disjuntores, DR e DPS conforme projeto elétrico', '1 conjunto'),
    ('AT', 'Aterramento e equipotencialização', '1 conjunto'),
    ('EN', 'Ensaios: continuidade, isolamento, DR e aterramento', '1 conjunto'),
]
fo.SEQ_ELE[:] = [
    ('1', ['Levantamento e ensaio — E02.',
           'Identificar quadro, circuitos e eletrodutos existentes. Medir isolamento.'], True),
    ('2', ['Projeto de retrofit.',
           'Diagrama unifilar, seções e proteção para a fiação nova nos eletrodutos existentes.'], True),
    ('3', ['Teste de passagem.',
           'Conferir cada eletroduto antes de comprar cabo. Obstruído: parar e decidir com o cliente.'], True),
    ('4', ['Retirada da fiação antiga e passagem da nova — FI.'], False),
    ('5', ['Ponto novo T20, antes da impermeabilização do banheiro.'], True),
    ('6', ['Infraestrutura aparente no teto — IN2.',
           'Somente após o preparo da laje, alinhada aos trilhos da FO4.'], False),
    ('7', ['Quadro, proteção e aterramento — QD, PR e AT.'], False),
    ('8', ['Ensaios — EN.', 'Continuidade, isolamento, DR e aterramento, com laudo por escrito.'], False),
    ('9', ['Espelhos e comandos novos.', 'Somente após a pintura concluída.'], False),
]
_varrer(p07.TAB_INST_WC, [('Tomada do lavatório, a validar em volume de proteção', 'Tomada existente do lavatório: manter, trocar espelho'),
                          ('Comando das arandelas do espelho, junto à bancada', 'Interruptor existente do espelho: trocar comando e espelho')])
_varrer(pg.LINHAS, [('eletrodutos, quadro, esperas AL e T18', 'troca da fiação, quadro e T20'), ('espera T18 e comando S10', 'sem espera da claraboia'), ('FC01 e FC02 na espera T18', 'FC01 e FC02, ponto próprio')])
p13.TOMADAS_Q[:] = []
p13.COMANDOS_Q[:] = []
p13.ESPERA_CLARABOIA = False
p13.TAB_FASE[:] = [r for r in p13.TAB_FASE if r[0] not in ('IN4', 'IN5')]
_subst(p13.TAB_FASE, 'FC02', ('FC02', 'Ponto e eletroduto do motor, aparentes sobre a laje pintada', '2027/28'))
_paragrafo(p13.NOTAS, '**Fechamento elétrico', [
    '**Fechamento elétrico: equipamento e ponto ficam para 2027/28.',
    'Sem pontos novos nesta obra, a espera T18 saiu. O motor vai precisar de ponto e eletroduto',
    'aparentes na época. A moldura fixa na faixa de 0,12 m em volta do vidro — confirmar viga de borda.'])
_subst(fo.TAB_CORT, 'FC02', ('FC02', '2027/28 — ponto e eletroduto do motor, aparentes, e comando', '1 conjunto'))
fo.SEQ_CORT[:] = [s for s in fo.SEQ_CORT if not s[1][0].startswith('Espera da claraboia')]
fo.SEQ_CORT[:] = [(str(i + 1),) + s[1:] for i, s in enumerate(fo.SEQ_CORT)]
fo.SEQ_CORT[-1] = (fo.SEQ_CORT[-1][0], ['2027/28 — fechamento elétrico FC01 e FC02.',
                                        'Moldura na faixa reservada; motor com ponto e eletroduto próprios.',
                                        'Não pode interferir no perfil PF1 que cruza por baixo da claraboia.'], True)

# ---- textos já desenhados: trocas na saída SVG ------------------------------
PARES_REV_V = [
    ('de correr e porta do banheiro girando para o quarto — está nas Pranchas 03 a 08.',
     'P03 de abrir e giro novo da porta do banheiro — está nas Pranchas 03 a 08.'),
    ('S04/S08 ficam do lado da dobradiça', 'S04 fica do lado da dobradiça'),
    ('esperas AL e T18', 'esperas AL'),
    ('espera T18 e comando S10', 'sem espera da claraboia'),
    ('FC01 e FC02 na espera T18', 'FC01 e FC02, com ponto próprio'),
    ('vão de 1,00 m na drywall R01', 'vão da P03 ampliado'),
    ('trilho P03 · giro novo da P02', 'porta P03 · giro novo da P02'),
    ('Forro novo do banheiro, resistente à umidade, a 2,40 m', 'Forro novo do banheiro, resistente à umidade, a 2,50 m'),
    ('Forro novo resistente à umidade, a 2,40 m', 'Forro novo resistente à umidade, a 2,50 m'),
    ('que volta novo (R03) a 2,40 m', 'que volta novo (R03) a 2,50 m'),
    ('3,8 × 2,40 × 10 = 91,2 m³/h', '3,8 × 2,50 × 10 = 95,0 m³/h'),
    ('(mantém forro)', '(forro novo)'),
    ('3,80 × 2,40 = 9,12 m³', '3,80 × 2,50 = 9,50 m³'),
    ('3,80 m² × 2,40 m × 10 trocas/h', '3,80 m² × 2,50 m × 10 trocas/h'),
    ('91,2 m³/h', '95,0 m³/h'),
    ('forro novo R03  ·  2,40 m livres', 'forro novo R03  ·  2,50 m livres'),
    ('forro novo a 2,40 m', 'forro novo a 2,50 m'),
    ('Altura livre de 2,40 m, contra 2,62 m', 'Altura livre de 2,50 m, contra 2,62 m'),
    ('2,40 m sob o forro do banheiro', '2,50 m sob o forro novo do banheiro'),
    ('2,40 sob o forro do banheiro', '2,50 sob o forro novo do banheiro'),
    ('exceto o banheiro, com 2,40 m sob o forro', 'exceto o banheiro, com 2,50 m sob o forro novo'),
    ('depois da D07, e 2,40 m', 'depois da D07, e 2,50 m'),
    ('banheiro se calculam com 2,40 — usar 2,62 lá dentro superestima em 9%.',
     'banheiro se calculam com 2,50 — usar 2,62 lá dentro superestima em 5%.'),
    ('piso e paredes até 2,40 m', 'piso e paredes até 2,50 m'),
    ('banheiro a 2,40 m e a exaustão a', 'banheiro a 2,50 m e a exaustão a'),
    ('O volume se calcula com 2,40 m, a altura sob o forro que permanece', 'O volume se calcula com 2,50 m, a altura sob o forro novo'),
    ('entram trilho, perfilado e evaporadora — e é ela que dá os 0,33 m acima da porta de correr de',
     'entram trilho, perfilado e evaporadora. O banheiro é o único com forro: novo, a 2,50 m;'),
    ('2,29 m. Fora do banheiro, único com forro (refeito novo), nada de embutido.', 'fora dele, nada de embutido.'),
    ('e a linha da porta de correr entre sala de TV e quarto.', 'e a soleira da porta P03, entre sala de TV e quarto.'),
    ('as soleiras da entrada e do banheiro, a linha da porta de', 'as soleiras da entrada, do banheiro e da porta'),
    ('correr P03 e o encontro com o porcelanato.', 'P03 e o encontro com o porcelanato.'),
    ('O trilho CT01 e o da porta P03 vão na laje pintada; o perfil PF1 e os apoios da cortina',
     'O trilho CT01 vai na laje pintada; o perfil PF1 e os apoios da cortina'),
    ('entram antes, com a espera T18 da claraboia. O fechamento elétrico é de 2027/28 e só usa',
     'entram antes. O fechamento elétrico da claraboia é de 2027/28 e terá'),
    ('o que fica pronto agora.', 'ponto e eletroduto próprios, feitos na época.'),
    ('Reservas de localização, sem circuitos executivos. Posições existentes conforme marcação do cliente sobre o estudo anterior.',
     'Retrofit: troca de toda a fiação e dos espelhos, pontos existentes mantidos. Único ponto novo: T20, atrás do vaso.'),
    ('>RESERVAS DE INFRAESTRUTURA ELÉTRICA<', '>ESCOPO ELÉTRICO — RETROFIT<'),
    ('>Tomada nova (reserva)<', '>Ponto novo — só o T20<'),
    ('>Comando / interruptor<', '>Comandos existentes<'),
    ('a claraboia ganha fechamento elétrico em 2027/28, com a infraestrutura feita agora.',
     'a claraboia ganha fechamento elétrico em 2027/28, com ponto e eletroduto feitos na época.'),
]
PARES_FOLHA = {
    'prancha-08-banheiro': [('0,20  plenum', '0,12  plenum')],
    'prancha-10-banheiro': [
        ('Folha anterior às medidas de 14/11: quantidades e detalhes do banheiro valem pelo Executivo do Banheiro.',
         'Quantidades desta folha = Executivo do Banheiro E3 (15/11). Detalhes e paginação, só no executivo.'),
        ('Geometria interna do scan de 02.09.2026 nas faces de revestimento retirado: 1,432 × 2,638 m. O CSV arredonda box e perímetro; esta folha usa o medido e mostra os dois.',
         'Medidas de obra de 14/11/2026, faces acabadas: 1,42 × 2,68 m internos. Quantidades pela malha do Executivo E3, peça a peça.'),
        ('Arredondar por caixa só após a paginação do produto.', 'Compra arredondada por caixa: 26 caixas de Bleu Nuit.'),
        ('Quantitativo de acabamento sobre o layout existente. Pontos hidráulicos mantidos como hipótese até confirmar água, esgoto, aquecimento e interferência na laje.',
         'Resumo do Executivo do Banheiro E3: medidas de obra de 14/11, paginação real, nicho e bancada revestida.'),
        ('21,73 m² líquidos  ·  23,90 m² com 10%', '20,43 m² líquidos  ·  22,09 m² com 10%'),
        ('revestimento até 2,40 m — o forro fica', 'revestimento até 2,50 m — forro novo'),
        ('>SUPERFÍCIES — SEM DUPLA CONTAGEM<', '>SUPERFÍCIES — EXECUTIVO E3<'),
        ('>O QUE MUDOU DESDE A FOLHA DE 11.09<', '>O QUE MUDOU DESDE A REV. U<'),
        ('>2,40 m<', '>2,50 m<'), ('>até o forro<', '>até o forro novo<'),
        ('BOX  1,43 × 0,93', 'BOX  1,42 × 0,92'), ('>2,47 m²<', '>2,50 m²<'), ('>1,33 m²<', '>1,31 m²<'),
        ('>1,43 m<', '>1,42 m<'), ('>2,64 m<', '>2,68 m<')],
}


FOLHAS = (
    (_com_at(construir_01, (722, 800, 628), (132, 182, 64.0, 6.2), AT_TXT), 'alt-a-v-prancha-01-planta-cotada', 'Prancha 01: planta baixa cotada'),
    (_com_at(construir_02, CX, P70, extra=EXTRA_DEMO), 'alt-a-v-prancha-02-demolicao', 'Prancha 02: demolição e desmontagem'),
    (_com_at(lambda: construir_piso_s('A'), CX, P70, extra=EXTRA_03A), 'alt-a-v-prancha-03-piso-monolitico-integral', 'Prancha 03: piso monolítico integral'),
    (_com_at(lambda: construir_piso_s('B'), CX, P70, extra=EXTRA_03B), 'alt-a-v-prancha-04-piso-porcelanato-monolitico', 'Prancha 04: piso porcelanato + monolítico'),
    (_com_at(construir_teto_fas, CX, P70, extra=EXTRA_TETO), 'alt-a-v-prancha-05-teto', 'Prancha 05: teto'),
    (_com_at(construir_eletrica, CX, P70, extra=EXTRA_ELE), 'alt-a-v-prancha-06-eletrica', 'Prancha 06: elétrica'),
    (_com_at(p06.construir, (70, 150, 600), desenho=False), 'alt-a-v-prancha-07-esquadrias', 'Prancha 07: esquadrias'),
    (_com_at(p07.construir, (70, 818, 345), [_plano_wc(190, 222.0, 118.0) + (7.0, True)]), 'alt-a-v-prancha-08-banheiro', 'Prancha 08: banheiro'),
    (_com_at(p09.construir, (722, 820, 628), desenho=False), 'alt-a-v-prancha-09-medicao', 'Prancha 09: medição e decisões'),
    (_com_at(p10.construir, (70, 640, 600), desenho=False, extra=EXTRA_WC), 'alt-a-v-prancha-10-banheiro-acabamentos', 'Prancha 10: banheiro, acabamentos'),
    (_com_at(construir_11_fas, (755, 450, 590), desenho=False), 'alt-a-v-prancha-11-ar-luz', 'Prancha 11: ar, exaustão e iluminação'),
    (_com_at(construir_riscos_r, None, desenho=False), 'alt-a-v-prancha-12-riscos', 'Prancha 12: riscos'),
    (_com_at(construir_quarto_s, (66, 660, 138), desenho=False, extra=EXTRA_13), 'alt-a-v-prancha-13-quarto-claraboia', 'Prancha 13: quarto adaptável e claraboia'),
    (_com_at(p14.construir, None, desenho=False), 'alt-a-v-prancha-14-programacao', 'Prancha 14: programação da obra'),
)
FOLHAS_FO = (
    (_com_at(folha_demolicao_alt, (178, 138, 168, 7.0), (70, 156, 63.0, 6.0), extra=EXTRA_DEMO), 'alt-a-v-fornecedor-01-demolicao', 'FO1: demolição e preparo'),
    (_com_at(folha_piso_s, (1130 - 340, 820, 560), [(70, 200, 40.0, 5.0), (414, 200, 40.0, 5.0)], extra=EXTRA_03), 'alt-a-v-fornecedor-02-piso', 'FO2: piso'),
    (_com_at(fo.folha_eletrica, (165, 138, 180, 7.0), (70, 156, 63.0, 6.0), extra=EXTRA_ELE), 'alt-a-v-fornecedor-03-eletrica', 'FO3: elétrica'),
    (_com_at(folha_iluminacao_fas, (162, 136, 143, 6.6), (70, 156, 54.0, 5.6), AT_MINI, EXTRA_TETO), 'alt-a-v-fornecedor-04-iluminacao', 'FO4: iluminação'),
    (_com_at(fo.folha_ar, (160, 134, 125, 6.3), (70, 156, 49.0, 5.4), AT_MINI, EXTRA_AR), 'alt-a-v-fornecedor-05-ar', 'FO5: ar-condicionado e exaustão'),
    (_com_at(fo.folha_cortina, (722, 760, 628), desenho=False), 'alt-a-v-fornecedor-06-cortina-claraboia', 'FO6: cortina e claraboia'),
    (_com_at(fo.folha_pedras_vidro_portas, (722, 820, 628), desenho=False), 'alt-a-v-fornecedor-07-pedras-vidro-portas', 'FO7: pedras, vidro do box e portas'),
    (_com_at(fo.folha_programacao, None, desenho=False), 'alt-a-v-fornecedor-08-programacao', 'FO8: programação da obra'),
)

if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    so = set(sys.argv[1:])
    geometria(True)
    for grupo, caderno, titulo_cad in (
            (FOLHAS, 'caderno-alternativo-a-rev-v-A3.pdf',
             'MaxHaus MainFloor — Caderno Alternativo A, REV. V (A3)'),
            (FOLHAS_FO, 'caderno-fornecedores-alternativo-a-rev-v-A3.pdf',
             'MaxHaus 81I — pacote para fornecedores, Alternativo A, REV. V (A3)')):
        saidas = []
        for fn, nome, titulo in grupo:
            if so and not any(s in nome for s in so):
                continue
            d_ = fn()
            for _i, _s in enumerate(d_.o):          # REV. U: a parede sala de TV/quarto não é refeita
                for _a, _b in (('na drywall reconstruída', 'na parede mantida'), ('na drywall R01', 'na parede sala/quarto'),
                               ('e drywall ainda sem porta', 'e o vão atual da porta sala de TV/quarto'),
                               ('fechar a drywall R01', 'requadrar o vão R01')) + tuple(PARES_REV_V) + \
                              tuple(par for k, v in PARES_FOLHA.items() if k in nome for par in v) + \
                              (('drywall R01', 'parede sala/quarto'),):
                    if _a in _s:
                        _s = _s.replace(_a, _b)
                d_.o[_i] = _s
            caminho = salvar(d_, pasta, nome)
            exportar_pdf_a3([caminho], os.path.join(pasta, nome + '-A3.pdf'),
                            'MaxHaus MainFloor — Alternativo A, REV. V — ' + titulo)
            exportar_png(caminho, os.path.join(pasta, nome + '.png'))
            saidas.append(caminho)
        if not so:
            exportar_pdf_a3(saidas, os.path.join(pasta, caderno), titulo_cad)
        print('ok %d folhas' % len(saidas))
    geometria(False)
