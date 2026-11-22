# ChatGPT Clone

A chat app where the user sends a message and gets an AI reply.

**Status:** Phase 0 (foundation) done. Next: Phase 1, streaming chat. See the [roadmap](docs/roadmap.md) and the stack in [ADR-0001](docs/adr/0001-tech-stack.md).

## Requirements

Docker, Node.js 24+, pnpm, uv, and make.

## Quick start

```sh
make setup    # git hooks, env files, dependencies
make infra    # Postgres + Redis in Docker
make dev      # API on http://localhost:8000, web on http://localhost:3000
```

Or run everything in Docker: `make up` (stop with `make down`). `make help` lists all commands.

## Project layout

- `apps/api`: FastAPI backend ([README](apps/api/README.md))
- `apps/web`: Next.js frontend ([README](apps/web/README.md))
- `docker/`: one folder per service ([README](docker/README.md))
- `docs/`: decisions, research, roadmap, and security plan

## How we work

- `main` is protected. All work happens on a branch and reaches `main` through a reviewed pull request, with CI passing.
- Full workflow and rules: [`AGENTS.md`](./AGENTS.md).
- Want to contribute? Start with [`CONTRIBUTING.md`](./CONTRIBUTING.md) and the [good first issues](https://github.com/MuhammadAbdullah95/chatgpt-clone/labels/good%20first%20issue).

## For AI agents

Read [`AGENTS.md`](./AGENTS.md) before making any change.
