	# Define environment variable names
SCRIPT_DETAIL_MIGRATION_DIR := ./internal/db/scriptdetail/migrations/
SCRIPT_MIGRATION_DIR := ./internal/db/script/migrations/
TAG_MIGRATION_DIR := ./internal/db/tag/migrations/
CONTRIBUTOR_MIGRATION_DIR := ./internal/db/contributor/migrations/
LANGUAGE_MIGRATION_DIR := ./internal/db/language/migrations/
GOOSE_DRIVER := postgres
GOOSE_DBSTRING := postgresql://$(DB_USER):$(DB_PASS)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)?sslmode=$(DB_SSL_MODE)
SQL_FILE=./utils/demo_data.sql
TMP_DIR=./tmp/migrations

connect_db:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

demo_data:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f $(SQL_FILE)

# Apply all migrations
migrate: _create_tmp_dir _migrate _remove_tmp_dir
# Rollback all migrations
rollback: _create_tmp_dir _rollback _remove_tmp_dir



_migrate:
	@echo "Running migrations"
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(TMP_DIR) up

_rollback:
	@echo "Running migrations"
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(TMP_DIR) down

_create_tmp_dir:
	@echo "Creating tmp dir to copy all migrations into one place"
	mkdir -p ./tmp/migrations
	cp -r $(SCRIPT_DETAIL_MIGRATION_DIR)* ./tmp/migrations/
	cp -r $(SCRIPT_MIGRATION_DIR)* ./tmp/migrations/
	cp -r $(TAG_MIGRATION_DIR)* ./tmp/migrations/
	cp -r $(CONTRIBUTOR_MIGRATION_DIR)* ./tmp/migrations/
	cp -r $(LANGUAGE_MIGRATION_DIR)* ./tmp/migrations/

_remove_tmp_dir:
	rm -r ./tmp

status:
	@echo "Checking migration status..."
	goose status
