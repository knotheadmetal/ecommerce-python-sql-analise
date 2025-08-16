class SQLiteQueries:
    # Consulta para Total de vendas por mês
    TOTAL_VENDAS_POR_MES = """
    SELECT
        strftime("%Y-%m", data_venda) AS ano_mes,
        SUM(valor_total) AS total_vendas
    FROM
        vendas
    GROUP BY
        ano_mes
    ORDER BY
        ano_mes
    """

    # Consulta para Produtos mais vendidos (Top 10)
    PRODUTOS_MAIS_VENDIDOS = """
    SELECT
        nome_produto,
        SUM(valor_total) AS total_vendido,
        SUM(quantidade) AS quantidade_vendida
    FROM
        vendas
    GROUP BY
        nome_produto
    ORDER BY
        total_vendido DESC
    LIMIT 10
    """

    # Consulta para Faturamento por categoria de produto
    FATURAMENTO_POR_CATEGORIA = """
    SELECT
        categoria,
        SUM(valor_total) AS faturamento_total
    FROM
        vendas
    GROUP BY
        categoria
    ORDER BY
        faturamento_total DESC
    """

    # Consulta para Média de valor gasto por cliente
    MEDIA_VALOR_GASTO_POR_CLIENTE = """
    SELECT
        AVG(total_gasto) AS media_gasto_por_cliente
    FROM
        (
            SELECT
                nome_cliente,
                SUM(valor_total) AS total_gasto
            FROM
                vendas
            GROUP BY
                nome_cliente
        )
    """

    # Consulta para Tendência de vendas ao longo do tempo (diário)
    TENDENCIA_VENDAS_TEMPO = """
    SELECT
        DATE(data_venda) AS data_venda,
        SUM(valor_total) AS total_vendas_dia
    FROM
        vendas
    GROUP BY
        data_venda
    ORDER BY
        data_venda
    """

    # Consulta para Vendas por dia da semana (para Heatmap)
    VENDAS_POR_DIA_SEMANA = """
    SELECT
        CASE strftime("%w", data_venda)
            WHEN "0" THEN "Sunday"
            WHEN "1" THEN "Monday"
            WHEN "2" THEN "Tuesday"
            WHEN "3" THEN "Wednesday"
            WHEN "4" THEN "Thursday"
            WHEN "5" THEN "Friday"
            WHEN "6" THEN "Saturday"
        END AS dia_semana,
        strftime("%H", data_venda) AS hora_dia,
        COUNT(id_pedido) AS total_pedidos
    FROM
        vendas
    GROUP BY
        dia_semana, hora_dia
    ORDER BY
        CASE dia_semana
            WHEN "Sunday" THEN 1
            WHEN "Monday" THEN 2
            WHEN "Tuesday" THEN 3
            WHEN "Wednesday" THEN 4
            WHEN "Thursday" THEN 5
            WHEN "Friday" THEN 6
            WHEN "Saturday" THEN 7
        END,
        hora_dia
    """


