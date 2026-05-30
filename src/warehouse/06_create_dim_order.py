from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

GOLD_PATH = Path("data/gold")

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/olist_dw"
)

fact_orders = pd.read_parquet(GOLD_PATH / "fact_orders.parquet")
fact_payments = pd.read_parquet(GOLD_PATH / "fact_payments.parquet")
fact_reviews = pd.read_parquet(GOLD_PATH / "fact_reviews.parquet")

orders_ids = pd.concat([
    fact_orders[["order_id"]],
    fact_payments[["order_id"]],
    fact_reviews[["order_id"]],
])

dim_order = orders_ids.drop_duplicates().reset_index(drop=True)

dim_order.to_parquet(
    GOLD_PATH / "dim_order.parquet",
    index=False
)

dim_order.to_sql(
    "dim_order",
    engine,
    if_exists="replace",
    index=False
)

print(f"dim_order criada com sucesso: {len(dim_order)} pedidos únicos")
