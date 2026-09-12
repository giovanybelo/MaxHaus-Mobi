# -*- coding: utf-8 -*-
"""
Base gráfica do caderno MaxHaus MainFloor.

Geometria extraída do levantamento "MaxHaus_Mainfloor.pdf" (scan de 02.09.2026,
pág. 2): paredes, aberturas e polígonos de ambiente foram lidos do vetor
original em pontos PDF e convertidos para metros pela escala 45,66 pt/m,
conferida contra as cotas gerais do pavimento (7,85 m x 9,43 m).

Dois estados convivem no caderno:
  ESTADO EXISTENTE (Prancha 02) — o fundo do box é um pano de vidro chão-teto,
  ponta a ponta (o scan o leu como vão) e a drywall entre sala e quarto não tem
  porta.
  ESTADO PROPOSTO (Pranchas 03, 04 e 05) — o pano de vidro sai e entra uma
  parede fechando o box; a drywall é refeita com uma porta de correr de
  1,00 x 2,29 m; a porta do banheiro abre para fora, no sentido da escada.

Demais decisões do cliente embutidas na base:
  · o teto é laje de concreto aparente — não há forro, salvo no banheiro;
  · a área da piscina do pavimento superior está centrada em (6,13 / 3,14) m,
    medida do canto noroeste, e condiciona luz, ar e furação da laje.

Todas as pranchas do caderno fecham em A3 deitado (420 x 297 mm).
"""
import math
import os

# ---------------------------------------------------------------------------
# 1. GEOMETRIA (pontos PDF do scan)
# ---------------------------------------------------------------------------
ORIGIN_X, ORIGIN_Y = 245.7, 124.38
PT_PER_M = 45.66
BUILDING_W, BUILDING_H = 7.85, 9.43

def mx(v): return (v - ORIGIN_X) / PT_PER_M
def my(v): return (v - ORIGIN_Y) / PT_PER_M
def px_(m_): return m_ * PT_PER_M + ORIGIN_X      # metro -> pt (eixo x)
def py_(m_): return m_ * PT_PER_M + ORIGIN_Y      # metro -> pt (eixo y)

ROOMS = {
    'jantar': dict(label='JANTAR', area=5.90, lx=525.0, ly=165.0,
        poly=[(448.4,126.7),(601.7,126.7),(601.7,211.2),(448.4,211.2)]),
    'sala': dict(label='SALA', area=23.00, lx=508.0, ly=285.0,
        poly=[(345.7,211.2),(601.7,211.2),(601.7,432.3),(415.6,432.3),
              (415.6,327.9),(345.7,327.9)]),
    'cozinha': dict(label='COZINHA', area=8.90, lx=297.0, ly=368.0,
        poly=[(277.8,211.2),(345.7,211.2),(345.7,432.3),(248.0,432.3),
              (248.0,284.8),(277.8,284.8)]),
    'banheiro': dict(label='BANHEIRO', area=3.80, lx=380.6, ly=360.0,
        poly=[(345.7,327.9),(415.6,327.9),(415.6,453.0),(345.7,453.0)]),
    'closet': dict(label='CLOSET', area=5.30, lx=314.0, ly=498.0,
        poly=[(248.0,432.3),(345.7,432.3),(345.7,552.7),(248.0,552.7)]),
    'quarto': dict(label='QUARTO', area=13.40, lx=505.0, ly=500.0,
        poly=[(415.6,432.3),(601.7,432.3),(601.7,552.7),(345.7,552.7),
              (345.7,453.0),(415.6,453.0)]),
}
ROOM_ORDER = ['jantar','sala','cozinha','closet','quarto','banheiro']

WALLS = [
    (446.11,124.38,604.03,128.94), (275.52,208.91,450.68,213.47),
    (275.52,208.91,280.09,287.11), (245.70,282.54,280.09,287.11),
    (279.36,430.06,345.67,434.63), (345.67,550.38,604.03,554.94),
    (343.39,432.34,347.96,455.24), (343.39,325.65,347.96,432.34),
    (415.61,430.06,601.74,434.63),
    (413.33,325.65,417.90,432.34), (599.46,432.34,604.03,554.94),
    (279.36,430.06,283.92,545.96), (245.70,550.38,345.67,554.94),
    (343.39,513.42,347.96,552.66), (446.11,124.38,450.68,213.47),
    (413.33,432.34,417.90,455.24), (599.46,124.38,604.03,432.34),
    (245.70,282.54,250.26,554.94), (343.39,325.65,417.90,330.22),
]
# fundo do box no estado existente: pano de vidro chão-teto, ponta a ponta.
# Será derrubado e substituído por parede (PAREDE_FUNDO_BOX).
VIDRO_BOX = (343.39, 450.67, 417.90, 455.24)
PAREDE_FUNDO_BOX = (343.39, 450.67, 417.90, 455.24)
# drywall sala/quarto: demolida e refeita, agora com porta
DRYWALL_SALA_QUARTO = (415.61, 430.06, 601.74, 434.63)
PORTA_NOVA = (416.90, 430.06, 462.50, 434.63)      # 1,00 x 2,29 m, de correr
PORTA_ENTRADA_H = 2.29                              # altura de referência
# parede do jantar / sob a escada: revestimento retirado e preparo para pintura
PAREDE_ESCADA_JANTAR = (446.11, 124.38, 450.68, 213.47)
PAREDE_SOB_ESCADA = (321.40, 208.91, 459.40, 213.47)

DOOR_ENTRADA = dict(rect=(275.52,220.10,280.09,265.76), hinge='n', leaf='e')  # 1,00 m
DOOR_BANHO   = dict(rect=(413.33,351.00,417.90,387.30), hinge='n', leaf='e')
JANELAS = [
    (599.46,142.50,604.03,193.20), (599.46,215.00,604.03,300.80),
    (599.46,348.00,604.03,394.40), (599.46,455.70,604.03,509.80),
    (251.40,550.38,342.00,554.94), (354.00,550.38,408.10,554.94),
]
ESCADA = dict(rect=(321.40,213.47,459.40,251.70), degraus=11)

# --- elementos existentes lidos do scan (para alvos de demolição) -----------
BANCADA_WC   = (347.96, 352.00, 366.00, 380.00)   # bancada + espelho (parede oeste)
BOX_WC       = (347.96, 408.20, 413.33, 450.67)   # box do banheiro
VIDRO_BOX_INT= (347.96, 408.20, 413.33, 411.00)   # vidro interno do box (manter)
CANTO_ALEMAO = (450.68, 128.94, 599.46, 145.00)   # banco de canto do jantar

# --- ponta em curva da cozinha (opção A de piso) ---------------------------
# A curva nasce na quina do degrau da parede — logo abaixo da porta de entrada,
# onde fica a geladeira — e morre na parede do banheiro. Só faz sentido quando
# há dois materiais no piso: é ela que resolve o encontro cumaru × monolítico.
CURVA_CX, CURVA_CY = 277.8, 325.65
CURVA_RX, CURVA_RY = 67.90, 40.85
QUINA_DEGRAU = (277.8, 284.80)
CURVA_FIM    = (345.7, 325.65)

# zonas da opção A, em pt do scan
COZ_MONO_POLY = None       # preenchido abaixo, depois de arco_pts
COZ_HALL_POLY = None

def arco_pts(n=28, invertido=False):
    pts = []
    for i in range(n + 1):
        th = math.radians(90.0 * (1.0 - i / float(n)))
        pts.append((CURVA_CX + CURVA_RX * math.cos(th),
                    CURVA_CY - CURVA_RY * math.sin(th)))
    return list(reversed(pts)) if invertido else pts


COZ_MONO_POLY = ([(248.0, 432.3), (248.0, 284.8)] + arco_pts() + [(345.7, 432.3)])
COZ_HALL_POLY = ([(277.8, 211.2), (345.7, 211.2), (345.7, 325.65)]
                 + arco_pts(invertido=True))
AREA_COZ_MONO = 6.34       # m², parte monolítica da cozinha (de 8,90)
AREA_HALL = 2.56           # m², corredor da entrada que fica em cumaru

# --- área da piscina do pavimento superior ---------------------------------
# 1,92 x 3,00 m, centrada no cruzamento marcado pelo cliente (6,13 / 3,14 m).
PISCINA_CX, PISCINA_CY = 6.13, 3.14
PISCINA_W, PISCINA_H = 1.92, 3.00
AREA_PISCINA = (px_(PISCINA_CX - PISCINA_W / 2), py_(PISCINA_CY - PISCINA_H / 2),
                px_(PISCINA_CX + PISCINA_W / 2), py_(PISCINA_CY + PISCINA_H / 2))
AREA_PISCINA_M2 = PISCINA_W * PISCINA_H
AREA_TETO = AREA_PISCINA          # compatibilidade
AREA_TETO_M2 = AREA_PISCINA_M2

# --- dados do levantamento (relatório Polycam, captura 02.09.2026) ----------
# Alturas informadas pelo cliente (12.09.2026). O relatório do scan mede 2,40 m
# com o forro, o que confere com os 2,42 m abaixo; o plenum de 0,20 m é o que
# se ganha ao retirar o forro (D07).
PE_DIREITO = 2.62          # m, piso ao fundo da laje — depois da demolição
PE_DIREITO_FORRO = 2.42    # m, altura livre com o forro atual
PLENUM_FORRO = 0.20        # m, o que o forro consome
AREA_LIVABLE = 60.2        # m² (soma dos ambientes: 60,30)
AREA_EXTERIOR = 64.7       # m²
AREA_PAREDES = 130.4       # m²
AREA_JANELAS = 14.77       # m² — vão, com as alturas do cliente (o scan dava 12,70)
VOLUME_TOTAL = 144.51      # m³ com forro; 158,0 m³ com a laje aparente
PERIMETRO_AMBIENTES = 78.1 # m

# J06 é do piso ao teto: 2,42 m de altura livre menos 0,15 m de apoio no topo
# e 0,10 m de peitoril — os únicos 0,10 m de peitoril medidos até agora.
# esquadrias: (id, tipo, ambiente, larg, alt, área, situação)
ESQUADRIAS = [
    ('J01', 'Janela', 'Jantar',   1.10, 1.63, 1.79, 'manter'),
    ('J02', 'Janela', 'Sala',     1.90, 1.63, 3.10, 'manter'),
    ('J03', 'Janela', 'Sala',     1.00, 1.63, 1.63, 'manter'),
    ('J04', 'Janela', 'Quarto',   1.20, 1.63, 1.96, 'manter'),
    ('J05', 'Janela', 'Quarto',   1.20, 1.63, 1.96, 'manter'),
    ('J06', 'Janela', 'Closet',   2.00, 2.17, 4.34, 'manter — do piso ao teto'),
    ('P01', 'Porta',  'Entrada',  1.00, 2.29, 2.29, 'manter'),
    ('P02', 'Porta',  'Banheiro', 0.80, 2.00, 1.64, 'giro invertido — abre p/ escada'),
    ('P03', 'Porta de correr', 'Quarto', 1.00, 2.29, 2.29, 'nova, na drywall R01'),
]

# ambientes: (nome, área, perímetro, bounding box, inscrita, parede s/ vãos)
AMBIENTES_SCAN = [
    ('Sala',     23.0, 20.7, '5,6 × 4,8', '4,8 × 4,0', 29.8),
    ('Quarto',   13.4, 16.2, '5,6 × 2,5', '5,6 × 2,1', 30.3),
    ('Cozinha',   8.9, 13.7, '4,7 × 2,1', '4,7 × 1,4', 23.3),
    ('Jantar',    5.9, 10.1, '3,3 × 1,8', '—',         15.2),
    ('Closet',    5.3,  9.3, '2,5 × 2,1', '—',         14.9),
    ('Banheiro',  3.8,  8.1, '2,6 × 1,4', '—',         16.7),
]

# --- norte -----------------------------------------------------------------
# 0° = norte para o topo da folha; o ângulo cresce no sentido horário.
#
# Medido, não arbitrado: o relatório do Upfloor (mesma captura, 02.09.2026) traz
# rosa dos ventos e GPS — o do MainFloor não traz nenhum dos dois. A pétala
# rotulada N do Upfloor aponta a −53,97° do topo daquela folha, e as duas plantas
# estão desenhadas com 180° de diferença (confirmado por dois elementos que os
# pavimentos compartilham: a caixa da escada e a área da piscina, que só cai no
# terraço do Upfloor com essa rotação). Logo, no MainFloor: −53,97 + 180 = 126°.
NORTE_DEG = 126.0
NORTE_CONFIRMADO = True
GPS_LAT, GPS_LON, GPS_ALT = -23.612988, -46.737727, 822

# rumo das fachadas, deduzido do norte acima
FACHADAS = [
    ('Leste da folha', 'J01, J02, J03, J04', '324° — noroeste', 'sol de tarde, o mais quente'),
    ('Sul da folha',   'J05, J06',           '54° — nordeste',  'sol de manhã'),
    ('Oeste da folha', 'parede cega',        '144° — sudeste',  'divisa'),
    ('Norte da folha', 'parede cega',        '234° — sudoeste', 'divisa'),
]

# ---------------------------------------------------------------------------
# 2. PALETA
# ---------------------------------------------------------------------------
# Identidade visual: quatro tintas puras — preto, ciano, magenta e amarelo —
# mais o branco do papel. Tudo o que parece cinza ou pastel aqui é porcentagem
# de uma dessas tintas, do jeito que uma gráfica trabalha.
K         = '#000000'
K70       = '#4d4d4d'
K45       = '#8c8c8c'
K20       = '#cccccc'
K12       = '#e0e0e0'
K07       = '#ededed'
K04       = '#f5f5f5'
CIANO     = '#00ffff'
CIANO35   = '#a6ffff'
CIANO18   = '#d6ffff'
MAGENTA   = '#ff00ff'
MAGENTA18 = '#ffd6ff'
AMARELO   = '#ffff00'
AMARELO40 = '#ffff99'
BRANCO    = '#ffffff'

# papel e traço
BG        = BRANCO
INK       = K
INK_SOFT  = K70
RULE      = K20
WALL      = K
GHOST     = K45
JOINT     = K
DIM       = K45
DIM_TXT   = K70

# códigos de cor do caderno
#   magenta = o que sai        ciano = água, ar e obra nova
#   amarelo = preparo/atenção  preto = o que fica, e toda a tipografia
DEMO      = MAGENTA        # demolir / retirar
PREP      = AMARELO        # preparo de superfície
KEEP      = K              # manter / reconstruir
NEW       = K              # ponto novo
EXIST     = K45            # ponto existente
AIR       = CIANO          # ar-condicionado e exaustão
GLASS     = CIANO
WET       = CIANO18        # área molhada
WET_LINE  = CIANO
MONO      = K07            # piso monolítico
MONO_LINE = K45
WOOD      = AMARELO        # sem uso desde a REV. F
WOOD_LINE = K
RED       = MAGENTA        # carimbo de advertência

# ---------------------------------------------------------------------------
# 3. FOLHA A3 E PRIMITIVAS
# ---------------------------------------------------------------------------
W, H = 1400, 990                      # proporção A3 deitado
FONT = "'Tiempos Text', 'Source Serif 4', Georgia, 'Times New Roman', Times, serif"
MARGIN = 48

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def br(v, casas=2):
    return (('%.' + str(casas) + 'f') % v).replace('.', ',')

class Draw(object):
    def __init__(self):
        self.o = []
        self.org = (0.0, 0.0)
        self.S = 55.0
    # --- primitivas ---------------------------------------------------------
    def add(self, s): self.o.append(s)
    def txt(self, x, y, t, size=10, fill=INK, weight='normal', anchor='start', ls=None, rot=None):
        a = ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" fill="%s" '
             'font-weight="%s" text-anchor="%s"' % (x, y, FONT, size, fill, weight, anchor))
        if ls: a += ' letter-spacing="%.2f"' % ls
        if rot: a += ' transform="rotate(%.1f %.1f %.1f)"' % (rot, x, y)
        self.add(a + '>' + esc(t) + '</text>')
    def line(self, x1, y1, x2, y2, stroke, w=1.0, opacity=None, cap=None):
        a = ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"'
             % (x1, y1, x2, y2, stroke, w))
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        if cap: a += ' stroke-linecap="%s"' % cap
        self.add(a + '/>')
    def rect(self, x, y, w_, h_, fill='none', stroke=None, sw=1.0, opacity=None, dash=None):
        a = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"' % (x, y, w_, h_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    def circle(self, x, y, r, fill='none', stroke=None, sw=1.0, opacity=None):
        a = '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"' % (x, y, r, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    def path(self, d_, fill='none', stroke=None, sw=1.0, opacity=None, dash=None):
        a = '<path d="%s" fill="%s"' % (d_, fill)
        if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
        if dash: a += ' stroke-dasharray="%s"' % dash
        if opacity is not None: a += ' opacity="%.2f"' % opacity
        self.add(a + '/>')
    # --- transformação planta ----------------------------------------------
    def set_plan(self, ox, oy, S):
        self.org = (ox, oy); self.S = S
    def P(self, x_pt, y_pt):
        return (self.org[0] + mx(x_pt) * self.S, self.org[1] + my(y_pt) * self.S)
    def PM(self, x_m, y_m):
        return (self.org[0] + x_m * self.S, self.org[1] + y_m * self.S)
    def R(self, r):
        a = self.P(r[0], r[1]); b = self.P(r[2], r[3])
        return (a[0], a[1], b[0] - a[0], b[1] - a[1])

def path_d(pp, close=True):
    d = ['%s%.2f %.2f' % ('M' if i == 0 else 'L', p[0], p[1]) for i, p in enumerate(pp)]
    return ' '.join(d) + (' Z' if close else '')

def bbox(pp):
    xs = [p[0] for p in pp]; ys = [p[1] for p in pp]
    return min(xs), min(ys), max(xs), max(ys)

def _spans(v):
    v.sort()
    return [(v[i], v[i + 1]) for i in range(0, len(v) - 1, 2)]

def spans_at_y(pp, y):
    xs = []
    n = len(pp)
    for i in range(n):
        x1, y1 = pp[i]; x2, y2 = pp[(i + 1) % n]
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return _spans(xs)

def spans_at_x(pp, x):
    ys = []
    n = len(pp)
    for i in range(n):
        x1, y1 = pp[i]; x2, y2 = pp[(i + 1) % n]
        if (x1 <= x < x2) or (x2 <= x < x1):
            ys.append(y1 + (x - x1) * (y2 - y1) / (x2 - x1))
    return _spans(ys)

# ---------------------------------------------------------------------------
# 4. DESENHO DA PLANTA
# ---------------------------------------------------------------------------
def fundo_ambientes(d, cor=MONO, opacity=1.0):
    for k in ROOM_ORDER:
        d.path(path_d([d.P(x, y) for x, y in ROOMS[k]['poly']]), fill=cor, opacity=opacity)

def paredes(d, estado='novo'):
    """estado='existente' mantém o fundo do box em vidro; 'novo' o fecha em parede."""
    for r in WALLS:
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill=WALL)
    if estado == 'novo':
        x, y, w_, h_ = d.R(PAREDE_FUNDO_BOX)
        d.rect(x, y, w_, h_, fill=WALL)

def vidro_box(d, rotulo=True):
    """Pano de vidro chão-teto no fundo do box, ponta a ponta."""
    x, y, w_, h_ = d.R(VIDRO_BOX)
    d.rect(x - 0.3, y - 0.3, w_ + 0.6, h_ + 0.6, fill=BG)
    d.rect(x, y, w_, h_, fill=CIANO18, stroke=K, sw=0.9)
    ym = y + h_ / 2.0
    d.line(x, ym, x + w_, ym, GLASS, 1.6)
    for t in (0.18, 0.5, 0.82):
        d.line(x + w_ * t, y, x + w_ * t, y + h_, GLASS, 0.7)

def vao(d, r):
    x, y, w_, h_ = d.R(r)
    d.rect(x - 0.3, y - 0.3, w_ + 0.6, h_ + 0.6, fill=BG)

def porta_horizontal(d, rect, hinge='w', swing='s'):
    """Porta em parede horizontal: dobradiça a oeste/leste, abrindo para norte/sul."""
    vao(d, rect)
    x, y, w_, h_ = d.R(rect)
    leaf = w_
    hx = x if hinge == 'w' else x + w_
    hy = y + h_ if swing == 's' else y
    ex = hx + (leaf if hinge == 'w' else -leaf)
    ty = hy + (leaf if swing == 's' else -leaf)
    d.line(hx, hy, hx, ty, WALL, 1.4)
    flag = 1 if (hinge == 'w') == (swing == 'n') else 0
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 %d %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>' % (hx, ty, leaf, leaf, flag, ex, hy, WALL))


def porta_correr_horizontal(d, rect, lado='n', sentido='e'):
    """Porta de correr em parede horizontal.

    A folha é desenhada fechada, encostada numa das faces da parede (`lado`),
    e a seta mostra para onde ela corre; o tracejado marca o trecho de parede
    que precisa ficar livre para a folha estacionar.
    """
    vao(d, rect)
    x, y, w_, h_ = d.R(rect)
    esp = 4.4                                     # espessura da folha em planta
    ty = (y - 4.6) if lado == 'n' else (y + h_ + 4.6)
    dx = w_ if sentido == 'e' else -w_
    # trecho de parede que precisa ficar livre para a folha estacionar:
    # tracejado explícito, porque o renderizador SVG ignora stroke-dasharray
    px0 = min(x + dx, x + 2 * dx)
    for by in (ty - esp / 2, ty + esp / 2):
        t = px0
        while t < px0 + w_:
            d.line(t, by, min(t + 4.5, px0 + w_), by, WALL, 0.8, opacity=0.5)
            t += 8.0
    for bx in (px0, px0 + w_):
        d.line(bx, ty - esp / 2, bx, ty + esp / 2, WALL, 0.8, opacity=0.5)
    # folha fechada
    d.rect(x, ty - esp / 2, w_, esp, fill=BG, stroke=INK, sw=1.5)
    # seta do sentido de abertura
    ay = ty + (-9.5 if lado == 'n' else 9.5)
    a0 = x + w_ * (0.40 if sentido == 'e' else 0.60)
    a1 = x + w_ * (1.25 if sentido == 'e' else -0.25)
    d.line(a0, ay, a1, ay, WALL, 0.9, opacity=0.75)
    p = 1 if sentido == 'e' else -1
    d.add('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f Z" fill="%s" opacity="0.75"/>'
          % (a1, ay, a1 - 4.6 * p, ay - 2.4, a1 - 4.6 * p, ay + 2.4, WALL))


def porta(d, door):
    vao(d, door['rect'])
    x, y, w_, h_ = d.R(door['rect'])
    leaf = h_
    hx = x + w_ if door['leaf'] == 'e' else x
    hy = y if door['hinge'] == 'n' else y + h_
    ex = hx + (leaf if door['leaf'] == 'e' else -leaf)
    ty = hy + (leaf if door['hinge'] == 'n' else -leaf)
    d.line(hx, hy, ex, hy, WALL, 1.4)
    d.add('<path d="M %.2f %.2f A %.2f %.2f 0 0 %d %.2f %.2f" fill="none" stroke="%s" '
          'stroke-width="0.8" opacity="0.5"/>'
          % (ex, hy, leaf, leaf, 1 if door['hinge'] == 'n' else 0, hx, ty, WALL))

def janelas(d):
    for r in JANELAS:
        vao(d, r)
        x, y, w_, h_ = d.R(r)
        d.rect(x, y, w_, h_, fill='none', stroke=WALL, sw=0.9)
        if w_ > h_:
            d.line(x, y + h_ / 2, x + w_, y + h_ / 2, WALL, 0.9)
        else:
            d.line(x + w_ / 2, y, x + w_ / 2, y + h_, WALL, 0.9)

def escada(d, rotulo=True):
    x, y, w_, h_ = d.R(ESCADA['rect'])
    d.rect(x, y, w_, h_, fill='none', stroke=WALL, sw=0.9, opacity=0.85)
    n = ESCADA['degraus']
    for i in range(1, n):
        xx = x + w_ * i / float(n)
        d.line(xx, y, xx, y + h_, WALL, 0.7, opacity=0.6)
    if rotulo:
        d.txt(x + w_ / 2, y + h_ / 2 + 3, 'ESCADA', 6.6, INK_SOFT, 'bold', 'middle', ls=0.8)

def rotulos(d, areas=True, size=8.8):
    for k in ROOM_ORDER:
        r = ROOMS[k]
        lx, ly = d.P(r['lx'], r['ly'])
        d.txt(lx, ly, r['label'], size, INK, 'bold', 'middle', ls=0.9)
        if areas:
            d.txt(lx, ly + 10, br(r['area']) + ' m²', size - 1.1, INK_SOFT, 'normal', 'middle')

def tracejado(d, pts_pt, stroke=JOINT, w=1.7, dash=6.0, gap=4.2, halo=True):
    pp = [d.P(x, y) for x, y in pts_pt]
    if halo:
        d.path(path_d(pp, close=False), stroke=BG, sw=w + 1.7, opacity=0.9)
    resto, on = 0.0, True
    for i in range(len(pp) - 1):
        (ax, ay), (bx, by) = pp[i], pp[i + 1]
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-9: continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0.0
        while t < L:
            passo = (dash if on else gap) - resto
            t2 = min(t + passo, L)
            if on:
                d.line(ax + ux * t, ay + uy * t, ax + ux * t2, ay + uy * t2, stroke, w, cap='butt')
            if t2 - t >= passo - 1e-9:
                on = not on; resto = 0.0
            else:
                resto += t2 - t
            t = t2

def _tick(d, x, y, vertical=False):
    if vertical:
        d.line(x - 3.0, y + 3.0, x + 3.0, y - 3.0, DIM, 1.1)
    else:
        d.line(x - 3.0, y + 3.0, x + 3.0, y - 3.0, DIM, 1.1)


def cota_h(d, x0_pt, x1_pt, y_pt, off, texto=None, size=7.2, ext=True):
    """Cota horizontal: x0..x1 em pt do scan, linha deslocada `off` px de y_pt."""
    a = d.P(x0_pt, y_pt); b = d.P(x1_pt, y_pt)
    yy = a[1] + off
    if ext:
        for xx in (a[0], b[0]):
            d.line(xx, a[1] + (3.0 if off > 0 else -3.0), xx, yy + (3.0 if off > 0 else -3.0),
                   DIM, 0.5, opacity=0.75)
    d.line(a[0], yy, b[0], yy, DIM, 0.7)
    _tick(d, a[0], yy); _tick(d, b[0], yy)
    t = texto if texto is not None else br(abs(x1_pt - x0_pt) / PT_PER_M)
    d.txt((a[0] + b[0]) / 2.0, yy - 4.0, t, size, DIM_TXT, 'normal', 'middle')


def cota_v(d, y0_pt, y1_pt, x_pt, off, texto=None, size=7.2, ext=True):
    """Cota vertical: y0..y1 em pt do scan, linha deslocada `off` px de x_pt."""
    a = d.P(x_pt, y0_pt); b = d.P(x_pt, y1_pt)
    xx = a[0] + off
    if ext:
        for yy in (a[1], b[1]):
            d.line(a[0] + (3.0 if off > 0 else -3.0), yy, xx + (3.0 if off > 0 else -3.0), yy,
                   DIM, 0.5, opacity=0.75)
    d.line(xx, a[1], xx, b[1], DIM, 0.7)
    _tick(d, xx, a[1], True); _tick(d, xx, b[1], True)
    t = texto if texto is not None else br(abs(y1_pt - y0_pt) / PT_PER_M)
    d.txt(xx - 4.0, (a[1] + b[1]) / 2.0, t, size, DIM_TXT, 'normal', 'middle',
          rot=-90.0)


def cadeia_h(d, cortes_pt, y_pt, off, size=7.0):
    for i in range(len(cortes_pt) - 1):
        cota_h(d, cortes_pt[i], cortes_pt[i + 1], y_pt, off, size=size, ext=(i == 0))


def cadeia_v(d, cortes_pt, x_pt, off, size=7.0):
    for i in range(len(cortes_pt) - 1):
        cota_v(d, cortes_pt[i], cortes_pt[i + 1], x_pt, off, size=size, ext=(i == 0))


def norte(d, cx, cy, r=17.0, graus=None, nota='duas'):
    """Símbolo de norte. `graus`: 0 = norte para o topo da folha, horário."""
    g = NORTE_DEG if graus is None else graus
    a = math.radians(g - 90.0)
    ca, sa = math.cos(a), math.sin(a)
    nx, ny = cx + r * ca, cy + r * sa          # ponta norte
    sx, sy = cx - r * ca, cy - r * sa          # ponta sul
    px, py = -sa, ca                            # perpendicular
    w = r * 0.26
    b1 = (cx + px * w, cy + py * w)
    b2 = (cx - px * w, cy - py * w)
    d.circle(cx, cy, r, fill='none', stroke=INK_SOFT, sw=0.9, opacity=0.75)
    d.add('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f Z" fill="%s"/>'
          % (nx, ny, b1[0], b1[1], b2[0], b2[1], INK))
    d.add('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f Z" fill="%s" stroke="%s" stroke-width="0.9"/>'
          % (sx, sy, b1[0], b1[1], b2[0], b2[1], BRANCO, INK))
    d.txt(cx + (r + 12) * ca, cy + (r + 12) * sa + 3.4, 'N', 10.0, INK, 'bold', 'middle', ls=0.6)
    if nota and NORTE_CONFIRMADO:
        d.txt(cx, cy + r + 23, 'NORTE 126°', 7.0, INK, 'bold', 'middle', ls=0.4)
        if nota == 'duas':
            d.txt(cx, cy + r + 33, 'rosa dos ventos do scan', 6.8, INK_SOFT, 'normal', 'middle')
            d.txt(cx, cy + r + 43, 'do pavimento superior', 6.8, INK_SOFT, 'normal', 'middle')
    elif nota:
        d.txt(cx, cy + r + 23, 'ORIENTAÇÃO PROVISÓRIA', 6.6, RED, 'bold', 'middle', ls=0.3)


def piso_reguas(d, poly_pt, larg=0.22, junta=3.00, sentido='ns',
                cor=K, op=0.32, sw=0.5):
    """Piso pronto em réguas, clipado no polígono e ancorado na origem do plano.

    As réguas correm norte-sul por padrão, paralelas ao lado maior (9,43 m).
    Os topos são defasados de 1/3 de junta a cada régua.
    """
    pp = [d.P(a, b) for a, b in poly_pt]
    d.path(path_d(pp), fill=BRANCO)
    ox, oy = d.org
    S = d.S
    x0, y0, x1, y1 = bbox(pp)
    if sentido == 'ns':
        i = 0
        while True:
            xa = ox + i * larg * S
            xb = xa + larg * S
            if xa > x1 + 1:
                break
            if xb >= x0 - 1:
                for (a, b) in spans_at_x(pp, xb):
                    d.line(xb, a, xb, b, cor, sw, opacity=op)
                desloc = (i % 3) / 3.0 * junta
                j = 0
                while True:
                    yy = oy + (desloc + j * junta) * S
                    if yy > y1 + 1:
                        break
                    if yy >= y0 - 1:
                        for (s0, s1) in spans_at_y(pp, yy):
                            aa, bb = max(s0, xa, x0), min(s1, xb, x1)
                            if bb > aa:
                                d.line(aa, yy, bb, yy, cor, sw, opacity=op)
                    j += 1
            i += 1
    else:
        i = 0
        while True:
            ya = oy + i * larg * S
            yb = ya + larg * S
            if ya > y1 + 1:
                break
            if yb >= y0 - 1:
                for (a, b) in spans_at_y(pp, yb):
                    d.line(a, yb, b, yb, cor, sw, opacity=op)
                desloc = (i % 3) / 3.0 * junta
                j = 0
                while True:
                    xx = ox + (desloc + j * junta) * S
                    if xx > x1 + 1:
                        break
                    if xx >= x0 - 1:
                        for (s0, s1) in spans_at_x(pp, xx):
                            aa, bb = max(s0, ya, y0), min(s1, yb, y1)
                            if bb > aa:
                                d.line(xx, aa, xx, bb, cor, sw, opacity=op)
                    j += 1
            i += 1
    d.path(path_d(pp), fill='none', stroke=K, sw=0.9)


def escala(d, y):
    ox = d.org[0]
    S = d.S
    for i in range(2):
        d.rect(ox + i * S, y, S, 5, fill=(INK if i % 2 == 0 else BG), stroke=INK, sw=0.8)
    for i in range(3):
        d.txt(ox + i * S, y + 16, str(i), 7.2, INK_SOFT, 'normal', 'middle')
    d.txt(ox + 2 * S + 13, y + 16, 'm   (base do scan)', 7.2, INK_SOFT)

def planta_base(d, estado='novo', fundo=True, com_rotulos=True, areas=True):
    if fundo:
        fundo_ambientes(d, MONO, 0.55)
    paredes(d, estado)
    janelas(d)
    if estado == 'existente':
        vidro_box(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    if estado == 'novo':
        porta_horizontal(d, PORTA_NOVA, hinge='w', swing='s')
    escada(d)
    if com_rotulos:
        rotulos(d, areas=areas)

# ---------------------------------------------------------------------------
# 5. BLOCOS DA FOLHA
# ---------------------------------------------------------------------------
def cabecalho(d, titulo, subtitulo, rev, dir1='', dir2=''):
    d.txt(MARGIN, 42, 'MAXHAUS / MAIN FLOOR', 10.0, INK_SOFT, 'bold', ls=1.6)
    d.txt(MARGIN, 78, titulo, 27, INK, 'bold')
    d.txt(MARGIN, 99, subtitulo, 9.6, INK_SOFT)
    d.txt(W - MARGIN, 42, rev, 10.0, RED, 'bold', 'end', ls=0.8)
    if dir1: d.txt(W - MARGIN, 78, dir1, 10.5, INK, 'bold', 'end')
    if dir2: d.txt(W - MARGIN, 99, dir2, 9.6, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 116, W - MARGIN, 116, RULE, 1.0)

def rodape(d, nota1, nota2, prancha, rev):
    d.line(MARGIN, 922, W - MARGIN, 922, RULE, 1.0)
    if nota1: d.txt(MARGIN, 940, nota1, 8.3, INK_SOFT)
    if nota2: d.txt(MARGIN, 953, nota2, 8.3, INK_SOFT)
    d.txt(MARGIN, 975, 'ESTUDO PRELIMINAR — NÃO LIBERADO PARA EXECUÇÃO   |   12/09/2026',
          9.0, RED, 'bold', ls=0.5)
    d.txt(W - MARGIN, 975, '%s   ·   %s' % (prancha, rev), 9.0, INK_SOFT, 'normal', 'end')

def legenda(d, itens, x, y, largura=None, col=1):
    """itens: (tipo, cor, texto). tipo: 'fill' | 'line' | 'dash' | 'dot' | 'ghost'."""
    cx, cy = x, y
    for (tipo, cor, texto) in itens:
        passo = 30 + len(texto) * 4.9
        if col == 1 and largura and cx > x and (cx + passo - 30) > (x + largura):
            cx, cy = x, cy + 17      # quebra de linha da legenda
        if tipo == 'fill':
            d.rect(cx, cy - 8, 15, 10, fill=cor, stroke=MONO_LINE, sw=0.7)
        elif tipo == 'ghost':
            d.rect(cx, cy - 8, 15, 10, fill='none', stroke=cor, sw=0.9, dash='3 2.5')
        elif tipo == 'line':
            d.line(cx, cy - 3, cx + 15, cy - 3, cor, 2.2)
        elif tipo == 'dash':
            for i in range(3):
                d.line(cx + i * 6, cy - 3, cx + i * 6 + 4, cy - 3, cor, 1.8, cap='butt')
        elif tipo == 'dot':
            d.circle(cx + 7, cy - 3, 4.2, fill='none', stroke=cor, sw=1.4)
        elif tipo == 'dotf':
            d.circle(cx + 7, cy - 3, 4.2, fill=cor, stroke=cor, sw=1.0)
        d.txt(cx + 22, cy, texto, 8.8, INK)
        if col == 1:
            cx += passo
        else:
            cy += 16
    return (cx, cy)

def tabela(d, x, y, largura, colunas, linhas, titulo=None, zebra=True):
    """colunas: [(rotulo, largura_relativa, alinhamento)]"""
    if titulo:
        d.txt(x, y - 9, titulo, 8.0, INK_SOFT, 'bold', ls=1.2)
    larguras = [c[1] for c in colunas]
    total = float(sum(larguras))
    xs, acc = [], 0.0
    for lw in larguras:
        xs.append(x + acc / total * largura)
        acc += lw
    d.rect(x, y, largura, 20, fill=K12)
    for i, (rot, lw, al) in enumerate(colunas):
        tx = xs[i] + 8 if al == 'start' else (xs[i] + (xs[i + 1] - xs[i] if i + 1 < len(xs) else largura - (xs[i] - x)) - 8)
        d.txt(tx, y + 13.5, rot, 8.2, INK_SOFT, 'bold', al, ls=0.6)
    ry = y + 20
    for n, linha in enumerate(linhas):
        alt = 22 if not isinstance(linha, tuple) or len(linha) < 4 else linha[3]
        if zebra and n % 2 == 1:
            d.rect(x, ry, largura, 22, fill=K04)
        for i, (rot, lw, al) in enumerate(colunas):
            val = linha[i] if i < len(linha) else ''
            tx = xs[i] + 8 if al == 'start' else (xs[i] + (xs[i + 1] - xs[i] if i + 1 < len(xs) else largura - (xs[i] - x)) - 8)
            peso = 'bold' if i == 0 else 'normal'
            cor = INK if i == 0 else INK_SOFT
            d.txt(tx, ry + 14.5, val, 8.6, cor, peso, al)
        d.line(x, ry + 22, x + largura, ry + 22, RULE, 0.6, opacity=0.8)
        ry += 22
    return ry

def paragrafos(d, x, y, largura, blocos, size=8.6, lh=13.0, gap=9.0):
    """blocos: lista de listas de linhas já quebradas."""
    yy = y
    for bloco in blocos:
        for ln in bloco:
            if ln.startswith('**'):
                d.txt(x, yy, ln[2:], size, INK, 'bold')
            else:
                d.txt(x, yy, ln, size, INK_SOFT)
            yy += lh
        yy += gap
    return yy

# ---------------------------------------------------------------------------
# 6. SAÍDA
# ---------------------------------------------------------------------------
def svg(d):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            % (W, H, W, H)) + '\n'.join(d.o) + '\n</svg>'

def folha_nova():
    d = Draw()
    d.rect(0, 0, W, H, fill=BG)
    return d

def salvar(d, pasta, nome_base):
    if not os.path.isdir(pasta):
        os.makedirs(pasta)
    caminho_svg = os.path.join(pasta, nome_base + '.svg')
    with open(caminho_svg, 'w') as f:
        f.write(svg(d))
    return caminho_svg

def exportar_pdf_a3(svgs, pdf_path, titulo):
    """Fecha uma ou mais folhas em A3 deitado (420 x 297 mm)."""
    import pymupdf
    folha = pymupdf.paper_rect('a3-l')
    saida = pymupdf.open()
    for caminho in svgs:
        src = pymupdf.open(caminho)
        doc = pymupdf.open('pdf', src.convert_to_pdf())
        pagina = saida.new_page(width=folha.width, height=folha.height)
        pagina.show_pdf_page(pagina.rect, doc, 0)
    saida.set_metadata({'title': titulo,
                        'subject': 'Estudo preliminar — A3, 420 x 297 mm',
                        'keywords': 'MaxHaus, MainFloor, estudo preliminar'})
    saida.save(pdf_path)
    return pdf_path

def exportar_png(svg_path, png_path, dpi=170):
    import pymupdf
    pymupdf.open(svg_path)[0].get_pixmap(dpi=dpi).save(png_path)
    return png_path
