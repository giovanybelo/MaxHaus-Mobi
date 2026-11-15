# -*- coding: utf-8 -*-
"""Caderno EXECUTIVO do banheiro — paginação das paredes (BE-12 a BE-17) e sequência (BE-18)."""
import collections
import math
from lib import *      # noqa

CAD = 'CADERNO EXECUTIVO'
PISO_Y = 770.0


def cortes(par):
    c = collections.Counter()
    for (n, fi, ci, frags, cheia) in par.pecas:
        if cheia:
            continue
        for (u0, u1, z0, z1) in frags:
            c[(round(u1 - u0), round(z1 - z0))] += 1
    return sorted(c.items(), key=lambda kv: -kv[1])


def resumo(par):
    n = len(par.pecas)
    return [('Largura da parede', '%d mm' % par.larg), ('Peças', str(n)), ('Inteiras', str(par.inteiras)),
            ('Cortadas', str(n - par.inteiras)), ('Área revestida', '%s m²' % br(par.area)),
            ('Colunas', '%d' % len(par.cols)), ('Fiadas', '%d (15 inteiras + topo de 145)' % len(par.rows))]


def be12():
    f = Folha(CAD, 'BE-12', 'Paginação: todas as paredes abertas', 'As seis faces na ordem em que se dá a volta no banheiro. Bleu Nuit 155 × 155, junta de 2 mm, 16 fiadas até o forro.', '1:30')
    x, N = 70.0, 30
    for par in PAREDES:
        P, s = f.elevacao(x, 560.0, N, par, 'linhas', indices=False)
        f.t(x, 560.0 - FORRO * s - 24, par.id, 11.0, DEMO, True)
        f.t(x, 560.0 - FORRO * s - 10, '%d mm' % par.larg, 7.0, K70)
        x += par.larg * s + 26
    f.cota_v(52, 560.0 - FORRO * MM / N, 560.0, '2500', 7.0)
    f.tab(70, 640, 800, [('Parede', 0.07, 'start'), ('Superfície', 0.37, 'start'), ('Largura', 0.11, 'end'), ('Peças', 0.10, 'end'),
                         ('Inteiras', 0.11, 'end'), ('Cortadas', 0.11, 'end'), ('Área m²', 0.13, 'end')],
          [(p.id, p.nome, '%d' % p.larg, len(p.pecas), p.inteiras, len(p.pecas) - p.inteiras, br(p.area)) for p in PAREDES]
          + [('Total', '', '', sum(len(p.pecas) for p in PAREDES), sum(p.inteiras for p in PAREDES),
              sum(len(p.pecas) - p.inteiras for p in PAREDES), br(sum(p.area for p in PAREDES)))], titulo='RESUMO POR PAREDE')
    f.par(910, 648, W - MARGIN - 910, [
        ('Como ler.', 'Peças em branco, só com as juntas. O número em magenta dentro de uma peça é a medida do corte, em mm. '
         'As áreas em cinza não levam revestimento: porta, nicho, gabinete e espelho.'),
        ('Regras da malha.', 'Fiadas inteiras a partir do piso pronto; a 16ª fiada é cortada em 145 mm junto ao forro. '
         'Cada parede nasce do seu eixo, com o mesmo corte nas duas pontas; a P3 é deslocada (59 mm no box, 92 mm na parede do vaso) para não deixar tira menor que 1/3 de peça ao lado do gabinete e do espelho. As juntas horizontais dão a volta no banheiro na mesma altura.'),
        ('Acentos Nuage.', 'As peças Nuage 75 × 155 do modelo R95 não estão marcadas: as paredes mudaram de medida e as posições precisam ser '
         'transportadas para esta malha. Marcar com o cliente antes de assentar.'),
    ], size=8.0, lh=11.4)
    return f


def _parede(cod, pid, N, extras=(), notas=()):
    par = PAR[pid]
    f = Folha(CAD, cod, 'Paginação · %s · %s' % (par.id, par.nome), 'À esquerda, as peças em branco com a medida dos cortes. À direita, a versão simplificada: só o número de cada peça.', '1:%d' % N)
    s = MM / N
    wl = par.larg * s
    x1 = 90.0
    x2 = x1 + wl + 70
    top = PISO_Y - FORRO * s
    for x, modo, tit in ((x1, 'linhas', 'A · JUNTAS E CORTES'), (x2, 'numeros', 'B · SIMPLIFICADA: NÚMERO DAS PEÇAS')):
        P, _ = f.elevacao(x, PISO_Y, N, par, modo)
        f.t(x, top - 30, tit, 8.4, INK, True, ls=0.6)
        f.cota_h(x, x + wl, top - 10, '%d' % par.larg, 7.0)
    f.cota_v(x1 - 26, top, PISO_Y, '2500', 7.0)
    f.t(x1, PISO_Y + 30, par.vista, 7.6, INK_SOFT)
    f.t(x1, PISO_Y + 44, 'Números da versão B: da fiada de baixo para cima, da esquerda para a direita. C = coluna, F = fiada.', 7.6, INK_SOFT)
    cx = max(x2 + wl + 60, 900.0)
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Dado', 0.50, 'start'), ('Valor', 0.50, 'end')], resumo(par), titulo='RESUMO', alt=15.5)
    ct = cortes(par)[:9]
    y = f.tab(cx, y + 28, cw, [('Corte (L × A, mm)', 0.60, 'start'), ('Qtde', 0.40, 'end')],
              [('%d × %d' % k, v) for k, v in ct], titulo='PEÇAS CORTADAS', alt=15.5)
    cols = par.cols
    ini = ' · '.join('%d' % round(c[0]) for c in cols)
    f.par(cx, y + 24, cw, [('Início de cada coluna, a partir da esquerda (mm).', ini)] + list(notas), size=7.8, lh=11.0, gap=6.0)
    return f


def be13():
    return _parede('BE-13', 'P5', 15, notas=[
        ('Vaso e toalheiro.', 'Eixo do vaso a 980 mm da parede da bancada. O ponto T20 do toalheiro fica nesse eixo, a +1170: furar no centro de uma peça ou na junta.')])


def be14():
    return _parede('BE-14', 'P4', 20, notas=[
        ('Porta.', 'Vão de 800 × 2150 a 780 mm da parede do vaso, por dentro. A guarnição cobre o corte nos batentes.'),
        ('Verga: atenção à tira de 46 mm.', 'A porta termina a +2150 e a junta da 14ª fiada fica a +2196: sobre o vão sobra uma tira de 46 mm: 4 peças, mais as duas em L dos batentes. '
         'Tira com menos de 1/3 da peça não se assenta. Saída preferida: guarnição da porta com 50 mm, cobrindo até a junta. '
         'Sem guarnição: sobre o vão, trocar a tira e a 15ª fiada por duas fiadas iguais de 100 mm. Decidir com o fornecedor da porta antes de assentar a P4.'),
        ('Batentes.', 'Os cortes de 67 e 73 mm encostam no vão; nas fiadas 14 a 16 as peças das duas colunas do batente são inteiras ou em L.')])


def be15():
    return _parede('BE-15', 'P1', 15, notas=[
        ('Nicho de parede a parede.', 'Faixa de 1170 × 400, base a +1100, da parede da porta até a face da área técnica: não é mais um retângulo fechado. '
         'A parede fica dividida em duas partes, abaixo e acima do nicho. Fundo, base, teto e as duas pontas do nicho são revestidos; a base tem caimento para dentro do box.'),
        ('Fiadas no nicho.', 'A base a +1100 cai 1 mm acima da junta da 7ª fiada: ajustar a base para +1099 e a fiada fica inteira. O topo a +1500 corta a 10ª fiada: sobram 68 mm acima do nicho.'),
        ('Recomendação de paginação.', 'Nicho com 314 mm (2 fiadas) ou 471 mm (3 fiadas) de altura fecha na junta em cima e embaixo, e o fundo leva só peças inteiras. '
         'Com 400 mm, o fundo tem 2 fiadas inteiras e uma tira de 87 mm. Decisão do cliente.'),
        ('Largura.', 'A parede tem 1170 mm porque a área técnica ocupa 250 mm do fundo do box.')])


def be16():
    f = Folha(CAD, 'BE-16', 'Paginação · P2 e P6 · faces da área técnica', 'À esquerda, peças em branco com a medida dos cortes. À direita, a versão simplificada: só o número de cada peça.', '1:15')
    N = 15
    s = MM / N
    top = PISO_Y - FORRO * s
    x = 90.0
    for pid in ('P2', 'P6'):
        par = PAR[pid]
        for modo, tit in (('linhas', 'A'), ('numeros', 'B')):
            f.elevacao(x, PISO_Y, N, par, modo)
            f.t(x, top - 30, '%s · %s' % (pid, tit), 8.8, INK, True)
            f.cota_h(x, x + par.larg * s, top - 10, '%d' % par.larg, 7.0)
            x += par.larg * s + 60
        x += 30
    f.cota_v(64, top, PISO_Y, '2500', 7.0)
    f.t(90, PISO_Y + 30, 'P2: de frente para o oeste, esquerda = fundo do box.   P6: de frente para o sul, esquerda = quina externa.', 7.6, INK_SOFT)
    cx = 880.0
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Dado', 0.40, 'start'), ('P2', 0.30, 'end'), ('P6', 0.30, 'end')],
              [(a[0], a[1], b[1]) for a, b in zip(resumo(PAR['P2']), resumo(PAR['P6']))][:5], titulo='RESUMO', alt=15.5)
    f.par(cx, y + 24, cw, [
        ('P2, a face do chuveiro.', 'Parede inteira dentro do box: impermeabilização até o forro antes de revestir. Registros e chuveiro no centro de uma peça ou exatamente na junta.'),
        ('P6, o retorno.', 'Face de 250 mm. Uma peça inteira encostada na quina externa, com perfil de canto, e o corte de 91 mm no canto interno.'),
        ('Trecho de 120 mm.', 'Entre o retorno e o vidro do box sobram 120 mm da parede da bancada. Esse trecho está na folha da P3 (BE-17), nas colunas da esquerda.'),
        ('Acesso à área técnica.', 'Prever tampa de inspeção na face P2, no tamanho de peças inteiras, para o registro novo da água quente (BE-06).'),
    ], size=8.0, lh=11.4)
    return f


def be17():
    return _parede('BE-17', 'P3', 20, notas=[
        ('Onde não vai revestimento.', 'Atrás do gabinete e da bancada (do piso a +980) e atrás do espelho (de +1340 a +2240), no trecho de 1600 mm. '
         'Revestir a faixa de 360 mm entre o tampo e o espelho e a faixa acima do espelho.'),
        ('Pontos.', 'Comandos Q e F a +1245, bica a +1250, tomada T17 a +1160: marcar sobre a malha antes de assentar.'),
        ('Pontas.', 'As duas pontas são revestidas do piso ao forro: 120 mm junto ao box e 160 mm junto à parede do vaso.')])


def be18():
    f = Folha(CAD, 'BE-18', 'Sequência de execução', 'A ordem dos serviços e os pontos em que a obra para até alguém conferir. Em amarelo, as liberações.', 'sem escala')
    cw = (W - 2 * MARGIN - 60) / 2.0
    a = [
        ('Proteção e registros.', 'Fechar água, proteger o piso de fora e os ralos. Fotografar tudo.', False),
        ('Desmontagem.', 'Vaso, gabinete, vidro do box e ferragens saem inteiros e etiquetados (BE-02).', False),
        ('Demolição.', 'Forro, revestimento das paredes, piso e base. Não tocar na área técnica nem na laje.', False),
        ('Levantamento de obra.', 'Medir o banheiro no osso, o esgoto do vaso, os dois ralos e a coluna de água quente. Corrigir as folhas se as medidas mudarem.', True),
        ('Água quente da pia.', 'Tê na coluna do chuveiro, registro, ramal a +1245 com isolamento. Teste de pressão com o rasgo aberto (BE-06).', True),
        ('Esgoto e ralos.', 'Corpo do ralo linear R1, ajuste do R2 e do ponto do vaso para o nível novo (BE-05).', False),
        ('Elétrica embutida.', 'Descidas para T17, T20 e comandos; esperas no forro para D1, D2, L3 e exaustor (BE-07).', False),
        ('Regularização e caimentos.', 'Contrapiso com os níveis da BE-03: box a -10 e -25, piso seco com 0,5% para o R2.', True),
        ('Impermeabilização.', 'Reforços, membrana e teste de estanqueidade de 72 horas, com registro (BE-04).', True),
    ]
    b = [
        ('Revestimento das paredes.', 'Bleu Nuit conforme BE-12 a BE-17, de baixo para cima, a partir do eixo de cada parede. Conferir calibre e tonalidade do lote antes.', False),
        ('Piso Confete.', 'Assentar conforme BE-11, com os cortes do box nas linhas de caimento. Perfil de metal no vão da porta.', False),
        ('Rejunte.', 'Rejunte acrílico Quartzolit nas juntas de 2 mm. Depois de rejuntar, esperar 5 dias antes de molhar ou liberar o uso, '
         'conforme o fabricante.', True),
        ('Forro.', 'Gesso resistente à umidade a +2500, com os furos de 53 e 34 mm das luminárias FAS (BE-08).', False),
        ('Pintura do forro.', 'Antes de instalar luminárias, vidro e louças.', False),
        ('Bancada e gabinete.', 'Gabinete no lugar, tampo B01 com saia, cuba e metais (BE-09). Espelho por último.', False),
        ('Vaso.', 'Anel de vedação novo, bacia aparafusada, engate novo. Testar descarga (BE-05).', False),
        ('Box, porta e elétrica.', 'Vidro do box, porta P02 (BE-10), luminárias, toalheiro, tomadas e exaustor.', False),
        ('Entrega.', 'Teste de todos os pontos de água, quente e fria, dos ralos, das luzes e do toalheiro. Só então liberar o uso.', True),
    ]
    f.passos(MARGIN, 160, cw, a, size=9.0, lh=13.0)
    d = f.d
    y = 150
    # segunda coluna, numerada em sequência
    x = MARGIN + cw + 60
    for i, (tit, txt, portao) in enumerate(b, len(a) + 1):
        yy = y + 10
        d.circle(x + 8, yy - 3, 8, fill=AMARELO if portao else BG, stroke=K, sw=1.0)
        f.t(x + 8, yy, str(i), 7.0, K, True, 'middle')
        f.t(x + 24, yy, tit, 9.0, INK, True)
        yy += 13
        for ln in quebra(txt, cw - 24, 9.0):
            f.t(x + 24, yy, ln, 9.0, INK_SOFT)
            yy += 13
        y = yy - 5
    f.legenda(MARGIN, 890, [('dot', AMARELO, 'Liberação: o serviço seguinte só começa depois de conferido'), ('dot', BG, 'Serviço')])
    return f


FOLHAS = [be12, be13, be14, be15, be16, be17, be18]
