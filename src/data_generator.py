import numpy as np
import pandas as pd

from src.config import (
    CUSTOMERS_FILE,
    ORDERS_FILE,
    PRODUCTS_FILE,
    create_directories,
)


def generate_data(
    seed: int = 42,
    n_customers: int = 100,
    n_products: int = 20,
    n_orders: int = 1000,
) -> dict[str, pd.DataFrame]:
    """Generate reproducible synthetic sales data."""
    if n_customers < 1 or n_products < 1 or n_orders < 1:
        raise ValueError("All record counts must be positive.")

    create_directories()
    rng = np.random.default_rng(seed)

    regions = ["North", "Northeast", "Central-West", "Southeast", "South"]
    categories = ["Electronics", "Home", "Office", "Accessories"]
    statuses = ["completed", "pending", "cancelled"]

    customers = pd.DataFrame({
        "customer_id": range(1, n_customers + 1),
        "customer_name": [
            f"Customer {i:03d}"
            for i in range(1, n_customers + 1)
        ],
        "region": rng.choice(regions, size=n_customers),
        "created_at": pd.to_datetime(
            rng.choice(
                pd.date_range("2023-01-01", "2025-12-31"),
                size=n_customers,
            )
        ).strftime("%Y-%m-%d"),
    })

    products = pd.DataFrame({
        "product_id": range(1, n_products + 1),
        "product_name": [
            f"Product {i:03d}"
            for i in range(1, n_products + 1)
        ],
        "category": rng.choice(categories, size=n_products),
        "unit_price": np.round(
            rng.uniform(15, 1200, size=n_products), 2
        ),
    })

    order_dates = pd.to_datetime(
        rng.choice(
            pd.date_range("2024-01-01", "2025-12-31"),
            size=n_orders,
        )
    )

    orders = pd.DataFrame({
        "order_id": range(1, n_orders + 1),
        "customer_id": rng.integers(
            1, n_customers + 1, size=n_orders
        ),
        "product_id": rng.integers(
            1, n_products + 1, size=n_orders
        ),
        "order_date": order_dates.strftime("%Y-%m-%d"),
        "quantity": rng.integers(1, 8, size=n_orders),
        "unit_price": np.nan,
        "status": rng.choice(
            statuses,
            size=n_orders,
            p=[0.75, 0.15, 0.10],
        ),
    })

    price_lookup = products.set_index("product_id")["unit_price"]
    orders["unit_price"] = orders["product_id"].map(price_lookup)
    orders["unit_price"] = (
        orders["unit_price"]
        * rng.uniform(0.90, 1.10, size=n_orders)
    ).round(2)

    # Inject intentional data-quality issues.
    if n_orders >= 10:
        orders.loc[0, "quantity"] = np.nan
        orders.loc[1, "unit_price"] = np.nan
        orders.loc[2, "quantity"] = 0
        orders.loc[3, "unit_price"] = -10
        orders = pd.concat(
            [orders, orders.iloc[[4]]],
            ignore_index=True,
        )

    customers.to_csv(CUSTOMERS_FILE, index=False)
    products.to_csv(PRODUCTS_FILE, index=False)
    orders.to_csv(ORDERS_FILE, index=False)

    return {
        "customers": customers,
        "products": products,
        "orders": orders,
    }


if __name__ == "__main__":
    datasets = generate_data()
    for name, dataframe in datasets.items():
        print(f"{name}: {len(dataframe)} records")
    print(f"CSV files created in: {CUSTOMERS_FILE.parent}")