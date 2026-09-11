# -*- coding: utf-8 -*-
"""
Monta a versão web (HTML) da Prancha 03 a partir das plantas geradas por
scripts/prancha_03_pisos.py.

Plano de projeto gráfico
  Cor    papel #f7f4ee · tinta #1b2730 · apoio #6d7681 · cumaru #c2813f ·
         monolítico #d8d4cc · área molhada #cfe1ea/#5e8ca3 · carimbo #a8372c
  Tipos  Archivo (títulos e etiquetas) + IBM Plex Sans (texto) +
         IBM Plex Mono (códigos e números do quadro de áreas)
  Layout folha técnica: faixa de legenda, duas colunas de opção lado a lado
         (empilham no celular) e carimbo no rodapé, como numa prancha impressa.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRANCHAS = os.path.join(ROOT, 'pranchas')

def read(n):
    with open(os.path.join(PRANCHAS, n)) as f:
        return f.read()

CSS = """
:root{
  --paper:#f7f4ee; --card:#fffdf8; --ink:#1b2730; --ink-2:#3c4a55; --muted:#6d7681;
  --line:#d8d3c8; --line-soft:#e7e2d8; --wood:#c2813f; --mono:#d8d4cc; --mono-line:#b3aea3;
  --wet:#cfe1ea; --wet-line:#5e8ca3; --stamp:#a8372c; --joint:#1f2c38;
  --shadow:0 1px 2px rgba(27,39,48,.06), 0 8px 24px rgba(27,39,48,.05);
}
:root:not([data-theme="light"]){ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#15181b; --card:#1c2023; --ink:#ece7dd; --ink-2:#cbc5ba; --muted:#97a0a8;
    --line:#343a3f; --line-soft:#282d31; --mono-line:#7d786f; --stamp:#e2705f;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  --paper:#15181b; --card:#1c2023; --ink:#ece7dd; --ink-2:#cbc5ba; --muted:#97a0a8;
  --line:#343a3f; --line-soft:#282d31; --mono-line:#7d786f; --stamp:#e2705f;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px rgba(0,0,0,.35);
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
.sheet{max-width:1180px; margin:0 auto; padding:16px; padding-block:28px 40px;}

.eyebrow{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-weight:600; font-size:11px;
  letter-spacing:.16em; text-transform:uppercase; color:var(--muted); margin:0 0 10px;
}
h1{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-weight:700; font-size:clamp(30px,5.2vw,46px);
  line-height:1.04; letter-spacing:-.015em; margin:0; text-wrap:balance;
}
.lede{max-width:62ch; color:var(--ink-2); margin:12px 0 0;}
.head{display:flex; flex-wrap:wrap; gap:20px 32px; align-items:flex-end; justify-content:space-between;}
.rev{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:12px; letter-spacing:.06em;
  color:var(--stamp); border:1px solid currentColor; border-radius:2px; padding:5px 10px;
  white-space:nowrap; align-self:flex-start;
}

.rule{height:1px; background:var(--line); margin:26px 0;}
.rule.thin{margin:22px 0;}

.legend{display:flex; flex-wrap:wrap; gap:10px 26px; align-items:center; font-size:13px;}
.legend span{display:inline-flex; align-items:center; gap:9px;}
.sw{width:20px; height:13px; border:1px solid var(--mono-line); flex:none;}
.sw.wood{background:var(--wood); border-color:#9c6530;}
.sw.mono{background:var(--mono);}
.sw.wet{background:var(--wet); border-color:var(--wet-line);}
.sw.joint{
  width:22px; height:0; border:0; border-top:2px dashed var(--joint); background:none;
}
.sw.ghost{background:none; border:1px dashed #9aa2ab;}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]) .sw.joint{border-top-color:#cbd5dd} }
:root[data-theme="dark"] .sw.joint{border-top-color:#cbd5dd}

.options{display:grid; grid-template-columns:1fr 1fr; gap:28px; align-items:start;}
@media (max-width:880px){ .options{grid-template-columns:1fr; gap:36px;} }

.opt-head{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:14px;}
.opt-code{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-weight:700; font-size:13px;
  letter-spacing:.1em; color:var(--paper); background:var(--ink); padding:3px 9px; border-radius:2px;
}
.opt-title{font-family:"Archivo",Helvetica,Arial,sans-serif; font-weight:600; font-size:20px; margin:0;}
.opt-tag{font-size:12.5px; color:var(--muted);}

figure{margin:0;}
.plate{
  background:#faf8f4; border:1px solid var(--line); box-shadow:var(--shadow);
  padding:10px 6px 2px; border-radius:2px;
}
.plate svg{display:block; width:100%; height:auto; max-width:100%;}
figcaption{font-size:11.5px; color:var(--muted); margin-top:9px;}

table{width:100%; border-collapse:collapse; margin-top:22px; font-size:13.5px;}
caption{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-weight:600; font-size:10.5px;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted);
  text-align:left; padding-bottom:7px; border-bottom:1px solid var(--line);
}
th,td{text-align:left; padding:8px 0; border-bottom:1px solid var(--line-soft); vertical-align:baseline;}
td.n,th.n{
  text-align:right; font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-variant-numeric:tabular-nums; white-space:nowrap; font-size:13px;
}
td.key{font-weight:600; white-space:nowrap; padding-right:12px;}
td.key .dot{display:inline-block; width:9px; height:9px; margin-right:8px; border:1px solid var(--mono-line);}
td.det{color:var(--muted); font-size:12.5px;}
tr.total td{border-bottom:0; border-top:1.5px solid var(--ink); font-weight:700; padding-top:10px;}
tr.total td.det{font-weight:400;}

ul.notes{margin:18px 0 0; padding:0; list-style:none;}
ul.notes li{
  position:relative; padding-left:18px; margin-bottom:9px; font-size:13.5px; color:var(--ink-2);
}
ul.notes li::before{
  content:""; position:absolute; left:0; top:.62em; width:7px; height:1.5px; background:var(--muted);
}
ul.notes li b{color:var(--ink); font-weight:600;}

.changes{
  border-left:3px solid var(--stamp); padding:2px 0 2px 18px;
}
.changes h2{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-size:12px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:var(--stamp); margin:0 0 12px;
}
.changes ol{margin:0; padding-left:20px; max-width:80ch;}
.changes li{margin-bottom:8px; color:var(--ink-2);}
.changes li b{color:var(--ink); font-weight:600;}

.stamp{
  border:1px solid var(--line); border-radius:2px; display:grid;
  grid-template-columns:repeat(4,1fr); background:var(--card);
}
@media (max-width:720px){ .stamp{grid-template-columns:repeat(2,1fr);} }
.stamp div{padding:11px 14px; border-right:1px solid var(--line-soft); border-bottom:1px solid var(--line-soft);}
.stamp div:nth-child(4n){border-right:0;}
@media (max-width:720px){
  .stamp div{border-right:1px solid var(--line-soft);}
  .stamp div:nth-child(2n){border-right:0;}
}
.stamp dt, .stamp .k{
  font-family:"Archivo",Helvetica,Arial,sans-serif; font-size:9.5px; font-weight:600;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted); display:block; margin-bottom:3px;
}
.stamp .v{font-size:13px; color:var(--ink);}
.stamp .v.mono{font-family:"IBM Plex Mono",ui-monospace,monospace; font-variant-numeric:tabular-nums;}
.stamp .v.warn{color:var(--stamp); font-weight:600;}
.fine{font-size:12px; color:var(--muted); margin-top:16px; max-width:95ch;}

.sheet-frame{
  border:1px solid var(--line); background:#faf8f4; box-shadow:var(--shadow);
  overflow-x:auto; border-radius:2px; padding:0;
}
.sheet-frame > div{min-width:940px;}
.sheet-frame svg{display:block; width:100%; height:auto;}
.board{margin-top:8px;}
.board + .board{margin-top:44px;}
.board-head{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:12px;}
.hint{font-size:11.5px; color:var(--muted); margin:8px 0 0;}
.keyrow{display:flex; flex-wrap:wrap; gap:8px 10px; margin:14px 0 0;}
.chip{
  font-size:12px; border:1px solid var(--line); border-radius:2px; padding:5px 9px;
  background:var(--card); color:var(--ink-2);
}
.chip b{color:var(--ink); font-weight:600;}
.chip.mono{font-family:"IBM Plex Mono",ui-monospace,monospace; font-variant-numeric:tabular-nums;}
"""

BOARDS = [
    ('02', 'Demolição e desmontagem', 'prancha-02-demolicao.svg',
     'Escopo sobre o modelo do scan: o que sai, o que se desmonta para remontar e o que fica.',
     ['<b>14</b> itens catalogados', '<b>Demolir e reconstruir</b> como serviços separados',
      '<b>Jantar e escada:</b> preparo para pintura', '<b>Porta nova</b> 1,00 × 2,30 m']),
    ('03', 'Pisos: cumaru ou monolítico', 'prancha-03-cumaru-ou-monolitico.svg',
     'Duas opções na mesma planta e na mesma escala, com a ponta da cozinha em curva na quina do degrau.',
     ['<b>A · cumaru</b> 44,86 m² (49,35 com reserva)', '<b>A · monolítico</b> 11,64 m²',
      '<b>B · monolítico</b> 56,50 m²', '<b>Banheiro</b> 3,80 m² à parte']),
    ('04', 'Teto, iluminação e ar-condicionado', 'prancha-04-teto.svg',
     'Sem forro, luz e ar dividem a mesma laje: trilhos aplicados, três luminárias de destaque e evaporadoras aparentes.',
     ['<b>6</b> trilhos eletrificados', '<b>P01–P03</b> destaques: jantar, cama, office',
      '<b>Piscina acima</b> 1,92 × 3,00 m', '<b>33.900–45.200</b> BTU/h']),
    ('05', 'Tomadas, comandos e quadro', 'prancha-05-eletrica.svg',
     'Reservas de localização com os pontos existentes que você marcou e o quadro junto à porta de entrada.',
     ['<b>9</b> tomadas existentes', '<b>8</b> reservas novas',
      '<b>7</b> comandos, dois na cabeceira', '<b>Quadro</b> na entrada']),
]

DECISOES = [
    ('Demolir e reconstruir são serviços separados',
     'A drywall entre sala e quarto cai e é refeita no mesmo eixo, agora com uma porta de '
     '1,00 × 2,30 m — a mesma altura da porta de entrada. O pano de vidro do fundo do box cai e '
     'vira parede. A Prancha 02 mostra o estado existente; as 03, 04 e 05 já mostram o proposto.'),
    ('Jantar e sob a escada: preparo, não demolição',
     'Nessas duas paredes saem o espelho e os revestimentos e a superfície é preparada para '
     'pintura. A parede fica.'),
    ('A piscina do pavimento superior fica sobre a sala',
     '1,92 × 3,00 m centrados em 6,13 / 3,14 m do canto noroeste. Essa laje não recebe furação: '
     'nem trilho, nem luminária, nem evaporadora podem invadi-la — a reserva AC01 caía dentro '
     'dela e foi deslocada.'),
    ('Sem forro em todo o MainFloor',
     'O teto é a laje de concreto aparente. A iluminação passa a ser aplicada — trilhos '
     'eletrificados, spots de sobrepor e pendentes — e o ar-condicionado trabalha sem plenum, '
     'com evaporadoras e tubulação aparentes. Só o banheiro mantém forro, para abrigar a '
     'exaustão e a luminária do box.'),
    ('A ponta do monolítico nasce na quina do degrau',
     'Logo abaixo da porta de entrada, onde fica a geladeira, a parede faz um degrau: é ali que '
     'a ponta do monolítico começa e gira em curva (1,49 × 0,89 m) até a parede do banheiro. '
     'O corredor da entrada e a escada ficam em cumaru.'),
    ('Três luminárias maiores que as demais',
     'Jantar, cama e office ganham corpo e diâmetro maiores que os spots dos trilhos — P01, P02 '
     'e P03. No quarto, as duas estão alinhadas no mesmo eixo.'),
    ('A porta do banheiro troca de lado',
     'Continua abrindo para o living, mas agora girando na direção do quarto, e não mais da '
     'escada. Na elétrica, o comando que caía dentro do box saiu e entraram dois novos na '
     'cabeceira da cama.'),
]


def build():
    boards_html = []
    for (cod, titulo, arquivo, desc, chips) in BOARDS:
        svg = read(arquivo)
        chips_html = ''.join('<span class="chip">%s</span>' % c for c in chips)
        boards_html.append(
            '<section class="board" id="p%s">'
            '<div class="board-head"><span class="opt-code">%s</span>'
            '<h2 class="opt-title">%s</h2></div>'
            '<p class="lede" style="margin:0 0 14px">%s</p>'
            '<div class="sheet-frame"><div>%s</div></div>'
            '<p class="hint">Folha A3 deitada (420 × 297 mm). Role na horizontal para ler a prancha inteira; '
            'o PDF vetorial está no arquivo <code>%s</code>.</p>'
            '<div class="keyrow">%s</div>'
            '</section>' % (cod, cod, titulo, desc, svg,
                            arquivo.replace('.svg', '-A3.pdf'), chips_html))

    decisoes_html = ''.join(
        '<li><b>%s.</b> %s</li>' % (t, c) for (t, c) in DECISOES)

    stamp = [
        ('Obra', 'MaxHaus MainFloor — João Baldinato 109, 81I', ''),
        ('Caderno', '4 pranchas — 02, 03, 04 e 05', ''),
        ('Formato', 'A3 deitado — 420 × 297 mm', 'mono'),
        ('Revisão', 'D — 11.09.2026', 'mono'),
        ('Escala', 'gráfica (barra de 2 m em cada planta)', ''),
        ('Base', 'scan MaxHaus MainFloor, 02.09.2026', ''),
        ('Área do pavimento', '60,30 m²', 'mono'),
        ('Situação', 'Estudo preliminar — não liberado para execução', 'warn'),
    ]
    stamp_html = ''.join(
        '<div><span class="k">%s</span><span class="v %s">%s</span></div>' % (k, c, v)
        for (k, v, c) in stamp)

    return """<title>Caderno MainFloor</title>
<meta name="description" content="Caderno de estudo preliminar MaxHaus MainFloor — REV. D.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>""" + CSS + """</style>

<div class="sheet">

  <header class="head">
    <div>
      <p class="eyebrow">MaxHaus · MainFloor · João Baldinato 109 — 81I</p>
      <h1>Caderno MainFloor</h1>
      <p class="lede">Quatro pranchas sobre o mesmo levantamento: o que se demole, que piso entra,
      como fica o teto agora que não há forro e onde ficam os pontos elétricos. Estudo preliminar —
      cores ilustrativas, nenhum produto ou espessura especificado.</p>
    </div>
    <p class="rev">REV. D · 11.09.2026</p>
  </header>

  <div class="rule"></div>

  <section class="changes">
    <h2>Decisões que reorganizaram o caderno</h2>
    <ol>""" + decisoes_html + """</ol>
  </section>

  <div class="rule"></div>

  """ + ''.join(boards_html) + """

  <div class="rule"></div>

  <div class="stamp">""" + stamp_html + """</div>

  <p class="fine">Áreas conforme o levantamento MaxHaus MainFloor (captura de 02.09.2026):
  sala 23,00 · quarto 13,40 · cozinha 8,90 · jantar 5,90 · closet 5,30 · banheiro 3,80 m².
  Geometria de paredes, vãos e ambientes extraída do arquivo do scan e convertida pela escala
  45,66 pt/m, conferida contra as cotas gerais do pavimento (7,85 × 9,43 m). Quantidades e posições
  são preliminares: servem para orientar visita, proposta e projetos complementares, não para fechar
  medição nem para executar. O caderno completo em PDF está em
  <code>caderno-mainfloor-A3.pdf</code>.</p>

</div>
"""


if __name__ == '__main__':
    out = os.path.join(PRANCHAS, 'caderno-mainfloor.html')
    with open(out, 'w') as f:
        f.write(build())
    print('ok', out)
