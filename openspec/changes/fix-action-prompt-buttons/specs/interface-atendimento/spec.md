# Spec Delta

## ADDED Requirements

### Requirement: Botões de Sugestão de Prompt (Starters) com Auto-ocultação
A interface SHALL apresentar botões interativos de sugestão de prompt (*chat starters*) cobrindo cenários do desafio técnico da loja, os quais devem desaparecer automaticamente assim que a primeira interação ou envio de mensagem ocorrer, emitindo a pergunta selecionada como uma mensagem do usuário (`user_message`) e disparando a resposta do assistente.

#### Scenario: Exibição inicial das sugestões
- **WHEN** uma nova sessão de atendimento é aberta
- **THEN** os botões de sugestão cobrindo catálogo (violões até R$ 1000), endereço, preço de instrumento, devoluções e status de pedido em trânsito são exibidos acima da caixa de mensagem ou sob a saudação

#### Scenario: Auto-ocultação e disparo de mensagem do usuário após clique
- **WHEN** o usuário clica em um botão de sugestão de teste
- **THEN** todos os botões de sugestão deixam de ser exibidos na tela, a pergunta selecionada é exibida como mensagem do usuário no balão da direita (`user_message`) e o agente inicia a geração da resposta
