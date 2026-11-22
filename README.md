# ChatGPT Clone

A chat app where the user sends a message and gets an AI reply.

**Status:** Tech stack decided: Next.js + FastAPI + OpenAI ([ADR-0001](docs/adr/0001-tech-stack.md)). Building starts with Phase 0 of the [roadmap](docs/roadmap.md).

## Setup after cloning

Turn on the project's git hooks (they protect `main` and block secrets):

```sh
git config core.hooksPath .githooks
```

## How we work

- `main` is protected. All work happens on a branch and reaches `main` through a reviewed pull request.
- Full workflow and rules: [`AGENTS.md`](./AGENTS.md).

## For AI agents

Read [`AGENTS.md`](./AGENTS.md) before making any change.
