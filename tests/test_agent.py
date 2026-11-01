"""Testes de integração para o agente LangGraph e ferramentas."""

import os
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from src.agent.tools import ALL_TOOLS, consultar_catalogo, consultar_pedido, consultar_politicas, consultar_promocoes
from src.agent.graph import create_agent
from src.knowledge.policies import TopicoPolitica


def test_tools_count_and_naming():
    """Garante que as 4 ferramentas estão registradas e com nomes corretos."""
    assert len(ALL_TOOLS) == 4
    nomes = [t.name for t in ALL_TOOLS]
    assert "consultar_catalogo" in nomes
    assert "consultar_pedido" in nomes
    assert "consultar_promocoes" in nomes
    assert "consultar_politicas" in nomes


def test_consultar_catalogo_tool_execution():
    """Valida retorno formatado da tool de catálogo."""
    res = consultar_catalogo.invoke({"categoria": "Violões", "preco_max": 1000.0})
    assert "Encontrados" in res
    assert "Violões" in res
    assert "R$" in res


def test_consultar_pedido_tool_execution():
    """Valida retorno formatado da tool de pedidos."""
    res = consultar_pedido.invoke({"identificador": "1"})
    assert "DETALHES DO PEDIDO #1" in res
    assert "BRAB1234567BR" in res


def test_consultar_promocoes_tool_execution():
    """Valida retorno formatado da tool de promoções."""
    res = consultar_promocoes.invoke({})
    assert "PROMOÇÕES ATIVAS" in res
    assert "% OFF" in res


def test_consultar_politicas_tool_execution():
    """Valida retorno da tool de políticas usando Enum."""
    res = consultar_politicas.invoke({"topico": TopicoPolitica.TROCAS_DEVOLUCOES})
    assert "7 (sete) dias" in res
    assert "Direito de Arrependimento" in res


def test_agent_graph_structure():
    """Valida a compilação e nós do StateGraph do LangGraph."""
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm

    with patch("src.agent.graph.get_llm", return_value=mock_llm):
        app = create_agent(checkpointer=MemorySaver())
        # Verifica se os nós principais estão registrados no grafo
        assert "agent" in app.nodes
        assert "tools" in app.nodes


def test_agent_multiturn_memory_retention():
    """Valida retenção de histórico em múltiplas mensagens na mesma thread."""
    mock_llm = MagicMock()
    # Simula resposta do LLM na primeira e segunda chamada
    mock_llm.invoke.side_effect = [
        AIMessage(content="Olá! Sou o assistente da Empório da Música. Como posso te ajudar hoje?"),
        AIMessage(content="Temos excelentes violões abaixo de R$ 1.000,00!"),
    ]
    mock_llm.bind_tools.return_value = mock_llm

    with patch("src.agent.graph.get_llm", return_value=mock_llm):
        app = create_agent(checkpointer=MemorySaver())
        thread_config = {"configurable": {"thread_id": "test_session_123"}}

        # Turno 1
        out1 = app.invoke({"messages": [HumanMessage(content="Olá, boa tarde!")]}, config=thread_config)
        assert len(out1["messages"]) >= 2

        # Turno 2
        out2 = app.invoke({"messages": [HumanMessage(content="Quais violões vocês têm?")]}, config=thread_config)
        # O estado deve conter o histórico acumulado
        assert len(out2["messages"]) >= 4
