# Project kickoff discussion (2026-11-22)

Verbatim log of the planning conversation between Muhammad Abdullah and the AI coding assistant that set up this repository: research on how ChatGPT is built, the tech stack, the folder structure, the guardrails, and Phase 0.

- Muhammad Abdullah's messages were dictated by voice in Urdu, and the dictation wrote them in Hindi (Devanagari) script. Here they are converted to Urdu script, with technical terms in English and obvious dictation mistakes fixed.
- The assistant's replies are in Roman Urdu, kept exactly as sent.
- Tool calls and their output are left out. Multiple-choice questions and the chosen answers are kept.

---

### Muhammad Abdullah

ہیلو Claude، ہم ابھی کوشش کرنے لگے ہیں کہ ChatGPT کا clone بنائیں، ٹھیک ہے۔ تو ابھی تم ہمارے لیے project کا structure بناؤ۔ اس میں اپنی CLAUDE.md فائل بناؤ، اور میں اسے ایسے بنانا چاہتا ہوں کہ اگر میں یہ folder کسی بھی اور agent کے ساتھ connect کروں، VS Code، Cursor کسی کے ساتھ بھی، تو اس میں مشترکہ یعنی common guidelines ہوں جو سب کے لیے ہوں، تاکہ وہ انہیں follow کریں اور انہیں follow کرتے ہوئے system بنائیں۔ اچھا، اب rules کیا کیا ہوں گے: جب بھی کوئی concept آئے گا، کوئی مشکل concept آ گیا، یا میں کوئی بھی بات پوچھ رہا ہوں، اسے آسان زبان میں simple explain کرو گے۔ over-explain نہیں کرنا اور کوئی پچھلا background ساتھ نہیں لگانا۔ مجھے to the point چیزیں بتانی ہیں کہ کیا ہوگا، کیسے ہوگا، اور میری help کرنی ہے۔ اور میں تم سے بات اردو میں ہی کروں گا، لیکن جو folder structure بنے گا، files بنیں گی، file میں جو لکھا ہوگا، وہ سب English میں ہوگا۔ comments، ہماری CLAUDE.md، جو کچھ بھی بنے گا، وہ سارے کا سارا English میں ہوگا، ٹھیک ہے۔ تو ابھی ایک پورا folder structure بناؤ، ہم ChatGPT کا clone بنانے لگے ہیں۔ folder structure سے مراد یہ ہے کہ ابھی کوئی file وغیرہ نہ بنانا۔ ابھی صرف ایک common شروعات کرو: git initialize کر دو، agents کے لیے common guidelines لکھ دو، وہ سارا کچھ کر دو۔

---

### Assistant

Setup ho gaya. Git `main` branch ke saath shuru ho gaya hai, aur yeh 4 files bani hain:

```
chatgpt-clone/
├── .git/
├── AGENTS.md     ← sab agents ke liye common rules (asal file yahi hai)
├── CLAUDE.md     ← sirf AGENTS.md ko load karti hai
├── README.md     ← project ka chhota sa taaruf
└── .gitignore    ← .env, node_modules wagaira git mein nahi jayenge
```

**Yeh har tool mein kaise chalega:**
- Cursor, VS Code Copilot, Codex aur Windsurf `AGENTS.md` khud parhte hain.
- Claude Code `CLAUDE.md` parhta hai, aur us mein `@AGENTS.md` likha hai, is liye woh bhi wahi rules uthata hai.
- Koi naya rule ho to sirf `AGENTS.md` mein likhein. Woh sab agents par lag jayega.

**`AGENTS.md` mein yeh rules hain:**
- Aap Urdu mein baat karenge aur agent Urdu mein jawab dega.
- Files, folders, code, comments aur commit messages sab English mein honge.
- Agent cheezein aasaan zubaan mein aur seedhi baat mein samjhayega. Na zyada lamba jawab, na background.
- Agent tech stack ya library khud nahi chunega, aap se poochega.
- API keys sirf `.env` mein rahengi aur kabhi commit nahi hongi.
- Commit tab hi hoga jab aap kahenge.

Main ne jawab ke liye Roman Urdu rakha hai, kyun ke terminal mein Urdu script aksar theek se nazar nahi aati. Agar Urdu script chahiye to bata dein, main rule badal dunga.

Abhi kuch commit nahi kiya. Kahein to pehla commit kar dun? Agla qadam tech stack chunna hai (maslan Next.js ya React + backend), us ke baad `AGENTS.md` ke khali hisse bhar denge.

---

### Muhammad Abdullah

اچھا یار، اب اس میں یہ rule add کرو کہ جب GitHub پر push کرنا ہے، تو ایک تو ہوگی main branch، ٹھیک ہے، اور جب بھی کوئی نیا feature بنے گا، کوئی بھی نئی چیز بنے گی، اسے branch میں بنانا ہے۔ branch بنے گی، اس کی PR open ہوگی، وہ review ہوگی، پھر merge ہوگی، as a professional developer، ٹھیک ہے۔ تو ابھی ہم نے اس میں کام کرنا ہے، تو تمہارا role یہ ہے کہ تم نے ایک experienced Solution Architect اور AI Platform Engineer کی طرح سوچنا ہے، ٹھیک ہے، اور اسی طرح ہم نے اس project کے اندر کام کرنا ہے۔ تو وہ سب rules اور guardrails بھی۔ اب میں AI سے، Claude سے کام کروں گا، تو AI کے اوپر کچھ guardrails بھی چاہیے ہوں گے، وہ بھی ایک engineer کی طرح اچھے سے apply کرو۔ پھر مجھے بتاؤ، پورا folder structure ready کرو اور rules بھی add کرو۔

---

### Assistant (question)

**ChatGPT clone ka tech stack kya ho? Isi se app ka folder structure banega (rules aur guardrails stack se alag hain, woh main har haal mein bana raha hoon).**
- Next.js + FastAPI (Recommended): Do apps: frontend/ (Next.js, TypeScript) aur backend/ (Python FastAPI). LLM calls, API keys aur AI logic backend mein rahenge. AI platform ke liye professional setup.
- Sirf Next.js (full-stack): Ek hi app: UI aur API routes dono Next.js mein. Kam moving parts, jaldi start, lekin AI logic aur UI ek hi jagah.
- Baad mein decide: Abhi sirf rules, guardrails, docs aur GitHub setup. App ke folders stack decide hone par banenge.
**GitHub par repo abhi bana dun? (Active gh account: MuhammadAbdullah95.) GitHub ke free plan par main branch protection sirf public repo par milti hai.**
- Public repo + protection (Recommended): Public repo banega, initial commit push hoga, aur main protect hoga: direct push aur force push band, sirf PR se merge.
- Private repo: Code private rahega. Free plan par GitHub protection nahi milegi, is liye sirf local git hooks main ko bachayenge.
- Abhi nahi: Sirf local setup. GitHub repo baad mein banayenge.

---

### Muhammad Abdullah (answer)

Your questions have been answered: "ChatGPT clone ka tech stack kya ho? Isi se app ka folder structure banega (rules aur guardrails stack se alag hain, woh main har haal mein bana raha hoon)."="Baad mein decide", "GitHub par repo abhi bana dun? (Active gh account: MuhammadAbdullah95.) GitHub ke free plan par main branch protection sirf public repo par milti hai."="Public repo + protection (Recommended)". You can now continue with these answers in mind.

---

### Assistant

Stack baad mein decide hoga, aur GitHub par public repo protection ke saath banega. Pehle saari files bana raha hoon.

Ab hooks ko executable bana kar on kar raha hoon, phir Claude ki settings file likhunga.

Initial commit ho gaya. Ab GitHub par jaane se pehle hooks ko ek alag test copy mein check kar raha hoon.

Test command ruk gaya. Shayad wajah `rm -rf` aur `core.hooksPath` hain, jin par abhi abhi "pehle poocho" wala rule lagaya hai. Test ko in dono ke baghair dobara chala raha hoon.

zsh variable ko split nahi karta, is liye function ke saath dobara chala raha hoon.

Saare 7 tests pass ho gaye. Ab GitHub par check karta hoon ke is naam ka repo pehle se to nahi hai.

Repo ban gaya aur push ho gaya. Ab `main` par branch protection aur merge settings laga raha hoon.

Setup poora ho gaya aur GitHub par bhi chala gaya hai: https://github.com/MuhammadAbdullah95/chatgpt-clone

**Folder structure:**
```
chatgpt-clone/
├── .claude/settings.json             ← Claude ke guardrails
├── .githooks/pre-commit, pre-push    ← main ko bachane wale hooks (har tool ke liye)
├── .github/pull_request_template.md  ← har PR ka checklist
├── docs/adr/0000-template.md         ← bade faislon ka record
├── .editorconfig, .gitignore
├── AGENTS.md                         ← saare rules yahan hain
├── CLAUDE.md                         ← AGENTS.md ko load karti hai
└── README.md
```
App ke folders abhi nahi banaye, kyun ke aap ne stack baad mein decide karna hai.

**Kaam ka tareeqa (`AGENTS.md` mein likha hai):**
1. `main` se nayi branch banegi, jaise `feat/chat-input`.
2. Kaam hoga, phir PR khulegi.
3. Pehle AI review karega (`/code-review`), phir aap diff dekhenge.
4. Aap squash merge karenge aur branch khud delete ho jayegi.

**Agent ka role:** Solution Architect aur AI Platform Engineer ki tarah sochega. Bada faisla khud nahi karega: options dega, aap chunenge, aur faisla `docs/adr/` mein record hoga.

**Guardrails teen level par hain:**
- **Git hooks:** `main` par commit ya push, `.env` files aur API keys block hoti hain. Yeh Cursor, VS Code ya kisi bhi tool se commit karne par chalte hain.
- **GitHub protection:** `main` mein sirf PR se merge hoga. Force push aur branch delete band hain, aur PR ke comments resolve kiye baghair merge nahi hoga.
- **Claude permissions:** Claude `.env` nahi parh sakta aur force push ya `main` par push nahi kar sakta. PR merge, `rm -rf` aur `reset --hard` se pehle aap se poochega.

**Test kiya:** hooks ke 7 cases chalaye (main par commit, `.env`, nakli API key, main par push, wagaira) aur sab ne sahi kaam kiya. GitHub ki protection settings bhi wapas parh kar confirm ki hain.

**Do baatein dhyan mein rakhein:**
- Approvals 0 rakhe hain, kyun ke GitHub par aap apni PR khud approve nahi kar sakte. Koi teammate aaye to 1 kar dena. PR phir bhi zaroori hai.
- Claude ki nayi permissions pakki lagne ke liye Claude Code ek dafa restart kar lein.

Agla qadam tech stack ka faisla hai. Woh pehli branch (`docs/adr-tech-stack`) aur pehli PR ban jayega.

---

### Muhammad Abdullah

ٹھیک ہے، ابھی ہمارا folder ready ہو گیا۔ اچھا، اب ہم app بنانا start کرتے ہیں۔ تو سب سے پہلے ہم research کرتے ہیں کہ ChatGPT جو بنا ہوا ہے وہ بنا کیسے ہے، اس میں tech stack کیا ہے، اس میں چیزیں کیسے چل رہی ہیں، اس میں کون کون سی چیزیں ہیں۔ جیسے وہ session manage کر رہے ہوتے ہیں، side پر میری chat history نظر آ رہی ہوتی ہے، streaming ہو رہی ہوتی ہے، وہ images کو سمجھ رہا ہوتا ہے، voice کو بھی سمجھ رہا ہوتا ہے، ایک اچھا سا UI ہے، backend ہے، database ہے۔ تو پہلے یہ ساری چیزیں دیکھتے ہیں کہ وہ اصل میں بنی کیسے ہیں، پھر انہیں دیکھ کر ہم اپنا بنائیں گے، کیونکہ ہم بالکل اسی طرح کا اپنا بنانا چاہ رہے ہیں۔

---

### Assistant

Pehle apne rule ke mutabiq is kaam ke liye nayi branch bana raha hoon, phir research shuru karunga.

Branch `docs/chatgpt-research` ban gayi. Ab 5 researchers ek saath laga raha hoon, har ek alag hissa dekhega: frontend, backend, images/voice, infrastructure aur features.

Research shuru ho gayi hai. Paanch researchers ek saath alag alag hissa dekh rahe hain:

1. **Frontend:** UI kis cheez se bana hai, streaming text screen par kaise aata hai, aur sidebar kaise kaam karta hai.
2. **Backend:** server ki language, streaming ka tareeqa, chats kahan aur kaise save hoti hain, login aur session.
3. **Images aur voice:** image upload, files, voice mode, aur WebRTC/LiveKit.
4. **Infrastructure:** Azure, Kubernetes, Cloudflare aur feature flags.
5. **Features:** chat ka title, memory, share link, search, aur clone mein kaun si cheez kis tarteeb se banayein.

Har baat ke saath likha hoga ke woh OpenAI ne khud confirm ki hai, kisi aur ne report ki hai, ya andaza hai. Sources bhi saath honge.

Sab ke khatam hone par ek poori report banegi. Woh branch `docs/chatgpt-research` par `docs/research/reports/How ChatGPT is built.md` mein save hogi, aur phir main aap ko Urdu mein short summary dunga.

Frontend wala hissa mukammal ho gaya hai, baaqi chaar abhi chal rahe hain. Sab ke khatam hone par poori report banegi.

Backend wala hissa bhi mukammal ho gaya. Ab teen baaqi hain: images aur voice, infrastructure, aur features.

Images aur voice wala hissa bhi mukammal ho gaya. Ab do baaqi hain: infrastructure aur features.

Features wala hissa bhi mukammal ho gaya. Ab sirf infrastructure baaqi hai, us ke baad report likhwaunga.

Saare 5 researchers ka kaam mukammal ho gaya. Ab report writer in sab notes ko mila kar ek report likhega.

Report likhi ja rahi hai. Mukammal hote hi aap ko Urdu mein short summary dunga.

Research mukammal ho gayi. Poori report English mein yahan hai: `docs/research/reports/How ChatGPT is built.md`. Har baat ke saath source hai, aur likha hai ke woh OpenAI ne confirm ki hai, kisi aur ne report ki hai, ya andaza hai.

**ChatGPT kaise bana hai, short mein:**

| Hissa | Kya use hota hai |
|---|---|
| Frontend | React + TypeScript (OpenAI ki job postings se confirm). React Router 7, Vite, Tailwind, Radix UI bahar se dekh kar pata chale hain |
| Backend | Zyada tar Python + FastAPI. Voice ka server Go mein hai |
| Streaming | SSE: ek POST request khuli rehti hai aur jawab chhote chhote tukron mein aata hai. Text ke liye WebSocket nahi |
| Database | Ek bada PostgreSQL aur us ki ~50 copies sirf parhne ke liye, Redis cache, aur naye bhaari data ke liye Cosmos DB |
| Chat ka structure | Har chat messages ka **tree** hai. Message edit ya regenerate karne par nayi branch banti hai, purana jawab mitta nahi |
| Sidebar | Chats 28 28 kar ke load hoti hain, nayi sab se upar. Title ek alag chhoti model call banati hai |
| Login | Email, Google, Microsoft, Apple. Lambi chalne wali cookie aur har request ke liye chhota token |
| Images | Pehle file upload hoti hai, phir message mein sirf us ki ID jaati hai |
| Voice | Live audio WebRTC (LiveKit) par. Naya GPT-Live sunte hue saath saath bol bhi sakta hai |
| Infra | Kai clouds (Azure, AWS, Oracle) par Kubernetes, aur aage Cloudflare |

**Sab se badi seekh:** ChatGPT ka app wala hissa aam tools se bana hai. Asal mushkil GPUs chalane ki hai, aur woh hamein nahi karna. Hum model ki API call karenge.

**Do faisle jo baad mein badalna mushkil hai, is liye shuru mein soch kar karne hain:**
1. Messages ko tree ki shakal mein save karna.
2. Streaming events ka format.

**Pehle version (MVP) ke 11 hisse:** chat screen, login, streaming endpoint, model gateway, chat database (tree), sidebar, edit/regenerate, model picker aur custom instructions, safety aur rate limits, feedback, aur logs/monitoring. Images, voice, search aur memory baad mein aayenge.

**Ek ehtiyat:** OpenAI ne chatgpt.com ka architecture kabhi officially publish nahi kiya. Frontend aur andar ki API ki zyada tar details bahar se dekh kar nikali gayi hain, aur yeh badal bhi sakti hain.

Sab kuch branch `docs/chatgpt-research` par hai, abhi commit nahi kiya. Report aur researchers ke notes commit kar ke PR khol dun? Us ke baad agla qadam isi report ki buniyad par tech stack ka faisla (ADR) hai.

---

### Muhammad Abdullah

اچھا ٹھیک ہے، ابھی تم نے research کر لی اور سارا کچھ مل گیا۔ اب ہم final conclusion پر آتے ہیں کہ اب ہمیں کرنا کیا ہے۔ ہمیں ایک full product چاہیے جو میرے system پر run ہو، بالکل ChatGPT کی طرح: UI، backend، اور اس میں جو جو functionalities ہیں وہ ساری implement ہوں۔ تو ابھی ہمیں کیا کرنا ہے، کون سا tech stack choose کرنا ہے اور کیسے کام کرنا ہے، مجھے ایک پورا overview دو، conclusion بتاؤ کہ اب ہمیں کیا کرنا ہے۔

---

### Assistant

Final faisle se pehle do aham libraries ki current docs check kar raha hoon, taake recommendation purani maloomat par na ho.

Do aham baatein docs se pakki kar li hain:
- Pydantic AI ka `VercelAIAdapter` FastAPI se jawab seedha Vercel AI SDK ke format mein stream karta hai.
- Better Auth ka JWT plugin ek alag Python backend ko login verify karne deta hai.

Neeche mera mashwara hai.

## Conclusion

Do apps banengi: **Next.js frontend** aur **FastAPI backend**. Database ke liye **PostgreSQL** aur **Redis** Docker mein chalenge. Sab kuch aap ke laptop par chalega. Kaam 11 phases mein hoga, aur har feature apni branch aur PR se aayega.

## Architecture

```
Browser (Next.js UI)
   │  login ─────────► Better Auth (Next.js ke andar)
   │  chat (POST, SSE stream)
   ▼
FastAPI backend ── Model gateway (Pydantic AI) ──► LLM provider
   │                                              (OpenAI / Gemini / Claude / Ollama)
   ├── PostgreSQL   users, chats (tree), messages; baad mein memory (pgvector)
   ├── Redis        rate limits, cache, background jobs
   └── File storage pehle local disk, baad mein S3
```

## Tech stack

| Hissa | Choice | Kyun |
|---|---|---|
| Frontend | Next.js + TypeScript + Tailwind + shadcn/ui | ChatGPT bhi React aur Tailwind par hai, aur shadcn usi Radix UI par bana hai jo ChatGPT use karta hai |
| Chat UI | Vercel AI SDK (`useChat`) + Streamdown | Streaming, stop button, aur adhoore markdown ko sambhalna pehle se bana hua milta hai |
| Backend | Python + FastAPI | ChatGPT ka backend bhi yahi hai, aur AI ki libraries Python mein sab se achhi hain |
| Model gateway | Pydantic AI | Provider sirf config se badal jata hai, aur streaming standard format mein milti hai, apna protocol nahi banana parega |
| Database | PostgreSQL + SQLAlchemy + Alembic | ChatGPT bhi Postgres use karta hai. Is mein JSON aur tree dono aasaani se save hote hain, aur baad mein memory ke liye alag vector DB nahi chahiye hoga |
| Cache aur jobs | Redis | Rate limits, cache, background jobs (jaise title banana), aur stream resume |
| Login | Better Auth + FastAPI mein JWT verify | Tested library hai aur Google login deti hai. Security code khud likhna khatarnak hota hai |
| Local run | Docker Compose (Postgres, Redis) + `pnpm dev` + `uv run` | Ek command se sab chal jayega |
| Quality | Ruff, pytest, ESLint, Vitest, Playwright + GitHub Actions CI | Har PR par tests khud chalenge |

**Sirf Next.js kyun nahi?** Alag backend hoga to AI ka kaam Python mein rahega aur API saaf alag hogi. Baad mein mobile app bhi isi backend ko use kar sakti hai.

**Do cheezein shuru se pakki hongi:** messages tree ki shakal mein save honge, aur streaming ka format standard hoga. Research ke mutabiq yahi dono baad mein badalna sab se mushkil hai.

## Folder structure

```
chatgpt-clone/
├── apps/
│   ├── web/                  Next.js (UI + login)
│   └── api/                  FastAPI (chat, history, files, voice)
├── infra/docker-compose.yml  Postgres + Redis
├── docs/                     adr, research, roadmap
└── .github/workflows/ci.yml
```

## Roadmap

| Phase | Kya banega | Result |
|---|---|---|
| 0 | Scaffold, Docker, CI | Dono apps chal rahi hongi |
| 1 | Streaming chat, markdown/code, stop | Pehla jawab screen par aayega |
| 2 | Login (Google + email), chats ka tree ki shakal mein save hona | Reload ke baad bhi chat bachi rahegi |
| 3 | Sidebar, auto titles, rename/delete/archive/pin | ChatGPT jaisi history |
| 4 | Edit, regenerate, versions, model picker, custom instructions | |
| 5 | Rate limits, moderation, feedback, logs, cost tracking | **MVP mukammal** |
| 6 | Images aur files (vision, PDF) | |
| 7 | Web search with citations, stream resume | |
| 8 | Projects aur memory | |
| 9 | Voice: dictation, read aloud, live voice (WebRTC) | |
| 10 | Image generation, share links, temporary chat, export | |
| 11 | Tools (MCP), code sandbox | |

Ek haqeeqat: features ChatGPT jaise honge, lekin scale aap ke laptop wala hoga. Model hum khud nahi chalayenge, provider ki API use karenge.

## Kaam kaise hoga

1. Har phase se pehle ek chhota plan banega aur aap approve karenge.
2. Har feature apni branch par banega, tests ke saath, phir PR khulegi.
3. Pehle AI review karega, phir aap dekh kar merge karenge.
4. PRs chhoti rakhenge, aur har qadam main aasaan alfaaz mein samjhaunga.

## Aap ka faisla chahiye: LLM provider

| Provider | Faida | Kami |
|---|---|---|
| OpenAI | Saare features ek jagah: vision, voice, image generation, search, aur moderation free | Paid hai |
| Gemini | Free tier hai, aur vision, live voice aur image generation bhi hain | Free tier ki limits hain |
| Claude | Chat aur coding mein bahut strong, vision bhi hai | Voice aur image generation ke liye doosra provider chahiye hoga |
| Ollama (local) | Free, private, internet ki zaroorat nahi | Achhi GPU chahiye, aur voice/image features kamzor hain |

Gateway har haal mein multi-provider hoga, is liye provider baad mein bhi badla ja sakta hai. ChatGPT jaise poore features ke liye mera mashwara OpenAI hai. Budget tight ho to Gemini ke free tier se shuru karein.

**Do sawal:**
1. Yeh stack aur roadmap theek hai, ya kuch badalna hai?
2. Aap ke paas kis provider ki API key hai?

Haan kehne par main `docs/adr/0001-tech-stack.md` aur `docs/roadmap.md` nayi branch par likh kar PR khol dunga. Research wali branch ki PR bhi saath khol dunga. Us ke baad Phase 0 shuru hoga.

---

### Muhammad Abdullah

اچھا یار، اس میں جو tech stack ہے وہ مجھے ٹھیک لگ رہا ہے۔ FastAPI اور Next.js ہم use کرنے والے ہیں۔ Next.js میں TypeScript کا جو version ہے، میرا خیال ہے ہم TypeScript 7 use کر لیتے ہیں، جو مجھے لگتا ہے fast ہے۔ حال ہی میں میں نے اس پر تھوڑا سا دیکھا تھا۔ اور provider ہم OpenAI ہی use کریں گے، اس کی API key میرے پاس ہے۔ اور FastAPI ہم use کر رہے ہیں، تو کیا FastAPI fast ہوگا، reliable ہوگا، scalable ہوگا؟ ذرا اس کے بارے میں بتانا۔ اور دوسرا ایک feature ہوتا ہے، میں نے ابھی try کیا: اگر میں ChatGPT کو کوئی message بھیجتا ہوں، اور message بھیج کر فوراً refresh کر دیتا ہوں یا میرا internet connection کٹ جاتا ہے تو کیا ہوگا؟ refresh کی صورت میں تو اس نے response پورا کر دیا، مجھے پتا چل گیا، لیکن اگر internet کٹ گیا تو پھر کیا ہوگا؟ یہ edge cases بھی مجھے ذرا بتانا، ہم اس چیز کو کیسے handle کریں گے اور یہ کیا ہوگا؟

---

### Assistant

Stack final ho gaya: **Next.js + TypeScript 7 + FastAPI + OpenAI**. Aap ke teeno sawalon ke jawab neeche hain.

## 1. TypeScript 7: haan, use kar sakte hain

- TypeScript 7.0 **8 July 2026 ko stable release** hua. Yeh Go mein dobara likha gaya compiler hai aur builds taqreeban **10 guna tez** hain.
- Next.js 16.4 ki official docs ke mutabiq `next build` ab khud project ka `tsc` chalata hai, is liye sirf `typescript@^7` install karna hai. Koi aur setting nahi chahiye.
- **Ek kami:** TS 7 mein abhi JavaScript API nahi hai (woh 7.1 mein aayegi). Is liye ESLint ke "type-aware" rules abhi nahi chalenge, aur Next.js build ke type errors simple `tsc` format mein dikhayega. Hum ESLint ke normal rules use karenge, aur 7.1 aane par type-aware rules on kar denge.

## 2. FastAPI: fast, reliable, scalable?

- **Fast:** Python ke sab se tez frameworks mein se hai, aur async hai. Hamari app ka asal intezar OpenAI ka jawab hai, jo seconds leta hai. FastAPI ka apna waqt milliseconds mein hai. Async ki wajah se ek process hazaron khule streams sambhal leta hai.
- **Reliable:** ChatGPT khud zyada tar Python + FastAPI par chalta hai. Python asyncio OpenAI ne confirm kiya hai, FastAPI unke engineers ne 2025 ke interview mein bataya. Reliability framework se zyada hamare design se aati hai: timeouts, retries, health checks.
- **Scalable:** Server khud koi data apne paas nahi rakhega, sab Postgres aur Redis mein hoga. Load badhe to server ki aur copies chala do.
- **Do rules jo hum follow karenge:**
  1. Async code mein koi blocking call nahi hogi (jaise `requests` ya `time.sleep`), warna sab users atak jayenge.
  2. CPU ka bhaari kaam (PDF parhna, image resize karna) background worker mein jayega.

## 3. Refresh aur internet cut: kya hoga, kaise sambhalenge

**Asal baat:** jawab banna browser ke connection se alag hona chahiye. Agar jawab connection se juda ho, to connection tootte hi jawab bhi mar jata hai. ChatGPT mein bhi refresh karne par jawab server par banta rehta hai.

**Hamara design:**
```
POST /chat ─► DB: user message + khali assistant message (status: generating)
          └─► background task (browser se azad)
                OpenAI ──tokens──► Redis Stream (buffer, numbered) ──► end par DB mein save
Browser ◄── SSE ── Redis Stream se parhta hai

Reconnect: GET /chat/{id}/stream ─► Redis se shuru se replay + live jaari
           (koi active jawab nahi to 204, phir DB se poora jawab)
```
Client side par Vercel AI SDK ka `useChat({ resume: true })` reconnect khud karta hai. Docs mein yahi tareeqa hai.

| Halat | Kya hoga |
|---|---|
| Jawab ke beech refresh | Server likhta rehta hai. Page khulte hi Redis se jud kar jawab wahin se live chalta hai |
| Internet cut | Server jawab poora kar ke DB mein save kar deta hai. UI "Reconnecting…" dikhata hai, aur internet aate hi khud jud jata hai |
| Bhejte waqt internet cut (message server tak nahi pohncha) | "Not sent, Retry" dikhega. Har message ki apni ID hogi, is liye dobara bhejne par duplicate nahi banega |
| Stop button | Server ko alag cancel request jayegi, aur jitna jawab bana woh "stopped" ke saath save hoga. Ab connection tootne ka matlab sirf "disconnect" hai, "stop" nahi |
| Server crash ya restart | Message "generating" mein phansa rahega. Cleanup job kuch der baad usay "interrupted" kar degi aur UI mein Regenerate ka button aayega |
| OpenAI error ya timeout | Pehla token aane se pehle error aaye to khud retry hoga. Baad mein aaye to adhoora jawab rahega aur Retry ka button aayega |
| Jawab ke dauran doosra message | Usi chat mein block hoga, jaise ChatGPT mein hota hai |
| Do tabs mein wahi chat | Dono tabs ek hi Redis stream se judenge |
| Tab band kar ke chale gaye | Jawab phir bhi poora ho kar save hoga. Cost `max_tokens` ki limit se qaboo mein rahegi |

**Roadmap mein tabdeeli:** pehle "stream resume" Phase 7 mein tha. Ab yeh **Phase 1–2 mein hi** banega, kyun ke baad mein jodna bohat mehnga padta hai.

**OpenAI key:** key chat mein paste na karein. Phase 0 mein woh `apps/api/.env` mein jayegi. Yeh file git mein nahi jaati, aur hamara hook usay commit hone se bhi rokta hai.

## Agla qadam

Main `docs/adr/0001-tech-stack.md` (stack, TS 7, OpenAI, aur yeh streaming design) aur `docs/roadmap.md` likh dun? Phir research aur ADR dono ki PRs khol dunga, aur us ke baad Phase 0 (scaffold) shuru hoga.

Sources:
- [Next.js docs: TypeScript 7 / useTypeScriptCli](https://github.com/vercel/next.js/blob/v16.4.5/docs/01-app/03-api-reference/05-config/02-typescript.mdx)
- [InfoQ: TypeScript 7.0 released](https://www.infoq.com/news/2026/08/typescript-7-released/)
- [Visual Studio Magazine: TypeScript 7.0 RC](https://visualstudiomagazine.com/articles/2026/06/22/typescript-7-0-rc-moves-microsofts-go-rewrite-into-the-mainline-compiler.aspx)
- [Next.js 16.3 blog](https://nextjs.org/blog/next-16-3)
- [AI SDK docs: Chatbot resume streams](https://ai-sdk.dev/v6/docs/ai-sdk-ui/chatbot-resume-streams)

---

### Muhammad Abdullah

github mcp connector bhi add kr do

---

### Assistant

GitHub MCP ka plugin pehle se configured lagta hai, lekin session shuru hote waqt woh "Authorization header is badly formatted" error ke saath connect nahi hua tha. Pehle dekhta hoon ke woh kahan configured hai aur kyun fail ho raha hai.

---

### Muhammad Abdullah

اچھا یار، یہ سب کچھ تو ہو گیا۔ اب مجھے یہ بتاؤ کہ ہم اس کی security کیسے manage کر رہے ہیں۔ plan کے اندر کیا کیا ہے کہ ہم security کو کیسے manage کریں گے اور کون کون سی چیزیں اس میں consider کریں گے۔ ہم ChatGPT کا clone بنا رہے ہیں: وہ کیا چیزیں دیکھ رہے ہیں، اور ہم کیا کریں گے؟

---

### Assistant

Security ka poora plan neeche hai. Ek baat pehle: GitHub MCP abhi theek nahi hua. Wajah mil gayi hai, us ka hal aakhir mein likha hai.

## Sab se bade 5 khatre

1. **Ek user ki chat doosre ko dikh jana.** ChatGPT ke saath March 2023 mein yahi hua tha: Redis cache ke bug se logon ko doosron ke chat titles dikh gaye the.
2. **OpenAI API key leak hona.** Koi bhi aap ke paison par API chala sakta hai.
3. **Bill ka bohat badh jana.** Koi bot ya user bohat saari requests bhej kar tokens jala de.
4. **AI ke jawab ke zariye hamla (XSS).** Model ke jawab mein `<script>` ya kharab link aa jaye aur browser usay chala de.
5. **Prompt injection.** Kisi web page, file ya user ke message se model ko ulta hukm mil jaye.

## Har layer ka plan

| Layer | ChatGPT kya karta hai | Hum kya karenge | Phase |
|---|---|---|---|
| **Repo aur code** | Maloom nahi | Ho chuka: hooks, branch protection, PR review. Naya: GitHub secret scanning, Dependabot, aur CI mein `pip-audit` / `pnpm audit` | 0 |
| **Secrets** | Key sirf server par | OpenAI key sirf FastAPI ke `.env` mein, browser ko kabhi nahi. OpenAI dashboard mein monthly budget limit. Voice ke liye server chhoti umar ka token banayega (OpenAI docs ka tareeqa) | 0, 9 |
| **Login** | auth.openai.com, refresh cookie + chhota token | Better Auth: password hash, HttpOnly/Secure/SameSite cookies, Google login, login par rate limit, email verification. FastAPI har request par JWT check karega (issuer, audience, expiry) | 2 |
| **Data isolation (A ↔ B)** | 2023 ke leak ke baad cache par ownership check | Har DB query mein `user_id`, har chat aur file par owner check, cache keys mein bhi `user_id`. Automated test ke "A, B ki chat nahi khol sakta" | 2–3 |
| **Web security** | Maloom nahi | Model ka jawab untrusted maana jayega: markdown mein raw HTML aur `javascript:` links band, CSP headers. SQLAlchemy se queries safe rahengi. CORS sirf hamare frontend ke liye | 1–2 |
| **AI security** | System prompt server par, tools ke liye permission | System prompt server par, aur us mein koi secret nahi. Web page aur file ka content sirf data hai, hukm nahi. Tools (MCP) user ki ijazat se chalenge. Code sandbox bina internet ke | 7, 11 |
| **Cost aur abuse** | Kai layers par rate limits, fallback models, Sentinel + Cloudflare Turnstile + proof-of-work | Har user aur har IP par rate limit (Redis), message ki lambai ki had, `max_tokens`, har user ka roz ka token budget, ek chat mein ek waqt ek hi jawab. Deploy par Cloudflare Turnstile | 1, 5 |
| **Content safety** | Moderation layers | OpenAI Moderation API (free) har input par | 5 |
| **Files** | 20MB limit, quotas | File ki asal type check hogi (sirf extension nahi), size limit, random file names, file kabhi execute nahi hogi, aur parsing worker mein timeout ke saath hogi | 6 |
| **Privacy** | Delete ki gayi chat 30 din mein mit jaati hai, temporary chat, export | Delete karne par DB se poori tarah delete, temporary chat khud delete, logs mein poora prompt nahi, export ka option | 5, 10 |
| **Memory aur Projects** | Maloom nahi | Vector search mein hamesha `user_id` / project ka filter | 8 |
| **Share links** | Share ek frozen snapshot hota hai | Share ek copy hogi, link guess nahi ho sakega, `noindex` hoga, aur band bhi kiya ja sakega | 10 |
| **Deploy (baad mein)** | Cloudflare | HTTPS, Cloudflare, DB encryption, backups | deploy |

AI wale khatron ki checklist **OWASP Top 10 for LLM Applications** par based hogi. Is mein prompt injection, unbounded consumption aur excessive agency jaise khatre shamil hain.

## Har PR par

- PR template mein security checklist hogi: secrets, owner check, input limits.
- Login, files aur sharing wali PRs par `/security-review` bhi chalega.
- Har security rule ka test likha jayega.

## Pehle kya

Abhi app aap ke laptop par chalegi, is liye bots aur DDoS ka khatra kam hai. Pehli priority yeh chaar hain: data isolation, key ki hifazat, XSS, aur cost limits. Baqi layers (Turnstile, Cloudflare, HTTPS) internet par deploy karte waqt lagengi.

## Do kaam pending hain

1. **GitHub MCP:** plugin `GITHUB_PERSONAL_ACCESS_TOKEN` maangta hai, jo set nahi hai. Hal yeh hai ke `~/.zshrc` mein yeh line daal di jaye:
   ```sh
   export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"
   ```
   Is tarah token kisi file mein nahi likha jayega, har dafa `gh` se aayega. Phir Claude Code restart karna hoga aur main test karunga. Yeh aap ki global shell file hai, is liye ijazat chahiye. Kar dun?
2. **Docs:** `docs/adr/0001-tech-stack.md`, `docs/roadmap.md` aur `docs/security.md` (yeh poora plan) likh kar PRs khol dun?

---

### Muhammad Abdullah

ٹھیک ہے، ہاں PR open کر دو۔ اچھا، اب ہم اپنے project کا structure بناتے ہیں، folder structure بناتے ہیں کہ کہاں پر کیا کیا چیزیں ہوں گی۔ جو آپ بناؤ گے وہ مجھے show کرواؤ، پھر ہم اسے approve کرتے ہیں، اور پھر کام start کرتے ہیں۔

---

### Assistant

Pehle dono PRs khol raha hoon: ek research ki, aur ek ADR, roadmap aur security docs ki. Us ke baad folder structure ka proposal dikhaunga.

PR #1 khul gayi. Ab `main` se nayi branch bana kar ADR, roadmap aur security docs likh raha hoon.

Ab `AGENTS.md` mein stack wala hissa aur PR template mein security checklist update kar raha hoon.

Dono PRs khul gayi hain:
- **PR #1:** research report: https://github.com/MuhammadAbdullah95/chatgpt-clone/pull/1
- **PR #2:** ADR, roadmap, security plan, aur PR template mein security checklist: https://github.com/MuhammadAbdullah95/chatgpt-clone/pull/2

Ab folder structure ka proposal hai. Abhi kuch banaya nahi, pehle aap approve karein.

## Proposed folder structure

```
chatgpt-clone/
├── apps/
│   ├── web/                              # Next.js frontend (TypeScript 7)
│   │   ├── src/
│   │   │   ├── app/                      # Routes only (thin files)
│   │   │   │   ├── (auth)/login/         #   /login
│   │   │   │   ├── (auth)/signup/        #   /signup
│   │   │   │   ├── (chat)/layout.tsx     #   Sidebar + chat area, shared by all chats
│   │   │   │   ├── (chat)/page.tsx       #   /        → new chat
│   │   │   │   ├── (chat)/c/[id]/        #   /c/<id>  → existing chat
│   │   │   │   ├── api/auth/[...all]/    #   Better Auth endpoints
│   │   │   │   ├── layout.tsx            #   Root layout, theme
│   │   │   │   └── globals.css           #   Tailwind + light/dark color tokens
│   │   │   ├── features/                 # One folder per feature
│   │   │   │   ├── chat/                 #   Messages, composer, stop button, useChat setup
│   │   │   │   ├── sidebar/              #   History list, rename/delete/archive menu
│   │   │   │   └── auth/                 #   Login/signup forms
│   │   │   ├── components/ui/            # shadcn/ui building blocks (Button, Dialog…)
│   │   │   ├── lib/
│   │   │   │   ├── auth.ts               #   Better Auth server config
│   │   │   │   ├── auth-client.ts        #   Better Auth browser client
│   │   │   │   └── api/                  #   Typed FastAPI client (generated from OpenAPI)
│   │   │   └── proxy.ts                  # Sends logged-out users to /login
│   │   ├── e2e/                          # Playwright end-to-end tests
│   │   ├── .env.example
│   │   ├── next.config.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── api/                              # FastAPI backend (Python)
│       ├── src/app/
│       │   ├── main.py                   # Creates the app, adds middleware + routers
│       │   ├── core/                     # Shared plumbing (no business logic)
│       │   │   ├── config.py             #   Typed settings from .env
│       │   │   ├── db.py                 #   PostgreSQL connection + sessions
│       │   │   ├── redis.py              #   Redis connection
│       │   │   ├── auth.py               #   Verify Better Auth JWT → current user
│       │   │   └── errors.py             #   Common error responses
│       │   ├── llm/                      # Model gateway: the ONLY place that talks to OpenAI
│       │   └── modules/                  # One folder per feature
│       │       ├── health/               #   GET /health
│       │       ├── conversations/        #   Conversation + message tables (tree), sidebar list, titles
│       │       └── chat/                 #   POST /chat, resume, cancel
│       │           ├── router.py         #     HTTP endpoints
│       │           ├── service.py        #     Logic
│       │           ├── schemas.py        #     Request/response shapes (Pydantic)
│       │           └── stream.py         #     Resumable stream (Redis)
│       ├── migrations/                   # Alembic database migrations
│       ├── tests/                        # pytest, including security/ (user A ≠ user B)
│       ├── .env.example
│       └── pyproject.toml                # uv: dependencies + Ruff + pytest config
│
├── docs/                                 # adr, research, roadmap, security (already there)
├── .github/
│   ├── workflows/ci.yml                  # Lint, type-check, tests for web + api on every PR
│   ├── dependabot.yml                    # Weekly dependency updates
│   └── pull_request_template.md
├── compose.yaml                          # PostgreSQL + Redis for local dev
├── Makefile                              # make setup / dev / test / db-up / db-migrate
└── .claude/ .githooks/ AGENTS.md CLAUDE.md README.md   (already there)
```

Baad ke phases mein naye folders isi pattern par aayenge, jaise `files/`, `search/`, `memory/`, `projects/`, `voice/` aur `sharing/`. Har ek backend ke `modules/` aur frontend ke `features/` dono mein banega.

## Ek message ka safar

1. `features/chat` ka composer `POST /chat` bhejta hai.
2. `modules/chat/router.py` pehle `core/auth.py` se poochta hai ke user kaun hai, phir `service.py` ko bulata hai.
3. `service.py` dono messages DB mein save karta hai (`conversations/`) aur background task shuru kar deta hai.
4. Background task `llm/` ke zariye OpenAI se baat karta hai. Tokens `stream.py` ke zariye Redis mein jaate hain, aur aakhir mein poora jawab DB mein save hota hai.
5. SSE wapas aata hai aur `features/chat` text screen par dikhata hai.

## 4 faisle jo approve karne hain

1. **Folders feature ke hisaab se, layer ke hisaab se nahi.** Chat ka saara code ek jagah hoga. Hamare aur AI agents dono ke liye dhoondna aasaan hoga.
2. **`apps/` ke andar do alag apps, bina Turborepo ya pnpm workspaces ke.** Abhi JS app sirf ek hai, is liye in tools ki zaroorat nahi. Zaroorat padi to baad mein add kar lenge.
3. **Root par `compose.yaml` aur `Makefile`.** `make dev` jaisi ek command se sab chal jayega.
4. **Ek hi Postgres.** Login wali tables Better Auth khud banayega, aur baaqi tables hamari Alembic migrations banayengi.

## Phase 0 kaise hoga (3 PRs)

1. `chore/api-scaffold`: FastAPI, uv, `/health`, Ruff, pytest
2. `chore/web-scaffold`: Next.js, TypeScript 7, Tailwind, shadcn/ui
3. `chore/local-infra-ci`: `compose.yaml`, `Makefile`, CI, Dependabot

Chat aur conversations ke folders Phase 1 mein banenge. Phase 0 sirf dhancha khada karega.

**Aap se teen cheezein chahiye:**
1. Structure theek hai, ya kuch badalna hai?
2. PR #1 aur #2 dekh kar squash merge kar dein. Chahein to merge se pehle main AI review chala dun. Inhein pehle merge karna zaroori hai, kyun ke Phase 0 bhi `AGENTS.md` badlega aur conflict aa sakta hai.
3. GitHub MCP ki `~/.zshrc` wali line abhi pending hai. Add kar dun?

---

### Muhammad Abdullah

اچھا، ابھی دیکھو، folder structure تم نے بتایا کہ feature کے حساب سے ہوگا، good ہے، میں بھی یہی سوچ رہا تھا۔ backend پر ذرا دیکھو، مجھے وہاں لگ رہا ہے کہ ویسا نہیں ہے۔ اور جو Docker ہم بنائیں گے، Docker کو root میں رکھو، اسے بھی ایک folder میں رکھو تاکہ چیزیں manage کرنا آسان ہو کہ کس کی کون سی Docker file بن رہی ہے اور کیسے بن رہی ہے، جیسے professionally ہوتا ہے، ٹھیک ہے، تاکہ Docker کو بھی manage کرنا آسان ہو۔

---

### Assistant

Aap theek keh rahe hain. Backend poori tarah feature-based nahi tha. Is mein teen masle the:
- `llm/` features se bahar ek alag cheez ban gaya tha.
- Backend mein naam `modules/` tha aur frontend mein `features/`.
- Har feature ke andar files ka koi ek pattern nahi tha.

Teeno theek kar diye hain, aur Docker ko ek alag folder mein daal diya hai.

## Root

```
chatgpt-clone/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # FastAPI backend
├── docker/           # Everything Docker: Dockerfiles + compose
├── docs/             # adr, research, roadmap, security
├── .github/          # CI, Dependabot, PR template
├── Makefile          # One place for all commands
└── AGENTS.md, CLAUDE.md, README.md, .claude/, .githooks/
```

## Backend: ab poora feature-based

```
apps/api/
├── src/app/
│   ├── main.py                     # Creates the app, mounts every feature's router
│   ├── core/                       # Shared plumbing only, no feature logic
│   │   ├── config.py               #   Typed settings from .env
│   │   ├── db.py                   #   PostgreSQL engine, sessions, Base model
│   │   ├── redis.py                #   Redis client
│   │   ├── security.py             #   Verify Better Auth JWT → current user
│   │   ├── llm.py                  #   OpenAI client (Pydantic AI), model config, token limits
│   │   ├── errors.py               #   Error types + handlers
│   │   └── logging.py              #   Structured logs (no secrets, no full prompts)
│   └── features/                   # One folder per feature, same pattern in each
│       ├── health/
│       │   └── router.py           #   GET /health
│       ├── conversations/          # Chats, message tree, sidebar
│       │   ├── router.py           #   HTTP endpoints only
│       │   ├── schemas.py          #   Request/response shapes (Pydantic)
│       │   ├── models.py           #   DB tables: Conversation, Message (tree)
│       │   ├── repository.py       #   DB queries, always filtered by user_id
│       │   ├── service.py          #   Logic: list, rename, delete, archive, pin
│       │   └── titles.py           #   Auto title (one cheap model call)
│       └── chat/                   # Send a message, stream the reply
│           ├── router.py           #   POST /chat, GET /chat/{id}/stream, POST /chat/{id}/cancel
│           ├── schemas.py
│           ├── service.py          #   Starts a reply, allows one reply per chat at a time
│           ├── agent.py            #   Chat agent: system prompt, tools
│           ├── generation.py       #   Background task: OpenAI → Redis → DB
│           └── stream.py           #   Redis Stream buffer: write, replay, resume
├── migrations/                     # Alembic (picks up models from every feature)
├── tests/
│   ├── features/                   # Same layout as src/app/features/
│   └── security/                   # Cross-feature checks: user A can't read user B
├── .env.example
└── pyproject.toml
```

**Backend ke rules:**
1. Har feature ka pattern ek jaisa hoga: `router.py` (sirf HTTP) → `service.py` (logic) → `repository.py` (DB). `models.py` aur `schemas.py` zaroorat ke hisaab se banenge.
2. Ek feature doosre feature se sirf us ki `service.py` ke zariye baat karega. Maslan `chat` sirf `conversations/service.py` ko bulayega, us ki repository ko kabhi nahi.
3. `core/` kisi feature ko import nahi karega. Sirf features `core/` ko use karenge.
4. OpenAI client sirf `core/llm.py` banayega. Har feature apne prompts khud rakhega (jaise `chat/agent.py`).
5. Naya feature matlab naya folder: `files/`, `search/`, `memory/`, `projects/`, `voice/`, `sharing/`, `users/`.

## Frontend: wahi naam jo backend mein hain

```
apps/web/src/
├── app/                    # Routes only: (auth)/login, (chat)/, (chat)/c/[id], api/auth
├── features/
│   ├── chat/               # Messages, composer, stop, useChat setup
│   ├── conversations/      # Sidebar: history list, rename/delete/archive menu
│   └── auth/               # Login/signup forms
│       (each: components/, hooks/, api.ts, types.ts)
├── components/ui/          # shadcn/ui building blocks
├── lib/                    # auth.ts, auth-client.ts, generated API client
└── proxy.ts                # Sends logged-out users to /login
```

`chat` frontend mein bhi hai aur backend mein bhi. `conversations` bhi dono taraf hai. Is se dhoondna aasaan rahega.

## Docker: sab ek folder mein

```
docker/
├── README.md                     # Which file builds what, and the commands
├── compose.yaml                  # All services; app containers behind a profile
├── api/
│   ├── Dockerfile                # Builds apps/api: multi-stage, uv, non-root user
│   └── Dockerfile.dockerignore   # Keeps .env, caches, tests out of the image
├── web/
│   ├── Dockerfile                # Builds apps/web: multi-stage, Next.js standalone, non-root
│   └── Dockerfile.dockerignore
└── postgres/
    └── init/                     # SQL that runs on first start (e.g. extensions)
```

| Service | Kahan se aata hai | Kab chalta hai |
|---|---|---|
| postgres | `pgvector/pgvector` image (Postgres aur vector search ek saath, Phase 8 ke liye tayyar) | Hamesha |
| redis | `redis` image | Hamesha |
| api | `docker/api/Dockerfile` | `apps` profile ke saath |
| web | `docker/web/Dockerfile` | `apps` profile ke saath |

**Chalane ke do tareeqe:**
- **Roz ka development:** `make infra` sirf Postgres aur Redis Docker mein chalata hai. Phir `make dev` dono apps ko seedha laptop par chalata hai, taake code badalte hi reload ho.
- **Poori app Docker mein:** `make up` chaaron containers chala deta hai, bilkul production ki tarah.

**Docker mein security:**
- Container root user ke baghair chalenge.
- Multi-stage build hoga, taake image chhoti rahe aur us mein build tools na hon.
- Secrets image mein nahi jayenge, sirf chalte waqt `.env` se aayenge.
- Postgres aur Redis sirf aap ke laptop (`127.0.0.1`) par khulenge, network par nahi.

Deploy ke waqt `docker/compose.prod.yaml` add karenge.

## Phase 0 (3 PRs)

1. `chore/api-scaffold`: FastAPI, `core/`, `features/health`, Ruff, pytest
2. `chore/web-scaffold`: Next.js, TypeScript 7, Tailwind, shadcn/ui
3. `chore/docker-and-ci`: `docker/` folder, `Makefile`, CI, Dependabot

Yeh structure approve hai? Haan kehne par Phase 0 shuru kar dunga.

Shuru karne se pehle PR #1 aur #2 merge ho jayein to behtar hai, warna `AGENTS.md` mein conflict aa sakta hai.

---

### Muhammad Abdullah

اچھا یار، Docker میں جو ہم compose.yaml بنا رہے ہیں، اس میں ساری services ایک ہی جگہ دے رہے ہیں، تو کیا یہ اچھی چیز ہے؟ کیا manage کرنا آسان ہوگا؟ اس میں سے میں Postgres بھی ڈھونڈوں گا، Redis بھی ڈھونڈوں گا، تو اگر کوئی مسئلہ آ جاتا ہے تو کیا یہ چیزیں آسان ہوں گی؟ اس کا کوئی آسان حل ہے کہ چیزیں manage کرنا آسان ہو؟

---

### Assistant

Docker Compose ki current docs mein `include` feature check kar raha hoon. Isi se har service ki apni compose file ban sakti hai.

Haan, is ka aasaan hal hai: Docker Compose ka **`include`** feature. Har service ka apna folder hoga, aur Postgres, Redis, api ya web ki har cheez usi folder mein rahegi. Main `compose.yaml` mein sirf in files ki list hogi.

Docs se confirm kiya hai ke `include` ki gayi har file apne paths apne hi folder ke hisaab se parhti hai. Matlab `postgres/compose.yaml` mein `./init` likhenge to woh `docker/postgres/init` ko hi dhoondega. Aap ke laptop par Compose v5.1.1 hai, jo yeh feature support karta hai.

## Naya `docker/` folder

```
docker/
├── compose.yaml                 # Only a list of the services below
├── README.md                    # Service, folder, port, common problems
├── postgres/
│   ├── compose.yaml             # Postgres service, data volume, healthcheck, port
│   └── init/                    # SQL that runs on first start (extensions)
├── redis/
│   └── compose.yaml             # Redis service, healthcheck, port
├── api/
│   ├── compose.yaml             # API container (profile: apps), waits for postgres + redis
│   ├── Dockerfile
│   └── Dockerfile.dockerignore
└── web/
    ├── compose.yaml             # Web container (profile: apps), waits for api
    ├── Dockerfile
    └── Dockerfile.dockerignore
```

Main file bas itni si hogi:

```yaml
name: chatgpt-clone

include:
  - postgres/compose.yaml
  - redis/compose.yaml
  - api/compose.yaml
  - web/compose.yaml
```

**Rule seedha hai:** Postgres mein masla ho to sirf `docker/postgres/` kholein, aur Redis mein ho to `docker/redis/`. Baad mein koi nayi service aaye, jaise background worker ya file storage, to us ka bhi apna folder banega aur list mein ek line judegi.

## Masla aane par dhoondna aasaan kaise hoga

Sirf folders kaafi nahi, is liye yeh bhi hoga:

1. **Har service par healthcheck.** `make ps` se seedha pata chalega kaun si service `healthy` hai aur kaun si `unhealthy`.
2. **Saaf container names:** `chatgpt-postgres`, `chatgpt-redis`, `chatgpt-api`, `chatgpt-web`.
3. **Makefile shortcuts:**

| Command | Kaam |
|---|---|
| `make ps` | Sab services ka haal |
| `make logs s=postgres` | Sirf ek service ke logs |
| `make restart s=redis` | Sirf ek service restart |
| `make db-shell` | Database ke andar (psql) |
| `make redis-shell` | Redis ke andar (redis-cli) |

4. **`docker/README.md`:** ek table jis mein har service ka folder, port aur aam masle aur un ka hal likha hoga.

Sach yeh hai ke sirf 4 services ke liye ek hi file bhi chal jaati. Lekin service-wise folders hamare feature-based tareeqe se milte hain, aur services badhne par bhi saaf rahenge, is liye yahi behtar hai.

Yeh tabdeeli theek hai? Haan kehne par Phase 0 isi structure se shuru karunga.

---

### Muhammad Abdullah

ہاں ٹھیک ہے، اب چیزیں کچھ بہتر لگ رہی ہیں۔ تو ابھی ہم آگے کیا کریں، آگے کیا ہوگا؟ ہاں اچھا، تم بتا رہے ہو کہ Phase 0 اسی structure سے شروع کرو گے۔ ہاں ٹھیک ہے، یہ پورا structure folder کے اندر بناؤ۔

---

### Assistant

Phase 0 shuru karne se pehle dekh raha hoon ke PRs ka kya haal hai aur laptop par zaroori tools (Node, pnpm, uv, Python) maujood hain.

Docs confirm ho gayi. Ab API ki branch bana kar FastAPI project shuru kar raha hoon.

`uv init` ne `pyproject.toml` mein aap ki git config se naam aur email bhi daal diya hai. Repo public hai, is liye main woh field hata raha hoon. Saath hi `app` package ka structure bana raha hoon.

`uv` ko pehle `src/app/__init__.py` chahiye. Pehle test likh raha hoon, phir code (TDD).

Test sahi wajah se fail hua: `app.main` abhi bana nahi. Ab code likh raha hoon.

Teeno tests pass hain aur lint/format bhi saaf hai. Ab check kar raha hoon ke server asal mein chalta hai.

Server chal gaya: `/health` ne `{"status":"ok"}` diya aur `/docs` ne 200. Ab README, `.gitignore` aur `AGENTS.md` update kar raha hoon.

Server mainey khud band kiya tha, is liye background task "failed" dikha raha hai. Yeh theek hai.

Ab API ka README aur `AGENTS.md` mein structure ke rules likh raha hoon.

API ki PR #3 khul gayi. Ab web scaffold shuru kar raha hoon. Pehle dekhta hoon `create-next-app` abhi kaun se options deta hai.

Next.js 16.4.6 ban gaya, lekin TypeScript 5.9 ke saath aaya hai. Ab TypeScript 7 aur baaqi packages update kar raha hoon. Saath hi shadcn ke current options dekh raha hoon.

Docs ke mutabiq shadcn ab default mein Base UI deta hai. Hum `-b radix` lenge, kyun ke ChatGPT bhi Radix UI use karta hai.

shadcn TypeScript 7 ke saath bhi chal gaya. Ab generate hui files dekh raha hoon, taake demo wali cheezein hata kar apna saaf skeleton rakhun.

Biome ne sirf formatting theek ki, ab check saaf hai. Ab TypeScript 7 ka type check aur production build chala raha hoon.

Build pass ho gaya. TypeScript ka check sirf 279ms mein hua, yahi TS 7 ki tezi hai. Ab server chala kar dekh raha hoon ke page asal mein khulta hai.

Page sahi khul raha hai: title "ChatGPT Clone" hai aur status 200. Ab ADR mein ESLint ki jagah Biome likh raha hoon, kyun ke yeh faisla abhi badla hai.

Web server bhi mainey khud band kiya tha, is liye "failed" aaya. Ab commit karke PR khol raha hoon.

Phase 0 ki pehli do PRs tayyar hain. Teesri PR (Docker aur CI) in dono ke merge hone ke baad banegi, kyun ke us ki Dockerfiles in dono apps ko build karengi.

## Kya bana

**PR #3: FastAPI backend.** https://github.com/MuhammadAbdullah95/chatgpt-clone/pull/3
```
apps/api/
├── src/app/
│   ├── main.py                 # App + CORS + routers
│   ├── core/config.py          # Settings from .env
│   └── features/
│       ├── health/router.py    # GET /health
│       ├── conversations/      # Phase 1 (placeholder)
│       └── chat/               # Phase 1 (placeholder)
├── tests/
│   ├── features/health/        # Health test
│   └── security/test_cors.py   # Only the frontend may call the API
├── pyproject.toml, uv.lock, .env.example, README.md
```
- **Check kiya:** 3 tests pass hain aur Ruff saaf hai. Server chala kar dekha: `/health` ne `{"status":"ok"}` diya.
- Ruff mein do khaas rules on kiye hain: async code mein blocking calls pakadne wale (`ASYNC`) aur security wale (`S`).
- `AGENTS.md` mein poora structure aur feature rules likh diye hain.

**PR #4: Next.js frontend.** https://github.com/MuhammadAbdullah95/chatgpt-clone/pull/4
```
apps/web/
├── src/
│   ├── app/                    # layout.tsx, page.tsx, globals.css
│   ├── features/README.md      # Feature folder pattern
│   └── lib/utils.ts            # shadcn helper
├── biome.json, components.json, next.config.ts, tsconfig.json
├── AGENTS.md (Next.js) + CLAUDE.md, README.md
```
- **Check kiya:** Biome saaf hai, TypeScript 7.0.2 ka type check pass hai, aur build pass hai. Page khol kar dekha: status 200 aur title "ChatGPT Clone".

## Raaste mein teen faisle

1. **ESLint ki jagah Biome.** ESLint ka TypeScript parser TS 7 par nahi chalta. Biome tez hai aur formatting bhi khud karta hai. ADR mein bhi likh diya hai.
2. **System font.** Google font hataya, ChatGPT ki tarah system font rakha. Ab kuch download nahi hota.
3. **`cn` package.** shadcn ne `clsx` aur `tailwind-merge` ki jagah yeh naya package daala. Mainey check kiya: is ke maintainer khud shadcn hain, is liye rakha hai.

## Aap se kya chahiye

1. PR #3 aur #4 dekh kar squash merge kar dein. Chahein to merge se pehle main dono par `/code-review` chala dun.
2. Merge ke baad main PR 3 banaunga: `docker/` folder (har service ka apna folder), `Makefile`, aur GitHub Actions CI.
3. GitHub MCP wali `~/.zshrc` line abhi bhi pending hai. Add karni hai to bata dein.

---

### Muhammad Abdullah

اچھا یار، جو PRs ہیں، انہیں خود ہی review کر کے merge کر دو، ٹھیک ہے، اور اگلی پر کام کرو۔ اور GitHub MCP والی جو بات ہے، اسے ابھی ignore کرو۔

---

### Assistant

Theek hai, GitHub MCP abhi chhod dete hain. Pehle dono PRs ka review karta hoon, phir merge, phir agla kaam.

Bug confirm ho gaya. Ab fix kar ke dobara check kar raha hoon.

Fix kaam kar gaya: ab `typecheck` pehle Next.js ki types banata hai, phir check karta hai. Commit kar ke PR #3 ke masle theek karne ja raha hoon.

Ab PR #3 ke masle. `CORS_ORIGINS` ko comma se alag kar ke likhne ki suvidha ke liye pydantic-settings ka sahi tareeqa docs se check kar raha hoon.

Docs confirm ho gayi: `NoDecode` ke saath comma se alag ki hui list parhi ja sakti hai. Pehle naye tests likh raha hoon (TDD), phir code.

---

### Muhammad Abdullah (sent while the assistant was working)

اچھا یار، اپنی file میں save کرو، rule میں رکھو کہ جب بھی comment کرنا ہے تو اس میں صرف میرا نام آئے کہ محمد عبداللہ کی طرف سے comment ہوا، Claude کا نام نہ آئے۔ ٹھیک ہے، تو جو پہلے comments ہیں انہیں بھی ٹھیک کر دو، ان میں بھی Claude نہ آئے، اور جو آئندہ comments ہوں گے ان میں بھی Claude نہیں آنا چاہیے۔

---

### Assistant

Saare 13 tests pass hain. Ab `AGENTS.md` ki do baatein theek kar raha hoon: jo cheezein abhi bani nahi un par "planned" likhna, aur health jaise feature ke liye rule ko saaf karna.

Fixes push ho gaye. Ab PR #3 ki description se Claude ka zikr hata kar usay squash merge kar raha hoon. Merge message mein bhi Claude ka naam nahi hoga.

Ab `AGENTS.md` mein web ki commands aur Biome add kar raha hoon. Code review ne yahi do baatein kahi thin.

Ab PR #4 ki description bhi saaf kar ke merge kar raha hoon.

Commit ab sirf aap ke naam (MuhammadAbdullah95) se hai. Ab PR khol kar merge kar raha hoon, phir purani PRs #1 aur #2 ki descriptions saaf karunga.

PR #5 mein "Claude" do jagah hai. Yeh attribution nahi, sirf settings file ka zikr hai. Phir bhi aap ki hidayat ke mutabiq woh alfaaz badal raha hoon.

Saari PR descriptions saaf ho gayi hain. Ab sirf ek cheez bachi hai, aur woh aap ka faisla hai.

---

### Assistant (question)

**`main` branch ke 4 purane commit messages mein abhi bhi Claude ka naam hai: 3 mein 'Co-Authored-By: Claude' aur 1 mein 'Claude Code attribution'. Inhein theek karne ke liye `main` ki history dobara likhni hogi (force push). Hamari branch protection, git hook aur Claude ki permissions abhi isi cheez ko rokti hain. Kya karein?**
- History saaf karo (Recommended): Main 4 messages local par theek karunga aur GitHub protection thodi der ke liye hataunga. Phir force push ki ek command aap khud chalayenge (Claude ko force push ki ijazat nahi), aur us ke baad protection wapas lag jayegi. Commit IDs badal jayengi, lekin PRs #1–#5 ke links chalte rahenge. Repo naya hai aur aap akele hain, is liye abhi yeh mehfooz hai.
- Rehne do: Purani history jaisi hai waisi rahegi aur koi risk nahi hoga. Aage ke saare commits aur PRs pehle hi saaf hain.

---

### Muhammad Abdullah (answer)

Your questions have been answered: "`main` branch ke 4 purane commit messages mein abhi bhi Claude ka naam hai: 3 mein 'Co-Authored-By: Claude' aur 1 mein 'Claude Code attribution'. Inhein theek karne ke liye `main` ki history dobara likhni hogi (force push). Hamari branch protection, git hook aur Claude ki permissions abhi isi cheez ko rokti hain. Kya karein?"="Rehne do". You can now continue with these answers in mind.

---

### Assistant

Docker chal raha hai aur saari images maujood hain. Ab GitHub Actions ke latest versions aur un ke commit SHA le raha hoon. Actions ko SHA par pin karna supply-chain security ka behtar tareeqa hai.

Saari images aur Actions ke versions mil gaye. Ab nayi branch par Docker ka structure bana raha hoon.

Next.js ki nested hidayat ke mutabiq `output: "standalone"` lagane se pehle bundled docs check kar raha hoon.

Docs ne confirm kar diya: `standalone` output ke saath `.next/static` folder khud copy karna padta hai. Dockerfile yahi karti hai.

Ab Docker setup ko asal mein chala kar test kar raha hoon. Pehle `make help` aur compose config ki validation.

Web ke healthcheck mein `? 0 : 1` likha hai. YAML `: ` ko key-value samajh leta hai, is liye string ko quote karna hoga. API wali line bhi ehtiyatan quote kar raha hoon.

Config sahi hai. Har file ke paths uske apne folder se resolve hue, aur saare ports sirf `127.0.0.1` par khule. Ab `make infra` se Postgres aur Redis chala raha hoon.

Postgres 18.7 (pgvector 0.8.7 ke saath) aur Redis dono healthy hain. Ab `make up` se API aur web ki images bana kar chaaron containers chala raha hoon. Is mein kuch minute lagenge.

Python dependencies saaf hain. Web mein ek **moderate** masla mila. CI sirf high aur critical par fail hoti hai, phir bhi dekh raha hoon ke yeh kya hai.

Contents API mein `ref` ke saath masla aa raha hai. Seedha raw file parh leta hoon.

Asal masla zsh ka tha: woh `$spec` ko khud nahi todta, is liye `$2` khali reh gaya. Seedhi commands chala raha hoon.

Saare inputs confirm ho gaye. Ab CI workflow aur Dependabot config likh raha hoon.

Ab `make check` chala raha hoon. CI bhi yahi checks chalayegi.

Saare checks pass hain, aur sirf wahi files badli hain jo is kaam ki thin. Ab har file ka naam le kar stage kar raha hoon, phir commit, push aur PR.

PR #6 khul gayi. Ab CI ke teeno jobs (API, Web, Docker) ke khatam hone ka intezar kar raha hoon.

CI ke teeno jobs pehli hi dafa mein pass ho gaye: API (9s), Web (32s), Docker (46s). Ab merge se pehle PR #6 ka code review chala raha hoon.

Review background mein chal raha hai. Is dauran GitHub par security settings dekh raha hoon: secret scanning, push protection aur Dependabot alerts.

Secret scanning aur push protection pehle se on hain, kyun ke public repo par yeh default hote hain. Dependabot alerts aur security updates band hain, unhein on kar raha hoon.

Dependabot alerts aur security updates on ho gaye. "Generic secret patterns" ki API call to kaamyab hui, lekin status phir bhi `disabled` hai. Yeh feature is plan par available nahi lagta.

Ab code review ke nateeje ka intezar hai.

---

### Muhammad Abdullah

pause hte work

---

### Assistant

Theek hai, kaam yahin rok diya. Abhi koi naya qadam nahi uthaunga.

**Abhi tak kya ho chuka:**
- PRs #1–#5 merge ho chuki hain: research, ADR/roadmap/security, API, web, aur authorship ka rule.
- **PR #6** (Docker, Makefile, CI, Dependabot) khuli hai aur CI ke teeno jobs pass hain. Abhi merge nahi hui: https://github.com/MuhammadAbdullah95/chatgpt-clone/pull/6
- GitHub par Dependabot alerts aur security updates on kar diye hain. Secret scanning aur push protection pehle se on the.
- Docker containers band hain (`make down`), aur data mehfooz hai.

**Jab dobara shuru karenge:**
1. PR #6 ka code review abhi background mein chal raha hai. Us ka nateeja dekh kar jo masle milenge woh theek karunga, phir merge.
2. `main` ki branch protection mein CI checks (API, Web, Docker) ko lazmi banaunga.
3. Us ke baad Phase 1: streaming chat.

Jab kahenge, wahin se shuru kar dunga.

PR #6 ka review mukammal ho gaya hai. Aap ne kaam roka hua hai, is liye main abhi kuch theek nahi kar raha, sirf nateeja bata raha hoon.

**Review mein 6 baatein aayin:**
- **1 "important":** `pnpm audit` CI mein fail hoga. Yeh ghalat nikla. Isi PR par CI ki Web job audit samet pass ho chuki hai, aur local par bhi pnpm 9.12 ke saath audit chala tha.
- **5 chhoti baatein, jo jaaiz hain:**
  1. `make check` mein CI wale saare checks nahi hain, jaise audits aur Docker build.
  2. `main` par ek naya push pichle CI run ko cancel kar deta hai.
  3. `standalone` output ke baad `pnpm start` ka script sahi nahi raha.
  4. CI mein `pip-audit` ka version pin nahi hai.
  5. Dependabot Node aur Python ke major versions (25 aur 3.15) bhi la sakta hai.

Jab aap dobara shuru karne ko kahenge, pehle yeh 5 baatein theek karunga. Phir PR #6 merge karunga, CI checks ko branch protection mein lazmi banaunga, aur Phase 1 shuru karunga.

---

### Muhammad Abdullah

Continue

---

### Assistant

Kaam wahin se shuru kar raha hoon. Pehle PR #6 ki 5 jaaiz baatein theek karunga.

Pehla "important" point ghalat tha, kyun ke `pnpm audit` CI mein pass ho chuka hai. Shuru mein `pip-audit` ka latest version dekh raha hoon, taake usay pin kar sakun.

Ab web ka `start` script aur `AGENTS.md` mein `make check` ki tafseel theek kar raha hoon.

`make check` ab audits samet pass ho raha hai. Ab naya `pnpm start` (standalone server) chala kar dekh raha hoon ke page aur CSS dono theek aate hain.

Standalone server theek chal raha hai: page aur CSS dono 200 de rahe hain, aur koi warning nahi aayi. Ab commit karke push kar raha hoon.

Teeno CI jobs pass ho gaye, aur GitHub ne `dependabot.yml` ko bhi sahi maana. Ab PR #6 ki description mein review ka hissa jod kar merge kar raha hoon.

Merge wali command 2 minute mein mukammal nahi hui, is liye background mein chali gayi. Is ke nateeje ka intezar kar raha hoon.

GitHub Actions ka app ID `15368` hai. Dependabot ne bhi pehli dafa kaam shuru kar diya hai. Ab protection update kar raha hoon. Purani saari settings wahi rahengi, sirf teen lazmi checks judenge.

Branch protection update ho gayi. Ab `main` mein koi PR tabhi merge hogi jab us ke teeno CI checks (API, Web, Docker) pass hon aur branch `main` ke saath up to date ho. Pichli saari settings bhi waisi hi hain.

## Phase 0 mukammal

| PR | Kya |
|---|---|
| #3 | FastAPI backend (13 tests, secure defaults) |
| #4 | Next.js + TypeScript 7 + shadcn/ui + Biome |
| #5 | Authorship rule: sirf aap ka naam |
| #6 | `docker/` (har service ka apna folder), Makefile, CI, Dependabot |

GitHub par bhi kaafi kuch on hai: CI har PR par chalti hai, Dependabot hafta-war updates aur security alerts deta hai, aur secret scanning push protection ke saath chal rahi hai.

## Phase 1 ka plan: streaming chat

**Maqsad:** jawab screen par stream ho, refresh ke baad bhi chalta rahe, aur Stop button kaam kare. Login Phase 2 mein aayega, tab tak ek local "dev user" use hoga.

| PR | Kya banega |
|---|---|
| 1. `feat/db-foundation` | Postgres connection (async SQLAlchemy), Redis, Alembic migrations, aur `conversations` ki tables: Conversation, aur Message tree ki shakal mein (`parent_id`, `current_node_id`). Tests asli Postgres par chalenge, CI mein bhi |
| 2. `feat/llm-gateway` | `core/llm.py` (Pydantic AI + OpenAI), model aur limits config se, aur `chat/agent.py` mein system prompt. Tests nakli model par chalenge, is liye OpenAI ka kharcha nahi hoga |
| 3. `feat/chat-streaming-api` | `POST /chat`, background generation (OpenAI → Redis Stream → DB), resume ke liye `GET /chat/{id}/stream`, cancel, ek chat mein ek waqt ek jawab, aur phansay hue jawabon ki cleanup. Refresh aur disconnect ke tests bhi |
| 4. `feat/chat-ui` | Chat screen (`/` aur `/c/[id]`), `useChat` ke saath `resume: true`, markdown, code aur math, Stop, auto-scroll |
| 5. `test/chat-e2e` | Playwright test: message bhejo, beech mein refresh karo, jawab poora aana chahiye |

**Saath ke faisle:**
- **IDs:** UUIDv7, jo Python 3.14 mein built-in hai aur waqt ke hisaab se sort hoti hain.
- **Message content:** JSONB mein, AI SDK ke "parts" format mein, taake frontend aur backend ek hi format bolein.
- **Model:** config se aayega. Development ke liye ek sasta model rahega, aur naam PR 2 mein OpenAI ki current docs se tay karunga.

**Aap ka ek kaam (Phase 1 ke PR 2 se pehle):** OpenAI key aap ko khud daalni hogi, kyun ke agents ko `.env` likhne ki ijazat nahi hai:
```sh
make setup        # creates apps/api/.env from the example
# then open apps/api/.env and add: OPENAI_API_KEY=sk-...
```
Key chat mein paste na karein.

Plan theek hai? Haan kehne par PR 1 (`feat/db-foundation`) se shuru kar dunga.

---

### Muhammad Abdullah

اچھا ابھی ایسے کرو کہ ہماری اب تک جتنی discussion ہوئی ہے، میں نے تمہارے ساتھ جو chats کی ہیں اور تمہارے جو responses ہیں، ان سب کو as it is ایک file میں save کرو، اور GitHub پر push کر دو۔ اب میں اپنے students کے لیے English میں ایک message لکھنا چاہتا ہوں: to the point، simple، کم سے کم الفاظ میں، کہ بچو، دیکھو یہ ہو گیا، اور GitHub repository کا link share کر کے۔ اور ان کے ساتھ پورا plan، جیسے ہم نے class میں discuss کیا کہ آپ سب لوگ اس project میں contribute کریں گے۔ اسی project میں ہمارے پاس پورا plan موجود ہے کہ ہم نے کیا بنانا ہے۔ آپ لوگ اسے سمجھو گے اور implement کرو گے: اپنے اپنے features implement کرو، PRs open کرو، میں review کروں گا، merge کریں گے اور ایک product بنے گی۔ ہم ChatGPT کا clone بنا رہے ہیں، اور یہ آپ لوگوں کے لیے learning بھی ہے کہ open source projects میں کس طرح contribute کرتے ہیں۔ So it's a practice for you۔ اور اگر آپ ChatGPT میں کچھ دیکھتے ہو کہ ہمیں یہ چیز add کرنی چاہیے جو ChatGPT میں نہیں ہے، تو آپ لوگ وہ feature بنا کر اس میں upload کرو۔ جیسے ہم نے class میں پورا دیکھا کہ ہم کیسے structure کرتے ہیں، کیسے چیزوں کو دیکھتے ہیں: folder structure بنایا، غلطیوں سے سیکھا، AI کو درست کیا، چیزوں کو deeply سمجھا۔ "Why" کا element آپ نے ہمیشہ اپنے ساتھ رکھنا ہے۔ جب آپ اس میں بھی کام کرو گے تو بار بار سوال کرو: یہ کیوں، ایسے کیوں۔ تو اس طرح کا ایک message لکھو، to the point، زیادہ لمبا نہ لکھنا۔ میں نے WhatsApp پر بھیجنا ہے، تاکہ بچے سمجھ بھی لیں اور کام بھی ہو جائے۔ message simple ہو، آسان زبان میں۔
