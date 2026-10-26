# -*- coding: utf-8 -*-
import json, os, math
from lib import *
import calc_r1 as CR
from draw_r1 import *

TOTAL = 22
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS_T, RES = CR.totals()
RT = {r['id']: r for r in ROWS_T}
R0S = json.load(open(os.path.join(HERE, 'dados', 'r0_stats.json')))
BUD = json.load(open(os.path.join(HERE, 'dados', 'budget.json')))
N_PCS = sum(r['nb'] + r['nn'] for r in ROWS_T)
N_FULL = sum(r['full'] for r in ROWS_T)
N_CUT = sum(r['cut'] for r in ROWS_T)
SC15 = 72 / 25.4 / 15     # pt por mm em 1:15
SC20 = 72 / 25.4 / 20
SC25 = 72 / 25.4 / 25
SC10 = 72 / 25.4 / 10

def brl(v):
    s = '{:,.2f}'.format(v)
    return 'R$ ' + s.replace(',', 'X').replace('.', ',').replace('X', '.')

INDICE = [
    ('01', 'Capa, índice e premissas'), ('02', 'Condições para liberação e o que muda da R0'),
    ('03', 'Planta e demolição'), ('04', 'Água quente e ralos'), ('05', 'Iluminação e energia'),
    ('06', 'Bancada e impermeabilização'), ('07', 'Critério de paginação e quadro R0 × R2'),
    ('08', 'Planificação das paredes'), ('09', 'P1 · fundo do box e nicho'), ('10', 'P2 · lateral do box e P6 · retorno'),
    ('11', 'P3 · parede da bancada'), ('12', 'P4 · parede da porta'), ('13', 'P5 · parede do vaso'),
    ('14', 'Bancada · tampo e bordas'), ('15', 'Quantitativo e compra'), ('16', 'Orçamento R2'),
    ('17', 'Compatibilização de compras'), ('18', 'Escopo de serviços'), ('19', 'Execução e aceite'),
    ('20', 'Recálculo com calibre e medida de obra'), ('21', 'Pendências e decisões'), ('22', 'Fontes e premissas'),
]

def s01(c):
    header(c, 'Caderno técnico de reforma do banheiro',
           'Everest + Gouache Bleu Nuit / Nuage. A R2 reestrutura o caderno R0: nicho centrado na parede do box, paginação com o máximo de peças inteiras, eixo central e '
           'cortes simétricos; compra dos revestimentos por área + 10%; orçamento R2 com sobreposições resolvidas.', 1, TOTAL)
    x0 = MG; y = PH - 135
    y = section(c, x0, y, 'R2 em quatro números', 580)
    tiles = [
        ('%d%%' % round(N_FULL / N_PCS * 100), 'das peças ficam inteiras', '%d de %d peças. Nenhuma fiada cortada no topo das paredes.' % (N_FULL, N_PCS)),
        ('%d' % (sum(R0S[k]['frag'] for k in R0S) - sum(RT[k]['nb'] + RT[k]['nn'] for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6'))), 'fragmentos a menos', 'nas paredes, contra o R0: some a tira de 36 mm do topo (107 tiras).'),
        ('%d + %d' % (RES['B']['caixas'], RES['N']['caixas']), 'caixas Bleu + Nuage', 'área revestida + 10%%: %s m² de compra. R0 e R1 previam 70 + 7.' %
         fm(RES['B']['m2_compra'] + RES['N']['m2_compra'], 2)),
        (brl(BUD['total']).replace('R$ ', ''), 'total R2 com 15%', 'subtotal %s. Inclui impermeabilização; argamassa com a empreiteira.' % brl(BUD['subtotal'])),
    ]
    tw = 139; gx = 8
    for i, (big, l1, l2) in enumerate(tiles):
        tx = x0 + i * (tw + gx)
        rect(c, tx, y - 112, tw, 112, None, K, 0.8)
        txt(c, tx + 8, y - 36, big, 24 if len(big) < 8 else 20, 'S-B')
        txt(c, tx + 8, y - 53, l1, 9.4, 'S-B')
        para(c, tx + 8, y - 57, tw - 14, l2, 8.2, 10.4, 'S', K70)
    y -= 134
    y = section(c, x0, y, 'Premissas', 580)
    rows = [
        ['Banheiro', '1.423 × 2.583 mm (modelo R47), box 1.271 × 877 mm, área técnica 150 × 877 mm, porta 800 mm na parede P4.'],
        ['Escopo', 'Demolição de acabamentos, bancada, extensão de água quente, troca dos dois ralos, iluminação adicional, impermeabilização, paginação e orçamento. Vaso, gabinete e box reaproveitados. Kit Hídrica (cozinha) excluído.'],
        ['Revestimento', 'Gouache Bleu Nuit nas paredes, com acentos Nuage; tampo e bordas da bancada em Nuage. Peça nominal 75 × 155 mm em pé, junta de 2 mm.'],
        ['Paginação', '15 fiadas inteiras desde o piso: o revestimento termina em 2.353 mm, com perfil. Colunas simétricas no eixo de cada parede.'],
        ['Compra', 'Área revestida × 1,10, arredondada para caixa fechada (0,30 m² / 26 peças) e conferida contra as peças físicas.'],
        ['Piso', 'Monofloor Everest contínuo; o sistema para o box depende de aprovação do fabricante.'],
    ]
    table(c, x0, y, [96, 484], None, rows, size=8.8, pad=3.6, bold_first=True, zebra=False)
    xi = 700; yi = PH - 135
    yi = section(c, xi, yi, 'Índice', PW - MG - xi)
    for n, t in INDICE:
        txt(c, xi, yi - 10, n, 10.5, 'S-B'); txt(c, xi + 28, yi - 10, t, 9.6)
        yi -= 20.5; line(c, xi, yi + 5, PW - MG, yi + 5, 0.3, K20)
    footer(c, 1, TOTAL)

def s02(c):
    header(c, 'Condições para liberação e o que muda da R0',
           'O que precisa estar resolvido antes de demolir e cortar, e o resumo das mudanças desta revisão.', 2, TOTAL)
    xl = MG; wl = 520
    y = section(c, xl, PH - 130, 'Condições para liberação', wl)
    cond = [
        ('Levantamento no local.', 'Prumos, dimensões acabadas, contrapiso, impermeabilização existente, tubulações, pressão e capacidade do aquecedor.'),
        ('Responsável técnico.', 'Compatibiliza instalações, estrutura da bancada e a reforma com o condomínio e emite a documentação aplicável. Não cortar laje, vigas, pilares ou shafts.'),
        ('Lote e calibre.', 'O modelo usa 75 × 155 mm; o certificado Nuage informa 76,5 × 155,5 mm de fabricação. Medir peças do lote real e refazer a paginação antes de cortar (Prancha 20).'),
        ('Gouache no tampo.', 'Gouache é revestimento de parede. Uso horizontal no tampo depende de aprovação do fabricante e de base impermeável detalhada.'),
        ('Monofloor.', 'O fabricante aprova o sistema Everest para o box: aderência, atrito molhado, selagem, ralos e manutenção.'),
        ('Altura do revestimento.', 'Aprovar o término em 2.353 mm com perfil e a faixa de 38 mm em pintura até o forro (Prancha 07).'),
        ('Nicho centrado.', 'O nicho anda 78 mm para o centro da P1: o responsável técnico confirma estrutura, impermeabilização e redes antes de reconstruí-lo.'),
    ]
    for i, (h, b) in enumerate(cond, 1):
        txt(c, xl, y - 12, str(i), 12, 'S-B')
        y = rich(c, xl + 20, y - 2, wl - 20, h, b, 9.4, 6)
    xr = MG + wl + 40; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'R0 → R2', wr)
    rows = [
        ['Paginação das paredes', 'Malha a partir do canto inferior esquerdo; ponta inteira de um lado e corte de 30–42 mm do outro; fiada de 36 mm no topo.',
         'Eixo central e pontas simétricas de 43,5 a 59 mm; 15 fiadas inteiras e topo em 2.353 mm; nicho centrado com os lados exatamente nas juntas.'],
        ['Peças nas paredes', '%d fragmentos (P1–P6)' % sum(R0S[k]['frag'] for k in R0S),
         '%d peças (P1–P6), %d inteiras' % (sum(RT[k]['nb'] + RT[k]['nn'] for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')),
                                           sum(RT[k]['full'] for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')))],
        ['Compra de revestimento', 'Cada peça cortada + 10%: 70 caixas Bleu e 7 Nuage.', 'Área + 10%%: %d caixas Bleu e %d Nuage, conferidas contra as peças físicas.' % (RES['B']['caixas'], RES['N']['caixas'])],
        ['Orçamento', 'R1: subtotal %s.' % brl(BUD['r1_subtotal']), 'R2: subtotal %s; argamassa com a empreiteira; impermeabilização incluída; sobreposições resolvidas.' % brl(BUD['subtotal'])],
        ['Nicho', 'Deslocado para a esquerda (59 a 1.061 mm); peças cortadas nos lados (16, 17, 58 mm).', 'Centrado na parede (137,5 a 1.137,5 mm), 1000 × 400 × 118: ocupa 13 colunas inteiras, lados sobre juntas, peça de 77 mm acima.'],
        ['Bancada', '10 inteiras + corte por fiada.', 'Igual em contagem; corte de 80 mm na ponta norte, fiadas inteiras a partir da frente.'],
        ['Caderno', '23 folhas, paginação por parede sem cotas de corte.', '22 pranchas A3 com elevações cotadas, régua de fiadas, escopo, execução e pendências.'],
    ]
    table(c, xr, yr, [112, (wr - 112) / 2, (wr - 112) / 2], ['Tema', 'R0', 'R2'], rows, size=8.6, pad=3.8, bold_first=True, hsize=8.6)
    footer(c, 2, TOTAL)

def plan_sheet(c, n, titulo, sub, mode, blocks):
    header(c, titulo, sub, n, TOTAL)
    ox = MG + 150; oy = PH - 175
    draw_plan(c, ox, oy, SC15, mode)
    txt(c, ox - 10, 72, 'Esquema cotado, escala 1:15 · não medir pela impressão. Posição do vaso e da derivação de água quente: conferir em obra.', 7.2, 'S-I', K70)
    xr = 660; wr = PW - MG - xr
    yr = PH - 130
    for titulo_b, itens in blocks:
        yr = section(c, xr, yr, titulo_b, wr)
        for h, b in itens:
            yr = rich(c, xr, yr, wr, h, b, 9.2, 6)
        yr -= 16
    footer(c, n, TOTAL)

def s03(c):
    plan_sheet(c, 3, 'Planta e demolição', 'O que sai, o que fica e em que ordem. A trama rosa é a área de demolição de acabamentos.', 'demo', [
        ('Remover', [
            ('Piso existente.', '3,54 m².'),
            ('Revestimentos verticais.', 'Previsão de 17,91 m²; confirmar a área atual antes de contratar a retirada.'),
            ('Bancada.', 'Retirar tampo e cuba antigos; preservar o gabinete se viável.'),
        ]),
        ('Preservar', [
            ('Estrutura e redes.', 'Posições das prumadas, áreas técnicas, nicho, porta, box e vaso. Desmontar e guardar os elementos reutilizáveis antes de demolir.'),
        ]),
        ('Sequência', [
            ('Ordem.', 'Proteção → isolamento das redes → desmontagem → remoção manual controlada → inspeção de base e redes → correção → impermeabilização → teste → revestimentos → montagem.'),
            ('Entulho.', 'Provisionar uma retirada; o volume real depende das espessuras. Não usar a área nova de azulejo como levantamento de demolição.'),
        ]),
    ])

def s04(c):
    plan_sheet(c, 4, 'Água quente e ralos', 'Derivação de água quente para a cuba e troca dos dois ralos. Traçado conceitual, não é rede levantada.', 'agua', [
        ('Água da cuba', [
            ('Derivação.', 'Água quente de ramal existente acessível, sem alterar o gás. Previsão de 6 m de tubo quente com isolamento; diâmetro, material e transições depois da abertura e do cálculo. Registro de isolamento acessível.'),
            ('Mistura.', 'Quente e fria chegam às bases do misturador; a bica recebe água já misturada. Não interligar redes com um tê simples. Não embutir mangueiras flexíveis.'),
        ]),
        ('R1 · ralo linear do box', [
            ('Produto.', 'Ralo completo 720 × 90 mm, conforme o modelo. O link de 600 × 90 mm foi descartado (Prancha 17). Confirmar altura do corpo, saída, fecho hídrico e vazão.'),
            ('Caimento.', '1 a 2% até o coletor, sujeito ao sistema Monofloor e às cotas existentes.'),
        ]),
        ('R2 · ao lado do vaso', [
            ('Proposta.', 'Grelha oculta quadrada 100 × 100 mm na posição da caixa existente, sem deslocar a saída. Posição desenhada é reserva: levantamento obrigatório. Preservar inspeção e desconexão sifonada.'),
        ]),
    ])

def s05(c):
    plan_sheet(c, 5, 'Iluminação e energia', 'Luminárias, chuveiro e toalheiro térmico. Quantitativos elétricos provisórios: o quadro não foi levantado.', 'luz', [
        ('L1 · L2 · L3', [
            ('L1.', 'Plafon geral existente; avaliar reaproveitamento.'),
            ('L2.', 'Plafon de box selado, proposta IP65 e 3000 K, no eixo do chuveiro; 304,5 mm entre centros.'),
            ('L3.', 'Perfil linear frontal ao espelho, 1650 mm, 3000 K, IRC ≥ 90, difusor contínuo, comando separado. Potência e fluxo pelo estudo luminotécnico; fonte acessível fora da área de respingos.'),
        ]),
        ('Toalheiro', [
            ('Aiello Unique Solo.', 'Inox escovado, fio oculto, variante com botão. Não especificar timer sem confirmação. Localizar a alimentação pelo gabarito do fabricante, sem atravessar redes hidráulicas, e casar a caixa com uma junta da malha.'),
        ]),
        ('Elétrica', [
            ('Verificação.', 'Eletricista confere volumes do box, tensão, aterramento, DR, proteções, seções, percurso e capacidade do circuito conforme a norma aplicável.'),
        ]),
    ])

def s06(c):
    header(c, 'Bancada e impermeabilização',
           'Cotas de coordenação da bancada, sistema de impermeabilização e critérios de acabamento. O corte mostra onde cada cota cai na malha das paredes.', 6, TOTAL)
    # corte esquemático da P3 com a bancada
    sc = SC15; ox = MG + 110; oy = 120
    Y = lambda v: oy + v * sc
    wx = 150  # largura do desenho (pt)
    rect(c, ox, Y(0), 18, CR.H_ROOM * sc, HexColor('#d9d9d9'), K, 0.6)
    for (y0, y1, t) in CR.ROWS:
        rect(c, ox + 18, Y(y0), 5, (y1 - y0) * sc, BLEU, K, 0.3)
    rect(c, ox + 18, Y(CR.H_TILE), 5, (CR.H_ROOM - CR.H_TILE) * sc, white, K45, 0.3)
    # tampo, borda, gabinete, cuba, espelho
    d = 530 * sc
    rect(c, ox + 23, Y(840 - 30), d, 30 * sc, NUAGE, K, 0.6)
    rect(c, ox + 23 + d - 9 * sc, Y(765), 9 * sc + 2, 75 * sc, NUAGE, K, 0.6)
    rect(c, ox + 23 + 20 * sc, Y(150), d - 60 * sc, (765 - 150) * sc, white, K45, 0.5, (3, 2))
    txt(c, ox + 23 + d / 2, Y(450), 'gabinete', 6.8, 'S-I', K70, 'c')
    rect(c, ox + 23 + 170 * sc, Y(840), 300 * sc, 160 * sc, white, K, 0.6)
    txt(c, ox + 23 + 320 * sc, Y(905), 'cuba', 6.6, 'S-I', K70, 'c')
    line(c, ox + 23, Y(1140), ox + 23 + 6, Y(1140), 1.6, K)
    rect(c, ox + 23, Y(1140), 4, 700 * sc, CIANO18, K, 0.4)
    marks = [(840, 'tampo acabado 840'), (765, 'base da borda frontal 765'), (1000, 'borda da cuba ≈ 1.000'), (1105, 'eixo da bica ≈ 1.105'),
             (1140, 'espelho, borda inferior 1.140'), (CR.H_TILE, 'topo do revestimento 2.353'), (CR.H_ROOM, 'superfície do modelo 2.391')]
    for v, lab in marks:
        line(c, ox - 30, Y(v), ox + 23 + d + 30, Y(v), 0.4, MAGENTA, (3, 2))
        txt(c, ox + 23 + d + 34, Y(v) - 2.5, lab, 7.2, 'S', K)
    for k in range(15):
        y0 = k * 157
        if k % 2 == 0: txt(c, ox - 34, Y(y0 + 77) - 2, 'F%d' % (k + 1), 5.6, 'S', K70, 'r')
    txt(c, ox, Y(CR.H_ROOM) + 14, 'CORTE NA BANCADA · P3 · 1:15', 8.4, 'S-B')
    para(c, ox, Y(0) - 8, 330, 'O tampo cai na fiada F6 (785–940) e o espelho na F8 (1.099–1.254): nenhuma linha de bancada coincide com junta, por isso o revestimento continua inteiro atrás do gabinete e do espelho, sem recorte.', 8.2, 10.6, 'S', K70)
    xr = 640; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Cotas de coordenação', wr)
    for h, b in [
        ('Tampo.', 'Acabado a 840 mm; 1650 × 530 mm. Borda nominal 75 mm, mantendo o gabinete abaixo. O modelo tem o topo da faixa frontal a 829 mm e o tampo a 840: compatibilizar os 11 mm com o lote. Não reduzir armadura nem apoios para acomodar azulejo.'),
        ('Espelho e cuba.', 'Espelho com borda inferior a 1.140 mm (300 mm acima do tampo). Cuba de apoio Ametista 16 com cerca de 160 mm: a borda fica perto de 1.000 mm.'),
        ('Bica e comandos.', 'Eixo aproximado a 1.105 mm. Ensaiar alcance do jato, mão de uso e afastamento do espelho com as peças reais. Furos só com o gabarito real.'),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 9.2, 6)
    yr -= 16
    yr = section(c, xr, yr, 'Impermeabilização (no orçamento R2)', wr)
    for h, b in [
        ('Área.', 'Todo o piso, paredes do box até 2.400 mm, rodapé técnico fora do box, bancada e nicho: cerca de 12 m², consumo a validar.'),
        ('Sistema.', 'Cimentício flexível completo, compatível com o substrato e com o revestimento (referência Tecplus Lastic, 3 baldes de 18 kg), com tela de poliéster em cantos, passagens, flanges e ralos. Base do nicho e tampo escoam sem empoçar.'),
        ('Teste.', 'Cura do fabricante e ensaio de estanqueidade por pelo menos 72 h antes de proteger e revestir, com registro. Selar perfurações posteriores.'),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 9.2, 6)
    yr -= 16
    yr = section(c, xr, yr, 'Critérios de acabamento', wr)
    yr = rich(c, xr, yr, wr, 'Junta e rejunte.', 'Junta adotada 2 mm; o fabricante lista 1,5 mm para paredes: confirmar com o lote. Rejunte acrílico Moon nas paredes é referência comercial a aprovar; Blanc no Nuage da bancada.', 9.2, 6)
    footer(c, 6, TOTAL)

def s07(c):
    header(c, 'Critério de paginação e quadro R0 × R2',
           'Prioridade: o máximo de peças inteiras com a paginação equilibrada. Os cortes que sobram ficam simétricos, largos e nas pontas.', 7, TOTAL)
    xl = MG; wl = 500
    y = section(c, xl, PH - 130, 'Regras', wl)
    regras = [
        ('R1 · Fiadas inteiras.', '15 fiadas inteiras desde o piso em todas as paredes (módulo 157 mm). O revestimento termina em 2.353 mm, com perfil; a faixa de 38 mm até o forro vai em pintura. Some a tira de 36 mm do R0.'),
        ('R2 · Eixo central.', 'Cada parede nasce do seu eixo. Fica o maior número de colunas inteiras em que a ponta ainda tem pelo menos 40% da peça (30 mm); as duas pontas recebem o mesmo corte.'),
        ('R3 · Vãos.', 'A porta existente não se move; a malha é recortada nela. O nicho é centrado na P1: com 13 colunas de largura, os dois lados caem exatamente nas juntas.'),
        ('R4 · Retorno estreito.', 'Na P6 (150 mm) a peça inteira fica na quina externa e o corte de 73 mm no canto interno.'),
        ('R5 · Acentos Nuage.', 'Mesma quantidade e região do R0, sempre em peça inteira (56 nas paredes e no nicho).'),
        ('R6 · Bancada.', 'Fiadas inteiras a partir da frente; cortes junto à parede e na ponta norte.'),
        ('R7 · Compra.', 'Área revestida × 1,10, por caixa fechada, e conferência contra as peças físicas.'),
    ]
    for h, b in regras:
        y = rich(c, xl, y, wl, h, b, 9.0, 5)
    y -= 6
    y = section(c, xl, y, 'Altura: por que parar em 2.353 mm', wl)
    para(c, xl, y, wl, 'Com 2.391 mm de parede e módulo de 157 mm, cabem 15 fiadas inteiras e sobram 36 mm. Revestir até o forro obriga uma fiada de 36 mm '
         'em todas as paredes (107 tiras, cerca de 27 peças a mais e +1 caixa). Parar na fiada 15 deixa todas as fiadas inteiras; o topo leva perfil e a faixa vai em pintura junto com o forro.', 9.0, 11.8)
    xr = MG + wl + 36; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Quadro R0 × R2 por parede', wr)
    rows = []
    for sid in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6'):
        r0 = R0S[sid]; r1 = RT[sid]
        rows.append([sid, '%s · %s' % (fm(r0['esq'], 1), fm(r0['dir'], 1)), fm(r0['topo'], 1), str(r0['frag']), str(r0['inteiras']),
                     ('%s · %s' % (fm(r1['c'], 1), fm(r1['c'], 1))) if sid != 'P6' else '73 · inteira', '—', str(r1['nb'] + r1['nn']), str(r1['full'])])
    rows.append({'cells': ['Total', '', '', str(sum(R0S[k]['frag'] for k in R0S)), str(sum(R0S[k]['inteiras'] for k in R0S)), '', '',
                           str(sum(RT[k]['nb'] + RT[k]['nn'] for k in R0S)), str(sum(RT[k]['full'] for k in R0S))], 'bold': True, 'fill': K08})
    yr = table(c, xr, yr, [40, 76, 54, 56, 52, 80, 44, 54, wr - 456], ['Parede', 'R0 pontas mm', 'R0 topo', 'R0 frag.', 'R0 int.', 'R2 pontas mm', 'R2 topo', 'R2 peças', 'R2 int.'],
               rows, size=8.4, pad=3.4, aligns=['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], bold_first=True, hsize=8.0)
    yr -= 14
    para(c, xr, yr, wr, 'O R0 conta mais peças inteiras em P1, P2, P4 e P5 porque ancorou a malha num canto: ganha uma coluna inteira por fiada, mas deixa um corte de 30 a 42 mm '
         'de um lado só, a tira de 36 mm no topo e recortes estreitos nos lados do nicho. A R2 troca essa coluna por duas pontas iguais e largas e elimina a tira do topo. '
         'Se preferir ancorar em canto nas paredes sem vão (P2 e P5), a troca é de 15 peças inteiras por parede: posso gerar essa variante.', 8.8, 11.4, 'S', K70)
    footer(c, 7, TOTAL)

def s08(c):
    header(c, 'Planificação das paredes',
           'As seis paredes abertas na ordem em que se dá a volta no banheiro, escala 1:25. As 15 fiadas atravessam todos os cantos na mesma altura.', 8, TOTAL)
    ox = MG + 70; oy = 330; x = ox
    for sid in CR.ORDEM:
        w = CR.WALLS[sid]
        draw_wall(c, x, oy, SC25, sid, chains='min', idx=(sid == 'P3'), nome=sid, tag=(w['nome'] if sid != 'P6' else None), name_dy=46, tags=False, vchain=(sid == 'P5'))
        x += w['W'] * SC25
    x = ox
    for sid in CR.ORDEM[:-1]:
        x += CR.WALLS[sid]['W'] * SC25
        line(c, x, oy - 10, x, oy + CR.H_ROOM * SC25 + 6, 1.6, K)
    legend_tiles(c, ox, oy - 34)
    y = oy - 60
    rows = []
    for sid in CR.ORDEM:
        r = RT[sid]
        rows.append([sid, r['nome'], fm(r['W']), ('%d inteiras + 2 × %s' % (r['n'], fm(r['c'], 1))) if sid != 'P6' else '1 inteira (quina) + 73',
                     fm(r['area'], 2), str(r['nb']), str(r['nn']), str(r['full']), str(r['cut'])])
    rows.append({'cells': ['Total', '', '', '', fm(sum(RT[k]['area'] for k in CR.ORDEM), 2), str(sum(RT[k]['nb'] for k in CR.ORDEM)),
                           str(sum(RT[k]['nn'] for k in CR.ORDEM)), str(sum(RT[k]['full'] for k in CR.ORDEM)), str(sum(RT[k]['cut'] for k in CR.ORDEM))], 'bold': True, 'fill': K08})
    table(c, MG, y, [44, 190, 66, 176, 70, 70, 70, 70, 70], ['Parede', 'Superfície', 'Largura', 'Colunas por fiada', 'Área m²', 'Bleu', 'Nuage', 'Inteiras', 'Cortadas'],
          rows, size=8.6, pad=3.6, aligns=['l', 'l', 'r', 'l', 'r', 'r', 'r', 'r', 'r'], bold_first=True, hsize=8.4)
    xn = MG + 860; wn = PW - MG - xn
    yn = section(c, xn, y + 6, 'Leitura', wn)
    for h, b in [('Mesma altura.', 'Todas as juntas horizontais estão em 155 + 157 × k mm a partir do piso.'),
                 ('Pontas.', 'Cada parede tem o mesmo corte nas duas pontas; os cantos recebem selante.'),
                 ('Topo.', 'Linha contínua em 2.353 mm; acima, faixa de 38 mm em pintura.')]:
        yn = rich(c, xn, yn, wn, h, b, 8.8, 5)
    footer(c, 8, TOTAL)

SHEETS = [s01, s02, s03, s04, s05, s06, s07, s08]
