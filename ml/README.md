# WaterLine — IA & Machine Learning

Previsão de chuva forte (10 mm ou mais) nas próximas 3 e 6 horas, com uma rede neural MLP em PyTorch e dados horários reais do INMET (estação A701, São Paulo — Mirante de Santana). Parte de Machine Learning da Global Solution 2026.2 da FIAP. A saída alimenta o endpoint `POST /previsoes` da API WaterLine.

## Conteúdo

| Caminho | O que é |
|---|---|
| `waterline_chuva_forte.ipynb` | Notebook executado, com todo o trabalho |
| `RELATORIO_ML.md` | Relatório com os resultados |
| `dados/README.md` | Fonte, estação, período e colunas dos dados |
| `dados/brutos/` | Os quatro CSVs do INMET (2023 a 2026) |
| `figuras/` | Gráficos gerados pelo notebook |
| `modelo/` | Pesos da rede, padronizador e limiar de cada horizonte |
| `enviar_previsao.py` | Envia a previsão para a API WaterLine |
| `fonte/` | Fonte do notebook em `.py` e o conversor para `.ipynb` |
| `requirements.txt` | Bibliotecas e versões |

## Como executar

Testado com Python 3.14 em CPU. Comandos no PowerShell, a partir da raiz do repositório:

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r ml\requirements.txt
.venv\Scripts\python.exe -m notebook ml\waterline_chuva_forte.ipynb
```

O notebook abre no navegador já executado, com todas as saídas e gráficos.

Para reexecutar tudo pela linha de comando (cerca de 3 minutos):

```
.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace ml\waterline_chuva_forte.ipynb
```

As sementes são fixas; os números do relatório se repetem a cada execução.

## Enviar a previsão para a API

Com a API WaterLine rodando em `http://localhost:5080`:

```
.venv\Scripts\python.exe ml\enviar_previsao.py --simular                      # só mostra o que seria enviado
.venv\Scripts\python.exe ml\enviar_previsao.py                                # última hora dos dados
.venv\Scripts\python.exe ml\enviar_previsao.py --momento "2026-01-16 18:00"   # uma hora específica (UTC)
.venv\Scripts\python.exe ml\enviar_previsao.py --api http://outro-endereco:5080
```

## Resultado em uma linha

No teste (janeiro a outubro de 2026), o alerta de 6 horas avisou 34 de 39 episódios de chuva forte (87%), com 5 horas de antecedência na mediana e 9 alarmes falsos por mês.
