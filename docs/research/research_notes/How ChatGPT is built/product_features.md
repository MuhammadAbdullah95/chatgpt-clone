# ChatGPT product features beyond basic chat, and how they work (state as of 2026-11-22)

Confidence tags used on every claim:
- **[Confirmed]**: OpenAI said it officially (openai.com blog, help.openai.com, API docs, release notes).
- **[Reported]**: credible third party (tech press, named reverse-engineering write-ups, academic papers, community docs).
- **[Inferred]**: my own reasoning from indirect evidence. All items under "Inferences" are [Inferred].

Method note: the ChatGPT release notes page (help.openai.com/en/articles/6825453) is about 278k characters long. I read all of it in three passes through an automated summarizer, so exact wording should be spot-checked before quoting it in a final report. Help-center pages show only relative "Updated" dates (e.g. "Updated 43 minutes ago" on 2026-11-22), so I treat them as current as of today.

---

## 1. Conversation basics: automatic titles, edit / regenerate / branching, stop generating

### Takeaway
OpenAI does not document how titles are generated. Community and reverse-engineering evidence points to a separate model call, made after the first user message, behind an internal `gen_title` route. Edits and regenerations are stored as a **message tree**: each message has a parent and children, and a `current_node` marks the active leaf. "Branch in new chat" (Sep 2025) copies a branch into a new conversation. A clone should build its data model as a tree from day one.

### Cited Findings
- **[Reported]** The reverse-engineered ChatGPT backend lists `POST backend-api/conversation/gen_title/:conversationId` as the route that generates a chat title. It is internal and undocumented, so it can change. — [scrapbox: chatGPT backend API](https://scrapbox.io/takker/chatGPT_backend_API)
- **[Reported]** Users report that ChatGPT generates the title automatically from the first user message. Users can rename chats by hand. Community threads ask for titles that update as the conversation evolves, which suggests titles are generated once and not refreshed. — [OpenAI Community: "Let chat titles update as the conversation evolves"](https://community.openai.com/t/let-chat-titles-update-as-the-conversation-evolves/1394299); [OpenAI Community: "Prompt to get ChatGPT API to write concise chat titles as it does in ChatGPT"](https://community.openai.com/t/prompt-to-get-chatgpt-api-to-write-concise-chat-titles-as-it-does-in-chatgpt-chat-application/85644)
- **[Reported]** A 2026 community thread reports "random Chinese spam-like text appearing as automatically generated ChatGPT chat titles". Garbled titles like this are consistent with a generative model writing them, not with truncating the user's text. — [OpenAI Community thread](https://community.openai.com/t/random-chinese-spam-like-text-appearing-as-automatically-generated-chatgpt-chat-titles/1392443)
- **[Reported]** Open-source clones such as LibreChat implement titles the same way: a separate LLM call (`titleConvo`) after the first exchange, with the client polling `GET /api/convos/gen_title/:conversationId` (backoff up to about 15 s). — [LibreChat API docs (mintlify)](https://www.mintlify.com/danny-avila/LibreChat/api/conversations); [LibreChat titleConvo.js](https://huggingface.co/spaces/tang-x/LibreChat/blob/3b6afc02409cd108df362e900bf2d0c05106b289/api/app/titleConvo.js)
- **[Reported]** In the data export, each conversation has a `mapping` object keyed by message UUID. Each node stores its `parent` and `children` IDs, and a `current_node` field marks the active leaf. Editing a message or regenerating a reply creates sibling children under the same parent, so the earlier versions stay in the export. — [Level Up Coding: "Your ChatGPT history is a tree, not a transcript" (2026)](https://levelup.gitconnected.com/your-chatgpt-history-is-a-tree-not-a-transcript-2026-5660ceb301d4); [OpenAI Community: decoding conversations.json](https://community.openai.com/t/decoding-exported-data-by-parsing-conversations-json-and-or-chat-html/403144)
- **[Reported]** To rebuild the branch the user sees, walk up from `current_node` through the parent links. Open WebUI uses the same parent/children model and a `history.currentId` pointer, and it can import ChatGPT exports. — [Level Up Coding](https://levelup.gitconnected.com/your-chatgpt-history-is-a-tree-not-a-transcript-2026-5660ceb301d4); [Open WebUI import/export docs](https://docs.openwebui.com/features/chat-conversations/data-controls/import-export.md)
- **[Confirmed, 2025-09-04]** "Branch in new chat" in a message's More actions menu opens a separate chat starting from that message (web first). — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-11-05]** "Interrupt ChatGPT": users can add information to long-running queries, such as deep research, without restarting them. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-03-18]** Unsent drafts in the composer are saved. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-07-17]** In agent mode, users "can interrupt, take over the browser, or stop a task". — [Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)
- **[Confirmed, 2026-06-08]** Longer web conversations get a table of contents. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

### Inferences
- **[Inferred]** Titles most likely come from an async, low-cost model call (a small model with a "summarize in about 5 words" prompt) fired after the first user message or first reply, then pushed to the sidebar. A clone can do this with a cheap model and a non-blocking job.
- **[Inferred]** The "< 2/2 >" version switcher is a UI over sibling nodes in the tree. Switching versions changes `current_node`. Editing a user message creates a new sibling user node plus a new assistant child. Nothing is deleted.
- **[Inferred]** "Stop generating" is most likely the client aborting the streamed response (SSE/fetch abort) plus a server-side cancel. The partial reply is saved as a normal assistant node.

### Gaps
- No official OpenAI documentation on how titles are generated (model, prompt, timing) or on the stop-generation protocol. Both are reverse-engineered or inferred only.
- No official schema for the export's `mapping` tree. Field names come from community documentation and may change.

---

## 2. Model picker, automatic routing, and reasoning ("thinking") display

### Takeaway
GPT-5 (2025-08-07) introduced a real-time **router** between a fast model and a reasoning model. Over 2025–2026 OpenAI moved away from automatic switching for paying users. It removed reasoning auto-switching with GPT-5.2 (Dec 2025), made it a user toggle (Mar and Jun 2026), and retired Instant-to-Thinking auto-switching for Plus and Pro on 2026-09-14. As of November 2026 the picker is a **thinking-depth slider** (Instant / Medium / High / Extra High / Pro) on **GPT-6** (Sol; Pro runs on GPT-6 Pro, powered by Astra). Free and Go get Instant plus "Think" on a Luna model. Automatic routing survives mainly for **rate-limit fallbacks** (hidden "mini" models) and **safety**.

### Cited Findings
- **[Confirmed, 2025-08-07]** GPT-5 in ChatGPT is a "unified system": a "smart, efficient model" for most questions, a "deeper reasoning model (GPT-5 thinking)", and a "real-time router". The router decides based on "conversation type, complexity, tool needs, and explicit intent" (e.g. "think hard about this"). It is "continuously trained on real signals, including when users switch models, preference rates for responses, and measured correctness." "Once usage limits are reached, a mini version of each model handles remaining queries." — [Introducing GPT-5](https://openai.com/index/introducing-gpt-5/)
- **[Confirmed, 2025-08-12]** The picker gained "Auto", "Fast" and "Thinking" for GPT-5. Plus got 3,000 GPT-5 Thinking messages a week, with a 196k-token context. GPT-4o returned for paid users, and a "Show additional models" toggle was added. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); press coverage: [TechCrunch, 2025-08-12](https://techcrunch.com/2025/08/12/chatgpts-model-picker-is-back-and-its-complicated) **[Reported]**
- **[Confirmed, 2025-09-17]** A thinking-time toggle was added to the composer for Plus, Business and Pro: "All queries default to Standard unless you choose to change it." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-10-03]** Safety routing for distress conversations: "When GPT-5 Auto or a non-reasoning model is selected, we'll instead route these conversations to GPT-5 Instant." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-11-12]** GPT-5.1 Instant and Thinking replaced GPT-5: "GPT-5.1 Auto continues to route each query to the best model." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-12-11]** GPT-5.2 Instant, Thinking and Pro launched, "removing automatic model switching for reasoning in ChatGPT". Free users default to GPT-5.2 Instant. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-02-20]** A manually selected Thinking model has a total context window of 256k tokens, up from 196k. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-03-05]** With GPT-5.4 Thinking, users "can see an upfront plan and adjust course mid-response". — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-03-17]** The picker became Instant / Thinking / Pro, with advanced options under "Configure", where users can turn "Auto-switch to Thinking" on or off. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-03-18 / 04-09 / 07-06]** Hidden fallback models serve requests once a user hits a rate limit, and they "will not appear as a selectable model in the model picker": GPT-5.4 mini (for GPT-5.4 Thinking), GPT-5.3 Instant mini, and then GPT-5.5 Instant Mini (after GPT-5.5 Instant or Auto limits). — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-04-22]** "Fast answers" give common factual questions quicker responses and "do not reference your past chats or memory". Users can turn this off in Personalization. This is a routing path for simple queries. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-04-28]** Model selection moved into the message composer, and thinking-effort controls moved into the model picker. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-06-10]** The picker became Instant, Medium, High, plus Pro-only tiers. "Users have the ability to decide whether Instant auto-switches to Medium for higher reasoning when required." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-08-06]** An updated GPT-5.6 Sol came with "a new slider to choose how much thought ChatGPT puts into a response". Luna became the Free and Go default. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-09-14]** "We're retiring automatic switching from Instant to Thinking (reasoning) for ChatGPT Plus and Pro users globally." The "Higher intelligence" setting was removed on web. A release-notes excerpt surfaced by search (not re-verified in the full text) adds that ChatGPT can still switch automatically for safety purposes. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-10-07]** GPT-6 with "Intelligent UI" rolled out in Chat. It "can choose the format automatically, and still use a simple text answer when that works best." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** Current lineup, per the GPT-6 help page:
  - "GPT-6" replaces "Latest" in the menu. Instant through Extra High run on **GPT-6 Sol**. Pro runs on **GPT-6 Pro (powered by GPT-6 Astra)**.
  - The slider has five levels: Instant, Medium, High, Extra High, Pro.
  - Free and Go: Instant and "Think", both on GPT-5.6 Luna.
  - Plus: Medium and High. Pro: up to Extra High and Pro.
  - Business admins keep a "Higher intelligence" control for automatic extra thinking while Instant is selected.
  - If a Thinking limit is reached, ChatGPT "may continue with another available model".
  - Intelligent UI works from Instant to Extra High, not at Pro, and can be reduced in Settings > "Layout and visuals".

  — [GPT-6 in ChatGPT (help center)](https://help.openai.com/en/articles/11909943-gpt-6-in-chatgpt)
- **[Confirmed; conflicting]** The 2026-10-07 release note says Free and Go use "GPT-6 Luna". The GPT-6 help page says Free and Go use **GPT-5.6 Luna**, and that Terra and Luna are not selectable in standard Chat. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) vs. [GPT-6 in ChatGPT](https://help.openai.com/en/articles/11909943-gpt-6-in-chatgpt)

### Inferences
- **[Inferred]** OpenAI's own path, from an automatic router (2025) to an explicit effort slider with opt-in auto-switching (2026), suggests a clone should **start with a manual picker or effort toggle**. Add a lightweight router later, mainly for fallback after rate limits and for cost control.
- **[Inferred]** The "thinking" display is most likely a summary of reasoning, shown while the reasoning model works. The 2026 "upfront plan, adjust mid-response" feature implies the plan is streamed as a separate event type before the answer. A clone can show the reasoning summaries that reasoning APIs return.
- **[Inferred]** Router training signals (users switching models, preference rates) mean the picker doubles as telemetry. A clone should log which model was used and any manual switches per message.

### Gaps
- OpenAI has not published the router's architecture (classifier vs. small LLM) or its latency budget.
- I did not fetch an official 2025–2026 source on whether raw chain-of-thought is hidden or summarized. The statement that it is summarized is inference, not verified here.
- Some 2026 model names (Sol, Luna, Terra, Astra; GPT-5.6 vs GPT-6) are inconsistent across OpenAI pages, as noted above.

---

## 3. Custom instructions and personalization

### Takeaway
Custom instructions (Jul 2023) grew into a Personalization hub: custom instructions, base personalities or styles, fine-grained tone sliders, and memory. As of 2025-11-07, changes also apply to existing chats. Implementation: user-editable text and settings injected into the system or developer context on every request.

### Cited Findings
- **[Confirmed, 2023-07-20]** Custom instructions launched in beta for Plus. They expanded to free users and the EU/UK in August 2023. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-01-17]** A new Custom Instructions UI added fields for traits, how ChatGPT should talk to you, and rules to follow. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-08-07]** Preset personalities (Default, Cynic, Robot, Listener, Nerd), which don't apply to Voice. Accent colors. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-09-15]** Personality, custom instructions and Memory moved into Settings > Personalization. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-11-07]** Personality and custom-instruction changes now apply to existing chats too. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-12-19]** Separate controls for warmth, enthusiasm, headers and lists, and emoji use. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-03-17]** The "Nerdy" base style was retired. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-07-15]** The custom instructions limit rose to 5,000 characters. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-10-30]** On mobile, up to two accounts can be signed in, and each keeps its own memory and settings. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Reported, Dec 2025]** Reverse engineering found the context ordered as: "System Instructions", "Developer Instructions", "Session Metadata", "User Memory", "Recent Conversations Summary", "Current Session Messages". — [LLMrefs summary of Manthan Gupta's analysis](https://llmrefs.com/blog/reverse-engineering-chatgpt-memory)

### Inferences
- **[Inferred]** Because changes apply to existing chats (Nov 2025), instructions are injected fresh on every request rather than frozen when a chat starts. The tone sliders probably compile into short instruction snippets in the same system or developer block.
- **[Inferred]** For a clone: one `user_settings` row (instructions text, up to about 5k characters; style enum; tone flags), injected into the system prompt on each turn. This is cheap and high-value.

### Gaps
- OpenAI has not published the exact prompt template that injects custom instructions or personality.

---

## 4. Memory: saved memories and "reference chat history"

### Takeaway
There are two official mechanisms:
1. **Saved memories**: discrete facts, created on request or automatically, stored separately from chats, and since Oct 2025 managed and rewritten automatically with version history.
2. **Reference chat history**: since April 2025, information drawn from past conversations.

Reverse engineering in 2025 found no RAG: a pre-computed "dossier" of memories plus summaries of about 15 recent chats was injected into the system prompt. In 2026, OpenAI's own wording ("searches for relevant context only when it is likely to improve a response"; past chats shown as sources) points to **on-demand retrieval over past chats**. The architecture appears to have changed.

### Cited Findings
- **[Confirmed, 2024-02-13 / 2024-04-29]** Memory testing began, with users able to tell ChatGPT to remember or forget things. It reached all Plus users (excluding Europe and Korea at first) on 2024-04-29. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); [Memory and new controls for ChatGPT (OpenAI blog)](https://openai.com/index/memory-and-new-controls-for-chatgpt/)
- **[Reported, 2025-04-10]** "Reference chat history" (the new memory) launched on 2025-04-10. — [Simon Willison, 2025-05-21](https://simonwillison.net/2025/May/21/chatgpt-new-memory/)
- **[Confirmed, 2025-05-08 / 2025-06-03]** Enhanced memory rolled out to Plus and Pro, off by default in the EEA, Switzerland and nearby countries. Free users then got memory of recent conversations. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-04-16]** Memory can inform third-party web search queries. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** The Memory FAQ:
  - When Memory is on, ChatGPT can draw on past chats, saved memories, custom instructions, files saved in Library or Space, and connected apps such as Gmail. "Memory does not retain every detail from every conversation."
  - Saved memories are "stored separately from chat history", so deleting a chat doesn't delete them.
  - ChatGPT searches for relevant context only "when it is likely to improve a response".
  - There is "no separate storage limit for what ChatGPT can reference through chat history."
  - Turning off Reference chat history means "information remembered from past chats is scheduled for deletion from OpenAI systems within 30 days."
  - If Reference saved memories is off, Reference chat history is off too.
  - OpenAI "may retain logs of deleted saved memories for up to 30 days for safety and debugging purposes."
  - "Don't mention this again" reduces future references but does not delete the source.
  - The memory summary is a high-level view, not a complete list.

  — [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)
- **[Confirmed, current]** Memory may be used to train models when "Improve the model for everyone" is on (personal accounts). Business, Enterprise, Edu and Healthcare content is not used for training by default. — [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)
- **[Confirmed, 2025-06-12 / 2025-08-22]** Project memory references past chats within the same project. **Project-only memory** lets a project use only its own chats and ignore saved memories from outside it. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-10-15]** "ChatGPT now manages saved memories automatically": it prioritizes relevant details, and users can view and restore prior versions. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-01-15]** Better past-chat recall for Plus and Pro: "Any past chat used to answer your question now appears as a source." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-01-07]** The Health space keeps its own memory and files, separate from the rest of ChatGPT. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-05-05]** Memory sources: "Tap the Sources icon below the response to view relevant saved memories". This shows which saved memories, past chats and custom instructions shaped a response. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-06-04]** "Memories are now updated automatically", to reduce stale or contradictory entries. Plus and Pro get 2x capacity. Users can revert to the legacy saved-memories system. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-08-14]** "Project memory switching". — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Reported, 2025-05-21]** Simon Willison extracted the injected "dossier" with a "Complete and verbatim" prompt on a paid plan with chat history enabled. Its sections were "Assistant Response Preferences", "Notable Past Conversation Topic Highlights", "Helpful User Insights" and "User Interaction Metadata". He cites Johann Rehberger's research that a summary is maintained and injected at the start of each new chat, rather than RAG. He criticized it for removing user control: past chats leaked into image generation and contaminated his experiments. — [Simon Willison](https://simonwillison.net/2025/May/21/chatgpt-new-memory/)
- **[Reported, Dec 2025]** Manthan Gupta's reverse engineering found:
  - **no vector database or RAG** over history;
  - "User Memory" (33 stored facts in his account) injected with every message;
  - a "Recent Conversations Summary" of about 15 recent chats, summarizing only the user's messages, with dates;
  - "Session Metadata" (device, approximate location, timezone, plan, usage habits), injected once per session and not saved;
  - when the token budget runs short, the oldest messages of the current chat are trimmed first.

  — [LLMrefs (updated 2025-12-13)](https://llmrefs.com/blog/reverse-engineering-chatgpt-memory); [GIGAZINE, 2025-12-26](https://www.gigazine.net/gsc_news/en/20251226-reverse-engineered-chatgpt-memory-system)
- **[Reported, Feb 2026]** An academic study of real users' ChatGPT memory entries found that "96% of memories in our dataset are created unilaterally by the conversational system", not by explicit "remember this" requests (per the search-result snippet; I did not read the full paper). — [arXiv 2602.01450, "The Algorithmic Self-Portrait"](https://arxiv.org/html/2602.01450)
- **[Confirmed, 2025-05-02]** OpenAI: "user memory contributes to exacerbating the effects of sycophancy", though it has no evidence that memory broadly increases sycophancy. — [Expanding on what we missed with sycophancy](https://openai.com/index/expanding-on-sycophancy/)

### Inferences
- **[Inferred]** 2025 architecture: a profile store (saved facts) plus a background job that summarizes recent chats, both pasted into the system prompt every turn. 2026 architecture: probably adds a retrieval or search tool over past chats, called only when useful. Evidence: past chats cited as sources, "searches... only when it is likely to improve a response", and no storage cap. These two views conflict only if you assume the system did not change between Dec 2025 and 2026.
- **[Inferred]** Clone design: (1) a `memories` table (text, created_at, source_conversation_id, version) plus a model tool `save_memory` / `forget_memory`, injected in the system prompt; (2) later, an embeddings index over past messages with a retrieval tool, citing the source chats. Respect a "temporary chat" flag that skips both reading and writing.

### Gaps
- OpenAI has not published the injection format or retrieval method. I could not verify the name of the memory-writing tool ("bio") in a fetched source.
- No official per-plan memory capacity numbers, only "2x capacity for Plus/Pro" (June 2026).

---

## 5. Conversation management: shared links, archive, delete, export, temporary chats

### Takeaway
Shared links from personal accounts are **frozen snapshots** that anyone with the URL can open, updated only via "Update link". Workspace links can be live and are limited to members. Recipients who continue a shared chat get a private copy. Export is an async ZIP with JSON and an HTML viewer. Temporary chats skip history and memory writes, but are kept up to 30 days for safety.

### Cited Findings
- **[Confirmed, 2023-05-24]** Shared links entered alpha. **[Confirmed, 2023-05-03]** Users could turn off chat history and export data. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** Shared links FAQ:
  - Personal-account links are snapshots of the content at creation or update time: "Messages added later are not included automatically." Use **Update link** to refresh.
  - Workspace links may show messages added later, and only members of that workspace can open them.
  - Links are anonymous by default.
  - Deleting the conversation deletes its link. "Delete all shared links" is available.
  - "Shared link pages are not intended for search-engine indexing, but this does not make a link private."
  - "Continuing a shared conversation creates a separate, private conversation in the recipient's account."

  — [ChatGPT Shared Links FAQ](https://help.openai.com/en/articles/7925741-chatgpt-shared-links-faq)
- **[Confirmed, current]** Memory "Sources" shown under responses are not included in shared links. — [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)
- **[Confirmed, 2026]** Locked chats were introduced on 2026-10-21. Locking a chat does not delete an existing shared link. The newer "Space" (2026-11-20, replacing Library) offers shared pages that require signed-in access, with no public links. That applies to Space pages, not conversation links. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); [Shared Links FAQ](https://help.openai.com/en/articles/7925741-chatgpt-shared-links-faq)
- **[Confirmed, current]** Archiving hides a chat. It "does not change whether it can be used to train OpenAI models." Deleting an account is permanent. "Delete a chat or your account separately when you want to remove content." — [Data Controls FAQ](https://help.openai.com/en/articles/7730893-data-controls-faq)
- **[Confirmed, current]** The export is a ZIP with an `index.html` export viewer (older exports have `chat.html`). Conversations are stored as JSON, other data as CSV and other formats. Notification comes by email or SMS. "Exports can take up to 7 days to arrive." "The download link expires 24 hours after you receive it." "An export cannot restore chats that have already been deleted." — [Exporting your ChatGPT history and data](https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data)
- **[Reported]** The JSON is `conversations.json`, sharded as `conversations-000.json` etc. in newer exports, with the `mapping` tree described in section 1. — [Level Up Coding (2026)](https://levelup.gitconnected.com/your-chatgpt-history-is-a-tree-not-a-transcript-2026-5660ceb301d4)
- **[Confirmed, current]** Temporary Chat FAQ:
  - "OpenAI may keep a copy of a temporary chat for up to 30 days for safety purposes."
  - Temporary chats are not used for training while they stay temporary.
  - Before the first message, the user picks **Unpersonalized** ("Does not use memory, custom instructions, or plugins") or **Personalized** ("Can use your existing memories, custom instructions, and plugins"). Neither creates or updates memories.
  - "If you do not save a temporary chat, it will not appear in your history". Saving converts it to a regular chat.
  - Temporary chat works with GPTs.

  — [Temporary Chat FAQ](https://help.openai.com/en/articles/8914046-temporary-chat-faq)
- **[Confirmed, 2026-08-27]** Temporary chats can now be personalized or not, and saved to history. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2025-12-17/18]** Pinned chats added. **[Confirmed, 2026-07-14]** Search across chats, projects and files upgraded. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

### Inferences
- **[Inferred]** Shared links = copy the active branch (root → `current_node`) into an immutable `shared_snapshots` row with a random slug, and render it read-only without auth. "Continue" forks the snapshot into the viewer's account. Add `noindex` and unguessable IDs.
- **[Inferred]** Temporary chat = a conversation flag that hides the chat from the history list, skips memory writes (and optionally reads), and sets a 30-day TTL deletion job.
- **[Inferred]** Export = a background job that serializes conversations (with the tree) and emails a signed URL with a 24-hour expiry.

### Gaps
- No official statement on retention after a user deletes a chat. The pages I fetched do not mention a 30-day window for deleted chats (only for temporary chats, memory logs, and chat-history memory).

---

## 6. Search: ChatGPT search / web browsing

### Takeaway
ChatGPT search (2024-10-31; available to everyone, logged-out included, by 2025-02-05) uses a fine-tuned model that decides when to search. It draws on "third-party search providers" plus content from news partners, and shows inline citations and a Sources sidebar. Bing is widely reported as the main index provider, but OpenAI's launch post doesn't name it. OpenAI runs its own crawler, **OAI-SearchBot**, for search inclusion. The public API `web_search` tool is the closest reference implementation.

### Cited Findings
- **[Confirmed, 2024-10-31]** "ChatGPT will choose to search the web based on what you ask", or users can trigger search manually. The search model is "a fine-tuned version of GPT-4o", post-trained with synthetic data including outputs distilled from o1-preview. It uses "third-party search providers, as well as content provided directly by our partners". Named news partners: AP, Axel Springer, Condé Nast, Dotdash Meredith, FT, GEDI, Hearst, Le Monde, News Corp, Prisa, Reuters, The Atlantic, Time, Vox Media. Users "click the Sources button below the response to open a sidebar with the references." It reached all logged-in users on 2024-12-16 and everyone, with no signup, on 2025-02-05. The post does not mention Bing. — [Introducing ChatGPT search](https://openai.com/index/introducing-chatgpt-search/)
- **[Reported, 2023-05]** Microsoft announced at Build 2023 that Bing would become ChatGPT's default search experience. — [GeekWire, 2023-05-23](https://www.geekwire.com/2023/microsoft-bing-will-become-chatgpts-default-search-engine-in-latest-openai-collaboration/)
- **[Reported, Nov 2024]** Analyses concluded that ChatGPT search's index appears to come from Bing, with OpenAI ranking results itself, so pages missing from Bing's index tend to be missing from ChatGPT. — [Search Engine Roundtable](https://www.seroundtable.com/bing-powers-chatgpt-search-38345.html); [Search Engine Land](https://searchengineland.com/chatgpt-search-microsoft-bing-seo-448019)
- **[Reported, speculative]** A LinkedIn post claims OpenAI moved off the Bing API (which Microsoft deprecated) toward its own index or another partner. I found no confirmation from OpenAI or Microsoft. — surfaced in search; treat as unverified.
- **[Confirmed, current]** OpenAI crawlers:
  - "OAI-SearchBot is used to surface websites in search results in ChatGPT's search features."
  - Sites that block OAI-SearchBot can still appear only as navigational links.
  - "ChatGPT-User" makes user-initiated visits, and robots.txt "may not apply". It "is not used to determine whether content may appear in Search."
  - "GPTBot" collects training data.

  — [OpenAI crawlers overview](https://developers.openai.com/api/docs/bots)
- **[Confirmed, 2025-09-16, 2026-03]** Search was improved for factuality, shopping-intent detection and formatting (Sep 2025). GPT-5.3 Instant web answers became more accurate (Mar 2026). — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, 2026-08-10]** Restaurant reservation search with OpenTable, Resy and Yelp. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** Memory can refine web searches, e.g. with location or dietary preferences. — [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)
- **[Confirmed, current]** API reference implementation, the Responses API tool `{ "type": "web_search" }`:
  - With `tool_choice: "auto"` the model decides whether to search.
  - Output contains `web_search_call` items with actions `search`, `open_page` and `find_in_page`.
  - Message text carries `url_citation` annotations (`start_index`, `end_index`, `url`, `title`).
  - `include: ["web_search_call.action.sources"]` returns every URL consulted.
  - Other controls: `filters.allowed_domains` / `blocked_domains`, `user_location`, `search_context_size`.
  - Chat Completions uses `gpt-5-search-api`, which always searches.
  - The docs require inline citations as "prominent, clickable links" whenever web results are displayed.

  — [OpenAI API: Web search tool](https://developers.openai.com/api/docs/guides/tools-web-search)

### Inferences
- **[Inferred]** ChatGPT search = a tool-calling loop (query → fetch/open pages → answer with span-level citations) and a Sources panel built from the tool's source list. A clone can get near parity cheaply by enabling the API `web_search` tool, or a search API such as Bing, Brave or Tavily, and rendering annotations.

### Gaps
- No official 2026 statement naming ChatGPT's current search index provider(s).

---

## 7. Projects, Canvas, custom GPTs, connectors / apps / plugins, agent mode and ChatGPT Work

### Takeaway
- **Projects** are folders with shared files, instructions and scoped memory.
- **Canvas** was a side-by-side editor. It was removed from GPT-5.5 models in May 2026 and replaced by in-chat writing and code blocks and a full-screen editor.
- **Custom GPTs** (2023) are retiring on **2026-12-11** in favor of **plugins**, which bundle skills, reference files and apps.
- **Connectors** became **apps** built on **MCP** (Apps SDK, Oct 2025).
- **Agent mode** (Jul 2025) ran tasks on a virtual computer. It has been superseded by **ChatGPT Work** (2026-07-09), a long-running agent built on Codex technology.

For a clone, Projects and MCP-style tools are the durable concepts.

### Cited Findings
- **Projects**
  - **[Confirmed, 2024-12-13]** Launched for Plus, Team and Pro: they group files and chats with shared custom instructions. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, 2025-06-12]** Added deep research, voice, memory referencing chats within the project, sharing, and starting a project from a chat. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, 2025-09-03]** File limits per project: Free 5; Plus, Go and Edu 25; Pro, Business and Enterprise 40. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, 2025-10-23]** Shared projects for all users. **[Confirmed, 2026-02-25]** Sources can be added from apps, saved responses and pasted text ("a living knowledge base"). — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **Canvas**
  - **[Confirmed, 2024-12-10]** Available by default in GPT-4o for all users, with Python execution. **[Confirmed, 2025-02-06]** Canvas content can be shared. **[Confirmed, 2025-01-14]** Responses can be imported into canvas. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, 2026-05-28]** "canvas will no longer be available in GPT-5.5 Instant or GPT-5.5 Thinking". Writing and coding happen in writing and code blocks in chat instead. **[Confirmed, 2026-06-08]** Long-form writing opens in a full-screen editor that can save to Library. Interactive charts were added. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **Custom GPTs**
  - **[Confirmed, 2023-11-06 / 2024-01-10]** GPTs launched, followed by the GPT Store. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, current]** A GPT is made of instructions, knowledge files, connected apps, custom actions, a selected model and sharing settings. "Custom GPTs are scheduled to retire on Dec 11, 2026" (Feb 28, 2027 for FedRAMP and approved deferrals). Migration: "the GPT's instructions become a skill within the new plugin". Knowledge files become the plugin's reference files and apps carry over. "GPT custom actions do not transfer", so they must be rebuilt, possibly as a custom MCP server. Plugins "bring reusable instructions, reference files, and connected apps together." — [Custom GPT retirement and migration FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq)
- **Connectors, apps and plugins**
  - **[Confirmed, 2025-06-04]** Custom connectors via MCP, and connectors in deep research. **[Confirmed, Jul–Aug 2025]** Gmail, Calendar and Contacts connectors that ChatGPT "references automatically when relevant". — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
  - **[Confirmed, 2025-10-06]** Apps in ChatGPT and the Apps SDK. Users call an app by name or ChatGPT suggests one, and interactive UI renders inline. The SDK "is built on the Model Context Protocol (MCP)" and extends it so developers define both logic and interface. Users give consent on first connect. Developers must collect only the minimum data needed. — [Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)
  - **[Confirmed, 2025-12-17/18]** Connectors now appear as apps in a browsable directory. **[Confirmed, 2026]** Release notes now say "plugins" (e.g. iCloud Mail and Calendar plugins 2026-10-27; multiple accounts per plugin 2026-09-17). — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **Agent mode and ChatGPT Work**
  - **[Confirmed, 2025-07-17]** Agent mode runs on "its own virtual computer" with a visual browser, a text browser, a terminal, direct API access and connectors. It combines Operator and deep research, and asks permission before consequential actions. "Watch Mode" applies to critical tasks such as sending email. At launch Pro had 400 messages a month and other paid plans 40. The page now says it is outdated. — [Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)
  - **[Confirmed, 2026-07-09]** ChatGPT Work is an agent that can "take action across your apps and files" and stay on a project for hours. It is built on Codex technology and powered by GPT-5.6. It supports plugins addressed with "@", Scheduled Tasks (once, recurring, event-triggered), Computer Use and a built-in browser on desktop, and asks for approval on important actions. Rollout: Pro, Enterprise and Edu first on web and mobile. Chat, Work and Codex are in the desktop app on every plan. The Atlas browser is being sunset, and Sites is in public beta. — [ChatGPT for your most ambitious work (OpenAI)](https://openai.com/index/chatgpt-for-your-most-ambitious-work/); [Android Authority](https://www.androidauthority.com/chatgpt-work-launch-3685935/) **[Reported]**
- **Other features (dated)**
  - **[Confirmed]** Group chats: pilot 2025-11-13; creation retired 2026-07-09.
  - **[Confirmed]** Pulse (proactive daily updates): 2025-09-25; being sunset as of 2026-06-17.
  - **[Confirmed]** Scheduled tasks: beta 2025-01-14; webhooks and sharing 2026-08-25.
  - **[Confirmed]** Library launched 2025-04-15 and was replaced by Space on 2026-11-20.

  — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

### Inferences
- **[Inferred]** Projects ≈ a `project` row holding instructions, files and a memory scope, plus retrieval over uploaded files (vector store / file search) and project-scoped chat-history memory.
- **[Inferred]** OpenAI's 2025–2026 consolidation (GPTs → plugins, connectors → MCP apps, agent → Work) shows the durable building blocks are **system-prompt bundles ("skills") + reference files + MCP tools**. A clone should build these rather than copy the "GPT Store" or Canvas.

### Gaps
- No official technical description of how project files are retrieved (chunking, embeddings, context limits).
- ChatGPT Work's current per-plan usage numbers were not found.

---

## 8. Safety layer and usage limits per plan

### Takeaway
OpenAI documents its building blocks rather than ChatGPT's internal pipeline:
- the free **Moderation API** (`omni-moderation-latest`, text plus images, 13 categories);
- model-level "safe completions" (GPT-5);
- real-time checks for high-risk bio and cyber requests (GPT-5.6/6);
- safety routing for distress conversations;
- an opt-in Lockdown Mode.

As of Nov 2026, Free and Go have **unlimited everyday text chats** (abuse safeguards apply). Paid tiers are separated by reasoning depth and Pro-model allowances, and hidden mini models take over when limits are hit.

### Cited Findings
- **[Confirmed, current]** Moderation API:
  - `omni-moderation-latest` accepts text and images (up to 20 MB), not audio.
  - Categories: `harassment`, `harassment/threatening`, `hate`, `hate/threatening`, `illicit`, `illicit/violent`, `self-harm`, `self-harm/intent`, `self-harm/instructions`, `sexual`, `sexual/minors`, `violence`, `violence/graphic`. Image input is scored only on the self-harm, sexual and violence families.
  - Response fields: `flagged`, `categories`, `category_scores` (0–1), `category_applied_input_types`.
  - "The moderation endpoint is free to use."
  - Inline moderation is available via a top-level `moderation` object on Responses API calls, covering both input and output.
  - Guidance: start with `flagged` and treat scores as policy signals. With streaming, scores arrive only after the full output. Thresholds need recalibrating as the model is upgraded.

  — [OpenAI Moderation guide](https://developers.openai.com/api/docs/guides/moderation)
- **[Confirmed, 2025-08-07]** "Safe completions" were introduced with GPT-5: the model "give[s] the most helpful answer where possible" within safety limits. Sycophantic replies fell "from 14.5% to less than 6%". — [Introducing GPT-5](https://openai.com/index/introducing-gpt-5/)
- **[Confirmed, current]** GPT-5.6 has trained-in protections plus real-time checks. Some high-risk biological and cybersecurity requests may be refused or need additional checks. — [GPT-6 in ChatGPT](https://help.openai.com/en/articles/11909943-gpt-6-in-chatgpt)
- **[Confirmed, 2025-10-03]** Distress conversations are routed to GPT-5 Instant (see section 2). **[Confirmed, current]** In temporary chats, "safety features may still use limited context in rare, high-risk situations." — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); [Temporary Chat FAQ](https://help.openai.com/en/articles/8914046-temporary-chat-faq)
- **[Confirmed, 2026-06-04]** Lockdown Mode is an opt-in security setting for all logged-in users. It restricts live browsing, deep research and agent mode, which suggests a defense against prompt injection and data exfiltration. — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** Users can flag content with the thumbs-down icon or "Report" for possible Terms of Use or legal violations. — [OpenAI model behavior feedback form](https://openai.com/form/model-behavior-feedback)
- **[Confirmed, current]** Usage limits:
  - Free and Go: "Unlimited everyday text chats, subject to abuse-prevention safeguards", with separate limits on file uploads, image generation, voice and data analysis. No hourly or weekly counts are published.
  - Free and Go reasoning: Instant and Think on Luna.
  - Plus: up to High. Pro: Extra High and Pro.
  - Pro $100: one weekly allowance shared by GPT-6 Pro and GPT-5.6 Sol Pro.
  - Pro $200: higher allowances. When GPT-6 Pro's weekly limit is hit, ChatGPT switches to GPT-5.6 Thinking at Medium.
  - The reset time is shown when a limit is reached.

  — [GPT-6 in ChatGPT](https://help.openai.com/en/articles/11909943-gpt-6-in-chatgpt)
- **[Confirmed via search snippet, not full-page verified]** Pro $200: "200 messages per week" for GPT-6 Pro, and a "separate 170 messages per day for GPT-5.6 Sol Pro", with both "limited to 200 messages per day". — [GPT-5.6 and GPT-6 Pro in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt)
- **[Confirmed, plan history]** Plan and limit history:
  - Plus GPT-4: 40 messages per 3 hours (2023-07-19).
  - Plus GPT-5 Thinking: 3,000 a week (2025-08-12).
  - Go launched in India at ₹399/month (2025-08-18).
  - A $100 Pro plan was added (2026-04-09).
  - "Pro 500" appears with Pro 100 and Pro 500 getting double Work and Codex allowance, and the Pro 200 reduction was cancelled (2026-09-29 / 2026-10-29).

  — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

### Inferences
- **[Inferred]** ChatGPT almost certainly runs classifiers like the Moderation API on both inputs and outputs, plus model-level refusal training and specialized classifiers for bio, cyber and self-harm. A clone should call the free Moderation API on every user message before generation, and on the final output (or chunks) after generation, and log `category_scores`.
- **[Inferred]** Limits are enforced per user, per model and per time window (rolling hours or weeks), with automatic fallback to a cheaper model rather than a hard block. A clone needs a usage-counter table keyed by (user, model, window) from the start if it offers tiers.

### Gaps
- ChatGPT's internal moderation pipeline (which classifiers, thresholds, and where they sit) is not public.
- Exact Free, Go and Plus message caps for 2026 are not published as numbers. Usage policy text was not fetched in this pass.

---

## 9. Feedback (thumbs up / thumbs down)

### Takeaway
Thumbs feedback is a **training signal**. OpenAI confirmed it used thumbs data as an extra reward signal in RLHF (this contributed to the April 2025 GPT-4o sycophancy incident). Giving feedback can make the whole conversation eligible for training even if the user opted out. Model-switching behavior and preference rates also train the router.

### Cited Findings
- **[Confirmed, 2025-05-02]** The April 25, 2025 GPT-4o update "introduced an additional reward signal based on user feedback—thumbs-up and thumbs-down data from ChatGPT". "User feedback in particular can sometimes favor more agreeable responses", which likely amplified sycophancy. A/B tests and offline evals failed to catch it. The update was rolled back on 2025-04-29. — [Expanding on what we missed with sycophancy](https://openai.com/index/expanding-on-sycophancy/); [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed, current]** If a user gives feedback (e.g. thumbs up or down), "the entire conversation associated with that feedback may be used to train OpenAI models", even with training opted out. "Improve the model for everyone" is on by default for personal Free, Plus and Pro accounts. — [Data Controls FAQ](https://help.openai.com/en/articles/7730893-data-controls-faq)
- **[Confirmed, 2025-08-07]** The GPT-5 router is trained on "when users switch models, preference rates for responses, and measured correctness." — [Introducing GPT-5](https://openai.com/index/introducing-gpt-5/)
- **[Confirmed, current]** Thumbs-down and "Report" are the in-product feedback channels. — [Model behavior feedback form](https://openai.com/form/model-behavior-feedback)
- **[Reported, 2024]** An academic study of the feedback features in ChatGPT's interface and how they are used. — [arXiv 2408.15066, "Constraining Participation"](https://arxiv.org/html/2408.15066v2)

### Inferences
- **[Inferred]** "Which response do you prefer?" side-by-side prompts (seen in ChatGPT) are pairwise preference collection for reward modeling. A clone should store feedback as (message_id, model, rating, optional reason/text, timestamp) for evals, even without training models.

### Gaps
- No official description of the thumbs-down reason taxonomy or of how often A/B preference prompts are shown.

---

## 10. Suggested build order for a ChatGPT clone (MVP vs. later)

### Takeaway
Build the core loop first: streaming chat, stop, a persisted **tree** of messages (edit and regenerate), auto titles, a model picker, custom instructions, moderation, feedback and per-user rate limits. Add search, files and Projects, memory, sharing, export and temporary chats next. Skip or defer features OpenAI itself is retiring (Canvas, Custom GPTs, group chats, the auto-router for paid users).

### Cited Findings
- **[Confirmed]** OpenAI retired or deprecated these in 2026:
  - automatic Instant-to-Thinking switching for Plus and Pro (2026-09-14);
  - Canvas in GPT-5.5 models (2026-05-28);
  - group chat creation (2026-07-09);
  - Pulse (being sunset, 2026-06-17);
  - custom GPTs (retiring 2026-12-11).

  — [ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); [Custom GPT retirement FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq)
- **[Confirmed]** Ready-made API building blocks exist for: moderation (free) — [Moderation guide](https://developers.openai.com/api/docs/guides/moderation); web search with citations — [Web search tool](https://developers.openai.com/api/docs/guides/tools-web-search); and MCP-based tools/apps — [Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)

### Inferences
**MVP (build first)**

| # | Feature | One-line reason |
|---|---|---|
| 1 | Auth + streaming chat (SSE) + Stop button | This is the product. Abort-on-stop is trivial once streaming exists. |
| 2 | Conversations stored as a **message tree** (`parent_id`, `current_node`) | Edit, regenerate, version switching and branching all depend on it, and it is painful to retrofit. |
| 3 | Sidebar history + rename/delete + auto title (async cheap-model call after first message) | Basic navigation. Titles cost one small LLM call. |
| 4 | Edit message / regenerate / `< n/m >` version switcher | High user value once the tree exists. Only UI work. |
| 5 | Model picker (manual; optional "reasoning effort" toggle) | Simple, and OpenAI itself moved to explicit user choice in 2026. |
| 6 | Custom instructions (≤5k chars) injected into the system prompt | Cheap, high value, one settings row. |
| 7 | Moderation API on input (and on final output) | Free, and needed for any public deployment. |
| 8 | Thumbs up/down + optional comment, stored per message | Cheap, and it is the only quality signal you'll have. |
| 9 | Per-user / per-model rate limits with fallback model | Controls cost from day one, and needed for Free vs Paid tiers. |

**Later (v2, roughly in this order)**

| # | Feature | One-line reason |
|---|---|---|
| 10 | Web search tool + inline citations + Sources panel | Biggest answer-quality gain. The API `web_search` tool makes it mostly a UI job. |
| 11 | File uploads → Projects (files + project instructions + retrieval) | Core power-user workflow. Needs a vector store and file pipeline. |
| 12 | Shared links (immutable snapshot of the active branch, `noindex`, "continue" forks a copy) | Growth loop. Simple once the tree exists. |
| 13 | Temporary chat (hidden from history, no memory writes, 30-day TTL) | Mostly flags and a cleanup job. Privacy expectation. |
| 14 | Archive + data export (async ZIP with JSON tree, emailed link valid 24h) | Privacy and compliance. Low complexity. |
| 15 | Memory v1: saved memories via a `save_memory` tool + system-prompt injection + management UI | Strong stickiness, but needs controls (view, delete, off) to avoid trust issues. |
| 16 | Memory v2: retrieval over past chats with "sources" shown | OpenAI's 2026 direction, but it needs embeddings and careful privacy UX. |
| 17 | Reasoning display (show model reasoning summaries / plan while thinking) | Nice transparency once reasoning models are offered. |
| 18 | Automatic router / auto-switch (heuristic or small classifier) | Optimizes cost. Add only once there is usage data, since OpenAI made it optional for paid users. |
| 19 | Tools via MCP ("apps"/"plugins": skills + reference files + MCP servers) | The extensibility pattern OpenAI settled on. Replaces building a GPT Store. |
| 20 | Agent mode (sandboxed browser/terminal, approvals, scheduled tasks) | Highest infrastructure and safety cost. Build last. |

**Skip or deprioritize:** Canvas (removed from GPT-5.5 models in May 2026), a Custom GPT Store (retiring Dec 2026), group chats (creation retired Jul 2026), Pulse-style proactive feeds (being sunset).

### Gaps
- The build order is my own judgment based on the cited dependencies. It is not an OpenAI recommendation.
