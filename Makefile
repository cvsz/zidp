SHELL := /bin/sh
COMPOSE := docker compose --project-directory . -f infra/dev/docker-compose.yml

.PHONY: help setup dev-up dev-down dev-test dev-reset config

help:
	@printf '%s\n' 'Targets: setup config dev-up dev-test dev-down dev-reset'

setup:
	@test -f .env || cp .env.example .env
	@printf '%s\n' 'Edit .env and set unique ZIDP_ADMIN_PASSWORD and ZIDP_DB_PASSWORD values.'

config:
	$(COMPOSE) config --quiet

dev-up:
	$(COMPOSE) up -d --wait --wait-timeout 240

dev-test:
	python3 scripts/test-idp-dev.py

dev-down:
	$(COMPOSE) down

dev-reset:
	$(COMPOSE) down --volumes --remove-orphans
