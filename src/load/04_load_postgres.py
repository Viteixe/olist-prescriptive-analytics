from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

GOLD_PATH = Path("data/gold")

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist_dw"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

tables = {
    "dim_customer": "dim_customer.parquet",
    "dim_date": "dim_date.parquet",
    "dim_product": "dim_product.parquet",
    "dim_seller": "dim_seller.parquet",
    "fact_orders": "fact_orders.parquet",
    "fact_payments": "fact_payments.parquet",
    "fact_reviews": "fact_reviews.parquet",
}

for table_name, file_name in tables.items():
    df = pd.read_parquet(GOLD_PATH / file_name)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Tabela carregada no PostgreSQL: {table_name} ({len(df)} linhas)")

print("\nCarga Gold → PostgreSQL concluída com sucesso.")