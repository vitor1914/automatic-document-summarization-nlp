import json

import pandas as pd
import pytest

import src.pipeline as pipeline_module
from src.data_generator import generate_data


def test_pipeline_cleans_and_loads_data(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    reports_dir = tmp_path / "reports"
    database_dir = tmp_path / "database"

    for directory in (
        raw_dir, processed_dir, reports_dir, database_dir
    ):
        directory.mkdir(parents=True)

    customers_file = raw_dir / "customers.csv"
    products_file = raw_dir / "products.csv"
    orders_file = raw_dir / "orders.csv"
    database_file = processed_dir / "sales.db"
    report_file = reports_dir / "data_quality_report.json"

    # Use the real schema file from the project.
    from src.config import SCHEMA_FILE

    monkeypatch.setattr(
        pipeline_module, "CUSTOMERS_FILE", customers_file
    )
    monkeypatch.setattr(
        pipeline_module, "PRODUCTS_FILE", products_file
    )
    monkeypatch.setattr(
        pipeline_module, "ORDERS_FILE", orders_file
    )
    monkeypatch.setattr(
        pipeline_module, "DATABASE_FILE", database_file
    )
    monkeypatch.setattr(
        pipeline_module, "QUALITY_REPORT_FILE", report_file
    )

    import src.config as config_module
    import src.database as database_module

    monkeypatch.setattr(config_module, "RAW_DIR", raw_dir)
    monkeypatch.setattr(config_module, "PROCESSED_DIR", processed_dir)
    monkeypatch.setattr(config_module, "REPORTS_DIR", reports_dir)
    monkeypatch.setattr(config_module, "DATABASE_DIR", database_dir)

    monkeypatch.setattr(database_module, "DATABASE_FILE", database_file)
    monkeypatch.setattr(database_module, "SCHEMA_FILE", SCHEMA_FILE)

    # Pipeline uses the paths imported into its own module.
    monkeypatch.setattr(pipeline_module, "DATABASE_FILE", database_file)
    monkeypatch.setattr(pipeline_module, "QUALITY_REPORT_FILE", report_file)

    rng_data = generate_data(
        seed=7,
        n_customers=15,
        n_products=5,
        n_orders=30,
    )

    # Redirect generator outputs to the temporary test directory.
    rng_data["customers"].to_csv(customers_file, index=False)
    rng_data["products"].to_csv(products_file, index=False)
    rng_data["orders"].to_csv(orders_file, index=False)

    result = pipeline_module.run_pipeline()

    assert result["orders_loaded"] > 0
    assert result["duplicate_orders_removed"] >= 1
    assert database_file.exists()
    assert report_file.exists()

    saved_report = json.loads(report_file.read_text(encoding="utf-8"))
    assert saved_report["orders_loaded"] == result["orders_loaded"]