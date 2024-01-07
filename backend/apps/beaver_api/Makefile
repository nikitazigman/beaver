SHELL := /bin/bash

.PHONY: all dev-server shell schema init-dev-structure

all:
	# intentionally left empty to prevent accidental run of first recipe

dev-server:
	set -a && source .env && poetry run python beaver_api/main.py dev-server

shell:
	set -a && source .env && poetry run ipython

schema:
	poetry run python beaver_api/main.py schema

init-dev-structure:
	mkdir -p pid
	mkdir -p logs
	touch logs/beaver_api.logs
