# ChatGPT Clone

A chat app where the user sends a message and gets an AI reply.

**Status:** Repo setup done. Tech stack not decided yet.

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
