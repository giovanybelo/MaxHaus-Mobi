# MaxHaus MainFloor — caderno de estudo preliminar

Pranchas geradas a partir do levantamento por scan `MaxHaus_Mainfloor.pdf`
(captura de 02.09.2026) do apartamento João Baldinato 109, 81I. Toda a geometria
— paredes, vãos e polígonos de ambiente — é lida do vetor do scan em pontos PDF
e convertida para metros pela escala 45,66 pt/m, conferida contra as cotas
gerais do pavimento (7,85 × 9,43 m).

Todo o material fecha em **A3 deitado (420 × 297 mm)** e é exportado em **PDF
vetorial**.

## Caderno (REV. L)

| Prancha | Assunto | Arquivo |
|---|---|---|
| 01 | Planta baixa cotada, com norte | `pranchas/prancha-01-planta-cotada-A3.pdf` |
| 02 | Demolição e desmontagem | `pranchas/prancha-02-demolicao-A3.pdf` |
| 03 | Piso — opção A: cumaru-ferro, cozinha e closet em monolítico | `pranchas/prancha-03-piso-cumaru-A3.pdf` |
| 04 | Piso — opção B: monolítico integral | `pranchas/prancha-04-piso-monolitico-A3.pdf` |
| 05 | Teto: laje aparente, iluminação e ar-condicionado | `pranchas/prancha-05-teto-A3.pdf` |
| 06 | Tomadas, comandos e quadro | `pranchas/prancha-06-eletrica-A3.pdf` |
| 07 | Esquadrias e dados do levantamento | `pranchas/prancha-07-esquadrias-A3.pdf` |
| — | Caderno completo, 7 folhas | `pranchas/caderno-mainfloor-A3.pdf` |

Versão web responsiva: `pranchas/caderno-mainfloor.html`.

## Identidade

- **Tipografia serifada** em todo o caderno (Tiempos Text, com Source Serif 4 e
  Georgia como alternativas).
- **Quatro tintas puras + branco**: magenta é o que sai, ciano é água, ar e obra
  nova, amarelo é preparo e atenção, preto é o que fica — e toda a tipografia.
  Tudo o que parece cinza é porcentagem de preto. Ciano e amarelo puros não têm
  contraste para texto, então entram como área, nunca como letra.

## Dados do levantamento (scan Polycam, captura 02.09.2026)

| Dado | Valor |
|---|---|
| Área útil (soma dos ambientes) | 60,30 m² (relatório: 60,20) |
| Área externa do pavimento | 64,70 m² |
| Área de parede | 130,40 m² |
| Área de esquadria (vão) | 14,77 m² — com as alturas de campo; o scan dava 12,70 |
| Volume | 144,51 m³ com forro · ~158 m³ com a laje aparente |
| Perímetro somado dos ambientes | 78,10 m |
| **Pé-direito — laje** | **2,62 m** (depois de retirar o forro) |
| **Pé-direito — forro atual** | **2,42 m** (plenum de 0,20 m) |

As alturas vieram de medição em campo (12.09.2026); o relatório do scan mede
2,40 m com o forro, o que confere com os 2,42 m. Retirar o forro (D07) devolve
0,20 m de plenum: é essa folga que acomoda a porta de correr de 2,29 m — 0,13 m
sob o forro de hoje, 0,33 m sobre a laje.

### Esquadrias

Vão livre, medição de campo em 12.09.2026 (larguras do scan):

| ID | Ambiente | Vão |
|---|---|---|
| J01 | Jantar | 1,10 × 1,63 |
| J02 | Sala | 1,90 × 1,63 |
| J03 | Sala | 1,00 × 1,63 |
| J04 | Quarto | 1,20 × 1,63 |
| J05 | Quarto | 1,20 × 1,63 |
| J06 | Closet | 2,00 × 2,17 — do piso ao teto: 2,42 menos 0,15 no topo e 0,10 de peitoril |
| P01 | Entrada | 1,00 × 2,29 |
| P02 | Banheiro | 0,80 × 2,00 — giro invertido |
| P03 | Quarto | 1,00 × 2,29 — de correr, nova |

**Norte: 126°** do topo da folha, sentido horário — medido, não arbitrado.

O relatório do MainFloor não traz orientação, mas o do **pavimento superior**
(`MaxHaus_Upfloor.pdf`, mesma captura de 02.09.2026) traz rosa dos ventos e GPS.
A pétala rotulada N daquela folha aponta a **−53,97°**, e as duas plantas estão
desenhadas com **180° de diferença** — confirmado por dois elementos que os
pavimentos compartilham: a caixa da escada e a área da piscina, que só cai no
terraço do Upfloor com essa rotação. Logo, −53,97 + 180 = **126°**.

| Face da folha | Esquadrias | Rumo | Sol |
|---|---|---|---|
| Leste | J01, J02, J03, J04 | 324° — **noroeste** | tarde, o mais quente |
| Sul | J05, J06 | 54° — **nordeste** | manhã |
| Oeste | parede cega | 144° — sudeste | divisa |
| Norte | parede cega | 234° — sudoeste | divisa |

Coordenadas do levantamento: 23°36'46,8"S 46°44'15,8"O, altitude 822 m.

## Dois estados

- **Estado existente** (Prancha 02): o fundo do box é um pano de vidro chão-teto,
  ponta a ponta — o scan o leu como vão — e a drywall entre sala e quarto não tem
  porta.
- **Estado proposto** (Pranchas 03, 04 e 05): o pano de vidro sai e entra uma
  parede fechando o box; a drywall é demolida e refeita no mesmo eixo, agora com
  uma **porta de correr** de 1,00 × 2,30 m, cuja folha estaciona no 1,00 m de
  parede a leste do vão, pela face da sala; a porta do banheiro abre para fora,
  no sentido da escada.

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

### Piso — duas opções, uma folha para cada

**Opção A (Prancha 03) — cumaru-ferro, piso pronto em réguas, com cozinha e
closet numa zona monolítica contínua.** A zona é um retângulo (da parede oeste
à linha da sala, do degrau à fachada sul, passando pela abertura entre cozinha
e closet) com **canto reto e a ponta arredondada**: um filete de 0,70 m de raio,
tangente aos dois lados, só na quina que aparece no corredor da entrada.

| Sistema | Onde | Área |
|---|---|---|
| Cumaru-ferro | sala 23,00 + quarto 13,40 + jantar 5,90 + corredor 2,39 | 44,69 m² |
| + reserva de 10% | cortes, perdas e reposição | 49,16 m² |
| Monolítico | cozinha 6,51 (de 8,90) + closet 5,30 | 11,81 m² |
| Banheiro | sistema à parte | 3,80 m² |
| | **total** | **60,30 m²** |

**Opção B (Prancha 04) — monolítico integral**, sistema único nos cinco
ambientes secos (56,50 m²), com o banheiro à parte (3,80 m²). Sem junta de
material e, por isso, sem curva.

Em ambas: o banheiro fica fora do sistema mas **na mesma cota** (P05), e a
soleira é junta de material, não degrau.

## Instalações — troca agora ou depois?

O imóvel tem 17 anos. A NBR 15575 dá **20 anos de vida útil de projeto** para
instalação elétrica e hidráulica embutida, então já está no fim da faixa — mas
a idade não é o que decide. O que decide é o **acesso**: nesta obra o piso sai,
o forro sai, o banheiro desce até a laje e as paredes perdem revestimento.
Trocar agora custa material e mão de obra; trocar depois custa refazer piso e
acabamento.

Antes de decidir, dois ensaios baratos, que entraram no escopo de demolição
como **E01** (estanqueidade por pressão na hidráulica) e **E02** (resistência de
isolamento com megômetro na elétrica): custam pouco e dizem a condição real da
instalação, em vez da idade. Prumadas e colunas são do condomínio — confirmar o
que é privativo.

Orientação de escopo, não laudo: a decisão final pede um engenheiro na inspeção.

## Identidade

- **Tipografia serifada** em todo o caderno (Tiempos Text, com Source Serif 4 e
  Georgia como alternativas).
- **Quatro tintas puras + branco**: magenta é o que sai, ciano é água, ar e obra
  nova, amarelo é preparo e atenção, preto é o que fica — e toda a tipografia.
  Tudo o que parece cinza é porcentagem de preto. Ciano e amarelo puros não têm
  contraste para texto, então entram como área, nunca como letra.

## Dados do levantamento (scan Polycam, captura 02.09.2026)

| Dado | Valor |
|---|---|
| Área útil (soma dos ambientes) | 60,30 m² (relatório: 60,20) |
| Área externa do pavimento | 64,70 m² |
| Área de parede | 130,40 m² |
| Área de esquadria (vão) | 14,77 m² — com as alturas de campo; o scan dava 12,70 |
| Volume | 144,51 m³ com forro · ~158 m³ com a laje aparente |
| Perímetro somado dos ambientes | 78,10 m |
| **Pé-direito — laje** | **2,62 m** (depois de retirar o forro) |
| **Pé-direito — forro atual** | **2,42 m** (plenum de 0,20 m) |

As alturas vieram de medição em campo (12.09.2026); o relatório do scan mede
2,40 m com o forro, o que confere com os 2,42 m. Retirar o forro (D07) devolve
0,20 m de plenum: é essa folga que acomoda a porta de correr de 2,29 m — 0,13 m
sob o forro de hoje, 0,33 m sobre a laje.

### Esquadrias

Vão livre, medição de campo em 12.09.2026 (larguras do scan):

| ID | Ambiente | Vão |
|---|---|---|
| J01 | Jantar | 1,10 × 1,63 |
| J02 | Sala | 1,90 × 1,63 |
| J03 | Sala | 1,00 × 1,63 |
| J04 | Quarto | 1,20 × 1,63 |
| J05 | Quarto | 1,20 × 1,63 |
| J06 | Closet | 2,00 × 2,17 — do piso ao teto: 2,42 menos 0,15 no topo e 0,10 de peitoril |
| P01 | Entrada | 1,00 × 2,29 |
| P02 | Banheiro | 0,80 × 2,00 — giro invertido |
| P03 | Quarto | 1,00 × 2,29 — de correr, nova |

**Norte: 126°** do topo da folha, sentido horário — medido, não arbitrado.

O relatório do MainFloor não traz orientação, mas o do **pavimento superior**
(`MaxHaus_Upfloor.pdf`, mesma captura de 02.09.2026) traz rosa dos ventos e GPS.
A pétala rotulada N daquela folha aponta a **−53,97°**, e as duas plantas estão
desenhadas com **180° de diferença** — confirmado por dois elementos que os
pavimentos compartilham: a caixa da escada e a área da piscina, que só cai no
terraço do Upfloor com essa rotação. Logo, −53,97 + 180 = **126°**.

| Face da folha | Esquadrias | Rumo | Sol |
|---|---|---|---|
| Leste | J01, J02, J03, J04 | 324° — **noroeste** | tarde, o mais quente |
| Sul | J05, J06 | 54° — **nordeste** | manhã |
| Oeste | parede cega | 144° — sudeste | divisa |
| Norte | parede cega | 234° — sudoeste | divisa |

Coordenadas do levantamento: 23°36'46,8"S 46°44'15,8"O, altitude 822 m.

## Dois estados

- **Estado existente** (Prancha 02): o fundo do box é um pano de vidro chão-teto,
  ponta a ponta — o scan o leu como vão — e a drywall entre sala e quarto não tem
  porta.
- **Estado proposto** (Pranchas 03, 04 e 05): o pano de vidro sai e entra uma
  parede fechando o box; a drywall é demolida e refeita no mesmo eixo, agora com
  uma **porta de correr** de 1,00 × 2,30 m, cuja folha estaciona no 1,00 m de
  parede a leste do vão, pela face da sala; a porta do banheiro abre para fora,
  no sentido da escada.

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
