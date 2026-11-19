"""Calcula a previsão de chuva forte e envia para a API WaterLine (POST /previsoes).

Uso:
    python enviar_previsao.py                      # última hora completa dos dados
    python enviar_previsao.py --momento "2026-01-16 18:00"   # uma hora específica (UTC)
    python enviar_previsao.py --simular            # só mostra o que seria enviado

As funções de leitura e de atributos são as mesmas do notebook waterline_chuva_forte.ipynb;
os pesos, o padronizador e o limiar vêm da pasta modelo/, gravada pelo notebook.
"""
import argparse
import glob
import json
import os

import joblib
import numpy as np
import pandas as pd
import requests
import torch
import torch.nn as nn

PASTA = os.path.dirname(os.path.abspath(__file__))
COLUNAS = ['chuva', 'pressao', 'pressao_max', 'pressao_min', 'radiacao', 'temp', 'orvalho',
           'temp_max', 'temp_min', 'orvalho_max', 'orvalho_min', 'umid_max', 'umid_min',
           'umidade', 'vento_dir', 'vento_rajada', 'vento_vel']


class RedeChuva(nn.Module):
    def __init__(self, n_atributos, n_neuronios):
        super().__init__()
        self.layer1 = nn.Linear(n_atributos, n_neuronios)
        self.activation = torch.sigmoid
        self.layer2 = nn.Linear(n_neuronios, 1)

    def forward(self, x):
        return self.layer2(self.activation(self.layer1(x)))


def carregar_inmet(pasta):
    partes = []
    for caminho in sorted(glob.glob(os.path.join(pasta, '*.CSV'))):
        parte = pd.read_csv(caminho, sep=';', decimal=',', skiprows=8, encoding='latin1')
        partes.append(parte.loc[:, ~parte.columns.str.startswith('Unnamed')])
    bruto = pd.concat(partes, ignore_index=True)
    momento = pd.to_datetime(bruto.iloc[:, 0] + ' ' + bruto.iloc[:, 1].str.slice(0, 4),
                             format='%Y/%m/%d %H%M')
    dados = bruto.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
    dados.columns = COLUNAS
    dados.index = momento
    dados = dados.replace(-9999, np.nan)
    return dados.reindex(pd.date_range(dados.index.min(), dados.index.max(), freq='h'))


def montar_atributos(dados):
    X = pd.DataFrame(index=dados.index)
    X['chuva_1h'] = dados['chuva']
    for janela in (3, 6, 24):
        X[f'chuva_{janela}h'] = dados['chuva'].rolling(janela, min_periods=janela).sum()
    X['pressao'] = dados['pressao']
    X['pressao_var_3h'] = dados['pressao'] - dados['pressao'].shift(3)
    X['temp'] = dados['temp']
    X['temp_var_3h'] = dados['temp'] - dados['temp'].shift(3)
    X['orvalho'] = dados['orvalho']
    X['depressao_orvalho'] = dados['temp'] - dados['orvalho']
    X['umidade'] = dados['umidade']
    X['umidade_var_3h'] = dados['umidade'] - dados['umidade'].shift(3)
    X['vento_vel'] = dados['vento_vel']
    X['vento_rajada'] = dados['vento_rajada']
    direcao = np.deg2rad(dados['vento_dir'])
    X['vento_sen'] = np.sin(direcao)
    X['vento_cos'] = np.cos(direcao)
    X['radiacao'] = dados['radiacao'].fillna(0).where(dados['temp'].notna())
    local = dados.index - pd.Timedelta(hours=3)
    X['hora_sen'] = np.sin(2 * np.pi * local.hour / 24)
    X['hora_cos'] = np.cos(2 * np.pi * local.hour / 24)
    X['mes_sen'] = np.sin(2 * np.pi * (local.month - 1) / 12)
    X['mes_cos'] = np.cos(2 * np.pi * (local.month - 1) / 12)
    return X


def prever(atributos, momento, horas):
    """Devolve o corpo do POST /previsoes para o momento e o horizonte pedidos."""
    with open(os.path.join(PASTA, 'modelo', f'config_{horas}h.json'), encoding='utf-8') as arquivo:
        config = json.load(arquivo)
    if list(atributos.columns) != config['atributos']:
        raise RuntimeError('Os atributos do script não batem com os do modelo treinado.')

    escalador = joblib.load(os.path.join(PASTA, 'modelo', f'escalador_{horas}h.joblib'))
    model = RedeChuva(len(config['atributos']), config['neuronios'])
    model.load_state_dict(torch.load(os.path.join(PASTA, 'modelo', f'rede_chuva_{horas}h.pt')))
    model.eval()

    x = torch.tensor(escalador.transform(atributos.loc[[momento]].values), dtype=torch.float32)
    with torch.no_grad():
        p_bruta = torch.sigmoid(model.forward(x)).item()
    # desfaz o peso da classe rara para informar uma probabilidade realista
    p_corrigida = p_bruta / (p_bruta + config['peso_positivo'] * (1 - p_bruta))
    return {
        'geradaEm': momento.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'horizonteHoras': horas,
        'probabilidade': round(p_corrigida, 4),
        'chuvaForte': bool(p_bruta >= config['limiar']),
    }


def main():
    parser = argparse.ArgumentParser(description='Envia a previsão de chuva forte para a API WaterLine.')
    parser.add_argument('--api', default='http://localhost:5080', help='endereço da API WaterLine')
    parser.add_argument('--momento', help='hora da previsão em UTC, ex.: "2026-01-16 18:00"')
    parser.add_argument('--simular', action='store_true', help='não envia, apenas mostra')
    args = parser.parse_args()

    atributos = montar_atributos(carregar_inmet(os.path.join(PASTA, 'dados', 'brutos'))).dropna()
    momento = pd.Timestamp(args.momento) if args.momento else atributos.index[-1]
    if momento not in atributos.index:
        raise SystemExit(f'Não há medições completas para {momento} (UTC).')

    for horas in (3, 6):
        corpo = prever(atributos, momento, horas)
        if args.simular:
            print('Simulação:', json.dumps(corpo))
            continue
        resposta = requests.post(f'{args.api}/previsoes', json=corpo, timeout=15)
        print(f'{horas} h -> enviado {json.dumps(corpo)} | HTTP {resposta.status_code}')
        print('   resposta:', resposta.text[:400])
        resposta.raise_for_status()


if __name__ == '__main__':
    main()
