# -*- coding: utf-8 -*-
"""Quarto adaptável no jantar e fechamento da claraboia (REV. N).

Duas decisões do cliente em 30.09.2026, as duas no teto:

  · uma cortina fecha o jantar como um quarto de hóspede. Recolhida, ela fica
    no canto noroeste do jantar, junto à parede oeste; estendida, desce pela
    lateral da escada, vira exatamente no fim da ponta da escada e corre até a
    fachada leste, a das esquadrias;
  · a claraboia — o fundo de vidro da piscina do pavimento superior, sobre a
    sala — recebe um fechamento elétrico em 2027/28. A infraestrutura entra
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
AFASTAMENTO = 0.06                 # eixo do trilho à face da parede ou da escada
X_JUNTO_PAREDE = FACE_OESTE_JANTAR + AFASTAMENTO          # 4,55
X_JUNTO_ESCADA = round(ESCADA_LESTE + 0.07, 2)            # 4,75
Y_CORTINA = round(ESCADA_PONTA + AFASTAMENTO, 2)          # 2,85
R_CURVA = 0.25


def _bezier(p0, c0, c1, p1, n=14):
    out = []
    for i in range(n + 1):
        t = i / float(n)
        a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t ** 2; e = t ** 3
        out.append((a * p0[0] + b * c0[0] + c * c1[0] + e * p1[0],
                    a * p0[1] + b * c0[1] + c * c1[1] + e * p1[1]))
    return out


def trilho_cortina():
    """Eixo do trilho, do canto noroeste do jantar até a fachada leste."""
    y0 = FACE_NORTE + AFASTAMENTO
    y_s0, y_s1 = 1.40, 1.85        # desvio que contorna a ponta da escada
    pts = [(X_JUNTO_PAREDE, y0), (X_JUNTO_PAREDE, y_s0)]
    pts += _bezier((X_JUNTO_PAREDE, y_s0), (X_JUNTO_PAREDE, (y_s0 + y_s1) / 2),
                   (X_JUNTO_ESCADA, (y_s0 + y_s1) / 2), (X_JUNTO_ESCADA, y_s1))[1:]
    yc = Y_CORTINA - R_CURVA
    pts.append((X_JUNTO_ESCADA, yc))
    cx = X_JUNTO_ESCADA + R_CURVA
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
    poly = [(X_JUNTO_PAREDE, FACE_NORTE), (FACE_LESTE, FACE_NORTE),
            (FACE_LESTE, Y_CORTINA)] + list(reversed(pts))
    s = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


TRILHO = trilho_cortina()
TRILHO_M = comprimento(TRILHO)                 # ≈ 5,6 m
AREA_QUARTO = area_quarto()                    # ≈ 8,5 m²
PACOTE_M = round(TRILHO_M * 0.10 + 0.05, 2)    # cortina recolhida ocupa ~10 % do trilho

# fixação do trilho no concreto: nunca dentro da moldura da claraboia
FIX_OESTE = MOLDURA[0] - 0.05                  # último apoio antes do vidro
FIX_LESTE = MOLDURA[2] + 0.02                  # primeiro apoio depois
VAO_LIVRE = FIX_LESTE - FIX_OESTE              # trecho sem apoio no teto ≈ 2,3 m

# --- cama e circulação ---------------------------------------------------------
FOLGA_TECIDO = 0.05                            # a cortina ocupa uns 5 cm de cada lado do eixo
CAMA_X = 5.45                                  # cabeceira na parede norte (divisa, parede cega)
CAMAS = [
    # (nome, largura, comprimento)
    ('Casal padrão', 1.38, 1.88),
    ('Viúva', 1.28, 1.88),
    ('Queen — referência', 1.58, 1.98),
]
CIRCULACAO_MIN = 0.60


def folgas(larg, comp):
    oeste = CAMA_X - X_JUNTO_ESCADA - FOLGA_TECIDO
    leste = FACE_LESTE - (CAMA_X + larg)
    pe = Y_CORTINA - FOLGA_TECIDO - (FACE_NORTE + comp)
    return oeste, leste, pe


CASAL = CAMAS[0]
# área de troca: faixa leste da cama até a cortina, junto à janela J01
TROCA = (CAMA_X + CASAL[1], FACE_NORTE, FACE_LESTE, Y_CORTINA - FOLGA_TECIDO)

# --- pontos novos (entram nas listas das Pranchas 05 e 06) ----------------------
AC01_NOVO = (4.76, 3.05)          # sai da linha da cortina, fica fora da moldura
PONTO_CLARABOIA = ('T18', 7.30, 4.86, 'espera do motor da claraboia — 2027/28')
TOMADA_CABECEIRA = ('T19', 5.25, 0.30, 'cabeceira — quarto adaptável')
T16_NOVO = ('T16', 7.05, 0.30, 'cabeceira / jantar')
COMANDO_QUARTO = ('S09', 7.62, 1.75)      # paralelo do S02, no pilar entre J01 e J02
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
    a = d.PM(X_JUNTO_PAREDE, FACE_NORTE + 0.06)
    b = d.PM(X_JUNTO_PAREDE, FACE_NORTE + 0.06 + PACOTE_M)
    d.rect(a[0] - 3.2, a[1], 6.4, b[1] - a[1], fill=MAGENTA18, stroke=DEMO, sw=0.9)
    if apoios:
        # apoios no concreto; nenhum entre FIX_OESTE e FIX_LESTE
        for (x, y) in [(X_JUNTO_PAREDE, 0.60), (X_JUNTO_PAREDE, 1.30),
                       (X_JUNTO_ESCADA, 2.20), (FIX_OESTE, Y_CORTINA),
                       (FIX_LESTE, Y_CORTINA), (FACE_LESTE - 0.12, Y_CORTINA)]:
            cx, cy = d.PM(x, y)
            d.rect(cx - 2.6, cy - 2.6, 5.2, 5.2, fill=K, stroke=None)
    if rotulo:
        e = d.PM(FACE_LESTE - 0.30, Y_CORTINA)
        d.txt(e[0], e[1] + 13, 'CT01 · cortina', size, DEMO, 'bold', 'end', ls=0.3)


def desenhar_cama(d, larg, comp, tracejada=False, rotulo=None, size=7.0):
    x0, y0 = d.PM(CAMA_X, FACE_NORTE); x1, y1 = d.PM(CAMA_X + larg, FACE_NORTE + comp)
    if tracejada:
        d.rect(x0, y0, x1 - x0, y1 - y0, fill='none', stroke=K45, sw=0.9, dash='4 3')
    else:
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=BRANCO, stroke=K, sw=1.3)
        # travesseiros
        tw = (x1 - x0 - 12) / 2.0
        for i in range(2):
            d.rect(x0 + 4 + i * (tw + 4), y0 + 4, tw, (y1 - y0) * 0.12, fill=K20,
                   stroke=K45, sw=0.6)
        d.line(x0, y0 + (y1 - y0) * 0.30, x1, y0 + (y1 - y0) * 0.30, K45, 0.6)
    if rotulo:
        d.txt((x0 + x1) / 2.0, y0 + (y1 - y0) * 0.62, rotulo, size, K, 'bold', 'middle')


def poly_quarto():
    """Polígono (m) do quarto com a cortina estendida."""
    return ([(X_JUNTO_PAREDE, FACE_NORTE), (FACE_LESTE, FACE_NORTE),
             (FACE_LESTE, Y_CORTINA)] + list(reversed(TRILHO)))
