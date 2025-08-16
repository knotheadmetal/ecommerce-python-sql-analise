import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Importar as consultas SQL para SQLite
from sqlite_queries import SQLiteQueries

DATABASE_NAME = "ecommerce.db"

class SQLiteAnalyzer:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name

    def run_query(self, query):
        # Conecta ao banco de dados SQLite e executa uma consulta, retornando um DataFrame do pandas.
        try:
            conn = sqlite3.connect(self.db_name)
            dataframe = pd.read_sql_query(query, conn)
            conn.close()
            print(f"Consulta executada com sucesso. {len(dataframe)} linhas retornadas.")
            return dataframe
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            return None

    def get_total_sales_by_month(self):
        print("Obtendo total de vendas por mês...")
        return self.run_query(SQLiteQueries.TOTAL_VENDAS_POR_MES)

    def get_top_selling_products(self):
        print("Obtendo produtos mais vendidos...")
        return self.run_query(SQLiteQueries.PRODUTOS_MAIS_VENDIDOS)

    def get_revenue_by_category(self):
        print("Obtendo faturamento por categoria de produto...")
        return self.run_query(SQLiteQueries.FATURAMENTO_POR_CATEGORIA)

    def get_avg_spend_per_customer(self):
        print("Obtendo média de valor gasto por cliente...")
        return self.run_query(SQLiteQueries.MEDIA_VALOR_GASTO_POR_CLIENTE)

    def get_sales_trend_over_time(self):
        print("Obtendo tendência de vendas ao longo do tempo...")
        return self.run_query(SQLiteQueries.TENDENCIA_VENDAS_TEMPO)

    def get_sales_by_day_hour(self):
        print("Obtendo vendas por dia da semana e hora do dia...")
        return self.run_query(SQLiteQueries.VENDAS_POR_DIA_SEMANA)


class DataProcessor:
    def clean_data(self, df, analysis_type):
        # Realiza limpeza simples de dados dependendo do tipo de análise.
        print(f"Iniciando limpeza de dados para {analysis_type}...")
        if df is None or df.empty:
            print("DataFrame vazio ou nulo, pulando limpeza.")
            return df

        if analysis_type == "total_sales_by_month":
            # Converte 'ano_mes' para datetime para ordenação e plotagem
            df["ano_mes"] = pd.to_datetime(df["ano_mes"])
            df = df.sort_values("ano_mes").reset_index(drop=True)
            # Remove linhas com valores nulos em colunas críticas
            df.dropna(subset=["ano_mes", "total_vendas"], inplace=True)
            # Remove vendas zeradas ou negativas
            df = df[df["total_vendas"] > 0]

        elif analysis_type == "sales_trend_over_time":
            # Converte 'data_venda' para datetime
            df["data_venda"] = pd.to_datetime(df["data_venda"])
            df = df.sort_values("data_venda").reset_index(drop=True)
            # Remove linhas com valores nulos em colunas críticas
            df.dropna(subset=["data_venda", "total_vendas_dia"], inplace=True)
            # Remove vendas zeradas ou negativas
            df = df[df["total_vendas_dia"] > 0]

        elif analysis_type == "revenue_by_category":
            # Remove categorias nulas ou vazias
            df.dropna(subset=["categoria", "faturamento_total"], inplace=True)
            df = df[df["faturamento_total"] > 0]

        elif analysis_type == "top_selling_products":
            df.dropna(subset=["nome_produto", "total_vendido"], inplace=True)
            df = df[df["total_vendido"] > 0]

        elif analysis_type == "sales_by_day_hour":
            df.dropna(subset=["dia_semana", "hora_dia", "total_pedidos"], inplace=True)
            df = df[df["total_pedidos"] > 0]
            # Mapear dias da semana para ordem correta
            day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            df["dia_semana"] = pd.Categorical(df["dia_semana"], categories=day_order, ordered=True)
            # Converter hora_dia para inteiro para ordenação
            df["hora_dia"] = df["hora_dia"].astype(int)
            df = df.sort_values(by=["dia_semana", "hora_dia"])

        print("Limpeza de dados concluída.")
        return df


class DataVisualizer:
    def __init__(self, output_dir="./plots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_total_sales_by_month(self, df):
        # Gráfico de linha com faturamento mensal
        if df is None or df.empty:
            print("DataFrame vazio para plotar faturamento mensal.")
            return
        print("Gerando gráfico de faturamento mensal...")
        plt.figure(figsize=(12, 6))
        plt.plot(df["ano_mes"], df["total_vendas"], marker='o')
        plt.title("Faturamento Mensal ao Longo do Tempo")
        plt.xlabel("Mês")
        plt.ylabel("Total de Vendas (USD)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "faturamento_mensal.png"))
        plt.close()
        print("Gráfico de faturamento mensal salvo.")

    def plot_top_selling_products(self, df):
        # Gráfico de barras com top 10 produtos mais vendidos
        if df is None or df.empty:
            print("DataFrame vazio para plotar produtos mais vendidos.")
            return
        print("Gerando gráfico de top 10 produtos mais vendidos...")
        plt.figure(figsize=(12, 7))
        sns.barplot(x="total_vendido", y="nome_produto", data=df.head(10), palette="viridis")
        plt.title("Top 10 Produtos Mais Vendidos (por Faturamento)")
        plt.xlabel("Total Vendido (USD)")
        plt.ylabel("Produto")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "top_produtos_vendidos.png"))
        plt.close()
        print("Gráfico de top 10 produtos mais vendidos salvo.")

    def plot_revenue_by_category(self, df):
        # Gráfico de pizza com distribuição de categorias
        if df is None or df.empty:
            print("DataFrame vazio para plotar faturamento por categoria.")
            return
        print("Gerando gráfico de faturamento por categoria...")
        # Para evitar muitas fatias pequenas, agrupar categorias com faturamento baixo
        df_filtered = df[df["faturamento_total"] > df["faturamento_total"].sum() * 0.01] # Apenas categorias > 1% do total
        if len(df) > len(df_filtered):
            other_revenue = df[df["faturamento_total"] <= df["faturamento_total"].sum() * 0.01]["faturamento_total"].sum()
            df_filtered = pd.concat([df_filtered, pd.DataFrame([{"categoria": "Outros", "faturamento_total": other_revenue}])])

        fig = px.pie(df_filtered, values="faturamento_total", names="categoria", title="Faturamento por Categoria de Produto")
        fig.write_image(os.path.join(self.output_dir, "faturamento_por_categoria.png"))
        print("Gráfico de faturamento por categoria salvo.")

    def plot_sales_heatmap_by_day_hour(self, df):
        # Heatmap de vendas por dia da semana e hora do dia
        if df is None or df.empty:
            print("DataFrame vazio para plotar heatmap de vendas.")
            return
        print("Gerando heatmap de vendas por dia/hora...")

        # Pivotar os dados para o formato de heatmap
        # Certifique-se de que todos os dias da semana e horas estão presentes para um heatmap completo
        # Criar um DataFrame completo com todas as combinações de dia da semana e hora
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hours_of_day = range(24)
        full_index = pd.MultiIndex.from_product([days_of_week, hours_of_day], names=["dia_semana", "hora_dia"])
        full_df = pd.DataFrame(index=full_index).reset_index()

        # Mesclar com os dados reais, preenchendo NaN com 0
        heatmap_data = pd.merge(full_df, df, on=["dia_semana", "hora_dia"], how="left").fillna(0)

        # Re-pivotar para o formato final do heatmap
        heatmap_data = heatmap_data.pivot(index="dia_semana", columns="hora_dia", values="total_pedidos")

        # Reordenar os dias da semana
        heatmap_data = heatmap_data.reindex(days_of_week)

        plt.figure(figsize=(14, 8))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5)
        plt.title("Total de Pedidos por Dia da Semana e Hora do Dia")
        plt.xlabel("Hora do Dia")
        plt.ylabel("Dia da Semana")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "heatmap_vendas_dia_hora.png"))
        plt.close()
        print("Heatmap de vendas por dia/hora salvo.")


# Função principal para executar a análise
def run_analysis():
    # Instanciar as classes
    analyzer = SQLiteAnalyzer()
    processor = DataProcessor()
    visualizer = DataVisualizer()

    # 1. Total de vendas por mês
    df_sales_month = analyzer.get_total_sales_by_month()
    df_sales_month = processor.clean_data(df_sales_month, "total_sales_by_month")
    visualizer.plot_total_sales_by_month(df_sales_month)

    # 2. Produtos mais vendidos
    df_top_products = analyzer.get_top_selling_products()
    df_top_products = processor.clean_data(df_top_products, "top_selling_products")
    visualizer.plot_top_selling_products(df_top_products)

    # 3. Faturamento por categoria de produto
    df_revenue_category = analyzer.get_revenue_by_category()
    df_revenue_category = processor.clean_data(df_revenue_category, "revenue_by_category")
    visualizer.plot_revenue_by_category(df_revenue_category)

    # 4. Média de valor gasto por cliente (apenas extração, sem visualização específica pedida)
    df_avg_spend = analyzer.get_avg_spend_per_customer()
    if df_avg_spend is not None:
        print("\nMédia de Valor Gasto por Cliente:")
        print(df_avg_spend)

    # 5. Tendência de vendas ao longo do tempo (diário) - usado para o heatmap
    df_sales_trend = analyzer.get_sales_trend_over_time()
    df_sales_trend = processor.clean_data(df_sales_trend, "sales_trend_over_time")
    # A visualização de tendência de vendas diária não foi explicitamente pedida como gráfico de linha separado,
    # mas os dados podem ser usados para análises mais detalhadas ou para o heatmap.
    # O heatmap já cobre a dimensão temporal (dia da semana e hora).

    # 6. Vendas por dia da semana e hora do dia (para Heatmap)
    df_sales_day_hour = analyzer.get_sales_by_day_hour()
    df_sales_day_hour = processor.clean_data(df_sales_day_hour, "sales_by_day_hour")
    visualizer.plot_sales_heatmap_by_day_hour(df_sales_day_hour)

    print("\nAnálise concluída. Verifique a pasta \'plots\' para os gráficos gerados.")

if __name__ == "__main__":
    run_analysis()


