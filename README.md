# MaxHaus MainFloor — caderno de estudo preliminar

Pranchas geradas a partir do levantamento por scan `MaxHaus_Mainfloor.pdf`
(captura de 02.09.2026) do apartamento João Baldinato 109, 81I. Toda a geometria
— paredes, vãos e polígonos de ambiente — é lida do vetor do scan em pontos PDF
e convertida para metros pela escala 45,66 pt/m, conferida contra as cotas
gerais do pavimento (7,85 × 9,43 m).

Todo o material fecha em **A3 deitado (420 × 297 mm)** e é exportado em **PDF
vetorial**.

## Caderno (REV. C)

| Prancha | Assunto | Arquivo |
|---|---|---|
| 02 | Demolição e desmontagem | `pranchas/prancha-02-demolicao-A3.pdf` |
| 03 | Pisos: cumaru ou monolítico | `pranchas/prancha-03-cumaru-ou-monolitico-A3.pdf` |
| 04 | Teto: laje aparente, iluminação e ar-condicionado | `pranchas/prancha-04-teto-A3.pdf` |
| 05 | Tomadas, comandos e quadro | `pranchas/prancha-05-eletrica-A3.pdf` |
| — | Caderno completo, 4 folhas | `pranchas/caderno-mainfloor-A3.pdf` |

Versão web responsiva: `pranchas/caderno-mainfloor.html`.

## Decisões embutidas na base

- **Não há forro.** O teto do MainFloor é a laje de concreto aparente. Toda a
  iluminação é aplicada (trilhos eletrificados, spots de sobrepor, pendentes) e
  o ar-condicionado trabalha sem plenum, com evaporadoras e tubulação aparentes.
  Só o banheiro mantém forro.
- **O fundo do box é um pano de vidro chão-teto, ponta a ponta.** O scan leu
  esse pano como vão; a correção vale para todas as pranchas.
- **A drywall entre sala e quarto será demolida** (desenhada em fantasma).
- **Área de teto marcada pelo cliente:** 1,92 × 3,00 m (5,76 m²) sobre a sala,
  encostada na fachada leste — condiciona luminárias, trilhos e evaporadoras.
- **Três luminárias de destaque**, maiores que os spots: jantar, cama e office.

### Pisos (Prancha 03)

| Opção | Cumaru | Monolítico | Sistema à parte |
|---|---|---|---|
| **A** | sala, jantar, quarto e hall — 44,24 m² (48,66 com reserva de 10%) | cozinha 6,96 + closet 5,30 — 12,26 m² | banheiro 3,80 m² |
| **B** | — | sala, jantar, quarto, cozinha e closet — 56,50 m² | banheiro 3,80 m² |

A cozinha vai até a quina da porta de entrada e a ponta do monolítico é
resolvida em curva (arco de raio 1,49 m, tangente à parede da entrada e à parede
do banheiro). Total do pavimento: 60,30 m².

## Como regerar

```bash
python3 scripts/build_all.py     # todas as pranchas, os PDFs A3 e a versão web
```

Ou uma folha por vez: `scripts/prancha_02_demolicao.py`,
`scripts/prancha_03_pisos.py`, `scripts/prancha_04_teto.py`,
`scripts/prancha_05_eletrica.py`.

`scripts/base_mainfloor.py` concentra a geometria, a paleta, as primitivas de
desenho da planta e a exportação em A3 — é a referência canônica do caderno.

> Estudo preliminar — não liberado para execução. Quantidades e posições são
> preliminares: orientam visita, proposta e projetos complementares; não fecham
> medição nem substituem projeto executivo.
