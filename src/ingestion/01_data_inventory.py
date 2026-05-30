from pathlib import Path
import pandas as pd

BRONZE_PATH = Path("data/bronze")

inventario = []

for arquivo in BRONZE_PATH.glob("*.csv"):

    df = pd.read_csv(
        arquivo,
        encoding="utf-8",
        low_memory=False
    )

    inventario.append({
        "arquivo": arquivo.name,
        "linhas": df.shape[0],
        "colunas": df.shape[1],
        "memoria_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    })

catalogo = pd.DataFrame(inventario)

catalogo.to_csv(
    "docs/data_catalog.csv",
    index=False
)

print(catalogo)
print("\nCatálogo salvo em docs/data_catalog.csv")