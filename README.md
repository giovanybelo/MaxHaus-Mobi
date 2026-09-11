# MaxHaus MainFloor — estudos de piso

Estudos gráficos do pavimento MainFloor (João Baldinato 109, 81I), gerados a
partir do levantamento por scan `MaxHaus_Mainfloor.pdf` (captura de 02.09.2026).

## Prancha 03 — Cumaru ou monolítico (REV. C)

Comparação em planta entre duas opções de piso:

| Opção | Cumaru | Monolítico | Sistema à parte |
|---|---|---|---|
| **A** — cumaru nas áreas secas | sala, jantar, quarto, hall — 44,24 m² (48,66 m² com reserva de 10%) | cozinha 6,96 + closet 5,30 — 12,26 m² | banheiro — 3,80 m² |
| **B** — monolítico no MainFloor | — | sala, jantar, quarto, cozinha, closet — 56,50 m² | banheiro — 3,80 m² |

Total do pavimento: **60,30 m²** (sala 23,00 · quarto 13,40 · cozinha 8,90 ·
jantar 5,90 · closet 5,30 · banheiro 3,80).

Definições em vigor:

- cozinha e closet são monolíticos também na proposta de cumaru;
- a cozinha vai até a **quina da porta de entrada** e a ponta do monolítico é
  resolvida **em curva** (arco de raio 1,49 m, tangente à parede da entrada e à
  parede do banheiro); o hall e a escada — 1,94 m² que o scan conta como
  cozinha — ficam em cumaru;
- a parede do **box do banheiro é fechada**: a abertura que o scan indicava na
  parede sul era o vidro do box, não um vão;
- a **drywall entre sala e quarto foi retirada** (indicada em fantasma); a faixa
  sob ela libera cerca de 0,40 m² de piso, a conferir em obra;
- o banheiro fica fora do monolítico nas duas opções;
- o piso é desenhado contínuo: toda a área é revestida, inclusive sob móveis;
  nenhum recorte de mobiliário é descontado.

### Arquivos

- `pranchas/prancha-03-cumaru-ou-monolitico-A3.pdf` — prancha fechada em A3
  deitado (420 × 297 mm), vetorial
- `pranchas/prancha-03-cumaru-ou-monolitico.svg` — mesma prancha em SVG
- `pranchas/prancha-03-cumaru-ou-monolitico.png` — versão rasterizada (170 dpi)
- `pranchas/prancha-03-cumaru-ou-monolitico.html` — versão web responsiva
- `pranchas/planta-opcao-a.svg`, `planta-opcao-b.svg` — plantas isoladas

### Como regerar

```bash
python3 scripts/prancha_03_pisos.py   # geometria + prancha (SVG/PDF A3/PNG) + plantas
python3 scripts/build_html.py         # versão web
```

A geometria (paredes, vãos, ambientes) está em `scripts/prancha_03_pisos.py`, em
pontos PDF do scan original, convertida para metros pela escala 45,66 pt/m —
conferida contra as cotas gerais do pavimento (7,85 m × 9,43 m).

> Estudo preliminar — não liberado para execução. Cores ilustrativas; nenhum
> produto, marca ou espessura está especificado.
