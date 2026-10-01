# -*- coding: utf-8 -*-
"""Prancha 14 — Programação da obra: quem entra quando (REV. O)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_mainfloor import *      # noqa
import programacao as pg

REV = 'REV. O'
PRANCHA = 'Prancha 14 / 14'

NOTAS = [
    ['**A ordem é fixa; as durações, não.',
     'Cada contratada preenche os seus prazos no cronograma. O que não muda é a sequência: ninguém',
     'entra antes de a fase anterior entregar a frente limpa, e nenhuma fase começa com a decisão',
     'do losango em aberto.'],
    ['**O banheiro é o caminho crítico.',
     'Reforma completa — paredes, piso e teto. Passa por cinco fornecedores em sequência:',
     'hidráulica, forro novo R03 com embutidos e exaustor, impermeabilização, revestimento e,',
     'por último, pedra, vidro do box, louças e metais. Atraso em um empurra todos os outros.'],
    ['**Pedras e vidro medem sobre o revestimento pronto.',
     'O orçamento sai das medidas da FO7; o corte, só do gabarito tirado em obra depois do',
     'revestimento. A opção B do box pede perfis na parede R02 antes de revestir — por isso',
     'a escolha A ou B fecha antes da fase 5.'],
    ['**Trilho, cortina, portas e luminárias só depois da pintura.',
     'O trilho CT01 e o da porta P03 vão na laje pintada; o perfil PF1 e os apoios da cortina',
     'entram antes, com a espera T18 da claraboia. O fechamento elétrico é de 2027/28 e só usa',
     'o que fica pronto agora.'],
]


def construir():
    d = folha_nova()
    cabecalho(d, 'Programação da obra',
              'Quem entra quando: as fases da obra, os fornecedores em cada uma e as decisões que precisam estar fechadas antes de cada fase.',
              REV, '14 frentes · 9 fases · 5 decisões',
              'durações a preencher com as contratadas')
    fim = pg.desenhar(d, MARGIN, 140, W - 2 * MARGIN, alt=37.0)
    pg.legenda_programacao(d, MARGIN, fim + 6)
    # notas em duas colunas
    cw = (W - 2 * MARGIN - 40) / 2.0
    paragrafos(d, MARGIN, fim + 34, cw, NOTAS[:2], size=8.2, lh=11.2, gap=5.0)
    paragrafos(d, MARGIN + cw + 40, fim + 34, cw, NOTAS[2:], size=8.2, lh=11.2, gap=5.0)
    rodape(d,
           'Sequência de referência sobre o escopo do caderno REV. O. Não substitui o cronograma físico das contratadas nem a programação do condomínio.',
           'Fases sem fornecedor marcado não exigem presença daquela disciplina. Alterações de escopo mudam a sequência: revisar esta folha a cada revisão.',
           PRANCHA, REV)
    return d


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta = os.path.join(raiz, 'pranchas')
    caminho = salvar(construir(), pasta, 'prancha-14-programacao')
    exportar_pdf_a3([caminho], os.path.join(pasta, 'prancha-14-programacao-A3.pdf'),
                    'MaxHaus MainFloor — Prancha 14: programação da obra')
    exportar_png(caminho, os.path.join(pasta, 'prancha-14-programacao.png'))
    print('ok prancha 14')
