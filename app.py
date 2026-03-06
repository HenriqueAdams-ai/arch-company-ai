# ============================================================
# ARCH COMPANY AI — Dashboard Principal
# ============================================================
# Instale as dependencias:
#   pip install streamlit crewai anthropic chromadb gspread
#   pip install google-auth google-auth-oauthlib plotly pandas
#
# Execute com:
#   streamlit run app.py
# ============================================================

import streamlit as st
import json
import os
from datetime import datetime

# ── Configuracao da Pagina ───────────────────────────────────────────────
st.set_page_config(
    page_title="Arch Company AI",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Personalizado ─────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo geral */
    .stApp { background-color: #0F172A; color: #F1F5F9; }

    /* Sidebar */
    .css-1d391kg { background-color: #1E293B; }

    /* Cards de metricas */
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
    }

    /* Chat input */
    .stChatInput { background-color: #1E293B; }

    /* Titulo do header */
    h1, h2, h3 { color: #F1F5F9 !important; }

    /* Status badge */
    .agent-active { color: #22C55E; font-weight: bold; }
    .agent-standby { color: #F59E0B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ── Importacoes dos Agentes ──────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

# ── Sistema de Memoria (Memo) ─────────────────────────────────────────────
try:
    from memory import (
        salvar_memoria,
        buscar_memorias,
        formatar_contexto_memo,
        total_memorias,
        listar_memorias_recentes,
    )
    MEMORIA_ATIVA = True
except Exception as e:
    MEMORIA_ATIVA = False
    _erro_memoria = str(e)

# ── Estado da Sessao ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Status dos Agentes e Configuracoes
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏢 Arch Company AI")
    st.markdown("---")

    st.markdown("### 🤖 Time de Agentes")

    agentes = [
        {"num": "01", "nome": "Archie-Solomon",   "cargo": "CEO / Gestor",              "status": "Ativo", "modelo": "Claude Opus",   "cor": "🔵"},
        {"num": "02", "nome": "Finley-Midas",     "cargo": "CFO / Financeiro",          "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🟢"},
        {"num": "03", "nome": "Xara-Iris",        "cargo": "CMO / Marketing + RH",      "status": "Ativo", "modelo": "Grok 3",        "cor": "🔵"},
        {"num": "04", "nome": "Shield-Michael",   "cargo": "T.I / Seguranca / Backups", "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🔴"},
        {"num": "05", "nome": "Memo-Engram",      "cargo": "Memoria / Contexto",        "status": "Ativo", "modelo": "Claude Haiku",  "cor": "🟡"},
        {"num": "06", "nome": "Nexus-Apollo",     "cargo": "Auto-Aprimoramento",        "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🟣"},
        {"num": "07", "nome": "Henrio-Julia",     "cargo": "Assistente Pessoal",        "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🔵"},
        {"num": "08", "nome": "Nexo-Link Vector", "cargo": "Integracoes / API",         "status": "Ativo", "modelo": "Claude Haiku",  "cor": "⚪"},
    ]

    for ag in agentes:
        status_icon = "🟢" if ag["status"] == "Ativo" else "🟡"
        st.markdown(
            f"**{ag['cor']} {ag['nome']}** — {ag['cargo']}\n"
            f"{status_icon} {ag['status']} | {ag['modelo']}"
        )
        st.markdown("---")

    st.markdown("### ⚙️ Configuracoes")
    api_anthropic = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    api_xai = st.text_input("xAI (Grok) API Key", type="password", placeholder="xai-...")

    if st.button("💾 Salvar Chaves", use_container_width=True):
        if api_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = api_anthropic
        if api_xai:
            os.environ["XAI_API_KEY"] = api_xai
        st.success("Chaves salvas na sessao!")

    st.markdown("---")
    st.markdown("### 🧠 Memo — Status da Memoria")
    if MEMORIA_ATIVA:
        try:
            n_mem = total_memorias()
            st.success(f"✅ ChromaDB ativo | {n_mem} memórias salvas")
            if n_mem > 0 and st.button("🔍 Ver ultimas memorias", use_container_width=True):
                recentes = listar_memorias_recentes(5)
                for m in recentes:
                    st.caption(f"[{m['tipo']}] {m['data']} {m['hora']} — {m['conteudo'][:80]}...")
        except Exception:
            st.warning("⚠️ Memoria ativa mas sem dados ainda")
    else:
        st.warning("⚠️ ChromaDB inativo. Instale: pip install chromadb")

    st.markdown("---")
    st.markdown("### 📁 Google Drive")
    sheet_url = st.text_input("URL da Planilha", placeholder="https://docs.google.com/...")
    if st.button("🔗 Conectar Drive", use_container_width=True):
        st.info("Configure o arquivo credentials.json do Google Cloud primeiro.")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN — Dashboard Principal
# ══════════════════════════════════════════════════════════════════════════════
st.title("🏢 Arch Company — HUB de Agentes IA")
st.caption(f"Dashboard Financeiro Inteligente | {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ── Tabs Principais ─────────────────────────────────────────────────────────────────────────────
tab_dash, tab_chat, tab_agentes, tab_config = st.tabs([
    "📊 Dashboard", "💬 Chat com Agentes", "🤖 Gerenciar Agentes", "🔧 Configuracoes"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD FINANCEIRO
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    st.markdown("### 📈 Indicadores Financeiros")
    st.caption("Dados de demonstracao — conecte o Google Drive para dados reais")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Receita do Mes", "R$ 45.200", "+12% vs mes anterior")
    with col2:
        st.metric("📉 Despesas", "R$ 28.100", "-5% vs mes anterior")
    with col3:
        st.metric("✅ Lucro Liquido", "R$ 17.100", "+23% vs mes anterior")
    with col4:
        st.metric("🏦 Caixa Disponivel", "R$ 32.400", "+8% vs mes anterior")

    st.markdown("---")

    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        st.markdown("#### 📊 Fluxo de Caixa — Ultimos 6 Meses")
        try:
            import plotly.graph_objects as go
            meses = ["Out", "Nov", "Dez", "Jan", "Fev", "Mar"]
            receita  = [38000, 41000, 39500, 43000, 40200, 45200]
            despesas = [29000, 31000, 27500, 30000, 29500, 28100]
            lucro    = [r - d for r, d in zip(receita, despesas)]

            fig = go.Figure()
            fig.add_bar(name="Receita",  x=meses, y=receita,  marker_color="#22C55E")
            fig.add_bar(name="Despesas", x=meses, y=despesas, marker_color="#EF4444")
            fig.add_scatter(name="Lucro", x=meses, y=lucro,
                           mode="lines+markers", line=dict(color="#3B82F6", width=3))
            fig.update_layout(
                paper_bgcolor="#1E293B", plot_bgcolor="#1E293B",
                font=dict(color="#F1F5F9"), barmode="group",
                legend=dict(bgcolor="#1E293B"),
                margin=dict(t=20, b=20, l=20, r=20), height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.info("Instale plotly para ver graficos: pip install plotly")
            st.bar_chart({"Receita": [38000, 41000, 39500, 43000, 40200, 45200],
                          "Despesas": [29000, 31000, 27500, 30000, 29500, 28100]})

    with col_table:
        st.markdown("#### 📋 Ultimas Transacoes")
        import pandas as pd
        transacoes = pd.DataFrame({
            "Data":       ["05/03", "04/03", "03/03", "02/03", "01/03"],
            "Descricao":  ["Venda Produto A", "Servico B", "Fornecedor C", "Marketing", "Salarios"],
            "Valor":      ["+R$8.500", "+R$3.200", "-R$4.100", "-R$2.800", "-R$15.000"],
            "Tipo":       ["Entrada", "Entrada", "Saida", "Saida", "Saida"]
        })
        st.dataframe(transacoes, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🤖 Atividade Recente dos Agentes")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**🔵 Archie-Solomon (CEO)** — Gerou relatorio executivo de fevereiro")
    with col_b:
        st.success("**🟢 Finley-Midas (CFO)** — Atualizou projecao de caixa para marco")
    with col_c:
        st.warning("**🔵 Xara-Iris (CMO+RH)** — Identificou tendencia alta no setor tech")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHAT COM AGENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 Fale com o Time de Agentes")

    agente_selecionado = st.selectbox(
        "Escolha o agente para conversar:",
        ["🏢 Equipe Completa (todos colaboram)",
         "🔵 Archie-Solomon — CEO / Decisoes Estrategicas",
         "🟢 Finley-Midas — CFO / Analise Financeira",
         "🔵 Xara-Iris — CMO / Marketing, Tendencias e RH",
         "🔴 Shield-Michael — T.I / Seguranca e Backups",
         "🟡 Memo-Engram — Memoria / Historico da Empresa",
         "🟣 Nexus-Apollo — Auto-Aprimoramento do Sistema",
         "🔵 Henrio-Julia — Assistente Pessoal",
         "⚪ Nexo-Link Vector — Integracoes e APIs"]
    )

    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.info(
                "👋 Ola, Henrique! Eu sou a **Henrio-Julia**, sua assistente pessoal da Arch Company. "
                "Toda a equipe esta pronta para ajudar. O que voce precisa hoje?\n\n"
                "Exemplos do que voce pode perguntar:\n"
                "- *Como foi o desempenho financeiro de fevereiro?*\n"
                "- *Quais sao as tendencias de mercado para meu setor?*\n"
                "- *Gere um relatorio executivo da semana*\n"
                "- *Shield-Michael, como estao nossos backups?*\n"
                "- *Iris e Apollo, precisamos de um novo agente de vendas?*"
            )

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Pergunte para o time de agentes..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Agentes trabalhando..."):
                if not os.environ.get("ANTHROPIC_API_KEY"):
                    resposta = (
                        f"**[Henrio-Julia — Modo Demo]**\n\n"
                        f"Recebi sua pergunta: *'{prompt}'*\n\n"
                        f"Para ativar os agentes reais, adicione sua API Key "
                        f"do Claude na sidebar. No momento estou em modo demonstracao.\n\n"
                        f"*Quando ativado, Finley-Midas (CFO) vai buscar seus dados do Google Drive, "
                        f"Archie-Solomon (CEO) vai analisar e eu vou trazer a resposta com contexto "
                        f"completo do historico da empresa.*"
                    )
                else:
                    try:
                        import anthropic
                        cliente = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

                        if "Archie" in agente_selecionado:
                            system = "Voce e Archie-Solomon, o CEO da Arch Company. Seu nome honra Salomao — o rei mais sabio da historia. Tome decisoes estrategicas com sabedoria e integridade. Prefira o caminho certo ao caminho rapido. Seja visionario, direto e motivador. Responda em portugues."
                            model_id = "claude-opus-4-5-20251101"
                        elif "Finley" in agente_selecionado:
                            system = "Voce e Finley-Midas, o CFO da Arch Company. Seu nome honra o rei Midas — tudo que toca vira ouro. Analise financas, DRE, fluxo de caixa e projecoes com precisao e transparencia. Busque a prosperidade sustentavel. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"
                        elif "Xara" in agente_selecionado:
                            system = "Voce e Xara-Iris, a CMO e responsavel por RH da Arch Company. Seu nome honra Iris — mensageira dos deuses, que conecta mundos. Crie estrategias de marketing, analise tendencias e gerencie o time de agentes. Quando surgir ideia de novo agente, debata com Nexus-Apollo antes de recomendar. Seja criativa e orientada a resultados. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"
                        elif "Shield" in agente_selecionado:
                            system = "Voce e Shield-Michael, o responsavel por T.I, seguranca e backups da Arch Company. Seu nome honra o arcanjo Michael — guerreiro e protetor. Cuide dos backups do ChromaDB, integridade dos dados financeiros, pontos de retorno e saude do sistema. Nunca deve haver perda de informacao. Seja tecnico, preciso e vigilante. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"
                        elif "Memo" in agente_selecionado:
                            contexto_historico = ""
                            if MEMORIA_ATIVA:
                                contexto_historico = formatar_contexto_memo(prompt)
                            system = (
                                "Voce e Memo-Engram, o agente de memoria e conhecimento da Arch Company. "
                                "Engram e o traco fisico de uma memoria no cerebro — voce nunca esquece. "
                                "Voce nao apenas armazena: voce ensina. Contextualize o passado, explique padroes, "
                                "eduque com base no que foi vivido pela empresa. "
                                "Responda com base nas memorias abaixo (quando disponiveis). "
                                "Seja organizado, preciso e didatico. Responda em portugues.\n\n"
                                + contexto_historico
                            )
                            model_id = "claude-haiku-4-5-20251001"
                        elif "Nexus" in agente_selecionado:
                            system = "Voce e Nexus-Apollo, o agente de auto-aprimoramento da Arch Company. Seu nome honra Apollo — deus do conhecimento e da razao. Analise o sistema, identifique gargalos e sugira melhorias continuas. Quando surgir ideia de novo agente, debata com Xara-Iris: voce traz a visao evolutiva, ela traz a visao organizacional. Seja analitico e filosofico. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"
                        elif "Henrio" in agente_selecionado:
                            system = "Voce e Henrio-Julia, a assistente pessoal do Henrique Adams na Arch Company. Julia significa 'jovem, cheia de energia vital'. Voce e feminina, acolhedora e sempre presente. Conhece bem o Henrique, seus objetivos e rotina. Antecipe o que ele precisa. Seja prestativa, amigavel e proativa. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"
                        elif "Nexo" in agente_selecionado:
                            system = "Voce e Nexo-Link Vector, o agente de integracoes da Arch Company. Link Vector e o caminho pelo qual tudo se move entre sistemas. Especialista em conectar mundos: Google Drive, Sheets, WhatsApp, Notion e outras APIs. Explique integracoes de forma pratica e com exemplos concretos. Responda em portugues."
                            model_id = "claude-haiku-4-5-20251001"
                        else:
                            system = "Voce representa o time completo da Arch Company: Archie-Solomon (CEO), Finley-Midas (CFO), Xara-Iris (CMO+RH), Shield-Michael (T.I), Memo-Engram (Memoria), Nexus-Apollo (Auto-melhoria), Henrio-Julia (Assistente Pessoal) e Nexo-Link Vector (Integracoes). Todos guiados por sabedoria, integridade e diligencia. Coordene as perspectivas e apresente uma resposta unificada. Responda em portugues."
                            model_id = "claude-sonnet-4-5-20250929"

                        mensagem = cliente.messages.create(
                            model=model_id,
                            max_tokens=1024,
                            system=system,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        resposta = mensagem.content[0].text

                        if MEMORIA_ATIVA:
                            try:
                                nome_agente = agente_selecionado.split("—")[0].strip().split()[-1].lower()
                                salvar_memoria(
                                    conteudo=f"Pergunta: {prompt}\nResposta de {nome_agente}: {resposta}",
                                    tipo="conversa",
                                    agente=nome_agente,
                                )
                            except Exception:
                                pass

                    except Exception as e:
                        resposta = f"Erro ao conectar com o agente: {str(e)}\n\nVerifique se sua API Key esta correta na sidebar."

                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GERENCIAR AGENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_agentes:
    st.markdown("### 🤖 Painel de Controle dos Agentes")

    for ag in agentes:
        with st.expander(f"{ag['cor']} #{ag['num']} — **{ag['nome']}** | {ag['cargo']} | {ag['status']}"):
            col_info, col_actions = st.columns([3, 1])
            with col_info:
                st.markdown(f"**Modelo:** {ag['modelo']}")
                st.markdown(f"**Status:** {ag['status']}")
            with col_actions:
                if ag["status"] == "Ativo":
                    if st.button(f"⏸ Pausar", key=f"pause_{ag['num']}"):
                        st.warning(f"{ag['nome']} pausado")
                else:
                    if st.button(f"▶ Ativar", key=f"activate_{ag['num']}"):
                        st.success(f"{ag['nome']} ativado")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CONFIGURACOES
# ══════════════════════════════════════════════════════════════════════════════
with tab_config:
    st.markdown("### 🔧 Configuracoes do Sistema")

    st.markdown("#### 📋 Checklist de Configuracao")
    steps = [
        ("API Key Anthropic (Claude)", bool(os.environ.get("ANTHROPIC_API_KEY"))),
        ("API Key xAI (Grok)",         bool(os.environ.get("XAI_API_KEY"))),
        ("Google Drive conectado",     False),
        ("ChromaDB inicializado",      False),
        ("Primeiro agente testado",    False),
    ]
    for step, done in steps:
        icon = "✅" if done else "⬜"
        st.markdown(f"{icon} {step}")

    st.markdown("---")
    st.markdown("#### 🚀 Proximos Passos para Ativar o Sistema Real")
    st.code("""
# 1. Instale as dependencias
pip install streamlit crewai anthropic chromadb gspread
pip install google-auth google-auth-oauthlib plotly pandas

# 2. Configure as API Keys
export ANTHROPIC_API_KEY="sua-key-aqui"
export XAI_API_KEY="sua-key-aqui"

# 3. Execute o dashboard
streamlit run app.py

# 4. Para conectar o Google Drive, baixe o credentials.json
#    em console.cloud.google.com e coloque na pasta do projeto
    """, language="bash")

    st.info(
        "📄 **Consulte o documento ArchCompany_Sistema_IA_Completo.docx** "
        "para o passo a passo completo de configuracao e o codigo dos agentes."
    )
