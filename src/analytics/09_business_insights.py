import pandas as pd
from pathlib import Path

ANALYTICS_PATH = Path("data/analytics")

# ==========================
# Carregar datasets
# ==========================

sales = pd.read_parquet(
    ANALYTICS_PATH / "sales_by_category.parquet"
)

customers = pd.read_parquet(
    ANALYTICS_PATH / "customers_by_state.parquet"
)

delivery = pd.read_parquet(
    ANALYTICS_PATH / "delivery_status.parquet"
)

reviews = pd.read_parquet(
    ANALYTICS_PATH / "review_distribution.parquet"
)

kpis = pd.read_parquet(
    ANALYTICS_PATH / "executive_kpis.parquet"
)

insights = []

# ==========================
# Categoria mais vendida
# ==========================

top_category = sales.iloc[0]

insights.append({
    "tipo": "Vendas",
    "insight":
        f"A categoria mais vendida é "
        f"{top_category['product_category_name_english']} "
        f"com {int(top_category['total_vendas'])} vendas."
})

# ==========================
# Estado com mais clientes
# ==========================

top_state = customers.iloc[0]

insights.append({
    "tipo": "Clientes",
    "insight":
        f"O estado com mais clientes é "
        f"{top_state['customer_state']} "
        f"com {int(top_state['total_clientes'])} clientes."
})

# ==========================
# Percentual de atraso
# ==========================

delay = kpis[
    kpis["kpi"] == "% Pedidos Atrasados"
]["valor"].iloc[0]

insights.append({
    "tipo": "Logística",
    "insight":
        f"{delay:.2f}% dos pedidos foram entregues com atraso."
})

# ==========================
# Avaliação média
# ==========================

rating = kpis[
    kpis["kpi"] == "Avaliação Média"
]["valor"].iloc[0]

insights.append({
    "tipo": "Satisfação",
    "insight":
        f"A nota média dos clientes é {rating:.2f}."
})

# ==========================
# Nota 5
# ==========================

nota5 = reviews[
    reviews["review_score"] == 5
]["quantidade"].iloc[0]

total_reviews = reviews["quantidade"].sum()

percentual_5 = (
    nota5 / total_reviews
) * 100

insights.append({
    "tipo": "Satisfação",
    "insight":
        f"{percentual_5:.2f}% das avaliações receberam nota máxima."
})

# ==========================
# Exportar
# ==========================

business_insights = pd.DataFrame(insights)

business_insights.to_parquet(
    ANALYTICS_PATH / "business_insights.parquet",
    index=False
)

business_insights.to_csv(
    ANALYTICS_PATH / "business_insights.csv",
    index=False
)

print("\nInsights gerados com sucesso.\n")
print(business_insights)