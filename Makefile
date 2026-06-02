SHELL := /bin/bash

ROOT_DIR := $(shell pwd)
ENV_FILE := $(ROOT_DIR)/.env
API_PORT ?= 8000
WEB_PORT ?= 3000

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
	@if redis-cli -p 6379 ping >/dev/null 2>&1; then \
		echo "Redis is already running"; \
	else \
		redis-server --dir "$(ROOT_DIR)/data/redis" --appendonly yes --port 6379 --daemonize yes; \
		sleep 1; \
	fi
	@$(MAKE) redis-ping

redis-ping:
	@redis-cli -p 6379 ping

start-api:
	cd api && set -a && source ../.env && set +a && uv run uvicorn app.main:app --host $${API_HOST:-127.0.0.1} --port $${API_PORT:-8000} --reload

start-web:
	set -a && source .env && set +a && pnpm --filter lite-dify-web dev --hostname 0.0.0.0 --port $${WEB_PORT:-3000}

codeserver-env:
	@if [ -z "$$VSCODE_PROXY_URI" ]; then \
		echo "VSCODE_PROXY_URI is not set"; \
		exit 1; \
	fi
	@proxy_8000="$${VSCODE_PROXY_URI/\{\{port\}\}/8000}"; \
	proxy_3000="$${VSCODE_PROXY_URI/\{\{port\}\}/3000}"; \
	proxy_origin="$$(python -c 'import os, urllib.parse; u=urllib.parse.urlparse(os.environ["VSCODE_PROXY_URI"].replace("{{port}}", "3000")); print(f"{u.scheme}://{u.netloc}")')"; \
	cp .env.example .env; \
	python scripts/update_env.py .env PUBLIC_API_URL "$$proxy_8000"; \
	python scripts/update_env.py .env NEXT_PUBLIC_API_BASE_URL "$$proxy_8000"; \
	python scripts/update_env.py .env PUBLIC_WEB_URL "$$proxy_3000"; \
	python scripts/update_env.py .env API_HOST "127.0.0.1"; \
	python scripts/update_env.py .env API_PORT "8000"; \
	python scripts/update_env.py .env WEB_PORT "3000"; \
	python scripts/update_env.py .env NEXT_ALLOWED_DEV_ORIGINS "$$proxy_origin"; \
	echo "Wrote .env for code-server"; \
	echo "Web: $$proxy_3000"; \
	echo "API: $$proxy_8000"

check:
	cd api && uv run python -c "from app.main import app; print(app.title)"
	pnpm --filter lite-dify-web type-check
