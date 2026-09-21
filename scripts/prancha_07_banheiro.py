# -*- coding: utf-8 -*-
"""Prancha 08 — Banheiro: planta detalhada, teto refletido e cotas de nível.

O banheiro é o ponto mais denso do pavimento: desce até a laje, é o único
ambiente que mantém forro, recebe sistema de área molhada e tem de voltar
na mesma cota do piso da casa. Esta folha isola esse trecho em escala grande.

Geometria interna lida do scan (pág. 2), faces internas de revestimento
retirado: 1,432 x 2,638 m, 3,78 m².
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa
from base_mainfloor import _tick
from prancha_04_teto import EMBUTIDOS_WC

REV = 'REV. M'
PRANCHA = 'Prancha 08 / 12'

# --- faces do banheiro, em pt do scan ---------------------------------------
WC_O, WC_L = 347.96, 413.33        # faces internas oeste e leste
WC_N, WC_S = 330.22, 450.67        # faces internas norte e sul
WC_OE, WC_LE = 343.39, 417.90      # faces externas
WC_NE, WC_SE = 325.65, 455.24

WC_W_M = (WC_L - WC_O) / PT_PER_M  # 1,432
WC_H_M = (WC_S - WC_N) / PT_PER_M  # 2,638

# --- paredes do trecho ------------------------------------------------------
PAREDES_WC = [
    (WC_OE, WC_NE, WC_O, WC_SE),      # oeste
    (WC_L, WC_NE, WC_LE, WC_SE),      # leste
    (WC_OE, WC_NE, WC_LE, WC_N),      # norte
    (WC_OE, WC_S, WC_LE, WC_SE),      # sul — R02, parede nova
]

TAB_DEMO_WC = [
    ('D03', 'Retirar piso, base e rebaixo até a laje', '3,80 m²'),
    ('D02', 'Demolir fechamento e base do box', '1 conjunto'),
    ('D06', 'Demolir pano de vidro chão-teto do fundo do box', '1,63 m'),
    ('D04', 'Demolir parede atrás do espelho e da bancada', '2,64 m a conferir'),
    ('K01', 'Vidro interno do box — MANTER e proteger', '1 peça'),
]
TAB_RECON_WC = [
    ('R02', 'Parede de fechamento do fundo do box, no lugar do vidro', '1,63 m'),
    ('P02', 'Porta 0,80 × 2,00 m, giro invertido — abre para a escada', '1 vão'),
    ('P05', 'Nivelar o banheiro na cota do piso da casa', 'cota única'),
]
TAB_PISO_WC = [
    ('C1', 'Impermeabilização de área molhada, com rodapé virado', '3,80 m²'),
    ('C2', 'Regularização com caimento para o ralo linear', '3,80 m²'),
    ('C3', 'Ralo linear no fundo do box, na face da parede R02', '1,43 m'),
    ('C4', 'Piso acabado, na mesma cota da casa', '3,80 m²'),
    ('C5', 'Soleira: junta de material no vão da porta, sem degrau', '0,80 m'),
]
TAB_INST_WC = [
    ('EM',   'Embutidos no forro — 2 pontos, eixo a 4,85 m', '2 pontos'),
    ('EX01', 'Exaustor no forro — 92,0 m³/h de referência', '1 ponto'),
    ('T17',  'Tomada do lavatório, a validar em volume de proteção', '1 ponto'),
    ('S03',  'Comando das arandelas do espelho, junto à bancada', '1 ponto'),
    ('S04',  'Comando do banheiro, fora do ambiente, na quina do box', '1 ponto'),
    ('E1–E3', 'Pontos existentes: arandelas do espelho e luz do box', '3 pontos'),
]

NOTAS = [
    ['**O banheiro é o único ambiente que mantém forro.',
     'Altura livre de 2,42 m, contra 2,62 m no resto do pavimento, onde a laje fica aparente.',
     'É por isso que só aqui cabem embutido e exaustor — fora daqui, tudo é aplicado na laje.'],
    ['**Descer até a laje e voltar na cota da casa é o problema desta folha.',
     'O piso, a base e o rebaixo saem (D03) e o pavimento passa a ter cota única (P05): a soleira',
     'vira junta de material, não degrau. Toda a espessura de impermeabilização, caimento e piso',
     'tem de caber entre a laje e essa cota — medir o desnível real antes de fechar o sistema.'],
    ['**A contenção de água passa a ser o ralo linear, não o degrau.',
     'Sem degrau na soleira, o caimento e o ralo no fundo do box são o que retém a água.',
     'O caimento é executado na regularização, sobre a impermeabilização, nunca no piso acabado.'],
    ['**O vidro interno do box (K01) fica.',
     'Sai o pano de vidro chão-teto do fundo (D06) e entra parede (R02); o vidro que divide o box',
     'do resto do banheiro é para manter e proteger durante toda a obra.'],
    ['**A porta abre para fora, no sentido da escada.',
     'Ganha área útil dentro do banheiro e libera a faixa junto à bancada. O giro passa a ocupar',
     'o patamar: conferir se a folha aberta não invade a passagem da escada.'],
]


def _plan_wc(d, ox, oy, S):
    """Posiciona o plano de modo que a quina externa noroeste do banheiro
    caia em (ox, oy)."""
    d.set_plan(ox - mx(WC_OE) * S, oy - my(WC_NE) * S, S)


def planta_detalhe(d, ox, oy, S, cotas=True):
    _plan_wc(d, ox, oy, S)
    # piso do banheiro
    r = d.R((WC_O, WC_N, WC_L, WC_S))
    d.rect(r[0], r[1], r[2], r[3], fill=WET)
    # box, mais claro, e o vidro que fica
    b = d.R((WC_O, 408.20, WC_L, WC_S))
    d.rect(b[0], b[1], b[2], b[3], fill=CIANO18, stroke=WET_LINE, sw=0.8)
    g = d.R(VIDRO_BOX_INT)
    d.rect(g[0], g[1], g[2], max(g[3], 2.4), fill=CIANO, stroke=K, sw=1.2)
    # ralo linear, na face da parede nova
    ra = d.P(WC_O + 2.0, WC_S - 7.0)
    rb = d.P(WC_L - 2.0, WC_S - 2.0)
    d.rect(ra[0], ra[1], rb[0] - ra[0], rb[1] - ra[1], fill=BRANCO, stroke=K, sw=1.2)
    for i in range(14):
        xx = ra[0] + 3 + i * (rb[0] - ra[0] - 6) / 13.0
        d.line(xx, ra[1] + 1.5, xx, rb[1] - 1.5, K45, 0.7)
    # setas de caimento
    for xm in (0.38, 0.72, 1.06):
        p0 = d.P(WC_O + xm * PT_PER_M, WC_N + 90.0)
        p1 = d.P(WC_O + xm * PT_PER_M, WC_S - 18.0)
        d.line(p0[0], p0[1], p1[0], p1[1], WET_LINE, 0.9, opacity=0.9)
        d.path('M%.1f %.1f L%.1f %.1f L%.1f %.1f' %
               (p1[0] - 3.2, p1[1] - 5.0, p1[0], p1[1], p1[0] + 3.2, p1[1] - 5.0),
               fill='none', stroke=WET_LINE, sw=1.1)
    # bancada e espelho, na parede oeste
    bc = d.R(BANCADA_WC)
    d.rect(bc[0], bc[1], bc[2], bc[3], fill=BRANCO, stroke=K, sw=1.2)
    d.line(bc[0], bc[1], bc[0], bc[1] + bc[3], K, 3.0)
    # paredes
    for w in PAREDES_WC:
        r = d.R(w)
        d.rect(r[0], r[1], r[2], r[3], fill=WALL, stroke=WALL, sw=0.4)
    # parede nova R02 marcada
    r = d.R((WC_OE, WC_S, WC_LE, WC_SE))
    d.rect(r[0], r[1], r[2], r[3], fill=WALL, stroke=DEMO, sw=2.0)
    # parede oeste com revestimento retirado (D04)
    r = d.R((WC_OE, WC_NE, WC_O, WC_SE))
    d.rect(r[0] - 3.0, r[1], 3.0, r[3], fill=AMARELO, stroke=K, sw=0.5)
    # vão e folha da porta, abrindo para fora (leste), dobradiça no batente norte
    pr = d.R((WC_L, 351.00, WC_LE, 387.30))
    d.rect(pr[0], pr[1], pr[2], pr[3], fill=BG)
    vaol = abs(pr[3])
    x0 = pr[0] + pr[2]
    d.path('M%.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f' %
           (x0 + vaol, pr[1], vaol, vaol, x0, pr[1] + vaol),
           fill='none', stroke=GHOST, sw=0.8)
    d.line(x0, pr[1], x0 + vaol, pr[1], K, 2.6)
    # rótulos do trecho
    cx, cy = d.P((WC_O + WC_L) / 2.0, 392.0)
    d.txt(cx, cy, 'BANHEIRO', 8.6, INK, 'bold', 'middle', ls=0.9)
    d.txt(cx, cy + 11, '3,80 m²', 7.4, INK_SOFT, 'normal', 'middle')
    cx, cy = d.P((WC_O + WC_L) / 2.0, 430.0)
    d.txt(cx, cy, 'BOX', 8.0, INK, 'bold', 'middle', ls=0.9)
    cx, cy = d.P((WC_O + WC_L) / 2.0, VIDRO_BOX_INT[1])
    d.txt(cx, cy - 5, 'K01  vidro que fica', 6.6, INK, 'bold', 'middle', ls=0.3)
    cx, cy = d.P((WC_O + WC_L) / 2.0, WC_S - 9.0)
    d.txt(cx, cy - 5, 'C3  ralo linear', 6.6, INK, 'bold', 'middle', ls=0.3)
    cx, cy = d.P((WC_OE + WC_LE) / 2.0, WC_SE)
    d.txt(cx, cy + 15, 'R02  parede nova no lugar do vidro chão-teto', 6.8, DEMO,
          'bold', 'middle', ls=0.3)
    cx, cy = d.P((BANCADA_WC[0] + BANCADA_WC[2]) / 2.0, BANCADA_WC[1])
    d.txt(cx + 22, cy - 6, 'BANCADA  ·  D04 revestimento sai', 6.4, INK, 'bold',
          'start', ls=0.3)
    cx, cy = d.P(WC_LE, (351.00 + 387.30) / 2.0)
    d.txt(cx + 8, cy + 14, 'P02', 6.8, INK, 'bold', 'start', ls=0.3)
    if cotas:
        cadeia_h(d, [WC_OE, WC_O, WC_L, WC_LE], WC_NE, -26)
        cota_h(d, WC_OE, WC_LE, WC_NE, -50, texto='1,63  externo')
        cadeia_v(d, [WC_NE, WC_N, 408.20, WC_S, WC_SE], WC_OE, -30)
        cota_v(d, WC_NE, WC_SE, WC_OE, -56, texto='2,84  externo')
        cota_v(d, 351.00, 387.30, WC_OE, -84, texto='0,80  vão')
        cota_v(d, BANCADA_WC[1], BANCADA_WC[3], WC_OE, -110, texto='0,61  bancada')
    return d


def teto_refletido(d, ox, oy, S):
    _plan_wc(d, ox, oy, S)
    r = d.R((WC_O, WC_N, WC_L, WC_S))
    d.rect(r[0], r[1], r[2], r[3], fill=K04, stroke=K45, sw=0.7)
    for w in PAREDES_WC:
        rr = d.R(w)
        d.rect(rr[0], rr[1], rr[2], rr[3], fill=WALL, stroke=WALL, sw=0.4)
    # embutidos e exaustor
    for (xm, ym) in EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 6.0, fill=BG, stroke=K, sw=1.3)
        d.circle(cx, cy, 2.0, fill=K)
    cx, cy = d.PM(2.95, 4.85)
    d.txt(cx, cy - 11, 'EM', 6.6, K, 'bold', 'middle', ls=0.3)
    cx, cy = d.PM(3.06, 6.06)
    d.rect(cx - 11, cy - 8, 22, 16, fill=CIANO35, stroke=K, sw=1.2)
    d.txt(cx, cy + 3.4, 'EX01', 6.4, K, 'bold', 'middle', ls=0.3)
    cx, cy = d.P((WC_O + WC_L) / 2.0, WC_S - 6.0)
    d.txt(cx, cy, 'forro mantido  ·  2,42 m livres', 6.6, INK_SOFT, 'normal',
          'middle', ls=0.3)
    # pontos existentes
    for (ident, xm, ym, nome) in (('E1', 2.55, 5.15, ''), ('E2', 3.05, 5.15, ''),
                                  ('E3', 3.05, 5.70, '')):
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.2, fill='none', stroke=K45, sw=1.0)
        d.txt(cx + 7, cy + 2.2, ident, 6.0, K45, 'normal', 'start')
    return d


def corte_niveis(d, x, y, largura):
    """Corte esquemático: da laje ao piso acabado, em cota única com a casa."""
    d.txt(x, y - 10, 'CORTE ESQUEMÁTICO DE NÍVEL — O BANHEIRO VOLTA NA COTA DA CASA',
          8.0, INK_SOFT, 'bold', ls=1.2)
    h = 78.0
    meio = x + largura * 0.52
    base = y + h
    # laje
    d.rect(x, base, largura, 13, fill=K20, stroke=K, sw=1.0)
    d.txt(x + 6, base + 9.6, 'LAJE ESTRUTURAL', 6.6, INK_SOFT, 'bold', ls=0.4)
    # camadas do banheiro, à esquerda
    camadas = [('impermeabilização', 7.0, CIANO),
               ('regularização com caimento', 15.0, CIANO18),
               ('piso acabado', 8.0, BRANCO)]
    yy = base
    for (nome, esp, cor) in camadas:
        yy -= esp
        d.rect(x, yy, meio - x, esp, fill=cor, stroke=K, sw=0.8)
        d.txt(x + (largura * 0.24 if nome == 'piso acabado' else 6), yy + esp - 2.4,
              nome, 6.4, INK, 'normal')
    topo_wc = yy
    # camadas da casa, à direita
    d.rect(meio, base - 22.0, x + largura - meio, 22.0, fill=MONO, stroke=K, sw=0.8)
    d.txt(meio + 8, base - 8.0, 'contrapiso regularizado (P06)', 6.4, INK, 'normal')
    d.rect(meio, base - 30.0, x + largura - meio, 8.0, fill=BRANCO, stroke=K, sw=0.8)
    d.txt(meio + 8, base - 24.0, 'piso acabado', 6.4, INK, 'normal')
    topo_casa = base - 30.0
    # cota única
    d.line(x - 6, topo_wc, x + largura + 6, topo_wc, DEMO, 1.4)
    d.txt(x + largura + 10, topo_wc + 3, 'COTA ÚNICA', 7.0, DEMO, 'bold', 'start', ls=0.5)
    if abs(topo_casa - topo_wc) > 0.6:
        d.line(meio, topo_casa, x + largura, topo_casa, DEMO, 1.4)
    # soleira: junta de material
    for i in range(5):
        d.line(meio, topo_wc + i * 5.5, meio, topo_wc + i * 5.5 + 3.2, DEMO, 2.0)
    d.txt(meio, topo_wc - 30, 'SOLEIRA', 6.6, DEMO, 'bold', 'middle', ls=0.4)
    d.txt(meio, topo_wc - 21, 'junta de material', 6.2, DEMO, 'normal', 'middle')
    d.txt(meio - 14, topo_wc - 8, 'BANHEIRO', 7.4, INK, 'bold', 'end', ls=0.6)
    d.txt(meio + 14, topo_wc - 8, 'CASA', 7.4, INK, 'bold', 'start', ls=0.6)
    # ralo
    rx = x + largura * 0.085
    d.rect(rx - 9, topo_wc, 18, 6, fill=BRANCO, stroke=K, sw=1.0)
    d.txt(rx, topo_wc - 5, 'ralo linear', 6.2, INK_SOFT, 'normal', 'middle')
    d.txt(x, base + 30, 'Espessuras fora de escala. O total das camadas do banheiro tem de caber '
          'entre a laje e a cota única: medir o desnível real após a D03.',
          7.2, INK_SOFT)
    return base + 42


def corte_altura(d, x, y, largura):
    """Altura livre: o banheiro mantém forro, o resto do pavimento não."""
    d.txt(x, y - 10, 'ALTURA LIVRE — O BANHEIRO É A EXCEÇÃO', 8.0, INK_SOFT,
          'bold', ls=1.2)
    h = 130.0                     # 2,62 m de pé-direito
    esc_v = h / PE_DIREITO
    base = y + h + 14
    lg = largura * 0.42
    gap = largura - 2 * lg
    for i, (rot, livre, forro) in enumerate(
            (('BANHEIRO', PE_DIREITO_FORRO, True), ('RESTO DO PAVIMENTO', PE_DIREITO, False))):
        xx = x + i * (lg + gap)
        topo = base - PE_DIREITO * esc_v
        # laje
        d.rect(xx, topo - 9, lg, 9, fill=K20, stroke=K, sw=0.9)
        # piso
        d.rect(xx, base, lg, 7, fill=MONO, stroke=K, sw=0.9)
        # ar
        d.rect(xx, topo, lg, base - topo, fill=BG, stroke=K45, sw=0.5)
        if forro:
            yf = base - livre * esc_v
            d.rect(xx, topo, lg, yf - topo, fill=CIANO18, stroke=CIANO, sw=0.9)
            d.line(xx, yf, xx + lg, yf, K, 1.6)
            d.txt(xx + lg / 2.0, (yf + topo) / 2.0 + 2.4, '0,20  plenum', 5.8, INK,
                  'normal', 'middle')
            d.txt(xx + lg / 2.0, yf + 10, 'forro', 6.2, INK_SOFT, 'normal', 'middle')
        cota_v_px(d, xx + 14, base - livre * esc_v, base, br(livre))
        d.txt(xx + lg / 2.0, base + 20, rot, 6.8, INK, 'bold', 'middle', ls=0.4)
    for i, ln in enumerate(('A retirada do forro (D07) devolve 0,20 m fora',
                            'do banheiro. Dentro dele o forro fica, para',
                            'abrigar embutido e exaustor.')):
        d.txt(x, base + 40 + i * 11, ln, 7.2, INK_SOFT)
    return base + 74


def cota_v_px(d, x, y0, y1, texto):
    d.line(x, y0, x, y1, DIM, 0.7)
    _tick(d, x, y0, True); _tick(d, x, y1, True)
    d.txt(x - 4, (y0 + y1) / 2.0, texto, 7.0, DIM_TXT, 'normal', 'middle', rot=-90.0)


def construir():
    d = folha_nova()
    cabecalho(d, 'Banheiro: planta detalhada',
              'O trecho mais denso do pavimento, em escala grande. Desce até a laje, mantém forro e volta na cota única da casa. Cotas em faces internas, com o revestimento retirado.',
              REV, '1,43 × 2,64 m  ·  3,80 m²',
              'único ambiente com forro — 2,42 m livres')

    S = 118.0
    OY = 222.0
    d.txt(190, 148, 'PLANTA  ·  faces internas', 10.5, K, 'bold')
    planta_detalhe(d, 190, OY, S)

    d.txt(492, 148, 'TETO REFLETIDO  ·  forro', 10.5, K, 'bold')
    teto_refletido(d, 492, OY, S)
    norte(d, 660, 176, 12, nota=None)

    base_pl = OY + 2.84 * S
    d.set_plan(70, OY, S)
    escala(d, base_pl + 34)
    legenda(d, [('fill', WET, 'Área molhada'), ('fill', CIANO, 'Vidro do box — manter (K01)'),
                ('fill', AMARELO, 'Revestimento retirado (D04)'),
                ('line', DEMO, 'Parede nova (R02) e cota única')],
            70, base_pl + 70, largura=600)

    corte_niveis(d, 70, base_pl + 128, 330)
    corte_altura(d, 470, base_pl + 128, 210)

    d.line(690, 140, 690, 916, RULE, 0.8, opacity=0.8)
    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 158, cw,
                 [('ID', 0.11, 'start'), ('O que sai', 0.65, 'start'),
                  ('Quantidade', 0.24, 'end')],
                 TAB_DEMO_WC, titulo='DEMOLIÇÃO DO BANHEIRO', alt=18)
    fim = tabela(d, cx, fim + 32, cw,
                 [('ID', 0.11, 'start'), ('O que volta', 0.65, 'start'),
                  ('Quantidade', 0.24, 'end')],
                 TAB_RECON_WC, titulo='RECONSTRUÇÃO', alt=18)
    fim = tabela(d, cx, fim + 32, cw,
                 [('ID', 0.11, 'start'), ('Sistema de área molhada', 0.65, 'start'),
                  ('Quantidade', 0.24, 'end')],
                 TAB_PISO_WC, titulo='PISO E IMPERMEABILIZAÇÃO', alt=18)
    fim = tabela(d, cx, fim + 32, cw,
                 [('ID', 0.13, 'start'), ('Instalação', 0.63, 'start'),
                  ('Quantidade', 0.24, 'end')],
                 TAB_INST_WC, titulo='INSTALAÇÕES NO TRECHO', alt=18)
    paragrafos(d, cx, fim + 26, cw, NOTAS, size=8.3, lh=11.9, gap=5.8)

    rodape(d,
           'Geometria interna lida do scan de 02.09.2026 nas faces de revestimento retirado: 1,432 × 2,638 m, 3,78 m². Conferir em campo após a D03, quando a laje estiver exposta.',
           'Louças e metais não estão levantados — o scan reconheceu bancada e box. Espessuras do corte são esquemáticas: sistema de impermeabilização e desnível de laje se definem em obra, com o piso escolhido.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-08-banheiro')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-08-banheiro-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 08: banheiro, planta detalhada')
    exportar_png(caminho, os.path.join(pasta, 'prancha-08-banheiro.png'))
    print('ok prancha 08')
