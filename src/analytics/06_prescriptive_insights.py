import pandas as pd
from pathlib import Path

# =====================================================
# Caminhos
# =====================================================

ANALYTICS_PATH = Path("data/analytics")

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

recommendations = []

# =====================================================
# Categoria mais vendida
# =====================================================

top_category = sales.iloc[0]

recommendations.append({
    "tipo": "Vendas",
    "insight": f"Categoria líder: {top_category.iloc[0]}",
    "recomendacao": "Investir em campanhas e estoque desta categoria."
})

# =====================================================
# Estado com mais clientes
# =====================================================

top_state = customers.iloc[0]

recommendations.append({
    "tipo": "Clientes",
    "insight": f"Maior concentração de clientes em {top_state.iloc[0]}",
    "recomendacao": "Avaliar expansão logística e campanhas regionais."
})

# =====================================================
# Entregas
# =====================================================

delivery_metric = delivery.iloc[0]

recommendations.append({
    "tipo": "Logística",
    "insight": str(delivery_metric.iloc[0]),
    "recomendacao": "Monitorar transportadoras e reduzir atrasos."
})

# =====================================================
# Avaliações
# =====================================================

nota1 = reviews[
    reviews["review_score"] == 1
]["quantidade"].sum()

nota5 = reviews[
    reviews["review_score"] == 5
]["quantidade"].sum()

if nota1 > 10000:
    recommendations.append({
        "tipo": "Satisfação",
        "insight": f"{nota1} avaliações nota 1",
        "recomendacao": "Investigar causas de insatisfação."
    })

recommendations.append({
    "tipo": "Satisfação",
    "insight": f"{nota5} avaliações nota 5",
    "recomendacao": "Identificar boas práticas dos vendedores."
})

# =====================================================
# Salvar resultado
# =====================================================

recommendations_df = pd.DataFrame(recommendations)

recommendations_df.to_parquet(
    ANALYTICS_PATH / "prescriptive_recommendations.parquet",
    index=False
)

print("\nRecomendações geradas com sucesso.")
