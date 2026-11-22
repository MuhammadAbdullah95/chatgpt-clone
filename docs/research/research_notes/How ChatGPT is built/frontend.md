# ChatGPT Web Frontend (chatgpt.com): Stack and Chat UI Behavior

_Research date: 2026-11-22. Confidence tags: **[Confirmed]** = OpenAI said it officially (blog, help center, careers page). **[Reported]** = credible third-party write-up, reverse-engineering, community forum, or tech press. **[Inferred]** = my reasoning from indirect evidence. OpenAI has never published an engineering post describing the chatgpt.com web stack; almost everything about the web client below is **[Reported]** from outside inspection. The single richest source is Dennis Brotzky, "Reverse Engineering ChatGPT Web: How OpenAI Built for a Billion Users", performance.dev, **2026-07-02** (the author states he does not work at OpenAI and has not seen the source; findings come from page HTML, JS, CSS, and network traffic)._

## 1. Which framework does chatgpt.com use today, and what did it use before?

### Takeaway
Timeline (all reverse-engineered, none announced by OpenAI): **Next.js 12 Pages Router at launch (Nov 30, 2022) → Remix v2 + Vite (switch noticed Aug–Sept 2024) → React Router v7 "framework mode" with streaming SSR on React 19 (followed the Remix→RR7 merge, Nov 2024; still the case as of July 2026)**. OpenAI has never officially stated its web framework or the reasons for the migration.

### Cited Findings
- **[Reported, Dec 2022]** At launch (Nov 30, 2022) chatgpt ran on **Next.js 12 with the Pages Router**; a December 2022 `_buildManifest.js` listed routes `/chat`, `/codespace`, `/auth/login`, and `/workspace/[[...tid]]`. — [performance.dev (2026-07-02)](https://performance.dev/chatgpt)
- **[Reported, Aug–Sept 2024]** Next.js was dropped for a **Remix** build. In the Remix era an Express server ran route loaders and serialized ~7,000 lines of JSON into `window.__remixContext`, but rendered little UI on the server; mutations went through ChatGPT's own API, not Remix actions. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, Sept 2024]** Remix co-creator **Ryan Florence** said most data loading used **TanStack Query** rather than Remix loaders (as relayed by the performance.dev article). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, 2024-09-04]** The migration surfaced publicly via an r/reactjs thread "ChatGPT migrates from Next.js to Remix" (Sept 4, 2024), which linked to a post by Ryan Florence. — [r/reactjs thread mirror](https://redlib.hackliberty.org/r/reactjs/comments/1f97zgr/chatgpt_migrates_from_nextjs_to_remix) (mirror was unreachable when fetched; date/title from search index)
- **[Reported, Sept 2024]** The New Stack reported "the community was abuzz this week" about the shift, with "numerous sources" confirming it from the shipped source code; it offered only theories for why. — [The New Stack](https://thenewstack.io/why-chatgpt-shifted-from-next-js-to-remix-some-theories/) (page returned 403 on fetch; summary from search snippet)
- **[Reported, opinion]** Commonly offered (unofficial) reasons: ChatGPT is a mostly client-rendered app where SEO matters little, and **Vite** gives faster/more flexible builds than Next.js's Webpack pipeline at that time. None come from OpenAI. — [DEV Community](https://dev.to/asif_1122se/openais-transition-from-nextjs-to-remix-a-strategic-move-in-web-development-5029); [Blockchain Council](https://www.blockchain-council.org/ai/why-did-openai-switch-from-next-js-to-remix/)
- **[Reported, Nov 2024 → July 2026]** When Remix v2 merged into **React Router v7** (Nov 2024), ChatGPT followed. As of July 2026 the page source contains `window.__reactRouterContext` with `"ssr": true` and `"isSpaMode": false`, lazy route discovery (`"mode": "lazy"`, `"manifestPath": "/__manifest"`) — i.e., **React Router 7 framework mode** (Vite-based, streaming SSR, code-split route modules). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** Runs on **React 19 / react-dom** with streamed server rendering: the server streams the HTML shell first, Suspense boundaries fill in as data resolves, and loader data streams over its own ReadableStream in parallel with the HTML. Logged-out pages are now real server-rendered HTML (a change from the thin-SSR Remix era). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** The route manifest holds **354 client routes**, only ~13 of which are the chat app; the rest are marketing pages in the same codebase, e.g. `($lang).codex.pricing`, `($lang).business._index`, `($lang).atlas.get-started`. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported]** "The migration was caught in the wild, not announced" — no OpenAI or React Router team statement confirms it. — [performance.dev](https://performance.dev/chatgpt)

### Inferences
- **[Inferred]** The 2024 move was less "Remix vs Next" and more "Vite + React Router data APIs + keep TanStack Query as the real data layer"; the RR7 upgrade then let OpenAI turn on real SSR/streaming for logged-out and first-paint performance (the logged-out, no-login-wall funnel became important). A clone can follow either path: an SPA (Vite + React Router) is closest to the 2024 architecture; RR7 framework mode or Next.js App Router with streaming is closest to 2026.

### Gaps
- No official OpenAI statement (blog, talk, or post) on the web framework or the reasons for the Next.js → Remix → RR7 moves was found.
- Could not read Ryan Florence's original 2024 post directly (X/Twitter not fetched); only secondhand accounts.
- Exact React Router minor version and whether RR v8 (released 2026 per reactrouter.com changelog) has been adopted are unknown.

## 2. Language, styling, component libraries, state management, markdown/code rendering, build tooling

### Takeaway
Publicly known: **TypeScript + React** (confirmed by job postings), **Vite** bundling, **Tailwind CSS (v4) on a semantic CSS-variable "token" layer**, **Radix UI** primitives, **TanStack Query** for server state, **ProseMirror** composer, **CodeMirror 6** for code blocks, **KaTeX (+ hidden MathML)** for math, **Motion** for animation, **Cloudflare** CDN, **Statsig** flags, **Datadog RUM**. All library identifications are **[Reported]** from bundle/DOM inspection (July 2026); only React + TypeScript are **[Confirmed]** via OpenAI job postings.

### Cited Findings
**Language**
- **[Confirmed, undated 2026 posting]** OpenAI's careers page for "Frontend Software Engineer, ChatGPT Space" requires "strong experience with modern frontend stacks such as **React and TypeScript**". — [OpenAI Careers](https://openai.com/careers/frontend-software-engineer-chatgpt-space-san-francisco/)

**Build tooling / delivery**
- **[Reported, July 2026]** **Vite** produces per-route JS and CSS chunks; >100 JS chunks on a logged-out cold load (160 content-hashed chunks total); the document `modulepreload`s only 14 critical files (entry, React vendor chunks, matched-route modules). The conversation core ships as a chunk named `conversation-small`; code-block rendering and chain-of-thought views load on demand. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** Loading-control flags in the page: `promoteCss`, `stripModulepreloadImports`, `deferStartupImportsUntilComposerTTFI` (startup imports wait until the composer is interactive). Boot is organized around "time to usable composer"; timing globals `window.__oai_SSR_HTML` and `window.__oai_SSR_TTI` (plus `__oai_logHTML`, `__oai_logTTI`). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** Logged-out document ≈84 KB compressed (~30 KB real markup), a 377 KB bootstrap JSON script, 548 DOM nodes after hydration. Assets served first-party from `chatgpt.com/cdn/assets` with 30-day cache headers; **no service worker** (plain HTTP caching). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** **Cloudflare** for CDN/caching/bot defense (proof-of-work challenge at `cdn-cgi/challenge-platform`); TTFB ≈50–65 ms from a nearby edge. OpenAI's own anti-abuse layer "**Sentinel**" runs in a sandboxed iframe (`sentinel/frame.html`, `sentinel/sdk.js`) with `/backend-anon/sentinel/chat-requirements/prepare` and `/finalize` handshakes before the user submits. — [performance.dev](https://performance.dev/chatgpt)

**Styling**
- **[Reported, July 2026]** **Tailwind CSS v4**; utility classes like `bg-token-main-surface-primary` and `border-token-border-light` sit on a **semantic CSS-variable token layer**, so light/dark and custom chat themes swap variable values. ChatGPT was added to the Tailwind showcase in **March 2023**. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** An inline `<head>` script reads `localStorage` and sets the theme class and `color-scheme` before first paint (no flash); a second script sets a data attribute for the saved chat theme. CSS is split: a root stylesheet, a larger conversation stylesheet, and lazily loaded feature sheets (`code-block.css`, `cot-message.css`, `global-modals.css`). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** No UI webfont: the **system font stack** is used; only a tiny semibold woff2 for brand moments is requested up front; **KaTeX fonts load only when an answer contains math**. — [performance.dev](https://performance.dev/chatgpt)

**Component libraries**
- **[Reported, July 2026]** **Radix UI** for menus, selects, toasts, scroll areas, popovers (visible `data-radix` attributes); **silk-hq** for mobile sheets; **Motion** for (sparse) animation; **Mapbox GL** for maps inside answers; **LiveKit/WebRTC** for voice; **WebAssembly** for audio processing and syntax grammars. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** The composer is a **ProseMirror** rich-text editor; the server renders a visually identical static placeholder and ProseMirror hydrates over it. — [performance.dev](https://performance.dev/chatgpt)

**State management / data**
- **[Reported, July 2026]** **TanStack Query** manages server state; the document initializes `window.__REACT_QUERY_CACHE__` so server-fetched data hydrates into the client cache (next to a small `Promise.withResolvers` polyfill). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, Sept 2024]** Ryan Florence: most data loading used TanStack Query instead of Remix loaders. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** Feature flags/experiments via **Statsig**, server-evaluated: bootstrap JSON carried 556 feature gates, 144 dynamic configs, 192 experiment layers, with hashed numeric gate names (e.g. `3479398748`). OpenAI acquired Statsig (Sept 2025, ~$1.1B) and made its founder Vijaye Raji CTO of Applications. **Datadog RUM** for real-user monitoring; first-party event logging via `chatgpt.com/ces/v1/`. — [performance.dev](https://performance.dev/chatgpt)

**Markdown / code / math rendering**
- **[Reported, July 2026]** Code blocks are rendered with **CodeMirror 6** (`.cm-editor`, `.cm-content` in the DOM) with syntax highlighting and a copy button, not a `<pre>`-based highlighter; the same library powers the Canvas editor. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** Math is rendered with **KaTeX** for visible output plus a hidden **MathML `<math>` tree** for screen readers and copy-paste. — [performance.dev](https://performance.dev/chatgpt)

### Inferences
- **[Inferred]** A practical clone stack that mirrors the observed design: React + TypeScript + Vite, Tailwind with a semantic token layer (CSS variables) for theming, Radix (or shadcn/ui, which is built on Radix) for menus/dialogs/toasts, TanStack Query for conversations/history, a rich-text or plain textarea composer, a lazily loaded code-block renderer (CodeMirror 6 or Shiki), and KaTeX loaded only when math is detected.
- **[Inferred]** Lazy-loading expensive renderers (code blocks, math fonts, chain-of-thought views) and gating startup work on "composer interactive" is the main performance lesson: the first thing the user needs is the input box.

### Gaps
- **Markdown parser not identified**: the 2026 teardown does not name remark/rehype/react-markdown/markdown-it, and I found no current public source naming it. Older (2023) community claims of `react-markdown` + `highlight.js` could not be verified in this session.
- **Client-state library unknown**: no public source names Zustand, Jotai, Redux, etc. for chatgpt.com.
- No evidence found on test tooling, monorepo layout, or design-system name.
- Total JS bundle size (KB) is not published in the sources found.

## 3. How the UI renders a streaming response (incremental markdown, auto-scroll, stop, regenerate)

### Takeaway
Tokens arrive as **Server-Sent Events over `fetch` (POST → `text/event-stream`)**, and the client **re-parses and re-renders the growing message in place on each update**, tolerating incomplete markdown mid-stream. Messages are **not virtualized**. Post-stream controls (copy, feedback, regenerate) appear when the stream completes; a stop button and (historically) a "Continue generating" button exist; stream resumption exists but is flaky per user reports. Implementation details beyond transport are thinly documented publicly.

### Cited Findings
- **[Reported, July 2026]** Chat tokens stream via **SSE over fetch**: e.g., `POST /backend-anon/f/conversation` returns `content-type: text/event-stream` (logged-out path). No WebSocket used for chat text; voice uses LiveKit/WebRTC. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** The growing message is **re-parsed and re-rendered in place** as tokens arrive; the article highlights the problem of incomplete markdown mid-stream (unclosed code fences, partial tables). — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** The message list is **not virtualized**: every message stays in the DOM. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, 2025–2026]** Users report UI freezes across web, Windows and Android clients "exacerbated by long chat histories and session reloads". — [OpenAI Community](https://community.openai.com/t/intermittent-ui-freeze-hangs-across-web-windows-and-android-clients-exacerbated-by-long-chat-histories-and-session-reloads/1355269)
- **[Reported, 2026]** A bug report describes the web chat staying in a "generating" state after a long response finishes, with the **copy and feedback controls missing** (they normally appear once generation completes); reload did not fix it. — [OpenAI Community](https://community.openai.com/t/chatgpt-web-gets-stuck-in-generating-state-after-long-gpt-5-6-sol-responses-finish/1393624)
- **[Reported]** On refresh mid-generation, "sometimes the full response is forced and you can't submit a new prompt until that response is complete" — i.e., generation continues server-side and the client re-attaches/blocks the composer. — [OpenAI Community](https://community.openai.com/t/restore-chatgpts-stop-button-without-errors/1132068?page=2)
- **[Reported, 2025]** A community thread asks to "Restore ChatGPT's Stop Button Without Errors", showing the stop control exists and has had reliability issues. — [OpenAI Community](https://community.openai.com/t/restore-chatgpts-stop-button-without-errors/1132068)
- **[Reported, 2024]** A "**Continue generating**" button existed (for truncated long answers) and had glitches/was reported broken in 2024. — [OpenAI Community (glitches)](https://community.openai.com/t/glitches-with-continue-generating-option/760191); [OpenAI Community (not working)](https://community.openai.com/t/continue-generating-button-no-longer-working/954559)
- **[Reported, 2026]** A "**Resume stream unavailable**" error appears to users mid-response; OpenAI's docs do not describe it. — [SmartScope blog](https://smartscope.blog/en/blog/chatgpt-resume-stream-unavailable-2026/)
- **[Reported, 2026]** A bug thread title lists "missing scroll lock" and "prompt version switching" among regressions, indicating the UI has scroll-lock (auto-scroll follow) behavior and per-message version switching for edits/regenerations. — [OpenAI Community](https://community.openai.com/t/several-bugs-after-recent-updates-response-couldnt-load-prompt-version-switching-missing-scroll-lock-temporary-chat/1403908/1.md) (title only)
- **[Reported, 2023]** A single conversation fetched from `/backend-api/conversation/:conversationId` returns a `mapping` of message nodes (a tree), not a flat list. — [0xdevalias gist](https://gist.github.com/0xdevalias/4e54bb28a02db5357ea4fa3a872fc5fc)
- **[Reported, July 2026]** Code-block and chain-of-thought renderers (`code-block.css`, `cot-message.css`) load lazily, so the first code fence/reasoning block in a streamed answer triggers a chunk load. — [performance.dev](https://performance.dev/chatgpt)

### Inferences
- **[Inferred]** The conversation is a **message tree** (the `mapping` field); "Regenerate" and "Edit message" create sibling branches, and the `< 1/2 >` version switcher walks siblings. A clone should store `parent_id`/`children` per message, not a flat array, if it wants regenerate/edit history.
- **[Inferred]** Generation is decoupled from the HTTP connection (server keeps generating; client can re-attach via a "resume stream" path), which is why refresh mid-stream can still show the full answer. A robust clone should persist partial output server-side and support resumption, or at least mark a message as interrupted.
- **[Inferred]** Re-rendering the whole message per token works at ChatGPT's scale only because heavy parts (code, math) are isolated into separate components/chunks; a clone should memoize completed blocks and only re-render the tail block.
- **[Inferred]** Auto-scroll is "stick to bottom unless the user scrolls up" (scroll lock); the stop button replaces the send button while streaming, and copy/feedback/regenerate render only after the stream's final event.

### Gaps
- No official or reverse-engineered source found describing the exact SSE event schema on chatgpt.com today (delta/patch format), throttling/batching of renders, or how incomplete markdown is "healed".
- No authoritative source on the stop mechanism (client abort vs explicit server cancel endpoint) or the regenerate API call.
- No source on scroll anchoring implementation details.

## 4. How the chat history sidebar works (client side)

### Takeaway
The sidebar loads history from a private endpoint, **`GET /backend-api/conversations?offset=…&limit=28&order=updated…`**, using **offset pagination in pages of 28**, sorted by last update; the server tells the client to prefetch history and starred conversations on load. Date-group headers ("Today", "Yesterday", …) were **reportedly removed in ~June 2025** in favor of a flat list (some sources still describe buckets). Archive/delete behavior is officially documented; Projects group chats.

### Cited Findings
- **[Reported, 2026-08-21]** The web client loads history with `GET /backend-api/conversations?offset=0&limit=28&order=updated_at…` (URL truncated in the post); a stress trace showed offsets **0, 28, 56, 84, 112** — i.e., **28 items per page**. Opening a new tab "commonly requires at least two sequential 28-item history loads"; deleting one conversation triggered refetches at offsets 0, 28, 56; persistent **429** rate-limit responses were reported. — [OpenAI Community](https://community.openai.com/t/chatgpt-web-conversation-history-returns-persistent-429-rate-limit-and-fails-to-load/1391615)
- **[Reported, 2023]** Earlier (on `chat.openai.com`), `/backend-api/conversations?offset=0&limit=100` listed conversations; `limit` had to be ≤100; the response included a `total` count. — [0xdevalias gist](https://gist.github.com/0xdevalias/4e54bb28a02db5357ea4fa3a872fc5fc)
- **[Reported, July 2026]** A write-up says the endpoint is offset/limit paged with `order=updated`, and that `total` can under-count (more pages exist when `total === offset + items.length + 1`). — [Level Up Coding](https://levelup.gitconnected.com/chatgpts-api-listed-775-of-10-500-chats-and-said-that-was-all-c7382bab2cbf) (403 on fetch; from search snippet — single author's observation)
- **[Reported, July 2026]** Route loader data includes server-directed flags `shouldPrefetchModels`, `shouldPrefetchHistory`, `shouldPrefetchStarredConversations`; the sidebar is part of the ~30 KB of server-rendered markup. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, 2025-06-07]** Users reported "The removal of the 'Today' and 'Yesterday' labels in the sidebar", which made the list flat; requests to restore it continued into Jan 2026. No OpenAI staff reply. — [OpenAI Community](https://community.openai.com/t/please-bring-back-the-chronological-sidebar-grouping/1280889)
- **[Reported, 2026]** A feature request for the **new desktop app** describes the sidebar "Activity" view as "a long flat list" and asks for Today / Yesterday / Previous 7 days / Older grouping. — [OpenAI Community](https://community.openai.com/t/feature-request-collapse-activity-view-by-date-in-chatgpt-desktop-sidebar/1398807)
- **[Reported, mid-2026, conflicting]** A third-party (sidebar add-on vendor) blog says the sidebar sorts chats into Today, Yesterday, Previous 30 Days, then looser groupings, based on last activity. This conflicts with the June 2025 removal reports; treat as low reliability. — [NorthLab Apps blog](https://northlabapps.com/blog/chatgpt-conversation-dates/)
- **[Confirmed]** Archiving removes a chat from the regular sidebar without deleting it; archived chats stay searchable and are managed in **Settings → Data controls → Archived chats** (unarchive or delete). Deleting removes a chat immediately from the history view and it is permanently deleted from OpenAI systems within 30 days (with stated exceptions). Bulk "archive all"/"delete all" exist and affect chats in the workspace **including chats in projects**. — [OpenAI Help Center 8809935](https://help.openai.com/en/articles/8809935-how-to-delete-and-manage-your-chatgpt-history-and-data)
- **[Confirmed, 2026]** In the new desktop app, Codex chats must be archived before they can be deleted. — [OpenAI Help Center 20001333](https://help.openai.com/en/articles/20001333-how-to-archive-and-delete-codex-chats-in-the-chatgpt-app)
- **[Confirmed, Dec 2024]** macOS app release notes list "keyword conversation search" (Dec 19, 2024) and support for **Projects** (Jan 15, 2025). — [OpenAI macOS release notes](https://help.openai.com/sr-rs/articles/9703738-chatgpt-macos-app-release-notes)
- **[Reported, 2026]** Users ask to separate Codex/Work projects from ChatGPT chat history, indicating that (post-July 2026 unification) projects from multiple products share the sidebar. — [OpenAI Community](https://community.openai.com/t/feature-request-separate-codex-work-projects-from-chatgpt-chat-history/1393075)

### Inferences
- **[Inferred]** Client pattern: a TanStack `useInfiniteQuery` over offset pages of 28, triggered when the user scrolls near the bottom of the sidebar (infinite scroll), with optimistic removal on archive/delete followed by refetch of loaded pages (matches the offsets 0/28/56 refetch on delete).
- **[Inferred]** "Starred conversations" (prefetch flag) is the pinned/starred chats section shown above recent history.
- **[Inferred]** For a clone, date grouping is a pure client-side transform over `update_time` (Today / Yesterday / Previous 7 days / Previous 30 days / month names); ChatGPT's own choice to drop it shows it is optional.

### Gaps
- No public source documents **rename** (likely a PATCH on the conversation with a new `title`) or the automatic title-generation call on the current site.
- No confirmed source on whether infinite scroll or a "load more" pattern is used today (the 429 thread mentions automatic pagination but not scroll triggers).
- No official documentation of Projects' URL scheme or client data model was found in this session.

## 5. URL addressing and client-side routing (new chat vs existing chat)

### Takeaway
The chat app is two React Router route modules: **`_conversation._index`** (new chat, at `/`) and **`_conversation.c.$conversationId`** (existing chat, at **`/c/<conversation-id>`**), sharing a `_conversation` layout (sidebar + composer). Routes are discovered lazily via `/__manifest`. Logged-out users get a full chat at `/` using `/backend-anon/*` endpoints.

### Cited Findings
- **[Reported, July 2026]** Chat route files: `routes/_conversation._index` (chat home) and `routes/_conversation.c.$conversationId` (single conversation), implying a `/c/<id>` URL under a shared `_conversation` pathless layout. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** React Router lazy route discovery: `"manifestPath": "/__manifest"`, `"mode": "lazy"` — the client fetches route-manifest fragments as the user navigates instead of shipping all 354 routes up front. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, July 2026]** No login wall: logged-out users can prompt immediately via `/backend-anon/me`, `/backend-anon/models`, `/backend-anon/conversation`, `/backend-anon/conversation/init`; anonymous visitors get a real user ID so rate limits and experiments work. — [performance.dev](https://performance.dev/chatgpt)
- **[Reported, 2023]** Logged-in APIs used `/backend-api/conversations` (list) and `/backend-api/conversation/:conversationId` (one conversation), originally on `chat.openai.com`. — [0xdevalias gist](https://gist.github.com/0xdevalias/4e54bb28a02db5357ea4fa3a872fc5fc)
- **[Reported, Dec 2022]** The original Next.js routes were `/chat`, `/codespace`, `/auth/login`, `/workspace/[[...tid]]`. — [performance.dev](https://performance.dev/chatgpt)

### Inferences
- **[Inferred]** New-chat flow: the user types at `/` (index route); on submit the client POSTs to the conversation endpoint without an ID; the server assigns a conversation ID early in the SSE stream; the client then updates the URL to `/c/<id>` (history replace, no remount of the composer/stream) and inserts the new item at the top of the cached sidebar list. Navigating to an existing `/c/<id>` triggers a loader/TanStack query for that conversation's message tree.
- **[Inferred]** Because the `_conversation` layout wraps both routes, the sidebar and composer persist across navigation; only the message pane swaps.

### Gaps
- No public source in this session confirmed the exact moment/mechanism of the URL change for a new chat, or URL formats for GPTs, projects, shared links, or temporary chats on chatgpt.com today.
- Date of the domain move from `chat.openai.com` to `chatgpt.com` was not verified in this session.

## 6. Desktop and mobile apps: technologies

### Takeaway
Mobile apps are **native**: iOS in **Swift (UIKit/SwiftUI)**, Android in **Kotlin + Jetpack Compose** (both confirmed by job postings). The original Mac app (now "**ChatGPT Classic**") is widely described as native. On **July 9, 2026** OpenAI launched a **new unified ChatGPT desktop app (Chat + Work + Codex) for macOS and Windows**, which is the **Codex app updated in place**; the Codex app is **reported to be Electron**, so the new desktop app is very likely Electron-based (inferred, not stated by OpenAI). OpenAI's Atlas browser is confirmed **SwiftUI + AppKit + Metal** over Chromium.

### Cited Findings
- **[Confirmed, 2026-07-09]** "The previous ChatGPT macOS app is now called **ChatGPT Classic**"; no migration required at launch. — [OpenAI macOS release notes](https://help.openai.com/sr-rs/articles/9703738-chatgpt-macos-app-release-notes)
- **[Confirmed, July 2026]** The new desktop app "includes Chat and Work under ChatGPT, alongside Codex, on macOS and Windows"; for existing Codex users the Codex app becomes the new app after updating, keeping chats and projects; Classic keeps getting model updates, fixes, and security patches but some new agent features are new-app-only. The page does not state the technology. — [OpenAI Help Center 20001276](https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app)
- **[Reported, 2026]** Users report the new desktop app "does not currently have full feature parity with ChatGPT Web or ChatGPT Classic"; Daring Fireball (July 11, 2026) reported the installer replaced Classic instead of installing alongside. — [OpenAI Community](https://community.openai.com/t/new-chatgpt-desktop-has-significant-feature-regressions-compared-to-chatgpt-web-and-classic/1386650); [Daring Fireball](https://daringfireball.net/linked/2026/07/11/can-someone-explain-to-me-how-to-get-chatgpt-classic)
- **[Confirmed, 2026-02-02 / 2026-03-04]** OpenAI launched the Codex app on macOS (Feb 2, 2026) and added Windows on March 4, 2026, building "the first Windows-native agent sandbox". — [OpenAI: Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
- **[Reported, Feb 2026]** The Codex app is built with **Electron and Node.js**; OpenAI's Romain Huet reportedly said Electron was chosen to support expansion to other OSes; some Mac developers criticized the memory cost. — [Simon Willison](https://simonwillison.net/2026/Feb/2/introducing-the-codex-app/); [Tessl](https://tessl.io/blog/openai-launches-macos-codex-app-for-supervising-ai-agents/); [DevClass](https://www.devclass.com/development/2026/02/05/traditional-ides-not-the-right-tool-for-development-with-agentic-ai-openai-claims/4090132)
- **[Reported, 2025-11-30]** Allen Pike: ChatGPT for Mac is "built on native tech", follows Mac conventions, and is stable/performant — contrasted with Claude's Electron-wrapped web UI. — [Allen Pike](https://allenpike.com/2025/why-is-chatgpt-so-good-claude)
- **[Reported, 2026-07-06]** A post quoting John Gruber: ChatGPT's Mac appeal is that it looks and feels like a Mac app; the Codex app is at least partly Electron; ChatGPT iOS "has a lot of SwiftUI". — [Manton Reece](https://www.manton.org/2026/07/06/john-gruber-with-another-blog.html)
- **[Confirmed, 2025-10-30]** OpenAI's Atlas browser uses **OWL (OpenAI's Web Layer)**: Chromium's browser process runs outside the app process and talks to the Atlas client over Mojo IPC; the UI uses "the most modern native frameworks… (**SwiftUI, AppKit and Metal**)" and Atlas is "built almost entirely in SwiftUI and AppKit". — [OpenAI: Building ChatGPT Atlas](https://openai.com/index/building-chatgpt-atlas)
- **[Confirmed, 2026 postings]** iOS: "iOS Engineer, ChatGPT Mobile Infrastructure" works on "the core **Swift** platform" (architecture, CI) powering **ChatGPT, Atlas, Sora** and other apps; requires Swift, concurrency, networking, Xcode, plus UIKit/SwiftUI experience. "iOS Engineer, Applied Foundations" asks for Swift fluency and familiarity with **UIKit and SwiftUI**. — [OpenAI Careers (iOS Mobile Infra)](https://openai.com/careers/ios-engineer-chatgpt-mobile-infrastructure-san-francisco/); [OpenAI Careers (Applied Foundations)](https://openai.com/careers/ios-engineer-applied-foundations-san-francisco/)
- **[Confirmed, 2026 postings]** Android: "Android Engineer, ChatGPT Library Team" requires "deep expertise in **Kotlin, Jetpack Compose**, the Android SDK, and modern Android architecture"; "Android Engineer, ChatGPT Mobile Infrastructure" owns "the core Kotlin-based platform… that powers ChatGPT, Sora" and other Android apps. — [OpenAI Careers (Library)](https://openai.com/careers/android-engineer-chatgpt-library-team-seattle/); [OpenAI Careers (Mobile Infra)](https://openai.com/careers/android-engineer-chatgpt-mobile-infrastructure-san-francisco/)
- **[Confirmed, Dec 2024–Mar 2025]** Mac app feature history: Advanced Voice with apps, keyword conversation search (Dec 19, 2024); Canvas, Tasks, Projects (Jan 15, 2025); code edits in IDE (Mar 6, 2025). — [OpenAI macOS release notes](https://help.openai.com/sr-rs/articles/9703738-chatgpt-macos-app-release-notes)

### Inferences
- **[Inferred]** Because the new (July 2026) ChatGPT desktop app *is* the Codex app updated in place, and the Codex app is reported to be Electron, the new desktop app is most likely Electron (with native modules for sandboxing), i.e., it probably reuses web UI code — a shift away from the native-Mac "Classic" approach. OpenAI has not confirmed this.
- **[Inferred]** OpenAI maintains shared mobile platform layers (Swift core for iOS, Kotlin core for Android) reused across ChatGPT, Sora, and Atlas; mobile UIs are not web views of chatgpt.com.

### Gaps
- No official statement of the framework for the **new** desktop app, and no verified source for the technology of the original (Oct 2024) **ChatGPT Windows** app (a search snippet claimed it was Electron-based, but the cited page did not contain that claim).
- No OpenAI talk/podcast describing desktop/mobile architecture for ChatGPT specifically (other than Atlas) was found.

## 7. OpenAI frontend job postings that list the stack

### Takeaway
OpenAI web postings consistently name only **React and TypeScript** and talk about component systems, state management, navigation, rendering performance, rich-text editors, and real-time UIs; **none of the postings found name Next.js, Remix, React Router, Vite, or Tailwind**.

### Cited Findings
- **[Confirmed, undated, live 2026]** "Frontend Software Engineer, ChatGPT Space" (SF; team "building a shared workspace where people and AI agents turn ideas into polished, editable work"): "Own frontend architecture decisions across **component systems, state management, navigation, and rendering performance**"; "strong experience with modern frontend stacks such as **React and TypeScript**"; nice-to-have: "collaborative applications, **rich-text editors, real-time interfaces**"; also testing, instrumentation, accessibility, and loading/error/concurrent-change UX. — [OpenAI Careers](https://openai.com/careers/frontend-software-engineer-chatgpt-space-san-francisco/)
- **[Reported, aggregator]** "Frontend Engineer, ChatGPT Engineering" lists React and TypeScript as top skills and describes building "best-in-class product experiences across ChatGPT"; one variant asks for "5+ years of frontend experience with modern web frameworks (e.g., React, TypeScript)". Pay ranges differ by aggregator (e.g., $185K–$385K on Built In; $230K–$385K for the ChatGPT Space role on a16z's board). — [Built In](https://builtin.com/job/frontend-engineer-chatgpt-engineering/8394655); [a16z jobs](https://jobs.a16z.com/jobs/openai/1f99d5d3-4512-4247-aaba-3133a3dabf5a--frontend-software-engineer-chatgpt-space)
- **[Reported, aggregator]** "Software Engineer, Frontend (ChatGPT for Work)" asks for 4+ years building production web apps. — [Built In](https://builtin.com/job/software-engineer-frontend-chatgpt-work/4549696)
- **[Confirmed]** Other ChatGPT product-engineering postings exist for Lifestyle and Shopping teams. — [OpenAI Careers (Lifestyle)](https://openai.com/careers/software-engineer-chatgpt-lifestyle-san-francisco/); [OpenAI Careers (Shopping)](https://openai.com/careers/software-engineer-chatgpt-shopping-san-francisco/)

### Inferences
- **[Inferred]** The emphasis on "navigation", "state management", "rendering performance" and "rich-text editors" lines up with the reverse-engineered stack (React Router, TanStack Query, ProseMirror/CodeMirror), but postings deliberately stay framework-agnostic.

### Gaps
- Posting dates are not shown on openai.com careers pages; several aggregator copies are stale/closed.
- No posting found that names a CSS framework, bundler, meta-framework, or testing stack.
