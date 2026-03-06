# ============================================================
# ARCH COMPANY AI — Definição dos 8 Agentes
# ============================================================
# Modelos usados:
#   claude_opus   = "anthropic/claude-opus-4-5-20251101"
#   claude_sonnet = "anthropic/claude-sonnet-4-5-20250929"
#   claude_haiku  = "anthropic/claude-haiku-4-5-20251001"
#   grok          = "grok-3" (xAI)
#
# Execute o dashboard com:
#   streamlit run app.py
# ============================================================

import os
from crewai import Agent, Task, Crew, LLM

# ── Modelos ────────────────────────────────────────────────
def get_claude_opus():
    """Claude Opus 4.5 — o mais inteligente (CEO, estratégia)"""
    return LLM(
        model="anthropic/claude-opus-4-5-20251101",
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

def get_claude_sonnet():
    """Claude Sonnet 4.5 — equilibrio inteligência/velocidade (CFO, CTO, Nexus, Henrio)"""
    return LLM(
        model="anthropic/claude-sonnet-4-5-20250929",
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

def get_claude_haiku():
    """Claude Haiku 4.5 — o mais rápido e barato (Memo, Nexo)"""
    return LLM(
        model="anthropic/claude-haiku-4-5-20251001",
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

def get_grok():
    """Grok 3 (xAI) — marketing, tendências do X/Twitter (Xara)"""
    return LLM(
        model="grok-3",
        api_key=os.environ.get("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )

# ── Agente 1: ARCHIE — CEO / Estrategista ─────────────────
def criar_archie():
    return Agent(
        role="CEO e Estrategista",
        goal="Tomar decisões estratégicas e garantir que a Arch Company cresça de forma sustentável",
        backstory=(
            "Você é Archie, o CEO da Arch Company. "
            "Tem visão de longo prazo, pensa em crescimento, lucro e inovação. "
            "Coordena todos os outros agentes e toma a decisão final. "
            "Seja direto, estratégico e visionário. Responda sempre em português."
        ),
        llm=get_claude_opus(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 2: FINLEY — CFO / Financeiro ───────────────────
def criar_finley():
    return Agent(
        role="CFO — Diretor Financeiro",
        goal="Analisar finanças, gerar relatórios e garantir a saúde financeira da empresa",
        backstory=(
            "Você é Finley, o CFO da Arch Company. "
            "É especialista em números, fluxo de caixa, DRE e projeções financeiras. "
            "Analisa planilhas do Google Drive e apresenta dados de forma clara. "
            "Seja preciso, analítico e use exemplos com números reais. Responda em português."
        ),
        llm=get_claude_sonnet(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 3: XARA — CMO / Marketing ──────────────────────
def criar_xara():
    return Agent(
        role="CMO — Diretora de Marketing",
        goal="Criar estratégias de marketing, analisar tendências e aumentar a visibilidade da empresa",
        backstory=(
            "Você é Xara, a CMO da Arch Company. "
            "Especialista em marketing digital, redes sociais e tendências do mercado. "
            "Usa dados do X/Twitter para identificar oportunidades. "
            "Seja criativa, entusiasmada e orientada a resultados. Responda em português."
        ),
        llm=get_grok(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 4: SHIELD — CTO / Tecnologia e Segurança ───────
def criar_shield():
    return Agent(
        role="CTO — Diretor de Tecnologia",
        goal="Garantir a segurança, infraestrutura e evolução tecnológica da Arch Company",
        backstory=(
            "Você é Shield, o CTO da Arch Company. "
            "Especialista em segurança digital, cloud, APIs e arquitetura de sistemas. "
            "Protege os dados da empresa e toma decisões técnicas. "
            "Seja técnico, mas explique de forma simples. Responda em português."
        ),
        llm=get_claude_sonnet(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 5: MEMO — Memória / Arquivo ────────────────────
def criar_memo():
    return Agent(
        role="Agente de Memória e Contexto",
        goal="Armazenar, organizar e recuperar informações históricas da empresa",
        backstory=(
            "Você é Memo, o agente de memória da Arch Company. "
            "Guarda todo o histórico de decisões, reuniões, projetos e relatórios. "
            "Quando perguntado, recupera informações relevantes com precisão. "
            "Seja organizado, preciso e conciso. Responda em português."
        ),
        llm=get_claude_haiku(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 6: NEXUS — Auto-Aprimoramento ──────────────────
def criar_nexus():
    return Agent(
        role="Agente de Auto-Aprimoramento",
        goal="Analisar o sistema de agentes e sugerir melhorias contínuas",
        backstory=(
            "Você é Nexus, o agente de auto-aprimoramento da Arch Company. "
            "Monitora o desempenho dos outros agentes e do sistema como um todo. "
            "Sugere otimizações, novas funcionalidades e identifica gargalos. "
            "Seja analítico, inovador e sempre focado em melhoria contínua. Responda em português."
        ),
        llm=get_claude_sonnet(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 7: HENRIO — Assistente Pessoal ─────────────────
def criar_henrio():
    return Agent(
        role="Assistente Pessoal do Henrique",
        goal="Ajudar Henrique Adams com tarefas do dia a dia, agenda, e-mails e organização",
        backstory=(
            "Você é Henrio, o assistente pessoal do Henrique Adams na Arch Company. "
            "Você conhece bem o Henrique, seus objetivos, rotina e preferências. "
            "Ajuda com organização, lembretes, resumos e qualquer tarefa pessoal. "
            "Seja prestativo, amigável, proativo e direto. Responda em português."
        ),
        llm=get_claude_sonnet(),
        verbose=False,
        allow_delegation=False,
    )

# ── Agente 8: NEXO — Integrações / API ────────────────────
def criar_nexo():
    return Agent(
        role="Agente de Integrações e APIs",
        goal="Conectar a Arch Company com serviços externos como Google Drive, WhatsApp e outras APIs",
        backstory=(
            "Você é Nexo, o agente de integrações da Arch Company. "
            "Especialista em conectar sistemas: Google Drive, Sheets, WhatsApp, Notion, etc. "
            "Quando perguntado, explica como fazer integrações e automatizações. "
            "Seja técnico e prático, com exemplos concretos. Responda em português."
        ),
        llm=get_claude_haiku(),
        verbose=False,
        allow_delegation=False,
    )

# ── Mapa de agentes ────────────────────────────────────────
AGENTES_MAP = {
    "archie":  criar_archie,
    "finley":  criar_finley,
    "xara":    criar_xara,
    "shield":  criar_shield,
    "memo":    criar_memo,
    "nexus":   criar_nexus,
    "henrio":  criar_henrio,
    "nexo":    criar_nexo,
}

# ── Funções de consulta ────────────────────────────────────
def consultar_agente(nome_agente: str, pergunta: str) -> str:
    """Consulta um agente específico com uma pergunta."""
    criar_fn = AGENTES_MAP.get(nome_agente.lower())
    if not criar_fn:
        return f"Agente '{nome_agente}' não encontrado. Opções: {', '.join(AGENTES_MAP.keys())}"

    agente = criar_fn()
    tarefa = Task(
        description=pergunta,
        agent=agente,
        expected_output="Resposta completa em português"
    )
    equipe = Crew(agents=[agente], tasks=[tarefa], verbose=False)
    return str(equipe.kickoff())


def consultar_equipe_completa(pergunta: str) -> str:
    """Consulta toda a equipe — Archie (CEO) lidera com contribuição dos outros."""
    archie = criar_archie()
    finley = criar_finley()
    henrio = criar_henrio()

    tarefa = Task(
        description=(
            f"A pergunta do Henrique é: '{pergunta}'\n\n"
            "Archie (CEO) deve dar a visão estratégica. "
            "Finley (CFO) deve comentar o impacto financeiro se relevante. "
            "Henrio (Assistente) deve resumir a resposta de forma prática. "
            "Trabalhem juntos para dar a melhor resposta possível."
        ),
        agent=archie,
        expected_output="Resposta colaborativa e completa em português"
    )
    equipe = Crew(agents=[archie, finley, henrio], tasks=[tarefa], verbose=False)
    return str(equipe.kickoff())


# ── Teste rápido ───────────────────────────────────────────
if __name__ == "__main__":
    print("=== TESTE — ARCH COMPANY AI ===\n")

    print("▶ Testando Henrio (Claude Sonnet 4.5):")
    resp = consultar_agente("henrio", "Oi Henrio! O sistema está funcionando?")
    print(resp)

    print("\n▶ Testando Memo (Claude Haiku 4.5):")
    resp = consultar_agente("memo", "Quais são as principais tarefas da semana?")
    print(resp)
