"""Testes unitários para o motor Zero-Flake de políticas da loja."""

from src.knowledge.policies import (
    TopicoPolitica,
    consultar_politica,
    resolver_topico,
    POLITICAS_MANUAL,
)


def test_enum_coverage():
    """Garante que todos os tópicos do Enum têm texto cadastrado no manual."""
    for topico in TopicoPolitica:
        assert topico in POLITICAS_MANUAL
        assert len(POLITICAS_MANUAL[topico]) > 50


def test_consultar_politica_by_enum():
    texto = consultar_politica(TopicoPolitica.TROCAS_DEVOLUCOES)
    assert "7 (sete) dias corridos" in texto
    assert "Direito de Arrependimento" in texto


def test_consultar_frete_campo_grande():
    texto = consultar_politica(TopicoPolitica.POLITICA_FRETE)
    assert "500,00" in texto
    assert "35,00" in texto
    assert "motoboy" in texto


def test_consultar_garantia():
    texto = consultar_politica(TopicoPolitica.GARANTIA)
    assert "90 (noventa) dias" in texto
    assert "Código de Defesa do Consumidor" in texto


def test_resolver_topico_synonyms():
    assert resolver_topico("arrependi") == TopicoPolitica.TROCAS_DEVOLUCOES
    assert resolver_topico("onde fica a loja?") == TopicoPolitica.SOBRE_A_LOJA
    assert resolver_topico("como funciona o frete") == TopicoPolitica.POLITICA_FRETE
    assert resolver_topico("posso parcelar em 10x?") == TopicoPolitica.REGRAS_PARCELAMENTO


def test_consultar_politica_fallback():
    texto = consultar_politica("topico_completamente_inexistente_12345")
    assert "não localizada" in texto
    assert "Tópicos disponíveis" in texto
