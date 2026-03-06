# ============================================================
# ARCH COMPANY AI — Sistema de Memória Persistente (Memo)
# ============================================================
# Usa ChromaDB para armazenar e recuperar memórias da empresa.
# Cada conversa, decisão e evento fica salvo em disco.
#
# Instalação necessária:
#   pip install chromadb
# ============================================================

import os
import chromadb
from chromadb.config import Settings
from datetime import datetime
from typing import Optional

# ── Configuração do ChromaDB ──────────────────────────────
# Os dados ficam salvos na pasta "memoria_arch_company"
# ao lado do app.py — PERSISTENTE entre reinicializações
PASTA_MEMORIA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memoria_arch_company"
)

_cliente_chroma = None
_colecao_memo = None


def _get_colecao():
    """Inicializa (ou retorna) a coleção ChromaDB de memórias."""
    global _cliente_chroma, _colecao_memo
    if _colecao_memo is None:
        _cliente_chroma = chromadb.PersistentClient(path=PASTA_MEMORIA)
        _colecao_memo = _cliente_chroma.get_or_create_collection(
            name="arch_company_memoria",
            metadata={"hnsw:space": "cosine"}
        )
    return _colecao_memo


# ── Salvar memória ────────────────────────────────────────
def salvar_memoria(
    conteudo: str,
    tipo: str = "conversa",
    agente: str = "sistema",
    tags: Optional[list] = None
) -> str:
    """
    Salva uma memória no ChromaDB.

    Args:
        conteudo: texto da memória (pergunta + resposta, decisão, etc.)
        tipo: "conversa" | "decisao" | "relatorio" | "evento" | "nota"
        agente: nome do agente que gerou a memória
        tags: lista de tags opcionais para filtro

    Returns:
        ID da memória salva
    """
    colecao = _get_colecao()
    agora = datetime.now()
    memoria_id = f"{tipo}_{agente}_{agora.strftime('%Y%m%d_%H%M%S_%f')}"

    colecao.add(
        documents=[conteudo],
        ids=[memoria_id],
        metadatas=[{
            "tipo": tipo,
            "agente": agente,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M"),
            "tags": ", ".join(tags) if tags else "",
        }]
    )
    return memoria_id


# ── Buscar memórias ───────────────────────────────────────
def buscar_memorias(
    consulta: str,
    n_resultados: int = 5,
    tipo: Optional[str] = None
) -> list[dict]:
    """
    Busca memórias relevantes por similaridade semântica.

    Args:
        consulta: texto de busca
        n_resultados: quantas memórias retornar
        tipo: filtrar por tipo ("conversa", "decisao", etc.) — opcional

    Returns:
        Lista de dicionários com conteúdo e metadados
    """
    colecao = _get_colecao()

    # Verifica se há memórias
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
            "tipo": meta.get("tipo", ""),
            "agente": meta.get("agente", ""),
            "data": meta.get("data", ""),
            "hora": meta.get("hora", ""),
            "tags": meta.get("tags", ""),
        })
    return memorias


# ── Listar memórias recentes ──────────────────────────────
def listar_memorias_recentes(n: int = 10) -> list[dict]:
    """Retorna as últimas N memórias salvas."""
    colecao = _get_colecao()
    total = colecao.count()
    if total == 0:
        return []

    # Busca todas e pega as mais recentes (ChromaDB não tem ORDER BY nativo)
    todos = colecao.get(include=["documents", "metadatas"])
    memorias = []
    for i, doc in enumerate(todos["documents"]):
        meta = todos["metadatas"][i]
        memorias.append({
            "conteudo": doc,
            "tipo": meta.get("tipo", ""),
            "agente": meta.get("agente", ""),
            "data": meta.get("data", ""),
            "hora": meta.get("hora", ""),
        })

    # Ordena por data/hora (mais recente primeiro)
    memorias.sort(key=lambda x: f"{x['data']} {x['hora']}", reverse=True)
    return memorias[:n]


# ── Total de memórias ─────────────────────────────────────
def total_memorias() -> int:
    """Retorna quantas memórias estão armazenadas."""
    return _get_colecao().count()


# ── Formatar contexto para o agente Memo ─────────────────
def formatar_contexto_memo(consulta: str) -> str:
    """
    Busca memórias relevantes e formata como contexto
    para o agente Memo responder com base no histórico real.
    """
    memorias = buscar_memorias(consulta, n_resultados=5)
    if not memorias:
        return "Nenhuma memória encontrada ainda. Este é o início do histórico da Arch Company."

    linhas = ["=== MEMÓRIAS RELEVANTES DA ARCH COMPANY ===\n"]
    for i, m in enumerate(memorias, 1):
        linhas.append(
            f"[{i}] {m['data']} {m['hora']} | {m['tipo'].upper()} | Agente: {m['agente']}\n"
            f"    {m['conteudo'][:300]}{'...' if len(m['conteudo']) > 300 else ''}\n"
        )
    return "\n".join(linhas)


# ── Teste rápido ──────────────────────────────────────────
if __name__ == "__main__":
    print("=== TESTE DO SISTEMA DE MEMÓRIA ===\n")

    # Salvar algumas memórias de teste
    id1 = salvar_memoria(
        "Henrique decidiu focar em clientes do setor de tecnologia em março/2026.",
        tipo="decisao",
        agente="archie",
        tags=["estrategia", "clientes", "2026"]
    )
    print(f"✅ Memória salva: {id1}")

    id2 = salvar_memoria(
        "Receita de fevereiro/2026: R$ 45.200. Despesas: R$ 28.100. Lucro: R$ 17.100.",
        tipo="relatorio",
        agente="finley",
        tags=["financeiro", "fevereiro", "2026"]
    )
    print(f"✅ Memória salva: {id2}")

    id3 = salvar_memoria(
        "Usuário perguntou: Como está o caixa da empresa? "
        "Henrio respondeu: O caixa está em R$ 32.400, com alta de 8% no mês.",
        tipo="conversa",
        agente="henrio",
        tags=["caixa", "financeiro"]
    )
    print(f"✅ Memória salva: {id3}")

    print(f"\nTotal de memórias: {total_memorias()}")

    # Buscar por relevância
    print("\n=== BUSCANDO: 'receita e lucro' ===")
    resultados = buscar_memorias("receita e lucro da empresa")
    for r in resultados:
        print(f"  [{r['tipo']}] {r['data']} — {r['conteudo'][:100]}...")

    print("\n✅ Sistema de memória funcionando!")
