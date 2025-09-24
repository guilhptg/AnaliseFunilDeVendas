from src.etl import load_all_data, merge_data, transform_data, ajust_data, save_to_sqlite, save_to_bigquery
import os

import logging
from src.config import setup_logging


# Logging config
setup_logging()


# --- Relative PATH's ---
RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed'
DATABASE_PATH = 'data/database'
OUTPUT_FILENAME_PARQUET = 'olist_master_dataset.parquet'
OUTPUT_FILENAME_CSV = 'olist_master_dataset.csv'
OUTPUT_DB = 'olist.db'
TABLE_NAME = 'olist_master'


# --- Configuração do BigQuery ---
GCP_PROJECT_ID = 'analise-olist-portfolio' 
BIGQUERY_TABLE_ID = 'olist_data.olist_master' 


def main():
    """
    Main Function - Executa o pipeline de ETL completo.
    """
    logging.info("Hello from Análise Funil de Vendas!")
    logging.info("=============================================")
    logging.info("Iniciando pipeline de ETL para o dataset Olist")
    logging.info("=============================================\n")
    
    # =============== Extração ===============
    # Carregar dados brutos da pasta 'data/raw'
    dataframes_dict = load_all_data(RAW_DATA_PATH)
    
    
    # ============== Transform ===============
    # Tratar e modelar os dados de 'data/raw'
    if dataframes_dict is not None:
        master_df = merge_data(dataframes_dict)
        
        try:
            master_df = transform_data(master_df)
        except Exception as e:
            logging.error(f'Erro inesperado ao transformar os dados: {e}')

        
        try:
            master_df = ajust_data(master_df)
        except Exception as e:
            logging.error(f'Error inesperado ao ajustar os dados: {e}')
            
        
        # =================== Extract ===================
        # Extrair DataFrame tratado para 'data/processed'
        if master_df is not None:
            # Garantir que a pasta de 'data/processed' exista antes de salvar
            os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

            output_path_parquet = os.path.join(PROCESSED_DATA_PATH, OUTPUT_FILENAME_PARQUET)
            output_path_csv = os.path.join(PROCESSED_DATA_PATH, OUTPUT_FILENAME_CSV)
            
            # Salvar em formado .parquet para melhor processamento e performance
            master_df.to_parquet(output_path_parquet, index=False)
            logging.info("=============================================")
            logging.info(f"Dataset .PARQUET processado salvo em: {output_path_parquet}")
            logging.info("=============================================\n")
            
            
            # Salvar em formato .csv para subir no Google Sheets
            master_df.to_csv(output_path_csv, index=False)
            logging.info(f"Dataset .CSV processado salvo em: {output_path_csv}")
            logging.info("=============================================\n")
            
            
            # Salvar em um banco de dados SQLite
            path_db = os.path.join(DATABASE_PATH, OUTPUT_DB)
            save_to_sqlite(master_df, path_db, TABLE_NAME)
            logging.info(f"Database processado salvo em: {path_db}")
            logging.info("=============================================\n")
            
            
            # Salvar em Google BigQuery (nuvem)
            save_to_bigquery(master_df, GCP_PROJECT_ID, BIGQUERY_TABLE_ID)
            
            
            logging.info(f"Pipeline concluído com sucesso!")
            logging.info("=============================================\n")


if __name__ == "__main__":
    main()
