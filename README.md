# MaxHaus MainFloor — caderno de estudo preliminar

Pranchas geradas a partir do levantamento por scan `MaxHaus_Mainfloor.pdf`
(captura de 02.09.2026) do apartamento João Baldinato 109, 81I. Toda a geometria
— paredes, vãos e polígonos de ambiente — é lida do vetor do scan em pontos PDF
e convertida para metros pela escala 45,66 pt/m, conferida contra as cotas
gerais do pavimento (7,85 × 9,43 m).

Todo o material fecha em **A3 deitado (420 × 297 mm)** e é exportado em **PDF
vetorial**.

## Caderno (REV. E)

| Prancha | Assunto | Arquivo |
|---|---|---|
| 02 | Demolição e desmontagem | `pranchas/prancha-02-demolicao-A3.pdf` |
| 03 | Pisos: cumaru ou monolítico | `pranchas/prancha-03-cumaru-ou-monolitico-A3.pdf` |
| 04 | Teto: laje aparente, iluminação e ar-condicionado | `pranchas/prancha-04-teto-A3.pdf` |
| 05 | Tomadas, comandos e quadro | `pranchas/prancha-05-eletrica-A3.pdf` |
| — | Caderno completo, 4 folhas | `pranchas/caderno-mainfloor-A3.pdf` |

Versão web responsiva: `pranchas/caderno-mainfloor.html`.

## Dois estados

- **Estado existente** (Prancha 02): o fundo do box é um pano de vidro chão-teto,
  ponta a ponta — o scan o leu como vão — e a drywall entre sala e quarto não tem
  porta.
- **Estado proposto** (Pranchas 03, 04 e 05): o pano de vidro sai e entra uma
  parede fechando o box; a drywall é demolida e refeita no mesmo eixo, agora com
  uma porta de 1,00 × 2,30 m; a porta do banheiro segue abrindo para o living,
  mas girando na direção do quarto.

## Decisões embutidas na base

- **Não há forro.** O teto do MainFloor é a laje de concreto aparente. Toda a
  iluminação é aplicada (trilhos eletrificados, spots de sobrepor, pendentes) e
  o ar-condicionado trabalha sem plenum, com evaporadoras e tubulação aparentes.
  Só o banheiro mantém forro.
- **Demolir e reconstruir são serviços separados.** Drywall e fundo do box caem
  e voltam; parede do jantar e parede sob a escada recebem apenas retirada de
  revestimento/espelho e preparo para pintura.
- **A piscina do pavimento superior** fica sobre a sala: 1,92 × 3,00 m (5,76 m²)
  centrados em 6,13 / 3,14 m do canto noroeste. Essa laje não recebe furação —
  condiciona trilhos, luminárias e evaporadoras.
- **Três luminárias de destaque**, maiores que os spots: jantar, cama e office;
  no quarto o TR5 corre no eixo de P02 e P03 e pode alimentá-las por adaptador.
- **Traçado dos trilhos (REV. E).** TR3 desceu para 5,60 m, ganhando recuo da
  drywall; TR5 desceu para 8,28 m; TR6 saiu da parede oeste e foi para 1,45 m, no
  eixo do TR4. O TR2 foi encurtado para 5,30 m — no traçado anterior cruzava o
  TR3 no meio da sala, e dois trilhos não se cruzam.
- **S08**, novo comando da luz da sala, na quina do box voltada para a escada,
  encostado no S04 do banheiro.

### Pisos (Prancha 03)

| Opção | Cumaru | Monolítico | Sistema à parte |
|---|---|---|---|
| **A** | sala, jantar, quarto e corredor — 44,86 m² (49,35 com reserva de 10%) | cozinha 6,34 + closet 5,30 — 11,64 m² | banheiro 3,80 m² |
| **B** | — | sala, jantar, quarto, cozinha e closet — 56,50 m² | banheiro 3,80 m² |

A ponta do monolítico nasce na quina do degrau da parede — logo abaixo da porta
de entrada, onde fica a geladeira — e gira em curva (1,49 × 0,89 m) até a parede
do banheiro. Total do pavimento: 60,30 m².

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
