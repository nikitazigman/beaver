# Define environment variable names
SCRIPT_MIGRATION_DIR := ./internal/storage/scriptdb/migrations
TAG_MIGRATION_DIR := ./internal/storage/tagdb/migrations
CONTRIBUTOR_MIGRATION_DIR := ./internal/storage/contributordb/migrations
LANGUAGE_MIGRATION_DIR := ./internal/storage/languagedb/migrations
GOOSE_DRIVER := postgres
GOOSE_DBSTRING := ${GOOSE_DRIVER}://$(PG_USER):$(PG_PASSWORD)@$(PG_HOST):$(PG_PORT)/$(PG_DB)
# Apply all migrations
migrate: migrate_tag migrate_language migrate_contributor migrate_script

migrate_tag:
	@echo "Running migrations for tag..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(TAG_MIGRATION_DIR) up

migrate_language:
	@echo "Running migrations for language..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(LANGUAGE_MIGRATION_DIR) up

migrate_contributor:
	@echo "Running migrations for contributor..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(CONTRIBUTOR_MIGRATION_DIR) up

migrate_script:
	@echo "Running migrations for script..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(SCRIPT_MIGRATION_DIR) up

# Rollback all migrations
rollback: rollback_tag rollback_language rollback_contributor rollback_script

rollback_tag:
	@echo "Running migrations for tag..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(TAG_MIGRATION_DIR) down

rollback_script:
	@echo "Running migrations for script..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(SCRIPT_MIGRATION_DIR) down

rollback_language:
	@echo "Running migrations for language..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(LANGUAGE_MIGRATION_DIR) down

rollback_contributor:
	@echo "Running migrations for contributor..."
	GOOSE_DBSTRING=${GOOSE_DBSTRING} GOOSE_DRIVER=${GOOSE_DRIVER} goose -dir $(CONTRIBUTOR_MIGRATION_DIR) down

status:
	@echo "Checking migration status..."
	goose status
