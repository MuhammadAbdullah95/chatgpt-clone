# Security plan

How we keep the ChatGPT clone, its users, and its OpenAI bill safe. AI-specific risks follow the OWASP Top 10 for LLM Applications. Phases refer to [roadmap.md](roadmap.md).

## Top risks

1. **One user sees another user's chats.** ChatGPT had this in March 2023, when a Redis cache bug showed some users other people's chat titles.
2. **The OpenAI API key leaks.** Anyone could then spend our money.
3. **Runaway cost.** A bot or a user sends many requests and burns tokens.
4. **XSS through model output.** A reply contains HTML, a script, or a `javascript:` link that the browser runs.
5. **Prompt injection.** A web page, a file, or a user message tells the model to ignore its rules.

## Plan by layer

| Layer | What we do | Phase |
|---|---|---|
| Repo and code | Git hooks, branch protection, PR review (in place). GitHub secret scanning, Dependabot, `pip-audit` and `pnpm audit` in CI | 0 |
| Secrets | OpenAI key only in the backend `.env`, never sent to the browser. Monthly budget limit in the OpenAI dashboard. Voice uses short-lived client tokens minted by our server | 0, 9 |
| Accounts | Better Auth: hashed passwords, HttpOnly + Secure + SameSite cookies, Google login, login rate limits, email verification. FastAPI checks every JWT (signature, issuer, audience, expiry) | 2 |
| Data isolation | Every query is scoped by `user_id`. Every conversation, message, and file is checked for ownership. Cache keys include `user_id`. Automated tests prove user A cannot read user B's data | 2-3 |
| Web security | Model output is untrusted: markdown renders without raw HTML, `javascript:` links are blocked, CSP headers are set. SQLAlchemy parameterized queries. CORS allows only our frontend. SameSite cookies against CSRF | 1-2 |
| AI security | System prompt lives on the server and holds no secrets. Web and file content is treated as data, not instructions. Tools (MCP) run only with user consent. Code sandbox has no internet | 7, 11 |
| Cost and abuse | Rate limits per user and per IP (Redis), message length limits, `max_tokens`, daily token budget per user, one active reply per chat. Cloudflare Turnstile when deployed | 1, 5 |
| Content safety | OpenAI Moderation API on user input | 5 |
| Files | Check real file type (not just the extension), size limits, random storage names, never execute uploads, parse in a worker with timeouts | 6 |
| Privacy | Delete means hard delete from the database. Temporary chats delete themselves. Logs never hold full prompts or replies. Data export | 5, 10 |
| Memory and projects | Vector search always filters by `user_id` and project | 8 |
| Shared links | A share is a frozen snapshot behind an unguessable link, marked `noindex`, and can be revoked | 10 |
| Deployment | HTTPS, Cloudflare, database encryption at rest, backups | Deploy |

## Every PR

- Fill in the security items in the PR template.
- Run `/security-review` (Claude Code) on PRs that touch auth, files, sharing, or tools.
- Every security rule gets a test.

## Priorities while running locally

Bots and DDoS matter only once the app is on the internet. Until then, focus on data isolation, key safety, XSS, and cost limits.
