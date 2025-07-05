import pandas as pd
import os


path = 'data/'



def load_all_data(raw_data_path: str) -> dict:
    # Lógica para carregar todos os CSVs da pasta raw
    # e retornar um dicionário de DataFrames
    """
    Carrega todos os arquivos .csv de uma pasta em um dicionário de DataFrames.
    
    O nome do arquivo (sem externção) se torna a chave do dicionário. 

    Args:
        raw_data_path (str): Caminho para pasta RAW, contendo os arquivos CSV.

    Returns:
        dict: Retorna um dicionário onde as chaves são os nomes dos arquivos e os valores são os DataFrames.
    """
    dataframes_dict = {}
    n_arquivos = 0
    print('Iniciando carregamento de dados brutos ...')
    
    try:
        for arquivo in os.listdir(raw_data_path):
            if arquivo.endswith('.csv'):
                nome_df = arquivo.replace('.csv', '').replace('olist_', '').replace('_dataset', '')
                caminho_completo = os.path.join(raw_data_path, arquivo)
                dataframes_dict[nome_df] = pd.read_csv(caminho_completo)
                print(f'    - Arquivo "{arquivo}" carregado como "{nome_df}" em {caminho_completo[:-7]}.')
                n_arquivos += 1
                
    except FileNotFoundError:
        print(f'ERRO: O diretório especificado não foi possível ser encontrado. - {raw_data_path}')
        return None
    
    print(f"Carregamento de {n_arquivos} dados brutos concluído. \n")
    
    return dataframes_dict


def merge_data(dataframes_dict: dict) -> pd.DataFrame:
    # Lógica para unir dataframes (orders, items, products, customers, payments, reviews ...)
    # return master_df
    """
    Une e transforma os DataFrames em um único DataFrame para análise

    Args:
        dataframes_dict (dict): Dicionário de DataFrames brutos.
        
    Returns:
        pd.DataFrame: Um único DataFrame, porem ainda bruto.
    """
    if not dataframes_dict:
        print("ERRO: Dicionário de dataframes está vazio. Transformação cancelada.")
        return None
    
    print("Iniciando modelagem de dados ...")
    
    # --- Merge nos DataFrames ---
    
    print("Iniciando merge de tabelas ...")
    
    # Primeiro merge
    master_df = pd.merge(
        left=dataframes_dict['orders'],
        right=dataframes_dict['order_items'],
        on='order_id',
        how='left'
    )
    
    # Tratamento para futuras mudanças nas tabelas
    tabelas_para_merge = {
        'products': 'product_id',
        'customers': 'customer_id',
        'sellers': 'seller_id',
        'order_payments': 'order_id',
        'product_category_name_translation': 'product_category_name'
    }
    
    for nome_tabela, chave_merge in tabelas_para_merge.items():
        if nome_tabela in dataframes_dict:
            master_df = pd.merge(master_df, dataframes_dict[nome_tabela], on=chave_merge, how='left')
        else:
            print(f"AVISO: Tabela '{nome_tabela}' não encontrada. Merge será pulado, verifique as informações da tabela.")
    
    print("Merge de tabelas concluída.")
    
    return master_df


def transform_data(master_df: pd.DataFrame) -> pd.DataFrame:
    # Lógica para converter conlunas de dadta, tratar valores nulos,
    # Criar novas colunas ( ex: tempo_de_entrega )
    """
    Transforma os valores do DataFrame único.

    Args:
        master_df (DataFrame): DataFrame unido, bruto.
        
    Returns:
        pd.DataFrame: Um único DataFrame limpo e pronto para análise
    """
    
    # df_columns
    # ['order_id' 'customer_id' 'order_status' 'order_purchase_timestamp' 
    # 'order_approved_at' 'order_delivered_carrier_date'
    # 'order_delivered_customer_date' 'order_estimated_delivery_date']
    
    columns_datetime = [
        'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
        'order_delivered_customer_date', 'order_estimated_delivery_date', 'shipping_limit_date'
    ]
    
    for col in columns_datetime:
        master_df[col] = pd.to_datetime(master_df[col], errors='coerce') # coerce to transnform erros in NaT (Not a Time)
    
    return master_df


def ajust_data(master_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta e renomeia colunas de categoria.

    Args:
        master_df (pd.DataFrame): DataFrame unido.

    Returns:
        pd.DataFrame: DataFrame com colunas de categoria renomeadas.
    """
        
    master_df.rename(columns={'product_category_name_english': 'product_category'}, inplace=True)
    
    master_df.drop(['product_category_name'], axis=1, inplace=True)
    
    print("    - Limpeza e transformação concluídas.")
    print("clean_and_transform_data finalizada.")
    
    return master_df