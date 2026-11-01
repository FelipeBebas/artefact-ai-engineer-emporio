"""Consultas parametrizadas e seguras ao banco SQLite da Empório da Música."""

import json
import sqlite3
from typing import Any, Dict, List, Optional, Union
from src.config import DB_PATH


def get_connection(db_path=DB_PATH) -> sqlite3.Connection:
    """Retorna uma conexão configurada com row_factory = sqlite3.Row."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def search_products(
    term: Optional[str] = None,
    category: Optional[Union[str, int]] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    only_in_stock: bool = True,
    limit: int = 10,
    db_path=DB_PATH,
) -> List[Dict[str, Any]]:
    """Busca produtos no catálogo com filtros flexíveis."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    query = """
        SELECT p.product_id, p.price_brl, p.name, p.category_id, c.name as category_name,
               p.description, p.stock_quantity, p.status, p.specs
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.status = 'active'
    """
    params: List[Any] = []

    if only_in_stock:
        query += " AND p.stock_quantity > 0"

    if max_price is not None:
        query += " AND p.price_brl <= ?"
        params.append(float(max_price))

    if min_price is not None:
        query += " AND p.price_brl >= ?"
        params.append(float(min_price))

    if category is not None:
        if isinstance(category, int) or (isinstance(category, str) and category.isdigit()):
            query += " AND p.category_id = ?"
            params.append(int(category))
        else:
            query += " AND (c.name LIKE ? OR p.name LIKE ?)"
            params.append(f"%{category}%")
            params.append(f"%{category}%")

    if term:
        query += " AND (p.name LIKE ? OR p.description LIKE ? OR c.name LIKE ?)"
        wildcard = f"%{term}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY p.price_brl ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        item = dict(r)
        if item.get("specs"):
            try:
                item["specs"] = json.loads(item["specs"])
            except Exception:
                pass
        results.append(item)
    return results


def get_product_by_id(product_id: int, db_path=DB_PATH) -> Optional[Dict[str, Any]]:
    """Retorna detalhes de um produto específico por ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = ?
        """,
        (product_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    if item.get("specs"):
        try:
            item["specs"] = json.loads(item["specs"])
        except Exception:
            pass
    return item


def get_order_details(identifier: Union[str, int], db_path=DB_PATH) -> Optional[Dict[str, Any]]:
    """Consulta detalhes completos de um pedido por ID, código de rastreio, e-mail ou telefone."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    base_select = """
        SELECT o.order_id, o.order_date, o.status, o.total_brl, o.payment_method,
               o.tracking_code, o.estimated_delivery, o.notes,
               c.customer_id, c.name as customer_name, c.email as customer_email,
               c.phone as customer_phone, c.city as customer_city
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
    """

    ident_str = str(identifier).strip()
    order_row = None

    # 1. Se for numérico simples, busca diretamente pelo order_id
    if ident_str.isdigit():
        cursor.execute(f"{base_select} WHERE o.order_id = ? LIMIT 1", (int(ident_str),))
        order_row = cursor.fetchone()

    # 2. Se começa com BR e parece código de rastreio
    if not order_row and ident_str.upper().startswith("BR"):
        cursor.execute(f"{base_select} WHERE UPPER(o.tracking_code) = ? LIMIT 1", (ident_str.upper(),))
        order_row = cursor.fetchone()

    # 3. Se for e-mail
    if not order_row and "@" in ident_str:
        cursor.execute(f"{base_select} WHERE c.email LIKE ? ORDER BY o.order_date DESC LIMIT 1", (f"%{ident_str}%",))
        order_row = cursor.fetchone()

    # 4. Se for telefone
    if not order_row and any(char.isdigit() for char in ident_str) and len(ident_str) >= 8:
        # extrai dígitos
        digits = "".join(ch for ch in ident_str if ch.isdigit())
        cursor.execute(f"{base_select} WHERE replace(replace(replace(replace(c.phone, '(', ''), ')', ''), '-', ''), ' ', '') LIKE ? ORDER BY o.order_date DESC LIMIT 1", (f"%{digits}%",))
        order_row = cursor.fetchone()

    # 5. Fallback geral
    if not order_row:
        cursor.execute(
            f"""
            {base_select}
            WHERE o.tracking_code LIKE ?
               OR c.name LIKE ?
            ORDER BY o.order_date DESC
            LIMIT 1
            """,
            (f"%{ident_str}%", f"%{ident_str}%"),
        )
        order_row = cursor.fetchone()

    if not order_row:
        conn.close()
        return None

    order_dict = dict(order_row)
    order_id = order_dict["order_id"]

    # Busca os itens vinculados ao pedido
    cursor.execute(
        """
        SELECT oi.quantity, p.product_id, p.name as product_name, p.price_brl
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
        """,
        (order_id,),
    )
    items = [dict(r) for r in cursor.fetchall()]
    order_dict["items"] = items
    conn.close()
    return order_dict


def get_active_promotions(
    product_id: Optional[int] = None,
    produto_id: Optional[int] = None,
    db_path=DB_PATH,
) -> List[Dict[str, Any]]:
    """Consulta promoções ativas na loja."""
    target_id = product_id if product_id is not None else produto_id
    conn = get_connection(db_path)
    cursor = conn.cursor()

    query = """
        SELECT pr.promotion_id, pr.discount_percent, pr.description as promo_description,
               pr.is_active, p.product_id, p.name as product_name, p.price_brl,
               ROUND(p.price_brl * (1.0 - pr.discount_percent / 100.0), 2) as promotional_price
        FROM promotions pr
        JOIN products p ON pr.product_id = p.product_id
        WHERE pr.is_active = 1
    """
    params: List[Any] = []
    if target_id is not None:
        query += " AND pr.product_id = ?"
        params.append(target_id)

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
