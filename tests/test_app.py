"""Testes para a aplicação Chainlit, Starters, Localização e Avatares."""

import asyncio
import json
from pathlib import Path
from src.app import set_starters
from src.database.queries import get_order_details


def test_set_starters_returns_challenge_scenarios():
    """Garante que a função set_starters retorna os 5 cenários definidos no case da vaga."""
    starters = asyncio.run(set_starters())
    assert isinstance(starters, list)
    assert len(starters) == 5

    labels = [s.label for s in starters]
    messages = [s.message for s in starters]

    # Verifica os 5 cenários do desafio
    assert any("Violões" in l for l in labels)
    assert any("Endereço" in l for l in labels)
    assert any("Takamine GD20" in l for l in labels)
    assert any("Devolução" in l for l in labels)
    assert any("Rastrear Pedido" in l for l in labels)

    # Verifica o pedido em trânsito com código BRJL5544332BR
    assert any("BRJL5544332BR" in m for m in messages)

    # Todos devem possuir ícone configurado
    for s in starters:
        assert s.icon == "/public/avatars/emporio_da_musica.svg"
        assert len(s.message) > 0


def test_chainlit_localization_config():
    """Verifica se o config.toml do Chainlit define o idioma pt-BR, avatar, tamanho e custom_js."""
    config_path = Path(".chainlit/config.toml")
    assert config_path.exists()

    content = config_path.read_text(encoding="utf-8")
    assert 'language = "pt-BR"' in content
    assert 'default_avatar_file_url = "/public/avatars/emporio_da_musica.svg"' in content
    assert 'avatar_size = 25' in content
    assert 'custom_js = "/public/custom.js"' in content


def test_pt_br_translation_file():
    """Valida o arquivo de tradução pt-BR, placeholder da caixa de texto e botão Readme."""
    translation_path = Path(".chainlit/translations/pt-BR.json")
    assert translation_path.exists()

    data = json.loads(translation_path.read_text(encoding="utf-8"))
    assert "chat" in data
    assert "input" in data["chat"]
    assert data["chat"]["input"]["placeholder"] == "Digite sua mensagem aqui..."
    assert data["navigation"]["header"]["readme"] == "Readme"


def test_custom_js_github_readme_redirect():
    """Valida que public/custom.js existe e intercepta o botão Readme com o repositório GitHub."""
    js_path = Path("public/custom.js")
    assert js_path.exists()
    content = js_path.read_text(encoding="utf-8")
    assert "readme-button" in content
    assert "https://github.com/FelipeBebas/artefact-ai-engineer-emporio" in content


def test_avatar_files_exist():
    """Garante que os arquivos de avatar SVG existem na pasta public/avatars/."""
    avatar_dir = Path("public/avatars")
    assert (avatar_dir / "emporio_da_musica.svg").exists()
    assert (avatar_dir / "default.svg").exists()

    svg_content = (avatar_dir / "emporio_da_musica.svg").read_text(encoding="utf-8")
    assert "<svg" in svg_content
    assert "</svg>" in svg_content


def test_order_tracking_data_exists():
    """Garante que o pedido #8 com status enviado (shipped) para teste do rastreio existe no banco."""
    order = get_order_details(8)
    assert order is not None
    assert order["tracking_code"] == "BRJL5544332BR"
    assert order["status"] == "shipped"
    assert order["customer_name"] == "Ana Carolina Ferreira"


def test_quick_prompt_user_message_type_and_author():
    """Valida que o callback de ação instancia a mensagem como user_message de autoria User."""
    import sys
    from unittest.mock import AsyncMock, patch
    import chainlit as cl
    from src.app import on_quick_prompt

    context_mod = sys.modules["chainlit.context"]

    action = cl.Action(
        name="quick_prompt",
        payload={"prompt": "Quanto custa o Takamine GD20?"},
        label="💰 Preço Takamine GD20",
    )

    captured_messages = []

    async def fake_send(self):
        captured_messages.append(self)
        return self

    async def run_scenario():
        context_mod.init_http_context()
        with patch.object(cl.Message, "send", fake_send), patch("src.app.process_user_query", new_callable=AsyncMock):
            await on_quick_prompt(action)

    asyncio.run(run_scenario())

    assert len(captured_messages) == 1
    user_msg = captured_messages[0]
    assert user_msg.content == "Quanto custa o Takamine GD20?"
    assert user_msg.author == "User"
    assert user_msg.type == "user_message"


def test_custom_css_step_separation_and_avatar_offset():
    """Garante que o CSS customizado aplica 2px de separação entre blocos de step e recuo no avatar."""
    css_path = Path("public/custom.css")
    assert css_path.exists()
    content = css_path.read_text(encoding="utf-8")

    # Separação de 2px nos steps
    assert ".step" in content
    assert "margin-top: 2px !important;" in content
    assert "margin-bottom: 2px !important;" in content

    # Recuo de 2px no avatar do sistema
    assert ".aspect-square.h-full.w-full.bg-transparent" in content
    assert "margin-left: 2px !important;" in content

    # Linhas laterais rosas (border-left) removidas para manter o design limpo
    assert "border-left: 3px" not in content
    assert "border-left: none !important;" in content



