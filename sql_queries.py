class SQLQueries:
    # Consulta para Total de vendas por mês
    TOTAL_VENDAS_POR_MES = """
    SELECT
        FORMAT_DATE('%Y-%m', created_at) AS ano_mes,
        SUM(sale_price) AS total_vendas
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items`
    WHERE
        status = 'Complete'
    GROUP BY
        ano_mes
    ORDER BY
        ano_mes
    """

    # Consulta para Produtos mais vendidos (Top 10)
    PRODUTOS_MAIS_VENDIDOS = """
    SELECT
        p.name AS nome_produto,
        SUM(oi.sale_price) AS total_vendido,
        COUNT(oi.product_id) AS quantidade_vendida
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items` AS oi
    JOIN
        `bigquery-public-data.thelook_ecommerce.products` AS p
    ON
        oi.product_id = p.id
    WHERE
        oi.status = 'Complete'
    GROUP BY
        nome_produto
    ORDER BY
        total_vendido DESC
    LIMIT 10
    """

    # Consulta para Clientes com mais compras (Top 10)
    CLIENTES_MAIS_COMPRAS = """
    SELECT
        u.first_name || ' ' || u.last_name AS nome_cliente,
        COUNT(oi.order_id) AS total_compras,
        SUM(oi.sale_price) AS total_gasto
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items` AS oi
    JOIN
        `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON
        oi.order_id = o.order_id
    JOIN
        `bigquery-public-data.thelook_ecommerce.users` AS u
    ON
        o.user_id = u.id
    WHERE
        oi.status = 'Complete'
    GROUP BY
        nome_cliente
    ORDER BY
        total_compras DESC
    LIMIT 10
    """

    # Consulta para Faturamento por categoria de produto
    FATURAMENTO_POR_CATEGORIA = """
    SELECT
        p.category AS categoria_produto,
        SUM(oi.sale_price) AS faturamento_total
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items` AS oi
    JOIN
        `bigquery-public-data.thelook_ecommerce.products` AS p
    ON
        oi.product_id = p.id
    WHERE
        oi.status = 'Complete'
    GROUP BY
        categoria_produto
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
                u.id AS user_id,
                SUM(oi.sale_price) AS total_gasto
            FROM
                `bigquery-public-data.thelook_ecommerce.order_items` AS oi
            JOIN
                `bigquery-public-data.thelook_ecommerce.orders` AS o
            ON
                oi.order_id = o.order_id
            JOIN
                `bigquery-public-data.thelook_ecommerce.users` AS u
            ON
                o.user_id = u.id
            WHERE
                oi.status = 'Complete'
            GROUP BY
                user_id
        )
    """

    # Consulta para Tendência de vendas ao longo do tempo (diário)
    TENDENCIA_VENDAS_TEMPO = """
    SELECT
        DATE(created_at) AS data_venda,
        SUM(sale_price) AS total_vendas_dia
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items`
    WHERE
        status = 'Complete'
    GROUP BY
        data_venda
    ORDER BY
        data_venda
    """

    # Consulta para Vendas por dia da semana (para Heatmap)
    VENDAS_POR_DIA_SEMANA = """
    SELECT
        FORMAT_DATE('%A', created_at) AS dia_semana,
        FORMAT_DATE('%H', created_at) AS hora_dia,
        COUNT(order_id) AS total_pedidos
    FROM
        `bigquery-public-data.thelook_ecommerce.order_items`
    WHERE
        status = 'Complete'
    GROUP BY
        dia_semana, hora_dia
    ORDER BY
        CASE
            WHEN FORMAT_DATE('%A', created_at) = 'Sunday' THEN 1
            WHEN FORMAT_DATE('%A', created_at) = 'Monday' THEN 2
            WHEN FORMAT_DATE('%A', created_at) = 'Tuesday' THEN 3
            WHEN FORMAT_DATE('%A', created_at) = 'Wednesday' THEN 4
            WHEN FORMAT_DATE('%A', created_at) = 'Thursday' THEN 5
            WHEN FORMAT_DATE('%A', created_at) = 'Friday' THEN 6
            WHEN FORMAT_DATE('%A', created_at) = 'Saturday' THEN 7
        END,
        hora_dia
    """


