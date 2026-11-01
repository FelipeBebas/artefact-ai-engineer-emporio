# Proposal: Empório da Música AI Customer Service Agent

## Why

A Empório da Música (Campo Grande/MS) enfrenta sobrecarga em sua equipe de atendimento devido a um alto volume de dúvidas recorrentes sobre horários de funcionamento, status e rastreamento de pedidos, disponibilidade e preços de instrumentos musicais, além de regras de garantia, devolução e pagamento. 

Este projeto constrói um protótipo funcional de agente conversacional inteligente em Python, atuando como primeiro ponto de contato acolhedor e resolutivo para desafogar a equipe humana, garantindo respostas precisas, ancoradas nos dados transacionais da loja e alinhadas às suas diretrizes operacionais.

## What Changes

- **Agente Conversacional Baseado em Grafo (LangGraph):** Orquestração orientada a estado (`MessagesState`) com memória conversacional multi-turn (`MemorySaver`) e capacidade de raciocínio com chamadas determinísticas de ferramentas.
- **Persona Especialista & Guardrails de Escopo:** Definição de persona musical acolhedora ("amigo que entende de instrumentos musicais"), com salvaguarda estrita para recusa cordial e redirecionamento de acessórios não comercializados (cordas, cabos, palhetas, amplificadores, pedais e cases).
- **Camada Transacional Determinística (SQLite):** Ingestão e indexação relacional dos datasets (`products.csv`, `orders.csv`, `order_items.csv`, `customers.csv`, `categories.csv`, `promotions.csv`), viabilizando consultas precisas de estoque, especificações em JSON, preços e rastreamento de entregas sem alucinações numéricas.
- **Motor de Políticas Determinístico (Zero-Flake Policy Engine):** Indexação seccional in-memory do manual de políticas (`políticas_da_loja.pdf`) com roteamento semântico garantido via tipos `Enum` do Pydantic, eliminando a fragilidade e ruído de embeddings vetoriais para pequenos volumes textuais.
- **Interface Interativa Moderna (Chainlit) e CLI:** Interface gráfica web conversacional com exibição transparente dos passos de raciocínio e chamadas de ferramentas, complementada por um runner CLI para testes rápidos e automatizados.
- **Documentação de Engenharia e Casos de Uso:** README abrangente com justificativas arquiteturais, limitações conhecidas, uso de assistentes de IA e registro de 5 cenários reais de atendimento.

## Capabilities

### New Capabilities
- `atendimento-emporio`: Atendimento conversacional inteligente aos clientes da Empório da Música, abrangendo identificação de persona, consulta a catálogo e estoque, verificação de pedidos e rastreio, checagem de promoções vigentes, esclarecimento de políticas operacionais (garantia, frete, devoluções, formas de pagamento) e bloqueio/redirecionamento de itens fora de escopo.

### Modified Capabilities
<!-- Nenhuma capacidade pré-existente está sendo modificada neste projeto greenfield. -->

## Impact

- **Código:** Criação da estrutura de módulos em `src/` (`agent/`, `database/`, `knowledge/`, `cli.py`, `app.py`).
- **Dependências:** Inclusão de `langgraph`, `langchain`, `pydantic`, `chainlit`, `python-dotenv`, `tabulate` em `requirements.txt`.
- **Dados:** Processamento automatizado dos arquivos existentes em `data/` para um banco de dados local SQLite (`emporio.db`).
- **Entregáveis do Desafio:** Repositório Git público, `README.md` técnico e documentação de 5 conversas em `docs/cenarios_interacao.md`.
