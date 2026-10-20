# -*- coding: utf-8 -*-
import math
from lib import *
import engine as E
import calc as C
from draw import *
from sheets_a import TOTAL, A, B, TA, TB, pct

AREA_LIQ = TA['area']                      # 17,94 m²

def lista_corte(opt):
    """Agrupa as peças cortadas por dimensão."""
    a, b = opt['a'], opt['b']
    grp = {}
    for nm in C.ORDEM:
        w = C.WALLS[nm]
        hp, vp, xs, ys, pcs = C.wall_pieces(w, opt)
        for p in pcs:
            if p['rem']: continue
            ww = p['x1'] - p['x0']; hh = p['y1'] - p['y0']
            kind = None
            if p['part']:
                o = p['part']
                full_h = o[2] <= p['y0'] + 1e-6 and o[3] >= p['y1'] - 1e-6
                full_w = o[0] <= p['x0'] + 1e-6 and o[1] >= p['x1'] - 1e-6
                if full_h:
                    ww = ww - (o[1] - o[0]); kind = 'Batente do vão'
                elif full_w:
                    hh = hh - (o[3] - o[2]); kind = 'Cabeça do vão'
                else:
                    kind = 'Canto do vão (L)'
                    ww = ww; hh = hh
            else:
                tx = p['tx']; ty = p['ty']
                if tx == 'f' and ty == 'f': continue
                kind = 'Ponta' if (tx == 'c' and ty == 'f') else ('Fiada de piso ou topo' if (ty == 'c' and tx == 'f') else 'Canto da malha')
            key = (kind, round(ww, 2), round(hh, 2))
            g = grp.setdefault(key, dict(n=0, walls=set()))
            g['n'] += 1; g['walls'].add(nm.capitalize())
    rows = []
    order = {'Ponta': 0, 'Fiada de piso ou topo': 1, 'Canto da malha': 2, 'Batente do vão': 3, 'Cabeça do vão': 4, 'Canto do vão (L)': 5}
    for (kind, ww, hh), g in sorted(grp.items(), key=lambda kv: (order[kv[0][0]], -kv[0][1], -kv[0][2])):
        rows.append([kind, '%s × %s' % (fx(ww, 2), fx(hh, 2)), str(g['n']), ', '.join(sorted(g['walls']))])
    return rows

def juntas_m(opt):
    tot = 0.0
    for nm in C.ORDEM:
        w = C.WALLS[nm]; hp, vp = C.plan(w['W'], w['H'], opt)
        nx = hp['n'] + 2; ny = vp['n'] + 2
        tot += ((nx - 1) * w['H'] + (ny - 1) * w['W']) / 100.0
    return tot

def s12(c):
    header(c, 'Quantitativo, lista de corte e consumíveis',
           'Quantidades das quatro paredes do banheiro (17,94 m² líquidos, vão da porta descontado), nas duas opções. A caixa usada é a do produto, não a de 1,44 m² dos arquivos recebidos. '
           'A parede de 358 × 260 cm fica de fora.', 12, TOTAL)
    xl = MG; wl = 560
    y = section(c, xl, PH - 130, 'Peças por parede', wl)
    rows = []
    for nm in C.ORDEM:
        qa = TA['rows'][nm]; qb = TB['rows'][nm]
        rows.append([nm, f(qa['area'], 2), str(qa['phys']), str(qa['ops']), str(qb['phys']), str(qb['ops'])])
    rows.append({'cells': ['Total', f(TA['area'], 2), str(TA['phys']), str(TA['ops']), str(TB['phys']), str(TB['ops'])], 'bold': True, 'fill': K08})
    y = table(c, xl, y, [90, 80, 100, 90, 100, wl - 460], ['Parede', 'Área líquida m²', 'A · peças físicas', 'A · cortes', 'B · peças físicas', 'B · cortes'], rows,
              size=9.0, pad=4, aligns=['l', 'r', 'r', 'r', 'r', 'r'], bold_first=True)
    y -= 22
    y = section(c, xl, y, 'Compra, com a caixa do produto', wl)
    rows = [
        ['Peças físicas (as duas pontas da opção B nas paredes de 2,64 m saem de uma peça só)', str(TA['phys']), str(TB['phys'])],
        ['Reserva de 10% (quebra, reposição)', str(TA['need']), str(TB['need'])],
        ['Peças por caixa', '36', '26'],
        ['m² por caixa', '0,87', '0,30'],
        {'cells': ['Caixas a comprar', str(TA['caixas']), str(TB['caixas'])], 'bold': True, 'fill': CIANO18},
        ['Peças compradas', str(TA['pcs_comprados']), str(TB['pcs_comprados'])],
        ['m² comprados (líquido 17,94)', fx(TA['m2_comprado'], 2), fx(TB['m2_comprado'], 2)],
        ['Metros de junta (aprox., sem descontar o vão)', f(juntas_m(A), 0) + ' m', f(juntas_m(B), 0) + ' m'],
        ['Menor corte da malha', '8,15 cm (53%)', '3,65 cm (49%)'],
    ]
    y = table(c, xl, y, [370, 95, 95], ['', 'Opção A · 15,5 × 15,5', 'Opção B · 7,5 × 15,5'], rows, size=9.0, pad=4, aligns=['l', 'r', 'r'], hsize=8.6)
    y -= 22
    y = section(c, xl, y, 'O que os PDFs recebidos mandavam comprar', wl)
    rows = [
        ['Norte e Sul · 7×15', '304 + 10% = 335', 'sem resultado', '13'],
        ['Norte e Sul · 15×15', '176', '3', '5'],
        ['Leste e Oeste · 7×15', '599', '5', '24'],
        ['Leste e Oeste · 15×15', '317', '6', '9'],
        ['Leste · 15×15 (358 × 260)', '431', '8', '12'],
    ]
    table(c, xl, y, [190, 150, 110, wl - 450], ['Arquivo', 'Peças com 10%', 'Caixas no PDF (1,44 m²)', 'Caixas reais'], rows, size=8.8, pad=3.6,
          aligns=['l', 'r', 'r', 'r'], hsize=8.2)
    # lista de corte
    xr = MG + 600; wr = PW - MG - xr; wc = (wr - 24) / 2
    yr = section(c, xr, PH - 130, 'Lista de corte · opção A', wc)
    ra = lista_corte(A)
    yA = table(c, xr, yr, [90, 62, 28, wc - 180], ['Corte', 'L × A cm', 'Qtd', 'Paredes'], ra, size=8.0, pad=3.0, aligns=['l', 'r', 'r', 'l'], hsize=7.2)
    xr2 = xr + wc + 24
    yr = section(c, xr2, PH - 130, 'Lista de corte · opção B', wc)
    rb = lista_corte(B)
    yB = table(c, xr2, yr, [90, 62, 28, wc - 180], ['Corte', 'L × A cm', 'Qtd', 'Paredes'], rb, size=8.0, pad=3.0, aligns=['l', 'r', 'r', 'l'], hsize=7.2)
    ylow = min(yA, yB) - 8
    para(c, xr, ylow, wr, 'Os cortes de ponta da opção B vêm em pares: cada peça de 7,5 cm é partida ao meio e as duas metades de 3,65 cm vão para as pontas esquerda e direita da mesma fiada. '
         'A lista conta as metades. Em A, cada corte consome uma peça.', 7.8, 10.2, 'S', K70)
    # consumíveis
    ycs = ylow - 44
    ycs = section(c, xr, ycs, 'Consumíveis · estimativas para confirmar com os fornecedores', wr)
    rej = lambda L, Cc: ((L + Cc) / (L * Cc)) * 9 * 3 * 1.9
    ra_ = rej(155, 155); rb_ = rej(75, 155)
    arg = 5.0 * AREA_LIQ * 1.15
    rows = [
        ['Argamassa colante ACII (ACIII se a ficha pedir)', '5,0 kg/m² com dentada de 6 mm, +15%', '%s kg · %d sacos de 20 kg' % (f(arg, 0), math.ceil(arg / 20)), 'igual à A'],
        ['Rejunte (tipo e cor a definir)', 'peça 155×155 / 75×155, 9 mm, junta 3 mm, densidade 1,9, +15%',
         '%s kg/m² · %s kg' % (fx(ra_, 2), f(ra_ * AREA_LIQ * 1.15, 1)), '%s kg/m² · %s kg' % (fx(rb_, 2), f(rb_ * AREA_LIQ * 1.15, 1))],
        ['Espaçadores de 3 mm', 'cerca de 1 por peça física', '%d un' % TA['phys'], '%d un' % TB['phys']],
        ['Selante de movimentação 6 × 6 mm', '4 cantos de 2,40 m + topo (8,14 m) + pé sem o vão (7,34 m) = 25 m', '4 cartuchos de 280 mL', 'igual à A'],
        ['Disco diamantado e corte úmido', 'um disco por parede é o usual', '%d cortes' % TA['ops'], '%d cortes' % TB['ops']],
        ['Peças de acabamento da linha', 'quinas e cantoneiras: a levantar com a Portobello', 'a definir', 'a definir'],
    ]
    table(c, xr, ycs, [150, 190, 100, wr - 440], ['Item', 'Base', 'Opção A', 'Opção B'], rows, size=7.6, pad=3, hsize=7.4)
    footer(c, 12, TOTAL)

def s13(c):
    header(c, 'Escopo de serviços',
           'O que o assentador e a obra precisam fazer para o revestimento de parede do banheiro, na ordem em que acontece. Os IDs D, R, C e P são os do caderno MaxHaus; '
           'os RV são novos e cobrem só o revestimento.', 13, TOTAL)
    y = PH - 130
    W = [44, 108, 396, 88, 138, 316]
    head = ['ID', 'Serviço', 'O que inclui', 'Quantidade', 'Depois de', 'Aceite']
    R = lambda *a: list(a)
    rows = [
        R('RV00', 'Medida de obra', 'Medir largura (em três alturas), altura (em três posições), prumo e esquadro das quatro paredes, com o emboço pronto e a cota do piso acabado marcada. Refazer a paginação (Prancha 15) se a largura mudar mais de 5 mm ou a altura mais de 10 mm.', '4 paredes', 'R02 emboçada · D04 · cota P05', 'Planilha de medidas assinada; paginação confirmada ou refeita.'),
        R('RV01', 'Substrato', 'Remover resíduos de D04, chapisco e emboço regularizado nas paredes existentes e na R02, com cura pelo prazo do fornecedor da argamassa. Planeza conferida com régua de 2 m.', '17,94 m² + vão', 'D04 · R02', 'Sem fissura nem pó; planeza conferida e registrada.'),
        R('RV02', 'Interface com a impermeabilização do box', 'Subida da impermeabilização nas paredes do box na altura definida no projeto de impermeabilização e ensaio de estanqueidade antes de revestir. Hoje o caderno só cobre o piso (C1).', 'box · 7,90 m²', 'RV01 · C1', 'Ensaio aprovado por escrito. ALTURA A DECIDIR (Prancha 16).'),
        R('RV03', 'Marcação', 'Eixo de cada parede, linha de piso (cota P05) e linha de forro (R03) com nível a laser, esquadro 3-4-5 nos cantos e régua de modulação com as marcas das Pranchas 06/07 ou 09/10. As fiadas atravessam os cantos na mesma altura.', '4 paredes', 'RV00', 'Marcas conferidas contra as pranchas; fiadas iguais nos cantos.'),
        R('RV04', 'Corte das peças', 'Cortar na bancada, com disco diamantado e água, todas as pontas, fiadas de piso e topo e recortes do vão; numerar e estocar por parede conforme a lista da Prancha 12.', 'A: %d cortes · B: %d' % (TA['ops'], TB['ops']), 'RV03', 'Peças conferidas contra a lista; fiadas de piso e topo 3 a 5 mm menores.'),
        R('RV05', 'Assentamento', 'Argamassa colante ACII (ACIII se a ficha do produto pedir), dentada de 6 mm, colagem simples, espaçadores de 3 mm. Abrir a partir do eixo, da fiada F2 para cima, com régua apoiada na linha de nível; as pontas e a fiada F1 por último. Misturar caixas (variação V4).', '17,94 m²', 'RV03 · RV04', 'Juntas alinhadas, sem degrau perceptível com luz rasante, colagem sem vazios.'),
        R('RV06', 'Recortes de pontos', 'Marcar T17, S03, registros e chuveiro sobre a malha antes de assentar. Furar com serra-copo diamantada. Centro da peça ou junta.', 'a definir', 'RV03 · projetos de elétrica e hidráulica', 'Pontos no centro de peça ou na junta; borda sem lasca.'),
        R('RV07', 'Peças de acabamento', 'Cantoneiras ou peças de quina da linha nas quinas vivas: retorno do batente da P02 e, se houver, topo do box.', 'a levantar', 'RV05', 'Nenhuma aresta cortada exposta.'),
        R('RV08', 'Juntas de movimentação', 'Selante elástico de 6 × 6 mm (poliuretano ou silicone neutro) nos quatro cantos internos, no encontro com o forro e com o piso, e na soleira, sem rejunte rígido atrás.', '≈ 25 m', 'RV05', 'Selante contínuo, sem bolha, rente à peça.'),
        R('RV09', 'Rejuntamento', 'Depois da cura da argamassa e com as juntas de movimentação limpas. Tipo e cor a definir (box: acrílico ou epóxi). Teste de cor em área pequena. Limpar o excesso na hora.', '17,94 m²', 'RV05 · RV08', 'Junta cheia e uniforme, sem manchas.'),
        R('RV10', 'Limpeza e proteção', 'Limpeza final e proteção do revestimento até a instalação de louças, do vidro K01 e do forro R03.', '4 paredes', 'RV09', 'Revestimento sem riscos até a entrega.'),
        R('RV11', 'Recebimento', 'Checklist da Prancha 14, fotos por parede, registro do lote e da tonalidade, entrega das peças de reposição identificadas.', '4 paredes', 'RV10', 'Termo de aceite assinado.'),
    ]
    y = table(c, MG, y, W, head, rows, size=9.4, pad=4.2, hsize=9.0, bold_first=True)
    y -= 24
    cw = (PW - 2 * MG - 28) / 2
    ya = section(c, MG, y, 'Fora deste escopo, mas com interface', cw)
    ya = para(c, MG, ya, cw, 'Impermeabilização do piso e rodapé virado (C1) · regularização com caimento (C2) · ralo linear (C3) · piso (C4) · soleira (C5) · porta P02 · forro novo R03 · '
              'vidro K01 · louças e metais · pontos elétricos e hidráulicos. Cada um pede data e responsável na ordem de execução.', 9.0, 12)
    yb = section(c, MG + cw + 28, y, 'Condições', cw)
    yb = para(c, MG + cw + 28, yb, cw, 'Quantidades da opção A ou B dependem da escolha do cliente. Alterações de escopo somente por escrito. Durações e prazos ficam em branco para a contratada preencher. '
              'Normas citadas para conferência na versão vigente: NBR 13754 (revestimento interno de parede com placas cerâmicas) e NBR 14081 (argamassa colante).', 9.0, 12)
    footer(c, 13, TOTAL)

def s14(c):
    header(c, 'Execução: sequência, pontos de parada e aceite',
           'A ordem em que o revestimento é feito. Os pontos de parada não passam sem aceite por escrito. Os critérios de aceite são propostos para este projeto e '
           'valem junto com a norma vigente e a ficha do fabricante.', 14, TOTAL)
    xl = MG; wl = 540
    y = section(c, xl, PH - 130, 'Sequência recomendada', wl)
    passos = [
        ('1', 'Fechar as pendências críticas da Prancha 16 e medir as paredes (RV00).', False),
        ('', 'PARADA 1 · aceite das medidas; paginação confirmada ou refeita.', True),
        ('2', 'Substrato pronto e curado (RV01). Impermeabilização do box e ensaio de estanqueidade (RV02).', False),
        ('', 'PARADA 2 · ensaio de estanqueidade aprovado.', True),
        ('3', 'Mock-up de 3 × 3 peças numa parede: junta, rejunte, cor e brilho.', False),
        ('', 'PARADA 3 · cliente aprova o mock-up.', True),
        ('4', 'Marcar as quatro paredes (RV03): nível a laser, eixos, linhas de piso e de forro, régua de modulação.', False),
        ('5', 'Cortar e numerar as peças (RV04).', False),
        ('6', 'Assentar parede por parede a partir do eixo, da F2 para cima. Pontas e fiada de topo (F16) depois; fiada de piso (F1) por último, depois do piso acabado.', False),
        ('', 'PARADA 4 · antes do rejunte: alinhamento, planeza, som cavo e pontos conferidos.', True),
        ('7', 'Selante de movimentação (RV08), depois rejunte (RV09).', False),
        ('8', 'Limpeza, proteção e recebimento (RV10 e RV11).', False),
        ('', 'PARADA 5 · recebimento com checklist e fotos.', True),
    ]
    for n, t, stop in passos:
        h = 15 if len(t) < 80 else 28
        if stop:
            rect(c, xl + 24, y - h - 2, wl - 24, h + 2, AMARELO45, K, 0.6)
            para(c, xl + 30, y - 2, wl - 36, t, 10.2, 12.5, 'S-B')
            y -= h + 10
        else:
            txt(c, xl, y - 12, n, 12, 'S-B')
            y = para(c, xl + 24, y - 2, wl - 24, t, 10.4, 13.2) - 10
    xr = MG + wl + 40; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Critérios de aceite propostos', wr)
    rows = [
        ['Juntas verticais', 'fio de prumo no eixo e a cada 1 m', 'sem desvio visível; pontas iguais nos dois lados, dentro de ±2 mm'],
        ['Fiadas nos cantos', 'régua nivelada atravessando o canto', 'a junta horizontal passa de uma parede à outra sem salto'],
        ['Corte das pontas', 'trena', 'igual nos dois lados e dentro de ±2 mm da prancha'],
        ['Planeza', 'régua de 2 m', 'sem ondulação perceptível; tolerância da norma vigente'],
        ['Degrau entre peças', 'luz rasante e ponta do dedo', 'sem degrau perceptível'],
        ['Largura da junta', 'espaçador', '3,0 mm (2,7 mm na opção B, paredes de 2,64 m), variação até ±0,5 mm'],
        ['Colagem', 'percussão com cabo de espátula', 'sem som cavo; bordas e cantos com cobertura completa'],
        ['Pontos', 'trena', 'no centro da peça ou na junta, nunca a 1 cm dela'],
        ['Tonalidade', 'luz natural, caixas misturadas', 'sem mancha por caixa ou lote'],
        ['Selante', 'visual', 'contínuo, sem bolha, rente'],
    ]
    yr = table(c, xr, yr, [112, 150, wr - 262], ['Item', 'Como medir', 'Aceite'], rows, size=9.4, pad=4.0, bold_first=True, hsize=9.2)
    yr -= 24
    yr = section(c, xr, yr, 'Como marcar a malha', wr)
    for h, b in [
        ('Eixo.', 'Marque o eixo de cada parede com linha de giz e confira com o esquadro nos cantos.'),
        ('Nível.', 'Transfira a linha do piso acabado e a do forro com o laser. A régua de modulação começa no piso: as marcas estão nas Pranchas 06, 07, 09 e 10.'),
        ('Referência.', 'Use a linha de 1,00 m acima do piso como conferência. Ela tem de passar pela mesma fiada nas quatro paredes.'),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 10.0, 6)
    footer(c, 14, TOTAL)

def pocket(c, x, y, wtab, titulo, W0, a, jm, wcols=None):
    """Tabela de bolso: corte em função da largura medida."""
    y = section(c, x, y, titulo, wtab)
    rows = []
    for dW in (-1.0, -0.5, 0.0, 0.5, 1.0):
        W_ = W0 + dW
        p = E.plan_axis(W_, a, 0.25, 0.35, jnom=jm)
        half_j = p['jh'] * 10
        cell = ['%s' % fx(W_, 1), str(p['n']), fx(p['c'], 2), pct(p['c'], a), fx(p['j'] * 10, 1), p['mode'] == 'meia' and 'meia peça' or 'junta nominal']
        rows.append({'cells': cell, 'fill': CIANO18} if dW == 0 else cell)
    return table(c, x, y, [40, 26, 44, 34, 46, wtab - 190], ['L (cm)', 'n', 'Corte', '%', 'Junta mm', 'Modo'], rows, size=8.0, pad=2.8,
                 aligns=['r', 'r', 'r', 'r', 'r', 'l'], hsize=7.6, zebra=False)

def s15(c):
    header(c, 'Recálculo com a medida real e detalhes de encontro',
           'As cotas desta emissão vêm de arquivos e de um scan. Com o emboço pronto, meça de novo e refaça a conta. Uma variação de 1 cm na largura mexe 5 mm em cada corte de ponta.', 15, TOTAL)
    xl = MG; wl = 520
    y = section(c, xl, PH - 130, 'Como refazer a paginação', wl)
    passos = [
        ('Medir.', 'Largura em três alturas (rodapé, meio, forro) e use a MENOR. Altura do piso acabado ao forro em três pontos, também a menor.'),
        ('Escolher n.', 'n é o número de peças inteiras por fiada. Corte de cada ponta: c = (L − n × peça − (n + 1) × junta) ÷ 2. Fica com a maior quantidade de inteiras em que c ainda seja de pelo menos 40% da peça.'),
        ('Meia peça.', 'Para ter c = (peça − 0,2) ÷ 2, ajuste a junta entre colunas: j = (L − n × peça − (peça − 0,2)) ÷ (n + 1). Aceite se j ficar entre 2,5 e 3,5 mm. Fora disso, volte à junta de 3,0 mm.'),
        ('Fiadas.', 'Mesma conta na vertical, com a peça de 15,5 cm e junta fixa de 3,0 mm, para as quatro paredes fecharem nos cantos.'),
        ('Conferir.', 'Cortes iguais nos dois lados, nada abaixo de 1/3 da peça, fiadas iguais nas quatro paredes. Refazer o Paginador com os novos valores e emitir a revisão.'),
    ]
    for i, (h, b) in enumerate(passos, 1):
        txt(c, xl, y - 12, str(i), 12, 'S-B')
        y = rich(c, xl + 20, y - 2, wl - 20, h, b, 9.2, 5)
    y -= 14
    yt = section(c, xl, y, 'Tabelas de bolso · corte em função da largura medida', wl)
    colw = (wl - 20) / 2
    y1 = pocket(c, xl, yt, colw, 'A · parede de 1,43 m', 143, 15.5, 0.3)
    y2 = pocket(c, xl + colw + 20, yt, colw, 'A · parede de 2,64 m', 264, 15.5, 0.3)
    yy = min(y1, y2) - 14
    y3 = pocket(c, xl, yy, colw, 'B · parede de 1,43 m', 143, 7.5, 0.3)
    y4 = pocket(c, xl + colw + 20, yy, colw, 'B · parede de 2,64 m', 264, 7.5, 0.3)
    # detalhes
    xr = MG + wl + 50; wr = PW - MG - xr
    FIADAS = True
    yr = section(c, xr, PH - 130, 'Detalhes de encontro · esquemas sem escala', wr)
    # D1 canto interno (planta)
    y0 = yr - 12
    txt(c, xr, y0, 'D1 · canto interno (planta)', 9, 'S-B')
    bx, by = xr + 20, y0 - 118
    # paredes: L invertido
    wall = HexColor('#d9d9d9')
    rect(c, bx, by, 14, 100, wall, K, 0.6)
    rect(c, bx, by + 86, 120, 14, wall, K, 0.6)
    rect(c, bx + 14, by, 4, 86, white, K, 0.5); rect(c, bx + 14, by + 82, 106, 4, white, K, 0.5)
    rect(c, bx + 18, by, 6, 82, CIANO18, K, 0.5); rect(c, bx + 24, by + 76, 96, 6, CIANO18, K, 0.5)
    rect(c, bx + 18, by + 76, 6, 6, AMARELO, K, 0.6)
    para(c, bx + 150, by + 100, wr - 190, 'Canto interno: as peças de ponta das duas paredes não se tocam. Folga de 3 a 5 mm preenchida com selante elástico (amarelo), sem rejunte rígido atrás.', 8.6, 11)
    # D2 forro (corte)
    y1_ = by - 28
    txt(c, xr, y1_, 'D2 · topo, encontro com o forro (corte)', 9, 'S-B')
    bx, by2 = xr + 20, y1_ - 138
    rect(c, bx, by2, 16, 130, wall, K, 0.6)
    rect(c, bx + 16, by2, 4, 100, white, K, 0.5)
    rect(c, bx + 20, by2, 9, 100, CIANO18, K, 0.5)
    rect(c, bx + 20, by2 + 100, 9, 4, AMARELO, K, 0.6)
    rect(c, bx - 10, by2 + 104, 130, 14, HexColor('#f0f0f0'), K, 0.6)
    txt(c, bx + 40, by2 + 108, 'forro novo R03 (2,40 m)', 7.6)
    txt(c, bx + 34, by2 + 50, 'F16', 7.6, 'S-B')
    para(c, bx + 150, by2 + 118, wr - 190, 'A fiada de topo (F16, 9,25 cm) termina 3 a 5 mm abaixo do forro; o vão é selado. Medir a cota real do forro antes de cortar a fiada.', 8.6, 11)
    # D3 pé
    y2_ = by2 - 28
    txt(c, xr, y2_, 'D3 · pé da parede e soleira (corte)', 9, 'S-B')
    bx, by3 = xr + 20, y2_ - 122
    rect(c, bx, by3 + 40, 16, 70, wall, K, 0.6)
    rect(c, bx + 16, by3 + 40, 4, 70, white, K, 0.5)
    rect(c, bx + 20, by3 + 44, 9, 66, CIANO18, K, 0.5)
    rect(c, bx + 20, by3 + 40, 9, 4, AMARELO, K, 0.6)
    rect(c, bx + 20, by3, 110, 36, HexColor('#ededed'), K, 0.6)
    rect(c, bx + 20, by3 + 36, 110, 4, white, K, 0.5)
    rect(c, bx + 29, by3 + 36, 101, 8, HexColor('#cfcfcf'), K, 0.5)
    txt(c, bx + 60, by3 + 18, 'laje · caimento · C1', 7.6)
    txt(c, bx + 70, by3 + 38, 'piso C4', 7.4)
    txt(c, bx + 34, by3 + 80, 'F1', 7.6, 'S-B')
    para(c, bx + 150, by3 + 112, wr - 190, 'A fiada de piso (F1, 9,25 cm) é a última a entrar, depois do piso acabado, com 3 a 5 mm de folga selada. Na soleira da P02 a junta de material é a C5, sem degrau.', 8.6, 11)
    yfi = section(c, xr, by3 - 26, 'Fiadas · altura medida (peça de 15,5 cm, junta de 3,0 mm)', wr)
    rows = []
    for H_ in (238.0, 239.0, 240.0, 241.0, 242.0):
        p = E.plan_axis(H_, 15.5, 0.3, 0.3)
        cell = [fx(H_, 1), str(p['n']), fx(p['c'], 2), pct(p['c'], 15.5)]
        rows.append({'cells': cell, 'fill': CIANO18} if H_ == 240 else cell)
    table(c, xr, yfi, [70, 50, 80, 60], ['H (cm)', 'n', 'Corte', '%'], rows, size=8.0, pad=2.6, aligns=['r', 'r', 'r', 'r'], hsize=7.6, zebra=False)
    footer(c, 15, TOTAL)

def s16(c):
    header(c, 'Pendências e decisões',
           'O que precisa ser respondido antes de cortar e comprar. As quatro críticas mudam número de peças, caixas ou a própria paginação.', 16, TOTAL)
    y = PH - 130
    W = [24, 250, 296, 130, 292, 70]
    head = ['#', 'Pendência', 'Por que trava', 'Quem decide', 'Efeito na paginação', 'Peso']
    CR = 'Crítica'; IM = 'Importante'; ME = 'Menor'
    rows = [
        ['1', 'Confirmar o produto: "Bouché" existe na Portobello? Pedir a ficha técnica.', 'As quantidades usam dados da linha Gouache de mesmo formato (36 e 26 peças por caixa, borda Bold, 9 mm). Formato real, borda, junta mínima e peças especiais podem ser outros.', 'Cliente e arquiteto, com a Portobello Shop', 'Pode mudar formato, caixa, junta e todos os números das Pranchas 5 a 12.', CR],
        ['2', 'Que parede é a Leste de 358 × 260 cm?', 'Há duas Lestes no projeto (264 × 240 e 358 × 260) e a altura de 2,60 m não bate com o forro a 2,40 m.', 'Arquiteto', 'Entra ou não no total. Prancha 11 pronta nas duas opções.', CR],
        ['3', 'Medir as paredes com o emboço pronto.', 'As cotas 143 × 264 vêm de arquivos e de scan (±1 cm).', 'Obra', 'Recálculo pela Prancha 15; pontas mudam 5 mm por centímetro.', CR],
        ['4', 'Cota do piso acabado (P05) e do forro novo (R03).', 'As fiadas de piso e de topo (9,25 cm) saem da altura de 2,40 m entre os dois.', 'Obra e arquiteto', 'Se a altura mudar, as fiadas mudam; as quatro paredes mudam juntas.', CR],
        ['5', 'Escolher a opção A (15,5 × 15,5) ou B (7,5 × 15,5).', 'A tem %d caixas e 8,15 cm de menor corte; B tem %d caixas, o dobro de juntas e menor corte de 3,65 cm.' % (TA['caixas'], TB['caixas']), 'Cliente', 'Define as Pranchas 5 a 10 que valem.', IM],
        ['6', 'Validar a junta de 3 mm em mock-up.', 'A ficha da linha de mesmo formato indica 1,5 mm; o anúncio de outra peça Portobello de borda Bold fala em mais de 2 mm.', 'Cliente e assentador', 'Entre 2,5 e 3,5 mm a simetria se mantém. Fora disso, recalcular.', IM],
        ['7', 'Altura da impermeabilização nas paredes do box.', 'C1 cobre o piso e o rodapé virado; as paredes do box (7,90 m²) vão até 2,40 m.', 'Arquiteto e impermeabilizador', 'Não muda a malha; muda o prazo e o escopo (RV02).', IM],
        ['8', 'Posição final do batente da P02.', 'A posição vem do vetor do scan (±2 cm). Na opção B os cortes de batente têm 2,7 e 2,5 cm.', 'Obra', 'Pode estreitar ou alargar os cortes de batente (Pranchas 7 e 10).', IM],
        ['9', 'Vidro K01: manter (A) ou trocar (B, perfis na parede antes do revestimento).', 'Perfil e fixação entram no revestimento. Na opção A de peça o vidro cai sobre uma junta.', 'Cliente', 'Define onde ficam furos e perfis.', IM],
        ['10', 'Posição final de T17, S03, registros, chuveiro e ducha.', 'Recortes precisam estar na malha antes de assentar.', 'Elétrica e hidráulica', 'Cada ponto vai para o centro de uma peça ou para a junta.', IM],
        ['11', 'Rejunte: tipo e cor (box: acrílico ou epóxi).', 'Define consumo e acabamento.', 'Cliente', 'Nenhum na malha.', ME],
        ['12', 'Peças de acabamento: quinas e cantoneiras.', 'Retorno do batente e topo do box.', 'Cliente', 'Soma ao pedido.', ME],
        ['13', 'Lote único e reposição.', 'Variação visual V4 (grande). Reserva de 10% a validar.', 'Compras', 'Caixas e reposição guardada.', ME],
    ]
    rows2 = []
    for r in rows:
        if r[5] == CR: rows2.append({'cells': r, 'fill': MAGENTA12})
        else: rows2.append(r)
    y = table(c, MG, y, W, head, rows2, size=9.6, pad=4.4, hsize=9.2, zebra=False, bold_first=False)
    y -= 20
    para(c, MG, y, PW - 2 * MG, 'Quando as quatro críticas estiverem fechadas, a emissão passa a REV. 01 e vale para corte e compra. O Paginador de Revestimentos atualizado (cortes iguais nas duas pontas e caixa do produto) refaz tudo em segundos.', 9.6, 12.6)
    footer(c, 16, TOTAL, 'Emissão para conferência em obra. Linhas em rosa são as pendências críticas.')

SHEETS = [s12, s13, s14, s15, s16]
