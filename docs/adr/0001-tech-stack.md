# ADR-0001: Tech stack

- **Status:** Accepted
- **Date:** 2026-11-22

## Context

We are building a ChatGPT clone that runs on a local machine first, with ChatGPT's main features: streaming chat, chat history, accounts, edit/regenerate, images and files, web search, memory, and voice.

Research ([How ChatGPT is built](../research/reports/How%20ChatGPT%20is%20built.md)) found that ChatGPT's app layer uses ordinary tools (React, Python with FastAPI, PostgreSQL, Redis, server-sent events). The two decisions that are hardest to change later are **the message data model** and **the streaming contract**. The web framework is easier to swap: ChatGPT changed its framework twice.

Constraints: a small team, learning while building, OpenAI as the model provider (API key available), runs locally first.

## Options

1. **Next.js frontend + FastAPI backend (two apps).** Pros: AI work stays in Python, which has the best AI ecosystem; a clean backend API that future mobile apps can reuse; mirrors ChatGPT's own split. Cons: two apps to run; auth spans two services.
2. **Next.js only (full-stack).** Pros: one app, fewer moving parts. Cons: AI logic and UI in one place; TypeScript-only AI ecosystem; backend harder to reuse.
3. **React Router 7 (ChatGPT's current framework) + FastAPI.** Pros: same framework as ChatGPT. Cons: smaller ecosystem and fewer learning resources than Next.js; matching ChatGPT's framework buys little because it changes.

## Decision

Option 1.

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router) + **TypeScript 7** + Tailwind CSS + shadcn/ui |
| Chat UI | Vercel AI SDK UI (`useChat`) + Streamdown for streaming markdown |
| Backend | Python + FastAPI (async), managed with uv |
| Model gateway | Pydantic AI, streaming in the AI SDK UI message stream protocol (`VercelAIAdapter`) |
| LLM provider | OpenAI, through the gateway so the provider can change by config |
| Database | PostgreSQL + SQLAlchemy 2 + Alembic; pgvector later for memory and project search |
| Cache, rate limits, jobs, stream buffer | Redis |
| Auth | Better Auth in Next.js (email + Google); FastAPI verifies Better Auth JWTs through its JWKS endpoint |
| File storage | Local disk behind a storage interface; S3-compatible storage when deploying |
| Local run | Docker Compose (PostgreSQL, Redis) + pnpm + uv |
| Quality | Ruff, pytest, Biome (lint + format), Vitest, Playwright, GitHub Actions CI |

### Design rules that come with this decision

1. **Messages are a tree.** Every message has a `parent_id`; every conversation has a `current_node_id`. Editing or regenerating adds a sibling branch; nothing is overwritten.
2. **Generation is decoupled from the browser connection.** `POST /chat` saves the user message and an empty assistant message (`status: generating`), then starts a background task. The task writes stream events to a Redis Stream with sequence numbers and saves the final message to PostgreSQL. The SSE response only reads from Redis.
   - A client that refreshes or loses its connection reconnects with `GET /chat/{id}/stream` and gets a replay plus the live rest (`204` if nothing is active).
   - **Stop** is an explicit cancel request, not a closed connection. The partial answer is saved as `stopped`.
   - A cleanup job marks answers stuck in `generating` as `interrupted`.
   - One active generation per conversation.
3. **Standard stream protocol.** We use the AI SDK UI message stream protocol on both sides instead of inventing our own.
4. **The OpenAI API key never reaches the browser.** See [security.md](../security.md).

## Consequences

- **Easier:** Python AI libraries; a documented streaming protocol on both ends; resumable streams from day one; switching model or provider is a config change.
- **Harder:** two apps and two env files; auth is split (Better Auth issues tokens, FastAPI verifies them); Redis is required even locally.
- **TypeScript 7** has no JavaScript API until 7.1. `next build` type-checks with the `tsc` CLI (the default since Next.js 16.4). ESLint's TypeScript parser needs that API, so the frontend uses **Biome** for linting and formatting instead of ESLint (updated 2026-11-22 during Phase 0).
- **Revisit later:** background job runner (in-process tasks first, a worker queue when needed); object storage when deploying.
