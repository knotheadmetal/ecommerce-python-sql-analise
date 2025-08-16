import pandas as pd
import numpy as np
from faker import Faker
import random
import datetime

# Inicializa o Faker para gerar dados fictícios
fake = Faker("pt_BR")

# --- Configurações da Geração de Dados ---
NUM_PEDIDOS = 1000
NUM_CLIENTES = 200
NUM_PRODUTOS = 50
DATA_INICIAL = datetime.date(2023, 1, 1)
DATA_FINAL = datetime.date(2024, 12, 31)

# --- Listas de Exemplo ---
CATEGORIAS_PRODUTOS = [
    "Eletrônicos", "Roupas", "Livros", "Casa e Cozinha", "Esportes",
    "Brinquedos", "Saúde e Beleza", "Ferramentas", "Jardim", "Automotivo"
]

# --- Geração de Clientes ---
def gerar_clientes(num_clientes):
    clientes = []
    for i in range(1, num_clientes + 1):
        clientes.append({
            "id_cliente": i,
            "nome_cliente": fake.name(),
            "localizacao_cliente": f"{fake.city()}, {fake.state_abbr()}"
        })
    return pd.DataFrame(clientes)

# --- Geração de Produtos ---
def gerar_produtos(num_produtos):
    produtos = []
    for i in range(1, num_produtos + 1):
        categoria = random.choice(CATEGORIAS_PRODUTOS)
        produtos.append({
            "id_produto": i,
            "nome_produto": f"Produto {chr(65 + (i % 26))}{i}",
            "categoria": categoria,
            "preco_unitario": round(random.uniform(10.5, 500.0), 2)
        })
    return pd.DataFrame(produtos)

# --- Geração de Pedidos ---
def gerar_pedidos(num_pedidos, df_clientes, df_produtos):
    pedidos = []
    dias_diff = (DATA_FINAL - DATA_INICIAL).days

    for i in range(1, num_pedidos + 1):
        id_cliente = random.choice(df_clientes["id_cliente"].tolist())
        id_produto = random.choice(df_produtos["id_produto"].tolist())
        quantidade = random.randint(1, 5)
        data_venda = DATA_INICIAL + datetime.timedelta(days=random.randint(0, dias_diff))

        preco_unitario = df_produtos.loc[df_produtos["id_produto"] == id_produto, "preco_unitario"].iloc[0]
        valor_total = round(preco_unitario * quantidade, 2)

        pedidos.append({
            "id_pedido": i,
            "id_cliente": id_cliente,
            "id_produto": id_produto,
            "data_venda": data_venda,
            "quantidade": quantidade,
            "valor_total": valor_total
        })
    return pd.DataFrame(pedidos)

# --- Função Principal ---
def gerar_dataset_ecommerce():
    print("Gerando dados de clientes...")
    df_clientes = gerar_clientes(NUM_CLIENTES)

    print("Gerando dados de produtos...")
    df_produtos = gerar_produtos(NUM_PRODUTOS)

    print("Gerando dados de pedidos...")
    df_pedidos = gerar_pedidos(NUM_PEDIDOS, df_clientes, df_produtos)

    # --- Juntando os DataFrames para criar o dataset final ---
    print("Juntando os datasets...")
    df_final = pd.merge(df_pedidos, df_clientes, on="id_cliente")
    df_final = pd.merge(df_final, df_produtos, on="id_produto")

    # Reordenando as colunas para o formato final
    df_final = df_final[[
        "id_pedido", "data_venda", "nome_produto", "categoria", "preco_unitario",
        "quantidade", "valor_total", "nome_cliente", "localizacao_cliente"
    ]]

    # Salvar em CSV
    output_path = "ecommerce_data.csv"
    df_final.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    print(f"Dataset fictício salvo com sucesso em: {output_path}")

if __name__ == "__main__":
    gerar_dataset_ecommerce()


