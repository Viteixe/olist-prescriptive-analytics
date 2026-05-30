from pathlib import Path
import pandas as pd

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")

SILVER_PATH.mkdir(parents=True, exist_ok=True)


def read_csv(file_name: str) -> pd.DataFrame:
    return pd.read_csv(
        BRONZE_PATH / file_name,
        encoding="utf-8",
        low_memory=False
    )


def save_parquet(df: pd.DataFrame, file_name: str) -> None:
    output_path = SILVER_PATH / file_name
    df.to_parquet(output_path, index=False)
    print(f"Salvo: {output_path}")


orders = read_csv("olist_orders_dataset.csv")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

orders["is_delivered"] = orders["order_status"].eq("delivered").astype(int)
orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.days

save_parquet(orders, "orders.parquet")


customers = read_csv("olist_customers_dataset.csv")
customers["customer_city"] = customers["customer_city"].str.strip().str.lower()
customers["customer_state"] = customers["customer_state"].str.strip().str.upper()

save_parquet(customers, "customers.parquet")


sellers = read_csv("olist_sellers_dataset.csv")
sellers["seller_city"] = sellers["seller_city"].str.strip().str.lower()
sellers["seller_state"] = sellers["seller_state"].str.strip().str.upper()

save_parquet(sellers, "sellers.parquet")


products = read_csv("olist_products_dataset.csv")
translation = read_csv("product_category_name_translation.csv")

products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

products["product_category_name"] = products["product_category_name"].fillna("unknown")
products["product_category_name_english"] = products["product_category_name_english"].fillna("unknown")

numeric_cols = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

for col in numeric_cols:
    products[col] = products[col].fillna(0)

save_parquet(products, "products.parquet")


items = read_csv("olist_order_items_dataset.csv")
items["shipping_limit_date"] = pd.to_datetime(items["shipping_limit_date"], errors="coerce")

save_parquet(items, "order_items.parquet")


payments = read_csv("olist_order_payments_dataset.csv")

save_parquet(payments, "payments.parquet")


reviews = read_csv("olist_order_reviews_dataset.csv")

reviews["review_creation_date"] = pd.to_datetime(
    reviews["review_creation_date"],
    errors="coerce"
)

reviews["review_answer_timestamp"] = pd.to_datetime(
    reviews["review_answer_timestamp"],
    errors="coerce"
)

reviews["review_comment_title"] = reviews["review_comment_title"].fillna("")
reviews["review_comment_message"] = reviews["review_comment_message"].fillna("")

save_parquet(reviews, "reviews.parquet")


geolocation = read_csv("olist_geolocation_dataset.csv")
geolocation["geolocation_city"] = geolocation["geolocation_city"].str.strip().str.lower()
geolocation["geolocation_state"] = geolocation["geolocation_state"].str.strip().str.upper()

save_parquet(geolocation, "geolocation.parquet")

print("\nCamada Silver criada com sucesso em formato Parquet.")