# Proposal: UI Polish and REST API Integration

## Why

A versão 1 do agente atendeu com êxito a todos os requisitos lógicos do desafio. Para a versão 2, a experiência do usuário precisa evoluir de um chat genérico para uma simulação fiel do WhatsApp Web com identidade visual da Empório da Música: eliminando uploads desnecessários de imagens, aplicando o papel de parede doodle com temática musical (`doodle-background.svg`), conferindo destaque ao botão de nova sessão, adicionando micro-animações fluidas e disponibilizando endpoints REST para integração externa.

## What Changes

- **Desativação de Upload de Arquivos/Imagens:** Bloqueio completo de upload espontâneo e arrastar-e-soltar (drag-and-drop) via `.chainlit/config.toml`, garantindo foco exclusivo em mensagens de texto.
- **Fundo Personalizado WhatsApp com Tema Musical:** Aplicação do arquivo SVG `doodle-background.svg` em repetição sutil com cores temáticas da loja no `public/custom.css`.
- **Destaque do Botão "Nova Conversa":** Melhoria visual e de acessibilidade no botão de reset/nova sessão da barra lateral com rótulo explícito e tooltip.
- **Micro-animações CSS3:** Animações fluidas de entrada de balões de mensagens (*fade-in + slide-up*) e efeito pulsante durante o raciocínio das ferramentas.
- **Camada de API REST (FastAPI):** Exposição de endpoints HTTP no servidor Chainlit (`POST /api/chat`, `GET /api/catalog`, `GET /api/health`, `/docs`) para testes automatizados e integração com ferramentas terceiras (ex: Typebot, Postman ou cURL).

## Capabilities

### New Capabilities
- `interface-atendimento`: Interface gráfica web especializada estilo WhatsApp Web (doodle wallpaper musical, bloqueio de anexos, animações fluidas e controle de sessão) complementada por API REST para consumo programático do agente.

### Modified Capabilities
<!-- Nenhuma alteração nos requisitos de negócio do atendimento-emporio. -->

## Impact

- **Frontend/UI:** Criação da pasta `public/` contendo `custom.css` e o asset `doodle-background.svg`; atualização de `.chainlit/config.toml`.
- **Backend:** Atualização de `src/app.py` para registrar rotas REST no FastAPI interno do Chainlit.
- **Documentação:** Atualização do `README.md` com detalhes dos novos endpoints REST e guia visual.
