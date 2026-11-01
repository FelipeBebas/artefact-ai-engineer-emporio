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
    """Verifica se o config.toml do Chainlit define o idioma pt-BR, avatar e avatar_size aumentado em 25%."""
    config_path = Path(".chainlit/config.toml")
    assert config_path.exists()

    content = config_path.read_text(encoding="utf-8")
    assert 'language = "pt-BR"' in content
    assert 'default_avatar_file_url = "/public/avatars/emporio_da_musica.svg"' in content
    assert 'avatar_size = 25' in content


def test_pt_br_translation_file():
    """Valida o arquivo de tradução pt-BR e o placeholder traduzido para a caixa de mensagem."""
    translation_path = Path(".chainlit/translations/pt-BR.json")
    assert translation_path.exists()

    data = json.loads(translation_path.read_text(encoding="utf-8"))
    assert "chat" in data
    assert "input" in data["chat"]
    assert data["chat"]["input"]["placeholder"] == "Digite sua mensagem aqui..."


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
