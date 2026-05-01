"""
transform.py — Lê o banco, transforma e exporta sumário para CSV.

Transformações aplicadas:
  - total_revenue por produto  (price × quantity)
  - médias e rankings por categoria
  - exporta data/raw/summary.csv para alimentar analyze.py
"""

import sys
import logging
from pathlib import Path

import pandas as pd
import psycopg2

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_CONFIG, DATA_SUMMARY_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ── 1. Extração ────────────────────────────────────────────────
def extract_from_db() -> pd.DataFrame:
    log.info("Lendo dados do PostgreSQL …")
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM sales ORDER BY sale_date DESC", conn)
    conn.close()
    log.info(f"{len(df)} linhas carregadas.")
    return df


# ── 2. Transformação ───────────────────────────────────────────
def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Receita total por produto
    df["total_revenue"] = df["price"] * df["quantity"]

    # Sumário por categoria
    category_summary = (
        df.groupby("category")
        .agg(
            total_revenue=("total_revenue", "sum"),
            avg_price=("price", "mean"),
            avg_rating=("rating", "mean"),
            num_products=("product", "count"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    # Top 5 produtos por receita
    top_products = (
        df[["product", "category", "price", "quantity", "total_revenue", "rating"]]
        .sort_values("total_revenue", ascending=False)
        .head(5)
    )

    return category_summary, top_products


# ── 3. Export ──────────────────────────────────────────────────
def export_summary(category_summary: pd.DataFrame, top_products: pd.DataFrame) -> None:
    Path(DATA_SUMMARY_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Junta tudo num único CSV legível pela IA
    with open(DATA_SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("=== RESUMO POR CATEGORIA ===\n")
        f.write(category_summary.to_string(index=False))
        f.write("\n\n=== TOP 5 PRODUTOS POR RECEITA ===\n")
        f.write(top_products.to_string(index=False))

    log.info(f"Sumário exportado para {DATA_SUMMARY_PATH}")


# ── Main ───────────────────────────────────────────────────────
def run():
    df = extract_from_db()
    category_summary, top_products = transform(df)

    print("\n Resumo por Categoria:")
    print(category_summary.to_string(index=False))
    print("\n Top 5 Produtos:")
    print(top_products.to_string(index=False))

    export_summary(category_summary, top_products)
    log.info("✅ Transformação concluída.")


if __name__ == "__main__":
    run()
