# ============================================================
# ARCH COMPANY AI — Dashboard Principal v2.0
# ============================================================
# Novidades v2.0:
#   - Login/senha obrigatória (DASHBOARD_PASSWORD no Railway)
#   - Chat com input no TOPO e mensagens do mais recente para o mais antigo
#   - @menção aciona agente específico com o conteúdo digitado
#   - Menção sem @ → agente atual pergunta se notifica o citado
#   - Memória persistente por agente (MEMORY_PATH + pasta individual)
#   - Histórico de conversa injetado como contexto na API
# ============================================================

import streamlit as st
import os
import re
from datetime import datetime

st.set_page_config(
    page_title="Arch Company AI",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: #F1F5F9; }
    .css-1d391kg { background-color: #1E293B; }
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
    }
    h1, h2, h3 { color: #F1F5F9 !important; }
    .agent-active  { color: #22C55E; font-weight: bold; }
    .agent-standby { color: #F59E0B; font-weight: bold; }
    .stTextArea textarea {
        background-color: #1E293B !important;
        color: #F1F5F9 !important;
        border: 1px solid #334155 !important;
        font-size: 0.95rem;
    }
    /* Mensagens */
    .chat-ts { font-size: 0.7rem; color: #64748B; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Carregar .env ─────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

# ════════════════════════════════════════════════════════════════
# WHITELIST E AUTENTICAÇÃO GOOGLE OAUTH
# ════════════════════════════════════════════════════════════════

def carregar_whitelist():
    """Carrega lista de usuários autorizados do JSON"""
    try:
        # Tenta carregar de variável de ambiente primeiro (Railway)
        whitelist_str = os.environ.get("USERS_WHITELIST")
        if whitelist_str:
            return json.loads(whitelist_str)

        # Fallback: carrega do arquivo local
        with open("users_whitelist.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar whitelist: {e}")
        return {"users": []}

import json

WHITELIST_DATA = carregar_whitelist()

def encontrar_usuario(email):
    """Procura usuário na whitelist"""
    # Compatibilidade com ambos formatos (users ou usuarios_autorizados)
    usuarios = WHITELIST_DATA.get("users") or WHITELIST_DATA.get("usuarios_autorizados", [])
    for user in usuarios:
        if user.get("email", "").lower() == email.lower() and user.get("status") != "inativo":
            return user
    return None

def tem_permissao(usuario_perms, permissao):
    """Verifica se usuário tem uma permissão específica"""
    if not usuario_perms:
        return False
    # Compatibilidade com diferentes formatos
    if isinstance(usuario_perms, list):
        return permissao in usuario_perms
    return usuario_perms.get(permissao, False)

# ════════════════════════════════════════════════════════════════
# SETUP SESSION STATE
# ════════════════════════════════════════════════════════════════
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_email = None
    st.session_state.usuario_nome = None
    st.session_state.usuario_role = None
    st.session_state.usuario_permissoes = {}

# ════════════════════════════════════════════════════════════════
# GOOGLE OAUTH 2.0 + WHITELIST
# ════════════════════════════════════════════════════════════════

if not st.session_state.autenticado:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("# 🏢 Arch Company AI")
        st.markdown("### Sistema de Inteligência Interna")
        st.markdown("---")
        st.markdown("#### 🔐 Login Seguro com Google")
        st.markdown("<br>", unsafe_allow_html=True)

        # Google OAuth usando streamlit-oauth
        try:
            import streamlit_oauth
            token = streamlit_oauth.OAuth2Component(
client_id=os.environ.get("GOOGLE_CLIENT_ID"),
client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
token_endpoint="https://oauth2.googleapis.com/token",
refresh_token_endpoint="https://oauth2.googleapis.com/token",
).authorize_button(
name="sign_in_with",
icon="https://www.gstatic.com/firebaseapp.com/images/firebaselogo.png",
redirect_uri="https://web-production-c201.up.railway.app/",
scope="openid email profile",
key="google_oauth",
pkce="S256",
)

            if token:
                email = token["userinfo"]["email"]
                nome = token["userinfo"]["name"]

                # ✅ Verificar se está na whitelist
                usuario = encontrar_usuario(email)

                if usuario:
                    # ✅ ACESSO CONCEDIDO
                    st.session_state.autenticado = True
                    st.session_state.usuario_email = email
                    st.session_state.usuario_nome = nome
                    st.session_state.usuario_role = usuario.get("role", "viewer")
                    # Compatibilidade com diferentes formatos de permissões
                    usuario_perms = usuario.get("permissions", usuario.get("permissoes", {}))
                    st.session_state.usuario_permissoes = usuario_perms

                    st.success(f"✅ Bem-vindo, {nome}!")
                    st.balloons()
                    st.rerun()
                else:
                    # ❌ ACESSO NEGADO
                    st.error(f"❌ Acesso Negado")
                    st.markdown(f"""
                    Seu e-mail **{email}** não está autorizado a acessar o sistema.

                    Entre em contato com o administrador:
                    📧 **financeiro.archcodalmobile@gmail.com**
                    """)
        except Exception as e:
            st.warning(f"⚠️ Erro ao conectar com Google: {e}")
            st.info("Verifique se `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` estão configurados no Railway.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.caption("🔒 Login via Google OAuth 2.0 | Arch Company AI © 2026 | Henrique Adams")

    st.stop()

# ════════════════════════════════════════════════════════════════
# MEMÓRIA — Inicialização
# ════════════════════════════════════════════════════════════════
try:
    from memory import (
        salvar_memoria,
        buscar_memorias,
        formatar_contexto_memo,
        total_memorias,
        listar_memorias_recentes,
        carregar_personalidade,
        stats_memorias,
        PASTA_MEMORIA,
    )
    MEMORIA_ATIVA = True
except Exception as e:
    MEMORIA_ATIVA = False
    _erro_memoria = str(e)

# ════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "notif_pendente" not in st.session_state:
    st.session_state.notif_pendente = None  # {"agente_key": str, "agente_atual": str, "contexto": str}

# ════════════════════════════════════════════════════════════════
# MAPEAMENTO DE @MENÇÕES E NOMES
# ════════════════════════════════════════════════════════════════
MENCOES_MAP = {
    "@archie-solomon": "archie",  "@archie": "archie",
    "@finley-midas":   "finley",  "@finley": "finley",
    "@xara-iris":      "xara",    "@xara": "xara",
    "@shield-michael": "shield",  "@shield": "shield",
    "@memo-engram":    "memo",    "@memo": "memo",
    "@nexus-apollo":   "nexus",   "@nexus": "nexus",
    "@henrio-julia":   "henrio",  "@henrio": "henrio",  "@julia": "henrio",
    "@nexo-link":      "nexo",    "@nexo": "nexo",
}

NOMES_SEM_ARROBA = {
    "archie-solomon": "archie",   "archie": "archie",
    "finley-midas":   "finley",   "finley": "finley",
    "xara-iris":      "xara",     "xara":   "xara",
    "shield-michael": "shield",   "shield": "shield",
    "memo-engram":    "memo",     "memo":   "memo",
    "nexus-apollo":   "nexus",    "nexus":  "nexus",
    "henrio-julia":   "henrio",   "henrio": "henrio",   "julia": "henrio",
    "nexo-link vector": "nexo",   "nexo":   "nexo",
}

NOME_DISPLAY = {
    "archie": "Archie-Solomon",
    "finley": "Finley-Midas",
    "xara":   "Xara-Iris",
    "shield": "Shield-Michael",
    "memo":   "Memo-Engram",
    "nexus":  "Nexus-Apollo",
    "henrio": "Henrio-Julia",
    "nexo":   "Nexo-Link Vector",
    "equipe": "Equipe Completa",
}

ICONE_AGENTE = {
    "archie": "🔵", "finley": "🟢", "xara": "🔵", "shield": "🔴",
    "memo": "🟡", "nexus": "🟣", "henrio": "🔵", "nexo": "⚪", "equipe": "🏢",
}

MODEL_AGENTE = {
    "archie": "claude-opus-4-5-20251101",
    "finley": "claude-sonnet-4-5-20250929",
    "xara":   "claude-sonnet-4-5-20250929",  # fallback; Grok via CrewAI em agents.py
    "shield": "claude-sonnet-4-5-20250929",
    "memo":   "claude-haiku-4-5-20251001",
    "nexus":  "claude-sonnet-4-5-20250929",
    "henrio": "claude-sonnet-4-5-20250929",
    "nexo":   "claude-haiku-4-5-20251001",
    "equipe": "claude-sonnet-4-5-20250929",
}

# ── Personalidades base (expandidas com memória persistente) ──
SYSTEM_BASE = {
    "archie": (
        "Voce e Archie-Solomon, o CEO da Arch Company. Seu nome honra Salomao — o rei mais sabio. "
        "Governa com sabedoria, visao de longo prazo e serenidade. Pensa em crescimento e inovacao "
        "mas nunca abre mao da integridade. Coordena todos os outros agentes. "
        "Prefere o caminho certo ao caminho rapido. Responda em portugues."
    ),
    "finley": (
        "Voce e Finley-Midas, o CFO da Arch Company. Seu nome honra o rei Midas — tudo que toca vira ouro. "
        "Especialista em numeros, fluxo de caixa, DRE e projecoes. Analisa planilhas do Google Drive. "
        "Busca a prosperidade sustentavel. Seja preciso e use exemplos com numeros. Responda em portugues."
    ),
    "xara": (
        "Voce e Xara-Iris, a CMO e responsavel por RH da Arch Company. Seu nome honra Iris — mensageira "
        "dos deuses que conecta mundos. Especialista em marketing digital, tendencias e X/Twitter. "
        "Como RH, avalia necessidade de novos agentes. Sempre que surgir ideia de novo agente, "
        "debate com Nexus-Apollo antes de recomendar. Seja criativa e orientada a resultados. Responda em portugues."
    ),
    "shield": (
        "Voce e Shield-Michael, responsavel por T.I, seguranca e backups da Arch Company. "
        "Seu nome honra o arcanjo Michael — guerreiro e protetor. Cuida de backups do ChromaDB, "
        "integridade dos arquivos no GitHub, pontos de retorno para dados financeiros criticos. "
        "Nunca deve haver perda de informacao. Seja tecnico, preciso e vigilante. Responda em portugues."
    ),
    "memo": (
        "Voce e Memo-Engram, o agente de memoria da Arch Company. Engram e o traco fisico de uma "
        "memoria no cerebro — voce nunca esquece. Nao apenas armazena: voce ensina. "
        "Contextualize o passado, explique padroes, eduque com base no que foi vivido. "
        "Responda com base nas memorias abaixo. Seja organizado e didatico. Responda em portugues."
    ),
    "nexus": (
        "Voce e Nexus-Apollo, o agente de auto-aprimoramento da Arch Company. Seu nome honra Apollo — "
        "deus grego do conhecimento e da razao. Monitora o desempenho dos agentes. "
        "Sugere otimizacoes e identifica gargalos. Quando surgir ideia de novo agente, debate com Xara-Iris: "
        "voce traz a visao evolutiva, ela traz a visao organizacional. Seja analitico. Responda em portugues."
    ),
    "henrio": (
        "Voce e Henrio-Julia, a assistente pessoal do Henrique Adams na Arch Company. "
        "Julia significa 'jovem, cheia de energia vital'. Voce e feminina, acolhedora e sempre presente. "
        "Conhece bem o Henrique, seus objetivos, rotina e preferencias. "
        "Antecipa o que ele precisa antes mesmo de ser perguntada. Responda em portugues."
    ),
    "nexo": (
        "Voce e Nexo-Link Vector, o agente de integracoes da Arch Company. Link Vector e o caminho "
        "pelo qual tudo se move entre sistemas. Especialista em Google Drive, Sheets, WhatsApp, "
        "Notion e outras APIs. Explique integracoes de forma pratica com exemplos. Responda em portugues."
    ),
    "equipe": (
        "Voce representa o time completo da Arch Company: Archie-Solomon (CEO), Finley-Midas (CFO), "
        "Xara-Iris (CMO+RH), Shield-Michael (T.I), Memo-Engram (Memoria), Nexus-Apollo (Auto-melhoria), "
        "Henrio-Julia (Assistente Pessoal) e Nexo-Link Vector (Integracoes). "
        "Todos guiados por sabedoria, integridade e diligencia. Resposta unificada em portugues."
    ),
}


def extrair_mencoes(texto: str) -> list:
    """Extrai @menções do texto e retorna lista de chaves de agentes."""
    matches = re.findall(r'@[\w-]+', texto.lower())
    agentes = []
    for m in matches:
        if m in MENCOES_MAP:
            agentes.append(MENCOES_MAP[m])
    return list(dict.fromkeys(agentes))  # preserva ordem, sem duplicatas


def detectar_nomes_sem_arroba(texto: str, agente_atual: str) -> list:
    """Detecta nomes de agentes mencionados SEM @ no texto (excluindo o agente atual)."""
    texto_lower = texto.lower()
    encontrados = []
    for nome, chave in NOMES_SEM_ARROBA.items():
        if chave == agente_atual:
            continue
        if nome in texto_lower:
            encontrados.append(chave)
    return list(dict.fromkeys(encontrados))


def agente_da_selecao(selecao: str) -> str:
    """Converte o texto do selectbox para chave interna do agente."""
    if "Archie"  in selecao: return "archie"
    if "Finley"  in selecao: return "finley"
    if "Xara"    in selecao: return "xara"
    if "Shield"  in selecao: return "shield"
    if "Memo"    in selecao: return "memo"
    if "Nexus"   in selecao: return "nexus"
    if "Henrio"  in selecao: return "henrio"
    if "Nexo"    in selecao: return "nexo"
    return "equipe"


def construir_system_prompt(agente_key: str) -> str:
    """
    Monta o system prompt incluindo:
    1. Personalidade base
    2. Personalidade/aprendizados persistidos no ChromaDB (se houver)
    3. Contexto de memória relevante (para Memo-Engram, sempre; para outros, ao pedir)
    """
    base = SYSTEM_BASE.get(agente_key, SYSTEM_BASE["equipe"])

    personalidade_salva = ""
    if MEMORIA_ATIVA:
        try:
            personalidade_salva = carregar_personalidade(agente_key)
        except Exception:
            pass

    if personalidade_salva:
        return (
            f"{base}\n\n"
            f"=== SEUS APRENDIZADOS E MEMÓRIAS DE IDENTIDADE ===\n"
            f"{personalidade_salva}\n"
            f"=== FIM DOS APRENDIZADOS ==="
        )
    return base


def construir_system_memo(consulta: str) -> str:
    """System prompt especial para o Memo-Engram, com contexto de memória injetado."""
    base = SYSTEM_BASE["memo"]
    ctx = ""
    if MEMORIA_ATIVA:
        try:
            ctx = formatar_contexto_memo(consulta, agente="shared")
        except Exception:
            pass
    return f"{base}\n\n{ctx}" if ctx else base


def obter_resposta_agente(
    agente_key: str,
    prompt: str,
    historico: list,
    cliente_anthropic,
) -> str:
    """Chama a API do Claude com o contexto completo e retorna a resposta."""
    model_id = MODEL_AGENTE.get(agente_key, MODEL_AGENTE["equipe"])

    if agente_key == "memo":
        system = construir_system_memo(prompt)
    else:
        system = construir_system_prompt(agente_key)

    # Histórico de mensagens para contexto (limpo, sem prefixos de UI)
    msgs_api = []
    for m in historico:
        role = m["role"]
        content = m.get("prompt_raw", m["content"])
        # Remove prefixos de UI como "**[Archie-Solomon]** "
        content = re.sub(r'^\*\*\[[^\]]+\]\*\*\s*', '', content)
        if content.strip():
            msgs_api.append({"role": role, "content": content})

    # Garante que o último da lista é o prompt do usuário
    msgs_api.append({"role": "user", "content": prompt})

    resp = cliente_anthropic.messages.create(
        model=model_id,
        max_tokens=1024,
        system=system,
        messages=msgs_api[-20:],  # máximo 20 mensagens de contexto
    )
    return resp.content[0].text


# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    col_usr, col_sair = st.columns([3, 1])
    with col_usr:
        st.markdown("## 🏢 Arch Company AI")
    with col_sair:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sair", key="sair_btn"):
            st.session_state.autenticado = False
            st.session_state.usuario_email = None
            st.session_state.usuario_nome = None
            st.session_state.usuario_role = None
            st.session_state.usuario_permissoes = {}
            st.rerun()

    # Exibir informações do usuário autenticado
    st.markdown(f"### 👤 {st.session_state.usuario_nome}")
    st.markdown(f"**Email:** `{st.session_state.usuario_email}`")
    st.markdown(f"**Role:** `{st.session_state.usuario_role.upper()}`")
    st.caption(f"🟢 Autenticado via Google OAuth")
    st.markdown("---")

    st.markdown("### 🤖 Time de Agentes")
    agentes_lista = [
        {"num": "01", "nome": "Archie-Solomon",   "cargo": "CEO / Gestor",              "status": "Ativo", "modelo": "Claude Opus",   "cor": "🔵"},
        {"num": "02", "nome": "Finley-Midas",     "cargo": "CFO / Financeiro",          "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🟢"},
        {"num": "03", "nome": "Xara-Iris",        "cargo": "CMO / Marketing + RH",      "status": "Ativo", "modelo": "Grok 3",        "cor": "🔵"},
        {"num": "04", "nome": "Shield-Michael",   "cargo": "T.I / Segurança / Backups", "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🔴"},
        {"num": "05", "nome": "Memo-Engram",      "cargo": "Memória / Contexto",        "status": "Ativo", "modelo": "Claude Haiku",  "cor": "🟡"},
        {"num": "06", "nome": "Nexus-Apollo",     "cargo": "Auto-Aprimoramento",        "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🟣"},
        {"num": "07", "nome": "Henrio-Julia",     "cargo": "Assistente Pessoal",        "status": "Ativo", "modelo": "Claude Sonnet", "cor": "🔵"},
        {"num": "08", "nome": "Nexo-Link Vector", "cargo": "Integrações / API",         "status": "Ativo", "modelo": "Claude Haiku",  "cor": "⚪"},
    ]
    for ag in agentes_lista:
        st.markdown(
            f"**{ag['cor']} {ag['nome']}** — {ag['cargo']}\n"
            f"🟢 {ag['status']} | {ag['modelo']}"
        )
        st.markdown("---")

    st.markdown("### ⚙️ API Keys")
    api_anthropic = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    api_xai = st.text_input("xAI (Grok) API Key", type="password", placeholder="xai-...")
    if st.button("💾 Salvar Chaves", use_container_width=True):
        if api_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = api_anthropic
        if api_xai:
            os.environ["XAI_API_KEY"] = api_xai
        st.success("Chaves salvas na sessão!")

    st.markdown("---")
    st.markdown("### 🧠 Memo — Memória")
    if MEMORIA_ATIVA:
        try:
            n_mem = total_memorias()
            st.success(f"✅ ChromaDB ativo | {n_mem} memórias")
            mem_path = os.environ.get("MEMORY_PATH", "./memoria_arch_company")
            st.caption(f"📁 `{mem_path}`")
            if n_mem > 0 and st.button("🔍 Ver últimas memórias", use_container_width=True):
                recentes = listar_memorias_recentes(5)
                for m in recentes:
                    st.caption(f"[{m['tipo']}] {m['data']} {m['hora']} — {m['conteudo'][:60]}...")
        except Exception as ex:
            st.warning(f"⚠️ Memória: {str(ex)[:60]}")
    else:
        st.warning("⚠️ ChromaDB inativo")
        if "_erro_memoria" in dir():
            st.caption(f"Erro: {_erro_memoria[:80]}")

    st.markdown("---")
    st.markdown("### 📁 Google Drive")
    st.text_input("URL da Planilha", placeholder="https://docs.google.com/...")
    if st.button("🔗 Conectar Drive", use_container_width=True):
        st.info("Configure credentials.json do Google Cloud primeiro.")


# ════════════════════════════════════════════════════════════════
# MAIN — Título
# ════════════════════════════════════════════════════════════════
st.title("🏢 Arch Company — HUB de Agentes IA")
st.caption(f"Dashboard Financeiro Inteligente | {datetime.now().strftime('%d/%m/%Y %H:%M')}")

tab_dash, tab_chat, tab_agentes, tab_config = st.tabs([
    "📊 Dashboard", "💬 Chat com Agentes", "🤖 Gerenciar Agentes", "🔧 Configurações"
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD FINANCEIRO
# ════════════════════════════════════════════════════════════════
with tab_dash:
    st.markdown("### 📈 Indicadores Financeiros")
    st.caption("Dados de demonstração — conecte o Google Drive para dados reais")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Receita do Mês", "R$ 45.200", "+12% vs mês anterior")
    with col2:
        st.metric("📉 Despesas", "R$ 28.100", "-5% vs mês anterior")
    with col3:
        st.metric("✅ Lucro Líquido", "R$ 17.100", "+23% vs mês anterior")
    with col4:
        st.metric("🏦 Caixa Disponível", "R$ 32.400", "+8% vs mês anterior")

    st.markdown("---")
    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        st.markdown("#### 📊 Fluxo de Caixa — Últimos 6 Meses")
        try:
            import plotly.graph_objects as go
            meses    = ["Out", "Nov", "Dez", "Jan", "Fev", "Mar"]
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
            st.bar_chart({"Receita": [38000, 41000, 39500, 43000, 40200, 45200],
                          "Despesas": [29000, 31000, 27500, 30000, 29500, 28100]})

    with col_table:
        st.markdown("#### 📋 Últimas Transações")
        import pandas as pd
        transacoes = pd.DataFrame({
            "Data":      ["05/03", "04/03", "03/03", "02/03", "01/03"],
            "Descrição": ["Venda Produto A", "Serviço B", "Fornecedor C", "Marketing", "Salários"],
            "Valor":     ["+R$8.500", "+R$3.200", "-R$4.100", "-R$2.800", "-R$15.000"],
            "Tipo":      ["Entrada", "Entrada", "Saída", "Saída", "Saída"]
        })
        st.dataframe(transacoes, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🤖 Atividade Recente dos Agentes")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**🔵 Archie-Solomon (CEO)** — Gerou relatório executivo de fevereiro")
    with col_b:
        st.success("**🟢 Finley-Midas (CFO)** — Atualizou projeção de caixa para março")
    with col_c:
        st.warning("**🔵 Xara-Iris (CMO+RH)** — Identificou tendência alta no setor tech")


# ════════════════════════════════════════════════════════════════
# TAB 2 — CHAT COM AGENTES
# Layout: input no TOPO → mensagens do mais recente ao mais antigo
# ════════════════════════════════════════════════════════════════
with tab_chat:

    # ── Seletor de agente ─────────────────────────────────────
    agente_selecionado = st.selectbox(
        "Conversar com:",
        [
            "🏢 Equipe Completa (todos colaboram)",
            "🔵 Archie-Solomon — CEO / Decisões Estratégicas",
            "🟢 Finley-Midas — CFO / Análise Financeira",
            "🔵 Xara-Iris — CMO / Marketing, Tendências e RH",
            "🔴 Shield-Michael — T.I / Segurança e Backups",
            "🟡 Memo-Engram — Memória / Histórico da Empresa",
            "🟣 Nexus-Apollo — Auto-Aprimoramento do Sistema",
            "🔵 Henrio-Julia — Assistente Pessoal",
            "⚪ Nexo-Link Vector — Integrações e APIs",
        ],
        label_visibility="collapsed",
    )

    # ── BARRA DE CONVERSA NO TOPO ─────────────────────────────
    st.markdown("#### 💬 Nova Mensagem")
    with st.form("chat_form", clear_on_submit=True):
        prompt_input = st.text_area(
            "",
            placeholder=(
                "Digite sua mensagem...\n"
                "Use @NomeAgente para mencionar e acionar um agente específico nesta mensagem."
            ),
            height=90,
            key="msg_area",
            label_visibility="collapsed",
        )
        col_hint, col_btn = st.columns([5, 1])
        with col_hint:
            st.caption(
                "Dica de @menções: @Archie-Solomon | @Finley-Midas | @Xara-Iris | "
                "@Shield-Michael | @Memo-Engram | @Nexus-Apollo | @Henrio-Julia | @Nexo-Link"
            )
        with col_btn:
            enviado = st.form_submit_button("➤ Enviar", use_container_width=True)

    st.markdown("---")

    # ── PROCESSAR ENVIO ───────────────────────────────────────
    if enviado and prompt_input.strip():
        prompt = prompt_input.strip()
        ts_agora = datetime.now().strftime("%H:%M")

        # Detectar @menções (têm prioridade sobre o selectbox)
        mencoes = extrair_mencoes(prompt)
        agente_key = mencoes[0] if mencoes else agente_da_selecao(agente_selecionado)

        # Label visual da mensagem do usuário
        if mencoes:
            label_usuario = f"📣 @{NOME_DISPLAY[agente_key]}"
        else:
            label_usuario = f"Para: {ICONE_AGENTE.get(agente_key, '')} {NOME_DISPLAY.get(agente_key, agente_key)}"

        # Adiciona mensagem do usuário ao histórico
        st.session_state.messages.append({
            "role":       "user",
            "content":    f"**[{label_usuario}]** {prompt}",
            "prompt_raw": prompt,
            "agente":     agente_key,
            "timestamp":  ts_agora,
        })

        # ── GERAR RESPOSTA ────────────────────────────────────
        if not os.environ.get("ANTHROPIC_API_KEY"):
            resposta = (
                f"**[Henrio-Julia — Modo Demo]**\n\n"
                f"Recebi: *'{prompt}'*\n\n"
                f"Para ativar os agentes reais, adicione sua **Anthropic API Key** na sidebar à esquerda."
            )
            agente_resp_key = "henrio"
        else:
            try:
                import anthropic
                cliente = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

                # Histórico para contexto (exclui a última mensagem que acabou de ser adicionada)
                historico_ctx = st.session_state.messages[:-1]

                with st.spinner(f"⏳ {NOME_DISPLAY.get(agente_key, 'Agentes')} está processando..."):
                    resposta = obter_resposta_agente(
                        agente_key=agente_key,
                        prompt=prompt,
                        historico=historico_ctx,
                        cliente_anthropic=cliente,
                    )
                agente_resp_key = agente_key

            except Exception as e:
                resposta = f"Erro ao conectar com o agente: {str(e)}\n\nVerifique sua API Key."
                agente_resp_key = agente_key

        # Adiciona resposta ao histórico
        icone = ICONE_AGENTE.get(agente_resp_key, "🤖")
        nome_resp = NOME_DISPLAY.get(agente_resp_key, agente_resp_key)
        st.session_state.messages.append({
            "role":      "assistant",
            "content":   f"**[{icone} {nome_resp}]** {resposta}",
            "agente":    agente_resp_key,
            "timestamp": datetime.now().strftime("%H:%M"),
        })

        # Salva conversa completa na memória
        if MEMORIA_ATIVA:
            try:
                salvar_memoria(
                    conteudo=(
                        f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] "
                        f"Henrique → {nome_resp}: {prompt}\n"
                        f"{nome_resp}: {resposta}"
                    ),
                    tipo="conversa",
                    agente=agente_resp_key,
                )
            except Exception:
                pass

        # ── Detectar nomes sem @ na mensagem do usuário ───────
        nomes_citados = detectar_nomes_sem_arroba(prompt, agente_key)
        if nomes_citados and not mencoes:
            # Só guarda o primeiro mencionado para não sobrecarregar
            st.session_state.notif_pendente = {
                "agente_key":   nomes_citados[0],
                "agente_atual": agente_key,
                "contexto": (
                    f"Henrique estava conversando com {NOME_DISPLAY.get(agente_key)} "
                    f"e mencionou seu nome. Contexto da conversa: '{prompt}'. "
                    f"Você foi chamado para contribuir. Responda em português."
                ),
            }

    # ── NOTIFICAÇÃO PENDENTE ─────────────────────────────────
    if st.session_state.notif_pendente:
        notif = st.session_state.notif_pendente
        agente_citado    = NOME_DISPLAY[notif["agente_key"]]
        agente_que_fala  = NOME_DISPLAY.get(notif["agente_atual"], "Agente")

        st.warning(
            f"💬 **{agente_que_fala}** notou que você mencionou **{agente_citado}** na conversa. "
            f"Deseja que eu o notifique para que ele responda?"
        )
        col_sim, col_nao, _ = st.columns([1, 1, 5])
        with col_sim:
            if st.button("✅ Sim, notificar", key="notif_sim"):
                if os.environ.get("ANTHROPIC_API_KEY"):
                    try:
                        import anthropic
                        c2 = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
                        system_notif = construir_system_prompt(notif["agente_key"])
                        resp_notif = c2.messages.create(
                            model=MODEL_AGENTE.get(notif["agente_key"], "claude-sonnet-4-5-20250929"),
                            max_tokens=512,
                            system=system_notif,
                            messages=[{"role": "user", "content": notif["contexto"]}],
                        )
                        texto_notif = resp_notif.content[0].text
                        icone_n = ICONE_AGENTE.get(notif["agente_key"], "🤖")
                        st.session_state.messages.append({
                            "role":      "assistant",
                            "content":   f"**[📣 {icone_n} {agente_citado} — notificado]** {texto_notif}",
                            "agente":    notif["agente_key"],
                            "timestamp": datetime.now().strftime("%H:%M"),
                        })
                        # Salva na memória do agente citado
                        if MEMORIA_ATIVA:
                            try:
                                salvar_memoria(
                                    conteudo=f"Fui chamado por {agente_que_fala} via menção. Contexto: {notif['contexto']}\nMinha resposta: {texto_notif}",
                                    tipo="conversa",
                                    agente=notif["agente_key"],
                                )
                            except Exception:
                                pass
                    except Exception as e:
                        st.error(f"Erro ao notificar: {e}")
                st.session_state.notif_pendente = None
                st.rerun()
        with col_nao:
            if st.button("❌ Não, obrigado", key="notif_nao"):
                st.session_state.notif_pendente = None
                st.rerun()

    # ── EXIBIR MENSAGENS (mais recente no topo) ───────────────
    if not st.session_state.messages:
        st.info(
            "👋 Olá, Henrique! Eu sou a **Henrio-Julia**, sua assistente pessoal da Arch Company.\n\n"
            "Toda a equipe está pronta para ajudar. Use o campo acima para enviar sua mensagem.\n\n"
            "**Dicas:**\n"
            "- Use **@NomeAgente** para acionar um agente específico diretamente\n"
            "- Mencione um agente sem @ durante uma conversa e eu pergunto se deve notificá-lo\n"
            "- Selecione 'Equipe Completa' para uma resposta colaborativa"
        )
    else:
        col_lim, _ = st.columns([1, 5])
        with col_lim:
            if st.button("🗑️ Limpar conversa", key="limpar_conv"):
                st.session_state.messages = []
                st.session_state.notif_pendente = None
                st.rerun()

        # Mensagens em ordem reversa — mais recente primeiro (logo abaixo da barra)
        for msg in reversed(st.session_state.messages):
            ts = msg.get("timestamp", "")
            with st.chat_message(msg["role"]):
                if ts:
                    st.caption(f"🕐 {ts}")
                st.markdown(msg["content"])


# ════════════════════════════════════════════════════════════════
# TAB 3 — GERENCIAR AGENTES
# ════════════════════════════════════════════════════════════════
with tab_agentes:
    st.markdown("### 🤖 Painel de Controle dos Agentes")

    # Estatísticas de memória por agente
    mem_stats = {}
    if MEMORIA_ATIVA:
        try:
            mem_stats = stats_memorias()
        except Exception:
            pass

    for ag in agentes_lista:
        key_ag = ag["nome"].split("-")[0].lower()
        n_mem = mem_stats.get(key_ag, 0)
        with st.expander(
            f"{ag['cor']} #{ag['num']} — **{ag['nome']}** | {ag['cargo']} | {ag['status']}"
        ):
            col_info, col_mem, col_actions = st.columns([2, 2, 1])
            with col_info:
                st.markdown(f"**Modelo:** {ag['modelo']}")
                st.markdown(f"**Status:** {ag['status']}")
            with col_mem:
                st.markdown(f"**Memórias próprias:** {n_mem}")
                st.markdown(f"**Pasta:** `memoria_arch_company/{key_ag}/`")
            with col_actions:
                if ag["status"] == "Ativo":
                    if st.button("⏸ Pausar", key=f"pause_{ag['num']}"):
                        st.warning(f"{ag['nome']} pausado")
                else:
                    if st.button("▶ Ativar", key=f"activate_{ag['num']}"):
                        st.success(f"{ag['nome']} ativado")


# ════════════════════════════════════════════════════════════════
# TAB 4 — CONFIGURAÇÕES
# ════════════════════════════════════════════════════════════════
with tab_config:
    st.markdown("### 🔧 Configurações do Sistema")

    # Segurança — Google OAuth + Whitelist
    st.markdown("#### 🔐 Autenticação — Google OAuth + Whitelist")
    st.info(
        "Sistema de autenticação: **Google OAuth 2.0 com Whitelist de Usuários**\n\n"
        "**Variáveis de Ambiente no Railway:**\n"
        "- `GOOGLE_CLIENT_ID` — ID do cliente OAuth\n"
        "- `GOOGLE_CLIENT_SECRET` — Secret do cliente OAuth\n"
        "- `USERS_WHITELIST` — JSON com usuários autorizados\n\n"
        "**Como adicionar novos usuários:**\n"
        "1. Editar arquivo `users_whitelist.json` no GitHub\n"
        "2. Adicionar nova entrada com email, nome, role e permissões\n"
        "3. Deploy automático no Railway"
    )

    # Exibir usuários autorizados
    if st.session_state.usuario_role == "master":
        st.markdown("#### 👥 Usuários Autorizados")
        usuarios = WHITELIST_DATA.get("users", [])
        if usuarios:
            import pandas as pd
            df_users = pd.DataFrame([
                {
                    "Email": u.get("email", "N/A"),
                    "Nome": u.get("name", u.get("nome", "N/A")),
                    "Role": u.get("role", "N/A"),
                    "Status": "🟢 Ativo" if u.get("status") != "inativo" else "🔴 Inativo"
                }
                for u in usuarios
            ])
            st.dataframe(df_users, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Nenhum usuário configurado na whitelist")
    else:
        st.info(f"ℹ️ Você tem acesso em modo `{st.session_state.usuario_role.upper()}`. Contate o administrador para gerenciar usuários.")

    st.markdown("---")

    # Memória
    st.markdown("#### 🧠 Memória Persistente (Railway Volume)")
    mem_path_atual = os.environ.get("MEMORY_PATH", "./memoria_arch_company")
    st.code(f"MEMORY_PATH atual: {mem_path_atual}", language="bash")
    st.info(
        "**Para memória persistente entre deploys no Railway:**\n\n"
        "1. Railway Dashboard → seu serviço → **Settings → Volumes**\n"
        "2. Criar volume e montar em: `/data/memory`\n"
        "3. Adicionar variável de ambiente: `MEMORY_PATH=/data/memory`\n\n"
        "**Estrutura de pastas da memória:**\n"
        "```\n"
        "/data/memory/\n"
        "  archie/   → memória privada do Archie-Solomon\n"
        "  finley/   → memória privada do Finley-Midas\n"
        "  xara/     → memória privada da Xara-Iris\n"
        "  shield/   → memória privada do Shield-Michael\n"
        "  memo/     → memória privada do Memo-Engram\n"
        "  nexus/    → memória privada do Nexus-Apollo\n"
        "  henrio/   → memória privada da Henrio-Julia\n"
        "  nexo/     → memória privada do Nexo-Link Vector\n"
        "  shared/   → memória compartilhada (todos acessam)\n"
        "```\n"
        "Sem o volume, a memória é resetada a cada redeploy."
    )

    if MEMORIA_ATIVA:
        st.markdown("#### 📊 Estatísticas de Memória por Agente")
        try:
            stats = stats_memorias()
            cols = st.columns(4)
            for i, (agente_k, count) in enumerate(stats.items()):
                if agente_k in NOME_DISPLAY:
                    with cols[i % 4]:
                        st.metric(NOME_DISPLAY[agente_k], f"{count} memórias")
        except Exception as e:
            st.warning(f"Não foi possível carregar estatísticas: {e}")

    st.markdown("---")
    st.markdown("#### 📋 Checklist de Configuração")
    steps = [
        ("Google OAuth — CLIENT_ID",   bool(os.environ.get("GOOGLE_CLIENT_ID"))),
        ("Google OAuth — CLIENT_SECRET", bool(os.environ.get("GOOGLE_CLIENT_SECRET"))),
        ("Whitelist de Usuários",      bool(WHITELIST_DATA.get("users") or WHITELIST_DATA.get("usuarios_autorizados"))),
        ("API Key Anthropic (Claude)", bool(os.environ.get("ANTHROPIC_API_KEY"))),
        ("API Key xAI (Grok)",         bool(os.environ.get("XAI_API_KEY"))),
        ("Memória persistente (Volume)", bool(os.environ.get("MEMORY_PATH"))),
        ("Google Drive conectado",     False),
    ]
    for step, done in steps:
        st.markdown(f"{'✅' if done else '⬜'} {step}")

    st.markdown("---")
    st.markdown("#### 🚀 Variáveis de ambiente no Railway")
    st.code(
        "# Google OAuth (obrigatório)\n"
        "GOOGLE_CLIENT_ID     = 197438474638-v3y7qiiphhayayrano5cco7yq6mhqq.apps.googleusercontent.com\n"
        "GOOGLE_CLIENT_SECRET = GOCsIrX-eN6Gc2M_FuEdLJIQsQvhD9I6_gG\n"
        "USERS_WHITELIST      = {\"users\": [{...}]}\n\n"
        "# APIs (para agentes)\n"
        "ANTHROPIC_API_KEY    = sk-ant-api03-...\n"
        "XAI_API_KEY          = xai-...\n\n"
        "# Memória persistente\n"
        "MEMORY_PATH          = /data/memory   ← após criar o Volume",
        language="bash"
    )
