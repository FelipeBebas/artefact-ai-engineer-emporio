"""Testes unitários para o banco de dados e consultas."""

import pytest
from src.database.queries import (
    search_products,
    get_product_by_id,
    get_order_details,
    get_active_promotions,
)


def test_search_products_by_term():
    results = search_products(term="Yamaha")
    assert len(results) > 0
    for prod in results:
        assert "yamaha" in prod["name"].lower() or "yamaha" in prod.get("description", "").lower()


def test_search_violao_under_1000():
    results = search_products(category="Violões", max_price=1000.0)
    assert len(results) > 0
    for prod in results:
        assert prod["price_brl"] <= 1000.0
        assert prod["category_name"] == "Violões"


def test_product_specs_parsing():
    results = search_products(term="C40")
    assert len(results) > 0
    c40 = results[0]
    assert isinstance(c40["specs"], dict)
    assert "top" in c40["specs"]


def test_get_product_by_id():
    prod = get_product_by_id(81)
    assert prod is not None
    assert prod["name"] == "Yamaha C40 Nylon Natural"


def test_get_order_details_by_id_and_tracking():
    order_by_id = get_order_details(1)
    assert order_by_id is not None
    assert order_by_id["tracking_code"] == "BRAB1234567BR"
    assert len(order_by_id["items"]) > 0

    order_by_tracking = get_order_details("BRAB1234567BR")
    assert order_by_tracking is not None
    assert order_by_tracking["order_id"] == 1


def test_get_active_promotions():
    promos = get_active_promotions()
    assert len(promos) > 0
    for promo in promos:
        assert promo["is_active"] == 1
        assert "promotional_price" in promo
        assert promo["promotional_price"] < promo["price_brl"]
