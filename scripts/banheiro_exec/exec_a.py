# -*- coding: utf-8 -*-
"""Caderno EXECUTIVO do banheiro — folhas de desenho BE-01 a BE-11 (equipe de obra)."""
from lib import *      # noqa

CAD = 'CADERNO EXECUTIVO'
OX, OY, N = 190.0, 215.0, 15       # planta padrão 1:15
CX = 760.0                         # coluna de texto
CW = W - MARGIN - CX


def _cotas_planta(f, P, interno=True):
    if interno:
        f.cadeia_h(P, [0, LARG], -PAREDE, -34)
        f.cadeia_v(P, [0, BOX_Y, COMP], -PAREDE, -34)
    # parede da porta, por fora
    xe = LARG + PAREDE
    f.cadeia_v(P, [-PAREDE, PORTA[0], PORTA[1], COMP + PAREDE], xe, 205)
    c = P(xe, -PAREDE)
    f.t(c[0] + 205, c[1] - 10, 'por fora', 6.4, K70, False, 'middle')
    f.cota_v(c[0] + 232, c[1], P(xe, COMP + PAREDE)[1], '2880', 7.0)


def be01():
    f = Folha(CAD, 'BE-01', 'Planta baixa do banheiro', 'Faces acabadas, com as medidas de obra de 14/11/2026. É a folha de referência de todas as outras.', '1:15')
    P, s = f.planta(OX, OY, N)
    f.ralos(P, s)
    f.ids_paredes(P)
    _cotas_planta(f, P)
    # cotas internas
    f.cadeia_h(P, [0, BANC[2], VASO_X, LARG], 760, 0)
    f.cadeia_v(P, [0, BANC[1], BANC[3]], 520, 0)
    f.cadeia_v(P, [BOX_Y, AT[1], AT[3]], 620, 0)
    f.cadeia_h(P, [0, AT[2], LARG], 2460, 0)
    f.cadeia_v(P, [0, PORTA[0], PORTA[1], COMP], LARG - 70, 0)
    c = P(LARG / 2, BOX_Y)
    f.t(c[0] + 60, c[1] - 6, 'vidro do box', 6.6, K70, False, 'middle')
    f.legenda(OX - 22, 880, [('fill', K20, 'Área técnica do chuveiro (AT-B)'), ('fill', CIANO18, 'Box'),
                             ('line', CIANO, 'Vidro do box'), ('fill', K45, 'Ralos R1 e R2')])
    y = f.tab(CX, 150, CW, [('Item', 0.20, 'start'), ('Medida (mm)', 0.26, 'start'), ('De onde vem', 0.54, 'start')], [
        ('Banheiro', '1420 × 2680', 'largura do modelo R95; comprimento = 2880 por fora, menos duas paredes de 100'),
        ('Parede da porta', '880 + 800 + 1200', 'medida por fora, lado da sala, de norte a sul (14/11)'),
        ('P02 · porta', 'vão 800 × 2150', 'medida de obra; abre para fora, sentido anti-horário'),
        ('Box', '1420 × 920', 'fundo de 920 mantido; vidro na linha a 1760 da parede do vaso'),
        ('AT-B · área técnica', '800 × 250', 'medida de obra; desenhada no canto sudoeste do box'),
        ('B01 · bancada', '1600 × 400, saia 100', 'medida de obra; topo a +980, sobre o gabinete'),
        ('Gabinete', '1600 × 400 × 880 (altura)', 'medida de obra; reaproveitado'),
        ('Espelho', '1600 × 900', 'medida de obra; base proposta a +1340'),
        ('Vaso', 'eixo a 980 da P3', 'modelo R95; conferir ponto de esgoto'),
        ('R1 · ralo linear', '720 × 90', 'modelo R95; no box, junto à área técnica'),
        ('R2 · ralo seco', 'grelha 100 × 100', 'ao lado do vaso; posição da caixa existente a levantar'),
        ('Forro', '+2500', 'modelo R95; laje a +2620'),
    ], titulo='MEDIDAS DE REFERÊNCIA')
    f.par(CX, y + 26, CW, [
        ('As paredes têm nome.', 'P5 é a do vaso (norte); P4, a da porta (leste); P1, o fundo do box (sul); P3, a da bancada (oeste). '
         'P2 e P6 são as duas faces da área técnica. A paginação de cada uma está nas folhas BE-13 a BE-17.'),
        ('O que ainda é premissa.', 'A área técnica foi desenhada encostada no fundo do box: sobram 120 mm de parede entre ela e o vidro. '
         'A bancada foi desenhada encostada no vidro do box: sobram 160 mm até a parede do vaso. Se em obra for o contrário, '
         'as medidas não mudam, só a posição: avisar antes de marcar a paginação da P3.'),
        ('Comprimento por dentro.', 'Os 2680 saem de 2880 por fora menos duas paredes de 100 mm. Se as paredes tiverem 120 mm, '
         'o banheiro tem 2640 por dentro. Medir de parede a parede depois de retirar o revestimento.'),
    ])
    return f


def be02():
    f = Folha(CAD, 'BE-02', 'Demolição e o que preservar', 'O que sai, o que fica e o que é desmontado para voltar. Não usar esta folha para medir revestimento novo.', '1:15')
    P, s = f.planta(OX, OY, N, box_cor=None, piso='#ffd9f2', rotulos=False)
    d = f.d
    for (x0, y0, x1, y1, cor) in [(0, -PAREDE * 0.35, LARG, 0, DEMO), (LARG, 0, LARG + PAREDE * 0.35, COMP, DEMO),
                                  (0, COMP, LARG, COMP + PAREDE * 0.35, DEMO), (-PAREDE * 0.35, 0, 0, COMP, DEMO)]:
        a, b = P(x0, y0), P(x1, y1)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=cor, opacity=0.55)
    a, b = P(LARG, PORTA[0]), P(LARG + PAREDE, PORTA[1])
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BG)
    f.ralos(P, s)
    for rot, x, y in (('D1', 900, 1250), ('D2', 1310, 2100), ('D3', 200, 900), ('M1', 980, 430), ('P', 125, 2280), ('M2', 720, 1700), ('D4', 900, 2300)):
        c = P(x, y)
        d.circle(c[0], c[1], 11, fill=BG, stroke=K, sw=1.0)
        f.t(c[0], c[1] + 3, rot, 6.8, K, True, 'middle')
    f.legenda(OX - 22, 880, [('fill', '#ffd9f2', 'Piso e base: retirar'), ('fill', DEMO, 'Revestimento de parede: retirar'),
                             ('fill', K20, 'Área técnica: não demolir')])
    y = f.tab(CX, 150, CW, [('ID', 0.08, 'start'), ('Serviço', 0.62, 'start'), ('Quantidade', 0.30, 'end')], [
        ('D1', 'Retirar piso, argamassa e base do banheiro e do box, de forma controlada, até o contrapiso', '3,81 m²'),
        ('D2', 'Retirar o revestimento de todas as paredes, até o forro atual', '~19,5 m² (medir)'),
        ('D3', 'Retirar tampo e cuba antigos; desmontar e guardar o gabinete (1600 × 400 × 880)', '1 conjunto'),
        ('D4', 'Retirar o forro existente; volta novo a +2500', '3,81 m²'),
        ('M1', 'Desmontar o vaso com caixa acoplada, tampar o esgoto e guardar', '1 peça'),
        ('M2', 'Desmontar vidro e ferragens do box, etiquetar e proteger', '1 conjunto'),
        ('P', 'Área técnica do chuveiro (AT-B): prumada do condomínio. Preservar e proteger', '800 × 250 mm'),
    ], titulo='ESCOPO DE DEMOLIÇÃO')
    f.passos(CX, y + 30, CW, [
        ('Fechar a água e proteger.', 'Fechar os registros, proteger ralos e o piso de fora do banheiro. Fotografar todas as paredes antes de quebrar.', True),
        ('Desmontar o que volta.', 'Vaso, gabinete, vidro do box e ferragens saem inteiros, etiquetados, para um lugar seco.', False),
        ('Forro e paredes.', 'Retirar o forro e o revestimento das paredes de cima para baixo. Em volta da AT-B, só ferramenta manual.', False),
        ('Piso.', 'Retirar piso e argamassa sem romper a impermeabilização antiga mais do que o necessário. Não cortar laje, viga nem pilar.', True),
        ('Medir antes de reconstruir.', 'Com a parede no osso: comprimento e largura por dentro, prumo, posição do esgoto do vaso, dos dois ralos e '
         'dos registros do chuveiro. Anotar na BT-02. Só depois liberar regularização e impermeabilização.', True),
    ])
    return f


def be03():
    f = Folha(CAD, 'BE-03', 'Níveis e rebaixo do piso', 'O porcelanato do banheiro termina no mesmo nível do monolítico Sinesse Pro de fora. Sem soleira: um perfil de metal marca a troca de piso.', 'cortes 1:2 na vertical')
    d = f.d
    # ---- corte A: vão da porta -------------------------------------------------
    x0, y0, e = 70.0, 300.0, MM / 2.0 * 2.2        # exagero vertical legível: 1 mm = 3,67 u
    f.t(x0, 150, 'CORTE A  ·  vão da porta P02', 9.4, INK, True)
    f.t(x0, 163, 'vista de sul para norte: sala à direita, banheiro à esquerda', 7.6, INK_SOFT)
    xm = x0 + 300
    HB = 120.0                                     # altura desenhada da base
    # sala (direita): monolítico 3 + base
    d.rect(xm, y0, 290, 3 * e, fill=K45)
    d.rect(xm, y0 + 3 * e, 290, HB, fill=K12, stroke=K45, sw=0.5)
    # banheiro (esquerda): porcelanato 9 + argamassa 5 + impermeabilização/proteção 4 + regularização
    d.rect(x0, y0, 298, 9 * e, fill=BRANCO, stroke=K, sw=0.8)
    d.rect(x0, y0 + 9 * e, 298, 5 * e, fill=K20)
    d.rect(x0, y0 + 14 * e, 298, 4 * e, fill=CIANO)
    d.rect(x0, y0 + 18 * e, 298, HB - 15 * e, fill=K12, stroke=K45, sw=0.5)
    d.rect(x0, y0 + HB + 3 * e, 590, 26, fill=K45)
    f.t(x0 + 295, y0 + HB + 3 * e + 17, 'LAJE  ·  não rebaixar', 7.4, BRANCO, True, 'middle')
    d.rect(xm - 3, y0, 5, 14 * e, fill=DEMO)                        # perfil metálico
    d.line(x0 - 20, y0, x0 + 620, y0, DEMO, 0.9)
    f.t(x0 + 624, y0 + 3, '±0  piso pronto', 7.4, DEMO, True)
    for (yy, txt, lado) in ((y0 + 4.5 * e, 'porcelanato Confete, 9 mm', 0), (y0 + 11.5 * e, 'argamassa colante, ~5 mm', 0),
                            (y0 + 16 * e, 'impermeabilização + proteção', 0), (y0 + 18 * e + 30, 'regularização com caimento (contrapiso)', 0)):
        f.t(x0 + 8, yy + 2.5, txt, 6.8, K, False)
    f.t(xm + 12, y0 + 3 * e + 16, 'monolítico Sinesse Pro, 2 a 4 mm, sobre a base preparada', 6.8, INK)
    f.t(xm - 1, y0 - 22, 'perfil de metal, 3 mm à vista', 7.0, DEMO, True, 'middle')
    d.line(xm - 0.5, y0 - 18, xm - 0.5, y0 - 2, DEMO, 0.7)
    f.t(x0 + 150, y0 - 10, 'BANHEIRO', 8.0, INK, True, 'middle', ls=0.8)
    f.t(xm + 150, y0 - 10, 'SALA DE TV', 8.0, INK, True, 'middle', ls=0.8)
    f.cota_v(x0 - 14, y0, y0 + 14 * e, '14', 6.8)
    f.cota_v(xm + 300, y0, y0 + 3 * e, '3', 6.8, lado=1)
    # ---- corte B: box -------------------------------------------------------------
    yb = 620.0
    f.t(x0, yb - 90, 'CORTE B  ·  box, de leste para oeste', 9.4, INK, True)
    f.t(x0, yb - 77, 'da parede da porta (direita) até o ralo linear junto à área técnica (esquerda)', 7.6, INK_SOFT)
    sx = 590.0 / LARG
    xr = x0 + 357 * sx              # eixo do ralo
    xat = x0 + 250 * sx
    d.rect(x0, yb - 60, xat - x0, 60 + 25 * e, fill=K20, stroke=K, sw=0.8)
    f.t((x0 + xat) / 2, yb - 25, 'AT-B', 7.0, K, True, 'middle')
    pts = [(x0 + 590, yb + 10 * e), (xr + 45 * sx, yb + 25 * e), (xr - 45 * sx, yb + 25 * e), (xat, yb + 24 * e)]
    d.path('M' + ' L'.join('%.1f %.1f' % p for p in pts), stroke=K, sw=1.6)
    d.path('M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (x0 + 590, yb + 10 * e, xr + 45 * sx, yb + 25 * e, xr + 45 * sx, yb + 40 * e, x0 + 590, yb + 40 * e),
           fill=K12, stroke='none')
    d.rect(xr - 45 * sx, yb + 25 * e, 90 * sx, 14 * e, fill=K45)
    d.line(x0 - 20, yb, x0 + 620, yb, DEMO, 0.9)
    f.t(x0 + 624, yb + 3, '±0  piso do banheiro', 7.4, DEMO, True)
    f.t(x0 + 590, yb + 10 * e - 6, '-10 na entrada do box', 7.0, INK, True, 'end')
    f.t(xr, yb + 25 * e + 14 * e + 12, 'R1 · ralo linear a -25', 7.0, INK, True, 'middle')
    f.t((xr + x0 + 590) / 2, yb + 15 * e - 8, 'caimento ~1,5% (15 mm em 1,02 m)', 7.0, INK_SOFT, False, 'middle')
    # ---- tabela e texto ---------------------------------------------------------------
    y = f.tab(CX, 150, CW, [('Ponto', 0.42, 'start'), ('Nível', 0.18, 'end'), ('Como se chega', 0.40, 'end')], [
        ('Piso pronto da sala (monolítico)', '±0', 'referência da obra'),
        ('Piso pronto do banheiro', '±0', 'porcelanato 9 + argamassa ~5'),
        ('Base do banheiro, sob a argamassa', '-14', 'mais impermeabilização e proteção'),
        ('Base da sala, sob o monolítico', '-2 a -4', 'conforme o sistema Sinesse Pro'),
        ('Entrada do box, na linha do vidro', '-10', 'desnível de contenção'),
        ('Ralo linear R1', '-25', 'ponto mais baixo'),
        ('Ralo R2, ao lado do vaso', '-3 a -5', 'caimento leve do piso seco'),
    ], titulo='NÍVEIS — REFERÊNCIA ±0 NO PISO PRONTO')
    f.par(CX, y + 26, CW, [
        ('A base do banheiro fica 10 a 12 mm abaixo da base da sala.', 'É a conta 9 + 5 - (2 a 4). Somar a espessura real da impermeabilização e da proteção. '
         'Conferir a espessura do Confete na etiqueta do lote: há catálogo antigo com 10,8 mm.'),
        ('Rebaixar não é quebrar laje.', 'Depois de tirar o piso antigo, medir o que sobrou. Se a altura já existe, só regularizar; se faltar, '
         'retirar contrapiso, nunca a laje. Registrar base existente, base alvo e a diferença.'),
        ('Perfil de metal no vão da porta.', 'Um perfil com 3 mm à vista, topo no nível do piso pronto, no eixo da folha fechada. '
         'Junta elástica dos dois lados. Sem soleira e sem degrau; a folha da P02 fica com 12 mm de folga embaixo.'),
        ('O esgoto manda no rebaixo.', 'Vaso e os dois ralos precisam de queda até a prumada. Se o piso sobe ou desce, conferir a cota de saída '
         'de cada um antes de fechar o nível. Sem queda, não se libera a regularização.'),
        ('Retorno curto junto à área técnica.', 'Entre o ralo linear e a área técnica sobram ~60 mm. Não manter ali o -10 da entrada do box: '
         'o piso desse trecho acompanha a borda do ralo. Decidir com o responsável técnico antes de cortar o porcelanato.'),
    ])
    return f


def be04():
    f = Folha(CAD, 'BE-04', 'Impermeabilização', 'Onde entra, até que altura sobe e em que ordem. O revestimento não impermeabiliza: quem segura a água é a membrana.', '1:15')
    P, s = f.planta(OX, OY, N, objetos=False, box_cor='#9fe8f0', piso=CIANO18, rotulos=False, porta=False)
    d = f.d
    # faixas de parede: box até o forro, resto rodapé de 300
    for (x0, y0, x1, y1, cor) in [(0, BOX_Y, -30, COMP, CIANO), (0, COMP, LARG, COMP + 30, CIANO), (LARG, BOX_Y, LARG + 30, COMP, CIANO),
                                  (0, 0, -18, BOX_Y, '#9fe8f0'), (0, 0, LARG, -18, '#9fe8f0'), (LARG, 0, LARG + 18, PORTA[0], '#9fe8f0'),
                                  (LARG, PORTA[1], LARG + 18, BOX_Y, '#9fe8f0')]:
        a, b = P(x0, y0), P(x1, y1)
        d.rect(min(a[0], b[0]), min(a[1], b[1]), abs(b[0] - a[0]), abs(b[1] - a[1]), fill=cor)
    f.ralos(P, s)
    c = P(LARG, (PORTA[0] + PORTA[1]) / 2)
    d.rect(c[0], P(0, PORTA[0])[1], PAREDE * s + 26, 800 * s, fill=CIANO18)
    f.t(c[0] + 36, c[1] - 4, 'I1 avança', 6.8, INK, True)
    f.t(c[0] + 36, c[1] + 6, '300 mm além', 6.8, INK)
    f.t(c[0] + 36, c[1] + 16, 'da porta', 6.8, INK)
    for rot, x, y in (('I1', 900, 1100), ('I2', 850, 2250), ('I4', 835, 2650), ('I5', 520, 2300), ('I5', 1280, 420), ('I3', 60, 600)):
        c = P(x, y)
        d.circle(c[0], c[1], 11, fill=BG, stroke=K, sw=1.0)
        f.t(c[0], c[1] + 3, rot, 6.8, K, True, 'middle')
    f.legenda(OX - 22, 880, [('fill', CIANO18, 'Piso seco'), ('fill', '#9fe8f0', 'Box e rodapé de 300'), ('fill', CIANO, 'Parede do box até +2500')])
    y = f.tab(CX, 150, CW, [('ID', 0.08, 'start'), ('Onde', 0.50, 'start'), ('Até onde', 0.42, 'end')], [
        ('I1', 'Todo o piso do banheiro, inclusive sob a bancada e o vão da porta', 'avança 300 mm para fora da porta'),
        ('I2', 'Piso do box e as três paredes do box, com a face da área técnica', 'do piso ao forro (+2500)'),
        ('I3', 'Rodapé nas paredes fora do box', '300 mm acima do piso pronto'),
        ('I4', 'Nicho do box: fundo, laterais, base e teto', 'base com caimento para dentro do box'),
        ('I5', 'Ralos R1 e R2 e passagens de tubo', 'flange e reforço com tela'),
        ('I6', 'Parede da bancada, atrás da cuba', 'faixa de +700 a +1400'),
    ], titulo='ÁREAS A IMPERMEABILIZAR')
    y = f.passos(CX, y + 30, CW, [
        ('Base pronta.', 'Regularização com os caimentos já feitos (BE-03), cantos arredondados em meia-cana, superfície firme, seca e limpa.', True),
        ('Reforços primeiro.', 'Tela de poliéster em todos os cantos, no encontro piso-parede, em volta dos tubos e nas flanges dos dois ralos.', False),
        ('Membrana.', 'Cimentício flexível ou sistema equivalente, no número de demãos e no consumo da ficha do fabricante. '
         'Demãos cruzadas, respeitando o intervalo entre elas.', False),
        ('Teste de estanqueidade: 72 horas.', 'Tampar os ralos, encher com 3 a 5 cm de água e marcar o nível. Não pode baixar nem aparecer mancha no vizinho de baixo. '
         'Registrar com foto e data. Só depois proteger e revestir.', True),
        ('Proteção.', 'Camada de proteção mecânica antes da argamassa do piso. Qualquer furo feito depois é selado antes de fechar.', False),
    ])
    f.par(CX, y + 8, CW, [
        ('Sistema e consumo.', 'Referência de planejamento: ~12 m², com reserva. O produto, o primer e o tempo de cura são definidos com o responsável técnico '
         'e precisam ser compatíveis com o porcelanato e com a argamassa.'),
    ])
    return f


def be05():
    f = Folha(CAD, 'BE-05', 'Esgoto: ralo do box, ralo do vaso e vaso', 'Remodelagem dos dois ralos e reinstalação do vaso no nível novo do piso. Posições das caixas existentes a confirmar depois da demolição.', '1:15')
    P, s = f.planta(OX, OY, N)
    d = f.d
    f.ralos(P, s)
    # caimentos
    def seta(x0, y0, x1, y1):
        a, b = P(x0, y0), P(x1, y1)
        d.line(a[0], a[1], b[0], b[1], CIANO, 1.2)
        import math
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for da in (2.6, -2.6):
            d.line(b[0], b[1], b[0] + 7 * math.cos(ang + da), b[1] + 7 * math.sin(ang + da), CIANO, 1.2)
    for yy in (2000, 2300, 2560):
        seta(1340, yy, 440, yy)
    seta(700, 1500, 1240, 420)
    seta(600, 760, 1200, 330)
    c = P(880, 2130)
    f.t(c[0], c[1], 'caimento ~1,5% para o R1', 6.8, INK, False, 'middle')
    c = P(1000, 1180)
    f.t(c[0], c[1], '0,5% para o R2', 6.8, INK, False, 'middle')
    c = P(VASO_X, 300)
    d.circle(c[0], c[1], 50 * s, fill='none', stroke=DEMO, sw=1.4)
    f.t(c[0] - 62 * s, c[1] - 70 * s, 'esgoto DN100', 6.6, DEMO, True, 'end')
    f.cadeia_h(P, [0, VASO_X], 300, 0)
    f.cadeia_v(P, [0, 300], VASO_X + 330, 0)
    f.cadeia_h(P, [AT[2], R1[0], R1[2]], 2655, 0)
    f.cadeia_v(P, [R1[1], R1[3], COMP], 480, 0)
    f.cadeia_h(P, [R2[2], LARG], 300, 0)
    f.legenda(OX - 22, 880, [('line', CIANO, 'Sentido do caimento'), ('fill', K45, 'Ralos'), ('dot', BG, 'Ponto de esgoto do vaso')])
    y = f.tab(CX, 150, CW, [('ID', 0.08, 'start'), ('Peça', 0.50, 'start'), ('Dado', 0.42, 'end')], [
        ('R1', 'Ralo linear do box, com corpo, flange e grelha', '720 × 90 mm; borda a -25'),
        ('R2', 'Ralo ao lado do vaso: grelha oculta quadrada', '100 × 100 mm; sobre a caixa existente'),
        ('VS', 'Vaso com caixa acoplada, reaproveitado', 'eixo a 980 da P3; esgoto a ~300 da P5'),
        ('AV', 'Anel de vedação novo e parafusos de fixação', '1 jogo'),
        ('PR', 'Prolongadores para ajustar a altura dos ralos ao piso novo', 'medir após a demolição'),
    ], titulo='PEÇAS')
    f.passos(CX, y + 30, CW, [
        ('Levantar o que existe.', 'Com o piso aberto: centro e profundidade da caixa sifonada do R2, saída do R1, ponto de esgoto do vaso e '
         'para onde cada um corre. Marcar na planta e fotografar com trena.', True),
        ('R2, o ralo ao lado do vaso.', 'Manter a caixa sifonada e a saída onde estão. Trocar o porta-grelha por um modelo de grelha oculta 100 × 100 '
         'e ajustar a altura com prolongador até o nível do piso pronto. Manter o fecho hídrico e o acesso para limpeza.', False),
        ('R1, o ralo linear do box.', 'Assentar o corpo do ralo antes da impermeabilização, com a flange colada na membrana. '
         'Conferir saída, sifão e vazão do modelo comprado. A grelha fica 1 mm abaixo do porcelanato.', False),
        ('Caimentos.', 'Box: do vidro e da parede da porta para o R1, ~1,5%. Piso seco: caimento leve, 0,5%, para o R2. '
         'Fazer na regularização, antes da membrana; não corrigir caimento com argamassa do piso.', True),
        ('Esgoto do vaso.', 'Conferir a distância do eixo do esgoto à parede acabada com a bacia em mãos (em geral 260 a 300 mm). '
         'Ajustar a altura da boca do tubo ao piso novo: ela fica rente ao piso pronto.', True),
        ('Instalar o vaso.', 'Depois do piso rejuntado: anel de vedação novo, bacia aparafusada no piso (não só colada), '
         'engate flexível novo na entrada de água, silicone neutro na base. Testar descarga e procurar vazamento.', False),
    ])
    return f


def be06():
    f = Folha(CAD, 'BE-06', 'Água quente na torneira da pia', 'O ramal novo sai da água quente do chuveiro, dentro da área técnica, e chega ao comando da pia. É o item mais importante desta reforma.', 'planta 1:15 · elevação 1:16,5')
    P, s = f.planta(OX - 60, OY, N, porta=False)
    d = f.d
    # traçado em planta: dentro da parede oeste
    a, b = P(-PAREDE / 2, AT[1] + 270), P(-PAREDE / 2, Q_Y)
    d.path('M%.1f %.1f L%.1f %.1f' % (a[0], a[1], b[0], b[1]), stroke=DEMO, sw=2.4, dash='6 3')
    d.circle(a[0], a[1], 5, fill=DEMO)
    for yy, cor, rot in ((Q_Y, DEMO, 'Q'), (CUBA_Y, K, 'B'), (F_Y, CIANO, 'F')):
        c = P(26, yy)
        d.circle(c[0], c[1], 6.5, fill=BG, stroke=cor, sw=1.6)
        f.t(c[0], c[1] + 2.6, rot, 6.2, K, True, 'middle')
    c = P(-PAREDE - 30, (AT[1] + Q_Y) / 2)
    f.t(c[0], c[1], 'AQ nova · dentro da parede', 6.8, DEMO, True, 'middle', rot=-90)
    c = P(-PAREDE - 30, AT[1] + 420)
    f.t(c[0], c[1], 'tê na coluna quente', 6.4, DEMO, False, 'middle', rot=-90)
    # ---- elevação da P3 (de frente para o oeste; esquerda = box) -------------------
    ex, ey, Ne = 545.0, 800.0, 16.5
    se = MM / Ne

    def E(u, z):
        return (ex + u * se, ey - z * se)
    f.t(ex, 150, 'ELEVAÇÃO DA PAREDE DA BANCADA (P3)', 9.0, INK, True)
    f.t(ex, 162, 'de frente para a parede; box e área técnica à esquerda', 7.4, INK_SOFT)
    a, b = E(-300, FORRO), E(1880, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.0)
    a, b = E(-300, FORRO), E(0, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K12, stroke=K, sw=0.8)
    f.t((a[0] + b[0]) / 2, a[1] + 16, 'AT-B', 7.0, K, True, 'middle')
    c = E(120, 0)
    d.line(c[0], E(0, FORRO)[1], c[0], c[1], CIANO, 2.0)
    f.t(c[0] + 4, E(0, 2380)[1], 'vidro', 6.4, K70)
    a, b = E(120, GABINETE_H), E(1720, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K04, stroke=K45, sw=0.8)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 'gabinete 1600 × 880', 7.0, K70, False, 'middle')
    a, b = E(120, TOPO_BANC), E(1720, GABINETE_H)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.0)
    a, b = E(120, ESP_BASE + ESP_H), E(1720, ESP_BASE)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=CIANO18, stroke=K45, sw=0.8)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 'espelho 1600 × 900', 7.0, K70, False, 'middle')
    uq, ub, uf = AT[1] - Q_Y, AT[1] - CUBA_Y, AT[1] - F_Y
    # cuba de apoio
    a, b = E(ub - 210, TOPO_BANC + 160), E(ub + 210, TOPO_BANC)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BG, stroke=K45, sw=0.7)
    # coluna quente do chuveiro na AT e ramal novo
    c0, c1 = E(-150, 300), E(-150, 2150)
    d.line(c0[0], c0[1], c1[0], c1[1], DEMO, 2.2)
    f.t(c0[0], c0[1] + 12, 'AQ do chuveiro', 6.4, DEMO, True, 'middle')
    t0, t1 = E(-150, Z_COMANDO), E(uq, Z_COMANDO)
    d.path('M%.1f %.1f L%.1f %.1f' % (t0[0], t0[1], t1[0], t1[1]), stroke=DEMO, sw=2.6, dash='7 3')
    d.rect(t0[0] - 5, t0[1] - 5, 10, 10, fill=DEMO)
    f.t(t0[0], t0[1] - 10, 'tê', 6.6, DEMO, True, 'middle')
    rg = E(60, Z_COMANDO)
    d.rect(rg[0] - 5, rg[1] - 6, 10, 12, fill=BG, stroke=DEMO, sw=1.4)
    f.t(rg[0], rg[1] - 10, 'registro', 6.2, DEMO, False, 'middle')
    f0, f1 = E(uf, 250), E(uf, Z_COMANDO)
    d.line(f0[0], f0[1], f1[0], f1[1], CIANO, 2.0)
    f.t(f0[0] + 5, f0[1] - 4, 'AF existente', 6.4, K70)
    for u, cor, rot, z in ((uq, DEMO, 'Q', Z_COMANDO), (ub, K, 'B', Z_BICA), (uf, CIANO, 'F', Z_COMANDO)):
        c = E(u, z)
        d.circle(c[0], c[1], 7, fill=BG, stroke=cor, sw=1.8)
        f.t(c[0], c[1] + 2.6, rot, 6.4, K, True, 'middle')
    f.cota_h(t0[0], t1[0], t1[1] + 22, '%d (ramal na horizontal)' % round(uq + 150), 6.6, DEMO)
    for z, rot in ((TOPO_BANC, '+980 tampo'), (Z_COMANDO, '+1245 comandos'), (ESP_BASE, '+1340 espelho'), (ESP_BASE + ESP_H, '+2240'), (FORRO, '+2500 forro')):
        c = E(1880, z)
        d.line(c[0], c[1], c[0] + 10, c[1], K70, 0.6)
        f.t(c[0] + 13, c[1] + 2.5, rot, 6.4, K70)
    f.cota_h(E(ub, 0)[0], E(uq, 0)[0], E(0, Z_BICA)[1] - 22, '100', 6.2)
    f.cota_h(E(uf, 0)[0], E(ub, 0)[0], E(0, Z_BICA)[1] - 22, '100', 6.2)
    # ---- texto ------------------------------------------------------------------------
    cx = 1030.0
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Item', 0.36, 'start'), ('Dado', 0.64, 'end')], [
        ('Origem', 'coluna de água quente do chuveiro, na AT-B'),
        ('Ramal', '~1,1 m na horizontal, a +1245'),
        ('Tubo', 'CPVC ou PPR 22 mm, a confirmar'),
        ('Isolamento', 'polietileno expandido, em todo o ramal'),
        ('Registro', '1, acessível, logo depois do tê'),
        ('Na pia', 'quente à esquerda de quem usa'),
        ('Reserva de compra', 'até 6 m de tubo e isolamento'),
    ], titulo='RAMAL DE ÁGUA QUENTE')
    f.passos(cx, y + 30, cw, [
        ('Achar a coluna quente.', 'Abrir a face da área técnica só o necessário e identificar a água quente do chuveiro. Confirmar material e diâmetro do tubo existente.', True),
        ('Tê e registro.', 'Tê do mesmo material da rede, com transição certificada se o ramal for de outro material. Registro logo depois do tê.', False),
        ('Rasgo na parede.', 'Rasgo horizontal a +1245, da área técnica até o comando da pia. Tubo com isolamento, sem emenda dentro da parede se possível.', False),
        ('Mistura.', 'Quente e fria chegam cada uma no seu comando. Não ligar as duas redes com um tê simples. Nada de flexível embutido.', True),
        ('Teste antes de fechar.', 'Pressurizar e deixar pelo menos 6 horas com o rasgo aberto. Abrir a água quente e medir quanto tempo leva para chegar.', True),
        ('Fechar e impermeabilizar.', 'Só depois do teste: fechar o rasgo, refazer a impermeabilização na faixa da cuba e revestir.', False),
    ], size=8.0, lh=11.2)
    return f


def be07():
    f = Folha(CAD, 'BE-07', 'Elétrica: pontos e comandos', 'Pontos de coordenação. Circuito, bitola e proteção são do eletricista, depois do levantamento do quadro.', '1:15')
    P, s = f.planta(OX, OY, N)
    d = f.d
    def ponto(x, y, rot, cor=CIANO, dx=12, dy=3, an='start'):
        c = P(x, y)
        d.circle(c[0], c[1], 6.5, fill=cor, stroke=K, sw=1.2)
        d.circle(c[0], c[1], 2, fill=K)
        f.t(c[0] + dx, c[1] + dy, rot, 7.0, K, True, an)
    ponto(VASO_X, 14, 'T20', dx=-60, dy=22)
    ponto(14, BANC[1] + 160, 'T17', dx=12)
    ponto(14, Q_Y + 380, 'L3', AMARELO, dx=12)
    ponto(D1[0], D1[1], 'D1', AMARELO)
    ponto(D2[0], D2[1], 'D2', AMARELO)
    ponto(EX[0], EX[1], 'EX01', BRANCO)
    for i, (rot, yy) in enumerate((('S04', PORTA[0] - 200), ('S03', PORTA[0] - 330))):
        c = P(LARG + PAREDE + 26, yy)
        d.rect(c[0] - 6, c[1] - 6, 12, 12, fill=BG, stroke=K, sw=1.2)
        d.line(c[0] - 3, c[1] + 3, c[0] + 3, c[1] - 3, K, 1.1)
        f.t(c[0] + 12, c[1] + 3, rot, 7.0, K, True)
    f.legenda(OX - 22, 880, [('dot', CIANO, 'Tomada / ponto de força'), ('dot', AMARELO, 'Ponto de luz'), ('dot', BRANCO, 'Exaustor')])
    y = f.tab(CX, 150, CW, [('ID', 0.10, 'start'), ('Ponto', 0.50, 'start'), ('Altura / dado', 0.40, 'end')], [
        ('T20', 'Toalheiro térmico Aiello Unique Solo, acima do vaso (ponto novo)', '127 V; caixa atrás do aparelho, +1170'),
        ('T17', 'Tomada da bancada, na faixa entre tampo e espelho', '+1160; 2P+T'),
        ('D1', 'Luz geral: FAS Halo embutido 7 W, 2700 K', 'no forro; furo de 53 mm'),
        ('D2', 'Luz do box: FAS Tiny embutido 5,8 W, 2700 K, IP', 'no forro; furo de 34 mm'),
        ('L3', 'Perfil linear sobre o espelho (existente)', 'reinstalar; fonte acessível'),
        ('EX01', 'Exaustor no forro', 'posição e duto a levantar'),
        ('S04', 'Comando do banheiro: D1 + D2 e exaustor', 'fora, ao norte da porta; +1100'),
        ('S03', 'Comando do perfil do espelho', 'junto ao S04; +1100'),
    ], titulo='PONTOS')
    f.par(CX, y + 26, CW, [
        ('O T20 é o ponto do toalheiro.', 'Fica na parede do vaso, no eixo dele, atrás do toalheiro (550 × 370 mm, base a +989). '
         'A versão de fio oculto liga direto na caixa, sem plugue: conferir a interface com a peça comprada antes de fechar a parede.'),
        ('Proteção.', 'Todos os circuitos do banheiro com DR de 30 mA e condutor de terra. Nada de emenda solta dentro da parede. '
         'Respeitar os volumes do box: nenhum ponto de força dentro dele.'),
        ('Interruptores do lado da dobradiça.', 'Com a porta abrindo em sentido anti-horário, S03 e S04 ficam do lado da dobradiça, a 880 mm '
         'de parede livre ao norte do vão. Conferir se o alcance fica bom com a folha aberta.'),
        ('Levar a fiação pelo forro.', 'O forro novo a +2500 deixa 120 mm até a laje. As descidas para T17, T20 e comandos são embutidas, '
         'feitas antes da impermeabilização e do revestimento.'),
    ])
    return f


def be08():
    f = Folha(CAD, 'BE-08', 'Forro e iluminação da FAS', 'Forro novo a +2500 com as duas luminárias embutidas do pedido FAS 22804. Detalhes de nicho da folha F02 da FAS.', 'planta de teto 1:15')
    P, s = f.planta(OX, OY, N, objetos=False, box_cor=None, piso=BRANCO, rotulos=False, porta=False)
    d = f.d
    a, b = P(0, BOX_Y), P(LARG, BOX_Y)
    for (x, y, rot, r) in ((D1[0], D1[1], 'D1', 53), (D2[0], D2[1], 'D2', 34)):
        c = P(x, y)
        d.circle(c[0], c[1], 13, fill=AMARELO, stroke=K, sw=1.3)
        d.circle(c[0], c[1], 3, fill=K)
        f.t(c[0] + 18, c[1] + 3, rot, 8.0, K, True)
    c = P(*EX)
    d.rect(c[0] - 13, c[1] - 13, 26, 26, fill=CIANO18, stroke=K, sw=1.0)
    f.t(c[0], c[1] + 3, 'EX01', 6.6, K, True, 'middle')
    c = P(*CH)
    d.circle(c[0], c[1], 16, fill='none', stroke=K45, sw=1.0)
    f.t(c[0], c[1] + 3, 'CH', 6.6, K70, True, 'middle')
    a, b = P(30, BANC[1]), P(30, BANC[3])
    d.line(a[0], a[1], b[0], b[1], AMARELO, 4.0)
    d.line(a[0], a[1], b[0], b[1], K, 0.6)
    f.t(a[0] + 9, (a[1] + b[1]) / 2, 'L3', 7.0, K, True)
    f.cadeia_h(P, [0, D1[0], LARG], D1[1], 0)
    f.cadeia_v(P, [0, D1[1]], D1[0] - 180, 0)
    f.cadeia_h(P, [0, D2[0], LARG], D2[1], 0)
    f.cadeia_v(P, [D2[1], COMP], D2[0] + 200, 0)
    f.legenda(OX - 22, 880, [('dot', AMARELO, 'Luminária embutida FAS'), ('line', AMARELO, 'Perfil do espelho (existente)'), ('fill', CIANO18, 'Exaustor')])
    # detalhes de nicho
    def nicho(x, y, nome, furo, corpo, larg_corpo):
        e = 2.2
        f.t(x, y - 12, nome, 8.4, INK, True)
        d.rect(x, y, 250, 40, fill=K20)
        f.t(x + 242, y + 16, 'LAJE', 6.8, K, True, 'end')
        d.rect(x, y + 40 + 105 * e, 250, 15 * e, fill=K07, stroke=K45, sw=0.6)
        f.t(x + 242, y + 40 + 105 * e + 22, 'forro de gesso, 15 mm', 6.4, K70, False, 'end')
        cx_ = x + 110
        d.rect(cx_ - furo * e / 2, y + 40 + 105 * e, furo * e, 15 * e, fill=BG)
        d.rect(cx_ - larg_corpo * e / 2, y + 40 + (105 - corpo) * e, larg_corpo * e, corpo * e + 15 * e, fill=AMARELO40, stroke=K, sw=0.9)
        f.cota_v(x - 14, y + 40, y + 40 + 105 * e, 'mín. 100', 6.6)
        f.cota_h(cx_ - furo * e / 2, cx_ + furo * e / 2, y + 40 + 120 * e + 20, 'furo %d' % furo, 6.6)
    nicho(CX, 190, 'D1 · HALO 7 W · furo de 53 mm', 53, 60, 50)
    nicho(CX + 320, 190, 'D2 · TINY 5,8 W IP · furo de 34 mm', 34, 64, 32)
    y = f.tab(CX, 560, CW, [('ID', 0.08, 'start'), ('Luminária (pedido FAS 22804)', 0.56, 'start'), ('Qtde', 0.10, 'end'), ('Onde', 0.26, 'end')], [
        ('D1', 'TE.4106 · Halo embutido orientável redondo, LED 7 W, 36°, 2700 K', '1', 'luz geral'),
        ('D2', 'TE.4676 · Tiny embutido, 5,8 W, 36°, 2700 K, bivolt, IP', '1', 'dentro do box'),
    ], titulo='LUMINÁRIAS')
    f.par(CX, y + 26, CW, [
        ('Altura livre no forro.', 'A FAS pede no mínimo 100 mm entre a laje e o forro. Com a laje a +2620 e o forro a +2500 sobram 120 mm, '
         'menos os 15 mm da placa: 105 mm. Não baixar o forro menos que isso; conferir a altura real da laje depois de tirar o forro antigo.'),
        ('Posições.', 'D1 no centro da área livre, entre a bancada e a parede da porta. D2 no box, afastado ~300 mm do eixo do chuveiro. '
         'São as posições do modelo R95 adaptadas às medidas novas: conferir com a folha F01 da FAS (planta), que não está neste pacote.'),
        ('Forro.', 'Gesso resistente à umidade, com tabica no perímetro. O revestimento das paredes termina no forro (+2500). '
         'Furos das luminárias só com a peça em mãos; fonte e conexões com acesso de manutenção.'),
        ('Projeto FAS aguardando aprovação.', 'A folha F02 está carimbada como aguardando aprovação. Confirmar com a FAS antes de furar o forro.'),
    ])
    return f


def be09():
    f = Folha(CAD, 'BE-09', 'Bancada, gabinete e espelho', 'Gabinete existente de 880 mm de altura, bancada nova de 1600 × 400 com saia de 100 por cima, topo a +980, e espelho de 1600 × 900.', 'elevação e corte 1:12,5')
    d = f.d
    Ne = 12.5
    se = MM / Ne
    ex, ey = 80.0, 860.0

    def E(u, z):
        return (ex + u * se, ey - z * se)
    f.t(ex, 150, 'ELEVAÇÃO  ·  de frente para a parede da bancada', 9.0, INK, True)
    a, b = E(0, 2500), E(1880, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.0)
    c = E(120, 0)
    d.line(c[0], a[1], c[0], c[1], CIANO, 2.2)
    f.t(c[0] - 4, E(0, 2420)[1], 'vidro do box', 6.4, K70, False, 'end')
    a, b = E(120, GABINETE_H), E(1720, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K04, stroke=K, sw=0.9)
    for i in range(1, 4):
        xx = a[0] + i * (b[0] - a[0]) / 4
        d.line(xx, a[1], xx, b[1], K45, 0.6)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 'GABINETE EXISTENTE  1600 × 880 × 400', 7.6, K70, True, 'middle')
    a, b = E(120, TOPO_BANC), E(1720, GABINETE_H)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.4)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 3, 'B01  ·  saia de 100', 7.4, K, True, 'middle')
    a, b = E(120, ESP_BASE + ESP_H), E(1720, ESP_BASE)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=CIANO18, stroke=K, sw=0.9)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 'ESPELHO  1600 × 900', 8.0, K70, True, 'middle')
    ub = AT[1] - CUBA_Y
    a, b = E(ub - 210, TOPO_BANC + 160), E(ub + 210, TOPO_BANC)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BG, stroke=K, sw=0.8)
    f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 3, 'cuba', 6.6, K70, False, 'middle')
    for u, rot, z in ((ub + 100, 'Q', Z_COMANDO), (ub, 'B', Z_BICA), (ub - 100, 'F', Z_COMANDO)):
        c = E(u, z)
        d.circle(c[0], c[1], 7, fill=BG, stroke=K, sw=1.3)
        f.t(c[0], c[1] + 2.6, rot, 6.4, K, True, 'middle')
    f.cota_h(E(0, 0)[0], E(120, 0)[0], ey + 24, '120', 6.6)
    f.cota_h(E(120, 0)[0], E(1720, 0)[0], ey + 24, '1600', 6.6)
    f.cota_h(E(1720, 0)[0], E(1880, 0)[0], ey + 24, '160', 6.6)
    xr = E(1880, 0)[0] + 26
    for z0, z1, rot in ((0, GABINETE_H, '880'), (GABINETE_H, TOPO_BANC, '100'), (TOPO_BANC, ESP_BASE, '360'), (ESP_BASE, ESP_BASE + ESP_H, '900'), (ESP_BASE + ESP_H, FORRO, '260')):
        f.cota_v(xr, E(0, z1)[1], E(0, z0)[1], rot, 6.6)
    f.cota_v(xr + 30, E(0, FORRO)[1], E(0, 0)[1], '2500', 7.0)
    # ---- corte ---------------------------------------------------------------------------
    cxx = 720.0

    def C(xw, z):
        return (cxx + xw * se, ey - z * se)
    f.t(cxx - 40, 150, 'CORTE', 9.0, INK, True)
    a, b = C(-100, 2500), C(0, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K20, stroke=K, sw=0.8)
    a, b = C(0, GABINETE_H), C(400, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K04, stroke=K, sw=0.9)
    a, b = C(0, TOPO_BANC), C(400, TOPO_BANC - 20)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.2)
    a, b = C(388, TOPO_BANC), C(400, GABINETE_H)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=1.2)
    a, b = C(0, ESP_BASE + ESP_H), C(8, ESP_BASE)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=CIANO, stroke=K, sw=0.6)
    a, b = C(40, TOPO_BANC + 160), C(360, TOPO_BANC)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BG, stroke=K, sw=0.8)
    f.cota_h(C(0, 0)[0], C(400, 0)[0], ey + 24, '400', 6.6)
    for z, rot in ((GABINETE_H, '+880'), (TOPO_BANC, '+980'), (TOPO_BANC + 160, '+1140 borda da cuba'), (Z_BICA, '+1250 bica'), (ESP_BASE, '+1340'), (ESP_BASE + ESP_H, '+2240')):
        c = C(400, z)
        d.line(c[0] + 4, c[1], c[0] + 16, c[1], K70, 0.6)
        f.t(c[0] + 20, c[1] + 2.5, rot, 6.6, K70)
    # ---- texto ----------------------------------------------------------------------------
    cx = 1010.0
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Item', 0.40, 'start'), ('Medida', 0.60, 'end')], [
        ('Tampo B01', '1600 × 400 mm'),
        ('Saia frontal', '100 mm (de +880 a +980)'),
        ('Topo do tampo', '+980'),
        ('Gabinete', '1600 × 400 × 880 de altura'),
        ('Espelho', '1600 × 900; base a +1340'),
        ('Faixa livre', '360 mm entre tampo e espelho'),
        ('Comandos / bica', '+1245 / +1250'),
        ('Material', 'Corian branco (R95), a confirmar'),
    ], titulo='BANCADA B01')
    f.par(cx, y + 24, cw, [
        ('Altura a conferir no uso.', 'Com o tampo a +980 e uma cuba de apoio de 160 mm, a borda da cuba fica a +1140: é alto. '
         'Vale simular com as peças antes de fabricar; uma cuba de semiencaixe ou de embutir baixa a borda.'),
        ('Saia e apoio.', 'A saia de 100 mm cobre a frente, do topo do gabinete ao topo do tampo. O gabinete não é presumido estrutural: '
         'apoios e reforços do tampo pelo fabricante.'),
        ('Furos.', 'Cuba, válvula e metais só com o gabarito das peças reais. A bancada tem 400 mm de fundo: conferir se a cuba cabe com a bica na parede.'),
        ('Espelho.', 'A base a +1340 mantém 90 mm acima do eixo da bica, como na R95. Se o espelho existente for reaproveitado, conferir a fixação.'),
        ('Parede.', 'Sem revestimento atrás do gabinete e do espelho: só na faixa de 360 mm e acima do espelho. Ver a paginação na BE-17.'),
    ], size=8.0, lh=11.4)
    return f


def be10():
    f = Folha(CAD, 'BE-10', 'Porta P02', 'Vão de 800 × 2150 mm a 880 mm do canto norte, por fora. Abre para fora, em sentido anti-horário.', 'elevação 1:10 · planta 1:15')
    d = f.d
    se = MM / 10.0
    x, y = 110.0, 180.0
    lw, lh = 794 * se, 2135 * se
    d.rect(x - 3 * se, y - 3 * se, 800 * se, 2150 * se, fill='none', stroke=K45, sw=0.8, dash='4 3')
    d.rect(x, y, lw, lh, fill=K04, stroke=K, sw=1.4)
    cy = y + lh - 1550 * se
    d.circle(x + lw / 2, cy, 200 * se, fill=CIANO18, stroke=K, sw=1.1)
    f.t(x + lw / 2, cy + 3, 'visor Ø400', 7.0, K70, False, 'middle')
    d.rect(x + lw - 22, y + lh - 1150 * se, 6, 300 * se, fill=K45)
    for i in (0.12, 0.5, 0.88):
        d.rect(x - 4, y + lh * i - 9, 6, 18, fill=K)
    f.cota_h(x, x + lw, y - 16, 'folha 794', 6.8)
    f.cota_v(x - 30, y, y + lh, 'folha 2135', 6.8)
    f.cota_v(x + lw + 34, y - 3 * se, y - 3 * se + 2150 * se, 'vão 2150', 6.8, lado=1)
    f.t(x, y + lh + 26, 'ELEVAÇÃO  ·  vista da sala, dobradiças à esquerda de quem olha de dentro', 7.6, INK_SOFT)
    # planta de abertura
    P, s = f.planta(440, 215, 15, objetos=False, rotulos=False)
    _cotas_planta(f, P, interno=False)
    c = P(LARG + PAREDE, PORTA[0])
    d.circle(c[0], c[1], 5, fill=DEMO)
    f.t(c[0] + 8, c[1] - 8, 'dobradiças', 6.8, DEMO, True)
    c = P(LARG + PAREDE, PORTA[1])
    f.t(c[0] + 8, c[1] + 12, 'fechadura', 6.8, K70)
    cx = 1050.0
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Item', 0.36, 'start'), ('Medida / acabamento', 0.64, 'end')], [
        ('Vão acabado', '800 × 2150 mm'),
        ('Folha', '794 × 2135 × 40 mm'),
        ('Folgas', '3 em cima e nos lados; 12 embaixo'),
        ('Posição', '880 do canto norte, por fora'),
        ('Abertura', 'para fora, anti-horária'),
        ('Dobradiças', 'no batente norte'),
        ('Visor', 'circular, Ø400, eixo a +1550'),
        ('Puxador', 'externo, 300 mm, aço escovado'),
        ('Tranca', 'interna, botão fixo; sem chave'),
        ('Pintura', 'azul #0D2135 (R95)'),
    ], titulo='P02')
    f.par(cx, y + 24, cw, [
        ('O que muda.', 'A altura do vão passa de 2103 (R95) para 2150 mm e a porta fica 0,33 m mais ao sul do que nas plantas antigas. '
         'A folha da R95 (2088) não serve: a nova tem 2135 mm.'),
        ('Por dentro e por fora.', 'De dentro, empurra-se com a mão direita. De fora, puxa-se com a esquerda. Aberta, a folha encosta ao norte do vão.'),
        ('Verga.', 'Com o vão a 2150, sobram 350 mm de parede até o forro. Conferir a verga existente antes de abrir ou fechar o vão.'),
        ('Piso.', 'Perfil de metal no eixo da folha fechada (BE-03). A folga de 12 mm embaixo é medida sobre o piso pronto.'),
    ], size=8.0, lh=11.4)
    return f


def be11():
    f = Folha(CAD, 'BE-11', 'Piso: porcelanato Confete 100 × 100', 'Malha do modelo R95 recortada nas medidas novas. Junta de 2 mm entre placas e 3 mm de folga no perímetro.', '1:15')
    P, s = f.planta(OX, OY, N, objetos=False, box_cor=None, piso=BRANCO, rotulos=False)
    d = f.d
    gx, gy = 683.0, [211.0, 1211.0, 2211.0]
    pecas = []
    zonas = [('S', 0, 0, LARG, BOX_Y - 3), ('B', 0, BOX_Y + 3, LARG, COMP), ('V', LARG, PORTA[0], LARG + PAREDE, PORTA[1])]
    for z, x0, y0, x1, y1 in zonas:
        xs = [x0] + [g for g in (gx,) if x0 < g < x1] + [x1]
        ys = [y0] + [g for g in gy if y0 < g < y1] + [y1]
        k = 0
        for i in range(len(xs) - 1):
            for j in range(len(ys) - 1):
                a, b, c_, e_ = xs[i], ys[j], xs[i + 1], ys[j + 1]
                if z == 'B' and c_ <= AT[2] + 1 and b >= AT[1] - 1:
                    continue
                k += 1
                rx0 = a + (3 if a in (x0,) else 1)
                ry0 = b + (3 if b in (y0,) else 1)
                rx1 = c_ - (3 if c_ in (x1,) else 1)
                ry1 = e_ - (3 if e_ in (y1,) else 1)
                pecas.append(('%s%d' % (z, k), rx0, ry0, rx1, ry1, z))
    for (pid, a, b, c_, e_, z) in pecas:
        p0, p1 = P(a, b), P(c_, e_)
        d.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=CIANO18 if z == 'B' else BRANCO, stroke=K, sw=0.9)
        cxm, cym = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        if p1[0] - p0[0] > 40:
            f.t(cxm, cym, pid, 9.0, K, True, 'middle')
            f.t(cxm, cym + 11, '%d × %d' % (round(c_ - a), round(e_ - b)), 6.6, K70, False, 'middle')
        else:
            f.t(cxm + 3, cym, '%s  %d × %d' % (pid, round(c_ - a), round(e_ - b)), 6.0, K, True, 'middle', rot=-90)
    a, b = P(*AT[:2]), P(*AT[2:])
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K20, stroke=K, sw=0.8)
    f.ralos(P, s, rot=False)
    a, b = P(0, BOX_Y), P(LARG, BOX_Y)
    d.line(a[0], a[1], b[0], b[1], CIANO, 2.6)
    c = P(LARG + PAREDE / 2, (PORTA[0] + PORTA[1]) / 2)
    d.line(c[0], P(0, PORTA[0])[1], c[0], P(0, PORTA[1])[1], DEMO, 2.4)
    f.t(c[0] + 14, c[1], 'perfil de metal', 6.8, DEMO, True)
    f.cadeia_h(P, [0, gx, LARG], -PAREDE, -30)
    f.cadeia_v(P, [0] + gy + [COMP], -PAREDE, -30)
    f.legenda(OX - 22, 880, [('fill', BRANCO, 'Piso seco (S)'), ('fill', CIANO18, 'Box (B): subdividir nas linhas de caimento'), ('line', DEMO, 'Perfil de metal')])
    area = sum((c_ - a) * (e_ - b) for (_, a, b, c_, e_, _) in pecas) / 1e6
    y = f.tab(CX, 150, CW, [('Peça', 0.12, 'start'), ('Largura', 0.18, 'end'), ('Comprimento', 0.22, 'end'), ('Zona', 0.48, 'end')],
              [(pid, '%d' % round(c_ - a), '%d' % round(e_ - b), {'S': 'piso seco', 'B': 'box: recortar no caimento', 'V': 'vão da porta, até o perfil'}[z])
               for (pid, a, b, c_, e_, z) in pecas], titulo='PEÇAS — MEDIDAS DO ENVELOPE (mm)', alt=15.5)
    f.par(CX, y + 22, CW, [
        ('Quantidade.', '%s m² líquidos em %d peças. Cabem em 5 placas de 100 × 100; comprar 6 (3 caixas de 2), uma de reserva. '
         'Refazer o plano de corte com as medidas tiradas depois da demolição.' % (br(area), len(pecas))),
        ('Box.', 'O porcelanato do box é cortado nas quebras de plano do caimento (BE-03 e BE-05). Não empenar placa de 1 m para fazer caimento. '
         'Recortes de ralo e de vaso só com gabarito.'),
        ('Juntas.', '2 mm entre placas, 3 mm no perímetro com junta elástica. Rejunte acrílico claro, próximo da cor do Confete, próprio para área molhada.'),
        ('Antiderrapante.', 'Conferir na ficha do lote se o acabamento do Confete atende piso de box. Se não atender, usar no box a versão antiderrapante da mesma linha.'),
    ])
    return f, pecas, area


FOLHAS = [be01, be02, be03, be04, be05, be06, be07, be08, be09, be10]
