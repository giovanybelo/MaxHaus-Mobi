# -*- coding: utf-8 -*-
"""Seis estudos exclusivos para sala, hall e cozinha (nov/2026), a partir da pasta do Pinterest
"maxhaus-mobi" do cliente (35 pins, 21 usados como referência).

  E1 · Freijó & Grafite      pins 03, 10, 12, 22
  E2 · Jardim Zenital        pins 26, 28, 34
  E3 · Cobalto Bauhaus       pins 11, 20, 24, 27
  E4 · Oliva & Terracota     pins 14, 16, 30, 32
  E5 · Biblioteca Noir       pins 23, 29, 35
  E6 · Navy & Caramelo       pins 02, 31, 33

Premissas fixas: laje de concreto aparente, claraboia na posição da planta, sol da tarde pela
fachada noroeste, escada, cozinha linear com geladeira inox, porcelanato na cozinha e monolítico no
resto, persianas horizontais de madeira.

Renders no Magnific (Nano Banana 2.1, 2K) sobre as bases do modelo, em estudos/sala-2026-11/img.
Saída: dois PDFs A3 (volume 1: E1–E3, volume 2: E4–E6), cada um abaixo de 3 MB.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.dirname(AQUI))
import pranchas as pc                                   # noqa: E402  (helpers do estudo de cores)
from base_mainfloor import (W, MARGIN, K20, K12, INK, INK_SOFT, RULE, DEMO, BRANCO,  # noqa: E402
                            folha_nova, salvar, exportar_pdf_a3)

RAIZ = os.path.dirname(os.path.dirname(AQUI))
PASTA = os.path.join(RAIZ, 'estudos', 'sala-2026-11')
IMG = os.path.join(PASTA, 'img')
REF = os.path.join(PASTA, 'ref')
pc.TMP = os.path.join(PASTA, '_tmp')
DATA = '18/11/2026'
TITULO_CAD = 'SEIS ESTUDOS · SALA, HALL E COZINHA'

VISTAS = [('1', 'hall', 'Entrada e hall, com a escada e a claraboia', '1'),
          ('2', 'living', 'Living: sofá, jantar e a fachada noroeste', '2'),
          ('3', 'tv', 'Sala de TV (parede do banheiro)', '3'),
          ('4', 'jantar', 'Jantar', '4'),
          ('5', 'cozinha', 'Cozinha linear: geladeira inox, cuba, cooktop', '6')]

E = {
    'E1': dict(
        nome='Freijó & Grafite', pins=['03', '12', '22', '10'],
        sub='Paredes forradas de freijó, pedra grafite, globos de vidro opalino: o modernismo brasileiro calmo.',
        conceito=('A madeira sobe pelas paredes: painéis verticais de freijó envolvem o jantar e a parede da TV e dão '
                  'calor à laje bruta. A pedra preta (mesa e cozinha) segura o conjunto, e os globos opalinos, em cacho, '
                  'repetem a luz da claraboia. Tecidos em aveia e couro conhaque, poucas peças e bem escolhidas.'),
        paleta=[('Freijó', '#B07A4A', 'painéis, persianas'), ('Grafite', '#2B2B2B', 'pedra, serralheria'),
                ('Off-white quente', '#EEE8DE', 'paredes lisas'), ('Aveia', '#D8CDB9', 'sofá, linho'),
                ('Conhaque', '#9A5A2E', 'couro, cadeiras'), ('Opalino', '#F7F5F0', 'globos de vidro')],
        piso=[('Cinza quente', '#B9B3A9', 'proposto'), ('Greige', '#C9C0B2', 'alternativa'), ('Cimento', '#A7A39C', 'alternativa')],
        materiais=[('Paredes', 'painel ripado/liso de freijó no jantar e na TV; resto em off-white quente'),
                   ('Persianas', 'madeira 50 mm, freijó'),
                   ('Cozinha', 'freijó nas portas, Nero Marquina na bancada e no frontão, metais pretos'),
                   ('Mobiliário', 'sofá modular de linho aveia, poltrona de couro conhaque, mesa de pedra grafite, cadeiras ripadas'),
                   ('Luz', 'cacho de globos opalinos no jantar, trilho preto na laje')]),
    'E2': dict(
        nome='Jardim Zenital', pins=['26', '28', '34'],
        sub='A claraboia vira jardim: verdes pendentes, nogueira escura, concreto e couro.',
        conceito=('A claraboia é o centro: um jardim suspenso de samambaias e pendentes cai da abertura e recebe a luz '
                  'zenital. Em volta, um loft calmo em concreto, nogueira escura e cinza-chumbo, com couro conhaque e pendentes '
                  'pretos. É a proposta que mais tira partido da piscina sobre a sala.'),
        paleta=[('Concreto', '#9C9A94', 'paredes, piso'), ('Nogueira escura', '#4E3424', 'marcenaria, persianas'),
                ('Chumbo', '#3A3B3D', 'sofá, tapete'), ('Conhaque', '#9A5A2E', 'poltrona de couro'),
                ('Verde-folha', '#4F6B3A', 'jardim suspenso'), ('Preto', '#1C1C1C', 'pendentes, serralheria')],
        piso=[('Cimento médio', '#9E9C96', 'proposto'), ('Cinza-claro', '#B8B6B0', 'alternativa'), ('Grafite', '#77756F', 'alternativa')],
        materiais=[('Paredes', 'massa cinza efeito concreto; uma parede terracota no jantar'),
                   ('Persianas', 'madeira 50 mm, nogueira escura'),
                   ('Cozinha', 'nogueira escura, granito Cinza Absoluto levigado, prateleira-trilho preta com ervas'),
                   ('Mobiliário', 'sofá modular chumbo, poltrona de couro conhaque, mesa de nogueira, cadeiras de aço preto'),
                   ('Claraboia', 'floreira suspensa no entorno, irrigação por gotejamento e luz de cultivo embutida')]),
    'E3': dict(
        nome='Cobalto Bauhaus', pins=['27', '24', '11', '20'],
        sub='Teca nas paredes, veludo cobalto, ferrugem e listras em vermelho e azul: Bauhaus com calor.',
        conceito=('A mais ousada: o azul-cobalto em veludo é o protagonista, sobre painéis de teca e piso creme. Ferrugem e '
                  'vermelho aparecem no tapete de listras diagonais, nas gravuras e no pendente. A cozinha leva o mesmo '
                  'cobalto em laca nos armários de baixo e conversa com o Bleu Nuit do banheiro.'),
        paleta=[('Cobalto', '#1F3FA6', 'sofá, laca da cozinha'), ('Teca', '#9A5B33', 'painéis, persianas'),
                ('Ferrugem', '#B0502A', 'parede, poltrona'), ('Vermelho', '#B8262E', 'tapete, pendente'),
                ('Creme', '#EFE7D7', 'piso, tapete'), ('Branco', '#F6F4EE', 'quartzo, mesa tulipa')],
        piso=[('Creme', '#E3D9C6', 'proposto'), ('Marfim', '#EAE3D4', 'alternativa'), ('Areia', '#D3C6AE', 'alternativa')],
        materiais=[('Paredes', 'painéis de teca; parede ferrugem atrás da TV'),
                   ('Persianas', 'madeira 50 mm, teca'),
                   ('Cozinha', 'inferiores laca cobalto, superiores teca, quartzo branco, metais escovados'),
                   ('Mobiliário', 'sofá de veludo cobalto, poltrona ferrugem, mesa tulipa branca, cadeiras de teca com assento cobalto'),
                   ('Arte e luz', 'gravuras pop em cores primárias, luminária de papel, pendente vermelho')]),
    'E4': dict(
        nome='Oliva & Terracota', pins=['16', '30', '14', '32'],
        sub='Mid-century quente: verde-oliva, terracota, nogueira, latão e a poltrona Eames.',
        conceito=('Um mid-century acolhedor: paredes verde-oliva e uma terracota, sofá curvo de bouclé oliva, poltronas de '
                  'veludo terracota e uma lounge de couro preto e nogueira. Nichos em arco iluminados, aparadores de '
                  'nogueira, lustre sputnik de latão e arte orgânica em laranja e verde. A cozinha vai para travertino e nogueira.'),
        paleta=[('Oliva', '#6E7444', 'paredes, sofá'), ('Terracota', '#B4553A', 'parede, poltronas'),
                ('Nogueira', '#6B4430', 'marcenaria, persianas'), ('Latão', '#B8964F', 'lustre, puxadores'),
                ('Travertino', '#D9C7A6', 'bancada da cozinha'), ('Areia', '#E2D6C2', 'piso, tapete')],
        piso=[('Areia', '#D9CCB6', 'proposto'), ('Bege-claro', '#E3D9C8', 'alternativa'), ('Caramelo claro', '#C9B394', 'alternativa')],
        materiais=[('Paredes', 'verde-oliva na sala e no jantar, terracota na parede das janelas'),
                   ('Persianas', 'madeira 50 mm, nogueira'),
                   ('Cozinha', 'nogueira com puxador de latão, travertino levigado, azulejo branco 10 × 10'),
                   ('Mobiliário', 'sofá curvo de bouclé oliva, poltronas de veludo terracota, lounge de couro e nogueira, mesa oval'),
                   ('Luz e arte', 'sputnik de latão, nichos em arco com LED, gravuras orgânicas laranja e verde')]),
    'E5': dict(
        nome='Biblioteca Noir', pins=['23', '35', '29'],
        sub='Estante-parede laqueada de preto, luz rasante e couro: a sala como biblioteca.',
        conceito=('Uma estante de piso a teto em laca preta fosca, com LED em cada prateleira, ocupa a parede longa e '
                  'emoldura a TV. Paredes carvão, piso grafite e couro conhaque; à tarde o sol corta faixas douradas pelas '
                  'persianas. A cozinha preta ganha um Calacatta como contraste. Pede luz artificial bem desenhada.'),
        paleta=[('Preto fosco', '#1B1B1B', 'estante, cozinha'), ('Carvão', '#3B3A38', 'paredes'),
                ('Grafite', '#55534F', 'piso'), ('Conhaque', '#9A5A2E', 'couro'),
                ('Calacatta', '#EEEBE6', 'bancada, frontão'), ('Latão', '#B8964F', 'metais, luminárias')],
        piso=[('Grafite', '#5B5955', 'proposto'), ('Chumbo', '#6E6C67', 'alternativa'), ('Cimento escuro', '#827F79', 'alternativa')],
        materiais=[('Paredes', 'carvão fosco; estante laqueada preta piso a teto com LED 2700 K'),
                   ('Persianas', 'madeira 50 mm, carvalho fumê'),
                   ('Cozinha', 'laca preta fosca, Calacatta na bancada e no frontão, metais de latão'),
                   ('Mobiliário', 'sofá modular chumbo, poltrona de couro conhaque, mesa de mármore preto, cadeiras de freijó escuro'),
                   ('Atenção', 'é a mais escura: testar em amostra grande antes, sob a luz da tarde')]),
    'E6': dict(
        nome='Navy & Caramelo', pins=['31', '33', '02'],
        sub='Barrado azul-marinho, freijó caramelo e listras: o modernismo brasileiro fresco, ligado ao quarto e ao banheiro.',
        conceito=('Um barrado azul-marinho de 1,10 m corre pelas paredes, com branco em cima, e liga a sala ao Bleu Nuit do '
                  'banheiro e ao quarto. Freijó caramelo na parede da TV e no mobiliário, couro caramelo e palhinha nas cadeiras, '
                  'listras navy e branco nos tecidos. A mais leve e a que melhor amarra a casa toda.'),
        paleta=[('Navy', '#1F2C4A', 'barrado, sofá, cozinha'), ('Branco', '#F5F3EE', 'paredes acima'),
                ('Freijó caramelo', '#B9824E', 'painel da TV, mobiliário'), ('Couro caramelo', '#A8683A', 'poltrona, cadeiras'),
                ('Juta', '#CDB68E', 'tapete'), ('Dolomita', '#ECE9E3', 'bancada da cozinha')],
        piso=[('Off-white', '#E4E1DA', 'proposto'), ('Gelo', '#D9D7D1', 'alternativa'), ('Areia clara', '#DDD3C4', 'alternativa')],
        materiais=[('Paredes', 'barrado navy até 1,10 m, branco acima; painel de freijó na parede da TV'),
                   ('Persianas', 'madeira 50 mm, carvalho claro'),
                   ('Cozinha', 'inferiores laca navy, superiores freijó, Dolomita na bancada, metais de latão escovado'),
                   ('Mobiliário', 'sofá de linho navy, poltrona modernista de couro caramelo, mesa redonda de freijó, cadeiras de palhinha'),
                   ('Liga', 'o navy repete o Gouache Bleu Nuit do banheiro e a cabeceira do quarto')]),
}


def folha(cod, titulo, sub, n, total):
    d = folha_nova()
    d.txt(MARGIN, 42, 'MAXHAUS 81  ·  MAIN FLOOR  ·  ' + TITULO_CAD, 8.6, INK_SOFT, 'bold', ls=1.2)
    d.txt(MARGIN, 78, titulo, 24, INK, 'bold')
    if sub:
        d.txt(MARGIN, 98, sub, 9.2, INK_SOFT)
    d.txt(W - MARGIN, 42, 'ESTUDO  ·  ' + DATA, 8.6, DEMO, 'bold', 'end', ls=0.8)
    d.txt(W - MARGIN, 78, cod, 22, INK, 'bold', 'end')
    d.txt(W - MARGIN, 98, 'prancha %d de %d  ·  A3' % (n, total), 8.4, INK_SOFT, 'normal', 'end')
    d.line(MARGIN, 112, W - MARGIN, 112, RULE, 1.0)
    d.line(MARGIN, 930, W - MARGIN, 930, RULE, 1.0)
    d.txt(MARGIN, 946, 'Imagens de estudo (IA, 2K) sobre as bases do modelo: valem para cor, material e atmosfera, não para medida. '
          'Mobiliário e arte são indicativos; referências do Pinterest do cliente.', 7.4, INK_SOFT)
    d.txt(MARGIN, 958, 'Cores em hexadecimal para conferência em tela: escolher a tinta pelo leque físico do fabricante, sob a luz da casa.', 7.4, INK_SOFT)
    d.txt(MARGIN, 976, 'MAXHAUS 81  ·  JOÃO BALDINATO 109  ·  ESTUDOS DE SALA', 8.2, DEMO, 'bold', ls=0.5)
    d.txt(W - MARGIN, 976, cod + '  ·  ' + DATA, 8.2, INK_SOFT, 'normal', 'end')
    return d


def _planta(d, ox, oy, S, piso_hex, cameras=True):
    pc.PROPOSTAS['_X'] = dict(piso=[('x', piso_hex, '')])
    cams = pc.CAMERAS
    pc.CAMERAS = {v[0]: cams[v[3]] for v in VISTAS} if cameras else {}
    pc.planta(d, ox, oy, S, prop='_X', cameras=cameras)
    pc.CAMERAS = cams


def capa(chaves, n, t, vol):
    d = folha('S-00', 'Seis estudos a partir do Pinterest', 'Volume %d de 2. Os 21 pins usados, a família de cada estudo e as premissas fixas.' % vol, n, t)
    x0, y0 = MARGIN, 134
    cw, gap = 182, 12
    for i, k in enumerate(sorted(E)):
        x = x0 + (i % 3) * (cw * 2 + gap * 2 + 6)
        y = y0 + (i // 3) * 385
        P = E[k]
        d.txt(x, y + 10, '%s · %s' % (k, P['nome'].upper()), 9.6, INK if k in chaves else INK_SOFT, 'bold')
        pins = P['pins'][:3]
        tw = (cw * 2 + gap - 2 * 6) / 3.0
        for j, p in enumerate(pins):
            pc._img(d, os.path.join(REF, 'pin%s.jpg' % p), x + j * (tw + 6), y + 22, tw, tw * 1.7, q=72, px=320)
        hx = x
        for c in P['paleta']:
            d.rect(hx, y + 30 + tw * 1.7, 22, 12, fill=c[1], stroke=K20, sw=0.4)
            hx += 25
        d.txt(x, y + 60 + tw * 1.7, 'pins ' + ', '.join(sorted(P['pins'])), 7.0, INK_SOFT)
    xr = x0 + 3 * (cw * 2 + gap * 2 + 6) - 4
    d.line(xr - 14, 128, xr - 14, 910, K12, 1.0)
    d.txt(xr, y0 + 10, 'FIXO NOS SEIS ESTUDOS', 9.0, INK, 'bold', ls=0.8)
    y = y0 + 32
    wr = W - MARGIN - xr
    for tit, txt in [
        ('Teto.', 'Laje de concreto aparente, selada fosca; trilho de luz aplicado.'),
        ('Piso.', 'Monolítico na sala e no hall (a cor muda por estudo); porcelanato na cozinha e no banheiro.'),
        ('Persianas.', 'Horizontais de madeira, 50 mm; a madeira muda por estudo.'),
        ('Claraboia.', 'Fundo de vidro da piscina, 1,92 × 3,00 m, na posição da planta (ver S-01).'),
        ('Sol.', 'Fachada envidraçada noroeste: sol baixo da tarde entrando em faixas.'),
        ('Fixos.', 'Escada metálica com degraus de madeira; cozinha linear na parede oeste com geladeira inox, cuba e cooktop.'),
        ('Vistas.', 'As mesmas cinco câmeras em todos os estudos, para comparar lado a lado.'),
    ]:
        d.txt(xr, y, tit, 8.6, INK, 'bold')
        y = pc._par(d, xr, y + 13, wr, txt, 8.0, 11.4) + 9
    return d


def chave(n, t):
    d = folha('S-01', 'Planta-chave: claraboia, sol e câmeras', 'Alternativo A com o banheiro E5. As cinco vistas de cada estudo.', n, t)
    _planta(d, 140, 150, 82.0, pc.K07)
    x, y = 930, 160
    d.txt(x, y, 'VISTAS', 9.0, INK, 'bold', ls=0.8)
    y += 22
    for num, _, txt, _c in VISTAS:
        d.circle(x + 8, y - 4, 8, fill=DEMO)
        d.txt(x + 8, y - 0.8, num, 7.6, BRANCO, 'bold', 'middle')
        d.txt(x + 24, y, txt, 8.2, INK)
        y += 20
    y += 20
    for tit, txt in [
        ('Claraboia.', '1,92 × 3,00 m, centro em 6,13 / 3,14 m do canto noroeste; lado longo paralelo à fachada, a ~0,66 m dela.'),
        ('Sol.', 'Fachada de vidro noroeste: sol baixo e quente no fim da tarde, em faixas pelas persianas; luz zenital da claraboia o dia todo.'),
        ('Piso.', 'Monolítico na área seca; porcelanato na cozinha (até a ponta arredondada) e no banheiro.'),
    ]:
        d.txt(x, y, tit, 8.6, INK, 'bold')
        y = pc._par(d, x, y + 13, W - MARGIN - x, txt, 8.0, 11.4) + 8
    return d


def p_conceito(k, n, t):
    P = E[k]
    d = folha(k + '.1', 'Estudo %s · %s' % (k[1], P['nome']), P['sub'], n, t)
    hw = 800
    pc._img(d, os.path.join(IMG, k + '_1_hall.jpg'), MARGIN, 126, hw, hw * 0.75, q=74, px=1500)
    d.circle(MARGIN + 16, 126 + hw * 0.75 + 14, 8, fill=DEMO)
    d.txt(MARGIN + 16, 126 + hw * 0.75 + 17, '1', 7.6, BRANCO, 'bold', 'middle')
    d.txt(MARGIN + 30, 126 + hw * 0.75 + 17, VISTAS[0][2], 8.0, INK_SOFT)
    x = MARGIN + hw + 26
    wr = W - MARGIN - x
    d.txt(x, 138, 'REFERÊNCIAS DO PINTEREST', 9.0, INK, 'bold', ls=0.8)
    np_ = len(P['pins'])
    tw = (wr - (np_ - 1) * 6) / float(np_)
    th = min(tw * 1.33, 120)
    for j, p in enumerate(P['pins']):
        pc._img(d, os.path.join(REF, 'pin%s.jpg' % p), x + j * (tw + 6), 148, tw, th, q=72, px=320)
    y = 148 + th + 24
    d.txt(x, y, 'CONCEITO', 9.0, INK, 'bold', ls=0.8)
    y = pc._par(d, x, y + 18, wr, P['conceito'], 8.2, 11.6) + 8
    d.txt(x, y, 'PALETA', 9.0, INK, 'bold', ls=0.8)
    y += 10
    sw = (wr - 2 * 10) / 3.0
    for i, (nm, hx, uso) in enumerate(P['paleta']):
        pc._swatch(d, x + (i % 3) * (sw + 10), y + (i // 3) * 70, sw, 34, nm, hx, uso)
    y += 2 * 70 + 18
    d.txt(x, y, 'PISO MONOLÍTICO · TONS DE TESTE', 9.0, INK, 'bold', ls=0.8)
    y += 10
    for i, (nm, hx, uso) in enumerate(P['piso']):
        pc._swatch(d, x + i * (sw + 10), y, sw, 26, nm, hx, uso)
    y += 26 + 46
    d.txt(x, y, 'MATERIAIS', 9.0, INK, 'bold', ls=0.8)
    y += 15
    for kk, v in P['materiais']:
        d.txt(x, y, kk, 7.8, INK, 'bold')
        y = pc._par(d, x + 78, y, wr - 78, v, 7.5, 10.4) + 3
    return d


def p_vistas(k, n, t):
    P = E[k]
    d = folha(k + '.2', 'Estudo %s · living, TV, jantar e cozinha' % k[1], P['nome'] + ': vistas 2 a 5 da planta-chave.', n, t)
    w, h = 560, 360
    for i, (num, ch, txt, _c) in enumerate(VISTAS[1:]):
        x = (W - 2 * w - 24) / 2.0 + (i % 2) * (w + 24)
        y = 126 + (i // 2) * (h + 36)
        pc._img(d, os.path.join(IMG, '%s_%s_%s.jpg' % (k, num, ch)), x, y, w, h, q=72, px=1150, grav='center')
        d.circle(x + 16, y + h + 14, 8, fill=DEMO)
        d.txt(x + 16, y + h + 17, num, 7.6, BRANCO, 'bold', 'middle')
        d.txt(x + 30, y + h + 17, txt, 8.0, INK_SOFT)
    return d


def montar():
    pdfs = []
    for vol, chaves in ((1, ['E1', 'E2', 'E3']), (2, ['E4', 'E5', 'E6'])):
        fns = [lambda n, t, c=chaves, v=vol: capa(c, n, t, v), chave]
        for k in chaves:
            fns += [lambda n, t, k=k: p_conceito(k, n, t), lambda n, t, k=k: p_vistas(k, n, t)]
        svgs = [salvar(fn(i, len(fns)), os.path.join(PASTA, 'svg'), 'V%d-%02d' % (vol, i)) for i, fn in enumerate(fns, 1)]
        pdf = os.path.join(PASTA, 'Estudos_Sala_Vol%d_%s_A3.pdf' % (vol, '-'.join(chaves)))
        exportar_pdf_a3(svgs, pdf, 'MaxHaus 81 — Seis estudos de sala, hall e cozinha · volume %d (A3)' % vol)
        pdfs.append(pdf)
    return pdfs


if __name__ == '__main__':
    for p in montar():
        print(p, os.path.getsize(p) // 1024, 'KB')
