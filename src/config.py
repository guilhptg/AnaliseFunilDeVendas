import logging
import sys

def setup_logging():
    """
    Configura o sistema de logging para o projeto.
    
    Define o formato das mensagens, o nível (INFO) e direciona a saída
    para o console (stdout).
    """
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout  # Garante que os logs vão para a saída padrão
    )
    logging.info("Logging configurado com sucesso.")

