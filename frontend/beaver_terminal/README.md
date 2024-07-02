# Local Development Setup Guide

Follow these steps to set up the project locally:

1. **Run Docker**
```bash
   ./scripts/dev up -d
```
2. Navigate to the API Source Directory

```bash
cd beaver_api/src
```
3. Run Migrations

```bash
python manage.py migrate
```
4. Create Superuser

```bash
python manage.py createsuperuser
```

5. Start the Development Server

```bash
python manage.py runserver
```
6. Access Admin Page and Generate Token
    * Go to the admin page at /admin
    * Navigate to /tokens
    * Generate and copy a token for your user

7. Set Up ETL Process
```bash
cd beaver_etl
```
8. Export API Token

```bash
export api_secret_token=<token>
```
9. Run ETL

```bash
python beaver_etl/main
```
10. Navigate to CLI Directory

```bash
cd beaver_cli
```
11. Run CLI Client

```bash
python beaver_cli/main.py
```

*Note: Ensure you activate the service's Poetry environment, install dependencies, and then exit the Poetry shell as needed.*