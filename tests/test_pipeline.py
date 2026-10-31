
import json
import sqlite3

import pandas as pd

import src.config as config_module
import src.database as database_module
import src.pipeline as pipeline_module


def test_pipeline_cleans_and_loads_data(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    reports_dir = tmp_path / "reports"
    database_dir = tmp_path / "database"

    for directory in (raw_dir, processed_dir, reports_dir, database_dir):
        directory.mkdir(parents=True)

    customers_file = raw_dir / "customers.csv"
    products_file = raw_dir / "products.csv"
    orders_file = raw_dir / "orders.csv"
    database_file = processed_dir / "sales.db"
    report_file = reports_dir / "data_quality_report.json"

    monkeypatch.setattr(config_module, "RAW_DIR", raw_dir)
    monkeypatch.setattr(config_module, "PROCESSED_DIR", processed_dir)
    monkeypatch.setattr(config_module, "REPORTS_DIR", reports_dir)
    monkeypatch.setattr(config_module, "DATABASE_DIR", database_dir)

    monkeypatch.setattr(pipeline_module, "CUSTOMERS_FILE", customers_file)
    monkeypatch.setattr(pipeline_module, "PRODUCTS_FILE", products_file)
    monkeypatch.setattr(pipeline_module, "ORDERS_FILE", orders_file)
    monkeypatch.setattr(pipeline_module, "DATABASE_FILE", database_file)
    monkeypatch.setattr(pipeline_module, "QUALITY_REPORT_FILE", report_file)

    monkeypatch.setattr(database_module, "DATABASE_FILE", database_file)

    customers = pd.DataFrame([
        {
            "customer_id": 1,
            "customer_name": "Customer A",
            "region": "Southeast",
            "created_at": "2024-01-01",
        },
        {
            "customer_id": 2,
            "customer_name": "Customer B",
            "region": "South",
            "created_at": "2024-01-02",
        },
    ])

    products = pd.DataFrame([
        {
            "product_id": 1,
            "product_name": "Product A",
            "category": "Office",
            "unit_price": 100.0,
        },
        {
            "product_id": 2,
            "product_name": "Product B",
            "category": "Home",
            "unit_price": 50.0,
        },
    ])

    orders = pd.DataFrame([
        {
            "order_id": 1, "customer_id": 1, "product_id": 1,
            "order_date": "2024-01-10", "quantity": 2,
            "unit_price": 100.0, "status": "completed",
        },
        {
            "order_id": 2, "customer_id": 2, "product_id": 2,
            "order_date": "2024-01-11", "quantity": None,
            "unit_price": None, "status": "completed",
        },
        {
            "order_id": 3, "customer_id": 1, "product_id": 1,
            "order_date": "2024-01-12", "quantity": 0,
            "unit_price": 100.0, "status": "completed",
        },
        {
            "order_id": 3, "customer_id": 1, "product_id": 1,
            "order_date": "2024-01-12", "quantity": 1,
            "unit_price": 100.0, "status": "completed",
        },
    ])

    customers.to_csv(customers_file, index=False)
    products.to_csv(products_file, index=False)
    orders.to_csv(orders_file, index=False)

    result = pipeline_module.run_pipeline()

    assert result["duplicate_orders_removed"] == 1
    assert result["missing_quantities_filled"] == 1
    assert result["missing_prices_filled"] == 1
    assert result["invalid_orders_removed"] == 1
    assert result["orders_loaded"] == 2
    assert database_file.exists()
    assert report_file.exists()

    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report["orders_loaded"] == 2

    with sqlite3.connect(database_file) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

    assert count == 2
