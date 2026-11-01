"""Aplicação conversacional em Chainlit e API REST FastAPI para a Empório da Música."""

import asyncio
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# Garante que a raiz do projeto esteja no sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import chainlit as cl
from chainlit.server import app as fastapi_app
from fastapi import APIRouter, FastAPI, Query
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from src.agent.graph import get_agent_graph, run_agent_message
from src.database.init_db import DB_PATH, init_database
from src.database.queries import search_products, get_order_details, get_active_promotions


# ==============================================================================
# Modelos Pydantic para a API REST
# ==============================================================================

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensagem ou pergunta do cliente")
    session_id: Optional[str] = Field(default=None, description="Identificador único da sessão para memória multi-turn")


class ChatResponse(BaseModel):
    response: str = Field(..., description="Resposta sintetizada pelo agente com tom musical da loja")
    session_id: str = Field(..., description="Identificador da sessão utilizada")


class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "Empório da Música — AI Customer Service API"
    version: str = "2.0.0"


# ==============================================================================
# Rotas REST da API
# ==============================================================================

api_router = APIRouter(prefix="/api")


@api_router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Retorna o status de saúde e versão da aplicação."""
    return HealthResponse()


@api_router.post("/chat", response_model=ChatResponse, tags=["Agent"])
def chat_endpoint(payload: ChatRequest):
    """Envia uma mensagem ao agente conversacional LangGraph via API HTTP REST."""
    if not DB_PATH.exists():
        init_database()

    session_id = payload.session_id or f"api_{uuid.uuid4().hex[:8]}"
    agent_reply = run_agent_message(payload.message, thread_id=session_id)
    return ChatResponse(response=agent_reply, session_id=session_id)


@api_router.get("/catalog", tags=["Catalog"])
def catalog_endpoint(
    termo: Optional[str] = Query(None, description="Termo de busca no catálogo (modelo, madeira, fabricante)"),
    categoria: Optional[str] = Query(None, description="Nome da categoria (ex: Violões, Guitarras)"),
    preco_max: Optional[float] = Query(None, description="Limite superior de preço em BRL"),
    apenas_estoque: bool = Query(True, description="Filtrar apenas itens com estoque > 0"),
    limit: int = Query(10, description="Quantidade máxima de instrumentos retornados"),
):
    """Consulta diretamente o catálogo de instrumentos musicais em formato JSON."""
    if not DB_PATH.exists():
        init_database()

    return search_products(
        term=termo,
        category=categoria,
        max_price=preco_max,
        only_in_stock=apenas_estoque,
        limit=limit,
    )


# Aplicação FastAPI Standalone (para uvicorn ou TestClient)
api_app = FastAPI(
    title="Empório da Música — AI Customer Service API",
    description="API RESTful para integração com o agente de atendimento ao cliente",
    version="2.0.0",
)
api_app.include_router(api_router)


# Integração transparente no servidor FastAPI do Chainlit
def _register_into_chainlit(app_server):
    try:
        if hasattr(app_server, "routes") and app_server.routes:
            chainlit_router = getattr(app_server.routes[-1], "original_router", None)
            if chainlit_router:
                chainlit_router.include_router(api_router)
                api_routes = [r for r in chainlit_router.routes if getattr(r, "path", "").startswith("/api")]
                for r in api_routes:
                    chainlit_router.routes.remove(r)
                    chainlit_router.routes.insert(0, r)
                app_server.routes[-1]._effective_candidates_version = -1
    except Exception:
        pass


_register_into_chainlit(fastapi_app)


# ==============================================================================
# Handlers do Chainlit (Interface Web Conversacional)
# ==============================================================================

@cl.set_starters
async def set_starters():
    """Botões de sugestão rápida com os principais cenários de teste do assistente."""
    return [
        cl.Starter(
            label="🎸 Violões até R$ 1.000",
            message="Quais opções de violões disponíveis custando até R$1000?",
            icon="/public/avatars/emporio_da_musica.svg",
        ),
        cl.Starter(
            label="📍 Endereço e Horários",
            message="Qual o endereço e horário de funcionamento da loja?",
            icon="/public/avatars/emporio_da_musica.svg",
        ),
        cl.Starter(
            label="💰 Preço Takamine GD20",
            message="Quanto custa o Takamine GD20?",
            icon="/public/avatars/emporio_da_musica.svg",
        ),
        cl.Starter(
            label="🔄 Política de Devolução",
            message="Me arrependi da minha compra, posso devolver meu pedido?",
            icon="/public/avatars/emporio_da_musica.svg",
        ),
        cl.Starter(
            label="📦 Rastrear Pedido a Caminho",
            message="Gostaria de saber o status do meu pedido #8 (código BRJL5544332BR)",
            icon="/public/avatars/emporio_da_musica.svg",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    """Inicialização da sessão de atendimento no Chainlit com duas saudações sequenciais."""
    if not DB_PATH.exists():
        init_database()

    thread_id = f"session_{uuid.uuid4().hex[:8]}"
    cl.user_session.set("thread_id", thread_id)

    # 1ª Mensagem de Saudação
    primeira_msg = "🎸 Olá! Seja muito bem-vindo(a) à Empório da Música! 🎶"
    await cl.Message(content=primeira_msg).send()

    # Delay de 1 segundo entre cada mensagem (simulando digitação natural)
    await asyncio.sleep(1.0)

    # 2ª Mensagem com menu de opções e escopo da loja
    segunda_msg = (
        "Sou o assistente virtual da loja e estou aqui para te ajudar com tudo o que precisar:\n\n"
        "🔍 **Buscar instrumentos:** Guitarras, baixos, violões, teclados, baterias e mais\n"
        "📦 **Status de pedidos:** Acompanhamento de entregas e código de rastreamento\n"
        "💳 **Pagamento e frete:** Parcelamento em até 12x sem juros, desconto PIX e cálculo de entrega\n"
        "🔄 **Políticas e garantias:** Trocas, devoluções em até 7 dias e suporte técnico\n\n"
        "> *Nota: Trabalhamos exclusivamente com instrumentos musicais (não comercializamos cordas avulsas, palhetas, cabos, pedais ou amplificadores).*\n\n"
        "**Como posso ajudar o seu som hoje?**"
    )

    # Botões de sugestão interativos exibidos na interface (somem após a 1ª interação)
    actions = [
        cl.Action(
            name="quick_prompt",
            payload={"prompt": "Quais opções de violões disponíveis custando até R$1000?"},
            label="🎸 Violões até R$ 1.000",
        ),
        cl.Action(
            name="quick_prompt",
            payload={"prompt": "Qual o endereço e horário de funcionamento da loja?"},
            label="📍 Endereço e Horários",
        ),
        cl.Action(
            name="quick_prompt",
            payload={"prompt": "Quanto custa o Takamine GD20?"},
            label="💰 Preço Takamine GD20",
        ),
        cl.Action(
            name="quick_prompt",
            payload={"prompt": "Me arrependi da minha compra, posso devolver meu pedido?"},
            label="🔄 Política de Devolução",
        ),
        cl.Action(
            name="quick_prompt",
            payload={"prompt": "Gostaria de saber o status do meu pedido #8 (código BRJL5544332BR)"},
            label="📦 Rastrear Pedido a Caminho",
        ),
    ]

    welcome_msg = await cl.Message(content=segunda_msg, actions=actions).send()
    cl.user_session.set("welcome_msg", welcome_msg)


async def process_user_query(query_text: str):
    """Execução do agente LangGraph e exibição dos passos de ferramentas com fallback resiliente."""
    thread_id = cl.user_session.get("thread_id", "default_thread")
    config = {"configurable": {"thread_id": thread_id}}
    app = get_agent_graph()

    final_reply = ""
    try:
        inputs = {"messages": [HumanMessage(content=query_text)]}
        for chunk in app.stream(inputs, config=config, stream_mode="updates"):
            for node_name, node_output in chunk.items():
                if node_name == "agent":
                    ai_message = node_output["messages"][-1]
                    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
                        for call in ai_message.tool_calls:
                            try:
                                async with cl.Step(name=f"Consultando: {call['name']}", type="tool") as step:
                                    step.input = call.get("args", {})
                            except Exception:
                                pass
                    else:
                        final_reply = ai_message.content

                elif node_name == "tools":
                    tool_messages = node_output.get("messages", [])
                    for t_msg in tool_messages:
                        tool_name = getattr(t_msg, "name", "tool")
                        try:
                            async with cl.Step(name=f"Resultado: {tool_name}", type="tool") as step:
                                step.output = t_msg.content[:400] + ("..." if len(t_msg.content) > 400 else "")
                        except Exception:
                            pass

        if not final_reply:
            snapshot = app.get_state(config)
            if snapshot.values.get("messages"):
                final_reply = snapshot.values["messages"][-1].content
    except Exception as stream_err:
        # Fallback para invocação direta via thread segura
        try:
            final_reply = await asyncio.to_thread(run_agent_message, query_text, thread_id, app)
        except Exception as fallback_err:
            final_reply = (
                f"Desculpe, ocorreu uma instabilidade na comunicação com o assistente ({fallback_err}). "
                "Por favor, tente novamente em alguns instantes."
            )

    if not final_reply:
        final_reply = "Desculpe, ocorreu uma instabilidade ao gerar a resposta. Poderia repetir a pergunta?"

    await cl.Message(content=final_reply).send()


@cl.action_callback("quick_prompt")
async def on_quick_prompt(action: cl.Action):
    """Disparado quando o usuário clica em um botão de sugestão de teste."""
    welcome_msg = cl.user_session.get("welcome_msg")
    if welcome_msg:
        try:
            await welcome_msg.remove_actions()
        except Exception:
            pass
        cl.user_session.set("welcome_msg", None)

    prompt = action.payload.get("prompt", "")
    if prompt:
        # Envia como user_message autêntica no balão rosa da direita
        user_msg = cl.Message(content=prompt, author="User", type="user_message")
        await user_msg.send()
        await process_user_query(prompt)


@cl.on_message
async def on_message(message: cl.Message):
    """Processamento de mensagens digitadas pelo usuário no chat."""
    welcome_msg = cl.user_session.get("welcome_msg")
    if welcome_msg:
        try:
            await welcome_msg.remove_actions()
        except Exception:
            pass
        cl.user_session.set("welcome_msg", None)

    await process_user_query(message.content)
