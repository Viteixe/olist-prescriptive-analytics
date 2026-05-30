import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

ANALYTICS_PATH = Path("data/analytics")
ANALYTICS_PATH.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/olist_dw"
)

kpis = []

# Receita Total
receita = pd.read_sql("""
SELECT ROUND(SUM(payment_value)::numeric, 2) AS valor
FROM fact_payments
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Receita Total",
    "valor": float(receita),
    "categoria": "Financeiro"
})

# Ticket Médio
ticket = pd.read_sql("""
SELECT ROUND(AVG(payment_value)::numeric, 2) AS valor
FROM fact_payments
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Ticket Médio",
    "valor": float(ticket),
    "categoria": "Financeiro"
})

# Total de Pedidos
pedidos = pd.read_sql("""
SELECT COUNT(DISTINCT order_id) AS valor
FROM dim_order
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Total de Pedidos",
    "valor": int(pedidos),
    "categoria": "Vendas"
})

# Total de Clientes
clientes = pd.read_sql("""
SELECT COUNT(DISTINCT customer_id) AS valor
FROM dim_customer
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Total de Clientes",
    "valor": int(clientes),
    "categoria": "Clientes"
})

# Total de Produtos
produtos = pd.read_sql("""
SELECT COUNT(DISTINCT product_id) AS valor
FROM dim_product
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Total de Produtos",
    "valor": int(produtos),
    "categoria": "Produtos"
})

# Avaliação Média
avaliacao = pd.read_sql("""
SELECT ROUND(AVG(review_score)::numeric, 2) AS valor
FROM fact_reviews
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "Avaliação Média",
    "valor": float(avaliacao),
    "categoria": "Satisfação"
})

# Percentual de Atraso
atraso = pd.read_sql("""
SELECT
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN delivery_delay_days > 0 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS valor
FROM fact_orders
""", engine).iloc[0]["valor"]

kpis.append({
    "kpi": "% Pedidos Atrasados",
    "valor": float(atraso),
    "categoria": "Logística"
})

executive_kpis = pd.DataFrame(kpis)

executive_kpis.to_parquet(
    ANALYTICS_PATH / "executive_kpis.parquet",
    index=False
)

executive_kpis.to_csv(
    ANALYTICS_PATH / "executive_kpis.csv",
    index=False
)

print("\nKPIs executivos gerados com sucesso.")
print(executive_kpis)