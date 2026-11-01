# Spec Delta: interface-atendimento

## Purpose

Define a experiência visual personalizada inspirada no WhatsApp Web para a Empório da Música, incluindo tema de fundo musical, controles de sessão acessíveis, micro-animações fluidas e endpoints REST para integração programática.

## ADDED Requirements

### Requirement: Desativação de Upload de Arquivos
A interface web de chat SHALL desabilitar o botão de anexo de arquivos, o seletor de arquivos e qualquer área de arraste e solte (drag-and-drop), mantendo a entrada de dados restrita a mensagens de texto.

#### Scenario: Ausência de controles de anexo
- **WHEN** o usuário acessa a interface web de conversação
- **THEN** nenhum ícone de clipe ou seletor de upload é exibido na caixa de composição de mensagem

### Requirement: Plano de Fundo Estilo WhatsApp com Tema Musical
A interface web SHALL exibir papel de parede com padrão repetido de doodle vetorial (SVG) com temática de instrumentos musicais em opacidade sutil sobre fundo bege claro (modo claro) ou grafite escuro (modo escuro).

#### Scenario: Renderização do papel de parede musical
- **WHEN** a tela de chat é carregada no navegador
- **THEN** o container principal exibe o padrão repetido do arquivo de imagem vetorial de doodle musical

### Requirement: Controle e Destaque de Nova Conversa
A interface SHALL fornecer um botão de reinício de conversa destacado na navegação, permitindo ao usuário iniciar uma nova sessão limpa com geração de novo identificador de atendimento.

#### Scenario: Reiniciar atendimento
- **WHEN** o usuário clica no botão "Nova Conversa"
- **THEN** a sessão atual é limpa e uma nova mensagem de boas-vindas da Empório da Música é apresentada

### Requirement: Micro-animações de Conversação
A interface SHALL aplicar transições animadas suaves em CSS3 na entrada de novas mensagens e no indicador de processamento das ferramentas da loja.

#### Scenario: Recepção de nova mensagem
- **WHEN** o assistente ou o usuário envia uma nova mensagem
- **THEN** o balão de mensagem aparece com transição fluida de elevação e opacidade

### Requirement: Endpoints REST para Integração
O servidor backend SHALL disponibilizar endpoints HTTP REST para consulta programática de catálogo, status do sistema e envio de mensagens para o agente conversacional.

#### Scenario: Envio de mensagem via API REST
- **WHEN** um cliente HTTP envia uma requisição POST para `/api/chat` com corpo contendo mensagem e identificador de sessão
- **THEN** o servidor retorna resposta JSON com a mensagem sintetizada pelo agente LangGraph e código 200 OK

#### Scenario: Consulta de catálogo via API REST
- **WHEN** um cliente HTTP envia uma requisição GET para `/api/catalog`
- **THEN** o servidor retorna a lista de instrumentos em formato JSON
