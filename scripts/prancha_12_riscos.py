# -*- coding: utf-8 -*-
"""Prancha 12 — Análise técnica: riscos, impasses e verificações.

Leitura crítica do conjunto, na posição de escritório com engenheiro na
equipe. Separa o que é risco de custo, o que é risco técnico e o que é
impasse — decisão que trava serviço se não for respondida antes.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa

REV = 'REV. M'
PRANCHA = 'Prancha 12 / 12'

# grau: 'impasse' | 'alto' | 'medio'
RISCOS = [
    ('E1', 'Estrutura', 'Piscina de 5,76 m² sobre a sala, em laje que a D07 vai expor',
     'impasse'),
    ('E2', 'Estrutura', 'Condição real da laje só aparece depois do forro sair — P03 é escopo aberto',
     'alto'),
    ('E3', 'Estrutura', 'Toda fixação de trilho, perfilado e evaporadora fura estrutura',
     'medio'),
    ('H1', 'Hidráulica', 'Rebaixo do banheiro: caimento do esgoto contra a cota única',
     'impasse'),
    ('H2', 'Hidráulica', 'Sem degrau, a contenção passa a ser caimento e ralo linear',
     'alto'),
    ('H3', 'Hidráulica', 'D04 pode abrir shaft de prumada — prumada é do condomínio',
     'alto'),
    ('H4', 'Hidráulica', 'Pressão e água quente não levantadas; o chuveiro depende delas',
     'medio'),
    ('L1', 'Elétrica', 'Folha da porta de entrada varre o quadro de distribuição',
     'impasse'),
    ('L2', 'Elétrica', 'Condensadora existente: modelo e nº de evaporadoras desconhecidos',
     'alto'),
    ('L3', 'Elétrica', 'Demanda nova sobre instalação de 17 anos — quadro e ramal a dimensionar',
     'alto'),
    ('L4', 'Elétrica', 'Faixa de 1,00 m a leste do vão da porta de correr é reservada',
     'medio'),
    ('A1', 'Acabamento', 'Monolítico de 56,50 m² não existe sem junta de movimentação',
     'alto'),
    ('A2', 'Acabamento', 'Cumaru sobre contrapiso de 17 anos: umidade e folga de movimentação',
     'medio'),
    ('A3', 'Acabamento', 'P06 pode não bastar: contrapiso trincado pede autonivelante',
     'medio'),
    ('C1', 'Condomínio', 'Rota de descarte da coifa pode não existir',
     'impasse'),
    ('C2', 'Condomínio', 'Exaustor do banheiro: mesma pergunta de rota e fachada',
     'alto'),
    ('D1', 'Documento', 'Duas séries numeradas / 08 circulando — resolvido nesta emissão',
     'medio'),
    ('D2', 'Documento', 'Altura de parede informada como 1,62 / 1,42 é impossível com janela de 1,63',
     'alto'),
]

IMPASSES = [
    ('H1', 'O rebaixo do banheiro contra a cota única',
     ['A D03 retira piso, base e rebaixo até a laje, e a P05 manda o banheiro voltar na cota da',
      'casa. O esgoto mora nesse rebaixo. Ao subir o piso, impermeabilização, regularização com',
      'caimento e piso acabado têm de caber entre a laje e a cota única — e o esgoto tem de',
      'manter queda até a prumada. Sobre 2,64 m, 1% de caimento já consome 2,6 cm.',
      'Se o rebaixo for raso, ou a cota única cai, ou o caimento cai. Não dá para ter os dois.',
      'PORTÃO: medir o desnível real e a cota de saída do esgoto no dia seguinte à D03,',
      'antes de comprar impermeabilizante, piso ou ralo.']),
    ('L1', 'A porta de entrada varre o quadro',
     ['O quadro fica junto à porta, no início da extensão da cozinha. Com 1,00 m de vão, a folha',
      'tem 1,00 m de raio e passa sobre ele. A NBR 5410 exige acesso livre e permanente ao quadro.',
      'São três saídas, e todas custam: deslocar o quadro, reduzir a folha, ou inverter o giro.',
      'PORTÃO: decidir antes da IN1, porque todo o traçado embutido sai dali.']),
    ('C1', 'A coifa pode não ter para onde descarregar',
     ['A vazão de 279,8 m³/h pressupõe duto próprio até uma saída permitida. Se o condomínio não',
      'tiver shaft de cozinha nem autorizar furo de fachada, a coifa vira recirculação com carvão',
      'ativado — e aí a conta de vazão não vale mais, o filtro vira manutenção periódica e a',
      'cozinha integrada passa a conviver com o odor.',
      'PORTÃO: consultar o condomínio antes de escolher a coifa e antes de fechar a marcenaria.']),
]

NOTAS = [
    ['**A piscina é o item que merece a primeira visita técnica.',
     'São 5,76 m² de lâmina sobre a sala. Enquanto havia forro, qualquer infiltração ficava',
     'escondida; com a laje aparente, mancha e eflorescência passam a ser o acabamento. Antes de',
     'assumir concreto à vista na sala, pedir ao condomínio o projeto estrutural e a data da',
     'última impermeabilização da piscina, e inspecionar a face inferior logo após a D07.'],
    ['**A escada aberta contamina a conta de ar.',
     'Os dois pavimentos trocam ar livremente, então dimensionar o MainFloor isolado é otimista.',
     'É por isso que a seleção vai pela coluna base sol, e ainda assim com ressalva.'],
    ['**Nada aqui é laudo.',
     'É leitura de projeto sobre levantamento digital, sem vistoria, sem ensaio e sem acesso aos',
     'projetos do edifício. Os ensaios E01 e E02 respondem a condição das instalações; a laje, a',
     'piscina e o esgoto pedem engenheiro em campo. Esta folha diz o que perguntar e quando — não',
     'substitui quem responde.'],
]

COR_GRAU = {'impasse': DEMO, 'alto': AMARELO, 'medio': BRANCO}
NOME_GRAU = {'impasse': 'IMPASSE', 'alto': 'ATENÇÃO', 'medio': 'ACOMPANHAR'}


def registro(d, x, y, largura):
    d.txt(x, y - 10, 'REGISTRO DE RISCO — CONJUNTO DO PROJETO', 8.0, INK_SOFT, 'bold', ls=1.2)
    d.rect(x, y, largura, 20, fill=K12)
    for tx, rot, al in ((x + 8, 'ID', 'start'), (x + 46, 'Disciplina', 'start'),
                        (x + 150, 'Ponto', 'start'), (x + largura - 8, 'Grau', 'end')):
        d.txt(tx, y + 13.5, rot, 8.2, INK_SOFT, 'bold', al, ls=0.6)
    yy = y + 20
    alt = 25.0
    for i, (ident, disc, texto, grau) in enumerate(RISCOS):
        if i % 2 == 1:
            d.rect(x, yy, largura, alt, fill=K04)
        d.txt(x + 8, yy + 16, ident, 8.6, INK, 'bold')
        d.txt(x + 46, yy + 16, disc, 8.4, INK_SOFT)
        d.txt(x + 150, yy + 16, texto, 8.4, INK)
        # selo de grau
        sw = 62.0
        sx = x + largura - sw - 8
        d.rect(sx, yy + 5.5, sw, 14, fill=COR_GRAU[grau], stroke=K,
               sw=1.4 if grau == 'impasse' else 0.8)
        d.txt(sx + sw / 2.0, yy + 15.6, NOME_GRAU[grau], 6.6,
              BRANCO if grau == 'impasse' else K, 'bold', 'middle', ls=0.5)
        d.line(x, yy + alt, x + largura, yy + alt, RULE, 0.6, opacity=0.8)
        yy += alt
    return yy


def bloco_impasse(d, x, y, largura, ident, titulo, linhas):
    alt = 42 + len(linhas) * 11.6
    d.rect(x, y, largura, alt, fill=MAGENTA18, stroke=DEMO, sw=1.4)
    d.rect(x, y, 34, 20, fill=DEMO)
    d.txt(x + 17, y + 14, ident, 8.6, BRANCO, 'bold', 'middle', ls=0.4)
    d.txt(x + 42, y + 14, titulo, 9.2, K, 'bold')
    yy = y + 33
    for ln in linhas:
        forte = ln.startswith('PORTÃO:')
        d.txt(x + 12, yy, ln, 8.1, DEMO if forte else INK, 'bold' if forte else 'normal')
        yy += 11.6
    return y + alt + 14


def construir():
    d = folha_nova()
    cabecalho(d, 'Análise técnica: riscos, impasses e verificações',
              'Leitura crítica do conjunto. Separa risco de custo, risco técnico e impasse — a decisão que trava serviço se não for respondida antes de começar.',
              REV, '18 pontos  ·  3 impasses',
              'orientação de escopo, não laudo')

    cx, cw = MARGIN, 700
    fim = registro(d, cx, 162, cw)
    paragrafos(d, cx, fim + 34, cw, NOTAS, size=8.4, lh=12.1, gap=7.0)

    d.line(776, 140, 776, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 806, W - MARGIN - 806
    d.txt(cx2, 152, 'OS TRÊS IMPASSES', 8.0, INK_SOFT, 'bold', ls=1.2)
    d.txt(cx2, 170, 'Cada um trava um serviço. Nenhum se resolve', 8.4, INK_SOFT)
    d.txt(cx2, 182, 'no desenho — os três pedem campo ou terceiro.', 8.4, INK_SOFT)
    yy = 200
    for (ident, titulo, linhas) in IMPASSES:
        yy = bloco_impasse(d, cx2, yy, cw2, ident, titulo, linhas)

    rodape(d,
           'Análise sobre levantamento digital de 02.09.2026 e sobre as decisões registradas até a REV. M. Sem vistoria, sem ensaio e sem acesso aos projetos do edifício.',
           'Orientação de escopo, não laudo. A decisão final sobre estrutura, impermeabilização e instalações pede engenheiro responsável em inspeção.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-12-riscos')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-12-riscos-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 12: riscos, impasses e verificações')
    exportar_png(caminho, os.path.join(pasta, 'prancha-12-riscos.png'))
    print('ok prancha 12')
