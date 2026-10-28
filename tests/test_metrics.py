import pytest

from src.database import get_connection, initialize_database
from src.metrics import get_kpis, get_top_products


@pytest.fixture
def sales_database(tmp_path, monkeypatch):
    import src.database as database_module

    monkeypatch.setattr(
        database_module, "DATABASE_FILE", tmp_path / "test_sales.db"
    )
    monkeypatch.setattr(
        database_module, "SCHEMA_FILE",
        database_module.SCHEMA_FILE,
    )

    initialize_database()

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO customers
            VALUES (1, 'Customer A', 'Southeast', '2024-01-01')
        """)
        connection.execute("""
            INSERT INTO products
            VALUES (1, 'Product A', 'Office', 100.0)
        """)
        connection.execute("""
            INSERT INTO orders
            VALUES (
                1, 1, 1, '2024-01-10', 2, 100.0, 'completed'
            )
        """)
        connection.execute("""
            INSERT INTO orders
            VALUES (
                2, 1, 1, '2024-01-11', 1, 100.0, 'pending'
            )
        """)

    return True


def test_kpis_calculate_completed_sales_only(sales_database):
    result = get_kpis()

    assert result["total_orders"] == 1
    assert result["revenue"] == 200.0
    assert result["units_sold"] == 2
    assert result["average_order_value"] == 200.0


def test_top_products_returns_units_and_revenue(sales_database):
    result = get_top_products(limit=5)

    assert len(result) == 1
    assert result[0]["product_name"] == "Product A"
    assert result[0]["units_sold"] == 2
    assert result[0]["revenue"] == 200.0


def test_top_products_rejects_invalid_limit():
    with pytest.raises(ValueError):
        get_top_products(limit=0)