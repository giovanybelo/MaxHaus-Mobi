# -*- coding: utf-8 -*-
"""Prancha 05 — Teto: laje aparente, iluminação e ar-condicionado (REV. K).

Substitui as pranchas anteriores de iluminação e de ar-condicionado: sem forro,
as duas disciplinas dividem a mesma laje e precisam ser resolvidas juntas.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'
PRANCHA = 'Prancha 05 / 12'

# --- trilhos eletrificados: (id, (x0,y0), (x1,y1), nº de spots) em metros ---
TRILHOS = [
    ('TR1', (4.75, 0.95), (7.50, 0.95), 4),   # jantar
    ('TR2', (4.55, 3.20), (4.55, 5.30), 3),   # sala, eixo norte-sul (encurtado: não cruza o TR3)
    ('TR3', (4.20, 5.60), (7.50, 5.60), 4),   # sala, faixa sul — recuado da drywall
    ('TR4', (1.45, 3.90), (1.45, 6.40), 4),   # cozinha
    ('TR5', (3.85, 8.28), (7.50, 8.28), 3),   # quarto, no eixo de P02 e P03
    ('TR6', (1.45, 7.50), (1.45, 9.00), 3),   # closet, alinhado ao TR4
]

# id do trilho deslocado para cima do início, onde o rótulo padrão colidiria
ROTULO_ACIMA = {'TR1', 'TR5'}

# --- luminárias de destaque (corpo maior que os spots dos trilhos) ----------
DESTAQUES = [
    ('P01', 6.12, 0.98, 'jantar'),
    ('P02', 6.10, 8.28, 'cama'),
    ('P03', 3.90, 8.28, 'office'),
]

# --- pontos existentes marcados pelo cliente (a confirmar em obra) ----------
EXISTENTES = [
    ('E1', 2.55, 5.15, 'arandela do espelho'),
    ('E2', 3.05, 5.15, 'arandela do espelho'),
    ('E3', 3.05, 5.70, 'luz do box'),
    ('E4', 5.17, 9.25, 'arandela'),
    ('E5', 7.37, 9.25, 'arandela'),
    ('E6', 0.42, 5.30, 'luz da cozinha'),
]

# --- banheiro: único ambiente com forro --------------------------------------
EMBUTIDOS_WC = [(2.60, 4.85), (3.30, 4.85)]

# --- ar-condicionado, coifa e exaustão --------------------------------------
MAQUINAS = [
    ('AC01', 4.70, 2.25, 'evaporadora — social + cozinha'),
    ('AC02', 5.72, 9.15, 'evaporadora — quarto + closet'),
    ('EX01', 3.06, 6.06, 'exaustor do banheiro'),
    ('CF01', 0.60, 6.20, 'coifa da cozinha'),
]

TAB_LUZ = [
    ('Sala',     '150 lux', '7.188 lm', '2.700 K'),
    ('Quarto',   '150 lux', '4.188 lm', '2.700 K'),
    ('Cozinha',  '300 lux', '5.563 lm', '3.000 K'),
    ('Jantar',   '150 lux', '1.844 lm', '2.700 K'),
    ('Closet',   '200 lux', '2.208 lm', '3.000 K'),
    ('Banheiro', '200 lux', '1.583 lm', '3.000 K'),
]
TAB_AR = [
    ('Social + cozinha',   '37,80 m²', '22.680 BTU/h', '30.240 BTU/h'),
    ('Quarto + closet',    '18,70 m²', '11.220 BTU/h', '14.960 BTU/h'),
    ('Total sem banheiro', '56,50 m²', '33.900 BTU/h', '45.200 BTU/h'),
]

NOTAS = [
    ['**Não há forro: a laje de concreto é o teto acabado, a 2,62 m do piso.',
     'Com o forro atual são 2,42 m; a retirada (D07) devolve os 0,20 m de plenum. É nessa faixa que',
     'entram trilho, perfilado e evaporadora — e é ela que dá os 0,33 m acima da porta de correr de',
     '2,29 m. Fora do banheiro, único ambiente que mantém forro, nada de embutido.'],
    ['**Fiação e infraestrutura ficam à vista.',
     'Perfilados ou eletrocalhas pintadas, alinhados às vigas e aos trilhos: o caminho da fiação',
     'vira desenho, não sobra de obra.'],
    ['**P01, P02 e P03 são as três luminárias de destaque pedidas pelo cliente',
     '— jantar, cama e office. Corpo e diâmetro maiores que os spots dos trilhos, em pendente',
     'ou plafon de sobrepor. No quarto o TR5 passa a correr no eixo de P02 e P03, a 8,28 m: as duas',
     'podem ser alimentadas pelo próprio trilho, com adaptador, dispensando saídas novas na laje.'],
    ['**Traçado dos trilhos revisado conforme a sua marcação:',
     'TR3 desceu para 5,60 m, ganhando recuo da drywall; TR5 desceu para 8,28 m, no eixo das duas',
     'luminárias do quarto; TR6 saiu de junto da parede oeste e foi para 1,45 m, no mesmo eixo do',
     'TR4 — os dois lêem como uma linha só. O TR2 foi encurtado para 5,30 m: no traçado anterior',
     'ele cruzava o TR3 no meio da sala, e dois trilhos não se cruzam — se tiverem de se encontrar,',
     'é com conector T.'],
    ['**Sem forro para dutar, e fachada envidraçada a noroeste.',
     'Evaporadoras hi-wall ou cassete aparente, com frigorígena, dreno e interligação elétrica',
     'aparentes, em calha e com caimento contínuo. Sala e jantar tomam o sol da tarde: dimensionar',
     'pela coluna base sol, não pela sombra. Somente Electrolux — marca igual não garante compatibilidade.'],
    ['**A piscina do pavimento superior fica sobre a sala — 1,92 × 3,00 m, centrada em',
     '6,13 / 3,14 m do canto noroeste. Essa laje não recebe furação: nem luminária, nem trilho,',
     'nem evaporadora ou tubulação podem invadi-la, e a região exige impermeabilização e',
     'sobrecarga verificadas em estrutura. Nenhum trilho a invade: TR2 corre a oeste e TR3 passa',
     '0,96 m ao sul.'],
    ['**A reserva AC01 caía dentro da projeção da piscina.',
     'Foi deslocada para oeste, mantendo a insuflação para sala e jantar. A posição definitiva',
     'depende de confirmar apoio acima do limite sala/jantar e o modelo da condensadora existente:',
     'não assumir que ela admite duas evaporadoras.'],
    ['**Vazões de referência, a validar com perda de carga do duto:',
     'banheiro 3,8 × 2,42 × 10 = 92,0 m³/h (mantém forro); coifa 8,9 × 2,62 × 12 = 279,8 m³/h — o',
     'segundo só valeria com cozinha isolada; integrada, seleciona-se por captura. Rotas próprias.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Teto: laje aparente, iluminação e ar-condicionado',
              'Distribuição conceitual sobre a laje de concreto. Reservas de posição, não quantidade final de luminárias nem de equipamentos.',
              REV, 'sem forro — tudo aplicado na laje',
              'piscina do pavimento superior sobre a sala')

    S = 70.0
    d.set_plan(70, 156, S)
    fundo_ambientes(d, K07)
    paredes(d, estado='novo')
    janelas(d)
    porta(d, DOOR_ENTRADA)
    porta(d, DOOR_BANHO)
    porta_correr_horizontal(d, PORTA_NOVA, lado='n', sentido='e')
    escada(d)
    norte(d, 140, 212, 15, nota='uma')

    # banheiro: único ambiente com forro
    pp = [d.P(px, py) for px, py in ROOMS['banheiro']['poly']]
    d.path(path_d(pp), fill=WET, opacity=0.6)
    d.path(path_d(pp), fill='none', stroke=WET_LINE, sw=0.9, dash='3 2.5')

    # área da piscina do pavimento superior
    x, y, w_, h_ = d.R(AREA_PISCINA)
    d.rect(x, y, w_, h_, fill=AMARELO, opacity=0.30)
    d.rect(x, y, w_, h_, fill='none', stroke=K, sw=1.2, dash='6 4')
    t = -h_
    while t <= w_:
        ax, ay = x + max(0.0, t), y + h_ - max(0.0, -t) * 0 - (h_ - min(h_, h_)) 
        x0 = x + max(0.0, t); y0 = y + h_ - (x0 - (x + t))
        x1 = min(x + w_, x + t + h_); y1 = y + h_ - (x1 - (x + t))
        if x1 > x0:
            d.line(x0, y0, x1, y1, K, 0.5, opacity=0.22)
        t += 13
    cxp, cyp = d.PM(PISCINA_CX, PISCINA_CY)
    d.line(cxp - 11, cyp, cxp + 11, cyp, K, 1.0)
    d.line(cxp, cyp - 11, cxp, cyp + 11, K, 1.0)
    d.circle(cxp, cyp, 3.4, fill='none', stroke=K, sw=1.0)
    d.txt(x + w_ / 2, y + h_ / 2 - 40, 'ÁREA DA PISCINA', 7.6, K, 'bold', 'middle', ls=0.5)
    d.txt(x + w_ / 2, y + h_ / 2 - 29, 'pavimento superior', 7.2, K70, 'normal', 'middle')
    d.txt(x + w_ / 2, y + h_ / 2 + 34, '1,92 × 3,00 m  ·  5,76 m²', 7.2, K70, 'normal', 'middle')
    d.txt(x + w_ / 2, y + h_ / 2 + 45, 'centro em 6,13 / 3,14 m', 7.0, K70, 'normal', 'middle')

    for k, lx, ly in (('jantar', 520.0, 142.0), ('sala', 470.0, 300.0),
                      ('cozinha', 300.0, 352.0), ('closet', 277.6, 505.0),
                      ('quarto', 520.0, 442.0), ('banheiro', 380.6, 430.0)):
        ROOMS[k]['lx'], ROOMS[k]['ly'] = lx, ly
    rotulos(d, areas=False, size=8.4)

    # trilhos + spots
    for (ident, p0, p1, n) in TRILHOS:
        a = d.PM(*p0); b = d.PM(*p1)
        d.line(a[0], a[1], b[0], b[1], BG, 5.0)
        d.line(a[0], a[1], b[0], b[1], INK, 2.6, cap='round')
        for i in range(n):
            t_ = (i + 0.5) / float(n)
            cx = a[0] + (b[0] - a[0]) * t_
            cy = a[1] + (b[1] - a[1]) * t_
            d.circle(cx, cy, 4.0, fill=BG, stroke=INK, sw=1.2)
            d.circle(cx, cy, 1.5, fill=INK)
        vertical = abs(b[0] - a[0]) < 1
        if ident in ROTULO_ACIMA:
            d.txt(a[0], a[1] - 12, ident, 7.2, INK, 'bold', 'start', ls=0.4)
        elif vertical:
            d.txt(a[0] + 9, a[1] - 6, ident, 7.2, INK, 'bold', 'start', ls=0.4)
        else:
            d.txt(a[0] - 9, a[1] + 3, ident, 7.2, INK, 'bold', 'end', ls=0.4)

    # luminárias de destaque
    for (ident, xm, ym, nome) in DESTAQUES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 10.5, fill=AMARELO, stroke=K, sw=1.8)
        d.circle(cx, cy, 3.4, fill=NEW)
        d.txt(cx, cy + 22, ident + ' · ' + nome, 7.4, NEW, 'bold', 'middle', ls=0.3)

    # embutidos do banheiro
    for (xm, ym) in EMBUTIDOS_WC:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.0, fill=BG, stroke=WET_LINE, sw=1.3)

    # pontos existentes
    for (ident, xm, ym, nome) in EXISTENTES:
        cx, cy = d.PM(xm, ym)
        d.circle(cx, cy, 4.6, fill='none', stroke=EXIST, sw=1.3)
        d.line(cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2, EXIST, 1.0)

    # máquinas
    for (ident, xm, ym, nome) in MAQUINAS:
        cx, cy = d.PM(xm, ym)
        if ident.startswith('AC'):
            d.rect(cx - 18, cy - 6, 36, 12, fill=CIANO35, stroke=K, sw=1.2)
            d.txt(cx, cy + 3.4, ident, 7.0, K, 'bold', 'middle', ls=0.3)
        else:
            d.circle(cx, cy, 6.0, fill=CIANO35, stroke=K, sw=1.2)
            d.line(cx - 3, cy, cx + 3, cy, K, 1.0)
            d.line(cx, cy - 3, cx, cy + 3, K, 1.0)
            d.txt(cx + 10, cy + 3, ident, 7.0, K, 'bold', 'start', ls=0.3)

    escala(d, 156 + BUILDING_H * S + 26)
    legenda(d, [('line', INK, 'Trilho eletrificado + spots de sobrepor'),
                ('fill', AMARELO, 'Luminária de destaque (corpo maior)'),
                ('dot', EXIST, 'Ponto existente — confirmar'),
                ('dot', WET_LINE, 'Embutido no forro do banheiro'),
                ('fill', CIANO35, 'Ar-condicionado / exaustão')],
            70, 156 + BUILDING_H * S + 64, largura=600)

    d.line(690, 140, 690, 900, RULE, 0.8, opacity=0.8)

    cx, cw = 722, W - MARGIN - 722
    fim = tabela(d, cx, 160, cw,
                 [('Ambiente', 0.34, 'start'), ('Alvo geral', 0.22, 'end'),
                  ('Fluxo inicial', 0.22, 'end'), ('Temperatura de cor', 0.22, 'end')],
                 TAB_LUZ, titulo='ILUMINAÇÃO POR AMBIENTE')
    fim = tabela(d, cx, fim + 34, cw,
                 [('Zona', 0.34, 'start'), ('Área', 0.22, 'end'),
                  ('Base sombra', 0.22, 'end'), ('Base sol', 0.22, 'end')],
                 TAB_AR, titulo='AR-CONDICIONADO — REGRA SIMPLIFICADA 600/800 BTU/h POR m²')
    paragrafos(d, cx, fim + 24, cw, NOTAS, size=8.4, lh=12.4, gap=6.0)

    rodape(d,
           'Fluxo = área × lux ÷ (0,60 × 0,80). Fatores de utilização e manutenção são hipóteses; a laje aparente escura reduz o fator de utilização e deve ser reavaliada.',
           'Carga térmica não é carga final: a fachada envidraçada a noroeste, a piscina sobre a sala, a escada aberta e a ocupação mudam o resultado. Estudar 2 ou 3 evaporadoras; não há número fechado.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-05-teto')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-05-teto-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 05: teto, iluminação e ar-condicionado')
    exportar_png(caminho, os.path.join(pasta, 'prancha-05-teto.png'))
    print('ok prancha 04')
