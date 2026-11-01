# Proposal

## Why

A interface de atendimento da Empório da Música necessita de refinamentos finais de usabilidade e identidade visual para proporcionar uma experiência de demonstração fluida e em conformidade estrita com o idioma do público-alvo (Português do Brasil). A caixa de entrada de texto atualmente exibe o texto padrão em inglês (*"Type your message here..."*), o avatar do sistema apresenta um efeito pulsante cinza temporário em vez da identidade da marca, e os avaliadores técnicos precisam de atalhos rápidos (botões de sugestão) para testar os cenários-chave descritos no desafio técnico da vaga (catálogo, endereço, preço, política de devolução e consulta de pedido a caminho em tempo real).

## What Changes

- **Tradução completa da interface para Português (pt-BR)**: Adição do arquivo de tradução `.chainlit/translations/pt-BR.json` e configuração de `language = "pt-BR"` em `.chainlit/config.toml`, garantindo que o placeholder da caixa de mensagem passe a ser *"Digite sua mensagem aqui..."* e os botões auxiliares fiquem em português.
- **Avatar estático da Empório da Música**: Criação e configuração de um avatar estático oficial em formato SVG com tema musical/identidade visual da marca em `public/avatars/emporio_da_musica.svg`, eliminando o esqueleto animado piscante cinza.
- **Botões de sugestão interativos (*Chat Starters*)**: Implementação via `@cl.set_starters` no Chainlit contendo 5 opções clicáveis representando os cenários exigidos na especificação do case:
  1. Consulta de catálogo com filtro de preço: *"Quais opções de violões disponíveis custando até R$1000?"*
  2. Informações gerais e endereço: *"Qual o endereço e horário de funcionamento da loja?"*
  3. Consulta de preço específico: *"Quanto custa o Takamine GD20?"*
  4. Aplicação de políticas de troca e devolução: *"Me arrependi da minha compra, posso devolver meu pedido?"*
  5. Consulta de status de pedido em tempo real: *"Gostaria de saber o status do meu pedido #1 (código BR1001MS)"* (apontando para pedido existente em trânsito via Jadlog).
- **Auto-ocultação dos Starters**: Os botões de sugestão desaparecem automaticamente da tela assim que o usuário clica em um deles ou envia a sua primeira mensagem.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade isolada necessária)*

### Modified Capabilities
- `interface-atendimento`: Adiciona requisitos de localização integral em pt-BR (incluindo placeholder da caixa de entrada), avatar estático oficial da loja e botões de sugestão iniciais (*starters*) com comportamento de auto-ocultação após envio.

## Impact

- **Código Frontend / Configuração**: Arquivos `.chainlit/config.toml`, criação de `.chainlit/translations/pt-BR.json`, criação de `public/avatars/emporio_da_musica.svg`, e inclusão do hook `@cl.set_starters` em `src/app.py`.
- **Dependências / APIs**: Nenhuma nova dependência externa necessária (recursos nativos do Chainlit 2.x).
- **Testes**: Atualização e expansão da suíte de testes em `tests/test_app.py` para validar a presença e o registro dos starters e a correta configuração de localização.
