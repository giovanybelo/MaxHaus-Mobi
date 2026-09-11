# MaxHaus MainFloor — estudos de piso

Estudos gráficos do pavimento MainFloor (João Baldinato 109, 81I), gerados a
partir do levantamento por scan `MaxHaus_Mainfloor.pdf` (captura de 02.09.2026).

## Prancha 03 — Cumaru ou monolítico (REV. B)

Comparação em planta entre duas opções de piso:

| Opção | Cumaru | Monolítico | Sistema à parte |
|---|---|---|---|
| **A** — cumaru nas áreas secas | sala, jantar, quarto — 42,30 m² (46,53 m² com reserva de 10%) | cozinha + closet — 14,20 m² | banheiro — 3,80 m² |
| **B** — monolítico no MainFloor | — | sala, jantar, quarto, cozinha, closet — 56,50 m² | banheiro — 3,80 m² |

Total do pavimento: **60,30 m²** (sala 23,00 · quarto 13,40 · cozinha 8,90 ·
jantar 5,90 · closet 5,30 · banheiro 3,80).

Definições desta revisão:

- cozinha e closet são monolíticos também na proposta de cumaru;
- a extensão da cozinha termina na soleira da **porta de entrada** — o hall e a
  escada ficam com o piso da área social;
- o banheiro sai do monolítico nas duas opções;
- o piso é desenhado contínuo: toda a área é revestida, inclusive sob móveis;
  nenhum recorte de mobiliário é descontado.

### Arquivos

- `pranchas/prancha-03-cumaru-ou-monolitico.svg` — prancha completa (impressão)
- `pranchas/prancha-03-cumaru-ou-monolitico.png` — mesma prancha rasterizada
- `pranchas/prancha-03-cumaru-ou-monolitico.html` — versão web responsiva
- `pranchas/planta-opcao-a.svg`, `planta-opcao-b.svg` — plantas isoladas

### Como regerar

```bash
python3 scripts/prancha_03_pisos.py   # geometria + prancha + plantas isoladas
python3 scripts/build_html.py         # versão web
```

A geometria (paredes, vãos, ambientes) está em `scripts/prancha_03_pisos.py`, em
pontos PDF do scan original, convertida para metros pela escala 45,66 pt/m —
conferida contra as cotas gerais do pavimento (7,85 m × 9,43 m).

> Estudo preliminar — não liberado para execução. Cores ilustrativas; nenhum
> produto, marca ou espessura está especificado.
