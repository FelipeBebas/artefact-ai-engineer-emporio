# Tasks

## 1. Localização e Placeholder em Português (pt-BR)

- [x] 1.1 Criar o arquivo `.chainlit/translations/pt-BR.json` com as traduções para a interface, incluindo `chat.input.placeholder` definido como "Digite sua mensagem aqui..." e ações de envio/anexo, e verificar validade da sintaxe JSON
- [x] 1.2 Atualizar `.chainlit/config.toml` para definir `language = "pt-BR"` e verificar carregamento da configuração

## 2. Avatar Estático da Empório da Música

- [x] 2.1 Criar o arquivo de imagem vetorial `public/avatars/emporio_da_musica.svg` com arte oficial da loja (tema musical com paleta escura e rosa) e verificar existência do arquivo
- [x] 2.2 Configurar `default_avatar_file_url = "/public/avatars/emporio_da_musica.svg"` em `.chainlit/config.toml` e verificar vinculação do avatar ao autor "Empório da Música"

## 3. Botões de Sugestão (Chat Starters) e Cenário de Rastreio

- [x] 3.1 Implementar a função decorada `@cl.set_starters` em `src/app.py` contendo os 5 cenários da especificação técnica (violões até R$ 1.000, endereço e horário de funcionamento, preço do Takamine GD20, devolução e rastreio do pedido #1 a caminho - Jadlog BR1001MS)
- [x] 3.2 Verificar e ajustar em `public/custom.css` a estilização dos starters para assegurar legibilidade e contraste elegantes no tema grafite escuro com auto-ocultação após envio

## 4. Testes Automatizados e Validação

- [x] 4.1 Adicionar testes unitários em `tests/test_app.py` para validar o registro e conteúdo dos starters do Chainlit e a configuração de idioma
- [x] 4.2 Executar a suíte de testes automatizados com `pytest tests/` e verificar que todos os testes passam com 100% de sucesso

## Workflow follow-up

- Arquivar a change após aprovação e implementação completa.
- Atualizar documentação e capturas de tela conforme necessário.
