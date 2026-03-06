# 🏢 Arch Company AI — HUB de Agentes Inteligentes

Dashboard inteligente com 8 agentes de IA para a Arch Company.
Construído com **Streamlit + CrewAI + Claude (Anthropic) + Grok (xAI)**.

---

## 🤖 Os 8 Agentes

| # | Nome | Cargo | Modelo |
|---|------|-------|--------|
| 01 | **Archie** | CEO / Estrategista | Claude Opus 4.5 |
| 02 | **Finley** | CFO / Financeiro | Claude Sonnet 4.5 |
| 03 | **Xara** | CMO / Marketing | Grok 3 (xAI) |
| 04 | **Shield** | CTO / Tecnologia | Claude Sonnet 4.5 |
| 05 | **Memo** | Memória / Arquivo | Claude Haiku 4.5 + ChromaDB |
| 06 | **Nexus** | Auto-Aprimoramento | Claude Sonnet 4.5 |
| 07 | **Henrio** | Assistente Pessoal | Claude Sonnet 4.5 |
| 08 | **Nexo** | Integrações / API | Claude Haiku 4.5 |

---

## 🚀 Rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/arch-company-ai.git
cd arch-company-ai

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
# Crie um arquivo .env com:
# ANTHROPIC_API_KEY=sk-ant-...
# XAI_API_KEY=xai-...

# 4. Rode o dashboard
streamlit run app.py
```

Acesse em: **http://localhost:8501**

---

## ⚙️ Variáveis de Ambiente

Configure no Railway (ou no `.env` local):

| Variável | Descrição |
|----------|-----------|
| `ANTHROPIC_API_KEY` | API Key da Anthropic (Claude) |
| `XAI_API_KEY` | API Key da xAI (Grok) |

---

## 🏗️ Stack Tecnológica

- **[Streamlit](https://streamlit.io/)** — Dashboard web em Python
- **[CrewAI](https://crewai.com/)** — Orquestração de agentes IA
- **[Anthropic](https://anthropic.com/)** — Claude Opus/Sonnet/Haiku
- **[xAI](https://x.ai/)** — Grok 3
- **[ChromaDB](https://www.trychroma.com/)** — Memória vetorial persistente
- **[Railway](https://railway.app/)** — Hospedagem em nuvem

---

## 📁 Estrutura

```
arch_company_dashboard/
├── app.py              ← Dashboard principal
├── agents.py           ← Definição dos 8 agentes (CrewAI)
├── memory.py           ← Sistema de memória (ChromaDB)
├── requirements.txt    ← Dependências Python
├── Procfile            ← Configuração Railway
├── railway.toml        ← Configuração Railway
└── .env                ← API Keys (NÃO enviar ao GitHub)
```

---

*Arch Company AI — Henrique Adams*
