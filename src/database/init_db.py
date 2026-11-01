"""Script de inicialização e ingestão dos arquivos CSV para o banco SQLite."""

import csv
import sqlite3
from pathlib import Path
from src.config import DATA_DIR, DB_PATH


def create_schema(conn: sqlite3.Connection):
    """Cria o esquema relacional no SQLite."""
    cursor = conn.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS promotions;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            price_brl REAL NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER,
            description TEXT,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            specs TEXT,
            created_at TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );

        CREATE TABLE promotions (
            promotion_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            discount_percent REAL NOT NULL,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            city TEXT
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT NOT NULL,
            total_brl REAL,
            payment_method TEXT,
            tracking_code TEXT,
            estimated_delivery TEXT,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            order_id INTEGER,
            quantity INTEGER NOT NULL,
            product_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )
    conn.commit()


def populate_db(conn: sqlite3.Connection, data_dir: Path) -> dict:
    """Carrega os arquivos CSV da pasta data/ para as tabelas SQLite."""
    cursor = conn.cursor()
    counts = {}

    # 1. Categories
    cat_file = data_dir / "desafio_tecnico_ai_eng - categories.csv"
    with open(cat_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(int(r["category_id"]), r["name"], r.get("description", "")) for r in reader]
        cursor.executemany("INSERT INTO categories VALUES (?, ?, ?)", rows)
        counts["categories"] = len(rows)

    # 2. Products
    prod_file = data_dir / "desafio_tecnico_ai_eng - products.csv"
    with open(prod_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(r["product_id"]),
                float(r["price_brl"]),
                r["name"],
                int(r["category_id"]),
                r.get("description", ""),
                int(r.get("stock_quantity", 0)),
                r.get("status", "active"),
                r.get("specs", ""),
                r.get("created_at", ""),
            )
            for r in reader
        ]
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        counts["products"] = len(rows)

    # 3. Promotions
    prom_file = data_dir / "desafio_tecnico_ai_eng - promotions.csv"
    with open(prom_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(r["promotion_id"]),
                int(r["product_id"]),
                float(r["discount_percent"]),
                r.get("description", ""),
                int(r.get("is_active", 0)),
            )
            for r in reader
        ]
        cursor.executemany("INSERT INTO promotions VALUES (?, ?, ?, ?, ?)", rows)
        counts["promotions"] = len(rows)

    # 4. Customers
    cust_file = data_dir / "desafio_tecnico_ai_eng - customers.csv"
    with open(cust_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (int(r["customer_id"]), r["name"], r.get("phone", ""), r.get("email", ""), r.get("city", ""))
            for r in reader
        ]
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", rows)
        counts["customers"] = len(rows)

    # 5. Orders
    ord_file = data_dir / "desafio_tecnico_ai_eng - orders.csv"
    with open(ord_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(r["order_id"]),
                int(r["customer_id"]),
                r.get("order_date", ""),
                r["status"],
                float(r["total_brl"]) if r.get("total_brl") else None,
                r.get("payment_method", ""),
                r.get("tracking_code", ""),
                r.get("estimated_delivery", ""),
                r.get("notes", ""),
            )
            for r in reader
        ]
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        counts["orders"] = len(rows)

    # 6. Order Items
    item_file = data_dir / "desafio_tecnico_ai_eng - order_items.csv"
    with open(item_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (int(r["order_id"]), int(r["quantity"]), int(r["product_id"]))
            for r in reader
        ]
        cursor.executemany("INSERT INTO order_items VALUES (?, ?, ?)", rows)
        counts["order_items"] = len(rows)

    conn.commit()
    return counts


def init_database(db_path: Path = DB_PATH, data_dir: Path = DATA_DIR) -> dict:
    """Executa a criação do banco de dados e retorna os registros inseridos."""
    conn = sqlite3.connect(db_path)
    try:
        create_schema(conn)
        counts = populate_db(conn, data_dir)
        return counts
    finally:
        conn.close()


if __name__ == "__main__":
    print(f"Inicializando banco de dados em: {DB_PATH}")
    inserted = init_database()
    print("Banco de dados inicializado com sucesso!")
    for table, count in inserted.items():
        print(f" - {table}: {count} registros")
