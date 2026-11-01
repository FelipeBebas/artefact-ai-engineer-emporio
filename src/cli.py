"""Interface de Linha de Comando (CLI) para interação com o agente da Empório da Música."""

import argparse
import sys
import uuid
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from langchain_core.messages import HumanMessage
from src.agent.graph import get_agent_graph
from src.database.init_db import DB_PATH, init_database


def main():
    parser = argparse.ArgumentParser(description="CLI do Agente Empório da Música")
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Pergunta avulsa para execução em modo script/não-interativo.",
    )
    parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="ID opcional da sessão de conversa para retenção de memória.",
    )
    args = parser.parse_args()

    # Garante que o banco de dados esteja inicializado
    if not DB_PATH.exists():
        print("Banco de dados local não encontrado. Inicializando a partir dos CSVs...")
        init_database()

    app = get_agent_graph()
    session_id = args.session or f"cli_{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": session_id}}

    if args.query:
        # Modo avulso / script
        print(f"\n[Usuário]: {args.query}")
        result = app.invoke({"messages": [HumanMessage(content=args.query)]}, config=config)
        last_msg = result["messages"][-1]
        print(f"\n[Empório da Música]:\n{last_msg.content}\n")
        return

    # Modo interativo contínuo
    print("=" * 65)
    print("   🎸 EMPÓRIO DA MÚSICA — ASSISTENTE VIRTUAL DE ATENDIMENTO 🎸   ")
    print("=" * 65)
    print(f"Sessão ativa: {session_id}")
    print("Digite sua pergunta abaixo. Para encerrar, digite 'sair' ou 'exit'.\n")

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nAté mais! Um abraço e boas músicas da equipe Empório da Música! 🎶")
                break

            print("\n[Consultando sistemas e gerando resposta...]")
            result = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
            last_msg = result["messages"][-1]
            print(f"\nEmpório da Música:\n{last_msg.content}")

        except KeyboardInterrupt:
            print("\nSessão encerrada.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[Erro ao processar mensagem]: {e}")


if __name__ == "__main__":
    main()
