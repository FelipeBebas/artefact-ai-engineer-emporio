# Tasks: UI Polish and REST API Integration

## 1. Configurações de Interface e Bloqueio de Anexos

- [x] 1.1 Atualizar `.chainlit/config.toml` desativando `spontaneous_file_upload.enabled = false`, ajustando nome da aplicação para "Empório da Música" e ativando `custom_css = "/public/custom.css"`.
- [x] 1.2 Mover e posicionar o arquivo `doodle-background.svg` da raiz para `public/doodle-background.svg` e verificar integridade do asset.

## 2. Estilização WhatsApp & Micro-animações CSS3

- [x] 2.1 Criar `public/custom.css` com papel de parede doodle musical repetido sobre o fundo bege clássico do WhatsApp (`#efeae2`), ajuste de contraste para tema escuro e destaque evidente para o botão de "Nova Conversa".
- [x] 2.2 Implementar keyframes CSS3 de micro-animações fluidas para entrada suave dos balões de mensagens (*slide-up + fade-in*) e efeito pulsante durante execução de ferramentas.

## 3. Camada de Endpoints REST (FastAPI)

- [x] 3.1 Adicionar rotas REST no FastAPI em `src/app.py` (`POST /api/chat`, `GET /api/catalog`, `GET /api/health`) com schemas Pydantic estruturados e documentação Swagger no `/docs`.
- [x] 3.2 Desenvolver testes de API em `tests/test_api.py` utilizando `starlette.testclient.TestClient` para validar chamadas HTTP e respostas JSON, verificando com `pytest`.

## 4. Atualização da Documentação e Validação Final

- [x] 4.1 Atualizar o `README.md` com a seção de uso da API REST (exemplos cURL e Postman), Swagger interativo e novo guia estético.
- [x] 4.2 Executar a suíte completa de testes (`pytest tests/`) e validar conformidade de todos os componentes da Versão 2.

## Workflow follow-up

- Arquivar a mudança via OpenSpec (`/opsx-archive`) após conclusão e validação.
