import json

import pandas as pd

from src.config import (
    CUSTOMERS_FILE,
    DATABASE_FILE,
    ORDERS_FILE,
    PRODUCTS_FILE,
    QUALITY_REPORT_FILE,
    create_directories,
)
from src.database import get_connection, initialize_database


def run_pipeline() -> dict:
    """Run the ETL pipeline and return a quality summary."""
    create_directories()

    required_files = [
        CUSTOMERS_FILE,
        PRODUCTS_FILE,
        ORDERS_FILE,
    ]
    missing_files = [str(path) for path in required_files if not path.exists()]

    if missing_files:
        raise FileNotFoundError(
            "Missing source files. Run the data generator first: "
            + ", ".join(missing_files)
        )

    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    orders = pd.read_csv(ORDERS_FILE)

    original_orders = len(orders)

    customers = customers.drop_duplicates(subset=["customer_id"])
    products = products.drop_duplicates(subset=["product_id"])

    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    duplicate_orders_removed = original_orders - len(orders)

    # Normalize and validate types.
    orders["quantity"] = pd.to_numeric(
        orders["quantity"], errors="coerce"
    )
    orders["unit_price"] = pd.to_numeric(
        orders["unit_price"], errors="coerce"
    )

    price_lookup = products.set_index("product_id")["unit_price"]

    missing_quantity = int(orders["quantity"].isna().sum())
    orders["quantity"] = orders["quantity"].fillna(1)

    missing_price = int(orders["unit_price"].isna().sum())
    orders["unit_price"] = orders["unit_price"].fillna(
        orders["product_id"].map(price_lookup)
    )

    orders["quantity"] = orders["quantity"].astype("int64")

    # Keep only rows with valid business rules and existing references.
    valid_statuses = {"completed", "pending", "cancelled"}

    valid_mask = (
        orders["quantity"].gt(0)
        & orders["unit_price"].gt(0)
        & orders["customer_id"].isin(customers["customer_id"])
        & orders["product_id"].isin(products["product_id"])
        & orders["status"].isin(valid_statuses)
        & pd.to_datetime(
            orders["order_date"], errors="coerce"
        ).notna()
    )

    invalid_rows_removed = int((~valid_mask).sum())
    orders = orders.loc[valid_mask].copy()

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    ).dt.strftime("%Y-%m-%d")

    # Prevent partially loaded datasets if a database operation fails.
    initialize_database()

    with get_connection() as connection:
        connection.execute("DELETE FROM orders")
        connection.execute("DELETE FROM products")
        connection.execute("DELETE FROM customers")

        customers.to_sql(
            "customers", connection, if_exists="append", index=False
        )
        products.to_sql(
            "products", connection, if_exists="append", index=False
        )
        orders.to_sql(
            "orders", connection, if_exists="append", index=False
        )

        customer_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]
        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        order_count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

    report = {
        "source_orders": original_orders,
        "duplicate_orders_removed": duplicate_orders_removed,
        "missing_quantities_filled": missing_quantity,
        "missing_prices_filled": missing_price,
        "invalid_orders_removed": invalid_rows_removed,
        "customers_loaded": int(customer_count),
        "products_loaded": int(product_count),
        "orders_loaded": int(order_count),
        "database": str(DATABASE_FILE.name),
    }

    QUALITY_REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("ETL pipeline completed.")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == "__main__":
    run_pipeline()