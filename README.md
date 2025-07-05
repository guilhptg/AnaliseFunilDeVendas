# AnaliseFunilDeVendas - E-commerce Olist


**Análise completa do ciclo de vida de pedidos da Olist para identificar gargalos operacionais e oportunidades de otimização na jornada do cliente.**

---

### Sumário

* [Visão Geral do Projeto](#-visão-geral-do-projeto)
* [Problema de Negócio](#-problema-de-negócio)

---

### Visão Geral do Projeto

Este projeto realiza uma análise aprofundada do funil de vendas e operações da Olist, a maior loja de departamentos em marketplaces brasileiros. O objetivo é construir um pipeline de dados robusto e reprodutível que transforma dados brutos de 9 fontes distintas em um dataset mestre, limpo e pronto para análise. A partir deste dataset, investigamos as principais métricas de conversão e eficiência operacional, culminando em um dashboard interativo para exploração dos resultados.

---

### Problema de Negócio

A Olist, operando como um grande marketplace, precisa garantir uma experiência de compra flúida desde o pagamento até a entrega. Atrasos ou falhas em qualquer etapa podem levar à insatisfação do cliente e impactar na reputação da plataforma. As principais questões de negócio que este projeto busca responder são:

1. **Onde estão os maiores gargalos no nosso de funil de processamento de pedidos?** (Tempo de entre pagamento, envio e entrega).

2. **Qual a eficiência dos nossos vendedores (sellers) em despachar os produtos no prazo?**

3. **Como a geografia(estado do cliente vs vendedor) impacta no tempo ou cancelamento?**

5. **Existem métodos de pagamento que correlacionam com atrasos ou cancelamentos?**

---

### Fonte de Dados

Os dados utilizados neste projeto são públicos e foram disponibilizados pela Olist no Kaggle. O dataset é composto por 9 arquivos `.csv` que contêm informações sobre pedidos, clientes, itens, pagamentos, vendedores e mais.

* **Link para o Dataset:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

### Arquitetura do Projeto

O projeto foi estruturado para garantir a separação de responsabilidades, reprodutibilidade e manutenibilidade, seguindo as melhores práticas de engenharia de dados.

1.  **`data/raw`**: Armazena os 9 arquivos `.csv` originais, sem modificações.
2.  **`src/etl.py`**: Contém as funções Python para extração, transformação (merge, limpeza, enriquecimento) e carga dos dados.
3.  **`main.py`**: Orquestra a execução do pipeline de ETL, chamando as funções do `etl.py` na ordem correta.
4.  **`data/processed`**: Destino do pipeline, onde o dataset mestre e limpo é salvo em formato `.parquet`.
5.  **`notebooks/`**: Ambiente para análise exploratória (EDA) sobre os dados já processados.
6.  **`reports/`**: Contém o dashboard final desenvolvido na ferramenta de BI.


---

### Ferramentas Utilizadas
* **Linguagem:** Python 3.12
* **Bibliotecas Principais:** Pandas, PyArrow
* **Gerenciador de Pacotes e Ambiente:** UV
* **Análise Exploratória:** Jupyter Notebook
* **Visualização de Dados:** Power BI (ou Tableau, Metabase, etc.)
* **Controle de Versão:** Git & GitHub


---

### Como Executar o Projeto

Para executar este projeto localmente, siga os passos abaixo:

```bash
# 1. Clone o repositório
git clone https://github.com/guilhptg/AnaliseFunilDeVendas.git
cd AnaliseFunilDeVendas

# 2. Crie e ative o ambiente virtual
uv venv
source .venv/bin/activate

# 3. Instale as dependências
uv pip install -r requirements.txt 
# (Lembre-se de criar um requirements.txt com 'uv pip freeze > requirements.txt')

# 4. Execute o pipeline de ETL
# Certifique-se de que os arquivos .csv da Olist estão na pasta 'data/raw'
python main.py

# 5. Após a execução, o arquivo 'olist_master_dataset.parquet' estará em 'data/processed'
# e pronto para ser usado no seu notebook ou ferramenta de BI.

```

---

### Autor

* **Guilherme Portugal**
* [**Linkedin**](https://linkedin.com/in/guilhptg) 
* [**GitHub**](https://github.com/guilhptg) 