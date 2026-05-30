from pathlib import Path
import pandas as pd

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")

GOLD_PATH.mkdir(parents=True, exist_ok=True)


def read_parquet(file_name: str) -> pd.DataFrame:
    return pd.read_parquet(SILVER_PATH / file_name)


def save_parquet(df: pd.DataFrame, file_name: str) -> None:
    output_path = GOLD_PATH / file_name
    df.to_parquet(output_path, index=False)
    print(f"Salvo: {output_path}")


orders = read_parquet("orders.parquet")
items = read_parquet("order_items.parquet")
customers = read_parquet("customers.parquet")
products = read_parquet("products.parquet")
sellers = read_parquet("sellers.parquet")
payments = read_parquet("payments.parquet")
reviews = read_parquet("reviews.parquet")


dim_customer = customers[[
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
]].drop_duplicates()

save_parquet(dim_customer, "dim_customer.parquet")


dim_product = products[[
    "product_id",
    "product_category_name",
    "product_category_name_english",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_photos_qty"
]].drop_duplicates()

save_parquet(dim_product, "dim_product.parquet")


dim_seller = sellers[[
    "seller_id",
    "seller_city",
    "seller_state"
]].drop_duplicates()

save_parquet(dim_seller, "dim_seller.parquet")


date_base = orders[["order_purchase_timestamp"]].dropna().copy()
date_base["date"] = date_base["order_purchase_timestamp"].dt.date
date_base = date_base[["date"]].drop_duplicates()

dim_date = pd.DataFrame()
dim_date["date"] = pd.to_datetime(date_base["date"])
dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.month_name()
dim_date["week"] = dim_date["date"].dt.isocalendar().week.astype(int)
dim_date["day"] = dim_date["date"].dt.day
dim_date["day_of_week"] = dim_date["date"].dt.day_name()

dim_date = dim_date[[
    "date_key",
    "date",
    "year",
    "quarter",
    "month",
    "month_name",
    "week",
    "day",
    "day_of_week"
]]

save_parquet(dim_date, "dim_date.parquet")


fact_orders = items.merge(
    orders,
    on="order_id",
    how="left"
)

fact_orders["date_key"] = fact_orders["order_purchase_timestamp"].dt.strftime("%Y%m%d")
fact_orders["date_key"] = pd.to_numeric(fact_orders["date_key"], errors="coerce").astype("Int64")

fact_orders["total_order_item_value"] = fact_orders["price"] + fact_orders["freight_value"]

fact_orders = fact_orders[[
    "order_id",
    "order_item_id",
    "customer_id",
    "seller_id",
    "product_id",
    "date_key",
    "order_status",
    "price",
    "freight_value",
    "total_order_item_value",
    "delivery_delay_days",
    "is_delivered"
]]

save_parquet(fact_orders, "fact_orders.parquet")


fact_payments = payments[[
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value"
]].copy()

save_parquet(fact_payments, "fact_payments.parquet")


fact_reviews = reviews[[
    "review_id",
    "order_id",
    "review_score",
    "review_creation_date",
    "review_answer_timestamp"
]].copy()

save_parquet(fact_reviews, "fact_reviews.parquet")


print("\nCamada Gold criada com sucesso em formato Parquet.")