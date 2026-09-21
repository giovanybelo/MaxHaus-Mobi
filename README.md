# MaxHaus MainFloor — caderno de estudo preliminar

Pranchas geradas a partir do levantamento por scan `MaxHaus_Mainfloor.pdf`
(captura de 02.09.2026) do apartamento João Baldinato 109, 81I. Toda a geometria
— paredes, vãos e polígonos de ambiente — é lida do vetor do scan em pontos PDF
e convertida para metros pela escala 45,66 pt/m, conferida contra as cotas
gerais do pavimento (7,85 × 9,43 m).

Todo o material fecha em **A3 deitado (420 × 297 mm)** e é exportado em **PDF
vetorial**.

## Caderno (REV. M)

| Prancha | Assunto | Arquivo |
|---|---|---|
| 01 | Planta baixa cotada, com norte | `pranchas/prancha-01-planta-cotada-A3.pdf` |
| 02 | Demolição e desmontagem | `pranchas/prancha-02-demolicao-A3.pdf` |
| 03 | Piso — opção A: cumaru-ferro, cozinha e closet em monolítico | `pranchas/prancha-03-piso-cumaru-A3.pdf` |
| 04 | Piso — opção B: monolítico integral | `pranchas/prancha-04-piso-monolitico-A3.pdf` |
| 05 | Teto: laje aparente, iluminação e ar-condicionado | `pranchas/prancha-05-teto-A3.pdf` |
| 06 | Tomadas, comandos e quadro | `pranchas/prancha-06-eletrica-A3.pdf` |
| 07 | Esquadrias e dados do levantamento | `pranchas/prancha-07-esquadrias-A3.pdf` |
| 08 | Banheiro: planta detalhada | `pranchas/prancha-08-banheiro-A3.pdf` |
| 09 | Base de medição e decisões | `pranchas/prancha-09-medicao-A3.pdf` |
| 10 | Banheiro: louças, metais e revestimentos | `pranchas/prancha-10-banheiro-acabamentos-A3.pdf` |
| 11 | Ar, exaustão e iluminação: base de cálculo | `pranchas/prancha-11-ar-luz-A3.pdf` |
| 12 | Análise técnica: riscos, impasses e verificações | `pranchas/prancha-12-riscos-A3.pdf` |
| — | Caderno completo, 12 folhas | `pranchas/caderno-mainfloor-A3.pdf` |

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
## REV. M — o que entrou e o que foi corrigido

A REV. M absorve uma série paralela de quantitativos recebida em 11.09.2026,
redesenhada na identidade do caderno, e acrescenta a leitura crítica do
conjunto. Quatro folhas novas: 09 a 12.

**A correção que muda compra.** As planilhas recebidas revestiam o banheiro até
**2,62 m** e calculavam a exaustão com o mesmo valor. O banheiro é o único
ambiente que **mantém forro**: a altura livre lá dentro é **2,42 m**. Revestir
até 2,62 m mede parede acima do forro, que não existe.

| Grandeza | Folha de 11.09 | REV. M | Diferença |
| --- | --- | --- | --- |
| Revestimento líquido | 23,38 m² | 21,90 m² | −1,48 m² |
| Revestimento com 10% | 25,72 m² | 24,09 m² | −1,63 m² |
| Exaustão do banheiro | 99,6 m³/h | 92,0 m³/h | −7,6 m³/h |

Outras reconciliações: o box passa a usar o medido (**1,43 × 0,93 m**, contra
1,40 × 0,90 arredondados no CSV); o vão da porta fica em **0,80 × 2,00 m** com
a divergência do modelo (0,81 × 2,03) registrada para conferência em campo; e
a numeração `/ 08` duplicada entre duas séries foi resolvida numa série única
de doze folhas.

A **Prancha 12** cataloga 18 pontos e isola **três impasses** — decisões que
travam serviço se não forem respondidas antes de começar: o rebaixo do banheiro
contra a cota única, a folha da porta de entrada varrendo o quadro, e a rota de
descarte da coifa.

## Banheiro (Prancha 08)

O banheiro é o trecho mais denso do pavimento e ganhou folha própria, em
escala grande. Geometria interna lida do scan nas faces de revestimento
retirado: **1,432 × 2,638 m, 3,78 m²** (3,80 m² nas tabelas).

A folha traz quatro desenhos:

- **Planta cotada** em faces internas, com o vão da porta (0,80 m), a bancada
  (0,61 m), o vidro do box que fica (K01), o ralo linear e o giro invertido da
  porta, que agora abre para a escada.
- **Teto refletido**, o único do caderno: é o único ambiente que mantém forro,
  com 2,42 m livres, dois embutidos e o exaustor.
- **Corte esquemático de nível**, que é o problema central da folha: o piso, a
  base e o rebaixo saem até a laje (D03) e o banheiro tem de voltar na **cota
  única** da casa (P05). Impermeabilização, regularização com caimento e piso
  acabado têm de caber entre a laje e essa cota — medir o desnível real depois
  da demolição. A soleira passa a ser junta de material, não degrau.
- **Altura livre**, comparando os 2,42 m do banheiro com os 2,62 m do resto do
  pavimento, onde a retirada do forro (D07) devolve os 0,20 m de plenum.

Sem degrau na soleira, a contenção de água passa a ser o caimento e o ralo
linear no fundo do box. O caimento é executado na regularização, sobre a
impermeabilização, nunca no piso acabado.

Louças e metais não estão levantados: o scan reconheceu bancada e box, e é isso
que a planta desenha.

## Pacote para fornecedores (EMISSÃO 01)

Material paralelo ao caderno, derivado dele mas com outra função: cotação e
execução. Sai **um mapa por disciplina**, cada um autossuficiente em A3 deitado,
para ir a um fornecedor diferente. Não leva justificativa de projeto, comparação
de materiais nem observação dirigida ao cliente — apenas tarefa, quantidade e
ordem.

| Folha | Disciplina | Conteúdo |
| --- | --- | --- |
| FO1 | Demolição e preparo | planta do estado existente, 20 tarefas (E01→K01), ordem em 10 passos |
| FO2 | Piso | as duas opções lado a lado na mesma escala, quantidades por sistema, ordem em 7 passos |
| FO3 | Elétrica | força, comando e quadro, 15 linhas de escopo, ordem em 10 passos |
| FO4 | Iluminação | trilho e luminárias sobre a laje, alvo de lux por ambiente, ordem em 9 passos |
| FO5 | Ar-condicionado e exaustão | evaporadoras, exaustor e coifa, carga térmica e vazão, ordem em 9 passos |

Elétrica, iluminação e ar são **três fornecedores diferentes**, então são três
folhas. A costura entre elas é explícita e está na FO3: as linhas **AL1 a AL5**
são as caixas de alimentação que o eletricista entrega — trilho, destaque,
embutido do banheiro, evaporadora, exaustor e coifa — com cabo passado e
circuito identificado. É o passo 7 da FO3 e o passo 1 da FO4; na FO5 é o passo 8.
Quem monta luminária ou evaporadora não abre parede nem laje.

Em todas as folhas:

- **ORDEM DE EXECUÇÃO** numerada; os passos em amarelo são **pontos de parada** —
  não seguem sem aceite por escrito (ensaios, recebimento do contrapiso,
  fechamento da drywall R01, cura do piso, conferência da condensadora).
- **SEQUÊNCIA GERAL DA OBRA** em oito fases, com as fases da folha destacadas,
  para o fornecedor ver onde entra no conjunto.
- **Zona sem furação** marcada na FO4 e na FO5: a projeção da piscina do
  pavimento superior, 1,92 × 3,00 m sobre a sala.
- **Durações e prazos ficam em branco**, para a contratada preencher no
  cronograma. Alterações de escopo somente por escrito.

Arquivos: `pranchas/fornecedor-01-demolicao-A3.pdf`, `fornecedor-02-piso-A3.pdf`,
`fornecedor-03-eletrica-A3.pdf`, `fornecedor-04-iluminacao-A3.pdf`,
`fornecedor-05-ar-A3.pdf` e o pacote reunido `caderno-fornecedores-A3.pdf`.

## Como regerar

```bash
python3 scripts/build_all.py     # o caderno: 12 pranchas, os PDFs A3 e a versão web
python3 scripts/fornecedores.py  # o pacote para fornecedores: FO1 a FO5
```

Ou uma folha por vez: `scripts/prancha_02_demolicao.py`,
`scripts/prancha_03_pisos.py`, `scripts/prancha_04_teto.py`,
`scripts/prancha_05_eletrica.py`.

`scripts/base_mainfloor.py` concentra a geometria, a paleta, as primitivas de
desenho da planta e a exportação em A3 — é a referência canônica do caderno.

`scripts/enxugar_pdf.py` é utilitário, fora do build: o subset de fonte que o
MuPDF grava é nominal — embute os 654 glifos da NimbusRoman quando uma prancha
usa pouco mais de oitenta. O script esvazia os glifos não usados e embute as
sub-rotinas, mantendo os GIDs no lugar (nada no resto do PDF muda). Rende só
uns 6% porque o peso está nos nomes de glifo e no índice, não nos contornos —
fica registrado para quem precisar de PDF menor.

```bash
python3 scripts/enxugar_pdf.py pranchas/prancha-08-banheiro-A3.pdf
```

> Estudo preliminar — não liberado para execução. Quantidades e posições são
> preliminares: orientam visita, proposta e projetos complementares; não fecham
> medição nem substituem projeto executivo.
