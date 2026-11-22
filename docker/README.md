# Docker

Everything Docker lives here. Each service has its own folder holding everything about it. `compose.yaml` only lists the folders with `include`.

| Service | Folder | What it is | Port (this machine only) | Started by |
|---|---|---|---|---|
| postgres | `postgres/` | PostgreSQL 18 with pgvector | 5432 | `make infra`, `make up` |
| redis | `redis/` | Redis 8 | 6379 | `make infra`, `make up` |
| api | `api/` | FastAPI app, built from `apps/api` | 8000 | `make up` |
| web | `web/` | Next.js app, built from `apps/web` | 3000 | `make up` |

To add a service: create a folder with its own `compose.yaml`, then add one line to `compose.yaml`.

## Two ways to run

- **Daily development:** `make infra` starts Postgres and Redis. Run the apps on your machine with `make dev` for hot reload.
- **Everything in Docker:** `make up` builds and starts all four containers, like production.

## Commands (from the repo root)

| Command | What it does |
|---|---|
| `make infra` | Start Postgres and Redis |
| `make up` | Build and start all four containers |
| `make down` | Stop all containers (data is kept) |
| `make ps` | Show every container and its health |
| `make logs s=postgres` | Follow one service's logs (leave out `s=` for all) |
| `make restart s=redis` | Restart one service |
| `make db-shell` | Open `psql` inside Postgres |
| `make redis-shell` | Open `redis-cli` inside Redis |

## Settings

Services read `docker/.env.example` first, then `docker/.env` if it exists. `make setup` creates `docker/.env` from the example; change the Postgres password there. `docker/.env` is never committed.

## Security

- Containers run as a non-root user.
- Multi-stage builds: the final images hold only what runs the app. The API image has no source code or build tools.
- No secrets inside images: settings come from env files when the container starts. Each Dockerfile has its own `Dockerfile.dockerignore` that keeps `.env` files out.
- Ports bind to `127.0.0.1`, so only this machine can reach them.
- Local only: Redis has no password, and the Postgres password is a local one. Deployment adds real secrets and a `compose.prod.yaml`.

## Troubleshooting

| Problem | Fix |
|---|---|
| Port already in use (5432, 6379, 8000, 3000) | Stop the other program using that port, or change the left side of `ports` in that service's `compose.yaml` |
| A service shows `unhealthy` in `make ps` | `make logs s=<service>` |
| An image did not pick up code changes | `make up` rebuilds; for a clean rebuild run `docker compose -f docker/compose.yaml --profile apps build --no-cache` |
| Start Postgres from scratch (**deletes all data**) | `docker compose -f docker/compose.yaml --profile apps down -v` |
