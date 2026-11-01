# Design

## Context

A interface atual da Empório da Música é executada sobre Chainlit 2.x com backend em LangGraph e banco SQLite (`emporio.db`).
Para motivação e escopo detalhado, veja `proposal.md` e a delta spec `specs/interface-atendimento/spec.md`.

## Goals / Non-Goals

**Goals:**
- Configurar localização declarativa em Português do Brasil (`pt-BR`) traduzindo nativamente o placeholder *"Digite sua mensagem aqui..."* e controles do chat sem hacks de Javascript.
- Estabelecer um avatar estático oficial em SVG com gradiente escuro e rosa da marca, servido nativamente pelo Chainlit para remover o efeito de carregamento pulsante.
- Implementar botões de sugestão (*Chat Starters*) nativos que apresentem as 5 perguntas de demonstração do desafio e desapareçam automaticamente após o envio da primeira mensagem.
- Integrar a demonstração de consulta de pedido com um registro real em trânsito (`BR1001MS`, Jadlog, Pedido #1) já existente em `emporio.db`.
- Garantir que todos os testes automatizados existentes continuem passando e novos testes cubram os starters e a localização.

**Non-Goals:**
- Não reescrever componentes internos do frontend em React ou compilar um bundle customizado.
- Não alterar a lógica de orquestração do LangGraph ou ferramentas existentes de busca e pedidos.
- Não modificar o esquema do banco de dados SQLite.

## Decisions

### 1. Localização via Arquivo de Tradução Nativo do Chainlit
- **Decisão**: Criar `.chainlit/translations/pt-BR.json` e definir `language = "pt-BR"` em `.chainlit/config.toml`.
- **Justificativa**: O Chainlit 2.x suporta i18n nativamente através de diretórios de tradução locais em `.chainlit/translations/`. Quando `language` está configurado, o Chainlit injeta as strings traduzidas no frontend React durante o handshake inicial, preenchendo o placeholder `chat.input.placeholder` de forma limpa e sem atraso de renderização.
- **Alternativas consideradas**:
  - *Injeção via CSS (`content:` ou `::placeholder`)*: Frágil e não altera o atributo HTML `placeholder` real.
  - *Script JS no DOM*: Inconsistente com re-renderizações do React e sujeito a flickering.

### 2. Avatar Estático da Loja via `public/avatars/`
- **Decisão**: Criar `public/avatars/emporio_da_musica.svg` com desenho vetorial de instrumento musical/marca e referenciá-lo em `default_avatar_file_url` no `.chainlit/config.toml`.
- **Justificativa**: O endpoint `/avatars/{avatar_id}` do Chainlit busca arquivos em `public/avatars/` sanitizando o nome da UI (`"Empório da Música"` -> `emporio_da_musica`). Na ausência desse arquivo, o Chainlit renderiza um componente de esqueleto (`Skeleton`) com animação CSS `pulse`. Disponibilizar o arquivo estático resolve a raiz do problema.
- **Alternativas consideradas**:
  - *Ocultar avatar via CSS*: Removeria a imagem do assistente em vez de exibir a marca da loja.

### 3. Sugestões de Prompt via Hook `@cl.set_starters`
- **Decisão**: Utilizar a função decorada `@cl.set_starters` em `src/app.py`, retornando uma lista de objetos `cl.Starter`.
- **Justificativa**: É a API oficial do Chainlit para sugestões iniciais. O Chainlit cuida nativamente de renderizar os cards clicáveis e esconde-os assim que uma mensagem é submetida na sessão.
- **Cenários Definidos**:
  1. `cl.Starter(label="🎸 Violões até R$ 1.000", message="Quais opções de violões disponíveis custando até R$1000?")`
  2. `cl.Starter(label="📍 Endereço e Horários", message="Qual o endereço e horário de funcionamento da loja?")`
  3. `cl.Starter(label="💰 Preço Takamine GD20", message="Quanto custa o Takamine GD20?")`
  4. `cl.Starter(label="🔄 Política de Devolução", message="Me arrependi da minha compra, posso devolver meu pedido?")`
  5. `cl.Starter(label="📦 Rastrear Pedido a Caminho", message="Gostaria de saber o status do meu pedido #1 (código BR1001MS)")`

## Risks / Trade-offs

- **[Risco] Cache do navegador com traduções antigas** → Mitigação: O Chainlit versiona os assets e a chave `language = "pt-BR"` é lida na inicialização do servidor.
- **[Risco] Sobrescrita de estilo nos cards de starter pelo CSS dark mode customizado** → Mitigação: Testar visualmente e, se necessário, garantir contraste do texto dos botões no tema grafite escuro em `public/custom.css`.
