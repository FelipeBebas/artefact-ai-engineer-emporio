# Design

## Context

Ao clicar nos botões de ação configurados em `src/app.py`, a mensagem enviada foi renderizada à esquerda com a identidade do assistente, e nenhuma resposta subsequente foi gerada para o usuário.
Veja `proposal.md` para motivação e `specs/interface-atendimento/spec.md` para os cenários normativos.

## Goals / Non-Goals

**Goals:**
- Garantir que a pergunta clicada pelo usuário seja renderizada à direita como uma mensagem do usuário (`author="User"`, `type="user_message"`), ativando a cápsula rosa `#831843`.
- Assegurar que a resposta do agente seja disparada e entregue ao usuário de maneira infalível, mesmo em caso de variações no contexto assíncrono do endpoint HTTP `/project/action` do Chainlit.
- Adicionar proteção com `try...except` e fallback de invocação para evitar qualquer falha silenciosa.

**Non-Goals:**
- Não alterar a lógica de negócios das ferramentas (`consultar_catalogo`, `consultar_pedido`, etc.).
- Não modificar o esquema de banco de dados SQLite.

## Decisions

### 1. Envio Explícito com `type="user_message"` e `author="User"`
- **Decisão**: Na função `on_quick_prompt`, instanciar a mensagem com:
  ```python
  await cl.Message(content=prompt, author="User", type="user_message").send()
  ```
- **Justificativa**: O construtor de `cl.Message` define por padrão `type="assistant_message"` e `author=config.ui.name`. Sem esses parâmetros explícitos, o Chainlit injeta `data-step-type="assistant_message"` no DOM, formatando o balão como se o assistente estivesse falando com ele mesmo. Ao passar `type="user_message"`, o frontend aplica a estilização do balão rosa na direita.

### 2. Resiliência de Execução com Fallback para `run_agent_message`
- **Decisão**: No callback de ação, envolver o processamento da query em bloco protegido. Se a execução com streaming de passos (`cl.Step`) falhar devido a restrições de contexto WebSocket no handler HTTP de ações do Chainlit, o sistema recorre imediatamente a `asyncio.to_thread(run_agent_message, prompt, thread_id)`.
- **Justificativa**: Garante 100% de confiabilidade na entrega da resposta final para o cliente, eliminando travamentos silenciosos.

### 3. Remoção Não-Bloqueante dos Botões de Sugestão
- **Decisão**: Tratar a chamada `welcome_msg.remove_actions()` com proteção contra falhas (`try/except`), garantindo que o ciclo de resposta nunca seja interrompido caso a remoção de botões sofra atraso no socket.

## Risks / Trade-offs

- **[Risco] Latência na resposta inicial do LLM** → Mitigação: Emissão imediata do balão do usuário e exibição de indicador de digitação antes do envio da resposta do assistente.
