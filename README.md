# MaxHaus MainFloor — caderno de estudo preliminar

Pranchas geradas a partir do levantamento por scan `MaxHaus_Mainfloor.pdf`
(captura de 02.09.2026) do apartamento João Baldinato 109, 81I. Toda a geometria
— paredes, vãos e polígonos de ambiente — é lida do vetor do scan em pontos PDF
e convertida para metros pela escala 45,66 pt/m, conferida contra as cotas
gerais do pavimento (7,85 × 9,43 m).

Todo o material fecha em **A3 deitado (420 × 297 mm)** e é exportado em **PDF
vetorial**.

## Caderno (REV. F)

| Prancha | Assunto | Arquivo |
|---|---|---|
| 02 | Demolição e desmontagem | `pranchas/prancha-02-demolicao-A3.pdf` |
| 03 | Piso monolítico | `pranchas/prancha-03-piso-monolitico-A3.pdf` |
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
- **A laje inteira é serviço (P03).** Com o forro fora, prever restauro,
  descascamento, limpeza e preparo dos 60,30 m², com o acabamento definido junto
  com a empreiteira.
- **Toda parede que perder revestimento é preparada para pintura** — regra de
  escopo, mapeada hoje em P01 e P02 e coberta por P04 para o que aparecer em obra.

### Piso (Prancha 03)

A comparação cumaru × monolítico foi encerrada: o piso é **monolítico**, sistema
único nos cinco ambientes secos, com o banheiro à parte.

| Sistema | Ambientes | Área |
|---|---|---|
| Monolítico contínuo | sala, quarto, cozinha, jantar e closet | 56,50 m² |
| Sistema à parte (área molhada) | banheiro | 3,80 m² |
| | **total do pavimento** | **60,30 m²** |

Sem junta de material entre os ambientes secos — por isso a ponta em curva da
cozinha saiu do desenho: ela existia apenas para resolver o encontro entre a
madeira e o monolítico. As únicas transições que restam são a soleira do banheiro
e a da porta de entrada. Juntas de movimentação entram no executivo.

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
