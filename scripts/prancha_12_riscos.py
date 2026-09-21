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

# grau: 'impasse' | 'curso' | 'alto' | 'medio' | 'ok'
RISCOS = [
    ('E1', 'Estrutura', 'Piscina de 5,76 m² sobre a sala, em laje que a D07 vai expor',
     'curso'),
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
    ('L1', 'Elétrica', 'Quadro atrás da folha aberta — acesso confirmado pelo cliente em 21.09',
     'ok'),
    ('L2', 'Elétrica', 'Condensadora existente: modelo e nº de evaporadoras desconhecidos',
     'alto'),
    ('L3', 'Elétrica', 'Demanda nova sobre instalação de 17 anos — quadro e ramal a dimensionar',
     'alto'),
    ('L4', 'Elétrica', 'Faixa de 1,00 m a leste do vão da porta de correr é reservada',
     'medio'),
    ('A1', 'Acabamento', 'Monolítico cimentício de 56,50 m² pede juntas — quantas depende do sistema',
     'alto'),
    ('A2', 'Acabamento', 'Cumaru sobre contrapiso de 17 anos: umidade e folga de movimentação',
     'medio'),
    ('A3', 'Acabamento', 'P06 pode não bastar: contrapiso trincado pede autonivelante',
     'medio'),
    ('C1', 'Condomínio', 'Rota de descarte da coifa pode não existir',
     'curso'),
    ('C2', 'Condomínio', 'Exaustor do banheiro: mesma pergunta de rota e fachada',
     'alto'),
    ('D1', 'Documento', 'Duas séries numeradas / 08 circulando — resolvido na REV. M',
     'ok'),
    ('D2', 'Documento', 'Altura de parede: erro de digitação confirmado — 2,40 com forro, 2,62 sem',
     'ok'),
]

IMPASSES = [
    ('H1', 'IMPASSE', 'O rebaixo do banheiro contra a cota única',
     'em análise com a empreiteira',
     ['A D03 retira piso, base e rebaixo até a laje, e a P05 manda o banheiro voltar na cota da',
      'casa. O esgoto mora nesse rebaixo. Ao subir o piso, impermeabilização, regularização com',
      'caimento e piso acabado têm de caber entre a laje e a cota única — e o esgoto tem de',
      'manter queda até a prumada. Sobre 2,64 m, 1% de caimento já consome 2,6 cm.',
      'Se o rebaixo for raso, ou a cota única cai, ou o caimento cai. Não dá para ter os dois.',
      'PORTÃO: medir o desnível real e a cota de saída do esgoto no dia seguinte à D03,',
      'antes de comprar impermeabilizante, piso ou ralo.']),
    ('E1', 'EM CURSO', 'A piscina sobre a sala',
     'visita técnica agendada · condomínio em contato',
     ['São 5,76 m² de lâmina sobre a sala. Enquanto havia forro, qualquer infiltração ficava',
      'escondida; com a laje aparente, mancha e eflorescência passam a ser o acabamento.',
      'O QUE LEVAR NA VISITA: projeto estrutural do trecho, data e sistema da última',
      'impermeabilização da piscina, e histórico de manutenção. Inspecionar a face inferior',
      'logo após a D07, antes de assumir concreto à vista na sala.']),
    ('C1', 'EM CURSO', 'A rota de descarte da coifa',
     'em alinhamento com a construtora',
     ['A vazão de 279,8 m³/h pressupõe duto próprio até uma saída permitida. Sem shaft de cozinha',
      'nem autorização de furo de fachada, a coifa vira recirculação com carvão ativado — a conta',
      'de vazão deixa de valer, o filtro vira manutenção periódica e a cozinha integrada convive',
      'com o odor.',
      'O QUE PERGUNTAR: existe shaft de exaustão de cozinha na prumada da unidade, e a fachada',
      'admite furo? Resolver antes de escolher a coifa e antes de fechar a marcenaria.']),
]

RESOLVIDOS = [
    ('L1', 'Quadro atrás da folha da porta',
     'O cliente confirmou em 21.09 que o arranjo é comum no edifício e o acesso é fácil — o quadro',
     'fica atrás da folha quando aberta. Decisão registrada. Resta só conferir que a porta do',
     'próprio quadro abre sem bater no batente.'),
    ('D2', 'A altura de parede',
     'Era erro de digitação. O cliente confirmou: 2,40 m com o forro atual e 2,62 m sem ele. O',
     'caderno inteiro foi recalculado nesta revisão — plenum passa a 0,22 m, o revestimento do',
     'banheiro a 2,40 m e a exaustão a 91,2 m³/h.'),
]

NOTAS = [
    ['**Juntas no piso monolítico: a pergunta certa é qual sistema, não se tem junta.',
     'Cimentício — cimento queimado, concreto polido, autonivelante aparente — retrai ao curar e',
     'acompanha o movimento da laje: pede painéis de 3 a 6 m de lado, o que dá de 4 a 8 juntas',
     'nos 56,50 m². Microcimento de 2 a 3 mm, com tela e primer, reduz as juntas às do substrato',
     'e ao perímetro. Resina epóxi ou poliuretano fecha contínuo de verdade — mas parece resina,',
     'não concreto. Em qualquer um deles, junta sobre junta estrutural é obrigatória.'],
    ['**A escada aberta contamina a conta de ar.',
     'Os dois pavimentos trocam ar livremente, então dimensionar o MainFloor isolado é otimista.',
     'É por isso que a seleção vai pela coluna base sol, e ainda assim com ressalva.'],
    ['**Nada aqui é laudo.',
     'É leitura de projeto sobre levantamento digital, sem vistoria, sem ensaio e sem acesso aos',
     'projetos do edifício. Os ensaios E01 e E02 respondem a condição das instalações; a laje, a',
     'piscina e o esgoto pedem engenheiro em campo. Esta folha diz o que perguntar e quando — não',
     'substitui quem responde.'],
]

COR_GRAU = {'impasse': DEMO, 'curso': CIANO, 'alto': AMARELO,
            'medio': BRANCO, 'ok': K12}
NOME_GRAU = {'impasse': 'IMPASSE', 'curso': 'EM CURSO', 'alto': 'ATENÇÃO',
             'medio': 'ACOMPANHAR', 'ok': 'RESOLVIDO'}


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


def bloco_impasse(d, x, y, largura, ident, selo, titulo, dono, linhas):
    aberto = (selo == 'IMPASSE')
    fundo = MAGENTA18 if aberto else CIANO18
    borda = DEMO if aberto else CIANO
    alt = 54 + len(linhas) * 11.6
    d.rect(x, y, largura, alt, fill=fundo, stroke=borda, sw=1.4)
    d.rect(x, y, 34, 20, fill=borda)
    d.txt(x + 17, y + 14, ident, 8.6, BRANCO if aberto else K, 'bold', 'middle', ls=0.4)
    d.txt(x + 42, y + 14, titulo, 9.2, K, 'bold')
    d.txt(x + largura - 10, y + 14, selo, 7.0, K, 'bold', 'end', ls=0.6)
    d.txt(x + 12, y + 30, dono, 7.6, INK_SOFT, 'normal')
    yy = y + 45
    for ln in linhas:
        forte = ln.startswith('PORTÃO:') or ln.startswith('O QUE ')
        d.txt(x + 12, yy, ln, 8.1, DEMO if (forte and aberto) else
              (K if forte else INK), 'bold' if forte else 'normal')
        yy += 11.6
    return y + alt + 12


def bloco_resolvido(d, x, y, largura, itens):
    d.txt(x, y - 10, 'RESOLVIDOS EM 21.09', 8.0, INK_SOFT, 'bold', ls=1.2)
    yy = y
    for (ident, titulo, *linhas) in itens:
        d.rect(x, yy, largura, 18 + len(linhas) * 11.2, fill=K04, stroke=K20, sw=0.8)
        d.rect(x, yy, 30, 16, fill=K45)
        d.txt(x + 15, yy + 11.5, ident, 7.6, BRANCO, 'bold', 'middle', ls=0.4)
        d.txt(x + 38, yy + 11.5, titulo, 8.4, K, 'bold')
        y2 = yy + 27
        for ln in linhas:
            d.txt(x + 12, y2, ln, 7.9, INK_SOFT)
            y2 += 11.2
        yy += 18 + len(linhas) * 11.2 + 10
    return yy


def construir():
    d = folha_nova()
    cabecalho(d, 'Análise técnica: riscos, impasses e verificações',
              'Leitura crítica do conjunto. Separa risco de custo, risco técnico e impasse — a decisão que trava serviço se não for respondida antes de começar.',
              REV, '18 pontos  ·  1 impasse aberto',
              '2 em curso  ·  3 resolvidos em 21.09')

    cx, cw = MARGIN, 700
    fim = registro(d, cx, 162, cw)
    paragrafos(d, cx, fim + 34, cw, NOTAS, size=8.4, lh=12.1, gap=7.0)

    d.line(776, 140, 776, 916, RULE, 0.8, opacity=0.8)
    cx2, cw2 = 806, W - MARGIN - 806
    d.txt(cx2, 152, 'O QUE TRAVA SERVIÇO', 8.0, INK_SOFT, 'bold', ls=1.2)
    d.txt(cx2, 170, 'Um impasse aberto e dois em curso, já com dono.', 8.4, INK_SOFT)
    d.txt(cx2, 182, 'Nenhum se resolve no desenho: os três pedem campo.', 8.4, INK_SOFT)
    yy = 200
    for (ident, selo, titulo, dono, linhas) in IMPASSES:
        yy = bloco_impasse(d, cx2, yy, cw2, ident, selo, titulo, dono, linhas)
    bloco_resolvido(d, cx2, yy + 18, cw2, RESOLVIDOS)

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
