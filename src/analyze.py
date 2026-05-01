"""
analyze.py — Gera insights de negócio com IA usando Google Gemini (GRATUITO).

Pré-requisitos:
  1. pip install google-generativeai python-dotenv
  2. Crie sua chave gratuita em: https://aistudio.google.com/apikey
  3. Adicione no .env:  GEMINI_API_KEY=sua_chave_aqui

Limites do plano gratuito (mais que suficiente pra projetos):
  - 1.500 requisições / dia
  - 1 milhão de tokens / minuto
  - Sem custo nenhum
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

from google import genai  
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ── Configuração ───────────────────────────────────────────────
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"       # modelo gratuito
DATA_SUMMARY_PATH = "data/raw/summary.csv"
INSIGHTS_PATH = "data/raw/insights.md"


# ── 1. Leitura do sumário ──────────────────────────────────────
def load_summary(path: str = DATA_SUMMARY_PATH) -> str:
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Arquivo {path} não encontrado. Execute transform.py primeiro."
        )
    return Path(path).read_text(encoding="utf-8")


# ── 2. System prompt ───────────────────────────────────────────
SYSTEM_PROMPT = """
Você é um analista de dados sênior especializado em e-commerce.
Analise os dados de vendas fornecidos e gere insights acionáveis,
claros e diretos para uma equipe de negócio não-técnica.

Estruture SEMPRE sua resposta assim:

1. 📌 Resumo Executivo (2–3 frases)
2. 🔍 Principais Achados (bullet points com números)
3. ⚠️ Alertas ou Riscos
4. 🚀 Recomendações (priorizadas por impacto)
""".strip()


# ── 3. Chamada à API Gemini ────────────────────────────────────
def generate_insights(summary: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY não encontrada.")

    log.info(f"Chamando Google Gemini ({GEMINI_MODEL}) …")

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options={"api_version": "v1"}
    )

    prompt = f"""
{SYSTEM_PROMPT}

Analise os dados de vendas abaixo e gere insights:

{summary}
""".strip()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text


# ── 4. Salva relatório ─────────────────────────────────────────
def save_insights(insights: str, path: str = INSIGHTS_PATH) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    header = f"# Insights — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    Path(path).write_text(header + insights, encoding="utf-8")
    log.info(f"Relatório salvo em {path}")


# ── Main ───────────────────────────────────────────────────────
def run():
    summary  = load_summary()
    insights = generate_insights(summary)

    print("\n" + "=" * 60)
    print("🤖 INSIGHTS GERADOS PELA IA (Gemini - Gratuito)")
    print("=" * 60)
    print(insights)
    print("=" * 60 + "\n")

    save_insights(insights)
    log.info("✅ Análise concluída.")


if __name__ == "__main__":
    run()