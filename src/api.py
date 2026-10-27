from fastapi import FastAPI, HTTPException, Query

from src.config import DATABASE_FILE
from src.metrics import get_kpis, get_regions, get_top_products

app = FastAPI(
    title="Enterprise Sales Intelligence API",
    description=(
        "API for sales KPIs and product performance "
        "using a synthetic dataset."
    ),
    version="1.0.0",
)


@app.get("/health", tags=["System"])
def health_check() -> dict:
    """Check API and database availability."""
    return {
        "status": "ok",
        "database_exists": DATABASE_FILE.exists(),
    }


@app.get("/regions", tags=["Sales"])
def list_regions() -> dict:
    """List available sales regions."""
    try:
        return {"regions": get_regions()}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Sales database is unavailable.",
        ) from exc


@app.get("/kpis", tags=["Sales"])
def sales_kpis(region: str | None = None) -> dict:
    """Get sales KPIs, optionally filtered by region."""
    try:
        if region and region not in get_regions():
            raise HTTPException(
                status_code=404,
                detail="Region not found.",
            )
        return get_kpis(region=region)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Could not calculate sales KPIs. Run the ETL first.",
        ) from exc


@app.get("/sales/top-products", tags=["Sales"])
def top_products(
    limit: int = Query(default=10, ge=1, le=100),
    region: str | None = None,
) -> dict:
    """Get the best-selling products by completed units sold."""
    try:
        if region and region not in get_regions():
            raise HTTPException(
                status_code=404,
                detail="Region not found.",
            )
        return {
            "region": region,
            "products": get_top_products(limit=limit, region=region),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve products. Run the ETL first.",
        ) from exc