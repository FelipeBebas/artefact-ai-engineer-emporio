"""Aplicação conversacional em Chainlit para a Empório da Música."""

import sys
import uuid
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent.graph import get_agent_graph
from src.database.init_db import DB_PATH, init_database


@cl.on_chat_start
async def on_chat_start():
    """Inicialização da sessão de atendimento no Chainlit."""
    # Garante inicialização do banco SQLite se não existir
    if not DB_PATH.exists():
        init_database()

    # Cada usuário recebe um thread_id único para persistência de memória no LangGraph
    thread_id = f"session_{uuid.uuid4().hex[:8]}"
    cl.user_session.set("thread_id", thread_id)

    boas_vindas = (
        "🎸 **Olá! Seja muito bem-vindo(a) à Empório da Música!** 🎶\n\n"
        "Sou o assistente virtual da loja e estou aqui para te ajudar com tudo o que precisar:\n"
        "- 🔍 **Buscar instrumentos:** Guitarras, baixos, violões, teclados, baterias e mais\n"
        "- 📦 **Status de pedidos:** Acompanhamento de entregas e código de rastreamento\n"
        "- 💳 **Pagamento e frete:** Parcelamento em até 12x sem juros, desconto PIX e cálculo de entrega\n"
        "- 🔄 **Políticas e garantias:** Trocas, devoluções em até 7 dias e suporte técnico\n\n"
        "> *Nota: Trabalhamos exclusivamente com instrumentos musicais (não comercializamos cordas avulsas, palhetas, cabos, pedais ou amplificadores).*\n\n"
        "**Como posso ajudar o seu som hoje?**"
    )

    await cl.Message(content=boas_vindas).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Processamento de mensagens dos clientes com exibição transparente dos passos do agente."""
    thread_id = cl.user_session.get("thread_id", "default_thread")
    config = {"configurable": {"thread_id": thread_id}}
    app = get_agent_graph()

    inputs = {"messages": [HumanMessage(content=message.content)]}

    final_reply = ""
    # Executa o grafo e acompanha chamadas de tools e nós
    for chunk in app.stream(inputs, config=config, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            if node_name == "agent":
                ai_message = node_output["messages"][-1]
                if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
                    for call in ai_message.tool_calls:
                        async with cl.Step(name=f"Consultando: {call['name']}", type="tool") as step:
                            step.input = call.get("args", {})
                else:
                    final_reply = ai_message.content

            elif node_name == "tools":
                tool_messages = node_output.get("messages", [])
                for t_msg in tool_messages:
                    tool_name = getattr(t_msg, "name", "tool")
                    async with cl.Step(name=f"Resultado: {tool_name}", type="tool") as step:
                        step.output = t_msg.content[:400] + ("..." if len(t_msg.content) > 400 else "")

    if not final_reply:
        # Fallback para capturar a última mensagem do estado
        snapshot = app.get_state(config)
        if snapshot.values.get("messages"):
            final_reply = snapshot.values["messages"][-1].content
        else:
            final_reply = "Desculpe, ocorreu uma instabilidade ao gerar a resposta. Poderia repetir a pergunta?"

    await cl.Message(content=final_reply).send()
