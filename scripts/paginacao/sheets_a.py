# -*- coding: utf-8 -*-
from lib import *
import engine as E
import calc as C
from draw import *

TOTAL = 16
A, B = C.OPTS['A'], C.OPTS['B']
TA, TB = C.total(A), C.total(B)

INDICE = [
    ('01', 'Capa, índice e premissas'),
    ('02', 'Análise dos cinco arquivos recebidos: erros e riscos'),
    ('03', 'Critério de paginação e quadro antes × depois'),
    ('04', 'Planta do banheiro e nomenclatura das paredes'),
    ('05', 'Opção A · 15,5 × 15,5 · planificação das quatro paredes'),
    ('06', 'Opção A · elevações Norte e Sul'),
    ('07', 'Opção A · elevações Leste e Oeste'),
    ('08', 'Opção B · 7,5 × 15,5 · planificação das quatro paredes'),
    ('09', 'Opção B · elevações Norte e Sul'),
    ('10', 'Opção B · elevações Leste e Oeste'),
    ('11', 'Parede Leste 358 × 260 cm (a confirmar)'),
    ('12', 'Quantitativo, lista de corte e consumíveis'),
    ('13', 'Escopo de serviços'),
    ('14', 'Execução: sequência, pontos de parada e aceite'),
    ('15', 'Recálculo com a medida real e detalhes de encontro'),
    ('16', 'Pendências e decisões'),
]

def pct(c_, a):
    return '%d%%' % round(c_ / a * 100)

def s01(c):
    header(c, 'Projeto executivo de paginação',
           'Revestimento de parede do banheiro com a linha Bouché (Portobello). Análise dos cinco arquivos recebidos, '
           'nova paginação com cortes iguais nas duas pontas de cada parede, nas duas opções de peça, mais quantitativo, '
           'escopo de serviços e roteiro de execução.', 1, TOTAL)
    x0 = MG; y = PH - 135
    # números
    y = section(c, x0, y, 'Resultado em quatro números', 560)
    tiles = [
        ('17,94 m²', 'de parede líquida', 'quatro paredes até o forro, vão da porta descontado'),
        ('49%', 'é o menor corte da malha', '3,65 cm na opção B; na opção A o menor é 8,15 cm (53%)'),
        ('9,25 cm', 'em cima e embaixo', 'mesma fiada nas quatro paredes: as juntas fecham nos cantos'),
        ('%d · %d' % (TA['caixas'], TB['caixas']), 'caixas A · B', 'com a embalagem real (36 e 26 peças), reserva de 10%'),
    ]
    tw = 134; gx = 8
    for i, (big, l1, l2) in enumerate(tiles):
        tx = x0 + i * (tw + gx)
        rect(c, tx, y - 112, tw, 112, None, K, 0.8)
        txt(c, tx + 8, y - 36, big, 28, 'S-B')
        txt(c, tx + 8, y - 53, l1, 9.6, 'S-B')
        para(c, tx + 8, y - 57, tw - 14, l2, 8.4, 10.6, 'S', K70)
    y -= 134
    y = section(c, x0, y, 'O que esta emissão entrega', 560)
    itens = [
        'Leitura crítica dos cinco PDFs: o que está certo, o que está errado e o que oferece risco, com a caixa de 1,44 m² que não existe no produto e as fiadas que não fecham nos cantos.',
        'Paginação refeita com o eixo no centro de cada parede e cortes iguais nas duas pontas, nas opções A (15,5 × 15,5) e B (7,5 × 15,5).',
        'Planificação e elevações cotadas das quatro paredes, com numeração de colunas e fiadas, vão da porta P02 e vidro K01 no lugar.',
        'Régua de modulação (marcas em cm) para levar a malha do papel para a parede.',
        'Quantitativo em peças e em caixas reais, lista de corte por dimensão e consumíveis estimados.',
        'Escopo de serviços (RV00 a RV11), sequência de execução, pontos de parada, critérios de aceite e recálculo com a medida de obra.',
    ]
    for it in itens:
        txt(c, x0, y - 10, '•', 9.8)
        y = para(c, x0 + 12, y, 545, it, 9.8, 12.8) - 5
    y -= 12
    y = section(c, x0, y, 'Premissas desta emissão', 560)
    rows = [
        ['Superfície', 'Banheiro 1,43 × 2,64 m · altura 2,40 m (forro novo R03) · 4 paredes · 17,94 m² líquidos (vão P02 de 1,60 m² descontado)'],
        ['Peça', 'Opção A 15,5 × 15,5 cm e opção B 7,5 × 15,5 cm (formato real). Os arquivos chamavam de 7×15 e 15×15.'],
        ['Dados da caixa', 'A: 36 peças = 0,87 m². B: 26 peças = 0,30 m². Fonte: ficha Portobello da linha Gouache de mesmo formato (borda Bold, 9 mm, variação V4). Ficha do Bouché não localizada.'],
        ['Junta', '3,0 mm entre fiadas em toda a obra. Entre colunas: 3,0 mm, exceto na opção B das paredes de 2,64 m (2,7 mm) para fechar a meia peça.'],
        ['Orientação', 'Faces como na folha do caderno (norte da folha no topo da planta). Elevações vistas de dentro do banheiro.'],
        ['Reserva', '10% sobre as peças físicas (quebra e reposição), arredondada para caixa fechada.'],
    ]
    table(c, x0, y, [96, 464], None, rows, size=9.0, pad=3.8, bold_first=True, zebra=False)
    # índice
    xi = 700; yi = PH - 135
    yi = section(c, xi, yi, 'Índice do caderno', PW - MG - xi)
    for n, t in INDICE:
        txt(c, xi, yi - 11, n, 12, 'S-B')
        txt(c, xi + 30, yi - 11, t, 10.8)
        yi -= 25
        line(c, xi, yi + 5, PW - MG, yi + 5, 0.3, K20)
    yi -= 8
    rect(c, xi, yi - 104, PW - MG - xi, 104, MAGENTA12, MAGENTA, 0.9)
    para(c, xi + 10, yi - 4, PW - MG - xi - 20,
         'ESTADO DA EMISSÃO', 9.6, 12, 'S-B', MAGENTA)
    para(c, xi + 10, yi - 20, PW - MG - xi - 20,
         'Para conferência em obra. As cotas vêm dos arquivos recebidos e do scan de 02.09.2026 e ainda não foram medidas com o emboço pronto. '
         'O produto Bouché não foi localizado no site da Portobello e a parede Leste de 358 × 260 cm não casa com o banheiro. '
         'Feche as pendências da Prancha 16 antes de cortar e comprar.', 9.4, 12.6)
    footer(c, 1, TOTAL)

def s02(c):
    header(c, 'Análise dos cinco arquivos recebidos',
           'Os PDFs são impressões do Paginador de Revestimentos. Reproduzi cada um com os mesmos dados de entrada e os números bateram. '
           'Abaixo, o que está certo, o que está errado e o que oferece risco.', 2, TOTAL)
    y = PH - 130
    W = [112, 128, 52, 118, 108, 118, 454]
    head = ['Arquivo', 'Entrada', 'Partida X · Y (cm)', 'Pontas esquerda · direita', 'Fiadas topo · piso', 'Compra no PDF → real', 'O que está errado']
    R = lambda *a: list(a)
    rows = [
        R('NORTE E SUL · 7×15', '143 × 240 cm · peça 7,5 × 15,5 · junta 3 mm · a prumo', '5,3 · 8,1',
          '5,0 · 5,1 (67%)\nsimétrica: boa', '7,8 · 10,7\ndiferença de 2,9 cm',
          'PDF sem resultado → 304 pç, 13 caixas',
          'O PDF perdeu a 3ª página: faltam área, caixas, cortes de borda e régua. Fiadas desiguais: a de piso é 2,9 cm maior que a de topo.'),
        R('NORTE E SUL · 15×15', '143 × 240 cm · peça 15,5 × 15,5', '8,1 · 6,6',
          '7,8 · 8,5 (50–55%)\nquase simétrica', '6,3 (41%) · 12,2 (79%)\ndiferença de 5,9 cm',
          '176 pç · 3 caixas → 5 caixas',
          'Fiada de topo no limite e a de piso quase inteira. As fiadas começam a 6,6 cm do teto, enquanto Leste e Oeste começam a 9,5: as juntas horizontais saltam 2,9 cm em cada canto.'),
        R('LESTE E OESTE · 7×15', '264 × 240 cm · peça 7,5 × 15,5', '0 · 9,5',
          '7,5 (inteira) · 6,6\nassimétrica', '9,2 · 9,3\nsimétricas: boas',
          '599 pç · 5 caixas → 24 caixas',
          'Ponta esquerda inteira e a direita cortada: o corte pesa só de um lado. A caixa de 1,44 m² subestima a compra em 4,8 vezes.'),
        R('LESTE E OESTE · 15×15', '264 × 240 cm · peça 15,5 × 15,5', '5,6 · 9,5',
          '5,3 (34%) · 5,6 (36%)\nestreitas', '9,2 · 9,3\nsimétricas: boas',
          '317 pç · 6 caixas → 9 caixas',
          'Pontas no limite de 1/3: o aviso do Paginador não disparou, mas são cortes frágeis. Com 15 inteiras o corte sobe para 13,35 cm nas duas pontas.'),
        R('LESTE · 15×15', '358 × 260 cm · peça 15,5 × 15,5', '0 · 11,6',
          '15,5 (inteira) · 10,4\nassimétrica', '11,3 · 11,4\nsimétricas: boas',
          '431 pç · 8 caixas → 12 caixas',
          'A parede Leste aparece com 358 × 260 aqui e com 264 × 240 em "Leste e Oeste". Ou são duas paredes, ou uma está errada. A altura de 2,60 m também não bate com o forro a 2,40 m.'),
    ]
    y = table(c, MG, y, W, head, rows, size=9.0, pad=4.2, hsize=8.6)
    y -= 28
    cw = (PW - 2 * MG - 28) / 2
    y1 = section(c, MG, y, 'Problemas que valem para os cinco arquivos', cw)
    gen = [
        ('Caixa de 1,44 m².', 'É o valor de exemplo do Paginador, não o do produto. A ficha Portobello de mesmo formato traz 36 peças = 0,87 m² (15,5 × 15,5) e 26 peças = 0,30 m² (7,5 × 15,5). Todas as caixas dos PDFs estão baixas.'),
        ('Junta de 3 mm sem validação.', 'A ficha da linha de mesmo formato indica 1,5 mm para parede interna molhada, e o anúncio de outra peça Portobello de borda Bold fala em mais de 2 mm. 3 mm pode ser a escolha certa, mas é decisão a provar em mock-up.'),
        ('Produto e formato.', 'Não achei "Bouché" no site da Portobello. As medidas 7,5 × 15,5 e 15,5 × 15,5, com borda Bold e 9 mm, batem com a linha Gouache. Os nomes dos arquivos (7×15, 15×15) são nominais: o pedido usa o formato real.'),
        ('Partida sem regra.', 'Cada arquivo usa um deslocamento digitado à mão, sem eixo comum. Por isso as paredes dão resultados incoerentes entre si.'),
    ]
    for h, b in gen:
        y1 = rich(c, MG, y1, cw, h, b, 9.2, 6)
    xr = MG + cw + 28
    y2 = section(c, xr, y, 'Também faltou', cw)
    gen2 = [
        ('Vãos e elementos.', 'Porta P02 (Leste, 0,80 × 2,00), vidro K01, bancada, ralo e pontos elétricos e hidráulicos não aparecem. Só o vão da porta tira %d peças da opção A e cria cortes de batente.' % TA['rows']['LESTE']['removed']),
        ('Cota vertical.', 'Os 2,40 m dependem do piso acabado (P05, cota única) e do forro novo (R03), ainda abertos. A fiada de piso e a de topo mudam com eles.'),
        ('Aproveitamento da peça.', 'Na opção B, nas paredes de 2,64 m, as duas pontas saem de uma única peça cortada ao meio: 16 peças a menos por parede.'),
        ('Impressão.', 'Cada PDF saiu em 2 ou 3 folhas A4, com o desenho cortado no meio da página e sem nome da parede, escala, data ou revisão. Dá para errar de parede na obra.'),
        ('Impermeabilização.', 'O item C1 prevê rodapé virado no piso, mas não define a altura da subida nas paredes do box, que são revestidas até 2,40 m.'),
    ]
    for h, b in gen2:
        y2 = rich(c, xr, y2, cw, h, b, 9.2, 6)
    footer(c, 2, TOTAL)

def cand_rows(W, a, jn=0.3):
    out = []
    for n in range(1, int(W // a) + 2):
        cc = (W - n * a - (n + 1) * jn) / 2
        if 0 < cc < a: out.append((n, cc))
    return out

def s03(c):
    header(c, 'Critério de paginação e quadro antes × depois',
           'A regra que você pediu, escrita para valer em todas as paredes: eixo no centro, cortes iguais nas duas pontas e, quando a junta deixa, meia peça '
           'de cada lado (7,5 cm vira 3,65 + 3,65).', 3, TOTAL)
    y = PH - 130
    wl = 505
    y = section(c, MG, y, 'As regras', wl)
    regras = [
        ('R1 · Eixo no centro.', 'Cada parede nasce do seu eixo vertical. As duas pontas recebem o mesmo corte. Número ímpar de peças inteiras põe uma peça no eixo; par põe uma junta.'),
        ('R2 · Meia peça sempre que a junta deixar.', 'Corte = (peça − 2 mm de disco) ÷ 2. A junta pode variar de 2,5 a 3,5 mm para chegar lá. Peça de 7,5 cm: 3,65 + 3,65, e as duas pontas saem da mesma peça.'),
        ('R3 · Se não der meia peça.', 'Junta de 3,0 mm e o corte mais próximo da metade, nunca abaixo de 40% da peça. Abaixo de 1/3 é crítico e não entra.'),
        ('R4 · Fiadas iguais nas quatro paredes.', 'Mesma regra na vertical, com junta fixa de 3,0 mm: corte igual embaixo e em cima (9,25 cm). Como as quatro paredes têm 2,40 m, as juntas horizontais fecham em volta do banheiro.'),
        ('R5 · Cotas de referência.', 'Piso acabado (cota única P05) e forro novo (R03). Fiadas de piso e de topo são cortadas 3 a 5 mm menores para a junta de movimentação.'),
        ('R6 · Vãos.', 'A malha é paginada na parede inteira e o vão é recortado depois, sem deslocar nada. Aresta de batente a menos de 2 cm de uma junta vira aviso.'),
        ('R7 · Pontos.', 'Tomadas, registros e chuveiro no centro da peça ou exatamente na junta. Nunca a 1 cm de uma junta.'),
        ('R8 · Espelhamento.', 'Norte e Sul têm a mesma malha, e Leste e Oeste também. Por isso a régua de uma serve à outra, espelhada.'),
    ]
    for h, b in regras:
        y = rich(c, MG, y, wl, h, b, 9.2, 5.5)
    # como o n é escolhido
    y -= 12
    y = section(c, MG, y, 'Como o número de peças inteiras é escolhido', wl)
    cand = []
    for nome, W_, a_ in (('A · 2,64 m', 264, 15.5), ('A · 1,43 m', 143, 15.5), ('B · 2,64 m', 264, 7.5), ('B · 1,43 m', 143, 7.5)):
        p = E.plan_axis(W_, a_, 0.25, 0.35)
        rows_ = cand_rows(W_, a_)
        for n, cc in rows_:
            if n >= p['n'] - 1 and n <= p['n'] + 0:
                escolhido = (n == p['n'])
                if escolhido and p['mode'] == 'meia':
                    cand.append({'cells': [nome, str(n), '%s cm (junta %s mm)' % (fx(p['c'], 2), fx(p['j'] * 10, 1)), pct(p['c'], a_), 'ESCOLHIDA · meia peça'], 'fill': CIANO18})
                elif escolhido:
                    cand.append({'cells': [nome, str(n), '%s cm' % fx(p['c'], 2), pct(p['c'], a_), 'ESCOLHIDA'], 'fill': CIANO18})
                else:
                    cand.append([nome, str(n), '%s cm' % fx(cc, 2), pct(cc, a_), 'recusada'])
    for n, cc in cand_rows(264, 15.5):
        if n == 16:
            cand.insert(0, ['A · 2,64 m', '16', '%s cm' % fx(cc, 2), pct(cc, 15.5), 'recusada: 35%, quase no limite de 1/3'])
    table(c, MG, y, [78, 52, 132, 48, 195], ['Parede · peça', 'Inteiras', 'Corte nas pontas', '% da peça', 'Decisão'], cand, size=8.6, pad=3.4, zebra=False)

    # quadro antes x depois
    xr = MG + wl + 30; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Antes × depois', wr)
    d = lambda p: '%s · %s' % (fx(p['c'], 2), fx(p['c'], 2))
    hpA143, vpA = C.plan(143, 240, A); hpA264, _ = C.plan(264, 240, A); hpA358, vpA2 = C.plan(358, 260, A)
    hpB143, vpB = C.plan(143, 240, B); hpB264, _ = C.plan(264, 240, B); hpB358, vpB2 = C.plan(358, 260, B)
    rows = [
        ['Norte e Sul · 7×15', '5,0 · 5,1', '7,8 · 10,7', d(hpB143), d(vpB), 'pontas já boas; fiadas igualadas'],
        ['Norte e Sul · 15×15', '7,8 · 8,5', '6,3 · 12,2', d(hpA143), d(vpA), 'fiada de topo sai de 41% para 60%'],
        ['Leste e Oeste · 7×15', '7,5 · 6,6', '9,2 · 9,3', d(hpB264), d(vpB), 'meia peça exata; junta 2,7 mm'],
        ['Leste e Oeste · 15×15', '5,3 · 5,6', '9,2 · 9,3', d(hpA264), d(vpA), 'de 34–36% para 86%'],
        ['Leste · 15×15 (358 × 260)', '15,5 · 10,4', '11,3 · 11,4', d(hpA358), d(vpA2), 'a confirmar (Prancha 11)'],
    ]
    table(c, xr, yr, [128, 62, 62, 66, 62, wr - 380], ['Arquivo', 'Pontas antes', 'Fiadas antes', 'Pontas depois', 'Fiadas depois', 'Efeito'],
          rows, size=8.6, pad=3.6, aligns=['l', 'r', 'r', 'r', 'r', 'l'], hsize=8.2)
    # esquema
    ye = yr - 215
    ye = section(c, xr, ye, 'Esquema: a mesma parede, antes e depois (opção A, 2,64 m, escala fora de 1:1)', wr)
    wpt = wr - 20
    # antes: ponta 5,6 / 5,3 (L/O 15x15)
    hp_old = dict(n=16, j=0.3, c=5.45)
    rect(c, xr, ye - 28, wpt, 24, None, None)
    # antes
    sc_ = wpt / 264.0
    def faixa(y_, ox, W_, a_, pts, lab):
        for (x0_, x1_, t_) in pts:
            rect(c, xr + x0_ * sc_, y_, (x1_ - x0_) * sc_, 24, AMARELO45 if t_ == 'c' else white, K, 0.4)
        txt(c, xr, y_ + 29, lab, 7.8, 'S-B')
    # antes: partida 5,6 → esquerda 5,3, direita 5,6 (arquivo Leste e Oeste 15x15)
    pts_ant = [(0, 5.3, 'c')]
    x = 5.6
    while x + 15.5 <= 264 + 1e-6:
        pts_ant.append((x, x + 15.5, 'f')); x += 15.8
    pts_ant.append((264 - 5.6, 264, 'c'))
    faixa(ye - 36, xr, 264, 15.5, pts_ant, 'Antes: 16 inteiras e pontas de 5,3 e 5,6 cm (34–36%)')
    faixa(ye - 96, xr, 264, 15.5, E.spans(264, 15.5, hpA264), 'Depois: 15 inteiras e pontas de 13,35 cm (86%), peça central sobre o eixo')
    for yy in (ye - 36, ye - 96):
        line(c, xr + wpt / 2, yy - 6, xr + wpt / 2, yy + 30, 0.8, MAGENTA, (4, 1.5, 1, 1.5))
    footer(c, 3, TOTAL)

def s04(c):
    header(c, 'Planta do banheiro e nomenclatura das paredes',
           'As quatro paredes recebem o nome da face da folha do caderno (norte da folha no topo da planta). Cada elevação deste caderno é vista de dentro do banheiro. '
           'Geometria lida do scan de 02.09.2026 e da Prancha 08 do caderno.', 4, TOTAL)
    sc = 1.78
    W, L = 143.0, 263.8
    ox = MG + 110; oy = 128
    X = lambda v: ox + v * sc
    Yt = lambda v: oy + (L - v) * sc            # v = distância a partir da face norte
    # paredes (espessura 10)
    t = 10
    rect(c, X(-t), Yt(L + t), (W + 2 * t) * sc, (L + 2 * t) * sc, K, None)
    rect(c, X(0), Yt(L), W * sc, L * sc, white, K, 0.8)
    # box
    rect(c, X(0), Yt(L), W * sc, (L - 171.1) * sc, CIANO18, None)
    txt(c, X(W / 2), Yt(L) + (L - 171.1) * sc / 2 + 12, 'BOX', 9, 'S-B', K70, 'c')
    txt(c, X(W / 2), Yt(L) + (L - 171.1) * sc / 2, '1,43 × 0,93', 7.2, 'S', K70, 'c')
    # K01
    rect(c, X(0), Yt(171.1) - 1.6, W * sc, 3.2, CIANO, K, 0.5)
    txt(c, X(W / 2), Yt(171.1) + 6, 'K01 vidro (171,1 do norte)', 6.6, 'S-B', K, 'c')
    # ralo
    rect(c, X(2), Yt(L - 2) , 5 * sc, 80 * sc, white, K, 0.6)
    txt(c, X(2) + 5 * sc + 4, Yt(L - 2) + 40 * sc, 'ralo linear', 6.2, 'S-I', K70, 'l')
    # bancada
    rect(c, X(0), Yt(109.1), 39.5 * sc, (109.1 - 47.8) * sc, white, K, 0.9)
    txt(c, X(0) + 39.5 * sc / 2, Yt(78.4) - 2, 'bancada', 6.8, 'S-B', K, 'c')
    # porta (vão na parede leste)
    rect(c, X(W) - 1, Yt(125.5), (t + 2) * sc, 80 * sc, white, K, 0.8)
    line(c, X(W + t), Yt(45.5), X(W + t), Yt(125.5), 0.5, K70)
    txt(c, X(W) + (t + 8) * sc, Yt(85.5), 'P02', 8.4, 'S-B', K, 'l')
    txt(c, X(W) + (t + 8) * sc, Yt(85.5) - 9, '0,80 × 2,00', 6.6, 'S', K70, 'l')
    # R02
    rect(c, X(-t), Yt(L), (W + 2 * t) * sc, t * sc, MAGENTA12, MAGENTA, 1.0)
    txt(c, X(W / 2), Yt(L) - 12, 'R02 parede nova · fundo do box', 6.6, 'S-B', MAGENTA, 'c')
    # nomes das faces
    txt(c, X(W / 2), Yt(0) + 10 * sc + 8, 'NORTE', 11, 'S-B', K, 'c', ls=1.2)
    txt(c, X(W / 2), Yt(L) - 10 * sc - 28, 'SUL', 11, 'S-B', K, 'c', ls=1.2)
    txt(c, X(-t) - 12, Yt(L / 2), 'OESTE', 11, 'S-B', K, 'c', rot=90, ls=1.2)
    txt(c, X(W + t) + 22, Yt(L / 2) - 30, 'LESTE', 11, 'S-B', K, 'c', rot=-90, ls=1.2)
    # cotas
    dimh(c, X(0), X(W), Yt(0) + 10 * sc + 40, '1,43 m', 7.2, bold=True)
    dimv(c, X(-t) - 36, Yt(L), Yt(0), '2,64 m', 7.2, bold=True)
    dimv(c, X(-t) - 22, Yt(171.1), Yt(0), '1,71', 6.6)
    dimv(c, X(-t) - 22, Yt(L), Yt(171.1), '0,93', 6.6)
    # setas de vista
    def seta(x, y, dx, dy, lab, ldx=0, ldy=0):
        line(c, x, y, x + dx, y + dy, 0.9, MAGENTA)
        import math
        ang = math.atan2(dy, dx); ah = 6
        px = x + dx; py = y + dy
        p = c.beginPath(); p.moveTo(px, py)
        p.lineTo(px - ah * math.cos(ang - 0.4), py - ah * math.sin(ang - 0.4))
        p.lineTo(px - ah * math.cos(ang + 0.4), py - ah * math.sin(ang + 0.4)); p.close()
        c.saveState(); c.setFillColor(MAGENTA); c.drawPath(p, fill=1, stroke=0); c.restoreState()
        txt(c, x + ldx, y + ldy, lab, 6.8, 'S-B', MAGENTA, 'c')
    cx_, cy_ = X(W / 2) + 12, Yt(88)
    seta(cx_, cy_ + 10, 0, 40, '', 0, 0); txt(c, cx_ + 6, cy_ + 54, 'vista N', 7.6, 'S-B', MAGENTA, 'l')
    seta(cx_ + 10, cy_, 36, 0, '', 0, 0); txt(c, cx_ + 52, cy_ - 2.6, 'vista L', 7.6, 'S-B', MAGENTA, 'l')
    seta(cx_, cy_ - 10, 0, -40, '', 0, 0); txt(c, cx_ + 6, cy_ - 58, 'vista S', 7.6, 'S-B', MAGENTA, 'l')
    seta(cx_ - 10, cy_, -26, 0, '', 0, 0); txt(c, cx_ - 42, cy_ - 2.6, 'vista O', 7.6, 'S-B', MAGENTA, 'r')
    # tabela das paredes
    xr = 640; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'As quatro paredes', wr)
    rows = [
        ['NORTE', '143 × 240', 'Esquerda = oeste, direita = leste', 'Parede lisa, só revestimento. Embutidos EM no forro, sem ponto na parede.'],
        ['LESTE', '264 × 240', 'Esquerda = norte, direita = sul', 'Porta P02 a 45,5–125,5 cm do canto norte (zona seca). K01 a 171,1. Box em 171,1–264.'],
        ['SUL', '143 × 240', 'Esquerda = leste, direita = oeste', 'R02, parede nova no fundo do box. Toda molhada. Pontos do chuveiro a definir.'],
        ['OESTE', '264 × 240', 'Esquerda = sul, direita = norte', 'Box em 0–92,9. K01 a 92,9. Bancada de 0,61 m (de 154,9 a 216,2) com espelho, S03 e T17.'],
    ]
    yy = table(c, xr, yr, [58, 70, 150, wr - 278], ['Parede', 'L × A (cm)', 'Vista de dentro', 'O que tem'], rows, size=9.0, pad=4.0, bold_first=True)
    yy -= 22
    yy = section(c, xr, yy, 'Fontes e tolerâncias', wr)
    for h, b in [
        ('Interior.', 'Scan: 1,432 × 2,638 m (3,78 m²). Os arquivos usaram 143 × 264, arredondado. O desenho usa 143,0 × 263,8 apenas na planta; a paginação usa 143 × 264.'),
        ('Porta e bancada.', 'Posições lidas do vetor do scan (Prancha 08). Precisão de cerca de 1 a 2 cm: conferir com o batente instalado.'),
        ('Altura.', '2,40 m, do piso acabado ao forro novo, confirmada pelo cliente em 21.09. Depende de P05 e R03.'),
        ('Norte.', 'Os nomes das faces seguem a folha do caderno. O norte verdadeiro está a 126° do topo da folha (Prancha 01).'),
    ]:
        yy = rich(c, xr, yy, wr, h, b, 9.2, 6)
    yy -= 10
    yy = section(c, xr, yy, 'Legenda da planta', wr)
    legend(c, xr, yy - 8, [('wet', 'área molhada (box)'), ('k01', 'vidro K01'), ('crit', 'R02 parede nova'), ('door', 'vão da porta P02')], 8.6, 18)
    footer(c, 4, TOTAL)
