# API

FastAPI backend for the ChatGPT clone. Structure and rules: see the root [`AGENTS.md`](../../AGENTS.md).

## Setup

```sh
cd apps/api
uv sync                 # install dependencies into .venv
cp .env.example .env    # then fill in values
```

## Commands (run inside `apps/api`)

| Task | Command |
|---|---|
| Dev server with reload | `uv run fastapi dev` |
| Tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |

The dev server runs on http://localhost:8000. Interactive API docs: http://localhost:8000/docs (disabled in production).
