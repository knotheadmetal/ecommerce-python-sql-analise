import pandas as pd
import sqlite3

DATABASE_NAME = "ecommerce.db"
CSV_FILE = "ecommerce_data.csv"
TABLE_NAME = "vendas"

def load_csv_to_sqlite():
    print(f"Carregando dados de {CSV_FILE} para o SQLite...")
    try:
        # Carregar o CSV para um DataFrame do pandas
        df = pd.read_csv(CSV_FILE)

        # Conectar ao banco de dados SQLite (ele será criado se não existir)
        conn = sqlite3.connect(DATABASE_NAME)

        # Salvar o DataFrame no SQLite
        # if_exists=\'replace\' irá recriar a tabela a cada execução
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Dados de {CSV_FILE} carregados com sucesso para a tabela {TABLE_NAME} em {DATABASE_NAME}.")
    except FileNotFoundError:
        print(f"Erro: O arquivo {CSV_FILE} não foi encontrado. Certifique-se de que ele foi gerado.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os dados para o SQLite: {e}")

if __name__ == "__main__":
    load_csv_to_sqlite()


