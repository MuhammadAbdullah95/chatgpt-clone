# Roadmap

How we build the ChatGPT clone, phase by phase. Stack and design rules: [ADR-0001](adr/0001-tech-stack.md). Security plan: [security.md](security.md).

Each phase is split into small feature branches. Each branch goes through a PR, an AI review, and the user's review before merging.

## MVP

| Phase | Goal | Main pieces | Done when |
|---|---|---|---|
| 0 | Foundation | `apps/web` (Next.js) and `apps/api` (FastAPI) scaffolds, Docker Compose (PostgreSQL, Redis), Makefile, CI, Dependabot, secret scanning, health check, `.env.example` files | Both apps run locally and CI is green |
| 1 | Streaming chat | Model gateway (OpenAI via Pydantic AI), conversation and message tables (tree), decoupled generation with a Redis Stream buffer, resume endpoint, cancel endpoint, chat UI (composer, messages, markdown/code/math, stop, auto-scroll), input limits, `max_tokens` | A reply streams on screen, survives a refresh, and Stop works (single local dev user) |
| 2 | Accounts | Better Auth (email + Google), JWT verification in FastAPI, protected routes, ownership checks, data isolation tests | Each user sees only their own chats |
| 3 | History sidebar | Conversation list with paging, auto titles, rename, delete, archive, pin | Sidebar works like ChatGPT's |
| 4 | Conversation controls | Edit message, regenerate, version switcher, model picker, custom instructions | Branching works end to end |
| 5 | Safety and operations | Rate limits, per-user token budgets, moderation, feedback (thumbs), structured logs, token/cost tracking | **MVP complete** |

## After the MVP

| Phase | Goal | Main pieces |
|---|---|---|
| 6 | Images and files | Uploads, file validation, vision input, PDF and document text extraction |
| 7 | Web search | Search tool with citations and a sources panel |
| 8 | Projects and memory | Projects with files and instructions, saved memories, pgvector search scoped per user |
| 9 | Voice | Dictation, read aloud, live voice over WebRTC (OpenAI Realtime, short-lived client tokens) |
| 10 | More chat features | Image generation, shared links (snapshots), temporary chats, data export |
| 11 | Tools | MCP tools with user consent, isolated code sandbox |

## Not planned

Features OpenAI has retired or is retiring: Canvas, a custom GPT store, group chats, Pulse-style daily feeds.
