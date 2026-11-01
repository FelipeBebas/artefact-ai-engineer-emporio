# Exemplos de Interação com o Agente — Empório da Música

Este documento reúne **6 cenários de conversação** (5 obrigatórios do briefing + 1 bônus não-trivial) demonstrando o agente em situações variadas: consultas a banco de dados relacional em tempo real, aplicação determinística de políticas da loja (Zero-Flake) e aplicação estrita de guardrails de escopo.

---

## 📌 Índice de Cenários

1. [Cenário 1: Consulta de Catálogo com Filtro de Preço (Violões até R$ 1.000)](#cenário-1-consulta-de-catálogo-com-filtro-de-preço-violões-até-r-1000)
2. [Cenário 2: Informações Institucionais e Horário de Funcionamento](#cenário-2-informações-institucionais-e-horário-de-funcionamento)
3. [Cenário 3: Consulta Direta de Preço e Especificações (Takamine GD20)](#cenário-3-consulta-direta-de-preço-e-especificações-takamine-gd20)
4. [Cenário 4: Aplicação de Política de Devolução e Arrependimento](#cenário-4-aplicação-de-política-de-devolução-e-arrependimento)
5. [Cenário 5: Guardrail de Escopo — Bloqueio e Redirecionamento de Acessórios](#cenário-5-guardrail-de-escopo--bloqueio-e-redirecionamento-de-acessórios)
6. [Cenário 6 (Bônus Não-Trivial): Consulta de Pedido em Tempo Real com Rastreamento](#cenário-6-bônus-não-trivial-consulta-de-pedido-em-tempo-real-com-rastreamento)

---

### Cenário 1: Consulta de Catálogo com Filtro de Preço (Violões até R$ 1.000)

**Objetivo:** Demonstrar o agente usando a ferramenta `consultar_catalogo` com parâmetros de categoria (`Violões`) e teto orçamentário (`preco_max=1000.0`), formatando as opções com preços reais e tom acolhedor.

- **Cliente:**
  > *"Olá, boa tarde! Quais opções de violões vocês têm disponíveis custando até R$ 1000?"*

- **Ação Interna do Agente (Tool Call):**
  ```json
  consultar_catalogo(categoria="Violões", preco_max=1000.0, apenas_em_estoque=true)
  ```
- **Retorno da Tool:**
  ```text
  Encontrados 8 instrumento(s):
  - [83] Tagima Memphis AC-39 Nylon Natural | Preço: R$ 429.90 | Estoque: 15 un. (top: Linden)
  - [85] Rozini RC-104 Nylon Estudante | Preço: R$ 459.90 | Estoque: 10 un. (top: Spruce)
  - [89] Shelby SN-100 Folk Aço Preto | Preço: R$ 549.00 | Estoque: 5 un. (top: Linden)
  - [88] Giannini GF-1R Aço Folk Sunburst | Preço: R$ 579.90 | Estoque: 7 un. (top: Spruce)
  - [81] Yamaha C40 Nylon Natural | Preço: R$ 599.90 | Estoque: 12 un. (top: Spruce)
  - [84] Giannini GN-15 Nylon Cedr Natural | Preço: R$ 689.00 | Estoque: 6 un. (top: Cedro)
  - [87] Yamaha F310 Aço Natural | Preço: R$ 699.90 | Estoque: 14 un. (top: Spruce)
  - [86] Tagima Dallas Tuner Aço Natural | Preço: R$ 749.00 | Estoque: 9 un. (top: Spruce)
  ```

- **Resposta da Empório da Música:**
  > *"Boa tarde! Tudo bem por aí? Temos ótimas opções de violões nessa faixa de preço, tanto para quem curte cordas de nylon quanto para quem prefere aço! Dá uma olhada em alguns dos nossos destaques:*
  > 
  > 1. **Tagima Memphis AC-39 (Nylon):** R$ 429,90 — super confortável e leve para quem tá começando nos estudos;
  > 2. **Yamaha C40 (Nylon):** R$ 599,90 — um clássico mundial para estudantes, com tampo em Spruce e excelente projeção;
  > 3. **Yamaha F310 (Aço Folk):** R$ 699,90 — sonoridade encorpada e pegada firme;
  > 4. **Tagima Dallas Tuner (Aço):** R$ 749,00 — já vem com afinador embutido!
  > 
  > *Lembrando que no PIX você ainda garante **5% de desconto** à vista, ou pode parcelar em até 6x sem juros! Você tem preferência por cordas de nylon ou de aço?"*

---

### Cenário 2: Informações Institucionais e Horário de Funcionamento

**Objetivo:** Demonstrar o agente consultando a base determinística de políticas para esclarecer localização física e horários de atendimento sem alucinar dados da loja.

- **Cliente:**
  > *"Qual o endereço da loja e qual horário vocês abrem aos sábados?"*

- **Ações Internas do Agente (Tool Calls):**
  ```json
  consultar_politicas(topico="sobre_a_loja")
  consultar_politicas(topico="horarios_funcionamento")
  ```

- **Resposta da Empório da Música:**
  > *"Nossa loja física fica bem no Centro de Campo Grande/MS, na **Rua 14 de Maio, 3200 (CEP 79202-333)**!*
  > 
  > *Aos sábados, nosso atendimento — tanto presencial quanto aqui no WhatsApp — funciona das **09:00 às 13:00**. Durante a semana (segunda a sexta), abrimos das 09:00 às 18:00 (domingos e feriados estamos fechados).*
  > 
  > *Se quiser passar aqui para tomar um café e testar algum instrumento, será muito bem-vindo!"*

---

### Cenário 3: Consulta Direta de Preço e Especificações (Takamine GD20)

**Objetivo:** Demonstrar precisão numérica e retorno de especificações técnicas ricas armazenadas no JSON do banco de dados relacional.

- **Cliente:**
  > *"Quanto custa o Takamine GD20?"*

- **Ação Interna do Agente (Tool Call):**
  ```json
  consultar_catalogo(termo="Takamine GD20")
  ```
- **Retorno da Tool:**
  ```text
  Encontrados 1 instrumento(s):
  - [95] Takamine GD20 Dreadnought Natural | Categoria: Violões | Preço: R$ 2199.00 | Estoque: 5 un. (top: Cedro Sólido, back_sides: Sapele, neck: Mogno)
  ```

- **Resposta da Empório da Música:**
  > *"O **Takamine GD20 Dreadnought Natural** está saindo por **R$ 2.199,00**!*
  > 
  > *É um instrumento sensacional com tampo em **Cedro Sólido**, corpo em Sapele e braço em Mogno, que entrega uma acústica quente e encorpada típica dos violões folk da Takamine. Temos 5 unidades disponíveis no estoque!*
  > 
  > *No PIX à vista ele sai com 5% de desconto por **R$ 2.089,05**, ou você pode parcelar em até **12x de R$ 183,25 sem juros** no cartão de crédito. Quer que eu separe um para você?"*

---

### Cenário 4: Aplicação de Política de Devolução e Arrependimento

**Objetivo:** Demonstrar aplicação das regras do Código de Defesa do Consumidor e do manual interno da loja de forma sintetizada, empática e sem regurgitar texto jurídico frio.

- **Cliente:**
  > *"Me arrependi da minha compra pela internet, posso devolver meu pedido?"*

- **Ação Interna do Agente (Tool Call):**
  ```json
  consultar_politicas(topico="trocas_devolucoes")
  ```

- **Resposta da Empório da Música:**
  > *"Pode sim, com certeza! Pela nossa política e pelo Código de Defesa do Consumidor, para compras online você tem até **7 (sete) dias corridos** após o recebimento do produto para solicitar a devolução por arrependimento, sem qualquer necessidade de justificativa.*
  > 
  > *O frete de retorno é **100% por conta da loja** e o reembolso é feito na mesma forma de pagamento em até 10 dias úteis. A única exigência é que o instrumento esteja na embalagem original, sem sinais de uso e acompanhado de todos os manuais.*
  > 
  > *Se você tiver em mãos o número do seu pedido ou seu e-mail cadastrado, já posso te orientar no início desse processo!"*

---

### Cenário 5: Guardrail de Escopo — Bloqueio e Redirecionamento de Acessórios

**Objetivo:** Validar a diretriz crítica de negócio da Empório da Música: a loja vende **exclusivamente instrumentos musicais** e **não comercializa acessórios**. O agente deve bloquear a intenção, não inventar produtos e redirecionar com gentileza.

- **Cliente:**
  > *"Vocês têm encordoamento de aço 0.10 da D'Addario e um pedal de distorção para guitarra?"*

- **Raciocínio & Guardrail Interno:**
  - O sistema detecta termos de acessórios banidos do escopo da loja (`encordoamento`, `cordas`, `pedal de distorção`).
  - O agente **NÃO realiza consulta ao catálogo** para não gerar alucinação.
  - O agente aciona a regra de recusa cordial e redirecionamento.

- **Resposta da Empório da Música:**
  > *"Olá! Poxa, nós não trabalhamos com encordoamentos, pedais ou outros acessórios. Aqui na Empório da Música nosso foco é **100% exclusivo na venda de instrumentos musicais** (como as guitarras, violões, baixos e teclados).*
  > 
  > *Para cordas, pedais, cabos e palhetas aqui em Campo Grande, recomendo dar uma olhada nas lojas de acessórios musicais parceiras ali na região central da Rua 14 de Maio ou Calógeras.*
  > 
  > *Se você estiver procurando uma guitarra nova ou precisar de suporte com algum instrumento, conte com a gente!"*

---

### Cenário 6 (Bônus Não-Trivial): Consulta de Pedido em Tempo Real com Rastreamento

**Objetivo:** Demonstrar consulta a dados operacionais em tempo real cruzando pedido, cliente e código de rastreamento com status de entrega.

- **Cliente:**
  > *"Queria saber sobre o meu pedido, o código de rastreio que me passaram é BRAB1234567BR"*

- **Ação Interna do Agente (Tool Call):**
  ```json
  consultar_pedido(identificador="BRAB1234567BR")
  ```
- **Retorno da Tool:**
  ```text
  DETALHES DO PEDIDO #1:
  - Cliente: Pedro Henrique Oliveira (Campo Grande)
  - Data da compra: 2025-10-15
  - Status atual: delivered
  - Valor total: R$ 11499.00
  - Forma de pagamento: pix
  - Código de rastreamento: BRAB1234567BR
  - Previsão de entrega: 2025-10-25
  - Itens do pedido: 1x Martin D-28 Dreadnought Natural (R$ 11499.00)
  ```

- **Resposta da Empório da Música:**
  > *"Localizei seu pedido aqui, Pedro! 📦*
  > 
  > *O seu pedido **#1**, referente ao violão **Martin D-28 Dreadnought Natural**, consta no sistema como **entregue** (`delivered`) no dia 25/10/2025 aí em Campo Grande.*
  > 
  > *Chegou tudo certinho com o instrumento? Se precisar de qualquer orientação sobre regulagem, garantia de 90 dias ou cuidados com a madeira, é só falar!"*
