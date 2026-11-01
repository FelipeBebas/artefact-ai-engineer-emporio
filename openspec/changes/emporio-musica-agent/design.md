# Design: Empório da Música AI Customer Service Agent

## Context

A Empório da Música possui uma operação de varejo musical com catálogo estruturado em CSVs (`products.csv`, `orders.csv`, `order_items.csv`, `customers.csv`, `categories.csv`, `promotions.csv`) e um manual de políticas de 8 páginas (`políticas_da_loja.pdf`). A solução deve ser desenvolvida em Python e atender aos critérios de robustez, determinismo numérico, alinhamento de persona e transparência de raciocínio avaliados no processo seletivo da Artefact (veja `proposal.md` para motivação e `specs/atendimento-emporio/spec.md` para requisitos comportamentais).

## Goals / Non-Goals

**Goals:**
- Orquestração de estado multi-turn robusta e auditável via LangGraph (`StateGraph`).
- Consultas determinísticas e livres de alucinação de preços, estoque e pedidos via SQLite local.
- Recuperação com 100% de recall e zero ruído vetorial das políticas da loja (Zero-Flake Policy Engine) utilizando tipagem estrita de `Enum` no Pydantic.
- Interface conversacional moderna e de baixa fricção via Chainlit, com visualização transparente de raciocínio e tool calls, além de suporte CLI nativo.
- Arquitetura desacoplada e agnóstica de provedor LLM (OpenAI, Gemini ou Anthropic via `.env`).

**Non-Goals:**
- Implementação de pipelines complexos de embeddings ou bancos vetoriais pesados (ChromaDB/Pinecone), injustificados para o volume de 8 páginas.
- Venda ou transações de checkout ativo (apenas consulta consultiva, status de pedidos e cálculo de frete/regras).
- Integração em produção com a infraestrutura da Meta/WhatsApp (o WhatsApp é simulado fielmente via Chainlit/CLI).

## Decisions

### 1. Framework do Agente: LangGraph (`StateGraph`)
- **Escolha:** Utilizar `langgraph.graph.StateGraph` com nó de agente (`LLMNode`) e nó de ferramentas (`ToolNode`) conectados condicionalmente por `tools_condition`.
- **Racional:** LangGraph é o padrão sênior da indústria para fluxos de agentes que exigem controle determinístico de ciclo, persistência de estado e clareza de transições.
- **Alternativas consideradas:**
  - *Scripts ReAct puros:* Difíceis de manter em produção e sem rastreabilidade de estado nativa.
  - *LlamaIndex / CrewAI:* Abstrações excessivas que ocultam o raciocínio e complicam o controle fino de guardrails.

### 2. Camada de Dados Transacionais: SQLite Relacional
- **Escolha:** Ingerir os CSVs em um banco SQLite local (`emporio.db`) durante a inicialização, expondo consultas parametrizadas encapsuladas em ferramentas Python (`@tool`).
- **Racional:** Os dados de catálogo e pedidos possuem relações estritas (ex: `order_items` -> `products`, `specs` em JSON). Text-to-SQL ingênuo é vulnerável a alucinações e injeção; ferramentas Python especializadas (`consultar_catalogo`, `consultar_pedido`) garantem 100% de precisão nos números e limites de preço (`<= R$1000`).
- **Alternativas consideradas:**
  - *DataFrames Pandas em memória:* Menos idiomático para modelar relacionamentos entre múltiplas tabelas.
  - *Vector DB sobre CSVs:* Inadequado para filtros numéricos exatos e checagem de estoque.

### 3. Motor de Políticas: Zero-Flake Sectional Engine com Pydantic `Enum`
- **Escolha:** Mapear as 8 seções do manual em um dicionário Python em memória, tipando o argumento da ferramenta com um `Enum` (`TopicoPolitica`).
- **Racional:** O manual tem apenas ~2.000 palavras. Um pipeline vetorial (chunking + embedding similarity) gera perda de contexto e falsos negativos. Ao fornecer um `Enum` no JSON Schema da tool, a LLM realiza o roteamento semântico nativamente, eliminando necessidade de Regex complexo e garantindo que o trecho oficial da regra seja injetado sem ruído.
- **Alternativas consideradas:**
  - *ChromaDB / FAISS:* Adiciona dependências pesadas de compilação C++ no ambiente do avaliador sem ganho real para 8 páginas.
  - *Parser de palavras-chave por Regex:* Frágil diante de variações de linguagem natural, gírias e frases negativas.

### 4. Interface do Usuário: Chainlit (+ CLI Fallback)
- **Escolha:** Chainlit como frontend principal e `cli.py` como interface de linha de comando.
- **Racional:** O Chainlit provê uma interface moderna, reativa, responsiva e com suporte nativo para inspecionar steps de raciocínio e execução de tools. Roda localmente com `chainlit run src/app.py` sem dependência de serviços em nuvem ou configurações externas.
- **Alternativas consideradas:**
  - *Streamlit:* Interface considerada antiquada e menos natural para chat contínuo com streaming.
  - *Typebot:* Exigiria que o avaliador criasse túneis externos (ngrok) e importasse fluxos em plataforma terceira.

### 5. Memória e Persistência de Conversa: LangGraph `MemorySaver`
- **Escolha:** Checkpointer em memória (`MemorySaver`) indexado por `thread_id` (sessão do usuário).
- **Racional:** Permite diálogos coesos multi-turn (ex: cliente referencia *"e esse modelo tem na cor preta?"* sem repetir o nome do violão).

---

## Architecture Diagram & Data Flow

```text
+-----------------------------------------------------------------------------+
|                          INTERFACE (Chainlit / CLI)                         |
+-----------------------------------------------------------------------------+
                                      |
                     (thread_id, user_message)
                                      v
+-----------------------------------------------------------------------------+
|                           LANGGRAPH STATEGRAPH                              |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  | Agent Node (LLM + System Instructions + Guardrails)                   |  |
|  | - Persona: Especialista e amigo músico da Empório da Música          |  |
|  | - Guardrail: Bloqueio estrito de acessórios (cordas, pedais, cabos)   |  |
|  | - Avaliação: Resposta direta OU Invocação de Tools                   |  |
|  +-----------------------------------+-----------------------------------+  |
|                                      |                                      |
|               +----------------------+----------------------+               |
|               | tools_condition                             |               |
|               v (Se tool call)                              v (Se final)    |
|  +---------------------------------------+             +-----------------+  |
|  | ToolNode (Execução Determinística)    |             | Resposta Final  |  |
|  |                                       |             | ao Cliente      |  |
|  | 1. consultar_catalogo(termo, preco)   |             +-----------------+  |
|  | 2. consultar_pedido(identificador)    |                      ^           |
|  | 3. consultar_promocoes(produto_id)    |                      |           |
|  | 4. consultar_politicas(Enum: topico)  |                      |           |
|  +-------------------+-------------------+                      |           |
|                      | (ToolMessage com fatos)                  |           |
|                      +------------------------------------------+           |
+-----------------------------------------------------------------------------+
```

---

## Risks / Trade-offs

- **[Risco: Alucinação em Preços ou Estoque]**  
  *Mitigação:* O system prompt proíbe expressamente inventar valores ou status sem antes executar a tool correspondente. As tools retornam apenas os dados verdadeiros do SQLite.
- **[Risco: Tentativa de Compra de Acessórios (Fora de Escopo)]**  
  *Mitigação:* Regra explícita de guarda no prompt que intercepta pedidos de cordas, palhetas, amplificadores e cabos, instruindo o modelo a negar a venda com gentileza e recomendar parceiros da região.
- **[Risco: Chave de API de Terceiros Ausente no Ambiente de Teste]**  
  *Mitigação:* Suporte padronizado via `python-dotenv`, documentação cristalina no README com exemplo em `.env.example` e fallback configurável entre OpenAI e Google Gemini.
