# ChatGPT Backend: Languages, Streaming, Conversation Storage, Auth & Sessions

Research date: 2026-11-22. Public sources only. No login to chatgpt.com, no private API calls were made.

Confidence tags used on every claim:
- **Confirmed**: OpenAI said it officially (engineering blog, docs, help center, status-page postmortem, job posting).
- **Reported**: credible third party (tech press, interviews in third-party outlets, reverse-engineering write-ups, open-source projects).
- **Inferred**: my own reasoning from indirect evidence.

Source-quality note: ChatGPT's web backend API (`/backend-api/...`) is undocumented and private. Everything about its wire format comes from community reverse-engineering, and it changes often (the path itself moved from `/backend-api/conversation` to `/backend-api/f/conversation` between 2023-2025 reports and 2026 reports). Treat every web-API detail as a snapshot with a date, not a stable contract.

---

## 1. Backend languages and frameworks

### Takeaway
ChatGPT's application backend is mainly **Python (asyncio) with FastAPI**. Around it sit some **C** for hot paths, **Temporal** for durable async workflows, **Kubernetes** on **Azure**, and **Redis Cluster** for caching. Job postings also name Go, Rust and C++ as accepted backend languages, but no official source says that any core ChatGPT request path is written in Go or Rust.

### Cited Findings
- **Confirmed (Mar 24, 2023):** ChatGPT's server is Python running on asyncio. OpenAI: "We use the redis-py library to interface with Redis from our Python server, which runs with Asyncio." The bug behind the March 20, 2023 outage was in "the Asyncio redis-py client for Redis Cluster". — [OpenAI, March 20 ChatGPT outage](https://openai.com/index/march-20-chatgpt-outage/)
- **Reported (May 13, 2025; OpenAI leaders on record):** "Under the hood the infrastructure is mostly Python and FastAPI! They're also using some C, and Temporal as a workflow engine." This is Simon Willison's summary of Gergely Orosz's Pragmatic Engineer interview with Sulman Choudhry (head of engineering, ChatGPT) and Srinivas Narayanan (VP engineering, OpenAI). — [Simon Willison](https://simonwillison.net/2025/May/13/launching-chatgpt-images/); original (paywalled): [The Pragmatic Engineer, "Building, launching, and scaling ChatGPT Images"](https://newsletter.pragmaticengineer.com/p/chatgpt-images)
- **Reported (May 2025):** In the same interview, C is used for performance-sensitive paths where Python overhead matters, and Temporal keeps multi-step async workflows reliable when individual steps fail. — [ZenML LLMOps database summary](https://www.zenml.io/llmops-database/scaling-image-generation-to-100m-new-users-in-one-week); [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/chatgpt-images)
- **Confirmed (job posting; seen via search summary, date not shown):** The OpenAI "Backend Software Engineer (Evals)" posting says the stack includes Python, FastAPI and Postgres. — [openai.com/careers, Backend SWE (Evals)](https://openai.com/careers/backend-software-engineer-(evals)-san-francisco/)
- **Confirmed (job posting via aggregator; seen via search summary):** A "Backend Software Engineer, ChatGPT Engineering" listing asks for "backend languages (e.g., Go, Python, Rust, C++)". — [Built In listing](https://builtin.com/job/backend-software-engineer-chatgpt-engineering/8383312)
- **Confirmed (job posting, fetched 2026-11-22):** The ChatGPT Infrastructure team "builds and operates the platforms that enable fast iteration". It asks for "caching, consistency, queueing/backpressure" and "rate limiting, load shedding, dependency isolation, backpressure". The posting names no specific language or framework. — [openai.com/careers, SWE ChatGPT Infrastructure](https://openai.com/careers/software-engineer-chatgpt-infrastructure-san-francisco/)
- **Confirmed (Jan 22, 2026):** The ChatGPT PgBouncer tier runs as Kubernetes deployments: "Each replica has its own Kubernetes deployment of multiple PgBouncer pods behind a shared Kubernetes Service." The post refers to ORMs generically but does not name a language or ORM. — [OpenAI, Scaling PostgreSQL to power 800 million ChatGPT users](https://openai.com/index/scaling-postgresql/)
- **Confirmed (Dec 2024 postmortem):** All OpenAI services, ChatGPT included, run on large Kubernetes clusters. On Dec 11, 2024, from 3:16 PM to 7:38 PM PST, a new telemetry service made resource-intensive Kubernetes API calls that overwhelmed the API servers and took down the control plane. ChatGPT recovered around 6:50 PM PST. — [OpenAI status write-up](https://status.openai.com/incidents/ctrsv3lwd797/write-up); [TechCrunch, Dec 13, 2024](https://techcrunch.com/2024/12/13/openai-blames-its-massive-chatgpt-outage-on-a-new-telemetry-service)
- **Confirmed (Jan 25, 2021; research infra, not ChatGPT-specific):** OpenAI ran Kubernetes clusters of 7,500 nodes for research workloads (GPT-3, CLIP, DALL·E). — [OpenAI, Scaling Kubernetes to 7,500 nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)
- **Reported (May 2025):** For ImageGen in March 2025, OpenAI "addressed the early scaling challenge by adding an asynchronous queue to defer the load for their free users". The launch added 100M new users in the first week and one million in a single hour. — [Simon Willison](https://simonwillison.net/2025/May/13/launching-chatgpt-images/)

### Inferences
- **Inferred:** Python/FastAPI on asyncio fits ChatGPT's workload. Most of a request's wall time is spent waiting on the model-inference service while streaming tokens, which is I/O-bound. A clone can use FastAPI or Starlette with async streaming responses, or Node or Go. The language matters less than having a non-blocking streaming path.
- **Inferred:** Go and Rust appear in postings but not in official ChatGPT architecture descriptions. They are probably used for specific infra components or other products (for example, OpenAI's Rust Codex CLI), not the main ChatGPT API tier. No source confirms this either way.
- **Inferred:** A clone should use a durable workflow engine (Temporal, or a queue plus worker) for slow, multi-step jobs such as image generation, file processing and deep research. Simple text chat can stay on the synchronous streaming path.

### Gaps
- No official 2026 OpenAI post describes the full ChatGPT service topology (gateway, conversation service, inference router). The Pragmatic Engineer article is paywalled; only secondary summaries were read.
- The ORM was not identified. The PostgreSQL post mentions "ORM-generated SQL" without naming it (SQLAlchemy is plausible for Python but unconfirmed).
- No source said whether the main ChatGPT backend is a monolith or microservices.

---

## 2. Streaming: how the ChatGPT web app receives a streamed answer (plus the public API as reference)

### Takeaway
ChatGPT's web client sends a **POST** to a conversation endpoint. Per reports, that is `/backend-api/conversation` in 2023-2025 and `/backend-api/f/conversation` in 2026. The response is an **SSE-formatted (`text/event-stream`) body**, read with `fetch()` plus a `ReadableStream` reader rather than the browser `EventSource`. In 2023 each event carried the **full cumulative message**. By 2026 the stream uses **`delta_encoding: "v1"`**, a JSON-Patch-like format: `append` operations on `/message/content/parts/0`, followed by compact `{"v":"..."}` continuation deltas. The public OpenAI API also uses SSE, with typed semantic events and **resumable streams** (`sequence_number` plus `starting_after`). No public source documents how the ChatGPT web app resumes a stream after a reload.

### Cited Findings
**ChatGPT web app (all Reported, private/undocumented API):**
- **Reported (Aug 25, 2025):** The web UI sends `POST /backend-api/conversation` and reads the response as a stream. ChatGPT "doesn't use `EventSource`" and "has its own lightweight solution" (a fetch body reader). DevTools' EventStream tab shows nothing. Each chat has a conversation ID, and messages carry a message ID and a `parent_message_id`. IDs are random UUIDs. Other listed endpoints are `/session`, `/conversations?offset=0&limit=20`, and `/message_feedback`. — [Ahmed Abdeltwab, "How ChatGPT Uses SSE Internally"](https://ahmed-n-abdeltwab.github.io/blog/2025/08/25/chatgpt-sse-architecture.html)
- **Reported (Mar 2023):** In 2023 the web stream sent the *full text so far* in every event (`parts[0]` grows), unlike the public API's incremental deltas. Clients computed deltas themselves. — [hideaway blog, "ChatGPT web to API" (Mar 2023)](https://hideaway-7r8.pages.dev/en/posts/2023/03/chatgpt-web-to-api/)
- **Reported (Sep 15, 2026):** The endpoint is now `POST /backend-api/f/conversation`. The response is "an SSE-style stream using `delta_encoding` `v1` and structured message/delta events". Visible text arrives as "append operations to `/message/content/parts/0`" followed by "compact `{"v":"..."}` continuation deltas". Message metadata includes `author.role` (`assistant`), `recipient` (`"all"`) and `channel` (`"commentary"` or `"final"`). The full op set is still "unverified". — [GitHub issue, AgentPanelSpeaker.NET #115](https://github.com/Ma-XX-oN/AgentPanelSpeaker.NET/issues/115)
- **Reported (Nov 19, 2026):** The request body includes `action`, `messages`, `parent_message_id`, `model`, `conversation_mode`, `supported_encodings: ["v1"]` and `timezone`. The reply is SSE with `delta_encoding` `v1` carrying `delta` patches. Before the main POST, the client calls `POST /sentinel/chat-requirements/prepare` and sends `OpenAI-Sentinel-Chat-Requirements-Prepare-Token` and `OpenAI-Sentinel-Proof-Token` headers (a proof-of-work anti-abuse step). — [GitHub issue, codex-gpui #1528](https://github.com/i098/codex-gpui/issues/1528)
- **Reported (2026, date not captured):** An open-source client proposes parsing v1 operations `add`, `append`, `replace`, `remove` and `patch`, with JSON-Pointer paths. — [GitHub issue, dsh-chatgpt-web #11](https://github.com/WLV-ZEDD/dsh-chatgpt-web/issues/11)
- **Reported (2023-2025):** Older proxy code checks for chunks beginning with `event: delta`, which points to named SSE events. Older write-ups show requests with `Accept: text/event-stream` and a Bearer token. — [search summary of HF-hosted reverse proxy and older write-ups](https://huggingface.co/spaces/deeme/c2a/blob/main/gateway/reverseProxy.py)

**Public OpenAI API (reference design, Confirmed):**
- **Confirmed (docs, fetched 2026-11-22):** "This guide focuses on HTTP streaming (`stream=true`) over server-sent events (SSE)." Events are "typed with a predefined schema". Common text events are `response.created`, `response.output_text.delta`, `response.completed` and `error`. Others include `response.output_item.added/done`, `response.content_part.added/done`, `response.function_call_arguments.delta/done` and `response.refusal.delta`, plus file-search and code-interpreter progress events. Text arrives in `event.delta`. A separate **WebSocket mode** is described as a persistent transport with incremental inputs via `previous_response_id`. Moderation scores arrive only after the full output. — [OpenAI Streaming API responses guide](https://developers.openai.com/api/docs/guides/streaming-responses)
- **Confirmed (API reference, fetched 2026-11-22):** The Responses streaming events reference includes a `response.compaction.compacting` event, which shows server-side context compaction exists in the API. — [Responses streaming events reference](https://developers.openai.com/api/reference/resources/responses/streaming-events)
- **Confirmed (docs, fetched 2026-11-22):** Resumable streams work via background mode. Set `background: true` and save the response ID. "If the connection drops, resume the stream by passing the last event's `sequence_number` as `starting_after`", for example `curl "https://api.openai.com/v1/responses/resp_123?stream=true&starting_after=42"`. Polling statuses are `queued` and `in_progress`, then a terminal state. Cancel with `POST /v1/responses/{id}/cancel` (idempotent). "You can't stream a response later if it was created without streaming." "Background mode temporarily stores response data even when you set `store` to `false`." — [OpenAI Background mode guide](https://developers.openai.com/api/docs/guides/background)
- **Confirmed (OpenAI docs) and Reported (terminator detail):** Chat Completions with `stream=True` returns "data-only server-sent events" of type `chat.completion.chunk`. OpenAI recommends the Responses API for streaming. Third-party docs state that the stream ends with the literal `data: [DONE]` sentinel. — [OpenAI Chat Completions streaming events](https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events); [Vercel AI Gateway docs](https://vercel.com/docs/ai-gateway/sdks-and-apis/openai-chat-completions/streaming)

### Inferences
- **Inferred:** ChatGPT uses `fetch` instead of `EventSource` because `EventSource` only supports GET and cannot send a JSON body or custom auth and sentinel headers. A clone should do the same: POST the user turn and parse SSE frames from `response.body.getReader()`, or use a library such as `@microsoft/fetch-event-source`.
- **Inferred:** The move from cumulative full-text events (2023) to `delta_encoding v1` patches (2026) saves bandwidth on long answers, which grows O(n²) with cumulative resends. It also lets one stream update several message fields (content, status, metadata, tool calls). A clone can copy this cheaply. Send an initial "message" event with the full message skeleton, then small `{p, o, v}` patch events (path, op, value), with a shorthand `{v}` meaning "append to the last path".
- **Inferred (resume design):** For page reload or network drop, the public API's design is the best public blueprint. Generate in a server-side job decoupled from the HTTP connection. Assign a monotonically increasing `sequence_number` to every event and buffer events (for example in Redis Streams). Let clients reconnect with `starting_after=N`. ChatGPT's web client probably does something similar, since replies are persisted server-side under a message ID, but this is unverified.
- **Inferred:** The sentinel and proof-of-work step is ChatGPT's abuse defence on the chat endpoint, separate from auth. A clone open to anonymous users needs some equivalent (captcha, PoW, or per-IP rate limits).

### Gaps
- No public, credible source documents how the ChatGPT **web app** resumes an in-flight stream after reload or network loss (endpoint, cursor, or whether it polls the finished message). The search of the help-center release notes found nothing for text responses.
- No verified source in this session confirms whether the 2026 ChatGPT web stream still ends with a literal `data: [DONE]` line, or what the exact names of the final events are (for example `message_stream_complete`).
- No public evidence shows the ChatGPT **web** app using WebSockets for text chat. Voice and realtime features may use WebRTC or WebSocket, but that is outside this scope and was not verified.
- The exact full v1 op set and payload examples were not captured verbatim from any fetched page.

---

## 3. Conversation data model (tree of messages)

### Takeaway
A ChatGPT conversation is stored as a **tree (DAG) of message nodes**. The best public evidence is the official data export, `conversations.json`, now split into `conversations-N.json`. Each conversation has a `mapping` of node-id to node, where each node has `{id, parent, children[], message}`. A `current_node` points to the active leaf. Edits and regenerations create **sibling branches**. The visible thread is rebuilt by walking `parent` links from `current_node` to the root and reversing the list. OpenAI has not published a formal spec; field lists come from third-party parsers.

### Cited Findings
- **Reported (2026 parser docs):** Conversation fields: `id`, `conversation_id`, `title`, `create_time` (float, epoch seconds), `update_time`, `current_node`, `default_model_slug`, `mapping: dict[str, Node]`. — [chatgpt-to-markdown data models](https://difegam.github.io/chatgpt-to-markdown/reference/data-models)
- **Reported (2026):** Node fields: `id`, `parent: str | None`, `children: list[str]`, `message: Message | None`. Message fields: `id`, `author` (roles `system`, `user`, `assistant`, `tool`), `content` (a union discriminated by `content_type`), `channel`, `recipient`, `create_time`, `status`, `weight`, `metadata`. — [chatgpt-to-markdown data models](https://difegam.github.io/chatgpt-to-markdown/reference/data-models)
- **Reported (2026):** `content_type` values include `text` (`parts: list[str]`), `multimodal_text` (`parts` mixing strings and `AssetPointer`s), `code`, `thoughts`, `reasoning_recap`, `execution_output`, `tether_quote`, `tether_browsing_display`, `sonic_webpage`, `system_error`, `computer_output` and `user_editable_context`. Files and images are referenced via `AssetPointer {asset_pointer, content_type: "image_asset_pointer", width, height, size_bytes}` and `metadata.attachments[] {id, name, size, ...}`. The export also has `user.json`, `message_feedback.json` (`rating: thumbs_up|thumbs_down`) and an export manifest. — [chatgpt-to-markdown data models](https://difegam.github.io/chatgpt-to-markdown/reference/data-models)
- **Reported (2026):** The export files are JSON arrays split into partitions (`conversations-0.json`, `conversations-1.json`, ...). The root node has `parent: null` and `message: null`. "The linearizer walks from current_node back to the root to reconstruct the conversation timeline." — [chatgpt-to-markdown export format](https://difegam.github.io/chatgpt-to-markdown/explanation/export-format)
- **Reported (2026):** "Your ChatGPT history is a tree, not a transcript." Regenerations create sibling children under the same parent, and edits of earlier user messages create new branches. — [Level Up Coding (2026)](https://levelup.gitconnected.com/your-chatgpt-history-is-a-tree-not-a-transcript-2026-5660ceb301d4); [OpenAI community forum: parsing conversations.json](https://community.openai.com/t/decoding-exported-data-by-parsing-conversations-json-and-or-chat-html/403144)
- **Reported (Nov 2026):** The live chat request sends `parent_message_id`, which ties each new turn to a specific node of the tree. — [codex-gpui #1528](https://github.com/i098/codex-gpui/issues/1528); [Abdeltwab, Aug 2025](https://ahmed-n-abdeltwab.github.io/blog/2025/08/25/chatgpt-sse-architecture.html)
- **Reported (2026):** No official OpenAI specification of the export format exists. A 2026 forum user asked whether it is documented and got no official answer. — [search summary of OpenAI community threads](https://community.openai.com/t/decoding-exported-data-by-parsing-conversations-json-and-or-chat-html/403144)

### Inferences
- **Inferred (clone schema):** `conversations(id, user_id, title, current_node_id, default_model, is_archived, created_at, updated_at)` plus `messages(id, conversation_id, parent_id NULL, role, content_type, content JSONB, channel, recipient, status, metadata JSONB, created_at)`. Children can be derived with an index on `(conversation_id, parent_id)`. An edit inserts a new user node under the edited node's parent. A regenerate inserts a new assistant node under the same user node. Both update `current_node_id`.
- **Inferred:** `channel` (`commentary` / `final`) and `recipient` (`all` vs a tool name) indicate that tool calls, reasoning summaries and final answers are all stored as nodes in the same tree. The UI hides some of them.
- **Inferred:** The export's assistant nodes include a `weight` field. Combined with `end_turn` metadata, this is likely how hidden or system nodes are kept out of model context. Unverified.

### Gaps
- No official schema. Field names may differ between export versions and the live API.
- Not found: how branches are stored server-side (one document per conversation vs. one row per message). The export's single-document shape hints at document storage but does not prove it.

---

## 4. Databases and storage

### Takeaway
**Confirmed (Jan 22, 2026):** ChatGPT's core relational store is **one unsharded Azure Database for PostgreSQL Flexible Server primary** with **nearly 50 read replicas across multiple regions**. It sits behind **PgBouncer on Kubernetes** with a **cache layer using lock/lease stampede protection**, serves **millions of QPS** for **800M users**, has **low double-digit ms p99** and **five-nines availability**. Shardable, write-heavy workloads were moved to **Azure Cosmos DB**, and new tables are no longer added to Postgres. **Redis Cluster** caches user info (Confirmed, 2023). No official source names the blob store for uploaded files.

### Cited Findings
All of the following come from **Confirmed (Jan 22, 2026, Bohan Zhang, Member of Technical Staff)** [OpenAI: Scaling PostgreSQL to power 800 million ChatGPT users](https://openai.com/index/scaling-postgresql/) unless another source is named:
- Scale: 800 million ChatGPT users. "Millions of queries per second" for read-heavy workloads. PostgreSQL load "has grown by more than 10x" over the past year.
- Topology: Azure PostgreSQL flexible server, **single primary** plus **nearly 50 read replicas across multiple regions**. Writes are not sharded in PostgreSQL. The primary runs in HA mode with a hot standby, and each region has multiple replicas with spare capacity. Replication lag is kept near zero.
- Write offload: shardable write-heavy workloads were migrated to **Azure Cosmos DB**. New tables are no longer added to PostgreSQL, and new workloads default to sharded systems. Sharding PostgreSQL itself is "not a near-term priority".
- Primary load reduction: read traffic goes to replicas where possible. Redundant writes were fixed, lazy writes added, and backfills strictly rate-limited (some take more than a week).
- Query hygiene: one query joining 12 tables was linked to past SEVs. Multi-table joins are avoided, and join logic moves into the application. ORM-generated SQL is reviewed. `idle_in_transaction_session_timeout` is used to kill idle transactions.
- Workload isolation: requests are split into low-priority and high-priority tiers on separate instances.
- Connection pooling: PgBouncer in statement or transaction pooling mode. Azure PG's limit is 5,000 connections. Average connection time fell from 50 ms to 5 ms. Each replica has its own Kubernetes deployment of PgBouncer pods behind a shared Kubernetes Service.
- Caching: a cache locking/leasing mechanism ensures only one reader fetches a missed key from PostgreSQL (thundering-herd protection). The cache technology is not named in the post.
- Rate limiting at the application, connection pooler, proxy and query layers. The ORM layer can block specific query digests. Retry intervals should not be too short.
- Schema changes: only lightweight changes, a strict 5-second timeout, and concurrent index create/drop allowed.
- Future: cascading replication, in testing with Azure, could allow more than 100 replicas.
- Results: low double-digit millisecond p99 client-side latency, five-nines availability, and only one SEV-0 in 12 months. That SEV-0 happened during the ChatGPT ImageGen launch, when write traffic rose more than 10x as more than 100M users signed up within a week.
- The author has also written about PostgreSQL MVCC pain (write and read amplification, bloat, autovacuum tuning) with Prof. Andy Pavlo (CMU), "The Part of PostgreSQL We Hate the Most".

Other sources:
- **Reported (Feb 2026):** InfoQ confirms the single primary with nearly 50 geo-distributed read replicas on Azure Database for PostgreSQL. — [InfoQ](https://www.infoq.com/news/2026/02/openai-runs-chatgpt-postgres)
- **Reported (Microsoft, 2026, partner source):** Microsoft's Azure Postgres team says geo-distributed replicas occasionally saw replication lag before a launch, and that read-scale fixes "did not help address the growing write scale". It points to Azure HorizonDB for write scaling. — [Microsoft Tech Community, "Supporting ChatGPT on PostgreSQL in Azure"](https://techcommunity.microsoft.com/blog/ADforPostgreSQL/supporting-chatgpt-on-postgresql-in-azure/4490247)
- **Confirmed (Mar 24, 2023):** "We use Redis to cache user information in our server so we don't need to check our database for every request." "We use Redis Cluster to distribute this load over multiple Redis instances." After the incident OpenAI added "checks to confirm cached data belongs to the requesting user". — [OpenAI, March 20 ChatGPT outage](https://openai.com/index/march-20-chatgpt-outage/)
- **Confirmed (Mar 24, 2023):** The cache held data used for the chat-history sidebar. The bug let some users see "other active users' chat titles" and possibly the first message of a new conversation. — [OpenAI, March 20 ChatGPT outage](https://openai.com/index/march-20-chatgpt-outage/)

### Inferences
- **Inferred:** Given "new workloads default to sharded systems", high-volume, per-user, append-heavy data is the most likely candidate for Cosmos DB, partitioned by user or conversation ID. That covers conversation and message records, memory items and feedback. OpenAI has **not** said which tables moved, so this is a guess.
- **Inferred:** The cache in the 2026 post is probably still Redis, given the 2023 Redis Cluster disclosure, but the 2026 post doesn't name it.
- **Inferred (clone design):** Start with a single Postgres (plus a read replica later), a connection pooler (PgBouncer or the platform's), Redis for session and user caching with stampede locks, and object storage (S3, Azure Blob or R2) for uploads referenced by ID, mirroring the export's `asset_pointer`. Partition messages by `conversation_id` from day one so they can move to a sharded store later. Keep joins in application code and set statement and idle-transaction timeouts.
- **Inferred:** Because OpenAI runs on Azure, Azure Blob Storage for file uploads and generated images is plausible, but unconfirmed.

### Gaps
- No official source names the store for uploaded files and images (blob storage), or the vector store used for memory or "reference chat history".
- It is unconfirmed which exact ChatGPT entities live in PostgreSQL vs Cosmos DB.
- I did not access OpenAI's PGConf.dev 2025 talk (Bohan Zhang), which may contain more numbers.

---

## 5. Chat history sidebar (server side): listing, pagination, titles

### Takeaway
Per reports, the sidebar is filled by a **paginated, offset/limit list endpoint**, `GET /backend-api/conversations?offset=0&limit=N`, that returns conversation summaries (id, title, timestamps), with titles stored per conversation. Official evidence is limited to the 2023 postmortem: chat titles were served through the Redis-cached path and the history sidebar.

### Cited Findings
- **Reported (Aug 25, 2025):** The client calls `/conversations?offset=0&limit=20` for the history list, with `/conversation` for the chat itself, `/session`, and `/message_feedback`. — [Abdeltwab, "How ChatGPT Uses SSE Internally"](https://ahmed-n-abdeltwab.github.io/blog/2025/08/25/chatgpt-sse-architecture.html)
- **Confirmed (Mar 24, 2023):** Users "could see titles from another active user's chat history" in the sidebar. This shows that sidebar titles are a server-side per-user list, delivered through the Python plus Redis path. — [OpenAI, March 20 ChatGPT outage](https://openai.com/index/march-20-chatgpt-outage/)
- **Reported (2026):** Each exported conversation carries `title`, `create_time` and `update_time`, so titles are persisted fields on the conversation record. — [chatgpt-to-markdown data models](https://difegam.github.io/chatgpt-to-markdown/reference/data-models)
- **Confirmed (help center):** Turning off "Reference chat history" schedules derived memory for deletion within 30 days, but "the original chats remain in your history unless you delete them". This shows chat history and memory are stored separately. — [OpenAI Help: How does Reference saved memories work](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work); [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)

### Inferences
- **Inferred:** Titles are generated by a small model call after the first exchange, then saved to the conversation row and pushed to the client (sidebar entries show a placeholder first). A clone can do this asynchronously after the first assistant reply.
- **Inferred (clone design):** Use keyset or cursor pagination on `(user_id, updated_at DESC, id)` rather than OFFSET for large histories. Keep the list query on a read replica or cache, and invalidate a per-user list cache on new messages. Always key cache entries by user ID and verify ownership, which is the lesson of the 2023 incident.

### Gaps
- No verified current (2026) path, page size, sort order or cursor format for the sidebar endpoint. The `offset/limit` detail is from one 2025 write-up.
- No source documents how titles are generated (model, timing, endpoint).
- Projects, folders, archive and pinned-chat server APIs were not researched.

---

## 6. Auth, sessions, rate limiting and message caps

### Takeaway
ChatGPT login supports **email/password and Google, Microsoft and Apple** social login. Accounts are bound to the sign-up method. The identity issuer is **`https://auth.openai.com`**, which in 2026 also acts as an **OAuth 2.0 / OIDC provider** for "Sign in with ChatGPT" (Authorization Code + PKCE). The domain was historically Auth0-backed (Reported/Inferred from an `auth0.openai.com` workaround), and the current vendor is unverified. Per reports, the web client holds a **long-lived session/refresh cookie** and uses a **short-lived Bearer access token** for backend API calls. As of Nov 2026, Free and Go users have **"unlimited everyday text chats, subject to abuse-prevention safeguards"**, while Thinking and Pro models have per-plan, often weekly, limits with model fallback.

### Cited Findings
- **Confirmed (help center):** If you signed up with Google, Microsoft or Apple you must keep using that method. Email/password accounts can later use a social login if the email matches. Apple "Hide My Email" relay accounts need the same Apple ID. You cannot change the login method of an existing account. SMS is not an alternative to email-based login. — [OpenAI Help: Can I change my authentication method?](https://help.openai.com/en/articles/4936824-can-i-change-my-authentication-method); [OpenAI Help: Why can't I log in to ChatGPT?](https://help.openai.com/en/articles/7426629-why-cant-i-log-in-to-chatgpt)
- **Reported (Oct 4, 2026, citing OpenAI docs and Sep 29, 2026 release notes):** "Sign in with ChatGPT" uses OAuth 2.0 Authorization Code with PKCE plus OpenID Connect. The discovery document is at auth.openai.com with issuer `https://auth.openai.com`. Scopes are `openid`, `profile`, `email`, and client IDs start with `oaiapp_`. Partner apps receive name, email and profile picture, but no conversations or memory. The feature is a limited trial with launch partners Airtable, Canva, GitLab, HubSpot and Supabase. — [MIXED News](https://mixed-news.com/en/?p=35164)
- **Reported (2024-2025, user anecdotes):** Users fixing login failures by changing `auth.openai.com` to `auth0.openai.com` suggests the login domain was fronted by Auth0. No official OpenAI statement found. — [Mozilla Support thread](https://support.mozilla.org/id/questions/1469068); [OpenAI community: SSO info error](https://community.openai.com/t/cant-fix-this-error-welcome-back-something-went-wrong-while-getting-your-sso-info/934573)
- **Reported (Aug 25, 2025):** Auth uses "a refresh token in a cookie plus a short-lived bearer access token", and expiry causes 403s. Backend calls send `Authorization: Bearer <access-token>`. — [Abdeltwab](https://ahmed-n-abdeltwab.github.io/blog/2025/08/25/chatgpt-sse-architecture.html)
- **Reported (Nov 19, 2026):** Separate from auth, chat POSTs need anti-abuse "sentinel" tokens. A `POST /sentinel/chat-requirements/prepare` returns a token, and the client sends `OpenAI-Sentinel-Chat-Requirements-Prepare-Token` plus a proof-of-work `OpenAI-Sentinel-Proof-Token` header. — [codex-gpui #1528](https://github.com/i098/codex-gpui/issues/1528)
- **Confirmed (help center, fetched 2026-11-22; page titled "GPT-6 and other models in ChatGPT"):** "Free and Go users have unlimited everyday text chats, subject to abuse-prevention safeguards." Limits for file uploads, image generation, voice and data analysis are separate. Thinking limits depend on plan. "If you reach a Thinking limit, ChatGPT may continue with another available model." GPT-6 Pro has weekly limits. On Pro $200, hitting the weekly limit switches to GPT-5.6 Thinking (Medium). On Pro $100, GPT-6 Pro and GPT-5.6 Sol Pro share one weekly allowance. ChatGPT shows the reset time when available. — [OpenAI Help: models in ChatGPT](https://help.openai.com/en/articles/11909943-gpt-52-in-chat)
- **Confirmed (earlier 2026 version of the same article, via search snippet; superseded):** Earlier, Free users had limited GPT-5.5 access "within a 5-hour window", with limits that "can be dynamic". — [OpenAI Help (GPT-5.5 version)](https://help-lb.openai.com/en/articles/11909943-gpt-55-in-chatgpt). Third-party sites reported Free/Plus caps of 10/160 messages per window in early 2026, conflicting with later "unlimited" wording. — [ai-toolbox](https://ai-toolbox.co/chatgpt-management-and-productivity/chatgpt-limits-messages-tokens-rate-2026); [Engadget (Aug 2026)](https://engadget.com/2234173/chatgpt-free-features-2026)
- **Confirmed (Jan 22, 2026):** Server-side rate limiting is layered across the application, connection pooler, proxy and query layers. — [OpenAI, Scaling PostgreSQL](https://openai.com/index/scaling-postgresql/)
- **Confirmed (job posting):** The ChatGPT Infrastructure team owns "rate limiting, load shedding, dependency isolation, backpressure". — [openai.com/careers](https://openai.com/careers/software-engineer-chatgpt-infrastructure-san-francisco/)

### Inferences
- **Inferred (clone design):** Use a hosted IdP or library (Auth0, Clerk, Supabase Auth, Auth.js) with Google, Microsoft and Apple OIDC. Use an HttpOnly, Secure, SameSite session or refresh cookie, and short-lived access tokens (JWT) for API calls. Refresh tokens silently, and return 401/403 on expiry. Store usage counters per user, plan and model in Redis with sliding windows (for example a 5-hour window or weekly), and fall back to a cheaper model instead of hard-blocking. That matches the documented fallback behavior.
- **Inferred:** Separating "auth" (who you are) from "sentinel" (is this a real browser/human) is a deliberate design. Rate limits keyed only by account do not stop scripted abuse of free tiers.

### Gaps
- **Unverified:** whether auth.openai.com still runs on Auth0 in 2026, or on an in-house identity service. No official statement was found either way.
- No official documentation of ChatGPT web session cookie names, token lifetimes or refresh flow. A search for those specifics was declined by the search tool as it touches session-credential reuse, and I did not pursue it further.
- Passkey support was not confirmed by any source found.
- Exact current numeric caps for Thinking models per plan are on separate help articles (Business, Enterprise/Edu, Rate Card) that were not fetched.

---

## 7. Context-window management for long conversations

### Takeaway
OpenAI publishes **per-plan context windows** for ChatGPT, which change with each model generation, and documents **memory** ("Reference saved memories" and "Reference chat history") as the mechanism for carrying information across chats. It does **not** officially document how ChatGPT truncates or summarizes a single long conversation. The public API's Responses streaming reference includes a **`response.compaction.compacting`** event, so OpenAI does have server-side context compaction at the API level.

### Cited Findings
- **Confirmed (earlier 2026 help article, via search snippet; superseded by GPT-6 page):** Instant context windows were Free 16K, Plus/Business 32K, Pro/Enterprise 128K. The current (Nov 2026) version of the page does **not** list context windows. — [OpenAI Help (GPT-5.5 version)](https://help-lb.openai.com/en/articles/11909943-gpt-55-in-chatgpt); [current page](https://help.openai.com/en/articles/11909943-gpt-52-in-chat)
- **Reported (2026, third-party, unverified):** Newer figures circulate: Instant 27K on Free, 54K on Go/Plus/Business, 128K on Pro/Enterprise, and reasoning models at 256K on Plus and 400K on Pro. — [ai-toolbox context windows 2026](https://www.ai-toolbox.co/chatgpt-models/chatgpt-context-window-token-limits-2026)
- **Confirmed (help center):** "Reference chat history" lets ChatGPT use relevant information from past conversations. That information "can change as ChatGPT updates what is most useful to remember". Turning it off schedules deletion within 30 days. Saved memories are stored separately from chat history, and deleting a chat does not delete a saved memory. There is no separate storage limit for what can be referenced via chat history. — [OpenAI Help: How does Reference saved memories work](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work); [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq); [How does memory use past conversations](https://help.openai.com/en/articles/10303002-how-does-memory-use-pastconversations)
- **Confirmed (API reference, fetched 2026-11-22):** The Responses API streaming events include `response.compaction.compacting`. — [Responses streaming events](https://developers.openai.com/api/reference/resources/responses/streaming-events)
- **Confirmed (API docs):** The Responses API WebSocket mode and stateful chaining use `previous_response_id`, which means the server holds conversation state and the client does not resend the history. — [OpenAI Streaming guide](https://developers.openai.com/api/docs/guides/streaming-responses)

### Inferences
- **Inferred:** In ChatGPT, when a conversation exceeds the plan's context window, older turns are dropped or compacted (summarized) server-side, and memory and retrieval re-inject relevant facts. The API's compaction event makes summarization-based compaction likely for ChatGPT too, but OpenAI hasn't documented ChatGPT's exact policy.
- **Inferred (clone design):** Build the prompt from the active branch only (walk `current_node` to the root). Apply a token budget per plan. Keep the system prompt, memory block and last N turns verbatim. Replace older turns with a rolling summary stored as a hidden node (like `weight=0`) or a conversation-level field. Retrieve from past chats via embeddings if offering "reference chat history".

### Gaps
- No official documentation of ChatGPT's in-conversation truncation or summarization behavior or thresholds.
- Current (Nov 2026) per-plan context windows for GPT-6-era models were not found on an official page.
- How memory retrieval is implemented (vector DB, embeddings model, ranking) is undocumented.
