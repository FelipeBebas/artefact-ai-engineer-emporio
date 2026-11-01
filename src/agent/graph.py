"""Grafo de orquestração do agente conversacional construído com LangGraph."""

from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from src.agent.prompts import SYSTEM_PROMPT
from src.agent.tools import ALL_TOOLS
from src.config import get_llm

_agent_graph_instance = None


def create_agent(checkpointer: Optional[Any] = None, custom_llm: Optional[Any] = None):
    """Cria e compila o StateGraph do agente com suporte a ferramentas e memória."""
    llm = custom_llm if custom_llm is not None else get_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    def agent_node(state: MessagesState) -> Dict[str, List[BaseMessage]]:
        messages = list(state["messages"])
        # Garante que o SystemMessage esteja presente no topo do histórico
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        elif isinstance(messages[0], SystemMessage):
            # Mantém atualizado o prompt do sistema
            messages[0] = SystemMessage(content=SYSTEM_PROMPT)

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(ALL_TOOLS)

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    memory = checkpointer if checkpointer is not None else MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app


def get_agent_graph():
    """Retorna a instância singleton do grafo compilado (lazy initialization)."""
    global _agent_graph_instance
    if _agent_graph_instance is None:
        _agent_graph_instance = create_agent()
    return _agent_graph_instance


def run_agent_message(
    user_text: str,
    thread_id: str = "default_session",
    graph: Optional[Any] = None,
) -> str:
    """Função utilitária síncrona para envio de mensagem e retorno da resposta final."""
    app = graph or get_agent_graph()
    config = {"configurable": {"thread_id": thread_id}}

    inputs = {"messages": [HumanMessage(content=user_text)]}
    final_output = app.invoke(inputs, config=config)

    # Retorna o conteúdo da última mensagem gerada
    last_message = final_output["messages"][-1]
    return last_message.content
