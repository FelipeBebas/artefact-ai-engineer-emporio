# Design: UI Polish and REST API Integration

## Context

A versão 1 do agente implementou o grafo LangGraph, ferramentas determinísticas e a interface básica do Chainlit. A versão 2 refina a experiência visual para se alinhar esteticamente com o WhatsApp Web (wallpaper doodle musical, remoção de uploads, destaque de nova conversa e animações fluidas) e adiciona uma camada de API REST para integração programática.

## Goals / Non-Goals

**Goals:**
- Desabilitar uploads e drag-and-drop de arquivos/imagens via configuração nativa do Chainlit (`config.toml`).
- Servir e aplicar o padrão vetorial musical `doodle-background.svg` via diretório estático `public/` e estilização CSS.
- Destacar o botão de nova sessão na interface com rótulo explícito e melhoria de contraste.
- Adicionar micro-animações CSS3 fluidas para entrada de mensagens e execução de ferramentas sem exigir Node.js/npm.
- Expor rotas HTTP REST (`/api/chat`, `/api/catalog`, `/api/health`) no mesmo servidor FastAPI do Chainlit com documentação automática no `/docs`.

**Non-Goals:**
- Criação de pacotes complexos de componentes React com `npm build` (para preservar a reprodutibilidade pura em Python sem dependências de compilação JavaScript no ambiente do avaliador).
- Mecanismo de autenticação com login e senhas (o foco é a experiência de atendimento e avaliação do case).

## Decisions

### 1. Desativação Nativa de Uploads
- **Decisão:** Configurar `[features.spontaneous_file_upload].enabled = false` em `.chainlit/config.toml`.
- **Racional:** Elimina o ícone de anexo e a área de drag-and-drop nativamente pelo Chainlit, mantendo o campo de entrada focado exclusivamente em texto.

### 2. Wallpaper Doodle Musical e Custom CSS
- **Decisão:** Mover `doodle-background.svg` para `public/doodle-background.svg` e registrar `custom_css = "/public/custom.css"` no `.chainlit/config.toml`.
- **Racional:** O Chainlit serve a pasta `public/` na raiz do projeto como assets estáticos. O CSS aplica o padrão de repetição sutil em mosaico (`background-repeat: repeat; background-size: 400px;`) sobre o fundo clássico bege do WhatsApp (`#efeae2`).

### 3. Micro-animações em CSS3 Puro
- **Decisão:** Utilizar keyframes CSS (`@keyframes messageSlideUp`) aplicadas às classes de mensagem e indicadores de processamento.
- **Racional:** Oferece taxa de quadros a 60 FPS acelerada por hardware sem exigir `node_modules` ou builds com Vite/Webpack, mantendo a instalação do projeto 100% restrita a `pip install -r requirements.txt`.

### 4. Camada de API REST no FastAPI do Chainlit
- **Decisão:** Utilizar o FastAPI subjacente exposto por `cl.server.app` ou instanciar rotas de API em `src/app.py`.
- **Racional:** O avaliador ou sistemas terceiros (como Typebot, cURL ou Postman) podem consumir o mesmo agente conversacional por HTTP enviando `{ "message": "...", "session_id": "..." }` e recebendo respostas em JSON, com documentação Swagger acessível em `http://localhost:8000/docs`.

---

## Architecture Diagram

```text
+-----------------------------------------------------------------------------+
|                          CONSUMIDORES DA APLICAÇÃO                          |
|                                                                             |
|   [ Navegador Web ]                               [ Cliente HTTP / API ]    |
|   (Chainlit + CSS3 + Doodle SVG)                  (Postman, Typebot, cURL)  |
+-------------------+-----------------------------------------+---------------+
                    |                                         |
     (WebSocket / Socket.io)                              (HTTP REST)
                    |                                         |
                    v                                         v
+-----------------------------------------------------------------------------+
|                     SERVIDOR FASTAPI UNIFICADO (src/app.py)                 |
|                                                                             |
|  - Rota Web UI: GET /                                                       |
|  - Rota Assets: GET /public/custom.css, /public/doodle-background.svg       |
|  - Rota REST:   POST /api/chat                                              |
|  - Rota REST:   GET /api/catalog                                            |
|  - Rota REST:   GET /api/health                                             |
|  - Rota Docs:   GET /docs (Swagger OpenAPI)                                 |
+--------------------------------------+--------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                     LANGGRAPH ENGINE (src/agent/graph.py)                   |
|                      SQLite DB + Zero-Flake Policies                        |
+-----------------------------------------------------------------------------+
```

---

## Risks / Trade-offs

- **[Risco: Conflito de seletores CSS no Chainlit]**  
  *Mitigação:* Usar regras com especificidade adequada e seletores de container (`.main-chat-container`, `div[data-testid="chat-message"]`) testados diretamente no navegador.
- **[Risco: Bloqueio assíncrono na rota REST]**  
  *Mitigação:* Usar `run_agent_message` em executor assíncrono ou chamada assíncrona do LangGraph (`app.ainvoke`), garantindo alta concorrência.
