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
    return [('Largura da parede', '%d mm' % par.larg), ('Bleu Nuit 155 × 155', str(par.n_bleu)), ('· inteiras', str(par.inteiras)),
            ('· cortadas', str(par.n_bleu - par.inteiras)), ('Nuage 75 × 155 (%d pares)' % len(par.acentos), str(par.n_nuage)), ('Área revestida', '%s m²' % br(par.area)),
            ('Colunas', '%d' % len(par.cols)), ('Fiadas', '%d (15 inteiras + topo de 145)' % len(par.rows))]


def be12():
    f = Folha(CAD, 'BE-12', 'Paginação: todas as paredes abertas', 'As seis faces na ordem em que se dá a volta no banheiro. Bleu Nuit 155 × 155 com pares Nuage 75 × 155, junta de 2 mm, 16 fiadas até o forro.', '1:30')
    x, N = 70.0, 30
    for par in PAREDES:
        P, s = f.elevacao(x, 560.0, N, par, 'linhas', indices=False)
        f.t(x, 560.0 - FORRO * s - 24, par.id, 11.0, DEMO, True)
        f.t(x, 560.0 - FORRO * s - 10, '%d mm' % par.larg, 7.0, K70)
        x += par.larg * s + 26
    f.cota_v(52, 560.0 - FORRO * MM / N, 560.0, '2500', 7.0)
    f.tab(70, 640, 800, [('Parede', 0.07, 'start'), ('Superfície', 0.33, 'start'), ('Largura', 0.09, 'end'), ('Bleu', 0.08, 'end'),
                         ('Inteiras', 0.10, 'end'), ('Cortadas', 0.10, 'end'), ('Nuage', 0.10, 'end'), ('Área m²', 0.13, 'end')],
          [(p.id, p.nome, '%d' % p.larg, p.n_bleu, p.inteiras, p.n_bleu - p.inteiras, p.n_nuage, br(p.area)) for p in PAREDES]
          + [('Total', '', '', sum(p.n_bleu for p in PAREDES), sum(p.inteiras for p in PAREDES),
              sum(p.n_bleu - p.inteiras for p in PAREDES), sum(p.n_nuage for p in PAREDES), br(sum(p.area for p in PAREDES)))], titulo='RESUMO POR PAREDE')
    f.par(910, 648, W - MARGIN - 910, [
        ('Como ler.', 'Peças em branco, só com as juntas. O número em magenta dentro de uma peça é a medida do corte, em mm. '
         'As áreas em cinza não levam revestimento: porta, nicho, gabinete e espelho.'),
        ('Regras da malha.', 'Fiadas inteiras a partir do piso pronto; a 16ª fiada é cortada em 145 mm junto ao forro. '
         'Cada parede nasce do seu eixo, com o mesmo corte nas duas pontas; a P3 é deslocada (59 mm no box, 92 mm na parede do vaso) para não deixar tira menor que 1/3 de peça ao lado do gabinete e do espelho. As juntas horizontais dão a volta no banheiro na mesma altura.'),
        ('Acentos Nuage: sempre em par.', 'Duas peças Nuage 75 × 155 lado a lado ocupam exatamente uma célula de 155 (75 + junta de 5 + 75). '
         'Assim nenhuma Bleu Nuit é cortada no meio da parede e todas as juntas verticais continuam alinhadas. No R95 cada Nuage vinha com uma Bleu cortada em 78 mm: isso saiu.'),
        ('Onde ficam os pares (amarelo, "N").', 'Cerca de 1 par a cada 10 peças, só em peças inteiras: no máximo um por fiada em cada parede, nenhum encostado em outro (nem na diagonal) '
         'e a mesma coluna só se repete depois de 4 fiadas. Não vão na fiada cortada do topo, nos cortes, no nicho nem na bancada. As posições podem mudar com o cliente: a quantidade quase não muda.'),
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
    f.legenda(x1, PISO_Y + 62, [('fill', BRANCO, 'Bleu Nuit 155 × 155'), ('fill', NUAGE_COR, 'N = par Nuage 75 × 155 (75 + 5 + 75 = 155)')])
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
        ('Verga: guarnição de 50 mm.', 'A porta tem 2150 de altura e a junta da 14ª fiada fica a +2196: sobre o vão sobram 46 mm, menos que 1/3 da peça. '
         'Solução adotada: a guarnição da porta, por dentro, tem 50 mm e cobre a faixa até a junta. As 4 peças sobre o vão e as 2 em L dos batentes são cortadas e escondidas pela guarnição. '
         'Pedir a guarnição de 50 mm junto com a porta P02.'),
        ('Batentes.', 'Os cortes de 67 e 73 mm encostam no vão; nas fiadas 14 a 16 as peças das duas colunas do batente são inteiras ou em L.')])


def be15():
    return _parede('BE-15', 'P1', 15, notas=[
        ('Nicho de parede a parede.', 'Faixa de 1170 × 400, base a +1100, da parede da porta até a face da área técnica: não é mais um retângulo fechado. '
         'A parede fica dividida em duas partes, abaixo e acima do nicho. Fundo, base, teto e as duas pontas do nicho são revestidos; a base tem caimento para dentro do box.'),
        ('Fiadas no nicho.', 'Base a +1100 (cliente, 15/11): fica 1 mm acima da junta da 7ª fiada; esse 1 mm some no assentamento da base do nicho e a 7ª fiada fica inteira. '
         'O topo a +1500 corta a 10ª fiada: 87 mm dentro do nicho e 68 mm acima dele.'),
        ('Fundo do nicho.', 'Altura de 400 mantida (cliente, 15/11): duas fiadas inteiras e, no alto, a tira de 87 mm, que fica sob o teto do nicho e quase não aparece.'),
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


def bancada_pecas():
    """Peças do tampo, da saia e da lateral norte, alinhadas às juntas da P3."""
    u0, u1 = TAMPO_U
    u = P3_E0 + JUNTA                                  # início da 2ª coluna da P3
    while u + PECA < u0:
        u += MOD
    cols = [(u0, u + PECA)]                            # primeiro corte, até a junta da P3
    u += MOD
    while u + PECA <= u1:
        cols.append((u, u + PECA))
        u += MOD
    if u1 - u > 1:
        cols.append((u, u1))
    fil = [(0.0, PECA), (MOD, MOD + PECA), (2 * MOD, BANC[2])]   # profundidade, a partir da frente
    tampo = [(c, f) for f in fil for c in cols]
    saia = [(c, (0.0, SAIA)) for c in cols]
    lateral = [(f, (0.0, SAIA)) for f in fil]
    return cols, fil, tampo, saia, lateral


def _mm(a):
    return round(a[1] - a[0])


def bancada_resumo():
    cols, fil, tampo, saia, lateral = bancada_pecas()
    inteiras = sum(1 for c, f in tampo if _mm(c) == PECA and _mm(f) == PECA)
    n = len(tampo) + len(saia) + len(lateral)
    area = (TAMPO_U[1] - TAMPO_U[0]) * (BANC[2] + SAIA) / 1e6 + BANC[2] * SAIA / 1e6
    return n, inteiras, area


def be19():
    f = Folha(CAD, 'BE-19', 'Paginação · bancada revestida B01', 'Tampo, saia e lateral norte em Bleu Nuit 155 × 155, com as juntas alinhadas às da parede da bancada (P3).', '1:8')
    cols, fil, tampo, saia, lateral = bancada_pecas()
    N = 8.0
    s = MM / N
    d = f.d
    u0 = TAMPO_U[0]
    ox, oy = 110.0, 400.0          # canto da frente do tampo, lado do box

    def T(u, p):                   # planta do tampo: u ao longo da parede, p a partir da frente
        return (ox + (u - u0) * s, oy - p * s)
    # parede ao fundo
    a, b = T(u0 - 120, BANC[2] + 60), T(TAMPO_U[1] + 160, BANC[2])
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=K20, stroke=K, sw=0.8)
    f.t((a[0] + b[0]) / 2, a[1] - 6, 'PAREDE P3 (oeste) · juntas da parede continuam no tampo', 7.0, K70, False, 'middle')
    n = 0
    for (c, fl) in tampo:
        n += 1
        a, b = T(c[0], fl[1]), T(c[1], fl[0])
        cheia = _mm(c) == PECA and _mm(fl) == PECA
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=0.7)
        if not cheia:
            f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 2.5, '%d×%d' % (_mm(c), _mm(fl)), 6.0, DEMO, False, 'middle')
    # cuba de apoio e furo da válvula
    uc = AT[1] - CUBA_Y
    c = T(uc, BANC[2] - 200)
    d.circle(c[0], c[1], 180 * s, fill='none', stroke=K45, sw=0.8)
    d.circle(c[0], c[1], 20 * s, fill=K, stroke=K, sw=0.6)
    f.t(T(TAMPO_U[1], 0)[0], oy + 52, 'círculo: cuba de apoio (Ø ~360, modelo a definir); ponto: válvula, no centro de uma peça', 6.8, K70, False, 'end')
    f.cota_h(T(u0, 0)[0], T(TAMPO_U[1], 0)[0], oy + 22, '1600', 7.0)
    f.cota_v(T(u0, 0)[0] - 22, T(u0, BANC[2])[1], oy, '400', 7.0)
    xs = [cc[0] for cc in cols] + [cols[-1][1]]
    for a_, b_ in zip(xs, xs[1:]):
        f.t((T(a_, 0)[0] + T(b_, 0)[0]) / 2, oy + 36, '%d' % round(b_ - a_), 5.8, K70, False, 'middle')
    f.t(ox, oy - BANC[2] * s - 62, 'A · TAMPO EM PLANTA', 8.4, INK, True)
    f.t(T(u0, 0)[0], oy + 52, 'frente (lado de quem usa)', 7.0, INK_SOFT)
    f.t(T(u0, 0)[0], T(u0, 0)[1] - BANC[2] * s - 16, 'box', 7.0, INK_SOFT)
    # saia em elevação
    ey = 570.0
    f.t(ox, ey - SAIA * s - 22, 'B · SAIA FRONTAL EM ELEVAÇÃO (+880 a +980)', 8.4, INK, True)
    for (c, z) in saia:
        a, b = (ox + (c[0] - u0) * s, ey - z[1] * s), (ox + (c[1] - u0) * s, ey)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=BRANCO, stroke=K, sw=0.7)
        f.t((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 2.5, '%d×%d' % (_mm(c), _mm(z)), 6.0, DEMO, False, 'middle')
    d.line(ox, ey - SAIA * s, ox + (TAMPO_U[1] - u0) * s, ey - SAIA * s, K, 2.4)
    f.t(ox + (TAMPO_U[1] - u0) * s + 8, ey - SAIA * s + 3, 'perfil de canto', 6.8, K70)
    f.cota_v(ox - 22, ey - SAIA * s, ey, '100', 7.0)
    # lateral norte
    lx, ey2 = ox, ey + 95
    f.t(lx, ey2 - SAIA * s - 22, 'C · LATERAL NORTE (frente à esquerda)', 8.4, INK, True)
    x = lx
    for (fl, z) in lateral:
        w_ = _mm(fl) * s
        d.rect(x, ey2 - z[1] * s, w_, z[1] * s, fill=BRANCO, stroke=K, sw=0.7)
        f.t(x + w_ / 2, ey2 - z[1] * s / 2 + 2.5, '%d×%d' % (_mm(fl), _mm(z)), 6.0, DEMO, False, 'middle')
        x += w_ + JUNTA * s
    f.t(x + 14, ey2 - 12, 'fica à vista: 160 mm livres até a parede do vaso', 7.0, INK_SOFT)
    # corte
    cy0, cx0 = 880.0, 110.0
    f.t(cx0, cy0 - 150, 'D · CORTE NA FRENTE DA BANCADA (1:1,1)', 8.4, INK, True)
    k = 0.9
    def C(xw, z):
        return (cx0 + xw * k, cy0 - (z - 850) * k)
    d.rect(*C(0, 880), 400 * k, 30 * k, fill=K04, stroke=K45, sw=0.6)
    d.rect(C(0, 966)[0], C(0, 966)[1], 400 * k, 22 * k, fill=K12, stroke=K, sw=0.9)
    d.rect(C(0, 980)[0], C(0, 980)[1], 400 * k, 9 * k, fill=CIANO18, stroke=K, sw=0.9)
    d.rect(C(400, 980)[0], C(400, 980)[1], 9 * k, 100 * k, fill=CIANO18, stroke=K, sw=0.9)
    d.line(C(400, 980)[0], C(400, 980)[1], C(409, 980)[0], C(409, 980)[1], K, 2.6)
    for z, rot in ((980, '+980 topo acabado'), (966, '+966 topo da base'), (880, '+880 topo do gabinete')):
        c = C(430, z)
        d.line(c[0] - 14, c[1], c[0] - 2, c[1], K70, 0.6)
        f.t(c[0], c[1] + 2.5, rot, 6.6, K70)
    f.t(C(0, 960)[0] + 4, C(0, 960)[1] + 9, 'base rígida', 6.6, K70)
    # texto
    n_, inteiras, area = bancada_resumo()
    cx = 980.0
    cw = W - MARGIN - cx
    y = f.tab(cx, 150, cw, [('Parte', 0.36, 'start'), ('Peças', 0.20, 'end'), ('Medida', 0.44, 'end')], [
        ('Tampo', len(tampo), '1600 × 400'),
        ('Saia frontal', len(saia), '1600 × 100'),
        ('Lateral norte', len(lateral), '400 × 100'),
        ('Total', n_, '%s m² · %d inteiras' % (br(area), inteiras)),
    ], titulo='PEÇAS DA BANCADA', alt=15.5)
    f.par(cx, y + 26, cw, [
        ('Base.', 'O tampo existente serve de base se for pedra ou cimentício e estiver firme, sem trinca nem flexão. Se for MDF ou madeira, '
         'trocar por placa cimentícia de 12 mm colada e parafusada no gabinete. O topo da base fica a +966: azulejo e argamassa somam 14 mm.'),
        ('Juntas.', 'As colunas do tampo continuam as juntas da parede P3, a mesma malha da BE-17. Na profundidade, duas fiadas inteiras na frente e o corte de 86 mm junto à parede, '
         'escondido pela primeira fiada da parede.'),
        ('Aresta.', 'Perfil metálico de canto (alumínio anodizado ou inox, 10 mm) na aresta frontal e na aresta da lateral. Nada de peça com borda crua.'),
        ('Rejunte do tampo.', 'Epóxi, não acrílico: o tampo recebe água parada, sabão e creme. Nas paredes segue o acrílico Quartzolit, com os 5 dias de espera.'),
        ('Cuba e válvula.', 'A cuba de apoio fica no eixo do tampo (u 920): o furo da válvula cai no centro de uma peça. Furar com serra-copo diamantada, depois do assentamento.'),
        ('Conferir com o fabricante.', 'Bleu Nuit é revestimento de parede. Confirmar que aceita uso em tampo de bancada; se não, só a saia e a lateral levam azulejo.'),
    ], size=7.8, lh=11.0, gap=6.0)
    return f


FOLHAS = [be12, be13, be14, be15, be16, be17, be18, be19]
