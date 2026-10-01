# -*- coding: utf-8 -*-
"""Quarto adaptável na sala de estar e fechamento da claraboia (REV. N).

Duas decisões do cliente em 30.09.2026, as duas no teto:

  · uma cortina fecha a sala de estar como um quarto de hóspede. Recolhida, ela fica
    no canto noroeste da sala de estar, junto à parede oeste; estendida, desce pela
    lateral da escada, vira exatamente no fim da ponta da escada e corre até a
    fachada leste, a das esquadrias;
  · a claraboia — o fundo de vidro da piscina do pavimento superior, sobre a
    sala de TV — recebe um fechamento elétrico em 2027/28. A infraestrutura entra
    agora, enquanto o teto está aberto.

O vidro não é furável. Tudo o que toca o teto nesta zona — trilho, moldura do
fechamento, alimentação — fixa no concreto em volta dele.

Medidas em metros, a partir do canto noroeste do pavimento, na mesma base do
scan das demais pranchas.
"""
import math

from base_mainfloor import (AREA_PISCINA, ESCADA, PISCINA_CX, PISCINA_CY,
                            PISCINA_W, PISCINA_H, mx, my, path_d, BG, INK, K, K20,
                            K45, K70, CIANO, CIANO18, AMARELO, AMARELO40, DEMO,
                            MAGENTA18, BRANCO, br)

# --- referências do scan -----------------------------------------------------
FACE_NORTE = my(128.94)            # 0,10 — face interna da parede norte do jantar
FACE_LESTE = mx(599.46)            # 7,75 — face interna da fachada das esquadrias
FACE_OESTE_JANTAR = mx(450.68)     # 4,49 — parede entre jantar e escada
FIM_PAREDE_OESTE = my(213.47)      # 1,95 — onde essa parede termina
ESCADA_LESTE = mx(ESCADA['rect'][2])   # 4,68 — lateral da escada voltada ao jantar
ESCADA_PONTA = my(ESCADA['rect'][3])   # 2,79 — fim da ponta da escada

# --- claraboia = fundo de vidro da piscina ------------------------------------
VIDRO = (PISCINA_CX - PISCINA_W / 2, PISCINA_CY - PISCINA_H / 2,
         PISCINA_CX + PISCINA_W / 2, PISCINA_CY + PISCINA_H / 2)   # 5,17 1,64 7,09 4,64
MARGEM_MOLDURA = 0.12              # moldura do fechamento, no concreto em volta
MOLDURA = (VIDRO[0] - MARGEM_MOLDURA, VIDRO[1] - MARGEM_MOLDURA,
           VIDRO[2] + MARGEM_MOLDURA, VIDRO[3] + MARGEM_MOLDURA)

# --- trilho da cortina (eixo), CT01 -------------------------------------------
# Reto, sem desvio: desce rente à parede oeste da sala de estar e segue na mesma
# linha por cima do degrau da ponta da escada (REV. O, pedido do cliente) até
# virar no fim da ponta da escada.
AFASTAMENTO = 0.06                 # eixo do trilho à face da parede ou da escada
X_TRILHO = FACE_OESTE_JANTAR + AFASTAMENTO                # 4,55
Y_CORTINA = round(ESCADA_PONTA + AFASTAMENTO, 2)          # 2,85
R_CURVA = 0.25


def trilho_cortina():
    """Eixo do trilho, do canto noroeste da sala de estar até a fachada leste."""
    y0 = FACE_NORTE + AFASTAMENTO
    yc = Y_CORTINA - R_CURVA
    pts = [(X_TRILHO, y0), (X_TRILHO, yc)]
    cx = X_TRILHO + R_CURVA
    for i in range(1, 10):
        a = math.radians(90.0 * i / 9.0)
        pts.append((cx - R_CURVA * math.cos(a), yc + R_CURVA * math.sin(a)))
    pts.append((FACE_LESTE - AFASTAMENTO, Y_CORTINA))
    return pts


def comprimento(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def area_quarto():
    """Área dentro da cortina estendida, até as paredes norte e leste."""
    pts = trilho_cortina()
    poly = [(X_TRILHO, FACE_NORTE), (FACE_LESTE, FACE_NORTE),
            (FACE_LESTE, Y_CORTINA)] + list(reversed(pts))
    s = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


TRILHO = trilho_cortina()
TRILHO_M = comprimento(TRILHO)                 # ≈ 5,7 m
AREA_QUARTO = area_quarto()                    # ≈ 8,8 m²
PACOTE_M = round(TRILHO_M * 0.10 + 0.05, 2)    # cortina recolhida ocupa ~10 % do trilho

# fixação do trilho no concreto: nunca dentro da moldura da claraboia
FIX_OESTE = MOLDURA[0] - 0.05                  # último apoio antes do vidro
FIX_LESTE = MOLDURA[2] + 0.02                  # primeiro apoio depois
VAO_LIVRE = FIX_LESTE - FIX_OESTE              # trecho sem apoio no teto ≈ 2,3 m

# --- cama e circulação ---------------------------------------------------------
# REV. O: a cama gira e fica no sentido leste–oeste, com a lateral longa
# encostada na parede norte (a divisa, parede cega) e a cabeceira a leste, do
# lado da fachada. Centrada no quadrado marcado pelo cliente (x 5,07 a 7,31).
FOLGA_TECIDO = 0.05                            # a cortina ocupa uns 5 cm de cada lado do eixo
CAMA_CX = 6.19                                 # centro da cama no sentido leste–oeste
CAMAS = [
    # (nome, largura, comprimento)
    ('Casal padrão', 1.38, 1.88),
    ('Viúva', 1.28, 1.88),
    ('Queen — referência', 1.58, 1.98),
]
CIRCULACAO_MIN = 0.60


def cama_rect(larg, comp):
    """(x0, y0, x1, y1) da cama: comprimento no eixo x, largura a partir da parede norte."""
    return (CAMA_CX - comp / 2.0, FACE_NORTE, CAMA_CX + comp / 2.0, FACE_NORTE + larg)


def folgas(larg, comp):
    """Folgas do pé (oeste, até a cortina), da cabeceira (leste) e da lateral sul."""
    x0, y0, x1, y1 = cama_rect(larg, comp)
    pe = x0 - X_TRILHO - FOLGA_TECIDO
    cabeceira = FACE_LESTE - x1
    sul = Y_CORTINA - FOLGA_TECIDO - y1
    return pe, cabeceira, sul


CASAL = CAMAS[0]
_CASAL = cama_rect(CASAL[1], CASAL[2])
# área de troca: a faixa sul inteira, entre a lateral da cama e a cortina
TROCA = (X_TRILHO + FOLGA_TECIDO, _CASAL[3], FACE_LESTE, Y_CORTINA - FOLGA_TECIDO)

# --- pontos novos (entram nas listas das Pranchas 05 e 06) ----------------------
AC01_NOVO = (4.76, 3.05)          # sai da linha da cortina, fica fora da moldura
PONTO_CLARABOIA = ('T18', 7.30, 4.86, 'espera do motor da claraboia — 2027/28')
TOMADA_CABECEIRA = ('T19', 7.62, 1.62, 'cabeceira sul — quarto adaptável')
T16_NOVO = ('T16', 7.45, 0.30, 'cabeceira norte / sala de estar')
COMANDO_QUARTO = ('S09', 7.62, 1.88)      # paralelo do S02, no pilar entre J01 e J02
COMANDO_CLARABOIA = ('S10', 7.62, 4.15)   # pilar entre J02 e J03, ao lado do T02


# ---------------------------------------------------------------------------
# DESENHO
# ---------------------------------------------------------------------------
def desenhar_vidro(d, rotulo=True, size=7.4):
    x0, y0 = d.PM(VIDRO[0], VIDRO[1]); x1, y1 = d.PM(VIDRO[2], VIDRO[3])
    d.rect(x0, y0, x1 - x0, y1 - y0, fill=AMARELO, opacity=0.30)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill='none', stroke=K, sw=1.2, dash='6 4')
    if rotulo:
        cx = (x0 + x1) / 2.0
        d.txt(cx, (y0 + y1) / 2.0 - 6, 'CLARABOIA', size, K, 'bold', 'middle', ls=0.5)
        d.txt(cx, (y0 + y1) / 2.0 + 6, 'fundo de vidro da piscina', size - 0.6, K70, 'normal', 'middle')
        d.txt(cx, (y0 + y1) / 2.0 + 17, 'não furável', size - 0.6, DEMO, 'bold', 'middle')


def desenhar_moldura(d, rotulo=True, size=7.0):
    """Moldura do fechamento elétrico — 2027/28, fixada fora do vidro."""
    x0, y0 = d.PM(MOLDURA[0], MOLDURA[1]); x1, y1 = d.PM(MOLDURA[2], MOLDURA[3])
    d.rect(x0, y0, x1 - x0, y1 - y0, fill='none', stroke=CIANO, sw=3.2, opacity=0.9)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill='none', stroke=K, sw=0.8, dash='2 2')
    if rotulo:
        d.txt(x1 - 4, y1 - 6, 'FC01 · fechamento elétrico 2027/28', size, K, 'bold', 'end', ls=0.3)


def desenhar_trilho(d, sw=2.6, rotulo=True, size=7.2, apoios=True):
    pp = [d.PM(x, y) for x, y in TRILHO]
    d.path(path_d(pp, close=False), stroke=BG, sw=sw + 3.0)
    d.path(path_d(pp, close=False), stroke=DEMO, sw=sw)
    # pacote da cortina recolhida, no canto do jantar
    a = d.PM(X_TRILHO, FACE_NORTE + 0.06)
    b = d.PM(X_TRILHO, FACE_NORTE + 0.06 + PACOTE_M)
    d.rect(a[0] - 3.2, a[1], 6.4, b[1] - a[1], fill=MAGENTA18, stroke=DEMO, sw=0.9)
    if apoios:
        # apoios no concreto; nenhum entre FIX_OESTE e FIX_LESTE
        for (x, y) in [(X_TRILHO, 0.60), (X_TRILHO, 1.30),
                       (X_TRILHO, 2.20), (FIX_OESTE, Y_CORTINA),
                       (FIX_LESTE, Y_CORTINA), (FACE_LESTE - 0.12, Y_CORTINA)]:
            cx, cy = d.PM(x, y)
            d.rect(cx - 2.6, cy - 2.6, 5.2, 5.2, fill=K, stroke=None)
    if rotulo:
        e = d.PM(FACE_LESTE - 0.30, Y_CORTINA)
        d.txt(e[0], e[1] + 13, 'CT01 · cortina', size, DEMO, 'bold', 'end', ls=0.3)


def desenhar_cama(d, larg, comp, tracejada=False, rotulo=None, size=7.0):
    cx0, cy0, cx1, cy1 = cama_rect(larg, comp)
    x0, y0 = d.PM(cx0, cy0); x1, y1 = d.PM(cx1, cy1)
    if tracejada:
        d.rect(x0, y0, x1 - x0, y1 - y0, fill='none', stroke=K45, sw=0.9, dash='4 3')
    else:
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=BRANCO, stroke=K, sw=1.3)
        # travesseiros na cabeceira, a leste
        w = x1 - x0; th = (y1 - y0 - 12) / 2.0
        for i in range(2):
            d.rect(x1 - 4 - w * 0.12, y0 + 4 + i * (th + 4), w * 0.12, th, fill=K20,
                   stroke=K45, sw=0.6)
        d.line(x1 - w * 0.30, y0, x1 - w * 0.30, y1, K45, 0.6)
    if rotulo:
        d.txt(x0 + (x1 - x0) * 0.38, y0 + (y1 - y0) * 0.30, rotulo, size, K, 'bold', 'middle')


def poly_quarto():
    """Polígono (m) do quarto com a cortina estendida."""
    return ([(X_TRILHO, FACE_NORTE), (FACE_LESTE, FACE_NORTE),
             (FACE_LESTE, Y_CORTINA)] + list(reversed(TRILHO)))
