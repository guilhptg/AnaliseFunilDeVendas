from src.etl import load_all_data, merge_data, transform_data, ajust_data
import os

import logging
from src.config import setup_logging


# Logging config
setup_logging()


# Relative PATH's
RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed'
OUTPUT_FILENAME = 'olist_master_dataset.parquet'


def main():
    """
    Main Function -Executa o pipeline de ETL completo.
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

            output_path = os.path.join(PROCESSED_DATA_PATH, OUTPUT_FILENAME)
            
            # Salvar em formado .parquet para melhor processamento e performance
            master_df.to_parquet(output_path, index=False)
            
            logging.info("=============================================")
            logging.info(f"Dataset processado salvo em: {output_path}")
            logging.info("=============================================\n")
            logging.info(f"Pipeline concluído com sucesso!")
            logging.info("=============================================\n")


if __name__ == "__main__":
    main()
