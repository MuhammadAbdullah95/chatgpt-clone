# Contributing

Thanks for helping build the ChatGPT clone. This is a learning project: you practice how real open-source teams work. Take your time, and ask "why?" at every step.

## 1. Read first

| File | What it tells you |
|---|---|
| [README.md](README.md) | What the project is and how to run it |
| [AGENTS.md](AGENTS.md) | The rules: structure, git workflow, guardrails (for people and AI tools) |
| [docs/roadmap.md](docs/roadmap.md) | What we build, phase by phase |
| [docs/adr/](docs/adr/) | Why we chose this stack |
| [docs/security.md](docs/security.md) | How we keep users and keys safe |
| [docs/discussions/](docs/discussions/) | The full planning discussion from class |

## 2. Set up

Requirements: Docker, Node.js 24+, pnpm, uv, and make.

1. Fork this repository on GitHub (the **Fork** button, top right).
2. Clone your fork and add this repository as `upstream`:

   ```sh
   git clone https://github.com/<your-username>/chatgpt-clone.git
   cd chatgpt-clone
   git remote add upstream https://github.com/MuhammadAbdullah95/chatgpt-clone.git
   ```

3. Install everything and start the app:

   ```sh
   make setup   # git hooks, env files, dependencies
   make infra   # Postgres + Redis in Docker
   make dev     # API on :8000, web on :3000
   ```

## 3. Pick something to work on

- Browse the [issues](https://github.com/MuhammadAbdullah95/chatgpt-clone/issues). Start with ones labelled **good first issue**.
- Comment **"I'd like to work on this"** and wait to be assigned. One person per issue, so nobody's work is wasted.
- Check **Depends on** in the issue. Don't start until those issues are merged.
- Have your own idea, even something ChatGPT doesn't have? Open a **Feature request** issue first and discuss it before you write code.

## 4. Build it

1. Start from the latest `main`:

   ```sh
   git switch main
   git pull upstream main
   git switch -c feat/<short-name>   # or fix/, docs/, test/, chore/
   ```

2. Follow the structure and rules in `AGENTS.md`: feature folders, `user_id` on every query, no secrets in code.
3. Write tests for what you build.
4. Commit in small steps with clear messages, e.g. `feat: add chat rename`.
5. Before you push, run the same checks as CI:

   ```sh
   make check
   make images   # only if you changed docker/ or dependencies
   ```

## 5. Open a pull request

1. Push the branch to your fork: `git push -u origin feat/<short-name>`
2. Open a pull request into `main` of this repository. Fill in the template and write `Closes #<issue-number>`.
3. CI must pass. Fix anything it reports.
4. If GitHub says your branch is out of date, run `git pull upstream main` and push again.
5. I review it. Answer every comment, push fixes to the same branch, and resolve the conversations.
6. Once approved, it gets squash-merged.

Keep pull requests small: one feature or fix each.

## Using AI tools

You can use Claude Code, Cursor, Copilot, or any other AI tool. They read `AGENTS.md` automatically. But:

- **You own every line.** Read and understand all the code before you commit it. In review, I will ask why you wrote it that way.
- If the AI suggests something you don't understand, ask it "why?" until you do, or ask in the issue.
- Your work is in your name: no AI attribution in commits or pull requests.

## Be kind

Be respectful in issues, reviews, and chats. Everyone here is learning.
