import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

ANALYTICS_PATH = Path("data/analytics")
ANALYTICS_PATH.mkdir(exist_ok=True)

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/olist_dw"
)

sales_category = pd.read_sql("""
SELECT
    p.product_category_name_english,
    COUNT(*) AS total_vendas,
    ROUND(
        SUM(f.total_order_item_value)::numeric,
        2
    ) AS faturamento
FROM fact_orders f
JOIN dim_product p
ON f.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY faturamento DESC
""", engine)

sales_category.to_parquet(
    ANALYTICS_PATH / "sales_by_category.parquet",
    index=False
)

print("sales_by_category criado")

customers_state = pd.read_sql("""
SELECT
    customer_state,
    COUNT(*) AS total_clientes
FROM dim_customer
GROUP BY customer_state
ORDER BY total_clientes DESC
""", engine)

customers_state.to_parquet(
    ANALYTICS_PATH / "customers_by_state.parquet",
    index=False
)

print("customers_by_state criado")

delivery = pd.read_sql("""
SELECT
    is_delivered,
    COUNT(*) AS total
FROM fact_orders
GROUP BY is_delivered
""", engine)

delivery.to_parquet(
    ANALYTICS_PATH / "delivery_status.parquet",
    index=False
)

print("delivery_status criado")

reviews = pd.read_sql("""
SELECT
    review_score,
    COUNT(*) AS quantidade
FROM fact_reviews
GROUP BY review_score
ORDER BY review_score
""", engine)

reviews.to_parquet(
    ANALYTICS_PATH / "review_distribution.parquet",
    index=False
)

print("review_distribution criado")

print("\nAnalytics gerados com sucesso.")