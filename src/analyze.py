"""
analyze.py — Gera insights com Groq (gratuito)
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
DATA_SUMMARY_PATH = "data/raw/summary.csv"
INSIGHTS_PATH     = "data/raw/insights.md"

SYSTEM_PROMPT = """
Você é um analista de dados sênior especializado em e-commerce.
Analise os dados de vendas e gere insights acionáveis para uma equipe não-técnica.

Estruture sua resposta em:
1. 📌 Resumo Executivo (2–3 frases)
2. 🔍 Principais Achados (bullet points com números)
3. ⚠️ Alertas ou Riscos
4. 🚀 Recomendações (priorizadas por impacto)
""".strip()


def load_summary() -> str:
    if not Path(DATA_SUMMARY_PATH).exists():
        raise FileNotFoundError("Execute transform.py primeiro.")
    return Path(DATA_SUMMARY_PATH).read_text(encoding="utf-8")


def generate_insights(summary: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY não encontrada no .env")

    client = Groq(api_key=GROQ_API_KEY)

    log.info("Chamando Groq (llama-3.3-70b) …")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Dados:\n{summary}\n\nData: {datetime.now().strftime('%d/%m/%Y %H:%M')}"},
        ],
        temperature=0.4,
        max_tokens=1000,
    )

    return response.choices[0].message.content


def save_insights(insights: str) -> None:
    Path(INSIGHTS_PATH).parent.mkdir(parents=True, exist_ok=True)
    header = f"# Insights — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    Path(INSIGHTS_PATH).write_text(header + insights, encoding="utf-8")
    log.info(f"Relatório salvo em {INSIGHTS_PATH}")


def run():
    summary  = load_summary()
    insights = generate_insights(summary)

    print("\n" + "=" * 60)
    print("🤖 INSIGHTS GERADOS PELA IA (Groq - Gratuito)")
    print("=" * 60)
    print(insights)
    print("=" * 60 + "\n")

    save_insights(insights)
    log.info("✅ Análise concluída.")


if __name__ == "__main__":
    run()