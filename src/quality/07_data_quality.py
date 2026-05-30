from pathlib import Path
import pandas as pd

GOLD_PATH = Path("data/gold")
QUALITY_PATH = Path("data/quality")

QUALITY_PATH.mkdir(parents=True, exist_ok=True)

report = []

# =========================
# CUSTOMER
# =========================

customer = pd.read_parquet(GOLD_PATH / "dim_customer.parquet")

report.append({
    "table": "dim_customer",
    "check": "duplicated_customer_id",
    "value": customer["customer_id"].duplicated().sum()
})

report.append({
    "table": "dim_customer",
    "check": "null_customer_id",
    "value": customer["customer_id"].isna().sum()
})

# =========================
# PRODUCT
# =========================

product = pd.read_parquet(GOLD_PATH / "dim_product.parquet")

report.append({
    "table": "dim_product",
    "check": "duplicated_product_id",
    "value": product["product_id"].duplicated().sum()
})

report.append({
    "table": "dim_product",
    "check": "null_product_id",
    "value": product["product_id"].isna().sum()
})

# =========================
# SELLER
# =========================

seller = pd.read_parquet(GOLD_PATH / "dim_seller.parquet")

report.append({
    "table": "dim_seller",
    "check": "duplicated_seller_id",
    "value": seller["seller_id"].duplicated().sum()
})

report.append({
    "table": "dim_seller",
    "check": "null_seller_id",
    "value": seller["seller_id"].isna().sum()
})

# =========================
# FACT ORDERS
# =========================

orders = pd.read_parquet(GOLD_PATH / "fact_orders.parquet")

orphan_customer = (
    ~orders["customer_id"].isin(customer["customer_id"])
).sum()

orphan_product = (
    ~orders["product_id"].isin(product["product_id"])
).sum()

orphan_seller = (
    ~orders["seller_id"].isin(seller["seller_id"])
).sum()

report.append({
    "table": "fact_orders",
    "check": "orphan_customer",
    "value": orphan_customer
})

report.append({
    "table": "fact_orders",
    "check": "orphan_product",
    "value": orphan_product
})

report.append({
    "table": "fact_orders",
    "check": "orphan_seller",
    "value": orphan_seller
})

# =========================
# EXPORT
# =========================

quality_report = pd.DataFrame(report)

quality_report.to_parquet(
    QUALITY_PATH / "quality_report.parquet",
    index=False
)

print("\nRelatório de qualidade criado com sucesso.")
print(quality_report)