# Enterprise Sales Intelligence Platform

🇧🇷 Português | 🇺🇸 English

## 🇧🇷 Sobre o projeto

Plataforma de análise de vendas desenvolvida para praticar engenharia de dados, análise de dados, bancos de dados relacionais, APIs REST, visualização de indicadores e testes automatizados.

O projeto utiliza dados fictícios de clientes, produtos e pedidos para construir um pipeline ETL, calcular indicadores comerciais e apresentar os resultados em um dashboard interativo.

## Funcionalidades

- Geração reproduzível de dados sintéticos.
- Pipeline ETL com validação, limpeza e relatório de qualidade.
- Banco de dados SQLite com chaves estrangeiras e índices.
- Indicadores de faturamento, pedidos concluídos, unidades vendidas e ticket médio.
- Análise de faturamento mensal e produtos mais vendidos.
- API REST desenvolvida com FastAPI.
- Dashboard interativo com Streamlit e Plotly.
- Exportação de dados filtrados para CSV.
- Testes automatizados com pytest.
- Integração contínua com GitHub Actions.

## Tecnologias

- Python
- Pandas
- NumPy
- SQLite
- FastAPI
- Streamlit
- Plotly
- Pytest
- GitHub Actions
- SQL

## Estrutura

```text
dashboard/     Aplicação de visualização
data/          Dados de entrada e arquivos processados
database/      Esquema SQL
docs/          Documentação e planejamento
reports/       Relatórios gerados
src/           Código-fonte e pipeline ETL
tests/         Testes automatizados
.github/       Fluxos de integração contínua
```

## Requisitos

- Python 3.12 ou compatível
- pip
- Git

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar o pipeline

Gere os dados fictícios:

```bash
python -m src.data_generator
```

Execute o ETL:

```bash
python -m src.pipeline
```

O banco SQLite será criado em `data/processed/sales.db`, e o relatório de qualidade será salvo em `reports/data_quality_report.json`.

## Executar o dashboard

```bash
streamlit run dashboard/app.py
```

## Executar a API

```bash
uvicorn src.api:app --reload
```

Documentação interativa da API:

- `/docs` — documentação Swagger
- `/redoc` — documentação ReDoc

Endpoints principais:

- `GET /health`
- `GET /regions`
- `GET /kpis`
- `GET /kpis?region=Southeast`
- `GET /sales/top-products`
- `GET /sales/top-products?limit=5&region=Southeast`

## Executar os testes

```bash
pytest -v
```

## Regras dos indicadores

O faturamento e os indicadores comerciais consideram somente pedidos com status `completed`. O ticket médio é calculado dividindo o faturamento pelo número de pedidos concluídos. Os dados utilizados são sintéticos e não representam transações reais.

## Próximas melhorias

- Suporte a PostgreSQL.
- Contêineres com Docker.
- Logging estruturado.
- Maior cobertura de testes.
- Previsão de vendas.
- Implantação em nuvem.

---

## 🇺🇸 About the project

A sales analytics platform built to practice data engineering, data analysis, relational databases, REST APIs, business intelligence, and automated testing.

The project uses synthetic customer, product, and order data to implement an ETL pipeline, calculate sales KPIs, and display results in an interactive dashboard.

## Features

- Reproducible synthetic data generation.
- ETL pipeline with data validation, cleaning, and quality reporting.
- SQLite database with foreign keys and indexes.
- Revenue, completed orders, units sold, and average order value KPIs.
- Monthly revenue and top-selling product analysis.
- REST API built with FastAPI.
- Interactive Streamlit and Plotly dashboard.
- Filtered CSV export.
- Automated tests with pytest.
- Continuous integration with GitHub Actions.

## Technologies

- Python
- Pandas
- NumPy
- SQLite
- FastAPI
- Streamlit
- Plotly
- Pytest
- GitHub Actions
- SQL

## Requirements

- Python 3.12 or compatible
- pip
- Git

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the pipeline

Generate synthetic data:

```bash
python -m src.data_generator
```

Run the ETL pipeline:

```bash
python -m src.pipeline
```

The SQLite database is created at `data/processed/sales.db`. The quality report is written to `reports/data_quality_report.json`.

## Run the dashboard

```bash
streamlit run dashboard/app.py
```

## Run the API

```bash
uvicorn src.api:app --reload
```

Interactive API documentation:

- `/docs` — Swagger documentation
- `/redoc` — ReDoc documentation

Main endpoints:

- `GET /health`
- `GET /regions`
- `GET /kpis`
- `GET /kpis?region=Southeast`
- `GET /sales/top-products`
- `GET /sales/top-products?limit=5&region=Southeast`

## Run tests

```bash
pytest -v
```

## KPI definitions

Revenue and sales KPIs include only orders with `completed` status. Average order value is calculated as revenue divided by the number of completed orders. All data is synthetic and does not represent real transactions.

## Future improvements

- PostgreSQL support.
- Docker containers.
- Structured logging.
- Expanded test coverage.
- Sales forecasting.
- Cloud deployment.

## License

This project is available for educational and portfolio purposes. Add a license file if you intend to distribute it under specific terms.