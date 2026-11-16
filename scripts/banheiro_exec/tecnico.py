# -*- coding: utf-8 -*-
"""Caderno TÉCNICO do banheiro — BT-01 a BT-07 (gestão da obra e empreiteira)."""
import math
from lib import *      # noqa
import exec_a
import exec_b

CAD = 'CADERNO TÉCNICO'
X1, X2 = MARGIN, 730.0
W1, W2 = 630.0, W - MARGIN - 730.0


def bt01():
    f = Folha(CAD, 'BT-01', 'Reforma do banheiro: escopo e leitura dos cadernos', 'Dois cadernos para dois públicos: este, técnico, para quem decide e contrata; o executivo (BE), para quem executa.')
    d = f.d
    num = [('2880', 'mm de parede da porta, por fora', '880 + vão de 800 + 1200'),
           ('800 × 2150', 'vão da porta P02', 'abre para fora, anti-horário'),
           ('800 × 250', 'área técnica do chuveiro', 'box mantido com 920 de fundo'),
           ('+980', 'topo da bancada', 'gabinete de 880 + saia de 100')]
    for i, (n, a, b) in enumerate(num):
        x = X1 + i * 162
        d.rect(x, 140, 150, 96, fill='none', stroke=K, sw=1.0)
        f.t(x + 10, 178, n, 19, INK, True)
        f.t(x + 10, 198, a, 7.8, INK, True)
        f.t(x + 10, 212, b, 7.4, INK_SOFT)
    y = f.par(X1, 272, W1, [
        ('O que esta emissão corrige.', 'As plantas anteriores do banheiro (scan, caderno R2 e executivo R95) tinham a porta 0,33 m mais ao norte, '
         'a área técnica com 150 a 240 mm de profundidade e a bancada com 530 mm. Em 14/11/2026 o cliente mediu em obra: a parede da porta, '
         'a área técnica, a bancada, o gabinete e o espelho. Tudo aqui parte dessas medidas.'),
        ('Escopo.', 'Demolição dos acabamentos; rebaixo e nivelamento do piso com o monolítico Sinesse Pro de fora, sem soleira, com perfil de metal; '
         'impermeabilização; remodelagem do ralo do box e do ralo ao lado do vaso; reinstalação do vaso e do esgoto; água quente na torneira da pia; '
         'pontos elétricos, com o ponto novo do toalheiro acima do vaso; forro e iluminação da FAS; revestimento das paredes; piso; bancada; porta.'),
        ('O item que não pode falhar.', 'Levar água quente à torneira da pia é a prioridade pessoal do cliente nesta reforma. O ramal está na BE-06 e na BT-04: '
         'derivação da coluna do chuveiro dentro da área técnica, cerca de 1,1 m de tubo isolado, registro acessível e teste antes de fechar a parede.'),
        ('O que continua valendo do R95.', 'Revestimento Gouache Bleu Nuit 155 × 155 com acentos Nuage, piso Confete 100 × 100, forro e topo do revestimento a +2500, '
         'ralo linear de 720 × 90, toalheiro Aiello e porta com visor circular. A bancada em Corian do R95 foi trocada pelo balcão atual revestido em Bleu Nuit.'),
        ('O que foi superado.', 'Do R95: comprimento de 2576, porta de 2103 de altura, bancada de 1640 × 530 a +840 com saia de 60, espelho de 1660 × 650 '
         'e área técnica de 240 ao longo de todo o box. Do caderno geral: forro novo a 2,40 m (aqui, +2500).'),
    ], size=8.8, lh=12.6)
    y2 = f.tab(X2, 150, W2, [('Folha', 0.12, 'start'), ('Conteúdo', 0.60, 'start'), ('Para quem', 0.28, 'end')], [
        ('BT-01', 'Escopo e leitura dos cadernos', 'gestão'),
        ('BT-02', 'Medidas de referência e conferência em obra', 'gestão e mestre'),
        ('BT-03', 'Piso, rebaixo e impermeabilização: critérios', 'gestão e empreiteira'),
        ('BT-04', 'Hidráulica: água quente, esgoto e ralos', 'gestão e encanador'),
        ('BT-05', 'Elétrica, forro e iluminação FAS', 'gestão e eletricista'),
        ('BT-06', 'Quantitativos e compra', 'gestão'),
        ('BT-07', 'Liberações, pendências e riscos', 'gestão'),
    ], titulo='CADERNO TÉCNICO')
    f.tab(X2, y2 + 30, W2, [('Folha', 0.12, 'start'), ('Conteúdo', 0.60, 'start'), ('Para quem', 0.28, 'end')], [
        ('BE-01', 'Planta baixa do banheiro', 'todos'),
        ('BE-02', 'Demolição e o que preservar', 'pedreiro'),
        ('BE-03', 'Níveis e rebaixo do piso', 'pedreiro'),
        ('BE-04', 'Impermeabilização', 'impermeabilizador'),
        ('BE-05', 'Esgoto: ralos e vaso', 'encanador'),
        ('BE-06', 'Água quente na torneira da pia', 'encanador'),
        ('BE-07', 'Elétrica: pontos e comandos', 'eletricista'),
        ('BE-08', 'Forro e iluminação da FAS', 'gesseiro e eletricista'),
        ('BE-09', 'Bancada, gabinete e espelho', 'azulejista / marceneiro'),
        ('BE-10', 'Porta P02', 'marceneiro'),
        ('BE-11', 'Piso Confete', 'assentador'),
        ('BE-12 a BE-17', 'Paginação das paredes, em duas versões', 'assentador'),
        ('BE-18', 'Sequência de execução', 'todos'),
    ], titulo='CADERNO EXECUTIVO', alt=15.5)
    return f


def bt02():
    f = Folha(CAD, 'BT-02', 'Medidas de referência e conferência em obra', 'De onde vem cada medida, o que é premissa e uma coluna em branco para anotar o que for medido depois da demolição.')
    linhas = [
        ('Parede da porta, por fora', '880 + 800 + 1200 = 2880', 'cliente, 14/11', ''),
        ('Comprimento por dentro (acabado)', '2680', 'calculado: 2880 - 2 × 100', ''),
        ('Largura por dentro (acabado)', '1420', 'modelo R95', ''),
        ('Espessura das paredes', '100', 'scan; pode ser 120', ''),
        ('Vão da porta P02', '800 × 2150', 'cliente, 14/11', ''),
        ('Fundo do box', '920', 'scan / R95, mantido pelo cliente', ''),
        ('Área técnica AT-B', '800 × 250', 'cliente, 14/11', ''),
        ('Posição da AT-B no box', 'encostada no fundo', 'premissa desta emissão', ''),
        ('Bancada B01', '1600 × 400, saia 100', 'cliente, 14/11', ''),
        ('Gabinete', '1600 × 400 × 880 de altura', 'cliente, 14/11', ''),
        ('Topo da bancada', '+980', 'cliente, 14/11', ''),
        ('Posição da bancada na parede', 'encostada no vidro do box', 'premissa desta emissão', ''),
        ('Espelho', '1600 × 900', 'cliente, 14/11', ''),
        ('Base do espelho', '+1340', 'proposta: 360 acima do tampo', ''),
        ('Forro novo', '+2500', 'modelo R95', ''),
        ('Laje', '+2620', 'cliente (pé-direito 2,62 m)', ''),
        ('Eixo do vaso', '980 da parede da bancada', 'modelo R95', ''),
        ('Esgoto do vaso até a parede', '~300', 'típico; depende da bacia', ''),
        ('Ralo linear R1', '720 × 90, a 62 da AT-B', 'modelo R95', ''),
        ('Ralo R2', 'grelha 100 × 100', 'caixa existente a levantar', ''),
        ('Nicho do box', 'de parede a parede: 1170 × 400, base a +1100', 'cliente, 14/11; altura e base do R95', ''),
    ]
    f.tab(X1, 150, 760, [('Medida', 0.30, 'start'), ('Valor adotado (mm)', 0.24, 'start'), ('Fonte', 0.28, 'start'), ('Medido em obra', 0.18, 'end')],
          linhas, titulo='MEDIDAS ADOTADAS', alt=16.5)
    x = X1 + 800
    w = W - MARGIN - x
    f.par(x, 152, w, [
        ('Por que conferir.', 'Só a parede da porta, a área técnica, a bancada, o gabinete e o espelho foram medidos em obra. O resto vem do modelo R95 e do scan. '
         'O revestimento antigo esconde o prumo e a espessura real das paredes.'),
        ('Quando.', 'Logo depois da demolição, com as paredes no osso e o piso aberto, antes da regularização. É a liberação 4 da sequência (BE-18).'),
        ('O que muda se a medida mudar.', 'Comprimento ou largura: refazer a paginação das paredes e o plano de corte do piso. '
         'Posição da área técnica ou da bancada: refazer só a parede da bancada (BE-17) e o fundo do box (BE-15). '
         'Esgoto do vaso: conferir a bacia antes de fechar o piso.'),
        ('Três premissas a confirmar com o cliente.', '1. A área técnica encostada no fundo do box, com 120 mm de parede até o vidro. '
         '2. A bancada encostada no vidro do box, com 160 mm de folga até a parede do vaso. '
         '3. Parede com 100 mm: se tiver 120, o banheiro tem 2640 por dentro.'),
        ('Tolerância.', 'A paginação aceita até 5 mm de diferença por parede, absorvidos nas pontas. Acima disso, recalcular antes de cortar.'),
    ], size=8.4, lh=12.0)
    return f


def bt03():
    f = Folha(CAD, 'BT-03', 'Piso, rebaixo e impermeabilização: critérios', 'O que se exige de cada sistema, como se confere e o que não se aceita.')
    y = f.tab(X1, 150, W1, [('Camada, de cima para baixo', 0.46, 'start'), ('Espessura', 0.20, 'end'), ('Observação', 0.34, 'end')], [
        ('Porcelanato Confete 100 × 100', '9 mm', 'conferir o lote'),
        ('Argamassa colante', '~5 mm', 'premissa de cálculo'),
        ('Proteção mecânica', 'conforme sistema', 'sobre a membrana'),
        ('Impermeabilização', 'conforme sistema', 'ver BE-04'),
        ('Regularização com caimento', 'variável', 'define os níveis'),
        ('Laje', '-', 'não rebaixar'),
    ], titulo='COMPOSIÇÃO DO PISO DO BANHEIRO')
    y = f.par(X1, y + 26, W1, [
        ('Nível único com a sala.', 'O piso pronto do banheiro fica no mesmo nível do monolítico Sinesse Pro (2 a 4 mm). Para isso a base do banheiro '
         'fica 10 a 12 mm abaixo da base da sala, mais a espessura da impermeabilização e da proteção. Não há soleira: a troca de piso é marcada '
         'por um perfil de metal de 3 mm à vista, com junta elástica.'),
        ('Quanto rebaixar.', 'Não é um número fixo: é a diferença entre a base que existir depois da demolição e a base alvo. '
         'A empreiteira mede, registra e só então decide se regulariza ou se retira contrapiso. A laje não se corta.'),
        ('Risco conhecido: esgoto contra nível.', 'O esgoto mora no rebaixo antigo. Com o piso no nível da casa, impermeabilização, caimento e piso '
         'têm de caber entre a laje e o ±0 e os ralos precisam manter queda. Se não couber, a decisão volta ao cliente antes de seguir: '
         'ou o piso do banheiro sobe alguns milímetros, ou o caimento diminui.'),
        ('Caimentos.', 'Box: ~1,5% para o ralo linear, de -10 na entrada a -25 no ralo. Piso seco: 0,5% para o ralo ao lado do vaso. '
         'Feitos na regularização, nunca na argamassa do porcelanato.'),
    ], size=8.6, lh=12.2)
    y2 = f.tab(X2, 150, W2, [('Critério', 0.34, 'start'), ('Exigência', 0.66, 'start')], [
        ('Área', 'todo o piso, paredes do box até +2500, rodapé de 300 no resto, nicho, faixa da cuba'),
        ('Sistema', 'membrana flexível compatível com porcelanato e argamassa; definir produto com o responsável técnico'),
        ('Reforços', 'tela em cantos, encontro piso-parede, tubos e flanges dos ralos'),
        ('Ensaio', 'lâmina de água de 3 a 5 cm por 72 horas, com foto e data'),
        ('Aceite', 'nível não baixa; sem mancha na laje de baixo; ralos estanques'),
        ('Depois do ensaio', 'proteção mecânica; furo novo só com selagem'),
    ], titulo='IMPERMEABILIZAÇÃO')
    f.par(X2, y2 + 26, W2, [
        ('Rejunte: 5 dias de espera.', 'Rejunte acrílico Quartzolit nas paredes e no piso. Depois de aplicado, aguardar 5 dias antes de molhar '
         'ou liberar o uso das áreas rejuntadas, conforme orientação do fabricante. Esse prazo entra no cronograma: o box só recebe água depois dele.'),
        ('Porcelanato no box.', 'Cortar nas quebras de plano do caimento; não empenar placa de 1 m. Conferir na ficha do lote se o acabamento serve para piso molhado.'),
        ('Não se aceita.', 'Caimento corrigido com argamassa do piso; membrana aplicada sobre base úmida ou solta; ensaio sem registro; '
         'ralo assentado depois da membrana; revestimento antes do ensaio.'),
        ('Responsabilidade.', 'Estas folhas orientam o escopo. Produto, consumo, cura e garantia da impermeabilização são do aplicador e do responsável técnico da obra.'),
    ], size=8.6, lh=12.2)
    return f


def bt04():
    f = Folha(CAD, 'BT-04', 'Hidráulica: água quente, esgoto e ralos', 'Memorial das instalações hidráulicas. Traçados de intenção: a rede embutida não foi levantada.')
    y = f.tab(X1, 150, W1, [('Item', 0.30, 'start'), ('Definição', 0.70, 'start')], [
        ('Origem', 'coluna de água quente do chuveiro, dentro da área técnica AT-B'),
        ('Fonte de calor', 'aquecedor a gás do apartamento (AT-A, no closet); sem alteração no gás'),
        ('Percurso', 'tê na coluna, registro, ~0,3 m dentro da AT-B e ~0,8 m embutido na parede da bancada, a +1245'),
        ('Tubo', 'CPVC ou PPR de 22 mm, conforme o material da rede existente; transição certificada se mudar'),
        ('Isolamento', 'polietileno expandido em todo o ramal'),
        ('Chegada', 'comando de água quente da pia, à esquerda de quem usa; água fria existente à direita'),
        ('Acesso', 'registro do ramal atrás de uma tampa de inspeção na face da área técnica'),
        ('Teste', 'pressão com o rasgo aberto por pelo menos 6 horas; depois, tempo de chegada da água quente'),
    ], titulo='RAMAL DE ÁGUA QUENTE DA PIA')
    f.par(X1, y + 26, W1, [
        ('Por que derivar do chuveiro.', 'É o ponto de água quente mais perto da pia e já está dentro da área técnica, que tem acesso. '
         'O ramal fica curto, com pouca água parada: a água quente chega rápido e perde pouco calor.'),
        ('O que conferir antes.', 'Material e diâmetro da coluna existente; pressão e vazão com chuveiro e pia abertos juntos; '
         'se o aquecedor acende com a vazão baixa de uma torneira de lavatório. Se não acender, avaliar com o instalador antes de fechar a parede.'),
        ('O que não fazer.', 'Ligar quente e fria por um tê simples; embutir flexível; fazer emenda sem acesso; mexer na tubulação de gás; '
         'fechar a parede sem teste.'),
        ('Altura dos metais.', 'Com o tampo a +980, os comandos ficam a +1245 e a bica a +1250, 265 mm acima do tampo. '
         'Conferir alcance do jato e a cuba escolhida antes de furar.'),
    ], size=8.6, lh=12.2)
    y2 = f.tab(X2, 150, W2, [('Ponto', 0.22, 'start'), ('Serviço', 0.78, 'start')], [
        ('R1 · ralo linear', 'corpo novo de 720 × 90 no box, flange colada na membrana, borda a -25; conferir saída, sifão e vazão do modelo'),
        ('R2 · ao lado do vaso', 'manter caixa sifonada e saída; trocar o porta-grelha por grelha oculta 100 × 100; prolongador até o piso novo; manter fecho hídrico e acesso'),
        ('Vaso', 'reaproveitado; ponto de esgoto DN100 com a boca rente ao piso novo; anel de vedação e engate novos; bacia aparafusada'),
        ('Prumada', 'a área técnica é prumada do condomínio: não demolir, não desviar'),
    ], titulo='ESGOTO E RALOS')
    f.par(X2, y2 + 26, W2, [
        ('Levantamento obrigatório.', 'Com o piso aberto, medir centro e profundidade de cada ponto de esgoto e o sentido de escoamento. '
         'As posições do R2 e do esgoto do vaso nas plantas são do modelo, não de medição.'),
        ('Queda.', 'Todo ramal de esgoto mantém queda até a prumada depois do rebaixo. É a verificação que libera a regularização (BT-03).'),
        ('Registros.', 'Aproveitar a obra para trocar registros antigos do banheiro e identificar o registro geral. '
         'Ensaio de estanqueidade da rede de água antes de fechar qualquer rasgo.'),
    ], size=8.6, lh=12.2)
    return f


def bt05():
    f = Folha(CAD, 'BT-05', 'Elétrica, forro e iluminação da FAS', 'Pontos, cargas a confirmar e a compatibilização do forro com as luminárias compradas.')
    y = f.tab(X1, 150, W1, [('ID', 0.08, 'start'), ('Ponto', 0.40, 'start'), ('Dado', 0.52, 'start')], [
        ('T20', 'Toalheiro elétrico, atrás do vaso: ÚNICO PONTO NOVO', '127 V; potência pela placa do aparelho; ligação direta na versão de fio oculto'),
        ('T17', 'Tomada existente da bancada', 'manter; trocar espelho'),
        ('D1', 'FAS Halo 7 W (TE.4106)', 'embutido orientável, 2700 K, 36°; furo de 53 mm'),
        ('D2', 'FAS Tiny 5,8 W IP (TE.4676)', 'embutido para o box, 2700 K, 36°, bivolt; furo de 34 mm'),
        ('L3', 'Perfil linear do espelho (existente)', 'reinstalar; fonte fora da área de respingos'),
        ('EX01', 'Exaustor no forro (existente)', 'vazão de referência 95 m³/h (3,80 × 2,50 × 10); duto a levantar'),
        ('S03 / S04', 'Interruptores existentes', 'manter posição; trocar comando e espelho'),
    ], titulo='PONTOS')
    f.par(X1, y + 26, W1, [
        ('Regra.', 'Troca de toda a fiação pelos eletrodutos existentes; pontos mantidos, espelhos trocados. Só o T20 é novo.'),
        ('Proteção.', 'Circuitos do banheiro com DR de 30 mA e terra. Dimensionamento, bitola e disjuntor pelo eletricista, '
         'depois do levantamento do quadro, que tem 17 anos.'),
        ('Toalheiro.', 'O ponto T20 fica no eixo do vaso, atrás do aparelho (550 × 370 mm, base a +989). Confirmar a variante comprada: '
         'a de fio oculto não usa tomada.'),
        ('Exaustão.', 'Não descarregar no vão do forro nem em shaft sem duto. Rota e saída dependem do condomínio.'),
    ], size=8.6, lh=12.2)
    y2 = f.tab(X2, 150, W2, [('Item', 0.34, 'start'), ('Dado', 0.66, 'start')], [
        ('Pedido FAS', '22804, de 06/11/2026; entrega prevista para a semana de 21/12/2026'),
        ('Banheiro', '1 Halo 7 W + 1 Tiny 5,8 W IP'),
        ('Folha F02 (detalhes)', 'nicho de 53 mm (D1) e de 34 mm (D2); altura mínima de 100 mm acima do forro'),
        ('Situação', 'folha carimbada "aguardando aprovação"'),
        ('Folha F01 (planta)', 'não recebida: posições desta emissão vêm do modelo R95'),
    ], titulo='PROJETO DE ILUMINAÇÃO FAS')
    f.par(X2, y2 + 26, W2, [
        ('Forro a +2500.', 'Laje a +2620 menos forro de 15 mm: sobram 105 mm para a luminária, contra 100 mm pedidos pela FAS. '
         'A folga é de 5 mm. Medir a laje depois de tirar o forro antigo; se faltar altura, o forro desce e o revestimento acompanha.'),
        ('Entrega em dezembro.', 'As luminárias chegam depois do forro pronto. Deixar os furos marcados e fazer com a peça em mãos, ou furar pelo gabarito da FAS.'),
        ('Caderno geral.', 'O Caderno Alternativo A ainda cita forro novo a 2,40 m e duas luminárias embutidas genéricas. Para o banheiro vale este caderno.'),
    ], size=8.6, lh=12.2)
    return f


def bt06():
    f = Folha(CAD, 'BT-06', 'Quantitativos e compra', 'Quantidades calculadas sobre as medidas desta emissão. Refazer depois da medição de obra e antes de comprar.')
    tot_p = sum(p.n_bleu for p in PAREDES)
    tot_n = sum(p.n_nuage for p in PAREDES)
    res_n = math.ceil(tot_n * 1.10)
    tot_a = sum(p.area for p in PAREDES)
    # nicho de parede a parede (1170 x 400 x 118): fundo 8 x 3, base e teto 8 + 8 tiras, duas pontas 3 + 3
    nicho_p = 24 + 16 + 6
    nicho_a = (1170 * 400 + 2 * 1170 * 118 + 2 * 118 * 400) / 1e6
    banc_p, _banc_int, banc_a = exec_b.bancada_resumo()
    res = math.ceil((tot_p + nicho_p + banc_p) * 1.10)
    cx_pecas = math.ceil(res / 36.0)
    cx_area = math.ceil((tot_a + nicho_a + banc_a) * 1.10 / 0.87)
    caixas = max(cx_pecas, cx_area)
    _, pecas_piso, area_piso = exec_a.be11()
    y = f.tab(X1, 150, W1, [('Parede', 0.10, 'start'), ('Superfície', 0.34, 'start'), ('Peças', 0.18, 'end'), ('Inteiras', 0.12, 'end'), ('Cortadas', 0.12, 'end'), ('Área m²', 0.14, 'end')],
              [(p.id, p.nome, '%d + %d N' % (p.n_bleu, p.n_nuage), p.inteiras, p.n_bleu - p.inteiras, br(p.area)) for p in PAREDES]
              + [('Total', '', '%d + %d N' % (tot_p, tot_n), sum(p.inteiras for p in PAREDES), tot_p - sum(p.inteiras for p in PAREDES), br(tot_a))],
              titulo='PAREDES — BLEU NUIT 155 × 155 + NUAGE 75 × 155 (N)')
    y = f.tab(X1, y + 30, W1, [('Material', 0.30, 'start'), ('Conta', 0.44, 'start'), ('Compra', 0.26, 'end')], [
        ('Bleu Nuit 155 × 155 (211997E)', '%d parede + %d nicho + %d bancada = %d peças; + 10%% = %d; caixa com 36 / 0,87 m²' % (tot_p, nicho_p, banc_p, tot_p + nicho_p + banc_p, res), '%d caixas' % caixas),
        ('Nuage 75 × 155 (12935E)', '%d pares nas paredes = %d peças; + 10%% = %d (BE-12)' % (tot_n // 2, tot_n, res_n), 'conferir peças por caixa'),
        ('Confete 100 × 100 (5041209)', '%s m² em %d recortes; 5 placas + 1 de reserva' % (br(area_piso), len(pecas_piso)), '3 caixas (6 placas)'),
        ('Nicho de parede a parede', 'fundo 1170 × 400 (24 peças), base e teto (16 tiras de 118), duas pontas (6): %d peças, %s m²' % (nicho_p, br(nicho_a)), 'na conta acima'),
        ('Bancada revestida B01', 'tampo 1600 × 400, saia 100 e lateral norte: %d peças, %s m² (BE-19)' % (banc_p, br(banc_a)), 'na conta acima'),
    ], titulo='REVESTIMENTOS')
    f.par(X1, y + 24, W1, [
        ('Como a conta foi feita.', 'Cada posição da malha conta uma peça, inteira ou cortada. Um corte pequeno não aproveita a sobra de outro: '
         'é a conta conservadora. Com plano de aproveitamento, a compra de Bleu Nuit pode cair uma ou duas caixas.'),
        ('Comparação com o R95.', 'O R95 comprava 21 caixas de Bleu Nuit para 15,16 m². Aqui são %s m²: a parede da bancada perde revestimento '
         '(o espelho cresceu) e a da porta ganha (o banheiro ficou 104 mm mais comprido).' % br(tot_a)),
    ], size=8.6, lh=12.2)
    f.tab(X2, 150, W2, [('Item', 0.34, 'start'), ('Quantidade', 0.22, 'start'), ('Base', 0.44, 'start')], [
        ('Impermeabilização', '~12 m²', 'piso, box até o forro, rodapé, nicho; consumo pelo sistema'),
        ('Rejunte acrílico Quartzolit, paredes', '8 kg azul + 1 kg claro', 'por cor na BT-06B'),
        ('Espaçador de 5 mm', '1 pacote', 'junta entre as duas Nuage de cada par'),
        ('Rejunte acrílico Quartzolit, piso', '1 kg', 'cor próxima do Confete'),
        ('Perfil de metal da porta', '1 peça de 0,80 m', '3 mm à vista'),
        ('Tubo de água quente + isolamento', 'até 6 m', 'reserva; percurso estimado de 1,1 m'),
        ('Registro de água quente', '1', 'no ramal da pia'),
        ('Ralo linear 720 × 90', '1', 'com corpo e flange'),
        ('Grelha oculta 100 × 100', '1', 'ralo R2; prolongador a medir'),
        ('Anel de vedação e engate do vaso', '1 jogo', 'novos'),
        ('Forro de gesso RU', '3,81 m²', 'a +2500, com tabica'),
        ('Base do tampo B01', 'tampo existente ou placa cimentícia 12 mm', 'conferir firmeza em obra'),
        ('Perfil metálico de canto', '~2,0 m (frente + lateral)', 'alumínio anodizado ou inox, 10 mm'),
        ('Rejunte epóxi', '1 kg', 'só no tampo da bancada'),
        ('Porta P02', 'folha 794 × 2135 × 40', 'com visor Ø400'),
        ('Luminárias FAS', 'D1 + D2', 'já compradas (pedido 22804)'),
    ], titulo='COMPLEMENTOS', alt=16.0)
    return f


def _rej(area, a, b, e=9.0, j=2.0, dens=1.7):
    """kg de rejunte: (A+B)/(A·B) × espessura × junta × densidade, medidas em mm."""
    return area * (a + b) / (a * b) * e * j * dens


def bt06b():
    f = Folha(CAD, 'BT-06B', 'Lista de compra: m², argamassa, rejunte, perfis e metais',
              'Tudo com 10% de perda. Quantidades sobre as medidas desta emissão: refazer depois da medição de obra.')
    pares = sum(len(p.acentos) for p in PAREDES)
    a_nuage = pares * 2 * 0.075 * 0.155
    a_par = sum(p.area for p in PAREDES) - pares * 0.155 * 0.155 + a_nuage
    a_bleu_par = a_par - a_nuage
    a_nicho = (1170 * 400 + 2 * 1170 * 118 + 2 * 118 * 400) / 1e6
    _n, _i, a_banc = exec_b.bancada_resumo()
    a_tampo = 1.60 * 0.40
    a_bleu = a_bleu_par + a_nicho + a_banc
    _, _pp, a_piso = exec_a.be11()
    k = 1.10
    n_bleu = sum(p.n_bleu for p in PAREDES) + 46 + _n
    n_nuage = sum(p.n_nuage for p in PAREDES)
    # --- revestimentos
    y = f.tab(X1, 150, W1, [('Revestimento', 0.36, 'start'), ('Líquido m²', 0.16, 'end'), ('+10% m²', 0.16, 'end'), ('Peças +10%', 0.32, 'end')], [
        ('Gouache Bleu Nuit 155 × 155', br(a_bleu), br(a_bleu * k), '%d peças · %d caixas' % (math.ceil(n_bleu * k), math.ceil(math.ceil(n_bleu * k) / 36.0))),
        ('· paredes P1 a P6', br(a_bleu_par), br(a_bleu_par * k), ''),
        ('· nicho (fundo, base, teto, pontas)', br(a_nicho), br(a_nicho * k), ''),
        ('· bancada B01 (tampo, saia, lateral)', br(a_banc), br(a_banc * k), ''),
        ('Gouache Nuage mate 75 × 155', br(a_nuage), br(a_nuage * k), '%d peças (%d pares)' % (math.ceil(n_nuage * k), pares)),
        ('Porcelanato Confete 100 × 100 (piso)', br(a_piso), br(a_piso * k), '6 placas (5 + 1 reserva)'),
    ], titulo='REVESTIMENTOS — m² COM 10%', alt=16.0)
    # --- argamassa
    arg_par = (a_bleu + a_nuage) * k * 5.0
    arg_piso = a_piso * k * 8.0
    y = f.tab(X1, y + 30, W1, [('Argamassa colante', 0.40, 'start'), ('Conta', 0.36, 'start'), ('Compra', 0.24, 'end')], [
        ('AC-III, paredes, nicho e bancada', '%s m² × 5 kg/m² = %d kg' % (br((a_bleu + a_nuage) * k), round(arg_par)), '%d sacos de 20 kg' % math.ceil(arg_par / 20.0)),
        ('AC-III, piso (dupla colagem)', '%s m² × 8 kg/m² = %d kg' % (br(a_piso * k), round(arg_piso)), '%d sacos de 20 kg' % math.ceil(arg_piso / 20.0)),
        ('Total', '%d kg' % round(arg_par + arg_piso), '%d sacos (%d kg)' % (math.ceil(arg_par / 20.0) + math.ceil(arg_piso / 20.0), 20 * (math.ceil(arg_par / 20.0) + math.ceil(arg_piso / 20.0)))),
    ], titulo='ARGAMASSA', alt=16.0)
    y = f.par(X1, y + 22, W1, [
        ('Consumo.', 'AC-III para porcelanato. Paredes com desempenadeira de 6 mm, cerca de 5 kg/m²; dentro do box, passar também no verso da peça (dupla colagem), por isso a margem. '
         'Piso em placa 100 × 100: dupla colagem obrigatória, cerca de 8 kg/m². Conferir o consumo na embalagem da marca escolhida.'),
    ], size=8.2, lh=11.6)
    # --- metais
    f.tab(X1, y + 18, W1, [('Metal / acessório', 0.38, 'start'), ('Qtde', 0.10, 'end'), ('Observação', 0.52, 'start')], [
        ('Misturador da pia, de parede', '1', 'novo, com água quente; comandos a +1245, bica a +1250'),
        ('Chuveiro + registro / misturador do box', '1 conj.', 'manter ou trocar: definir; água quente pela coluna no AT-B'),
        ('Registro de água quente (ramal da pia)', '1', 'novo, acesso pela tampa de inspeção na P2'),
        ('Válvula de escoamento da cuba + sifão', '1', 'conforme a cuba de apoio escolhida'),
        ('Engates flexíveis', '3', '2 do misturador + 1 do vaso'),
        ('Anel de vedação do vaso', '1', 'novo, na reinstalação'),
        ('Ralo linear 720 × 90', '1', 'com corpo e flange; no box'),
        ('Grelha oculta 100 × 100 (R2)', '1', 'junto ao vaso; prolongador a medir'),
        ('Toalheiro elétrico Aiello Unique Solo', '1', 'ponto novo T20, atrás do vaso'),
    ], titulo='METAIS', alt=15.5)
    # --- rejunte por cor
    r_bleu = _rej(a_bleu_par + a_nicho + a_banc - a_tampo, 155, 155) * k
    r_nuage = _rej(a_nuage, 75, 155) * k
    r_par5 = pares * 0.155 * 1000 * 3 * 9 / 1e6 * 1.7 * k      # 3 mm a mais de junta em cada par
    r_tampo = _rej(a_tampo, 155, 155, dens=1.6) * k
    r_piso = _rej(a_piso, 1000, 1000) * k
    az = r_bleu + r_nuage
    y2 = f.tab(X2, 150, W2, [('Rejunte · cor', 0.40, 'start'), ('Onde', 0.36, 'start'), ('kg c/ 10%', 0.24, 'end')], [
        ('Acrílico Quartzolit — azul-marinho (próximo do Bleu Nuit)', 'todas as juntas de 2 mm das paredes, do nicho, da saia e da lateral, inclusive em volta dos pares Nuage',
         '%s: compra %d kg' % (br(az), math.ceil(az))),
        ('Acrílico Quartzolit — claro (próximo do Nuage)', 'só a junta de 5 mm entre as duas Nuage de cada par', '%s: compra 1 kg' % br(r_par5)),
        ('Epóxi — azul-marinho', 'tampo da bancada', '%s: compra 1 kg' % br(r_tampo)),
        ('Acrílico Quartzolit — próximo do Confete', 'piso', '%s: compra 1 kg' % br(r_piso)),
    ], titulo='REJUNTE POR COR', alt=16.0)
    y2 = f.par(X2, y2 + 22, W2, [
        ('Conta.', 'kg = área × (A + B) / (A × B) × espessura × junta × densidade (1,7 acrílico; 1,6 epóxi). Espessura das peças adotada: 9 mm. '
         'Rejunte vende em potes de 1 kg: arredondado para cima.'),
        ('Cor da junta do par.', 'Com rejunte claro na junta de 5 mm, o par Nuage lê como uma peça clara só. Se preferir ver as duas faixas, use o azul também ali '
         '(some 1 kg ao azul e corte a linha do claro). Escolher pela cartela com as peças na mão.'),
    ], size=8.2, lh=11.6)
    cantos = 2.50 + 2.00 + 2 * 1.17
    f.tab(X2, y2 + 18, W2, [('Perfil de metal', 0.40, 'start'), ('Medida', 0.30, 'start'), ('Compra', 0.30, 'end')], [
        ('Canto — quina externa da área técnica', '2,50 m (piso ao forro)', ''),
        ('Canto — bancada (frente + lateral)', '2,00 m', ''),
        ('Canto — bordas do nicho (base e teto)', '2 × 1,17 = 2,34 m', ''),
        ('Perfil de canto, total', '%s m + 10%% = %s m' % (br(cantos), br(cantos * k)), '%d barras de 3 m' % math.ceil(cantos * k / 3.0)),
        ('Transição de piso na porta P02', '0,80 m (3 mm à vista)', '1 barra de 1 m'),
    ], titulo='PERFIS DE METAL', alt=16.0)
    f.t(X2, 905, 'Perfil de canto: alumínio anodizado ou inox, 10 mm, mesmo acabamento dos metais. Espaçador de 5 mm: 1 pacote.', 7.8, INK_SOFT)
    return f


def bt07():
    f = Folha(CAD, 'BT-07', 'Liberações, pendências e riscos', 'O que precisa de decisão do cliente, o que a obra confere e o que pode travar o serviço.')
    y = f.tab(X1, 150, W1, [('Nº', 0.06, 'start'), ('Pendência', 0.56, 'start'), ('Quem decide', 0.18, 'start'), ('Até quando', 0.20, 'end')], [
        ('1', 'Área técnica: encostada no fundo do box ou no vidro?', 'cliente', 'antes da paginação'),
        ('2', 'Bancada: encostada no vidro do box ou na parede do vaso?', 'cliente', 'antes de fabricar'),
        ('3', 'Topo da bancada a +980 com cuba de apoio (borda a +1140): confirmar ou trocar a cuba', 'cliente', 'antes de fabricar'),
        ('4', 'Bleu Nuit aceito em tampo pelo fabricante? Base atual firme?', 'loja / obra', 'antes de revestir'),
        ('5', 'Base do espelho a +1340 e reaproveitamento do espelho existente', 'cliente', 'antes do revestimento'),
        ('6', 'Aprovar a posição dos pares Nuage (BE-12 a BE-17)', 'cliente', 'antes de assentar'),
        ('7', 'Folha F01 da FAS e aprovação do projeto de iluminação', 'cliente / FAS', 'antes do forro'),
        ('8', 'Guarnição de 50 mm na porta P02 (esconde a tira sobre o vão)', 'fornecedor da porta', 'com o pedido da porta'),
        ('9', 'Produto de impermeabilização e responsável técnico', 'empreiteira', 'antes da demolição'),
        ('10', 'Antiderrapante do Confete no box', 'cliente / loja', 'antes da compra'),
    ], titulo='PENDÊNCIAS')
    f.tab(X1, y + 30, W1, [('Liberação', 0.34, 'start'), ('O que se confere', 0.66, 'start')], [
        ('Medição pós-demolição', 'medidas da BT-02 anotadas; plantas corrigidas se preciso'),
        ('Água quente', 'teste de pressão com rasgo aberto; água quente chegando à pia'),
        ('Níveis', 'queda de esgoto garantida; base no nível alvo; caimentos feitos'),
        ('Impermeabilização', 'ensaio de 72 horas registrado'),
        ('Rejunte', '5 dias de espera antes de molhar (Quartzolit)'),
        ('Entrega', 'todos os pontos de água, luz e esgoto testados'),
    ], titulo='LIBERAÇÕES (BE-18)')
    y2 = f.tab(X2, 150, W2, [('Risco', 0.44, 'start'), ('Como tratar', 0.56, 'start')], [
        ('Rebaixo raso: esgoto sem queda no nível da casa', 'medir depois da demolição; decidir com o cliente entre subir o piso ou reduzir caimento'),
        ('Aquecedor não acende com a vazão da pia', 'testar antes de fechar a parede; avaliar com o instalador'),
        ('Área técnica é prumada do condomínio', 'não demolir; acesso só pela tampa de inspeção'),
        ('Altura do forro insuficiente para a FAS', 'medir a laje; folga de projeto é de 5 mm'),
        ('Medidas internas diferentes das adotadas', 'liberação de medição antes de cortar qualquer peça'),
        ('Lote de revestimento com calibre diferente', 'medir peças reais; refazer a malha se o módulo mudar'),
        ('Retorno curto do piso junto ao ralo linear', 'acompanhar a borda do ralo; decidir com o responsável técnico'),
    ], titulo='RISCOS')
    f.par(X2, y2 + 26, W2, [
        ('Limite deste caderno.', 'É orientação de escopo, não laudo nem projeto legal. Estrutura, impermeabilização, gás e instalações pedem '
         'responsável técnico em obra e as aprovações do condomínio. Nenhuma medida foi conferida por quem redigiu estas folhas: '
         'vêm do cliente, do modelo R95 e do scan.'),
        ('Outros documentos.', 'O Caderno Alternativo A (REV. T) traz o banheiro dentro do pavimento. As pranchas 08 e 10 dele são anteriores '
         'às medidas de 14/11: para o banheiro, valem estes dois cadernos.'),
    ], size=8.6, lh=12.2)
    return f


FOLHAS = [bt01, bt02, bt03, bt04, bt05, bt06, bt06b, bt07]
