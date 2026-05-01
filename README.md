# Data Insights Pipeline com IA

> Pipeline de dados end-to-end que coleta, processa e gera insights automáticos com IA — pronto para produção.

---

## Problema

Empresas acumulam dados, mas raramente conseguem extrair valor deles com velocidade. Análises manuais são lentas, caras e não escalam. Insights ficam presos em planilhas que ninguém lê.

## Solução

Um pipeline automatizado que vai da coleta ao insight em minutos:

```
API Externa → Ingestão Python → PostgreSQL → Transformação → IA (Groq) → Relatório
```

Sem dashboards caros. Sem dependência de times de BI. Análise contínua, acionável e escalável.

---

## Arquitetura

```
data-insights-pipeline/
│
├── src/
│   ├── config.py       # Variáveis de ambiente centralizadas
│   ├── ingest.py       # Coleta da API + persistência no banco
│   ├── transform.py    # Transformações + exportação de sumário
│   └── analyze.py      # Geração de insights com OpenAI
│
├── sql/
│   └── schema.sql      # DDL da tabela sales
│
├── data/
│   └── raw/            # JSON bruto + CSV sumário + relatório .md
│
├── requirements.txt
├── .env                # Credenciais 
└── README.md
```

---

## Tecnologias

| Camada        | Tecnologia           |
|---------------|----------------------|
| Linguagem     | Python 3.11+         |
| Banco         | PostgreSQL           |
| Transformação | Pandas               |
| IA            | Groq (llama-3.3-70b) |
| API Fonte     | FakeStore API        |
| Config        | python-dotenv        |

---

## Como rodar

### 1. Clone e instale dependências

```bash
git clone https://github.com/aleesousa/data-insights-pipeline.git
cd data-insights-pipeline
pip install -r requirements.txt
```

### 2. Configure o ambiente

```bash
cp .env.example .env
# edite .env com suas credenciais
```

### 3. Crie o banco

```bash
psql -U postgres -c "CREATE DATABASE dados;"
psql -U postgres -d dados -f sql/schema.sql
```

### 4. Execute o pipeline

```bash
# Passo 1 — Ingestão
python src/ingest.py

# Passo 2 — Transformação
python src/transform.py

# Passo 3 — Insights com IA
python src/analyze.py
```

---

## Resultado

Ao final do pipeline você terá:

- **Dados estruturados** no PostgreSQL, prontos para consultas
- **Sumário analítico** em `data/raw/summary.csv`
- **Relatório de insights** em `data/raw/insights.md`, gerado por IA

Exemplo de output do `analyze.py`:

```
============================================================
INSIGHTS GERADOS PELA IA
============================================================

📌 Resumo Executivo
A categoria "electronics" concentra 42% da receita total, com ticket
médio 3x superior às demais categorias. A base de produtos tem boa
cobertura de avaliações (média 3.9/5).

🔍 Principais Achados
• Receita total: $1.847 | Categorias ativas: 4
• "Electronics" lidera com $780 (+42% do total)
• Produto mais lucrativo: "Fjallraven Backpack" — $109,95
• Rating médio da categoria top: 4.1

⚠️ Alertas
• Categoria "women's clothing" com menor ticket médio ($28)
• Concentração de receita em uma única categoria = risco

🚀 Recomendações
1. Ampliar mix de "electronics" com produtos de maior giro
2. Testar bundle de "women's clothing" para elevar ticket
3. Monitorar rating abaixo de 3.5 como sinal de churn
============================================================
```

---

## Próximos passos (roadmap)

- [ ] Agendamento via Airflow ou cron
- [ ] Suporte a múltiplas APIs de fonte
- [ ] Dashboard com Streamlit
- [ ] Alertas automáticos por e-mail

---

## Autor

Alexandre Pereira de Sousa