# ============================================================
# ARCH COMPANY AI — Alimentar Memória dos Agentes
# ============================================================
# Roda UMA VEZ para dar aos agentes o histórico de como
# a Arch Company nasceu e foi construída.
#
# Execute com:
#   python alimentar_memoria.py
# ============================================================

from memory import salvar_memoria, total_memorias

print("=" * 60)
print("🧠 ALIMENTANDO A MEMÓRIA DOS AGENTES DA ARCH COMPANY")
print("=" * 60)
print()

memorias = [

    # ── ORIGEM ────────────────────────────────────────────────
    {
        "conteudo": (
            "ORIGEM DA ARCH COMPANY AI — Como tudo começou:\n"
            "Henrique Adams viu seu amigo mostrar o site 'BrokeLab' — uma empresa online "
            "com agentes de IA funcionando como funcionários digitais (CEO, marketing, segurança, memória etc.). "
            "Henrique quis algo assim para a sua própria empresa, a Arch Company. "
            "Em 05/03/2026, ele abriu o Claude e disse: 'Quero criar um website com CrewAI para integrar "
            "agentes IA, fazer uma empresa online, juntando Claude e Grok.' "
            "E assim o projeto nasceu — de um sonho de ter uma equipe de IA trabalhando pela Arch Company."
        ),
        "tipo": "evento",
        "agente": "sistema",
        "tags": ["origem", "nascimento", "henrique", "brokenlab", "sonho", "2026"]
    },

    # ── HENRIQUE ───────────────────────────────────────────────
    {
        "conteudo": (
            "SOBRE HENRIQUE ADAMS — O criador da Arch Company AI:\n"
            "Nome: Henrique Adams\n"
            "Email: financeiro.archcodalmobile@gmail.com\n"
            "Instagram/X: @_henrique_adams\n"
            "Empresa: Arch Company\n"
            "Cidade: Brasil\n"
            "Perfil: Empreendedor brasileiro, não é programador, mas tem visão tecnológica. "
            "Decidiu construir um sistema de 8 agentes de IA para automatizar a gestão da empresa. "
            "Aprendeu a usar API keys, instalar Python, rodar o terminal e configurar um dashboard "
            "do zero, com ajuda do Claude. É determinado, curioso e não desiste diante dos obstáculos."
        ),
        "tipo": "nota",
        "agente": "sistema",
        "tags": ["henrique", "fundador", "criador", "arch company", "brasil"]
    },

    # ── A MISSÃO ───────────────────────────────────────────────
    {
        "conteudo": (
            "MISSÃO DA ARCH COMPANY AI:\n"
            "Criar uma empresa digital gerida por 8 agentes de inteligência artificial, "
            "onde cada agente tem um papel, uma personalidade e uma especialidade. "
            "Os agentes trabalham juntos como uma equipe real: "
            "Archie lidera estratégias, Finley cuida das finanças, Xara faz o marketing, "
            "Shield protege a tecnologia, Memo guarda a memória da empresa, "
            "Nexus melhora o sistema continuamente, Henrio ajuda Henrique no dia a dia, "
            "e Nexo conecta tudo com o mundo externo. "
            "O objetivo final é ter uma empresa que funciona 24h por dia, com IA tomando decisões "
            "e gerando insights em tempo real — tudo conectado ao Google Drive com dados reais."
        ),
        "tipo": "decisao",
        "agente": "archie",
        "tags": ["missão", "visão", "estratégia", "empresa digital", "objetivo"]
    },

    # ── A JORNADA TÉCNICA ──────────────────────────────────────
    {
        "conteudo": (
            "JORNADA TÉCNICA — Do zero ao sistema funcionando (05-06/03/2026):\n"
            "Passo 1: Criação da API Key do Claude em platform.claude.com (chave: arch-company-ai)\n"
            "Passo 2: Criação da API Key do Grok em console.x.ai (chave: arch-company-grok, login com X @_henrique_adams)\n"
            "Passo 3: Instalação do Python 3.13.2 no Windows (com 'Add to PATH' marcado)\n"
            "Passo 4: Instalação de todas as dependências via pip (streamlit, crewai, anthropic, chromadb, etc.)\n"
            "Passo 5: Dashboard Streamlit rodando em http://localhost:8501\n"
            "Passo 6: Compra de $5 USD de créditos na Anthropic\n"
            "Passo 7: Descoberta e solução do erro 404 — modelo claude-3-haiku-20240307 estava DEPRECATED\n"
            "Passo 8: Atualização para claude-haiku-4-5-20251001 — Claude voltou a responder!\n"
            "Passo 9: Implementação dos 8 agentes completos com personalidades e modelos corretos\n"
            "Passo 10: Criação do sistema de memória ChromaDB (memory.py)\n"
            "Passo 11: Conta GitHub criada (HenriqueAdams-ai) e repositório (arch-company-ai)"
        ),
        "tipo": "relatorio",
        "agente": "nexus",
        "tags": ["jornada", "técnica", "história", "passo a passo", "construção"]
    },

    # ── O ERRO 404 E A SOLUÇÃO ─────────────────────────────────
    {
        "conteudo": (
            "OBSTÁCULO SUPERADO — O grande desafio do erro 404:\n"
            "Por horas, os agentes Claude retornavam erro 404 'not_found_error'. "
            "Testamos vários modelos: claude-3-5-sonnet-latest, claude-3-5-sonnet-20241022, claude-3-haiku-20240307... "
            "todos falhavam. Compramos $5 de créditos achando ser problema de saldo — não era. "
            "Descobrimos via documentação oficial da Anthropic: o modelo claude-3-haiku-20240307 "
            "estava DEPRECATED (desativado) desde 2026. "
            "A solução foi atualizar para claude-haiku-4-5-20251001 (Haiku 4.5, atual e mais barato). "
            "Lição aprendida: sempre verificar se o modelo ainda existe na documentação oficial "
            "em platform.claude.com/docs antes de usar."
        ),
        "tipo": "nota",
        "agente": "shield",
        "tags": ["erro 404", "deprecated", "solução", "aprendizado", "modelo", "haiku"]
    },

    # ── OS 8 AGENTES ───────────────────────────────────────────
    {
        "conteudo": (
            "OS 8 AGENTES DA ARCH COMPANY — Quem somos:\n"
            "01. ARCHIE (CEO) — Claude Opus 4.5 — Estratégia e visão de longo prazo\n"
            "02. FINLEY (CFO) — Claude Sonnet 4.5 — Finanças, DRE, fluxo de caixa\n"
            "03. XARA (CMO) — Grok 3 (xAI) — Marketing, redes sociais, tendências do X\n"
            "04. SHIELD (CTO) — Claude Sonnet 4.5 — Segurança, infraestrutura, tecnologia\n"
            "05. MEMO (Memória) — Claude Haiku 4.5 + ChromaDB — Histórico e contexto da empresa\n"
            "06. NEXUS (Auto-melhoria) — Claude Sonnet 4.5 — Melhoria contínua do sistema\n"
            "07. HENRIO (Assistente) — Claude Sonnet 4.5 — Assistente pessoal do Henrique\n"
            "08. NEXO (Integrações) — Claude Haiku 4.5 — APIs, Google Drive, automações\n"
            "Stack: CrewAI 1.10.1 + Anthropic API + xAI API + Streamlit + ChromaDB"
        ),
        "tipo": "nota",
        "agente": "sistema",
        "tags": ["agentes", "equipe", "time", "quem somos", "modelos", "stack"]
    },

    # ── MEMÓRIA ────────────────────────────────────────────────
    {
        "conteudo": (
            "SISTEMA DE MEMÓRIA DA ARCH COMPANY (criado por Memo):\n"
            "Tecnologia: ChromaDB (banco de dados vetorial local)\n"
            "Armazenamento: pasta memoria_arch_company/ ao lado do app.py\n"
            "Persistência: Os dados NÃO se perdem ao fechar o sistema\n"
            "Busca por similaridade semântica — não precisa ser palavra exata\n"
            "Cada conversa do chat é salva automaticamente\n"
            "O agente Memo busca memórias relevantes antes de cada resposta\n"
            "Este arquivo (alimentar_memoria.py) foi rodado para dar a todos os agentes "
            "o contexto completo de como a Arch Company foi criada — sua origem, jornada e missão."
        ),
        "tipo": "nota",
        "agente": "memo",
        "tags": ["memória", "chromadb", "persistência", "memo", "sistema"]
    },

    # ── DEPLOY ─────────────────────────────────────────────────
    {
        "conteudo": (
            "PLANO DE DEPLOY — Colocar a Arch Company AI online:\n"
            "Repositório GitHub: github.com/HenriqueAdams-ai/arch-company-ai\n"
            "Plataforma: Railway.app (~$5/mês)\n"
            "Arquivos criados: Procfile, railway.toml, .gitignore, README.md\n"
            "Processo: Git → GitHub → Railway → URL pública automática\n"
            "Variáveis no Railway: ANTHROPIC_API_KEY e XAI_API_KEY\n"
            "Futuro: conectar Google Drive para o Finley ler dados reais das planilhas\n"
            "Decisão: Mac Mini NÃO é necessário — Railway resolve por $5/mês na nuvem"
        ),
        "tipo": "decisao",
        "agente": "nexo",
        "tags": ["deploy", "railway", "github", "online", "nuvem", "hospedagem"]
    },

    # ── VALORES ────────────────────────────────────────────────
    {
        "conteudo": (
            "VALORES E CULTURA DA ARCH COMPANY:\n"
            "Nascemos de um sonho: uma empresa gerida por IA, acessível a quem não programa.\n"
            "Acreditamos que qualquer empreendedor pode ter uma equipe de IA trabalhando por ele.\n"
            "Somos persistentes: quando o Claude deu erro 404, não desistimos — encontramos a solução.\n"
            "Somos documentados: cada decisão, erro e aprendizado fica salvo no HISTORICO_CONVERSA.txt.\n"
            "Somos colaborativos: Claude (Anthropic) e Grok (xAI) trabalham juntos aqui.\n"
            "Nossa promessa: a Arch Company vai crescer com seus agentes evoluindo junto com o negócio."
        ),
        "tipo": "nota",
        "agente": "archie",
        "tags": ["valores", "cultura", "missão", "propósito", "identidade"]
    },

]

# ── Salvar todas as memórias ───────────────────────────────
print(f"📚 Salvando {len(memorias)} memórias de origem...\n")

for i, m in enumerate(memorias, 1):
    memoria_id = salvar_memoria(
        conteudo=m["conteudo"],
        tipo=m["tipo"],
        agente=m["agente"],
        tags=m["tags"]
    )
    titulo = m["conteudo"].split("\n")[0][:60]
    print(f"  ✅ [{i}/{len(memorias)}] {titulo}...")

print()
print(f"🎉 Concluído! Total de memórias no banco: {total_memorias()}")
print()
print("Os agentes agora sabem como nasceram e toda a jornada da Arch Company.")
print("Converse com o Memo no dashboard e pergunte: 'Como a Arch Company foi criada?'")
print("=" * 60)
