# Common commands for the whole project. Run `make` or `make help` to list them.

COMPOSE := docker compose -f docker/compose.yaml
# Pick one service for logs/restart: make logs s=postgres
s ?=

.DEFAULT_GOAL := help
.PHONY: help setup infra up down ps logs restart db-shell redis-shell \
        dev dev-api dev-web test lint audit images check

# Keep in sync with .github/workflows/ci.yml
PIP_AUDIT := pip-audit==2.10.1

help: ## List all commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

# ---- Setup ----

setup: ## First-time setup: git hooks, env files, dependencies
	git config core.hooksPath .githooks
	@test -f docker/.env || cp docker/.env.example docker/.env
	@test -f apps/api/.env || cp apps/api/.env.example apps/api/.env
	cd apps/api && uv sync
	cd apps/web && pnpm install

# ---- Docker ----

infra: ## Start Postgres and Redis (for daily development)
	$(COMPOSE) up -d --wait postgres redis

up: ## Build and start everything in Docker (postgres, redis, api, web)
	$(COMPOSE) --profile apps up -d --build --wait

down: ## Stop all containers (data is kept)
	$(COMPOSE) --profile apps down

ps: ## Show every container and its health
	$(COMPOSE) --profile apps ps

logs: ## Follow logs (all, or one: make logs s=postgres)
	$(COMPOSE) --profile apps logs -f $(s)

restart: ## Restart one service: make restart s=redis
	$(COMPOSE) --profile apps restart $(s)

db-shell: ## Open psql inside the Postgres container
	$(COMPOSE) exec postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

redis-shell: ## Open redis-cli inside the Redis container
	$(COMPOSE) exec redis redis-cli

# ---- Apps on this machine (hot reload) ----

dev: ## Run API and web together with hot reload
	$(MAKE) -j2 dev-api dev-web

dev-api: ## Run only the API (http://localhost:8000)
	cd apps/api && uv run fastapi dev

dev-web: ## Run only the web app (http://localhost:3000)
	cd apps/web && pnpm dev

# ---- Quality ----

test: ## Run all tests
	cd apps/api && uv run pytest

lint: ## Lint, format-check, and type-check both apps (same as CI)
	cd apps/api && uv run ruff check . && uv run ruff format --check .
	cd apps/web && pnpm exec biome ci . && pnpm typecheck

audit: ## Check dependencies for known vulnerabilities (same as CI)
	cd apps/api && f=$$(mktemp) && \
		uv export --format requirements-txt --no-dev --no-emit-project --locked > "$$f" && \
		uvx $(PIP_AUDIT) --disable-pip --require-hashes -r "$$f"; \
		status=$$?; rm -f "$$f"; exit $$status
	cd apps/web && pnpm audit --prod --audit-level high

images: ## Build the Docker images (CI's Docker job)
	$(COMPOSE) --profile apps config --quiet
	$(COMPOSE) --profile apps build

check: lint test audit ## CI's API and Web checks, plus the web build
	cd apps/web && pnpm build
