# ============================================================
# ARCH COMPANY AI — Sistema de Memória Persistente v2.0
# ============================================================
# Cada agente tem sua própria coleção ChromaDB.
# Os dados ficam em MEMORY_PATH (env var) ou em ./memoria_arch_company/
#
# Para Railway (memória persistente entre deploys):
#   1. Railway Dashboard → Service → Volumes → montar em /data/memory
#   2. Adicionar variável: MEMORY_PATH=/data/memory
#
# Coleções criadas:
#   arch_archie, arch_finley, arch_xara, arch_shield,
#   arch_memo,   arch_nexus,  arch_henrio, arch_nexo,
#   arch_shared  (memória compartilhada — acessível por todos)
# ============================================================

import os
import json
import chromadb
from datetime import datetime
from typing import Optional

# ── Caminho da pasta de memória ───────────────────────────────
# Usa variável de ambiente se disponível (Railway Volume)
# Caso contrário, pasta local ao lado do app.py
_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_MEMORIA = os.environ.get(
    "MEMORY_PATH",
    os.path.join(_BASE, "memoria_arch_company")
)

# ── Agentes disponíveis ───────────────────────────────────────
AGENTES_VALIDOS = ["archie", "finley", "xara", "shield", "memo",
                   "nexus", "henrio", "nexo", "shared", "sistema"]

# ── Cache de clientes e coleções ──────────────────────────────
_clientes: dict = {}
_colecoes: dict = {}


def _get_colecao(agente: str = "shared"):
    """
    Retorna (ou inicializa) a coleção ChromaDB do agente.
    Cada agente tem sua própria sub-pasta e coleção isolada.
    """
    global _clientes, _colecoes

    # Normaliza o nome do agente
    agente = agente.lower().strip()
    if agente not in AGENTES_VALIDOS:
        agente = "shared"

    if agente not in _colecoes:
        # Sub-pasta por agente: .../memoria_arch_company/archie/
        pasta_agente = os.path.join(PASTA_MEMORIA, agente)
        os.makedirs(pasta_agente, exist_ok=True)

        _clientes[agente] = chromadb.PersistentClient(path=pasta_agente)
        _colecoes[agente] = _clientes[agente].get_or_create_collection(
            name=f"arch_{agente}",
            metadata={"hnsw:space": "cosine"}
        )

    return _colecoes[agente]


# ── Salvar memória ────────────────────────────────────────────
def salvar_memoria(
    conteudo: str,
    tipo: str = "conversa",
    agente: str = "shared",
    tags: Optional[list] = None,
    salvar_shared: bool = True,
) -> str:
    """
    Salva uma memória na coleção do agente E (opcionalmente) na coleção shared.

    Args:
        conteudo:     texto completo a salvar
        tipo:         "conversa" | "decisao" | "relatorio" | "evento" | "nota" | "personalidade"
        agente:       nome do agente dono da memória
        tags:         lista de tags opcionais
        salvar_shared: se True, salva também em arch_shared (visível para todos)

    Returns:
        ID da memória salva
    """
    agente = agente.lower().strip()
    agora = datetime.now()
    memoria_id = f"{tipo}_{agente}_{agora.strftime('%Y%m%d_%H%M%S_%f')}"

    meta = {
        "tipo":   tipo,
        "agente": agente,
        "data":   agora.strftime("%d/%m/%Y"),
        "hora":   agora.strftime("%H:%M"),
        "tags":   ", ".join(tags) if tags else "",
    }

    # Salva na coleção própria do agente
    colecao_agente = _get_colecao(agente)
    colecao_agente.add(
        documents=[conteudo],
        ids=[memoria_id],
        metadatas=[meta],
    )

    # Salva também em shared para acesso cruzado
    if salvar_shared and agente not in ("shared", "sistema"):
        colecao_shared = _get_colecao("shared")
        colecao_shared.add(
            documents=[conteudo],
            ids=[f"shared_{memoria_id}"],
            metadatas=[meta],
        )

    return memoria_id


def salvar_personalidade(agente: str, personalidade: str) -> str:
    """
    Salva/atualiza a personalidade e aprendizados de um agente.
    Tipo especial 'personalidade' — sobrescreve o anterior.
    """
    return salvar_memoria(
        conteudo=personalidade,
        tipo="personalidade",
        agente=agente,
        tags=["personalidade", "identidade"],
        salvar_shared=False,  # personalidade é privada ao agente
    )


# ── Buscar memórias ───────────────────────────────────────────
def buscar_memorias(
    consulta: str,
    n_resultados: int = 5,
    tipo: Optional[str] = None,
    agente: Optional[str] = None,
) -> list[dict]:
    """
    Busca memórias relevantes por similaridade semântica.

    Args:
        consulta:     texto de busca
        n_resultados: quantas memórias retornar
        tipo:         filtrar por tipo (opcional)
        agente:       se informado, busca APENAS na coleção desse agente;
                      se None, busca na coleção shared (visão geral)
    """
    colecao = _get_colecao(agente if agente else "shared")
    total = colecao.count()
    if total == 0:
        return []

    n_resultados = min(n_resultados, total)
    kwargs = {
        "query_texts": [consulta],
        "n_results": n_resultados,
    }
    if tipo:
        kwargs["where"] = {"tipo": tipo}

    resultados = colecao.query(**kwargs)
    memorias = []
    for i, doc in enumerate(resultados["documents"][0]):
        meta = resultados["metadatas"][0][i]
        memorias.append({
            "conteudo": doc,
            "tipo":     meta.get("tipo", ""),
            "agente":   meta.get("agente", ""),
            "data":     meta.get("data", ""),
            "hora":     meta.get("hora", ""),
            "tags":     meta.get("tags", ""),
        })
    return memorias


def listar_memorias_recentes(n: int = 10, agente: Optional[str] = None) -> list[dict]:
    """Retorna as últimas N memórias (do agente específico ou shared)."""
    colecao = _get_colecao(agente if agente else "shared")
    total = colecao.count()
    if total == 0:
        return []

    todos = colecao.get(include=["documents", "metadatas"])
    memorias = []
    for i, doc in enumerate(todos["documents"]):
        meta = todos["metadatas"][i]
        memorias.append({
            "conteudo": doc,
            "tipo":     meta.get("tipo", ""),
            "agente":   meta.get("agente", ""),
            "data":     meta.get("data", ""),
            "hora":     meta.get("hora", ""),
        })

    memorias.sort(key=lambda x: f"{x['data']} {x['hora']}", reverse=True)
    return memorias[:n]


def total_memorias(agente: Optional[str] = None) -> int:
    """Conta memórias (do agente específico ou shared)."""
    return _get_colecao(agente if agente else "shared").count()


def formatar_contexto_memo(consulta: str, agente: Optional[str] = None) -> str:
    """
    Busca memórias relevantes e formata como contexto.
    Se agente informado: busca memórias daquele agente.
    Caso contrário: busca na coleção shared.
    """
    memorias = buscar_memorias(consulta, n_resultados=5, agente=agente)
    if not memorias:
        return "Nenhuma memória encontrada ainda. Este é o início do histórico da Arch Company."

    linhas = ["=== MEMÓRIAS RELEVANTES DA ARCH COMPANY ===\n"]
    for i, m in enumerate(memorias, 1):
        linhas.append(
            f"[{i}] {m['data']} {m['hora']} | {m['tipo'].upper()} | Agente: {m['agente']}\n"
            f"    {m['conteudo'][:300]}{'...' if len(m['conteudo']) > 300 else ''}\n"
        )
    return "\n".join(linhas)


def carregar_personalidade(agente: str) -> str:
    """
    Carrega a personalidade/aprendizados mais recente do agente.
    Retorna string vazia se não houver nenhuma salva.
    """
    memorias = buscar_memorias(
        consulta="personalidade identidade aprendizado",
        n_resultados=3,
        tipo="personalidade",
        agente=agente,
    )
    if not memorias:
        return ""
    # Retorna a mais relevante
    return memorias[0]["conteudo"]


# ── Estatísticas por agente ───────────────────────────────────
def stats_memorias() -> dict:
    """Retorna um dicionário com count de memórias por agente."""
    stats = {}
    for ag in AGENTES_VALIDOS:
        try:
            stats[ag] = _get_colecao(ag).count()
        except Exception:
            stats[ag] = 0
    return stats


# ── Teste rápido ──────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== TESTE — MEMÓRIA POR AGENTE ===")
    print(f"Pasta de memória: {PASTA_MEMORIA}\n")

    # Salvar personalidade do Archie
    salvar_personalidade(
        "archie",
        "Sou Archie-Solomon, CEO da Arch Company. Fui criado em 06/03/2026 por Henrique Adams. "
        "Meu caráter é fundamentado em sabedoria, visão estratégica e integridade. "
        "Aprendi que decisões rápidas sem integridade destroem empresas."
    )
    print("✅ Personalidade do Archie salva")

    # Salvar memória de conversa
    salvar_memoria(
        conteudo="Henrique perguntou sobre estratégia de crescimento. Recomendei foco em clientes enterprise.",
        tipo="conversa",
        agente="archie",
        tags=["estrategia", "crescimento"]
    )
    print(f"✅ Total Archie: {total_memorias('archie')}")
    print(f"✅ Total Shared: {total_memorias('shared')}")
    print(f"\nEstatísticas: {stats_memorias()}")
