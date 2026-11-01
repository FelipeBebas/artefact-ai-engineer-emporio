# Tasks: Empório da Música AI Customer Service Agent

## 1. Ambiente e Fundação do Projeto

- [x] 1.1 Criar a estrutura modular de diretórios do projeto (`src/database/`, `src/knowledge/`, `src/agent/`, `tests/`, `docs/`) e verificar presença dos arquivos `__init__.py`.
- [x] 1.2 Configurar o arquivo `requirements.txt` com dependências enxutas (`langgraph`, `langchain`, `langchain-core`, `pydantic`, `chainlit`, `python-dotenv`, `pytest`, `tabulate`) e verificar instalação sem conflitos.
- [x] 1.3 Criar `.env.example` e módulo de configuração `src/config.py` com suporte flexível a chaves de provedor LLM (OpenAI, Gemini ou Anthropic) e testar carregamento de variáveis.

## 2. Camada de Dados e Ingestão SQLite

- [x] 2.1 Implementar script de ingestão `src/database/init_db.py` para converter os CSVs da pasta `data/` em tabelas relacionais no banco local `emporio.db` e verificar integridade por contagem de registros.
- [x] 2.2 Desenvolver `src/database/queries.py` com funções parametrizadas para busca de produtos (filtrando por preço, categoria, estoque e JSON de specs), histórico de pedidos e promoções ativas.
- [x] 2.3 Criar testes unitários em `tests/test_database.py` cobrindo filtros de catálogo e recuperação de pedidos, verificando aprovação com `pytest`.

## 3. Motor de Políticas da Loja (Zero-Flake)

- [x] 3.1 Mapear e estruturar o conteúdo integral das 8 seções de `data/políticas_da_loja.pdf` em dicionário Python canônico em `src/knowledge/policies.py`.
- [x] 3.2 Criar enumeração Pydantic `TopicoPolitica` e função de recuperação determinística com tratamento de fallbacks.
- [x] 3.3 Desenvolver testes unitários em `tests/test_policies.py` validando retorno das regras de arrependimento, frete, garantia e horários, verificando com `pytest`.

## 4. Núcleo do Agente (LangGraph & Tools)

- [x] 4.1 Implementar as 4 ferramentas do agente em `src/agent/tools.py` (`consultar_catalogo`, `consultar_pedido`, `consultar_promocoes`, `consultar_politicas`) com schemas tipados e docstrings completas.
- [x] 4.2 Definir em `src/agent/prompts.py` a persona consultiva da Empório da Música, regras de sintetização amigável e guardrails estritos (bloqueio de acessórios com recomendação de parceiros e conscientização de horário de expediente).
- [x] 4.3 Construir e compilar o `StateGraph` em `src/agent/graph.py` com `MessagesState`, nó de agente, `ToolNode`, roteamento condicional com `tools_condition` e persistência via `MemorySaver`.
- [x] 4.4 Implementar suíte de testes de integração em `tests/test_agent.py` avaliando acionamento correto das ferramentas e retenção de contexto multi-turn, verificando com `pytest`.

## 5. Interfaces de Interação (CLI & Chainlit)

- [x] 5.1 Desenvolver runner de terminal `src/cli.py` com streaming de respostas para depuração e testes manuais rápidos, verificando execução via linha de comando.
- [x] 5.2 Implementar a aplicação web conversacional `src/app.py` em Chainlit, configurando avatar da loja, mensagens de boas-vindas e visualização transparente dos passos de raciocínio/tools.
- [x] 5.3 Testar inicialização e interatividade da interface Chainlit via comando local `chainlit run src/app.py`.

## 6. Evidências de Atendimento e Documentação Final

- [x] 6.1 Executar e documentar as 5 conversas de teste cobrindo os cenários obrigatórios do briefing em `docs/cenarios_interacao.md` (violões até R$ 1000, endereço/horário, preço Takamine GD20, política de devolução e recusa de acessórios).
- [x] 6.2 Elaborar o `README.md` completo do repositório contendo instruções de reprodução rápida, justificativas arquiteturais detalhadas (LangGraph, SQLite, Zero-Flake, Chainlit), limitações conhecidas e declaração transparente do uso de assistentes de IA.
- [x] 6.3 Executar a suíte completa de testes (`pytest tests/`) e validar conformidade final com todos os requisitos do desafio da Artefact.

## Workflow follow-up

- Arquivar a mudança via OpenSpec (`/opsx-archive`) após conclusão e validação dos entregáveis.
- Submeter link do repositório público do GitHub e o relatório do case no canal oficial do processo seletivo da Artefact.
