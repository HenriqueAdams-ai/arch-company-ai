# ARCH COMPANY AI — Como Usar

## Inicio Rapido (5 minutos)

### 1. Instale as dependencias
```bash
pip install -r requirements.txt
```

### 2. Configure as API Keys
```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sua-key-do-claude"
$env:XAI_API_KEY       = "sua-key-do-grok"

# Mac/Linux
export ANTHROPIC_API_KEY="sua-key-do-claude"
export XAI_API_KEY="sua-key-do-grok"
```

### 3. Execute o dashboard
```bash
streamlit run app.py
```

### 4. Acesse no navegador
```
http://localhost:8501
```

## Onde conseguir as API Keys

| API | Link | Custo |
|-----|------|-------|
| Claude (Anthropic) | console.anthropic.com | ~R$0,05/resposta |
| Grok (xAI) | console.x.ai | Mais barato que Claude |

## Arquivos do Projeto

```
arch_company_dashboard/
├── app.py              <- Dashboard principal (abra aqui)
├── agents.py           <- Definicao dos 8 agentes CrewAI
├── requirements.txt    <- Dependencias para instalar
└── COMO_USAR.md        <- Este arquivo
```

## Proximos Passos

1. Conectar Google Drive: Baixe o `credentials.json` em console.cloud.google.com
2. Adicionar memoria real: O ChromaDB ja esta configurado em agents.py
3. Deploy online: Use Railway.app para acessar de qualquer lugar

Consulte o arquivo **ArchCompany_Sistema_IA_Completo.docx** para o plano completo.
