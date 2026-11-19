# Dados

## Fonte

- **Órgão:** Instituto Nacional de Meteorologia (INMET)
- **Portal:** Dados Históricos Anuais — https://portal.inmet.gov.br/dadoshistoricos
- **Estação:** A701 — São Paulo, Mirante de Santana (estação automática)
- **Localização:** latitude -23,4964, longitude -46,6200, altitude 785,6 m
- **Em operação desde:** 25/07/2006
- **Período usado:** 01/01/2023 a 31/10/2026, medições horárias (33.600 horas)
- **Download:** arquivos `2023.zip`, `2024.zip`, `2025.zip` e `2026.zip` do portal, baixados em 15/11/2026. De cada ZIP foi extraído somente o arquivo da estação A701.

Os dados são reais e estão exatamente como o INMET publica. Nada foi simulado nem editado à mão.

## Arquivos em `brutos/`

| Arquivo | Horas |
|---|---|
| `INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2023_A_31-12-2023.CSV` | 8.760 |
| `INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2024_A_31-12-2024.CSV` | 8.784 |
| `INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_31-12-2025.CSV` | 8.760 |
| `INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2026_A_31-10-2026.CSV` | 7.296 |

## Formato

- Codificação Latin-1, separador `;`, vírgula como separador decimal.
- As 8 primeiras linhas trazem os dados da estação (região, UF, nome, código, latitude, longitude, altitude, data de fundação).
- A linha 9 é o cabeçalho; cada linha seguinte é uma hora.
- Horário em **UTC** (Brasília = UTC − 3).
- Hora sem medição aparece vazia ou como `-9999`.

## Colunas

| Coluna original | Nome no código | Unidade | Usada no modelo |
|---|---|---|---|
| Data | índice | AAAA/MM/DD | sim (mês) |
| Hora UTC | índice | HHMM UTC | sim (hora local) |
| PRECIPITAÇÃO TOTAL, HORÁRIO | `chuva` | mm | sim (atributos e alvo) |
| PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA | `pressao` | mB | sim |
| PRESSÃO ATMOSFERICA MAX. NA HORA ANT. | `pressao_max` | mB | não |
| PRESSÃO ATMOSFERICA MIN. NA HORA ANT. | `pressao_min` | mB | não |
| RADIACAO GLOBAL | `radiacao` | kJ/m² | sim |
| TEMPERATURA DO AR - BULBO SECO, HORARIA | `temp` | °C | sim |
| TEMPERATURA DO PONTO DE ORVALHO | `orvalho` | °C | sim |
| TEMPERATURA MÁXIMA NA HORA ANT. | `temp_max` | °C | não |
| TEMPERATURA MÍNIMA NA HORA ANT. | `temp_min` | °C | não |
| TEMPERATURA ORVALHO MAX. NA HORA ANT. | `orvalho_max` | °C | não |
| TEMPERATURA ORVALHO MIN. NA HORA ANT. | `orvalho_min` | °C | não |
| UMIDADE REL. MAX. NA HORA ANT. | `umid_max` | % | não |
| UMIDADE REL. MIN. NA HORA ANT. | `umid_min` | % | não |
| UMIDADE RELATIVA DO AR, HORARIA | `umidade` | % | sim |
| VENTO, DIREÇÃO HORARIA | `vento_dir` | graus | sim |
| VENTO, RAJADA MAXIMA | `vento_rajada` | m/s | sim |
| VENTO, VELOCIDADE HORARIA | `vento_vel` | m/s | sim |

## Valores faltantes

Percentual de horas sem medição:

| Coluna | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Chuva | 7,4% | 0,2% | 0,5% | 1,2% |
| Pressão, temperatura, umidade, vento | 2,4% a 2,5% | 0,2% | 0,5% | 1,1% a 1,2% |
| Radiação | 47,6% | 46,5% | 46,4% | 43,8% |

Tratamento adotado no notebook:

- **Radiação:** vazia à noite porque o sensor não registra sem sol. Preenchida com zero, desde que os demais sensores estivessem funcionando naquela hora.
- **Demais colunas:** nenhum valor é inventado. A linha é descartada quando algum atributo ou o alvo depende de uma hora sem medição (por exemplo, o acumulado de 24 h precisa das 24 horas anteriores completas).
- **Resultado:** das 33.600 horas, ficaram 29.761 para o horizonte de 3 h (11,4% descartadas) e 29.471 para o de 6 h (12,3% descartadas). A maior parte das perdas está em 2023.
