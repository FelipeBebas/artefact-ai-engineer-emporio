# Spec Delta

## ADDED Requirements

### Requirement: Localização em Português do Brasil
A interface web de atendimento SHALL ser localizada integralmente em Português do Brasil (pt-BR), exibindo o texto de sugestão (placeholder) da caixa de entrada como "Digite sua mensagem aqui..." e traduzindo botões de ação e estados do chat.

#### Scenario: Visualização do placeholder traduzido
- **WHEN** o usuário carrega a interface de conversação
- **THEN** a caixa de entrada de texto exibe o placeholder "Digite sua mensagem aqui..." em português

#### Scenario: Controles e rótulos de envio traduzidos
- **WHEN** o usuário interage com o botão de envio ou ações de controle de conversa
- **THEN** os rótulos visuais e tooltips são apresentados no idioma Português do Brasil

### Requirement: Identidade Visual e Avatar Estático do Assistente
A interface SHALL exibir um avatar estático oficial com tema musical da Empório da Música nas mensagens emitidas pelo assistente, sem apresentar efeitos visuais de carregamento ou esqueleto cinza piscante.

#### Scenario: Exibição do avatar estático nas mensagens
- **WHEN** o assistente envia uma mensagem de resposta ou saudação inicial
- **THEN** a mensagem é acompanhada do avatar oficial estático da Empório da Música sem transição pulsante de esqueleto

### Requirement: Botões de Sugestão de Prompt (Starters) com Auto-ocultação
A interface SHALL apresentar botões interativos de sugestão de prompt (*chat starters*) cobrindo cenários do desafio técnico da loja, os quais devem desaparecer automaticamente assim que a primeira interação ou envio de mensagem ocorrer.

#### Scenario: Exibição inicial das sugestões
- **WHEN** uma nova sessão de atendimento é aberta
- **THEN** os botões de sugestão cobrindo catálogo (violões até R$ 1000), endereço, preço de instrumento, devoluções e status de pedido em trânsito são exibidos acima da caixa de mensagem

#### Scenario: Auto-ocultação após primeiro envio
- **WHEN** o usuário clica em um botão de sugestão ou envia sua primeira mensagem de texto
- **THEN** todos os botões de sugestão deixam de ser exibidos na tela, mantendo o histórico de mensagens limpo
