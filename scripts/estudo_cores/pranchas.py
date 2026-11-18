# -*- coding: utf-8 -*-
"""Estudo de cores e ambientação — living, hall, cozinha e quarto (nov/2026).

Três propostas desenvolvidas a partir das referências do cliente (pasta _Reference/Teste):
  A · Bauhaus gráfico        (opção 002 e as duas referências do pouf cobalto)
  B · Mid-century paulistano (opção 004 e room 01)
  C · Modernismo brasileiro  (opções 001 e 003, laje de concreto aparente)

Premissas comuns: laje de concreto aparente (sem forro, exceto o banheiro), persianas horizontais
de madeira, piso monolítico em todo o MainFloor menos cozinha e banheiro (porcelanato, o mesmo
nos dois), claraboia 1,92 × 3,00 m centrada em 6,13 / 3,14 m (base_mainfloor) e sol da tarde
entrando pela fachada envidraçada noroeste.

Renders gerados no Magnific (Nano Banana 2.1, 1K) sobre as bases do modelo; ficam em
estudos/cores-2026-11/img. Saída: estudos/cores-2026-11/Estudo_Cores_MainFloor_A3.pdf
"""
import base64
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import alt_a_rev_o as alt                     # noqa: E402  (geometria do Alternativo A + E5)
import base_mainfloor as bm                   # noqa: E402
from base_mainfloor import (W, H, MARGIN, K, K70, K45, K20, K12, K07, K04, INK, INK_SOFT, RULE,  # noqa: E402
                            DEMO, BRANCO, folha_nova, salvar, exportar_pdf_a3, path_d)

RAIZ = os.path.dirname(os.path.dirname(AQUI))
PASTA = os.path.join(RAIZ, 'estudos', 'cores-2026-11')
IMG = os.path.join(PASTA, 'img')
REF = os.path.join(PASTA, 'ref')
TMP = os.path.join(PASTA, '_tmp')
DATA = '18/11/2026'
TITULO_CAD = 'ESTUDO DE CORES E AMBIENTAÇÃO · LIVING, HALL, COZINHA E QUARTO'

PROPOSTAS = {
    'A': dict(
        nome='Bauhaus gráfico', sub='Branco, azul-cobalto, preto e cores primárias; aço tubular e carvalho claro.',
        refs=['bh_op002.jpg', 'bh_op002_cobalto.jpg', 'bh_op002_grafico.jpg'],
        paleta=[('Branco quente', '#F2EFE8', 'paredes'), ('Azul-cobalto', '#1F3FA6', 'parede de destaque, marcenaria'),
                ('Preto', '#1A1A1A', 'serralheria, estantes'), ('Vermelho sinal', '#C8322B', 'pontos de cor'),
                ('Amarelo', '#E9B824', 'pontos de cor'), ('Carvalho claro', '#C9A77A', 'persianas, degraus')],
        piso=[('Cinza-claro frio', '#C9CBC8', 'proposto'), ('Gelo', '#DCDCD7', 'alternativa'), ('Cimento médio', '#AEB0AC', 'alternativa')],
        conceito=('A casa como um quadro: planos brancos, um plano inteiro em azul-cobalto e o preto da escada desenhando a '
                  'estrutura. As cores primárias entram só em pontos: o pouf, a arte e um vaso. O aço tubular cromado e o '
                  'vidro deixam a sala leve, para a laje de concreto e a claraboia serem as protagonistas.'),
        materiais=[('Paredes', 'branco quente fosco; azul-cobalto na parede da TV e na das janelas'),
                   ('Teto', 'laje de concreto aparente, só selador; trilho preto'),
                   ('Persianas', 'madeira horizontal 50 mm, carvalho claro'),
                   ('Piso', 'monolítico cinza-claro frio; porcelanato na cozinha e no banheiro'),
                   ('Cozinha', 'inferiores cobalto, superiores laca branca, granito preto absoluto levigado, azulejo branco 15 × 15'),
                   ('Mobiliário', 'sofá bouclé marfim, poltrona de aço tubular e couro preto, cadeiras cantilever com palhinha, mesas de vidro e cromo'),
                   ('Quarto', 'parede da cabeceira cobalto, cama de aço tubular preto, roupa de cama branca'),
                   ('Liga com o banheiro', 'o cobalto conversa com o Gouache Bleu Nuit, mais escuro')]),
    'B': dict(
        nome='Mid-century paulistano', sub='Marfim, azul-marinho Bleu Nuit, nogueira, conhaque, mostarda e laranja queimado.',
        refs=['mc_op004.jpg', 'mc_room01.jpg', 'wc_bleu_nuit.jpg'],
        paleta=[('Marfim', '#EEE7DA', 'paredes'), ('Marinho Bleu Nuit', '#1E2A44', 'parede de destaque, cozinha, quarto'),
                ('Nogueira', '#6B4430', 'marcenaria, persianas'), ('Conhaque', '#A0612B', 'couro, poltrona'),
                ('Mostarda', '#C99A2E', 'tecidos'), ('Laranja queimado', '#C25A2A', 'tecidos, quarto')],
        piso=[('Areia', '#CBBFAE', 'proposto'), ('Greige claro', '#D9D0C3', 'alternativa'), ('Taupe', '#B3A491', 'alternativa')],
        conceito=('O azul-marinho do banheiro (Gouache Bleu Nuit) vira a cor-âncora da casa: uma parede da sala, os armários '
                  'de baixo da cozinha e a cabeceira do quarto. Em volta, nogueira, couro conhaque e tecidos mostarda e '
                  'ferrugem, com a luz da tarde passando pelas persianas de nogueira. É a proposta que mais amarra quarto, '
                  'cozinha e banheiro.'),
        materiais=[('Paredes', 'marfim fosco; marinho na parede atrás do sofá e na cabeceira'),
                   ('Teto', 'laje de concreto aparente, só selador; trilho preto'),
                   ('Persianas', 'madeira horizontal 50 mm, nogueira'),
                   ('Piso', 'monolítico areia; porcelanato na cozinha e no banheiro'),
                   ('Cozinha', 'inferiores marinho, superiores nogueira, quartzito Taj Mahal, azulejo marinho artesanal'),
                   ('Mobiliário', 'sofá de couro marfim, poltrona de couro conhaque com concha de nogueira, mesa redonda de nogueira, cadeiras de varetas'),
                   ('Quarto', 'parede marinho, cabeceira preta, roupa de cama marinho, banco ferrugem, criados de nogueira'),
                   ('Liga com o banheiro', 'mesmo azul do Gouache Bleu Nuit; metais em latão escovado')]),
    'C': dict(
        nome='Modernismo brasileiro', sub='Cal, barro, jacarandá e freijó, palhinha, pedra-sabão, latão e arte popular.',
        refs=['mb_op001.jpg', 'mb_op003_bancada.jpg', 'mb_op003_concreto.jpg'],
        paleta=[('Cal', '#EFE9DE', 'paredes'), ('Barro', '#B5654A', 'parede de destaque'),
                ('Jacarandá', '#4A2A1E', 'mobiliário, painel da TV'), ('Freijó', '#B98A55', 'persianas, marcenaria'),
                ('Pedra-sabão', '#4F5D55', 'bancada, mesas laterais'), ('Índigo', '#2B3A5C', 'tecidos, liga com o banheiro')],
        piso=[('Argila clara', '#C9B39A', 'proposto'), ('Areia quente', '#D6C6B0', 'alternativa'), ('Terracota suave', '#B4927A', 'alternativa')],
        conceito=('Uma casa paulistana dos anos 50 dentro da laje do MaxHaus: paredes em cal, uma parede de barro, móveis de '
                  'jacarandá com palhinha, pedra-sabão e latão. A arte popular (xilogravura e pintura naïf) dá a cor. O índigo '
                  'dos tecidos faz a ponte com o azul do banheiro.'),
        materiais=[('Paredes', 'cal off-white; barro na parede das janelas e na cabeceira'),
                   ('Teto', 'laje de concreto aparente, só selador; trilho preto'),
                   ('Persianas', 'madeira horizontal 50 mm, freijó'),
                   ('Piso', 'monolítico argila clara; porcelanato na cozinha e no banheiro'),
                   ('Cozinha', 'inferiores freijó com palhinha, superiores laca cal, pedra-sabão levigada, azulejo artesanal rosado'),
                   ('Mobiliário', 'sofá baixo de linho cru, poltrona de couro e jacarandá, mesa redonda de jacarandá com base branca, cadeiras de palhinha'),
                   ('Quarto', 'cama de jacarandá com cabeceira de palhinha, linho cru, manta índigo, tapete kilim'),
                   ('Liga com o banheiro', 'índigo dos tecidos e metais em latão')]),
}
VISTAS = [('1', 'entrada', 'Entrada e hall: a escada, a sala ao fundo e a claraboia'),
          ('2', 'living', 'Living: sofá, jantar e as janelas da fachada noroeste'),
          ('3', 'tv', 'Sala de TV: parede da TV (parede do banheiro)'),
          ('4', 'jantar', 'Jantar, junto à sala de estar'),
          ('5', 'claraboia', 'A claraboia: fundo de vidro da piscina, na laje'),
          ('6', 'cozinha', 'Cozinha linear: geladeira inox, cuba e porcelanato'),
          ('7', 'quarto', 'Quarto')]
# câmeras na planta (pt do scan) e direção do olhar (graus, 0 = leste da folha, 90 = sul da folha)
CAMERAS = {'1': (292, 242, 0), '2': (565, 405, 228), '3': (588, 300, 150), '4': (470, 290, 305),
           '5': (440, 385, 320), '6': (300, 440, 270), '7': (432, 448, 35)}


# --- imagem ---------------------------------------------------------------------------------
def _img(d, caminho, x, y, w, h, q=82, px=1100, grav='center'):
    """Recorta a imagem na proporção w:h e embute em base64."""
    if not os.path.isdir(TMP):
        os.makedirs(TMP)
    alvo = os.path.join(TMP, '%s_%d_%d_%s.jpg' % (os.path.basename(caminho).rsplit('.', 1)[0], int(w), int(h), grav))
    if not os.path.exists(alvo):
        pw = px
        ph = int(round(px * h / w))
        subprocess.check_call(['convert', caminho, '-resize', '%dx%d^' % (pw, ph), '-gravity', grav,
                               '-extent', '%dx%d' % (pw, ph), '-quality', str(q), alvo])
    b = base64.b64encode(open(alvo, 'rb').read()).decode('ascii')
    d.add('<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="none" '
          'href="data:image/jpeg;base64,%s"/>' % (x, y, w, h, b))


def _quebra(t, n):
    out, cur = [], ''
    for p in t.split():
        if cur and len(cur) + 1 + len(p) > n:
            out.append(cur)
            cur = p
        else:
            cur = (cur + ' ' + p) if cur else p
    if cur:
        out.append(cur)
    return out


def _par(d, x, y, w, texto, size=8.6, lh=12.6, cor=INK_SOFT):
    n = int(w / (size * 0.47))
    for ln in _quebra(texto, n):
        d.txt(x, y, ln, size, cor)
        y += lh
    return y


# --- folha ----------------------------------------------------------------------------------
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
    d.txt(MARGIN, 946, 'Imagens de estudo (IA, 1K) sobre as bases do modelo: valem para cor, material e atmosfera, não para medida. '
          'Mobiliário e arte são indicativos; peças assinadas aparecem como referência de estilo.', 7.4, INK_SOFT)
    d.txt(MARGIN, 958, 'Cores em hexadecimal para conferência em tela: escolher a tinta pelo leque físico do fabricante, sob a luz da casa.', 7.4, INK_SOFT)
    d.txt(MARGIN, 976, 'MAXHAUS 81  ·  JOÃO BALDINATO 109  ·  ESTUDO DE CORES', 8.2, DEMO, 'bold', ls=0.5)
    d.txt(W - MARGIN, 976, cod + '  ·  ' + DATA, 8.2, INK_SOFT, 'normal', 'end')
    return d


def _swatch(d, x, y, w, h, nome, hexa, uso):
    d.rect(x, y, w, h, fill=hexa, stroke=K20, sw=0.6)
    d.txt(x, y + h + 13, nome, 8.2, INK, 'bold')
    d.txt(x, y + h + 24, hexa + '  ·  ' + uso, 6.8, INK_SOFT)


# --- planta ---------------------------------------------------------------------------------
def planta(d, ox, oy, S, prop=None, cameras=True):
    """Planta do Alternativo A (E5) com zonas de piso, claraboia, câmeras e sol da tarde."""
    alt.geometria(True)
    d.set_plan(ox, oy, S)
    piso_m = PROPOSTAS[prop]['piso'][0][1] if prop else K07
    for k, r in bm.ROOMS.items():
        d.path(path_d([d.P(*p) for p in r['poly']]), fill=piso_m)
    # porcelanato 100 × 100: cozinha (zona da opção B cortada na parede nova R04) e banheiro
    coz = [(248.0, 284.8)] + bm.filete_pts() + [(345.7, 450.67), (248.0, 450.67)]
    for poly in (coz, bm.ROOMS['banheiro']['poly']):
        d.path(path_d([d.P(*p) for p in poly]), fill='#F3F1EC', stroke=K45, sw=0.5, dash='3 2')
    for w in bm.WALLS:
        d.rect(*d.R(w), fill=K)
    for j in bm.JANELAS:
        x, y, w, h = d.R(j)
        d.rect(x, y, w, h, fill=BRANCO, stroke=K45, sw=0.6)
    e = bm.ESCADA['rect']
    x, y, w, h = d.R(e)
    d.rect(x, y, w, h, fill='none', stroke=K45, sw=0.6)
    for i in range(1, bm.ESCADA['degraus']):
        xx = x + w * i / bm.ESCADA['degraus']
        d.line(xx, y, xx, y + h, K45, 0.4)
    # claraboia
    x, y, w, h = d.R(bm.AREA_PISCINA)
    d.rect(x, y, w, h, fill='#7FE3E8', stroke='#1A9AA3', sw=1.2, opacity=0.85)
    d.txt(x + w / 2, y + h / 2 - 4, 'CLARABOIA', 7.0, K, 'bold', 'middle')
    d.txt(x + w / 2, y + h / 2 + 7, '1,92 × 3,00', 6.4, K70, 'normal', 'middle')
    for k, r in bm.ROOMS.items():
        c = d.P(r['lx'], r['ly'])
        d.txt(c[0], c[1], r['label'], 6.8, K70, 'bold', 'middle')
    # sol da tarde: fachada envidraçada (borda leste da folha) = noroeste real
    xs = d.P(604.0, 0)[0] + 34
    for yy in (180.0, 300.0, 420.0, 500.0):
        p = d.P(604.0, yy)
        d.line(xs + 26, p[1] - 10, p[0] + 6, p[1], '#E39A2E', 1.6)
        d.path('M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (p[0] + 6, p[1], p[0] + 15, p[1] - 6, p[0] + 16, p[1] + 3), fill='#E39A2E')
    c = d.P(604.0, 340.0)
    d.circle(xs + 40, c[1] - 120, 13, fill='#F4C24D', stroke='#E39A2E', sw=1.2)
    d.txt(xs + 40, c[1] - 96, 'sol da tarde', 7.2, '#B66A10', 'bold', 'middle')
    d.txt(xs + 40, c[1] - 86, 'fachada NO', 6.6, '#B66A10', 'normal', 'middle')
    if cameras:
        import math
        for n, (cx, cy, ang) in CAMERAS.items():
            p = d.P(cx, cy)
            a1, a2 = math.radians(ang - 24), math.radians(ang + 24)
            r = 40
            d.path('M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (p[0], p[1], p[0] + r * math.cos(a1), p[1] + r * math.sin(a1),
                                                          p[0] + r * math.cos(a2), p[1] + r * math.sin(a2)),
                   fill=DEMO, opacity=0.18)
            d.circle(p[0], p[1], 8.5, fill=DEMO)
            d.txt(p[0], p[1] + 3.2, n, 8.0, BRANCO, 'bold', 'middle')
    alt.geometria(False)


# --- pranchas -------------------------------------------------------------------------------
def p00(n, t):
    d = folha('E-00', 'Leitura das referências e premissas', 'As referências da pasta Teste separadas em três linhas; o que vale para as três.', n, t)
    cols = [('A', 'BAUHAUS GRÁFICO', 'opção 002 e o pouf cobalto: planos brancos, cobalto, preto, cromo e arte em cores primárias.'),
            ('B', 'MID-CENTURY PAULISTANO', 'opção 004 e room 01: nogueira, marinho, conhaque, mostarda e ferrugem; e o Bleu Nuit do banheiro.'),
            ('C', 'MODERNISMO BRASILEIRO', 'opções 001 e 003: jacarandá, palhinha, pedra-sabão, latão, arte popular e concreto aparente.')]
    x0, y0, wcol = MARGIN, 140, 270
    for i, (L, tit, txt) in enumerate(cols):
        x = x0 + i * (wcol + 22)
        d.txt(x, y0 + 10, L + ' · ' + tit, 10.5, INK, 'bold')
        _par(d, x, y0 + 28, wcol, txt, 8.0, 11.2)
        refs = PROPOSTAS[L]['refs']
        tw, th = 86, 115
        for j, r in enumerate(refs):
            _img(d, os.path.join(REF, r), x + j * (tw + 6), y0 + 62, tw, th, px=500)
        _img(d, os.path.join(IMG, L + '1_entrada.jpg'), x, y0 + 190, wcol, wcol * 0.75, px=900)
        d.txt(x, y0 + 190 + wcol * 0.75 + 14, 'resultado: entrada e hall', 7.2, INK_SOFT)
    xr = x0 + 3 * (wcol + 22) + 8
    d.line(xr - 14, 130, xr - 14, 910, K12, 1.0)
    d.txt(xr, y0 + 10, 'PREMISSAS COMUNS ÀS TRÊS PROPOSTAS', 9.0, INK, 'bold', ls=0.8)
    y = y0 + 34
    for tit, txt in [
        ('Teto: laje de concreto aparente.', 'Sem forro fora do banheiro. Concreto limpo e selado (selador acrílico fosco, sem verniz brilhante), '
         'marcas de fôrma e furos de ancoragem à vista. Iluminação em trilho preto aplicado.'),
        ('Piso.', 'Monolítico em todo o MainFloor; porcelanato na cozinha e no banheiro, o mesmo nos dois (Confete 100 × 100). '
         'O monolítico muda só de cor entre as propostas: três tons de teste em cada uma.'),
        ('Persianas horizontais de madeira.', 'Lâminas de 50 mm em todas as janelas. A madeira muda com a proposta: carvalho claro, nogueira ou freijó.'),
        ('Claraboia na posição da planta.', 'Fundo de vidro da piscina, 1,92 × 3,00 m, centrado em 6,13 / 3,14 m do canto noroeste, '
         'paralelo à fachada e a ~0,66 m dela. Ver E-01.'),
        ('Luz.', 'A fachada envidraçada é noroeste: o sol entra baixo à tarde, em faixas pelas persianas. É a luz de todas as imagens.'),
        ('Banheiro E5.', 'Gouache Bleu Nuit nas paredes e Confete no piso. As três propostas conversam com esse azul: '
         'cobalto (A), o próprio marinho (B) ou índigo nos tecidos (C).'),
        ('Fixos.', 'Escada metálica com degraus de madeira, cozinha linear na parede oeste (geladeira inox, cuba, cooktop), '
         'claraboia e laje.'),
    ]:
        d.txt(xr, y, tit, 8.6, INK, 'bold')
        y = _par(d, xr, y + 13, W - MARGIN - xr, txt, 8.0, 11.4) + 8
    return d


def p01(n, t):
    d = folha('E-01', 'Planta-chave: claraboia, sol e câmeras', 'Alternativo A com o banheiro E5. Zonas de piso, posição da claraboia e de onde foi tirada cada imagem.', n, t)
    planta(d, 140, 150, 82.0)
    x = 930
    d.txt(x, 150, 'LEGENDA', 9.0, INK, 'bold', ls=0.8)
    y = 172
    for cor, txt in ((K07, 'Monolítico, cor conforme a proposta'), ('#F3F1EC', 'Porcelanato 100 × 100: cozinha e banheiro'),
                     ('#7FE3E8', 'Claraboia: fundo de vidro da piscina'), (DEMO, 'Câmera e campo de visão')):
        d.rect(x, y - 9, 16, 11, fill=cor, stroke=K45, sw=0.5)
        d.txt(x + 24, y, txt, 8.2, INK)
        y += 18
    d.circle(x + 8, y - 4, 7, fill='#F4C24D', stroke='#E39A2E')
    d.txt(x + 24, y, 'Sol da tarde: fachada envidraçada noroeste', 8.2, INK)
    y += 34
    d.txt(x, y, 'VISTAS (IGUAIS NAS TRÊS PROPOSTAS)', 9.0, INK, 'bold', ls=0.8)
    y += 20
    for num, _, txt in VISTAS:
        d.circle(x + 8, y - 4, 8, fill=DEMO)
        d.txt(x + 8, y - 0.8, num, 7.6, BRANCO, 'bold', 'middle')
        d.txt(x + 24, y, txt, 8.2, INK)
        y += 20
    y += 16
    for tit, txt in [
        ('Claraboia.', '1,92 × 3,00 m, centro em 6,13 / 3,14 m do canto noroeste (base_mainfloor). O lado longo corre paralelo à '
         'fachada, a cerca de 0,66 m dela, começando na passagem para a sala de estar. Laje não furável em volta (0,12 m).'),
        ('Sol.', 'A fachada de vidro é noroeste: sol baixo e quente no fim da tarde, entrando em faixas pelas persianas. '
         'De manhã, a sala recebe luz difusa, e a claraboia dá luz zenital esverdeada o dia todo.'),
        ('Câmeras.', 'Posições aproximadas, lidas das bases do modelo. As imagens servem para cor e atmosfera, não para medida.'),
    ]:
        d.txt(x, y, tit, 8.6, INK, 'bold')
        y = _par(d, x, y + 13, W - MARGIN - x, txt, 8.0, 11.4) + 8
    return d


def p_conceito(L, n, t):
    P = PROPOSTAS[L]
    d = folha('E-%s1' % L, 'Proposta %s · %s' % (L, P['nome']), P['sub'], n, t)
    hw = 820
    _img(d, os.path.join(IMG, L + '1_entrada.jpg'), MARGIN, 128, hw, hw * 0.75, px=1400)
    d.txt(MARGIN, 128 + hw * 0.75 + 16, '1 · Entrada e hall, com a claraboia ao fundo e o sol da tarde nas persianas', 7.8, INK_SOFT)
    x = MARGIN + hw + 28
    wr = W - MARGIN - x
    d.txt(x, 140, 'CONCEITO', 9.0, INK, 'bold', ls=0.8)
    y = _par(d, x, 158, wr, P['conceito'], 8.4, 12.0) + 10
    d.txt(x, y, 'PALETA', 9.0, INK, 'bold', ls=0.8)
    y += 12
    sw = (wr - 2 * 10) / 3.0
    for i, (nm, hx, uso) in enumerate(P['paleta']):
        cx = x + (i % 3) * (sw + 10)
        cy = y + (i // 3) * 82
        _swatch(d, cx, cy, sw, 44, nm, hx, uso)
    y += 2 * 82 + 6
    d.txt(x, y, 'PISO MONOLÍTICO · TONS DE TESTE', 9.0, INK, 'bold', ls=0.8)
    y += 12
    for i, (nm, hx, uso) in enumerate(P['piso']):
        _swatch(d, x + i * (sw + 10), y, sw, 34, nm, hx, uso)
    y += 34 + 40
    d.txt(x, y, 'MATERIAIS', 9.0, INK, 'bold', ls=0.8)
    y += 16
    for k, v in P['materiais']:
        d.txt(x, y, k, 7.8, INK, 'bold')
        y = _par(d, x + 92, y, wr - 92, v, 7.6, 10.6) + 3
    return d


def p_sala(L, n, t):
    P = PROPOSTAS[L]
    d = folha('E-%s2' % L, 'Proposta %s · living e claraboia' % L, P['nome'] + ': as vistas 2 a 5 da planta-chave.', n, t)
    w, h = 560, 360
    for i, (num, chave, txt) in enumerate(VISTAS[1:5]):
        x = (W - 2 * w - 24) / 2.0 + (i % 2) * (w + 24)
        y = 126 + (i // 2) * (h + 36)
        _img(d, os.path.join(IMG, '%s%s_%s.jpg' % (L, num, chave)), x, y, w, h, px=1200, grav='north')
        d.circle(x + 16, y + h + 14, 8, fill=DEMO)
        d.txt(x + 16, y + h + 17, num, 7.6, BRANCO, 'bold', 'middle')
        d.txt(x + 30, y + h + 17, txt, 8.0, INK_SOFT)
    return d


def p_coz_quarto(L, n, t):
    P = PROPOSTAS[L]
    d = folha('E-%s3' % L, 'Proposta %s · cozinha e quarto' % L, P['nome'] + ': as vistas 6 e 7 da planta-chave e a planta com o tom do piso.', n, t)
    w, h = 520, 390
    for i, (num, chave, txt) in enumerate(VISTAS[5:7]):
        x = MARGIN + i * (w + 22)
        _img(d, os.path.join(IMG, '%s%s_%s.jpg' % (L, num, chave)), x, 126, w, h, px=1100)
        d.circle(x + 16, 126 + h + 14, 8, fill=DEMO)
        d.txt(x + 16, 126 + h + 17, num, 7.6, BRANCO, 'bold', 'middle')
        d.txt(x + 30, 126 + h + 17, txt, 8.0, INK_SOFT)
    planta(d, MARGIN + 20, 556, 36.0, prop=L, cameras=False)
    x = MARGIN + 2 * (w + 22) + 6
    wr = W - MARGIN - x
    d.txt(x, 140, 'ESPECIFICAÇÃO RESUMIDA', 9.0, INK, 'bold', ls=0.8)
    y = 160
    for k, v in P['materiais']:
        d.txt(x, y, k, 7.8, INK, 'bold')
        y = _par(d, x, y + 11, wr, v, 7.6, 10.6) + 7
    d.txt(MARGIN + 520, 600, 'O PISO NA PLANTA', 9.0, INK, 'bold', ls=0.8)
    _par(d, MARGIN + 520, 618, 420, 'Monolítico em %s em toda a área seca; porcelanato 100 × 100 claro na cozinha e no banheiro, '
         'com perfil de transição na ponta arredondada da cozinha e na soleira do banheiro. Claraboia em azul.' % P['piso'][0][0].lower(), 8.0, 11.4)
    for i, (nm, hx, uso) in enumerate(P['piso']):
        _swatch(d, MARGIN + 520 + i * 140, 680, 128, 30, nm, hx, uso)
    return d


def montar():
    fns = [p00, p01]
    for L in 'ABC':
        fns += [lambda n, t, L=L: p_conceito(L, n, t), lambda n, t, L=L: p_sala(L, n, t), lambda n, t, L=L: p_coz_quarto(L, n, t)]
    total = len(fns)
    svgs = []
    for i, fn in enumerate(fns, 1):
        d = fn(i, total)
        svgs.append(salvar(d, os.path.join(PASTA, 'svg'), 'E-%02d' % i))
    pdf = os.path.join(PASTA, 'Estudo_Cores_MainFloor_A3.pdf')
    exportar_pdf_a3(svgs, pdf, 'MaxHaus 81 — Estudo de cores e ambientação (A3)')
    return pdf, svgs


if __name__ == '__main__':
    print(montar()[0])
