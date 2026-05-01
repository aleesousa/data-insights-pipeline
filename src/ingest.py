"""
ingest.py — Coleta dados da API e persiste no PostgreSQL.

Fluxo:
  1. Busca produtos em API_URL (FakeStore por padrão)
  2. Salva JSON bruto em data/raw/
  3. Insere/atualiza registros na tabela `sales`
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime

import requests
import psycopg2

# Adiciona raiz do projeto ao path para importar config
sys.path.insert(0, str(Path(__file__).parent))
from config import API_URL, DB_CONFIG, DATA_RAW_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ── 1. Fetch ───────────────────────────────────────────────────
def fetch_data(url: str) -> list[dict]:
    log.info(f"Buscando dados em {url} …")
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    log.info(f"{len(data)} registros recebidos.")
    return data


# ── 2. Persistência local (raw) ────────────────────────────────
def save_raw(data: list[dict], path: str = DATA_RAW_PATH) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"JSON bruto salvo em {path}")


# ── 3. Inserção no banco ───────────────────────────────────────
def load_to_db(data: list[dict]) -> None:
    log.info("Conectando ao PostgreSQL …")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    inserted = 0
    for item in data:
        rating_rate = item.get("rating", {}).get("rate") if item.get("rating") else None
        cursor.execute(
            """
            INSERT INTO sales (product, category, price, quantity, rating, sale_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                item.get("title", "Unknown")[:200],
                item.get("category", "unknown")[:100],
                float(item.get("price", 0)),
                1,
                rating_rate,
                datetime.now(),
            ),
        )
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    log.info(f"{inserted} registros inseridos no banco.")


# ── Main ───────────────────────────────────────────────────────
def run():
    data = fetch_data(API_URL)
    save_raw(data)
    load_to_db(data)
    log.info("Ingestão concluída.")


if __name__ == "__main__":
    run()
