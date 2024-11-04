# Beaver API

The Beaver API is a Django-based backend application designed for the Beaver project. This service provides an API to retrieve random code snippets and implements several endpoints for ETL (Extract, Transform, Load) operations to ingest code documents from a GitHub dataset into the database.

## Getting Started with Beaver API
This guide will help you set up the Beaver API using Poetry as your dependency management tool.

### Prerequisites

1. Ensure you have Python 3.12 or higher installed.
2. Install Poetry by following the instructions on [the official Poetry website](https://python-poetry.org/docs/).
3. Install Docker and Docker Compose on [the official Docker website](https://docs.docker.com/engine/install/)

### Step-by-Step Setup for local development

Start docker postgres container
```bash
./IaC/scripts/dev.sh up beaver_db -d
```

Go to the api folder
```bash
cd backend/apps/beaver_api/
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

Run Database Migrations:
```bash
python manage.py migrate
```

Create a superuser account
```bash
python manage.py createsuperuser
```

Start a django server
```bash
python manage.py runserver
```


### How to create an access token for the `beaver_etl`
1. Go to the admin page `http://127.0.0.1:8000/admin`.
2. Go to the tokens page
3. Click `add token` button on the right top corner of the page

### How to run all in docker

``` bash
./IaC/scripts/dev.sh up -d
```

### How to run tests

Inside the `beaver_api` folder
```bash
pytest .
```
