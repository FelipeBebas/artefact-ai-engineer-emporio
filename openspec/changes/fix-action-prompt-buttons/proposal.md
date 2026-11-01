# Proposal

## Why

Ao clicar em um dos botões de sugestão interativos (*quick prompts / actions*), o comportamento observado divergiu da experiência esperada:
1. O texto da pergunta foi renderizado como mensagem do sistema/assistente (balão escuro à esquerda com avatar do bot), em vez de uma mensagem autêntica do cliente (balão rosa à direita com `type="user_message"`).
2. Nenhuma resposta foi gerada pelo assistente, devido ao processamento da ação ter falhado silenciosamente sem emissão de mensagem de retorno ou por ausência de ciclo de vida de tarefa ativo no contexto HTTP da ação no Chainlit.

## What Changes

- **Renderização correta da mensagem do usuário**: Definir explicitamente `type="user_message"` e `author="User"` ao instanciar e enviar a mensagem originada pelo clique no botão, assegurando que o texto apareça estilizado no balão rosa à direita.
- **Execução confiável do agente no callback de ação**: Reestruturar a execução da consulta ao LangGraph para rodar de forma assíncrona protegida (`try/except`), garantindo a geração e envio do balão de resposta do assistente (e passos de ferramentas quando aplicável), mesmo quando disparado via callback HTTP de ação do Chainlit.
- **Tratamento gracioso de erros**: Capturar eventuais falhas de conexão com APIs externas ou timeouts e emitir uma resposta amigável ao usuário em vez de falha silenciosa.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade isolada necessária)*

### Modified Capabilities
- `interface-atendimento`: Garante que interações disparadas por botões de ação simulem fielmente a mensagem do usuário (`user_message`) e engatilhem a resposta do agente com persistência e feedback visual.

## Impact

- **Código**: `src/app.py` (ajuste em `on_quick_prompt` e `process_user_query`).
- **Testes**: `tests/test_app.py` (verificação de envio com `type="user_message"` e resposta gerada).
