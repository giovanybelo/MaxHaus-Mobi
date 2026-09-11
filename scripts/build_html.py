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
"""

def linha(cor, nome, det, val):
    return ('<tr><td class="key"><span class="dot" style="%s"></span>%s</td>'
            '<td class="det">%s</td><td class="n">%s</td></tr>' % (cor, nome, det, val))

SW_WOOD = 'background:#c2813f;border-color:#9c6530'
SW_MONO = 'background:#d8d4cc'
SW_WET  = 'background:#cfe1ea;border-color:#5e8ca3'
SW_NONE = 'background:transparent;border-style:dashed'

def build():
    a = read('planta-opcao-a.svg')
    b = read('planta-opcao-b.svg')

    tabela_a = ('<table><caption>Quadro de áreas — opção A (m²)</caption><tbody>'
        + linha(SW_WOOD, 'Cumaru', 'sala 23,00 + quarto 13,40 + jantar 5,90 + hall 1,94', '44,24')
        + linha(SW_NONE, '+ reserva 10%', 'cortes, perdas e reposição futura', '48,66')
        + linha(SW_MONO, 'Monolítico', 'cozinha 6,96 (de 8,90) + closet 5,30', '12,26')
        + linha(SW_WET,  'Banheiro', 'sistema à parte (área molhada)', '3,80')
        + '<tr class="total"><td class="key">Total do pavimento</td><td class="det"></td>'
          '<td class="n">60,30</td></tr></tbody></table>')

    tabela_b = ('<table><caption>Quadro de áreas — opção B (m²)</caption><tbody>'
        + linha(SW_MONO, 'Monolítico', 'sala, jantar, quarto, cozinha e closet', '56,50')
        + linha(SW_WET,  'Banheiro', 'sistema à parte (área molhada)', '3,80')
        + linha(SW_NONE, 'Sem reserva', 'aplicação moldada in loco, sem perda de corte', '—')
        + '<tr class="total"><td class="key">Total do pavimento</td><td class="det"></td>'
          '<td class="n">60,30</td></tr></tbody></table>')

    notas_a = ('<ul class="notes">'
      '<li>A cozinha sobe pela extensão e <b>para na quina da porta de entrada</b>: dali a ponta do '
      'monolítico <b>gira em curva</b> — arco de raio 1,49 m, tangente à parede da entrada e à parede '
      'do banheiro.</li>'
      '<li>O <b>hall e a escada</b> ficam em cumaru. São 1,94 m² que o scan contabiliza dentro da '
      'cozinha — por isso a cozinha entra no quadro com 6,96 m² e não com 8,90 m².</li>'
      '<li>Cumaru nas áreas secas de convívio: <b>44,24 m² líquidos</b>; com reserva de 10% para '
      'cortes e reposição, 48,66 m² de material.</li>'
      '<li><b>Closet</b> inteiro em monolítico, com junta de transição no vão para o quarto.</li>'
      '<li>Banheiro fora dos dois sistemas: 3,80 m² em solução própria de área molhada.</li>'
      '</ul>')

    notas_b = ('<ul class="notes">'
      '<li>Monolítico contínuo em <b>56,50 m²</b> de base horizontal — 60,30 m² do pavimento '
      'menos os 3,80 m² do banheiro — <b>sem junta de material</b> entre os ambientes secos.</li>'
      '<li><b>Sem reserva de material</b>: aplicação moldada in loco, sem perda de corte.</li>'
      '<li><b>Degraus excluídos</b>; o piso acessível sob a escada permanece.</li>'
      '<li>Juntas de dilatação e de transição a definir no projeto executivo.</li>'
      '<li>No banheiro, especificar sistema compatível com água, impermeabilização e '
      'acabamento antiderrapante.</li>'
      '</ul>')

    stamp = [
        ('Obra', 'MaxHaus MainFloor — João Baldinato 109, 81I', ''),
        ('Assunto', 'Pisos: cumaru nas áreas secas × monolítico', ''),
        ('Prancha', '03 / 08', 'mono'),
        ('Revisão', 'C — 11.09.2026', 'mono'),
        ('Formato', 'A3 deitado — 420 × 297 mm', 'mono'),
        ('Escala', 'gráfica (barra de 2 m em cada planta)', ''),
        ('Base', 'scan MaxHaus MainFloor, 02.09.2026', ''),
        ('Situação', 'Estudo preliminar — não liberado para execução', 'warn'),
    ]
    stamp_html = ''.join(
        '<div><span class="k">%s</span><span class="v %s">%s</span></div>' % (k, c, v)
        for (k, v, c) in stamp)

    return """<title>Cumaru ou monolítico</title>
<meta name="description" content="Prancha 03 REV. C — comparação de pisos do MainFloor MaxHaus.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>""" + CSS + """</style>

<div class="sheet">

  <header class="head">
    <div>
      <p class="eyebrow">MaxHaus · MainFloor · João Baldinato 109 — 81I</p>
      <h1>Cumaru ou monolítico</h1>
      <p class="lede">Duas opções de piso desenhadas na mesma planta e na mesma escala, sobre o
      levantamento do apartamento. Cores ilustrativas: nenhum produto, marca ou espessura está
      especificado nesta fase.</p>
    </div>
    <p class="rev">REV. C · 11.09.2026</p>
  </header>

  <div class="rule"></div>

  <div class="legend">
    <span><i class="sw wood"></i>Cumaru em réguas</span>
    <span><i class="sw mono"></i>Piso monolítico</span>
    <span><i class="sw wet"></i>Banheiro — sistema à parte (área molhada)</span>
    <span><i class="sw joint"></i>Junta / soleira de transição entre acabamentos</span>
    <span><i class="sw ghost"></i>Parede de drywall retirada</span>
  </div>

  <div class="rule"></div>

  <main class="options">
    <section class="option">
      <div class="opt-head">
        <span class="opt-code">A</span>
        <h2 class="opt-title">Cumaru nas áreas secas</h2>
        <span class="opt-tag">cozinha e closet em monolítico</span>
      </div>
      <figure>
        <div class="plate">""" + a + """</div>
        <figcaption>Planta do MainFloor — cumaru na sala, no jantar, no quarto e no hall da entrada;
        monolítico na cozinha e no closet, com a ponta em curva na quina da porta.</figcaption>
      </figure>
      """ + tabela_a + notas_a + """
    </section>

    <section class="option">
      <div class="opt-head">
        <span class="opt-code">B</span>
        <h2 class="opt-title">Monolítico no MainFloor</h2>
        <span class="opt-tag">banheiro em sistema à parte</span>
      </div>
      <figure>
        <div class="plate">""" + b + """</div>
        <figcaption>Planta do MainFloor — um único piso monolítico do jantar ao quarto, sem
        transição de material entre os ambientes secos.</figcaption>
      </figure>
      """ + tabela_b + notas_b + """
    </section>
  </main>

  <div class="rule"></div>

  <section class="changes">
    <h2>O que muda nesta revisão</h2>
    <ol>
      <li><b>A cozinha vai até a quina da porta de entrada e a ponta é em curva.</b> O arco tem raio
      de 1,49 m e sai tangente à parede da entrada, fechando na parede do banheiro — como no croqui.
      O hall e a escada (1,94 m²) passam para o cumaru: a cozinha entra com 6,96 m² e o cumaru sobe
      para 44,24 m² líquidos.</li>
      <li><b>A parede do box do banheiro está fechada.</b> A abertura que o scan mostrava na parede
      sul era o vidro do box, não um vão — o banheiro agora tem só a porta.</li>
      <li><b>A drywall entre sala e quarto foi retirada</b>, indicada em fantasma na planta. A sala e
      o quarto viram um espaço contínuo; a faixa sob a parede acrescenta cerca de 0,40 m² de piso,
      a conferir em obra.</li>
      <li><b>O banheiro segue fora do monolítico nas duas opções</b> e o piso continua desenhado
      contínuo, inclusive sob móveis e equipamentos.</li>
    </ol>
  </section>

  <div class="rule thin"></div>

  <div class="stamp">""" + stamp_html + """</div>

  <p class="fine">Áreas conforme o levantamento MaxHaus MainFloor (captura de 02.09.2026):
  sala 23,00 · quarto 13,40 · cozinha 8,90 · jantar 5,90 · closet 5,30 · banheiro 3,80 m².
  A escada é o único elemento deduzido da base horizontal, conforme nota da opção B; a faixa liberada
  pela drywall retirada (~0,40 m²) não está somada a esses números. Geometria de paredes, vãos e
  ambientes extraída do arquivo do scan. A prancha fechada em A3 (420 × 297 mm) está no arquivo
  <code>prancha-03-cumaru-ou-monolitico-A3.pdf</code>; quantitativos para orçamento devem ser
  conferidos em obra antes de qualquer compra.</p>

</div>
"""

if __name__ == '__main__':
    out = os.path.join(PRANCHAS, 'prancha-03-cumaru-ou-monolitico.html')
    with open(out, 'w') as f:
        f.write(build())
    print('ok', out)
