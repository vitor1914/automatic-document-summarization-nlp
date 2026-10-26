import pandas as pd

from src.database import get_connection


def get_kpis(region: str | None = None) -> dict:
    """Calculate sales KPIs for completed orders."""
    conditions = ["o.status = 'completed'"]
    parameters: list[str] = []

    if region:
        conditions.append("c.region = ?")
        parameters.append(region)

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(SUM(o.quantity * o.unit_price), 0) AS revenue,
            COALESCE(SUM(o.quantity), 0) AS units_sold,
            COALESCE(
                SUM(o.quantity * o.unit_price)
                / NULLIF(COUNT(DISTINCT o.order_id), 0),
                0
            ) AS average_order_value
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE {where_clause}
    """

    with get_connection() as connection:
        row = connection.execute(query, parameters).fetchone()

    return {
        "total_orders": int(row["total_orders"]),
        "revenue": round(float(row["revenue"]), 2),
        "units_sold": int(row["units_sold"]),
        "average_order_value": round(
            float(row["average_order_value"]), 2
        ),
    }


def get_monthly_revenue(region: str | None = None) -> pd.DataFrame:
    """Return completed sales revenue grouped by month."""
    query = """
        SELECT
            substr(o.order_date, 1, 7) AS month,
            ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE o.status = 'completed'
    """
    parameters: list[str] = []

    if region:
        query += " AND c.region = ?"
        parameters.append(region)

    query += " GROUP BY substr(o.order_date, 1, 7) ORDER BY month"

    with get_connection() as connection:
        return pd.read_sql_query(query, connection, params=parameters)


def get_top_products(
    limit: int = 10,
    region: str | None = None,
) -> list[dict]:
    """Return products ranked by completed units sold."""
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(o.quantity) AS units_sold,
            ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
        FROM orders o
        JOIN products p ON p.product_id = o.product_id
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE o.status = 'completed'
    """
    parameters: list[str] = []

    if region:
        query += " AND c.region = ?"
        parameters.append(region)

    query += """
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY units_sold DESC, revenue DESC
        LIMIT ?
    """
    parameters.append(str(limit))

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [
        {
            "product_id": int(row["product_id"]),
            "product_name": row["product_name"],
            "category": row["category"],
            "units_sold": int(row["units_sold"]),
            "revenue": round(float(row["revenue"]), 2),
        }
        for row in rows
    ]


def get_regions() -> list[str]:
    """Return the regions present in the customer table."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT region FROM customers ORDER BY region"
        ).fetchall()

    return [row["region"] for row in rows]


def get_sales_data(region: str | None = None) -> pd.DataFrame:
    """Return completed order details for dashboard analysis."""
    query = """
        SELECT
            o.order_id,
            o.order_date,
            c.customer_name,
            c.region,
            p.product_name,
            p.category,
            o.quantity,
            o.unit_price,
            o.quantity * o.unit_price AS revenue,
            o.status
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        JOIN products p ON p.product_id = o.product_id
        WHERE o.status = 'completed'
    """
    parameters: list[str] = []

    if region:
        query += " AND c.region = ?"
        parameters.append(region)

    query += " ORDER BY o.order_date DESC"

    with get_connection() as connection:
        return pd.read_sql_query(query, connection, params=parameters)