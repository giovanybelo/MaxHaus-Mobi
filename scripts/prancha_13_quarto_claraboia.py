# -*- coding: utf-8 -*-
"""Prancha 13 — Quarto adaptável na sala de estar e fechamento da claraboia (REV. O).

Detalha as duas decisões de 30.09.2026 que mexem no teto: a cortina que fecha
a sala de estar como quarto de hóspede e o fechamento elétrico da claraboia, previsto
para 2027/28 mas com infraestrutura feita agora.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa
import quarto_adaptavel as qa

REV = 'REV. O'
PRANCHA = 'Prancha 13 / 14'

S = 140.0
X0_M, Y0_M = 4.0, -0.05           # canto do recorte, em metros
OX, OY = 70.0, 150.0


def _folgas_txt(larg, comp):
    o, l, p = qa.folgas(larg, comp)
    ok = min(o, l, p) >= qa.CIRCULACAO_MIN - 1e-6
    return [br(o), br(l), br(p), 'sim' if ok else 'no limite']


TAB_NUM = [
    ('Área dentro da cortina', '%s m²' % br(qa.AREA_QUARTO), 'sala de estar 5,90 m² + faixa da sala de TV até a ponta da escada'),
    ('Largura × profundidade', '%s × %s m' % (br(qa.FACE_LESTE - qa.X_TRILHO), br(qa.Y_CORTINA - qa.FACE_NORTE)),
     'da cortina à fachada · da parede norte à cortina'),
    ('Linha da cortina', '2,85 m', 'da parede norte — 0,06 m além da ponta da escada'),
    ('Cortina recolhida', '~%s m de trilho' % br(qa.PACOTE_M), 'pacote no canto noroeste, junto à parede'),
]


def _m(a, b):
    return '%s m' % br(b - a)


# trilho CT01 — medidas no eixo, em metros a partir do canto noroeste
TAB_TRILHO = [
    ('Descida rente à parede oeste (x %s)' % br(qa.X_TRILHO), 'y %s a %s' % (br(qa.Y0_TRILHO), br(qa.Y_CURVA)),
     '%s m' % br(qa.DESCIDA_M)),
    ('Curva no fim da ponta da escada, R %s' % br(qa.R_CURVA), 'y %s a x %s' % (br(qa.Y_CURVA), br(qa.X_CURVA)),
     '%s m' % br(qa.CURVA_M)),
    ('Reta até o último apoio antes da claraboia', 'x %s a %s' % (br(qa.X_CURVA), br(qa.FIX_OESTE)),
     _m(qa.X_CURVA, qa.FIX_OESTE)),
    ('Vão sob a claraboia, sem apoio — perfil PF1', 'x %s a %s' % (br(qa.FIX_OESTE), br(qa.FIX_LESTE)),
     '%s m' % br(qa.VAO_LIVRE)),
    ('   · dentro do vão: faixa da moldura FC01', 'x %s a %s' % (br(qa.MOLDURA[0]), br(qa.MOLDURA[2])),
     _m(qa.MOLDURA[0], qa.MOLDURA[2])),
    ('   · dentro do vão: sobre o vidro', 'x %s a %s' % (br(qa.VIDRO[0]), br(qa.VIDRO[2])),
     _m(qa.VIDRO[0], qa.VIDRO[2])),
    ('Do apoio leste até a fachada (J02)', 'x %s a %s' % (br(qa.FIX_LESTE), br(qa.X_FIM)),
     _m(qa.FIX_LESTE, qa.X_FIM)),
    ('Total do eixo CT01', 'do canto noroeste à fachada', '%s m' % br(qa.TRILHO_M)),
    ('Linha sob o vidro, a y %s' % br(qa.Y_CORTINA), 'borda norte %s · sul %s' % (br(qa.VIDRO[1]), br(qa.VIDRO[3])),
     '%s / %s m' % (br(qa.Y_CORTINA - qa.VIDRO[1]), br(qa.VIDRO[3] - qa.Y_CORTINA))),
    ('Apoios AP, só no concreto', 'y 0,60 · 1,30 · 2,20 · x %s · %s · %s' % tuple(br(a[0]) for a in qa.APOIOS[3:]),
     '6 pontos'),
]

TAB_CAMA = [(n, '%s × %s' % (br(l), br(c))) + tuple(_folgas_txt(l, c))
            for (n, l, c) in qa.CAMAS]

TAB_FASE = [
    ('CT01', 'Trilho da cortina + perfil autoportante no trecho da claraboia', 'agora'),
    ('CT02', 'Cortina de tecido, pé-direito inteiro — blackout a definir', 'agora'),
    ('IN4', 'Eletroduto aparente e caixa de espera T18 junto à moldura', 'agora'),
    ('IN5', 'Comando S10 com cabo guia até a espera', 'agora'),
    ('MR1', 'Faixa de 0,12 m em volta do vidro reservada à moldura', 'agora'),
    ('FC01', 'Fechamento elétrico da claraboia: moldura, motor e painel', '2027/28'),
    ('FC02', 'Ligação na espera T18 e programação do comando S10', '2027/28'),
]

NOTAS = [
    ['**Trilho reto, com uma curva só, no fim da ponta da escada.',
     'Desce rente à parede, passa sobre o degrau, vira e corre a 2,85 m da parede norte até a J02.',
     'Se a J02 tiver montante central, o trilho termina nele. Cama e folgas: ver a tabela acima.'],
    ['**Sob a claraboia: %s m sem fixação, do apoio x %s ao x %s.' % (br(qa.VAO_LIVRE), br(qa.FIX_OESTE), br(qa.FIX_LESTE)),
     'Trilho comum pede apoio a cada ~1,0 m: perfil autoportante PF1 (tubo metálico) no concreto',
     'antes e depois da moldura, com o trilho preso nele — ou cabo de aço tensionado. Medidas',
     'sobre o scan: conferir vidro e moldura em obra antes de cortar o perfil.'],
    ['**Fechamento elétrico: o equipamento é de 2027/28, a espera é de agora.',
     'Eletroduto, caixa T18 e comando S10 com cabo guia entram com o teto aberto. A moldura fixa',
     'na faixa de 0,12 m em volta do vidro — confirmar se há viga de borda da piscina ali.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Quarto adaptável e fechamento da claraboia',
              'A cortina fecha a sala de estar como quarto de hóspede; a claraboia ganha fechamento elétrico em 2027/28, com a infraestrutura feita agora.',
              REV, 'cama de casal com 0,60 m de circulação nos três lados',
              '%s m² dentro da cortina  ·  claraboia não furável' % br(qa.AREA_QUARTO))

    d.set_plan(OX - X0_M * S, OY - Y0_M * S, S)
    fundo_ambientes(d, K07)
    # quarto adaptável
    pq = [d.PM(x, y) for x, y in qa.poly_quarto()]
    d.path(path_d(pq), fill=CIANO18)
    # área de troca
    t = qa.TROCA
    a = d.PM(t[0], t[1] + 0.05); b = d.PM(t[2], t[3])
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=AMARELO40, opacity=0.7)
    paredes(d, estado='novo')
    janelas(d)
    escada(d)
    qa.desenhar_vidro(d, size=8.4)
    qa.desenhar_moldura(d, rotulo=True, size=8.0)
    qa.desenhar_cama(d, qa.CASAL[1], qa.CASAL[2], rotulo='cama de casal')
    cr = qa.cama_rect(qa.CASAL[1], qa.CASAL[2])
    x0, y0 = d.PM(cr[0], cr[1])
    d.txt(x0 + (cr[2] - cr[0]) * S * 0.38, y0 + (cr[3] - cr[1]) * S * 0.30 + 12, '1,38 × 1,88 m', 7.6, K70, 'normal', 'middle')
    qa.desenhar_trilho(d, sw=3.2, rotulo=False)

    # textos de ambiente e da troca
    c = d.PM(6.75, 1.95)
    d.txt(c[0], c[1], 'TROCA', 7.6, K, 'bold', 'middle', ls=0.4)
    d.txt(c[0], c[1] + 10, '%s × %s' % (br(t[2] - t[0]), br(t[3] - t[1])), 7.0, K70, 'normal', 'middle')
    c = d.PM(4.62, 3.55)
    d.txt(c[0], c[1], 'SALA DE TV', 9.0, INK, 'bold', 'start', ls=0.9)
    c = d.PM(5.30, 2.42)
    d.txt(c[0], c[1], 'QUARTO ADAPTÁVEL', 8.6, INK, 'bold', 'start', ls=0.6)
    d.txt(c[0], c[1] + 11, '%s m² com a cortina fechada' % br(qa.AREA_QUARTO), 7.4, K70, 'normal', 'start')
    c = d.PM(qa.FACE_OESTE_JANTAR - 0.12, 0.45)
    d.txt(c[0], c[1], 'CT01', 8.0, DEMO, 'bold', 'end', ls=0.4)
    d.txt(c[0], c[1] + 11, 'recolhida', 7.2, DEMO, 'normal', 'end')

    # luz do jantar sobre a cama
    a = d.PM(4.75, 0.95); b = d.PM(7.50, 0.95)
    d.line(a[0], a[1], b[0], b[1], INK, 2.0, opacity=0.55)
    cx, cy = d.PM(6.12, 0.98)
    d.circle(cx, cy, 9.0, fill=AMARELO, stroke=K, sw=1.4)
    d.txt(cx + 13, cy - 8, 'P01 · plafon', 7.4, NEW, 'bold', 'start')
    d.txt(a[0] + 3, a[1] - 5, 'TR1', 7.0, INK, 'bold', 'start')

    # pontos elétricos novos e afetados
    def tomada(ident, xm, ym, nova=True, lado='s'):
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 5.6, fill=CIANO if nova else BG, stroke=K if nova else K45, sw=1.3)
        d.circle(cx, cy, 1.8, fill=K if nova else K45)
        if lado == 's':
            d.txt(cx, cy + 15, ident, 7.0, K, 'bold', 'middle')
        else:
            d.txt(cx - 9, cy + 2.5, ident, 7.0, K, 'bold', 'end')

    def comando(ident, xm, ym):
        cx, cy = d.PM(xm, ym)
        d.rect(cx - 5.4, cy - 5.4, 10.8, 10.8, fill=BG, stroke=K, sw=1.3)
        d.line(cx - 2.5, cy + 2.5, cx + 2.5, cy - 2.5, K, 1.2)
        d.txt(cx - 9, cy + 2.5, ident, 7.0, K, 'bold', 'end')

    tomada(qa.TOMADA_CABECEIRA[0], qa.TOMADA_CABECEIRA[1], qa.TOMADA_CABECEIRA[2], lado='o')
    tomada(qa.T16_NOVO[0], qa.T16_NOVO[1], qa.T16_NOVO[2])
    tomada('T01', 7.62, 2.46, nova=False, lado='o')
    tomada('T02', 7.62, 4.51, nova=False, lado='o')
    comando(*qa.COMANDO_QUARTO)
    comando(*qa.COMANDO_CLARABOIA)
    cx, cy = d.PM(qa.PONTO_CLARABOIA[1], qa.PONTO_CLARABOIA[2])
    d.rect(cx - 5, cy - 5, 10, 10, fill=AMARELO, stroke=K, sw=1.3)
    d.txt(cx - 9, cy + 16, 'T18 · espera do motor', 7.0, K, 'bold', 'end')
    cx, cy = d.PM(*qa.AC01_NOVO)
    d.rect(cx - 18, cy - 6, 36, 12, fill=CIANO35, stroke=K, sw=1.2)
    d.txt(cx, cy + 3.4, 'AC01', 7.0, K, 'bold', 'middle', ls=0.3)
    # janelas
    for ident, ym in (('J01', 0.95), ('J02', 3.40)):
        cx, cy = d.PM(qa.FACE_LESTE + 0.16, ym)
        d.txt(cx, cy, ident, 7.0, K70, 'bold', 'start', rot=90)

    # cotas (em metros, convertidas para pt do scan)
    def ch(x0m, x1m, ym, off, texto=None):
        cota_h(d, px_(x0m), px_(x1m), py_(ym), off, texto, size=7.8)
    def cv(y0m, y1m, xm, off, texto=None):
        cota_v(d, py_(y0m), py_(y1m), px_(xm), off, texto, size=7.8)
    o, l, p = qa.folgas(qa.CASAL[1], qa.CASAL[2])
    ch(qa.X_TRILHO + qa.FOLGA_TECIDO, cr[0], 0.68, 0, br(o))
    ch(cr[2], qa.FACE_LESTE, 0.68, 0, br(l))
    cv(cr[3], qa.Y_CORTINA - qa.FOLGA_TECIDO, 5.70, 0, br(p))
    ch(qa.X_CURVA, qa.FIX_OESTE, qa.Y_CORTINA, 22, br(qa.FIX_OESTE - qa.X_CURVA))
    ch(qa.FIX_OESTE, qa.FIX_LESTE, qa.Y_CORTINA, 22, '%s sem apoio no teto' % br(qa.VAO_LIVRE))
    ch(qa.FIX_LESTE, qa.X_FIM, qa.Y_CORTINA, 22, br(qa.X_FIM - qa.FIX_LESTE))
    ch(qa.VIDRO[0], qa.VIDRO[2], qa.Y_CORTINA, -16, '%s sobre o vidro' % br(qa.VIDRO[2] - qa.VIDRO[0]))
    cv(qa.VIDRO[1], qa.Y_CORTINA, 7.00, 0, br(qa.Y_CORTINA - qa.VIDRO[1]))
    cv(qa.Y_CORTINA, qa.VIDRO[3], 7.00, 0, br(qa.VIDRO[3] - qa.Y_CORTINA))
    c = d.PM(4.05, 3.32)
    d.txt(c[0], c[1], 'fim da ponta da escada (acima)', 7.2, K70, 'normal', 'start')

    # recorte: máscaras fora da janela de desenho
    d.rect(-60, 120, OX - 8 + 60, H - 60, fill=BG)
    d.rect(-60, 858, 750, H - 800, fill=BG)
    d.rect(628, 120, 60, 760, fill=BG)

    base = 866
    d.set_plan(OX, OY, S)
    escala(d, base)
    legenda(d, [('line', DEMO, 'Cortina CT01 — apoios só no concreto'),
                ('ghost', CIANO, 'Moldura FC01 — 2027/28'),
                ('fill', AMARELO, 'Claraboia de vidro'),
                ('fill', CIANO18, 'Quarto com a cortina fechada'),
                ('fill', AMARELO40, 'Área de troca')],
            70, base + 36, largura=600)

    d.line(700, 140, 700, 916, RULE, 0.8, opacity=0.8)
    cx2, cw = 730, W - MARGIN - 730
    fim = tabela(d, cx2, 160, cw,
                 [('Grandeza', 0.30, 'start'), ('Valor', 0.20, 'end'), ('Leitura', 0.50, 'end')],
                 TAB_NUM, titulo='QUARTO ADAPTÁVEL — NÚMEROS', alt=18)
    fim = tabela(d, cx2, fim + 34, cw,
                 [('Cama', 0.28, 'start'), ('Medida m', 0.18, 'end'), ('Pé oeste', 0.12, 'end'),
                  ('Cabeceira', 0.14, 'end'), ('Lado sul', 0.13, 'end'), ('Atende 0,60', 0.15, 'end')],
                 TAB_CAMA, titulo='CAMA × CIRCULAÇÃO — LESTE–OESTE, JUNTO À PAREDE NORTE', alt=18)
    fim = tabela(d, cx2, fim + 34, cw,
                 [('ID', 0.12, 'start'), ('Item', 0.70, 'start'), ('Fase', 0.18, 'end')],
                 TAB_FASE, titulo='ESCOPO — O QUE ENTRA AGORA E O QUE FICA PARA 2027/28', alt=18)
    fim = tabela(d, cx2, fim + 34, cw,
                 [('Trilho CT01 — trecho', 0.46, 'start'), ('De – até (m)', 0.36, 'end'), ('Medida', 0.18, 'end')],
                 TAB_TRILHO, titulo='TRILHO CT01 — MEDIDAS NO EIXO, A PARTIR DO CANTO NOROESTE', alt=17)
    paragrafos(d, cx2, fim + 24, cw, NOTAS, size=8.0, lh=11.0, gap=5.0)

    rodape(d,
           'Circulação mínima adotada de 0,60 m em volta da cama; cortina com ~5 cm de tecido de cada lado do eixo do trilho. Medidas sobre o scan de 02.09.2026.',
           'O vidro da claraboia não recebe fixação. Apoios do trilho e da moldura só no concreto em volta, com posição confirmada em estrutura antes de furar.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-13-quarto-claraboia')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-13-quarto-claraboia-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 13: quarto adaptável e claraboia')
    exportar_png(caminho, os.path.join(pasta, 'prancha-13-quarto-claraboia.png'))
    print('ok prancha 13')
