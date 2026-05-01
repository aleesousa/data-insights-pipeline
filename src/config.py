"""
config.py — Centraliza variáveis de ambiente do pipeline.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ── Banco de dados ─────────────────────────────────────────────
DB_CONFIG = {
    "dbname":   os.getenv("DB_NAME",     "dados"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
}

# ── IA ─────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-2.5-flash"
    
# ── API Externa ────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "https://fakestoreapi.com/products")

# ── Paths ──────────────────────────────────────────────────────
DATA_RAW_PATH     = "data/raw/products.json"
DATA_SUMMARY_PATH = "data/raw/summary.csv"
