# 🎸 Empório da Música — AI Customer Service Agent
> **Technical Case — AI Engineer | Artefact**  
> Candidato: **Felipe Barros** (`felipe.barros.ia@gmail.com`)  
> LinkedIn: [linkedin.com/in/felipe-barros-ai](https://www.linkedin.com/in/felipe-barros-ai/)

---

### 📦 Repositório do Projeto no GitHub
Acesse o código-fonte completo, arquitetura, suíte de testes e documentação:  
👉 **[Abrir Repositório no GitHub (FelipeBebas/artefact-ai-engineer-emporio)](https://github.com/FelipeBebas/artefact-ai-engineer-emporio)**

---

### 🏛️ Arquitetura da Solução
- **Agente Conversacional**: LangGraph com StateGraph e `MemorySaver` para memória multi-turn determinística.
- **Tools Determinísticas**:
  1. `consultar_catalogo`: Busca de instrumentos com filtros rígidos de teto de preço, categoria e disponibilidade de estoque.
  2. `consultar_pedido`: Rastreamento de pedidos em tempo real por ID, código de rastreio (`BR...BR`), e-mail ou telefone.
  3. `consultar_promocoes`: Consulta de condições vigentes (PIX com 5% de desconto, até 12x sem juros).
- **Guardrails de Negócio**: Escopo exclusivo de instrumentos musicais (recusa cordial e redirecionamento de acessórios como cordas, palhetas, cabos e pedais).
- **Interface e Experiência**: Chainlit com tema WhatsApp Dark personalizado na identidade visual Rosa (`#831843`).
