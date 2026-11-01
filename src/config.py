"""Configurações globais e inicialização de provedores de LLM."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env a partir da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Caminhos do projeto
DATA_DIR = BASE_DIR / "data"
DB_PATH = Path(os.getenv("DB_PATH", str(BASE_DIR / "emporio.db")))

# Configurações do modelo
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Chaves de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


def get_llm():
    """Inicializa e retorna o cliente de LLM configurado.
    Permite inicialização com chave de fallback para evitar quebras em testes de schema.
    """
    if LLM_PROVIDER == "google" or "gemini" in LLM_MODEL.lower():
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = GOOGLE_API_KEY or os.getenv("GEMINI_API_KEY", "") or "dummy-google-key"
        return ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=api_key, temperature=0.1)
    elif LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        api_key = ANTHROPIC_API_KEY or "dummy-anthropic-key"
        return ChatAnthropic(model=LLM_MODEL, api_key=api_key, temperature=0.1)
    else:
        # Padrão: OpenAI
        from langchain_openai import ChatOpenAI
        api_key = OPENAI_API_KEY or "sk-dummy-key-for-test-initialization"
        return ChatOpenAI(model=LLM_MODEL, api_key=api_key, temperature=0.1)
