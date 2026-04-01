import pandas as pd
from io import StringIO
import requests
import csv

def execute(empresas_unicas, data, logger=None):
        
    raw_df = []

    emp_atual = 0
    for empresa in empresas_unicas:
        emp_atual += 1
        response = requests.get('https://ws1.soc.com.br/WebSoc/exportadados?parametro={"empresa":"'+ str(empresa) +
                                '","codigo":"exporta_code","chave":"exporta_key","tipoSaida":"csv"}')

        csv.field_size_limit(10_000_000)
        raw_dados = pd.read_csv(StringIO(response.text), sep=";", dtype=str, engine='python', on_bad_lines='skip').fillna('0')
        if raw_dados.columns[-1] == raw_dados.shape[1]-1:
            raw_dados = raw_dados.iloc[:, :-1]
        
        raw_dados['empresa'] = empresa
        raw_df.append(raw_dados)
        logger(f'Empresa {emp_atual} de {len(empresas_unicas)}: {empresa}')
    
    dados_soc = pd.concat(raw_df, ignore_index=True)

    #Normalizing fields code and name
    data['empresa'] = data['empresa'].astype(str)
    data['nome'] = data['nome'].str.lower().str.strip()
    data['codigo'] = data['codigo'].astype(str).str.lower().str.strip()
    dados_soc['empresa'] = dados_soc['empresa'].astype(str)
    dados_soc['NOME'] = dados_soc['NOME'].str.lower().str.strip()
    dados_soc['CODIGORH'] = dados_soc['CODIGORH'].astype(str).str.lower().str.strip()

    #Verifying the USC name in the company
    data['chave_nome'] = data[['empresa', 'nome']].agg('_'.join, axis=1)
    dados_soc['chave_nome'] = dados_soc[['empresa', 'NOME']].agg('_'.join, axis=1)

    data['status'] = data['chave_nome'].isin(dados_soc['chave_nome']).map({True: 'Localizado', False: 'Não localizado'})

    #Verifying the USC name and cod.RH in the company
    data['chave_completa'] = data[['empresa', 'nome', 'codigo']].agg('_'.join, axis=1)
    dados_soc['chave_completa'] = dados_soc[['empresa', 'NOME', 'CODIGORH']].agg('_'.join, axis=1)

    mask = data['status'] == 'Localizado'
    data.loc[mask, 'status'] = data.loc[mask, 'chave_completa'].isin(dados_soc['chave_completa']).map({True: 'Chave encontrada', False: 'Chave não encontrada'})

    #Verifying code duplicates in the instance
    data['chave_cod'] = data[['empresa', 'codigo']].astype(str).agg('_'.join, axis=1)
    dados_soc['chave_cod'] = dados_soc[['empresa', 'CODIGORH']].astype(str).agg('_'.join, axis=1)

    mask = data['status'] == 'Chave não encontrada'

    data.loc[mask, 'status'] = data.loc[mask, 'chave_cod'].isin(dados_soc['chave_cod']).map({True: 'Código RH em outra USC', False: 'Pendente'})

    #Status priority
    prioridade = [
        'Chave encontrada',
        'Pendente',
        'Código RH em outra USC',
        'Localizado',
        'Chave não encontrada',
        'Código não encontrado',
        'Não localizado'
    ]
    prioridade_map = {status: i for i, status in enumerate(prioridade)}

    #Checking the obrigatory fields
    for col in ['empresa', 'nome', 'codigo', 'status']:
        if col not in data.columns:
            raise KeyError(f"A coluna '{col}' não existe no DataFrame.")

    #Exact duplicates (company + name + code)
    mask_exatas = data.duplicated(subset=['empresa', 'nome', 'codigo'], keep='first')
    data.loc[mask_exatas, 'status'] = 'Duplicata exata'

    #Company + name duplicates
    data['prioridade'] = data['status'].map(prioridade_map).fillna(len(prioridade))

    #Calculate priority groups
    data['min_prioridade_grupo'] = (
        data.groupby(['empresa', 'nome'])['prioridade']
        .transform('min')
    )

    data['rank_grupo'] = data.groupby(['empresa', 'nome']).cumcount()

    #Duplicates with different code mask
    mask_inferior = (
        (data['prioridade'] > data['min_prioridade_grupo']) |
        ((data['prioridade'] == data['min_prioridade_grupo']) & (data['rank_grupo'] > 0))
    )

    mask_atualizar = mask_inferior & (data['status'] != 'Chave encontrada')
    data.loc[mask_atualizar, 'status'] = 'Duplicata com código RH diferente'

    data.drop(columns=['chave_nome', 'chave_completa', 'chave_cod', 'prioridade', 'min_prioridade_grupo', 'rank_grupo'], inplace=True)

    return(data)