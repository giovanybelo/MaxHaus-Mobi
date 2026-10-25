# -*- coding: utf-8 -*-
import math
from lib import *
import calc_r1 as CR
from draw_r1 import *
from s_r1a import TOTAL, RT, RES, ROWS_T, BUD, brl, fm, N_PCS, N_FULL, N_CUT

def s15(c):
    header(c, 'Quantitativo e compra',
           'Quantidades da paginação R1 e compra dos revestimentos por área revestida + 10%, arredondada para caixa fechada (0,30 m² / 26 peças) e conferida contra as peças físicas.', 15, TOTAL)
    xl = MG; wl = 600
    y = section(c, xl, PH - 130, 'Por superfície', wl)
    rows = []
    for r in ROWS_T:
        rows.append([r['id'], r['nome'], '%s × %s' % (fm(r['W']), fm(r['H'])), fm(r['area'], 3), str(r['nb']), str(r['nn']), str(r['full']), str(r['cut'])])
    rows.append({'cells': ['Total', '', '', fm(sum(r['area'] for r in ROWS_T), 3), str(sum(r['nb'] for r in ROWS_T)), str(sum(r['nn'] for r in ROWS_T)),
                           str(N_FULL), str(N_CUT)], 'bold': True, 'fill': K08})
    table(c, xl, y, [34, 170, 92, 62, 58, 58, 64, 62], ['', 'Superfície', 'L × A mm', 'Área m²', 'Bleu', 'Nuage', 'Inteiras', 'Cortadas'], rows,
          size=8.2, pad=2.9, aligns=['l', 'l', 'r', 'r', 'r', 'r', 'r', 'r'], bold_first=True, hsize=8.0)
    xr = xl + wl + 36; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Compra', wr)
    B, N = RES['B'], RES['N']
    rows = [
        ['Área revestida', fm(B['area'], 2) + ' m²', fm(N['area'], 2) + ' m²'],
        ['Reserva', '10%', '10%'],
        ['m² de compra', fm(B['m2_compra'], 2), fm(N['m2_compra'], 2)],
        {'cells': ['Caixas', str(B['caixas']), str(N['caixas'])], 'bold': True, 'fill': CIANO18},
        ['Peças compradas', str(B['pcs_compradas']), str(N['pcs_compradas'])],
        ['Peças físicas da paginação', str(B['pcs_fisicas']), str(N['pcs_fisicas'])],
        ['Folga sobre as peças físicas', '%d%%' % round(B['folga'] * 100), '%d%%' % round(N['folga'] * 100)],
        ['R0 / R1 (peça cortada + 10%)', '70 caixas', '7 caixas'],
    ]
    yr = table(c, xr, yr, [wr - 180, 90, 90], ['', 'Bleu Nuit', 'Nuage'], rows, size=8.8, pad=3.6, aligns=['l', 'r', 'r'], bold_first=True, hsize=8.6)
    yr -= 18
    yr = section(c, xr, yr, 'Leitura', wr)
    for h, b in [
        ('Área + 10% cobre a obra.', 'Como quase nada se perde em corte, a compra pela área já deixa %d%% de peças sobrando no Bleu e %d%% no Nuage depois de todos os cortes.' % (round(B['folga'] * 100), round(N['folga'] * 100))),
        ('Nuage.', 'A área do Nuage soma os 56 acentos (peça 75 × 155) e o tampo com as bordas da bancada.'),
        ('Alternativa até o forro.', 'Revestir até 2.391 mm soma 0,31 m² de Bleu e 107 tiras de 36 mm (cerca de 27 peças): 64 caixas em vez de 63.'),
        ('Lote.', 'Comprar tudo de um lote só e misturar as caixas no assentamento. Guardar uma caixa de cada cor para reposição.'),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 9.0, 5)
    footer(c, 15, TOTAL)

def s16(c):
    header(c, 'Orçamento R2',
           'Materiais e peças do banheiro, valores em R$ em 25/10/2026, sem frete. Planilha Orcamento_Banheiro_R2.xlsx com memória de cálculo, sobreposições e comparação com a proposta Portobello.', 16, TOTAL)
    xl = MG; wl = 420
    y = section(c, xl, PH - 130, 'Resumo', wl)
    rows = [[k, brl(v)] for k, v in BUD['cats']]
    rows.append({'cells': ['Subtotal', brl(BUD['subtotal'])], 'bold': True, 'fill': K08})
    rows.append(['Contingência 15% (à parte)', brl(BUD['cont'])])
    rows.append({'cells': ['Total com contingência', brl(BUD['total'])], 'bold': True, 'fill': CIANO18})
    y = table(c, xl, y, [wl - 120, 120], ['Categoria', 'Total'], rows, size=9.2, pad=4, aligns=['l', 'r'], hsize=9.0)
    y -= 20
    y = section(c, xl, y, 'R1 → R2', wl)
    rr = []
    for a, b1, b2, d, why in BUD['rev']:
        money = 'R$' in a
        f_ = (lambda v: brl(float(v))) if money else (lambda v: '%d' % round(float(v)))
        rr.append([a.replace(', R$', ''), f_(b1), f_(b2), f_(d)])
    y = table(c, xl, y, [150, 90, 90, wl - 330], ['Item', 'R1', 'R2', 'Diferença'], rr, size=8.4, pad=3.2, aligns=['l', 'r', 'r', 'r'], hsize=8.2)
    y -= 14
    para(c, xl, y, wl, 'Fora do orçamento: piso Monofloor Everest, elétrica e iluminação, mão de obra, argamassa colante (empreiteira), logística e pintura da faixa de 38 mm.', 8.6, 11.2, 'S', K70)
    xr = xl + wl + 36; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Revestimentos e impermeabilização', wr)
    rows = []
    for it in BUD['itens']:
        if it[0] in ('Revestimentos', 'Impermeabilização'):
            q = it[3] if it[3] is not None else 0
            rows.append([it[1], it[2], fm(float(q), 0) if float(q) == int(float(q)) else fm(float(q), 2), brl(float(it[4])), brl(float(it[5])), it[6]])
    yr = table(c, xr, yr, [wr - 330, 34, 46, 80, 90, 80], ['Item', 'Un.', 'Qtd', 'R$/un.', 'Total', 'Origem'], rows, size=8.0, pad=3.0,
               aligns=['l', 'c', 'r', 'r', 'r', 'l'], hsize=7.8)
    yr -= 16
    yr = section(c, xr, yr, 'Logística (fora do orçamento)', wr)
    para(c, xr, yr, wr, 'Frete das compras (Portobello, metais e itens de internet, cotados sem frete; o frete antigo de R$ 300 é só referência), agendamento de entrega e subida pelo '
         'elevador do condomínio, guarda e proteção do material na obra e retirada do entulho (caçamba ou sacos, uma retirada prevista). Gestão é a coordenação da obra. '
         'Se quiser, entram como provisão na próxima revisão.', 8.8, 11.4)
    footer(c, 16, TOTAL)

def s17(c):
    header(c, 'Compatibilização de compras',
           'Itens que se sobrepõem foram resolvidos: fica um por função, o de maior valor que atende ao projeto. Abaixo, as pendências de compatibilidade antes de comprar.', 17, TOTAL)
    y = section(c, MG, PH - 130, 'Sobreposições resolvidas no R2', PW - 2 * MG)
    rows = []
    for f_, keep, vk, drop, vd, why in BUD['sob']:
        rows.append([f_, keep, brl(float(vk or 0)), drop, brl(float(vd or 0)) if vd else '—', why])
    y = table(c, MG, y, [120, 210, 80, 180, 80, PW - 2 * MG - 670], ['Função', 'Fica', 'R$', 'Sai', 'R$', 'Por quê'], rows, size=8.4, pad=3.4,
              aligns=['l', 'l', 'r', 'l', 'r', 'l'], bold_first=True, hsize=8.2)
    y -= 22
    y = section(c, MG, y, 'Compatibilidade a confirmar antes da compra', PW - 2 * MG)
    rows = [
        ['Bica Bracci 200 mm', 'Previsão R$ 445,69; o anúncio tem título "aço" e descrição "preto". Confirmar aço escovado e compatibilidade da base.'],
        ['Bases de parede 3 furos', 'Bica, união de mistura e dois registros Round homologados juntos. Não adaptar a Royale monocomando.'],
        ['B09048BN chuveiro', 'Acabamento monocomando: base DECA ou conversor DOCOL não confirmados. O modelo 3D vindo de DWG 2D não é gabarito.'],
        ['Metais', 'Bracci aço PVD, Aiello inox escovado e bica de outro fabricante não têm tonalidade idêntica garantida: aprovar amostras reais.'],
        ['Ralos', 'R1 de 720 mm: altura do corpo, saída e fecho hídrico. R2 de 100 × 100 mm com tampa removível: validar a caixa existente.'],
        ['Cuba Ametista 16', 'Confirmar estoque e se a válvula vem inclusa; sifão rígido compatível com a saída existente.'],
        ['Gouache', 'Lote único; calibre real medido antes de cortar; Nuage com cotação própria (hoje usa o preço do Bleu).'],
    ]
    table(c, MG, y, [190, PW - 2 * MG - 190], ['Item', 'Decisão ou pendência'], rows, size=8.8, pad=3.6, bold_first=True, hsize=8.6)
    footer(c, 17, TOTAL)

def s18(c):
    header(c, 'Escopo de serviços', 'O que cada frente faz, na ordem da obra. Insumos fora do orçamento de materiais estão indicados.', 18, TOTAL)
    W = [46, 150, 520, 160, PW - 2 * MG - 876]
    R = lambda *a: list(a)
    rows = [
        R('DM01', 'Proteção e isolamento', 'Proteger áreas vizinhas; isolar água, esgoto e circuitos do banheiro; desmontar e guardar box, vaso, gabinete e metais reaproveitáveis.', 'Empreiteira', '—'),
        R('DM02', 'Demolição de acabamentos', 'Piso (3,54 m²), revestimentos verticais (≈ 17,9 m²), tampo e cuba, com remoção manual controlada. Não cortar laje, vigas, pilares ou shafts.', 'Empreiteira', 'DM01'),
        R('DM03', 'Entulho', 'Uma retirada prevista; volume real depende das espessuras.', 'Empreiteira (logística)', 'DM02'),
        R('LV01', 'Levantamento aberto', 'Prumos, medidas acabadas, contrapiso, redes, pressão e aquecedor. Atualiza a paginação (Prancha 20).', 'Responsável técnico', 'DM02'),
        R('HI01', 'Água quente da cuba', 'Derivação de ramal existente, 6 m de tubo com isolamento, registro acessível; quente e fria até as bases do misturador.', 'Hidráulica', 'LV01'),
        R('HI02', 'Ralos e esgoto', 'R1 linear 720 mm no box; R2 100 × 100 mm junto ao vaso; esgoto DN50/DN40 e reinstalação do vaso.', 'Hidráulica', 'LV01'),
        R('EL01', 'Elétrica', 'L2 IP65 no box, perfil L3 sobre o espelho com fonte acessível, toalheiro Aiello; DR, aterramento e seções conferidos.', 'Elétrica (fora do orçamento)', 'LV01'),
        R('IM01', 'Impermeabilização', 'Piso, box até 2.400 mm, rodapé técnico, bancada e nicho (≈ 12 m²), tela nos cantos e ralos; ensaio de estanqueidade de 72 h registrado.', 'Empreiteira · material no R2', 'HI01 · HI02'),
        R('RV01', 'Paginação a seco', 'Medir peças do lote e paredes prontas, refazer a malha, marcar eixos, linha de piso e fiadas (155 + 157 × k).', 'Assentador', 'IM01'),
        R('RV02', 'Assentamento', 'Argamassa da empreiteira; junta 2 mm; 15 fiadas inteiras até 2.353 mm; pontas simétricas; acentos Nuage nas posições das pranchas.', 'Empreiteira (argamassa contratada)', 'RV01'),
        R('RV03', 'Perfis e juntas', 'Perfil no topo (8,02 m) e nas quinas; selante nos cantos, encontros com piso, louças e bancada.', 'Assentador · perfis no R2', 'RV02'),
        R('RV04', 'Rejunte', 'Acrílico Moon nas paredes e Blanc na bancada, depois de aprovar amostra de cor.', 'Assentador · rejunte no R2', 'RV03'),
        R('BC01', 'Bancada', 'Base impermeável, tampo e bordas em Nuage conforme a Prancha 14; furos com gabarito real.', 'Empreiteira', 'IM01'),
        R('MF01', 'Piso Monofloor Everest', 'Sistema aprovado pelo fabricante para o box, caimento para R1, selagem e encontro com ralos e paredes.', 'Monofloor (fora do orçamento)', 'RV04'),
        R('FO01', 'Forro e pintura', 'Forro resistente à umidade e pintura da faixa de 38 mm acima do revestimento.', 'Fora do orçamento', 'RV03'),
        R('MT01', 'Montagem e testes', 'Louças, metais, box, espelho, toalheiro; testes de vazão, escoamento, estanqueidade, iluminação; registro fotográfico.', 'Empreiteira e instaladores', 'MF01'),
    ]
    table(c, MG, PH - 130, W, ['ID', 'Serviço', 'O que inclui', 'Responsável / insumo', 'Depois de'], rows, size=9.8, pad=4.6, bold_first=True, hsize=9.6)
    footer(c, 18, TOTAL)

def s19(c):
    header(c, 'Execução e aceite', 'Sequência de obra com pontos de parada: não seguem sem aceite por escrito.', 19, TOTAL)
    xl = MG; wl = 540
    y = section(c, xl, PH - 130, 'Sequência', wl)
    passos = [
        ('1', 'Conferência e aprovação do responsável técnico; compra por lote, com amostra.', False),
        ('', 'PARADA 1 · RT aprova o caderno e o lote é conferido (calibre e tonalidade).', True),
        ('2', 'Proteção, isolamento das redes, demolição e levantamento aberto.', False),
        ('3', 'Hidráulica e elétrica executadas e testadas.', False),
        ('', 'PARADA 2 · redes testadas antes de fechar.', True),
        ('4', 'Impermeabilização e ensaio de estanqueidade por pelo menos 72 h.', False),
        ('', 'PARADA 3 · ensaio aprovado e registrado.', True),
        ('5', 'Paginação a seco com peças do lote: eixos, linha de piso e fiadas marcadas; recálculo se o calibre mudar.', False),
        ('', 'PARADA 4 · paginação a seco aprovada pelo cliente.', True),
        ('6', 'Assentamento e cura; perfis, selantes e rejunte.', False),
        ('7', 'Monofloor, montagem e limpeza.', False),
        ('8', 'Testes de vazão, escoamento, estanqueidade, iluminação e toalheiro; registro fotográfico.', False),
        ('', 'PARADA 5 · recebimento com checklist.', True),
    ]
    for n, t, stop in passos:
        if stop:
            rect(c, xl + 24, y - 18, wl - 24, 18, AMARELO45, K, 0.6)
            para(c, xl + 30, y - 2, wl - 36, t, 9.6, 12, 'S-B'); y -= 26
        else:
            txt(c, xl, y - 12, n, 12, 'S-B'); y = para(c, xl + 24, y - 2, wl - 24, t, 9.8, 12.6) - 9
    xr = xl + wl + 40; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Critérios de aceite do revestimento', wr)
    rows = [
        ['Fiadas', 'trena e nível a laser', 'juntas horizontais em 155 + 157 × k mm em todas as paredes; passam o canto sem salto'],
        ['Topo', 'nível a laser', 'linha contínua em 2.353 mm com perfil, nas seis paredes'],
        ['Pontas', 'trena', 'iguais nos dois lados de cada parede, ±2 mm da prancha'],
        ['Nicho', 'trena', 'lados do nicho nas juntas; nenhuma peça cortada na vertical em volta dele'],
        ['Acentos', 'prancha', 'posição e quantidade de Nuage conforme as elevações, sempre em peça inteira'],
        ['Junta', 'espaçador', '2 mm (ou a junta validada no lote), constante'],
        ['Planeza e degrau', 'régua de 2 m e luz rasante', 'sem degrau perceptível entre peças'],
        ['Colagem', 'percussão', 'sem som cavo'],
        ['Selantes', 'visual', 'contínuos nos cantos e encontros, sem rejunte rígido em junta de movimentação'],
    ]
    table(c, xr, yr, [100, 130, wr - 230], ['Item', 'Como medir', 'Aceite'], rows, size=9.0, pad=3.8, bold_first=True, hsize=8.8)
    footer(c, 19, TOTAL)

def s20(c):
    header(c, 'Recálculo com calibre e medida de obra',
           'O modelo usa 75 × 155 mm; o certificado do Nuage informa 76,5 × 155,5 mm. Com as peças do lote e as paredes prontas, a malha se refaz com as regras abaixo.', 20, TOTAL)
    xl = MG; wl = 500
    y = section(c, xl, PH - 130, 'Como refazer', wl)
    for i, (h, b) in enumerate([
        ('Medir.', 'Dez peças do lote (largura e altura, use a média) e cada parede em três alturas, depois do emboço.'),
        ('Fiadas.', 'Número de fiadas inteiras = maior n com n × altura + (n − 1) × junta ≤ altura da parede. O revestimento termina na última fiada inteira.'),
        ('Colunas.', 'Ponta c = (L − n × largura − (n + 1) × junta) ÷ 2. Fica o maior n com c de pelo menos 40% da largura.'),
        ('Vãos.', 'Conferir onde caem os lados do nicho e o batente da porta; peça a menos de 10 mm vira sobra que some na guarnição.'),
        ('Compra.', 'Área revestida × 1,10 por caixa fechada, conferida contra as peças físicas.'),
    ], 1):
        txt(c, xl, y - 12, str(i), 12, 'S-B'); y = rich(c, xl + 20, y - 2, wl - 20, h, b, 10.4, 8)
    xr = xl + wl + 36; wr = PW - MG - xr
    yr = section(c, xr, PH - 130, 'Sensibilidade ao calibre (junta 2 mm)', wr)
    rows = []
    for sid in ('P1', 'P2', 'P3', 'P4', 'P5'):
        W = CR.WALLS[sid]['W']
        p75 = CR.cols_sym(W, 75.0); p76 = CR.cols_sym(W, 76.5)
        rows.append([sid, fm(W), '%d + 2 × %s' % (p75['n'], fm(p75['c'], 1)), '%d + 2 × %s' % (p76['n'], fm(p76['c'], 1))])
    top76 = 15 * 155.5 + 14 * 2
    rows.append(['Fiadas', '2.391', '15 inteiras · topo 2.353', '15 inteiras · topo %s' % fm(top76, 1)])
    yr = table(c, xr, yr, [60, 70, (wr - 130) / 2, (wr - 130) / 2], ['Parede', 'Largura', 'Peça 75 × 155', 'Peça 76,5 × 155,5'], rows, size=10.0, pad=4.6,
               aligns=['l', 'r', 'r', 'r'], bold_first=True, hsize=9.8)
    yr -= 16
    p76 = CR.cols_sym(1275.0, 76.5)
    starts = [p76['c'] + 2 + k * 78.5 for k in range(p76['n'])]
    d0 = min(abs(s - 61.1) for s in starts); d1 = min(abs(s + 76.5 - 1058.7) for s in starts)
    yr = section(c, xr, yr, 'O que muda com 76,5 mm', wr)
    for h, b in [
        ('Colunas.', 'P1, P3 e P5 perdem uma coluna inteira por fiada; as pontas continuam simétricas e largas.'),
        ('Nicho.', 'Com 76,5 mm os lados do nicho deixam de cair nas juntas (ficam a %s e %s mm delas): recalcular antes de cortar.' % (fm(d0, 1), fm(d1, 1))),
        ('Topo.', 'Com 155,5 mm o revestimento termina em %s mm, ainda abaixo dos 2.391.' % fm(top76, 1)),
    ]:
        yr = rich(c, xr, yr, wr, h, b, 10.2, 7)
    footer(c, 20, TOTAL)

def s21(c):
    header(c, 'Pendências e decisões', 'O que precisa ser respondido antes de cortar e comprar. As linhas em rosa travam a compra do revestimento.', 21, TOTAL)
    W = [24, 270, 330, 140, PW - 2 * MG - 764]
    CRIT = 'rosa'
    rows = [
        ('1', 'Medir o calibre do lote (75 × 155 ou 76,5 × 155,5).', 'Muda colunas por parede, lados do nicho e topo (Prancha 20).', 'Obra e Portobello', 'Recálculo das pranchas 08–14', True),
        ('2', 'Aprovar o término em 2.353 mm com perfil e faixa pintada.', 'Alternativa até o forro: 107 tiras de 36 mm e +1 caixa.', 'Cliente', 'Prancha 07', True),
        ('3', 'Gouache no tampo da bancada.', 'É revestimento de parede; uso horizontal depende do fabricante.', 'Portobello', 'Prancha 14', True),
        ('4', 'Junta 2 mm × 1,5 mm do fabricante.', 'Com 1,5 mm as pontas mudam alguns milímetros.', 'Assentador e cliente', 'Prancha 20', True),
        ('5', 'Cotação do Nuage.', 'Hoje usa o preço do Bleu.', 'Compras', 'Orçamento R2', False),
        ('6', 'Verga da porta a 1.990 mm.', 'Deixa 49 mm de peça acima do vão; a 2.041 mm o recorte some.', 'Cliente e marcenaria', 'Prancha 12', False),
        ('7', 'Sistema Everest no box.', 'Monofloor aprova aderência, atrito molhado, selagem e ralos.', 'Monofloor', 'MF01', False),
        ('8', 'Ralo R1 de 720 mm.', 'Produto e altura disponíveis; o link de 600 mm foi descartado.', 'Hidráulica', 'Prancha 04', False),
        ('9', 'Posição do vaso e da caixa do R2.', 'Desenhados como reserva.', 'Obra', 'Pranchas 03–04', False),
        ('10', 'Bases e metais.', 'Base do chuveiro, bica e registros; tonalidade dos metais.', 'Cliente e hidráulica', 'Prancha 17', False),
        ('11', 'Rejunte Moon nas paredes.', 'Azul escuro exige amostra e aprovação.', 'Cliente', 'RV04', False),
        ('12', 'Logística e gestão.', 'Frete, entrega no condomínio e caçamba fora do orçamento: incluir como provisão?', 'Cliente', 'Orçamento R2', False),
    ]
    rr = []
    for n, a, b, d, e, crit in rows:
        cells = [n, a, b, d, e]
        rr.append({'cells': cells, 'fill': MAGENTA12} if crit else cells)
    table(c, MG, PH - 130, W, ['#', 'Pendência', 'Por que importa', 'Quem decide', 'Onde'], rr, size=9.2, pad=4.0, hsize=9.0, zebra=False)
    footer(c, 21, TOTAL)

def s22(c):
    header(c, 'Fontes e premissas', 'Consulta em 25/10/2026. Preços web sem frete, sujeitos a estoque e condições comerciais. Nenhuma compra foi realizada.', 22, TOTAL)
    xl = MG; wl = PW - 2 * MG
    y = section(c, xl, PH - 130, 'Fontes', wl)
    fontes = [
        ('PB', 'Proposta Portobello 05310148, 13/10/2026, válida até 31/10/2026 (Bleu Nuit R$ 339,99/m²).'),
        ('NU', 'portobello.com.br · Gouache Nuage 7,5 × 15,5 brilho (12892E)'),
        ('BN', 'portobello.com.br · Gouache Bleu Nuit 7,5 × 15,5 brilho (211991E)'),
        ('GR', 'media.portobello.com.br · folder de linha Gouache 26.0'),
        ('CU', 'bellobanho.com.br · cuba de apoio Ametista 16 Duramatt branca'),
        ('AI', 'grupoaiello.com.br · toalheiro térmico Unique Solo (variante 47080769945771)'),
        ('RO', 'uniquestore.com.br · torneira Royale (alternativa descartada)'),
        ('BI', 'leroymerlin.com.br · bica para banheira aço escovado'),
        ('RL', 'leroymerlin.com.br · ralo linear inox 600 mm (descartado; projeto pede 720 mm)'),
        ('MF', 'monofloor.com.br · perguntas frequentes'),
        ('IM', 'telhanorte.com.br · Quartzolit Tecplus Lastic 18 kg (R$ 199,90) e tela estruturante 73 cm × 10 m (R$ 67,90)'),
        ('AQ', 'tigre.com.br · tubo Aquatherm'),
    ]
    for k, v in fontes:
        txt(c, xl, y - 11, k, 9.6, 'S-B'); y = para(c, xl + 34, y, wl - 34, v, 9.6, 12.6) - 4
    y -= 14
    y = section(c, xl, y, 'Geometria e premissas', wl)
    for h, b in [
        ('Modelo.', 'R47 / Estudos_Banheiro/E_R1.json, modelo MaxHaus_R47_Interiores.skp e o caderno R0 de 25/10/2026, de onde vieram as posições de porta, nicho, ralos, luminárias e acentos.'),
        ('Redes.', 'Não há levantamento das tubulações embutidas nem do quadro elétrico. Tubos, conexões e condutores são reservas, não lista de montagem.'),
        ('Consumo de impermeabilizante.', 'Cerca de 3,5 kg/m² é estimativa de planejamento; o consumo vem do sistema escolhido e da ficha do fabricante.'),
    ]:
        y = rich(c, xl, y, wl, h, b, 9.4, 6)
    footer(c, 22, TOTAL)

SHEETS = [s15, s16, s17, s18, s19, s20, s21, s22]
