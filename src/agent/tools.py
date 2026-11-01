"""Ferramentas determinísticas expostas para o agente LangGraph."""

from typing import Optional
from langchain_core.tools import tool
from src.database.queries import search_products, get_order_details, get_active_promotions
from src.knowledge.policies import TopicoPolitica, consultar_politica


@tool
def consultar_catalogo(
    termo: Optional[str] = None,
    categoria: Optional[str] = None,
    preco_max: Optional[float] = None,
    apenas_em_estoque: bool = True,
) -> str:
    """Consulta instrumentos musicais no catálogo da Empório da Música.

    Args:
        termo: Nome, modelo ou palavra-chave do instrumento (ex: 'Yamaha', 'Takamine GD20', 'acústica').
        categoria: Categoria do instrumento (ex: 'Violões', 'Guitarras', 'Baixos', 'Teclados e Pianos', 'Baterias e Percussão', 'Ukuleles').
        preco_max: Limite máximo de preço em Reais (BRL).
        apenas_em_estoque: Se True, retorna apenas instrumentos com estoque disponível.
    """
    prods = search_products(
        term=termo,
        category=categoria,
        max_price=preco_max,
        only_in_stock=apenas_em_estoque,
        limit=8,
    )

    if not prods:
        criterios = []
        if termo:
            criterios.append(f"termo '{termo}'")
        if categoria:
            criterios.append(f"categoria '{categoria}'")
        if preco_max is not None:
            criterios.append(f"até R$ {preco_max:.2f}")
        criterios_str = ", ".join(criterios) if criterios else "os filtros informados"
        return f"Nenhum instrumento musical encontrado para {criterios_str}."

    linhas = [f"Encontrados {len(prods)} instrumento(s):"]
    for p in prods:
        specs_resumo = ""
        if isinstance(p.get("specs"), dict):
            specs_list = [f"{k}: {v}" for k, v in list(p["specs"].items())[:3]]
            specs_resumo = f" ({', '.join(specs_list)})"

        linhas.append(
            f"- [{p['product_id']}] {p['name']} | Categoria: {p.get('category_name', 'Geral')} | "
            f"Preço: R$ {p['price_brl']:.2f} | Estoque: {p['stock_quantity']} un.{specs_resumo}"
        )
    return "\n".join(linhas)


@tool
def consultar_pedido(identificador: str) -> str:
    """Consulta informações, status e rastreamento de um pedido na loja.

    Args:
        identificador: Número do pedido (ex: '8'), código de rastreamento (ex: 'BRAB1234567BR'), e-mail ou telefone do cliente.
    """
    pedido = get_order_details(identificador)
    if not pedido:
        return (
            f"Pedido com identificador '{identificador}' não foi localizado no sistema. "
            "Por favor, verifique se o número do pedido, código de rastreio ou e-mail/telefone está correto."
        )

    itens_str = ", ".join(
        [f"{it['quantity']}x {it['product_name']} (R$ {it['price_brl']:.2f})" for it in pedido.get("items", [])]
    )
    if not itens_str:
        itens_str = "Nenhum item listado"

    rastreio_str = pedido.get("tracking_code") or "Aguardando geração / Retirada presencial"
    previsao_str = pedido.get("estimated_delivery") or "Não informada"

    return (
        f"DETALHES DO PEDIDO #{pedido['order_id']}:\n"
        f"- Cliente: {pedido.get('customer_name')} ({pedido.get('customer_city')})\n"
        f"- Data da compra: {pedido.get('order_date')}\n"
        f"- Status atual: {pedido.get('status')}\n"
        f"- Valor total: R$ {pedido.get('total_brl', 0.0):.2f}\n"
        f"- Forma de pagamento: {pedido.get('payment_method')}\n"
        f"- Código de rastreamento: {rastreio_str}\n"
        f"- Previsão de entrega: {previsao_str}\n"
        f"- Itens do pedido: {itens_str}"
    )


@tool
def consultar_promocoes(produto_id: Optional[int] = None) -> str:
    """Consulta as promoções ativas da loja com percentual de desconto e preço promocional.

    Args:
        produto_id: ID opcional do produto para verificar se está em promoção ativa.
    """
    promos = get_active_promotions(product_id=produto_id)
    if not promos:
        if produto_id:
            return f"O produto #{produto_id} não possui nenhuma promoção ativa no momento."
        return "No momento não há promoções ativas no catálogo."

    linhas = ["PROMOÇÕES ATIVAS:"]
    for pr in promos:
        linhas.append(
            f"- [{pr['product_id']}] {pr['product_name']}: {pr['discount_percent']}% OFF "
            f"({pr.get('promo_description', 'Oferta')}) -> De R$ {pr['price_brl']:.2f} por R$ {pr['promotional_price']:.2f}"
        )
    linhas.append("\nNota: Promoções não são cumulativas com o desconto de 5% do PIX.")
    return "\n".join(linhas)


@tool
def consultar_politicas(topico: TopicoPolitica) -> str:
    """Consulta as regras e políticas oficiais da Empório da Música no manual interno.

    Use SEMPRE para dúvidas sobre:
    - horarios_funcionamento: horários da loja presencial e WhatsApp.
    - formas_pagamento: PIX, cartões de crédito/débito, boleto.
    - regras_parcelamento: parcelas mínimas e parcelamento até 12x.
    - trocas_devolucoes: prazo de 7 dias de arrependimento online, 30 dias de defeito, condições.
    - politica_frete: frete grátis Campo Grande (> R$ 500), taxa fixa (R$ 35), prazos dos Correios e Jadlog.
    - garantia: 90 dias legal e garantia de fábrica.
    - sobre_a_loja: endereço, história e dados da empresa.
    - lgpd_privacidade: proteção de dados do cliente.
    """
    return consultar_politica(topico)


ALL_TOOLS = [
    consultar_catalogo,
    consultar_pedido,
    consultar_promocoes,
    consultar_politicas,
]
