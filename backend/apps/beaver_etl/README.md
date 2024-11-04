# Beaver ETL Service
The Beaver ETL service is designed to parse datasets within the repository and perform ETL (Extract, Transform, Load) operations to ingest code algorithms into the beaver_api.

## Getting Started with Beaver ETL
This guide will help you set up the Beaver ETL using Poetry as your dependency management tool.

### Prerequisites

1. Ensure you have Python 3.12 or higher installed.
2. Install Poetry by following the instructions on [the official Poetry website](https://python-poetry.org/docs/).
3. Install Docker and Docker Compose on [the official Docker website](https://docs.docker.com/engine/install/)
4. Run `beaver_api` server locally on in docker
5. Generate token in the `beaver_api` admin

### Step-by-Step Setup for local development


Go to the etl folder
```bash
cd backend/apps/beaver_etl/
```

Use Poetry to install the project's dependencies:
```bash
poetry install
```

Activate the Virtual Environment:
```bash
poetry shell
```

Create `.env` file
```bash
cp .env.example .env
```

Add the generated token from `beaver_api` into your `.env` file
```bash
API_SECRET_TOKEN="past the generated token here"
```

To run the `beaver_etl` call the main function
```bash
python src/main.py
```

## How to run tests
Call pytest inside the project folder
``` bash
pytest .
```
