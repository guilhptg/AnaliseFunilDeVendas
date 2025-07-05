from src.etl import load_all_data, merge_data, clean_and_transform_data
import os

# Relative PATH's
RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed'
OUTPUT_FILENAME = 'olist_master_dataset.parquet'


def main():
    """
    Main Function -Executa o pipeline de ETL completo.
    """
    print("Hello from Análise Funil de Vendas!")
    print("=============================================")
    print("Iniciando pipeline de ETL para o dataset Olist")
    print("=============================================\n")
    
    # =============== Extração ===============
    # Carregar dados brutos da pasta 'data/raw'
    dataframes_dict = load_all_data(RAW_DATA_PATH)
    
    
    # ============== Transform ===============
    # Tratar e modelar os dados de 'data/raw'
    if dataframes_dict is not None:
        master_df = merge_data(dataframes_dict)
        
        try:
            master_df = clean_and_transform_data(master_df)
        except Exception as e:
            print(f'Erro inesperado ao limpar os dados: {e}')

        # =================== Extract ===================
        # Extrair DataFrame tratado para 'data/processed'
        if master_df is not None:
            # Garantir que a pasta de 'data/processed' exista antes de salvar
            os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

            output_path = os.path.join(PROCESSED_DATA_PATH, OUTPUT_FILENAME)
            
            # Salvar em formado .parquet para melhor processamento e performance
            master_df.to_parquet(output_path, index=False)
            
            print("=============================================")
            print(f"Pipeline concluído com sucesso!")
            print(f"Dataset processado salvo em: {output_path}")
            print("=============================================\n")


if __name__ == "__main__":
    main()
