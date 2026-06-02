SHELL := /bin/bash

ROOT_DIR := $(shell pwd)
ENV_FILE := $(ROOT_DIR)/.env
API_PORT ?= 18080
WEB_PORT ?= 13080
REDIS_PORT ?= 16379

.PHONY: install install-api install-web dev start-api start-web redis-start redis-ping codeserver-env check

install: install-api install-web

install-api:
	cd api && uv sync

install-web:
	pnpm install

dev:
	$(MAKE) -j2 start-api start-web

redis-start:
	@mkdir -p data/redis
	@if redis-cli -p $(REDIS_PORT) ping >/dev/null 2>&1; then \
		echo "Redis is already running on $(REDIS_PORT)"; \
	else \
		redis-server --dir "$(ROOT_DIR)/data/redis" --appendonly yes --port $(REDIS_PORT) --daemonize yes; \
		sleep 1; \
	fi
	@$(MAKE) redis-ping

redis-ping:
	@redis-cli -p $(REDIS_PORT) ping

start-api:
	cd api && set -a && source ../.env && set +a && uv run uvicorn app.main:app --host $${API_HOST:-127.0.0.1} --port $${API_PORT:-8000} --reload

start-web:
	set -a && source .env && set +a && pnpm --filter lite-dify-web dev --hostname 0.0.0.0 --port $${WEB_PORT:-3000}

codeserver-env:
	@if [ -z "$$VSCODE_PROXY_URI" ]; then \
		echo "VSCODE_PROXY_URI is not set"; \
		exit 1; \
	fi
	@proxy_api="$${VSCODE_PROXY_URI/\{\{port\}\}/18080}"; \
	proxy_web="$${VSCODE_PROXY_URI/\{\{port\}\}/13080}"; \
	proxy_origin="$$(python -c 'import os, urllib.parse; u=urllib.parse.urlparse(os.environ["VSCODE_PROXY_URI"].replace("{{port}}", "13080")); print(f"{u.scheme}://{u.netloc}")')"; \
	cp .env.example .env; \
	python scripts/update_env.py .env PUBLIC_API_URL "$$proxy_api"; \
	python scripts/update_env.py .env NEXT_PUBLIC_API_BASE_URL "$$proxy_api"; \
	python scripts/update_env.py .env PUBLIC_WEB_URL "$$proxy_web"; \
	python scripts/update_env.py .env API_HOST "127.0.0.1"; \
	python scripts/update_env.py .env API_PORT "18080"; \
	python scripts/update_env.py .env WEB_PORT "13080"; \
	python scripts/update_env.py .env REDIS_URL "redis://127.0.0.1:16379/0"; \
	python scripts/update_env.py .env NEXT_ALLOWED_DEV_ORIGINS "$$proxy_origin"; \
	echo "Wrote .env for code-server"; \
	echo "Web: $$proxy_web"; \
	echo "API: $$proxy_api"

check:
	cd api && uv run python -c "from app.main import app; print(app.title)"
	pnpm --filter lite-dify-web type-check
