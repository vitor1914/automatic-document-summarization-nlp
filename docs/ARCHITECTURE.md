# Architecture

## Overview

The project implements a small sales analytics platform.

## Data flow

1. The generator creates synthetic customers, products and orders.
2. CSV files are written to `data/raw/`.
3. The ETL pipeline validates and transforms the records.
4. Clean records are loaded into a SQLite database.
5. The metrics module calculates business indicators.
6. FastAPI exposes selected indicators through REST endpoints.
7. Streamlit presents interactive charts and filtered data.
8. Pytest validates calculations and pipeline behavior.
9. GitHub Actions runs tests after pushes and pull requests.

## Components

- `src/data_generator.py`: synthetic data generation.
- `src/pipeline.py`: extraction, transformation and loading.
- `src/database.py`: database connections and initialization.
- `src/metrics.py`: reusable analytics functions.
- `src/api.py`: REST API.
- `dashboard/app.py`: interactive dashboard.
- `tests/`: automated tests.

## Data quality rules

- Duplicate order identifiers are removed.
- Missing quantities are replaced with 1.
- Missing order prices use the corresponding product price.
- Non-positive quantities and prices are rejected.
- Orders with invalid dates or unknown foreign keys are rejected.
- A JSON report records cleaning and loading counts.

## Limitations

The dataset is synthetic and intended for learning and demonstration.
This project is not a production financial system.