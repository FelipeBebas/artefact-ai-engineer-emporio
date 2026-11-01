# Tasks

## 1. Ajuste da Mensagem do Usuário e Callback de Ação

- [x] 1.1 Atualizar `on_quick_prompt` em `src/app.py` para instanciar e enviar a mensagem com `author="User"` e `type="user_message"`, garantindo que o texto apareça no balão rosa do usuário à direita
- [x] 1.2 Implementar remoção protegida das ações com tratamento de exceções para que atrasos no socket não interrompam o ciclo de resposta

## 2. Resiliência do Processamento de Queries e Fallback do Agente

- [x] 2.1 Refatorar `process_user_query` em `src/app.py` adicionando proteção `try/except` com fallback automático para invocação síncrona/thread caso o streaming de steps sofra instabilidade no handler de ação
- [x] 2.2 Adicionar testes unitários em `tests/test_app.py` validando o comportamento de `on_quick_prompt` e a emissão de mensagem de tipo `user_message`
- [x] 2.3 Executar a suíte completa de testes com `pytest tests/` e certificar que todos os testes passam com 100% de sucesso
