# WaterLine — IA & Machine Learning

Parte de Machine Learning da **WaterLine**, a CitizenTech da Global Solution 2026.2 (FIAP). Uma rede neural MLP em PyTorch prevê chuva forte (10 mm ou mais) nas próximas 3 e 6 horas, com dados horários reais do INMET, e envia a previsão à API WaterLine para priorizar a limpeza das bocas de lobo antes da chuva.

## Integrantes

| Nome | RM |
| --- | --- |
| Carlos Eduardo de Queiroz Menezes | RM99849 |
| Leonardo Correia | RM550413 |

## Entregáveis

| Item | Onde |
| --- | --- |
| Notebook executado | [`ml/waterline_chuva_forte.ipynb`](ml/waterline_chuva_forte.ipynb) |
| Relatório | [`ml/RELATORIO_ML.md`](ml/RELATORIO_ML.md) |
| Descrição dos dados (fonte, link e período) | [`ml/dados/README.md`](ml/dados/README.md) |
| Bibliotecas e versões | [`ml/requirements.txt`](ml/requirements.txt) |
| Instruções de execução | [`ml/README.md`](ml/README.md) |
| Vídeo (até 5 min, não listado) | [[link do vídeo]](https://youtu.be/E7dgtbL5o_I) |

## Resultado em uma linha

No teste (janeiro a outubro de 2026), o alerta de 6 horas avisou 34 de 39 episódios de chuva forte (87%), com 5 horas de antecedência na mediana e 9 alarmes falsos por mês.

## Repositórios relacionados

| Parte | Repositório |
| --- | --- |
| API principal (C#), que recebe a previsão em `POST /previsoes` | https://github.com/Carlosqmenezes/GS_WATER-LINE_C-Sharp |
| App do gari (Mobile) | https://github.com/Carlosqmenezes/GS_WATER-LINE_mobile |
