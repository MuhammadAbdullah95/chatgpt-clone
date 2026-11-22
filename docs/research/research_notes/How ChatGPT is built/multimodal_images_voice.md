# How ChatGPT Handles Multimodal Input and Output (Images, Files, Voice)

Research date: 2026-11-22. All sources were accessed on that date. Help Center pages show only relative "updated" dates, which are converted to approximate dates below.
Confidence tags: **[Confirmed]** = OpenAI official (blog, docs, help center, release notes). **[Reported]** = credible third party (tech press, partner such as LiveKit, reverse-engineering write-ups). **[Inferred]** = my reasoning from indirect evidence.
Naming note: by late 2026 ChatGPT's model names include "GPT-6 at Instant", "GPT-6 Astra", "GPT-5.6", "GPT-5.5", and voice models "GPT-Live-1 / 1.1 / 1.1 Quip". These names are taken verbatim from the sources below. They postdate my training data, so I relied only on the sources for them.

## 1. Image understanding: what happens when a user attaches an image

### Takeaway
In ChatGPT, every model accepts images: PNG, JPEG, or non-animated GIF, up to 20 MB each, with no fixed per-message image count. The image is uploaded to OpenAI file storage first and then referenced from the chat message by a file pointer. That flow is documented only by reverse engineering; OpenAI has not published ChatGPT's internal protocol. The public API equivalent is an `input_image` content part that takes a URL, a base64 data URL, or a Files API `file_id`, plus a `detail` level. Images are billed as tokens: 32 px patches on newer models, 512 px tiles on older ones.

### Cited Findings
**ChatGPT product behaviour (as of Nov 2026)**
- **[Confirmed]** "All ChatGPT models accept image inputs." It works on web (chatgpt.com), iOS, and Android, for Free and paid plans, "subject to plan-specific usage limits." On mobile web, users can attach photos before signing in. — [OpenAI Help: Image inputs FAQ (updated ~Oct 2026)](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)
- **[Confirmed]** Users upload with the **+** icon ("Add photos & files"), by drag-and-drop into the text area, or by pasting from the clipboard. Formats are PNG, JPEG (.jpeg/.jpg), and non-animated GIF. Each image can be up to **20 MB**. There is no fixed number of images per message: it "depends on image size and accompanying text." — [Image inputs FAQ](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)
- **[Confirmed]** Images "are resized before analysis," and the model "does not process file names or metadata." Listed limitations: specialized medical images (e.g., CT scans), non-Latin scripts, rotated text, graphs with varying line styles, precise spatial localization (chess positions), panoramic/fisheye images, and approximate object counts. — [Image inputs FAQ](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)
- **[Confirmed]** Video files can be attached, including on Free plans, but analysis "may be incomplete or inaccurate," and video counts toward file-upload limits. — [Image inputs FAQ](https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq)
- **[Confirmed]** The general file-upload limit for images is also 20 MB per image. — [OpenAI Help: File Uploads FAQ (updated ~2026-11-15)](https://help.openai.com/en/articles/8555545-file-uploads-faq)
- **[Confirmed]** Recent release notes on attachments: Feb 13, 2026, up to **20 files per message** (up from 10). Feb 27, 2026, web users can edit messages that have image attachments. Jun 8, 2026, iOS can edit messages with attachments and shows image previews right after sending. Aug 21, 2026, on iOS you can press and hold + to attach recent photos. Oct 1, 2026, the iOS camera can scan multiple pages into one PDF. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

**History**
- **[Confirmed]** On Sep 25, 2023, image understanding launched in ChatGPT, powered by "multimodal GPT-3.5 and GPT-4," with a drawing tool in the mobile app for focusing on part of an image. It rolled out first to Plus and Enterprise on all platforms. — [OpenAI: ChatGPT can now see, hear, and speak](https://openai.com/index/chatgpt-can-now-see-hear-and-speak/)
- **[Confirmed]** On May 13, 2024, GPT-4o was "a single new model end-to-end across text, vision, and audio," and "GPT-4o's text and image capabilities are starting to roll out today in ChatGPT" (Free tier included). — [OpenAI: Hello GPT-4o](https://openai.com/index/hello-gpt-4o/)

**Upload flow inside ChatGPT (unofficial)**
- **[Reported]** A reverse-engineered ChatGPT wrapper describes a three-step upload. (1) `POST /backend-anon/files` registers the file and returns an `upload_url` that points to **Azure Blob Storage**. (2) The client PUTs the bytes directly to that URL. (3) `POST .../files/process_upload_stream` tells the backend to process the file. The message then references the file with a `file-service://{file_id}` pointer. This is one third-party implementation that uses the logged-out `backend-anon` path. The authenticated `backend-api` path was not independently confirmed. — [DeepWiki: realasfngl/ChatGPT, image upload & multimodal support](https://deepwiki.com/realasfngl/ChatGPT/8.4-image-upload-and-multimodal-support) (fetched via search summary; the direct fetch returned HTTP 429); [DeepWiki: OpenAI backend endpoints](https://deepwiki.com/realasfngl/ChatGPT/9-openai-backend-endpoints)
- **[Reported]** A community gist that tracks ChatGPT's internal API warns that some documented endpoints are "outdated/missing," so internal paths change over time. — [0xdevalias gist](https://gist.github.com/0xdevalias/4ac297ee3f794c17d0997b4673a2f160)

**How images are passed to models (public API reference design)**
- **[Confirmed]** There are three input methods: a fully qualified image URL, a base64 data URL (`data:image/jpeg;base64,...`), or a **file ID from the Files API** (uploaded with `purpose: "vision"`). In the Responses API, the user message `content` array mixes `input_text` and `input_image` parts. `input_image` takes `image_url` or `file_id` plus an optional `detail`. — [OpenAI API docs: Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- **[Confirmed]** `detail` options: `low`, `high`, `auto` (the default), and `original`. `original` is for large, dense, spatially sensitive, or computer-use images on models that support it. `gpt-5.1`, `gpt-4.1`, `gpt-4o`, and `gpt-4o-mini` support only low/high/auto, and `gpt-5.2` and `gpt-4.1-mini` do not support `original`. — [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- **[Confirmed]** Limits per request: up to **512 MB** total payload and up to **1,500 images**. Each image can have at most **30,000 patches** after resizing; images over that are rejected, not auto-resized. Formats are PNG, JPEG, WEBP, and non-animated GIF. — [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- **[Confirmed]** Token cost, newer models (patch-based): patches = ceil(w/32) × ceil(h/32). Some model/detail combinations have a patch budget, and larger images are scaled down to fit it. Tokens = patches × a model multiplier: 1.2 for `gpt-6-astra`, `gpt-5.5`, `gpt-5.4`, and `gpt-5.2`; 1.62 for `gpt-4.1-mini`. Example: a 1024×1024 image on `gpt-6-astra` at `detail: high` costs 1,229 tokens, and a 2048×2048 image costs 3,000 tokens (2,500-patch budget). — [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- **[Confirmed]** Token cost, older models (tile-based, 512 px): base + per-tile tokens. `gpt-4o`/`gpt-4.1` are 85 + 170 per tile, `gpt-4o-mini` is 2,833 + 5,667, and `gpt-5.1` is 70 + 140. `low` costs only the base. For `high`/`auto`, the image is fitted within 2048×2048, the shortest side is capped at 768 px, and the 512 px tiles are counted. — [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- **[Confirmed]** Vision-capable models in the doc's sizing table: `gpt-6-astra`, `gpt-5.6-sol/terra/luna`, `gpt-5.5`, `gpt-5.4` (plus mini/nano), `gpt-5.2`, `gpt-5.1`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4o`, and `gpt-4o-mini`. Deprecated models are excluded from the table: `gpt-5`, `gpt-5-mini/nano`, `o1`, `o3`, and `o4-mini`. CAPTCHA submissions are blocked. — [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)

### Inferences
- **[Inferred]** ChatGPT's flow follows the pattern "upload to blob storage via a presigned URL, then send the message with a `file_id` pointer." The reverse-engineered evidence (Azure Blob `upload_url` → `file-service://` pointer) matches the public API design, where `input_image` accepts a `file_id`. For a clone: (1) request a presigned upload URL from your backend, (2) PUT the bytes to S3/R2/Azure, (3) store `{file_id, mime, width, height, size}`, (4) put the `file_id` in the message, and (5) when you build the model request, resolve it to an OpenAI Files `file_id`, a signed URL, or base64 in an `input_image` part.
- **[Inferred]** The Help Center says images "are resized before analysis," and the API caps images by patches and tiles. Downscaling on the client before upload (for example, to roughly 2048 px on the long side) saves bandwidth and cost without losing model-visible detail, except where `original` detail is used.
- **[Inferred]** "All ChatGPT models accept image inputs" means a clone can treat vision as a default capability of every model it routes to. It needs no special "vision model" switch, as long as the backing API models are from the vision-capable list.

### Gaps
- OpenAI does not publish ChatGPT's internal upload endpoints, which `detail` level ChatGPT uses, or how many image tokens ChatGPT spends per image.
- No official per-plan limit on the number of images per day was found. The Help Center says only that limits are plan-specific.

## 2. File uploads (PDFs, docs, spreadsheets, audio): processing and limits

### Takeaway
ChatGPT takes documents (≤512 MB and ≤2M tokens per file), spreadsheets (~50 MB), presentations, and, since Oct 2026, audio (≤512 MB, paid plans only). Uploads are capped at 80 files per 3 hours (Free: 3 per day). PDFs attached directly to a chat are read for both text and embedded images. Spreadsheets and complex analysis go to a stateful Python/Jupyter sandbox ("Data Analysis") with no internet access. The public API mirrors the PDF behaviour: it sends extracted text plus page images to vision models, extracts text only from other documents, and parses spreadsheets up to the first 1,000 rows per sheet.

### Cited Findings
**ChatGPT limits (as of ~Nov 15, 2026)** — all from [OpenAI Help: File Uploads FAQ](https://help.openai.com/en/articles/8555545-file-uploads-faq) **[Confirmed]**
- Documents and presentations: **512 MB per file**. Text and document files are capped at **2 million tokens per file**; the token cap does not apply to spreadsheets.
- CSV and spreadsheets: **~50 MB**, "depending on the size of each row." Images: **20 MB**. Audio: up to **512 MB**.
- Upload rate: **80 files every 3 hours**. **Free users: 3 file uploads per day.** Limits may be lowered at peak hours, and the remaining quota is not shown in the UI.
- Storage: **25 GB per user**, **100 GB per organization** (Settings > Storage).
- Projects: Free 5 files, Go/Plus 25, Edu/Pro/Business/Enterprise 40. GPTs: up to 20 knowledge files.
- Supported types: DOCX, PDF, TXT, MD, HTML, XML, JSON, YAML, Python, RTF, ODT, EML. Spreadsheets: XLSX, XLS, CSV, TSV, ODS. Presentations: PPTX, ODP. Audio: WAV, MP3, OGG, audio-only WebM/MP4, PCM, FLAC, AAC, M4A. Google Docs must be exported first.
- PDFs attached directly to a chat: ChatGPT "can analyze text and images in PDFs, including charts and diagrams." Files saved as GPT knowledge or project files "may not include embedded images automatically."
- ChatGPT may use tools (Data Analysis) to open ZIP archives and to process long audio in sections.
- Audio transcription in chat runs on "GPT-6 at Instant," up to **6 minutes per recording** directly. Longer audio may be split up through Data Analysis on a best-effort basis. Audio uploads are not available on Free.
- Deleting a chat does not delete files saved separately in Library. Enterprise, Edu, and Healthcare files follow workspace retention policy.

**Conflict flagged:** the May 15, 2026 release note gives per-plan **Library** storage caps of Free 500 MB, Go 4 GB, Plus/Business 20 GB, and Pro 100 GB. The current FAQ says "25 GB per user." These may measure different things (Library vs. total), or the caps may have changed after May. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) vs [File Uploads FAQ](https://help.openai.com/en/articles/8555545-file-uploads-faq)

**Release-note timeline for files** — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) **[Confirmed]**
- Feb 13, 2026: 20 files per message (up from 10), plus more text and code types.
- Mar 23, 2026: File **Library** auto-saves uploads (web; recent files on mobile). May 15, 2026: Library expands to Free and Go.
- Mar 25, 2026: pastes over 5k characters become attachments (Plus/Pro/Business). Jun 22, 2026: the threshold rises to **10k characters** and extends to Free/Go. Aug 4, 2026: Enterprise/Edu get the same.
- Aug 7, 2026: saved Library files can be added to a chat without re-uploading. Aug 13 and Sep 10, 2026: Google Drive, then Box, Dropbox, and SharePoint files are browsable in Library.
- Oct 6, 2026: audio file uploads produce transcripts, summaries, and follow-up drafts.

**Data Analysis sandbox (code interpreter)**
- **[Confirmed]** ChatGPT "writes and runs Python code in a stateful Jupyter notebook environment" for some analysis tasks. The environment "cannot make external web requests or API calls," so data must be uploaded or come from a connected source. Image-based tables and scanned files may not be extracted reliably. The help article's "File limits" section defers to plan-specific upload limits. — [OpenAI Help: Data analysis with ChatGPT](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt) (read via search snippets of several cached versions; the wording differs between versions)

**Public API reference: file inputs**
- **[Confirmed]** Files are passed as `input_file` with a base64 `file_data`, an uploaded `file_id`, or an external `file_url`. Chat Completions accepts only PDFs, and only via `file_data`/`file_id`. — [OpenAI API docs: File inputs](https://developers.openai.com/api/docs/guides/pdf-files)
- **[Confirmed]** "For PDF files, the API extracts both text and page images and sends both to models that accept image inputs." Other documents (.docx, .pptx, .txt, code) are **text-extracted only**; embedded charts are lost, so OpenAI recommends converting to PDF. **Spreadsheets:** the API parses "up to the first 1,000 rows per sheet" and adds model-generated summary and header metadata. — [File inputs](https://developers.openai.com/api/docs/guides/pdf-files)
- **[Confirmed]** Each file must be under **50 MB**, with **50 MB combined** per request. The PDF `detail` setting is `auto`/`low`/`high`; for GPT-5.6+ `auto` means `high`, and for earlier models it means `low`. It affects only page images, and extracted text is always included. — [File inputs](https://developers.openai.com/api/docs/guides/pdf-files)

### Inferences
- **[Inferred]** ChatGPT appears to have three ways of handling a file. (a) **Direct context:** extracted text, plus page images for PDFs, goes into the prompt. This matches the 2M-token per-file cap and the API's text-plus-page-image PDF handling. (b) **Retrieval/search over the file** when it is too large for context, or for project/GPT knowledge files. The FAQ's note that knowledge files "may not include embedded images" suggests a separate, text-only indexing pipeline. (c) **The Python sandbox** for spreadsheets, ZIPs, and long audio. A clone can copy this: extract text (and render PDF pages to images for a vision model), inline it when it is small, chunk and embed it for retrieval when it is large, and send tabular files to a sandboxed Jupyter kernel.
- **[Inferred]** Turning long pastes into attachments (>10k characters) is a UX pattern worth copying. It keeps the composer usable and lets the backend treat the long paste through the same file pipeline.

### Gaps
- OpenAI does not officially describe ChatGPT's retrieval mechanics: chunk sizes, embedding model, when it switches from full context to search, or the internal tool names. Third-party "leaked system prompt" write-ups exist, but I did not verify them in this session.
- No exact sandbox specs (CPU, RAM, timeouts, preinstalled libraries) were found in official sources for 2026.

## 3. Image generation inside ChatGPT

### Takeaway
ChatGPT generates images inline in the conversation. It used DALL·E 3 until March 2025, then GPT-4o's native image generation from Mar 25, 2025. "ChatGPT Images" followed in Dec 2025, then Images 2.0 (gpt-image-2, Apr 21, 2026), 2.5 (Sep 8, 2026), and 2.6 (Nov 4, 2026). Generation is multi-turn: the model can use uploaded images and earlier turns as context, and outputs carry C2PA metadata. The DALL·E GPT retired on Aug 30, 2026.

### Cited Findings
- **[Confirmed]** Mar 25, 2025: OpenAI "built our most advanced image generator yet into GPT-4o." It can "build upon images and text in chat context," "analyze and learn from user-uploaded images," render text accurately, and handle "up to 10-20 different objects." Images "take longer to render, often up to one minute." All outputs carry **C2PA metadata**. DALL·E stayed accessible "through a dedicated DALL·E GPT." The rollout covered Plus, Pro, Team, and Free (Enterprise/Edu later), with API access promised "in the next few weeks." — [OpenAI: Introducing 4o Image Generation](https://openai.com/index/introducing-4o-image-generation/)
- **[Confirmed]** Dec 16, 2025: new ChatGPT Images on web and mobile, "powered by our best image generation model yet." Images are saved under "My images." — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed]** Apr 21, 2026: **ChatGPT Images 2.0** on all plans, plus "images with thinking" for paid users on Thinking/Pro models. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Reported]** Images 2.0 uses the **gpt-image-2** model: native reasoning, 2K resolution, and multi-image consistency, available in the API as `gpt-image-2`. API pricing was reported as $8.00 input / $2.00 cached input / $30.00 output (units presumably per 1M tokens; the snippet did not say). — [eWeek](https://www.eweek.com/news/openai-chatgpt-images-2-0/); [IT Brief Australia](https://itbrief.com.au/story/openai-launches-chatgpt-images-2-0-with-api-access) (search snippets only)
- **[Confirmed]** Sep 8, 2026: **Images 2.5.** It is better at multi-turn editing ("follows specific editing instructions more reliably across multiple edits") and at using uploaded reference photos. It adds **Sketch** (draw in ChatGPT as a visual guide, invoked with "@Sketch"), templates (Poster, Merch), **comments placed directly on images** for targeted edits, and prompt sharing. Latency is "up to 50%" lower than Images 2.0. API models: **GPT-Image-2.5 Flare** (the default) and **GPT-Image-2.5 Sunburst** (more precise, slower). C2PA metadata and invisible watermarking are used. ">3 billion images" are created weekly across ChatGPT and the API. — [OpenAI: Introducing ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/)
- **[Confirmed]** Jul 31, 2026: the DALL·E GPT retires on **Aug 30, 2026**. Oct 1, 2026: virtual try-on. Nov 4, 2026: **Images 2.6**, which is faster, preserves details across edits, adds GIF creation, and adds saved reference images. Sep 29, 2025: parental controls can remove image generation for teen accounts. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

### Inferences
- **[Inferred]** In the chat flow, image generation behaves like a tool the chat model calls. The model decides to generate, writes or forwards a prompt that includes conversation and uploaded-image context, and the result renders inline as an assistant message attachment that is also saved to an images library. Users iterate by replying in text or, since Sep 2026, with on-image comments and sketches. For a clone, the simplest equivalent is to expose an image-generation tool (for example, calling a GPT-Image model with the user's uploaded images as references), stream a placeholder while generation runs (which can take up to a minute), and store results as files.

### Gaps
- The exact date DALL·E 3 was integrated into ChatGPT (widely remembered as Oct 2023) was not re-verified in this session.
- OpenAI has not published the internal tool interface between the chat model and the image model in ChatGPT, or the name of the model behind Images 2.6.

## 4. Voice: dictation (speech-to-text in the composer)

### Takeaway
Dictation is the microphone in the composer. Audio goes to OpenAI's transcription models and comes back as editable text that the user can change before sending. Since Nov 18, 2026, **Live Dictation** streams text as you speak and has no 10-minute cap. A new STT model improved accuracy on Jun 26, 2026. OpenAI does not name the ChatGPT dictation model. On the API side, `gpt-transcribe` (files) and `gpt-live-transcribe` (live audio) replace Whisper and the gpt-4o-transcribe family, which shut down Feb 26, 2027.

### Cited Findings
- **[Confirmed]** "When you press the microphone icon to record an audio message, the recorded audio is sent to our models to be transcribed. The transcription is returned as text, which you can edit before sending as a user message." Dictation audio is kept as long as the chat stays in history and is deleted within 30 days of chat deletion. Consumer users who opted in may have it used for training; business users are not trained on by default. — [OpenAI Help: Voice Dictation FAQ (updated ~Oct 2026)](https://help.openai.com/en/articles/12168547-voice-dictation-faq)
- **[Confirmed]** "ChatGPT Dictation is separate" from Voice: "it records one prompt for editing before sending." — [OpenAI Help: Voice Mode FAQ (updated ~2026-11-13)](https://help.openai.com/en/articles/8400625-voice-mode-faq)
- **[Confirmed]** Dictation release notes: Jan 12, 2026, fewer empty transcriptions and better accuracy. Jun 26, 2026, "a new speech-to-text model" improves accuracy across languages and in noise. Aug 7, 2026, iOS auto-retries once on a timeout. Aug 14, 2026, Android keeps the dictation button after text or attachments are added. **Nov 18, 2026: Live Dictation shows text as you speak, and the 10-minute recording limit is removed.** — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Reported]** Live Dictation is "rolling out globally across all ChatGPT subscription tiers, including free and paid plans." — [Digital Trends](https://digitaltrends.com/computing/chatgpt-now-supports-live-dictation-openai-removes-the-10-minute-recording-limit) (search snippet)
- **[Reported]** OpenAI says "more than 150 million people use features like Voice and Dictation" (Jul 8, 2026). — [TechCrunch](https://techcrunch.com/2026/07/08/openai-releases-new-voice-models-for-more-natural-live-conversations/)
- **[Confirmed]** Sep 25, 2023: the original voice feature used **Whisper** ("our open-source speech recognition system") to transcribe speech. — [OpenAI: ChatGPT can now see, hear, and speak](https://openai.com/index/chatgpt-can-now-see-hear-and-speak/)

**Public API STT reference (Nov 2026)** — [OpenAI API docs: Speech to text](https://developers.openai.com/api/docs/guides/speech-to-text) **[Confirmed]**
- `gpt-transcribe` is "the recommended model for transcribing recorded speech in its original language." `gpt-live-transcribe` is recommended for live audio (Realtime transcription).
- **Deprecated, shutting down Feb 26, 2027:** `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize`, and the `/v1/audio/translations` endpoint (migrate to `/v1/realtime/translations` / `gpt-realtime-translate`).
- File limit is **25 MB**. Formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm.
- Streaming: `stream=true` with `gpt-transcribe` emits `transcript.text.delta` events, then `transcript.text.done` with detected languages. `gpt-transcribe` accepts `prompt`, `keywords`, and `languages`. Diarization uses `response_format: diarized_json` (speaker/start/end; up to 4 known-speaker reference clips of 2–10 s) and is not available in Realtime sessions.
- **[Confirmed]** Realtime transcription sessions can use `server_vad`, `semantic_vad`, or `null` turn detection. For `gpt-realtime-whisper` transcription sessions, VAD is not supported. — [OpenAI API reference: Realtime client events](https://developers.openai.com/api/reference/resources/realtime/client-events) (via Context7)

### Inferences
- **[Inferred]** The Nov 2026 Live Dictation change (streaming text, no length cap) suggests ChatGPT moved dictation from "record a clip, then upload it to a transcription endpoint" to a streaming transcription session, like the API's realtime transcription with `gpt-live-transcribe`. A clone can start with MediaRecorder plus a `/v1/audio/transcriptions` upload (≤25 MB) and later upgrade to a streaming Realtime transcription session over WebRTC/WebSocket.

### Gaps
- OpenAI does not say which model powers ChatGPT dictation, whether the Jun 26, 2026 "new speech-to-text model" is `gpt-transcribe` or `gpt-live-transcribe`, or which transport Live Dictation uses.

## 5. Voice conversations: Standard, Advanced, and GPT-Live ("Live")

### Takeaway
ChatGPT has had three generations of voice. (1) **Standard Voice** (Sep 2023): a cascaded pipeline of Whisper STT, then the text model, then TTS, turn by turn. (2) **Advanced Voice Mode** (GPT-4o speech-to-speech): alpha from summer 2024, all Plus/Team from Sep 24, 2024, with VAD-based turn-taking, video, and screen share. (3) **GPT-Live** (from Jul 8, 2026): a full-duplex model that listens and speaks at once, has no turn detector in the audio path, and delegates search and reasoning asynchronously to frontier models such as GPT-5.5. Advanced and Standard retire on **Dec 11, 2026**, and users move to Live automatically.

### Cited Findings
**Generation 1: Standard Voice (cascaded)**
- **[Confirmed]** Sep 25, 2023: voice launched on iOS/Android (opt-in) for Plus/Enterprise. Whisper handled STT, a new TTS model ("human-like audio from just text and a few seconds of sample speech") handled speech output, and there were 5 voices created with professional voice actors. — [OpenAI: ChatGPT can now see, hear, and speak](https://openai.com/index/chatgpt-can-now-see-hear-and-speak/)
- **[Confirmed]** OpenAI described the old Voice Mode as "a pipeline of three separate models," with average latencies of **2.8 s (GPT-3.5)** and **5.4 s (GPT-4)**. It "can't directly observe tone, multiple speakers, or background noises" and can't output "laughter, singing, or express emotion." — [OpenAI: Hello GPT-4o (May 13, 2024)](https://openai.com/index/hello-gpt-4o/)
- **[Confirmed]** Today, Standard is "a turn-by-turn Voice experience that transcribes your speech before generating a response." Standard audio "is deleted after transcription," unless the user shared it for training. — [Voice Mode FAQ](https://help.openai.com/en/articles/8400625-voice-mode-faq)

**Generation 2: Advanced Voice Mode (GPT-4o native audio)**
- **[Confirmed]** GPT-4o (May 13, 2024) was trained "end-to-end across text, vision, and audio" and can "respond to audio inputs in as little as **232 milliseconds**, with an average of **320 milliseconds**." OpenAI promised "a new version of Voice Mode with GPT-4o in alpha within ChatGPT Plus in the coming weeks." — [Hello GPT-4o](https://openai.com/index/hello-gpt-4o/)
- **[Reported]** Sep 24, 2024: Advanced Voice rolled out to all Plus and Team users over that week, with Enterprise/Edu later. It added 5 voices (Arbor, Maple, Sol, Spruce, Vale) for a total of 9, plus Custom Instructions and Memory. Daily usage caps applied, with a warning at 15 minutes left. There was no video or screen share yet. It was initially unavailable in the EU, UK, Switzerland, Iceland, Norway, and Liechtenstein. — [TechCrunch, Sep 24, 2024](https://techcrunch.com/2024/09/24/openai-rolls-out-advanced-voice-mode-with-more-voices-and-a-new-look/)
- **[Confirmed]** Sep 18, 2025: quality and latency improvements for "Advanced Voice powered by GPT-4o mini." **Nov 25, 2025: voice is integrated into the chat interface**, with spoken answers alongside streamed text and visuals; users can switch back to "Separate mode." Dec 11, 2025: voice in the macOS desktop app retires Jan 15, 2026. Feb 12, 2026: better instruction following and tool use (web search) in voice. Apr 2, 2026: voice in **Apple CarPlay**. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed]** Advanced is now "the previous real-time Voice experience" and is still required for **video and screen sharing** on iOS/Android (camera button; "Share Screen" in the ••• menu). Advanced audio and video clips are kept with the transcript for 30 days. — [Voice Mode FAQ](https://help.openai.com/en/articles/8400625-voice-mode-faq)

**Generation 3: GPT-Live (full-duplex)**
- **[Reported]** Jul 8, 2026: OpenAI released **GPT-Live-1** and **GPT-Live-1 mini**. They are "full-duplex," meaning they "can speak and listen at the same time," which enables natural interruption and live translation. GPT-Live-1 mini replaced Advanced Voice by default, and paid users get GPT-Live-1. The models hand off "search, reasoning, or agentic tasks to newer text models such as GPT-5.5 while the conversation continues," can stay silent for long periods, and can show information visually. A demo showed Hindi with a "heavy American accent." — [TechCrunch, Jul 8, 2026](https://techcrunch.com/2026/07/08/openai-releases-new-voice-models-for-more-natural-live-conversations/)
- **[Confirmed]** The Jul 8, 2026 release note says GPT-Live-1 powers Voice for paid users and GPT-Live-1 mini for Free, while video and screen share stay on Advanced. Later updates: Jul 23, voice in Work and Codex on desktop. Aug 7, background-session safeguards, plus file uploads and Projects in GPT-Live. Aug 31, Lock Screen/Dynamic Island. Sep 9, voice can call **GPT-5.6 or GPT-6 Astra** for harder questions, and separate "Voice intelligence levels" are deprecated. Sep 23, plugins in Live and voice in Work. Oct 15, **GPT-Live-1.1** and **GPT-Live-1.1 Quip** (mini) with new voices and accents. **Nov 10, 2026: Advanced and Standard retire Dec 11, 2026.** — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed]** OpenAI's engineering post on the system, "How we built a realtime system for responsive voice AI in six months" (Justin Uberti and Zahan Malkani, **Aug 3, 2026**; served at the GPT-Live URL below), says:
  - GPT-Live is the "third-generation voice system." It "removes the turn detector from the audio path," and its model "is full-duplex, which means it can listen and speak at the same time."
  - Earlier systems used turn detectors to decide when to start inference, and cascaded systems ran STT, then the LLM, then TTS in series.
  - In GPT-Live, audio streams in and out of the model continuously, while "delegation, tool use, and persistence" run on a **separate asynchronous RPC path**. A frontier model (GPT-5.5) does "Search + reason" in the background.
  - The media frontend and inference logic were rewritten in **Go**, replacing a **Python asyncio** implementation, and the new system's "p95 [matches] the previous system's p50" for frame delivery.
  - Stateful handoffs let a new model instance take over without a media gap, and context compaction runs the same way.
  - Transcript segmentation keeps backchannels ("mm hmm") from becoming separate messages.
  - The post claims "sub-second responsiveness." — [OpenAI engineering post](https://openai.com/index/continuous-voice-interaction-with-gpt-live/) (fetched URL slug "continuous-voice-interaction-with-gpt-live"; the content returned was the engineering post above, so the URL may host or redirect to it)
- **[Confirmed]** Current state (Voice Mode FAQ, ~Nov 13, 2026):
  - **Live** runs on GPT-Live-1.1 (Quip on some plans). It can use web search and memory, show widgets, and work with text and images. It "can listen and speak at the same time," so users can interrupt. It shows text while speaking. There is **no video or screen share**, and preset personalities don't apply.
  - Usage limits per rolling 24 h: Go 3 h (Quip), Plus 3 h, Pro $100 15 h, Pro $200 unlimited, Business 3 h or 15 h plus 1.25 credits/min, Enterprise usage-based $0.05/min.
  - Voices: Arbor, Breeze, Cove, Ember, Juniper, Maple, Sol, Spruce, and Vale, plus Live-only locale voices (e.g., Viola/Rio pt-BR, Aube/Rivage fr, Himari/Rindō ja).
  - Users can have one voice conversation at a time. Background conversations continue when the phone is locked. A transcript is added to the chat afterwards.
  - Live and Advanced audio clips are kept 30 days. — [Voice Mode FAQ](https://help.openai.com/en/articles/8400625-voice-mode-faq)
- **[Reported]** Reports on the Nov 10, 2026 retirement announcement say voice usage "nearly doubled" since GPT-Live and that "virtually all" voice users now use it, and that custom-GPT voice stays on Advanced until Dec 11. — [Interesting Engineering](https://interestingengineering.com/ai-robotics/chatgpt-drops-two-voice-modes-december-2026); [Open The Magazine](https://openthemagazine.com/technology/quick-take-chatgpt-is-retiring-two-voice-modes-what-changes-on-december-11-seven-things-to-know) (search snippets only; the claims are attributed to OpenAI)

### Inferences
- **[Inferred]** A clone can choose among three architectures that match ChatGPT's generations. (1) **Cascaded:** browser STT upload, then a text LLM, then TTS. This is the cheapest and simplest option, with 2–5 s latency, and works with any LLM. (2) **Speech-to-speech with VAD:** the Realtime API (`gpt-realtime-*`) over WebRTC, with server or semantic VAD and barge-in. This is AVM-like at roughly 300 ms. (3) **Full-duplex with delegation:** the GPT-Live API (`gpt-live-1.1`), where the voice model keeps talking while a backend agent runs tools. Option 2 is the realistic target for a student clone, and option 1 is a good fallback.
- **[Inferred]** Showing spoken answers in the chat with streamed text (Nov 2025 onward), plus a transcript stored in chat history, means voice sessions should write into the same conversation and message store as text chat rather than into a separate log.

### Gaps
- I did not re-verify the exact AVM alpha start date (summer 2024) or the exact date video/screen share was added to Advanced Voice (widely remembered as Dec 2024).
- I did not verify whether OpenAI announced and then reversed a Standard Voice retirement in 2025. The current FAQ shows Standard still exists until Dec 11, 2026.
- No official latency figures in milliseconds were found for GPT-Live, only "sub-second."

## 6. Real-time transport: LiveKit partnership and the public Realtime / GPT-Live API

### Takeaway
On Oct 3, 2024, LiveKit announced that ChatGPT's Advanced Voice runs on LiveKit. A LiveKit client SDK in the app streams mic audio over WebRTC through LiveKit Cloud to OpenAI's server-side voice agent, which talks to GPT-4o over a WebSocket. LiveKit released a Multimodal Agent API alongside the OpenAI Realtime API. In Jan 2026, TechCrunch still reported that "LiveKit powers OpenAI's ChatGPT voice mode." For GPT-Live (Aug 2026), OpenAI describes its own WebRTC optimizations (WARP, Instant Connect, a Go media frontend). The public APIs recommend WebRTC for clients, WebSocket for server-to-server, and SIP for phones, with ephemeral client secrets and server or semantic VAD with automatic interruption.

### Cited Findings
**LiveKit and OpenAI**
- **[Reported, partner announcement]** Oct 3, 2024 (Russ d'Sa): LiveKit and OpenAI partnered, and LiveKit released a **Multimodal Agent API** with built-in support for OpenAI's new **Realtime API**. The described ChatGPT Advanced Voice flow is: a **LiveKit client SDK in the ChatGPT app** captures speech, which streams over **LiveKit Cloud** to OpenAI's server-side voice agent. The agent passes the speech to **GPT-4o** (over a **WebSocket**, which OpenAI exposes as the Realtime API), receives streamed speech back, and sends it over LiveKit Cloud to the device. Advanced Voice responds in "~300ms." — [LiveKit blog](https://livekit.com/blog/openai-livekit-partnership-advanced-voice-realtime-api)
- **[Reported]** Rationale given for WebRTC over WebSocket to the device: WebSocket handles packet loss poorly, most loss happens between server and client device, and WebSocket gives no programmatic control over lossy WiFi or cellular, which leads to choppy or garbled audio. WebRTC was "specially designed for transferring audio with ultra-low latency between servers and clients," with built-in codecs and adaptive bitrate. — [LiveKit blog](https://livekit.com/blog/openai-livekit-partnership-advanced-voice-realtime-api)
- **[Reported]** LiveKit docs describe LiveKit as the bridge between a WebRTC frontend and the OpenAI Realtime API, which runs over WebSockets. — [LiveKit docs: OpenAI integration](https://docs.livekit.io/agents/integrations/openai)
- **[Reported]** Jan 22, 2026: LiveKit raised $100M at a $1B valuation, led by Index Ventures. "LiveKit powers OpenAI's ChatGPT voice mode." Other customers include xAI, Salesforce, Tesla, and 911 operators. — [TechCrunch](https://techcrunch.com/2026/01/22/voice-ai-engine-and-openai-partner-livekit-hits-1b-valuation/)
- **[Confirmed]** OpenAI's "GPT-Live partner integrations" page lists LiveKit (via LiveKit's OpenAI plugin) alongside Twilio, Telnyx, Bandwidth, and Daily/Pipecat as ways to build GPT-Live voice agents. — [OpenAI API docs: GPT-Live partner integrations](https://developers.openai.com/api/docs/guides/live-partner-integrations); [GPT-Live guide](https://developers.openai.com/api/docs/guides/live)

**OpenAI's own transport work for GPT-Live (Aug 3, 2026)** **[Confirmed]** — [OpenAI engineering post](https://openai.com/index/continuous-voice-interaction-with-gpt-live/)
- WebRTC is the foundation: it handles packet loss, and "if packets arrive late, WebRTC can subtly stretch audio to prevent gaps."
- **WARP** "reduces media and data startup from six network round trips to just one." It piggybacks the DTLS handshake over ICE (SPED), uses DTLS 1.3, pre-negotiates SCTP (SNAP), and pre-negotiates data channels instead of using DCEP. It is being advanced in the IETF TSVWG and supported in **libwebrtc and Pion**.
- **Instant Connect** removes the SDP exchange from the critical path, so the client can "start a session with a single UDP packet."
- The media frontend and inference logic were rewritten in Go, replacing Python asyncio.

**Public Realtime API (reference design)** **[Confirmed]**
- Current docs: "The session connects over **WebRTC in the browser** or **WebSocket on the server**." The example model is `gpt-realtime-2.1`. The server creates ephemeral credentials with `POST /v1/realtime/client_secrets`, and WebRTC sessions are established via `/v1/realtime/calls`. The GA interface uses `session.type`, `session.audio.output`, and events such as `response.output_audio.delta`. Remove the `OpenAI-Beta: realtime=v1` header. Send an `OpenAI-Safety-Identifier` header (for ephemeral tokens, on the server request that mints them). "For full-duplex conversations with a separate delegated backend, see GPT-Live." — [OpenAI API docs: Realtime](https://developers.openai.com/api/docs/guides/realtime)
- WebRTC browser flow (official sample): fetch an ephemeral key from your server, then create an `RTCPeerConnection`, add the mic track from `getUserMedia`, play the remote track in an `<audio>` element, create the data channel `"oai-events"` for JSON events, then POST the SDP offer to `https://api.openai.com/v1/realtime/calls` with `Content-Type: application/sdp` and set the returned answer. — [OpenAI API docs: Voice WebRTC](https://developers.openai.com/api/docs/guides/voice-webrtc) (via Context7)
- **Turn detection:**
  - `server_vad` detects speech by audio volume. Defaults: `threshold` 0.5, `prefix_padding_ms` 300, `silence_duration_ms` 500. `idle_timeout_ms` (5,000–30,000) auto-prompts after silence.
  - `semantic_vad` uses a turn-detection model to estimate whether the user is done, with `eagerness` low/medium/high/auto.
  - Both modes have `create_response` (default true) and `interrupt_response` (default true: "automatically interrupt (cancel) any ongoing response … when a VAD start event occurs").
  - `turn_detection: null` means the client triggers responses manually (push-to-talk). — [OpenAI API reference: client_secrets](https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create); [Realtime client events](https://developers.openai.com/api/reference/resources/realtime/client-events) (via Context7)
- **Interruption bookkeeping:** `conversation.item.truncate` (`item_id`, `content_index: 0`, `audio_end_ms`) is sent when the user interrupts. "The server will produce audio faster than realtime," so truncation syncs the server with what was actually played. It also "will delete the server-side text transcript to ensure there is not text in the context that hasn't been heard by the user." — [Realtime client events](https://developers.openai.com/api/reference/resources/realtime/client-events)
- **Public GPT-Live API:**
  - Model `gpt-live-1.1`. It is full duplex: "It can listen while speaking."
  - Delegation modes: **Responses delegation** (OpenAI runs a Responses model as the backend; your app still runs its own function tools) or **Client delegation** (any model or agent you control). The mode is fixed per session.
  - Backend work can continue after the caller interrupts.
  - Connections: WebRTC (recommended "in browser, mobile, and server applications"; audio on media tracks, JSON events on a data channel), WebSocket (one connection carries audio and events), SIP/telephony, and a server-side **"sideband"** WebSocket for monitoring and control.
  - Billing is by session duration plus backend model and tool usage. — [OpenAI API docs: GPT-Live](https://developers.openai.com/api/docs/guides/live)

### Inferences
- **[Inferred]** It is unclear whether GPT-Live in ChatGPT still routes media through LiveKit Cloud. The Aug 2026 post describes a Go media frontend that OpenAI built and WebRTC protocol work in libwebrtc and Pion. That could be OpenAI's own SFU, or work layered on LiveKit, whose SFU is also Go/Pion-based. The "Python asyncio implementation" that was replaced plausibly corresponds to the earlier agent design, possibly on LiveKit's Python Agents framework. None of this is confirmed.
- **[Inferred]** Reference design for a clone:
  - Your backend mints a short-lived Realtime client secret (the API key never reaches the browser).
  - The browser opens a WebRTC peer connection directly to OpenAI, or to LiveKit Cloud with a LiveKit agent bridging to the Realtime API over WebSocket.
  - Use `semantic_vad` with `interrupt_response: true`.
  - On user speech start, stop local playback and send `conversation.item.truncate` with the played milliseconds (mainly needed for WebSocket clients, which manage playback themselves).
  - Persist `conversation.item` transcripts to the chat's message store.

### Gaps
- No public figures on LiveKit's share of ChatGPT voice traffic, contract terms, or whether LiveKit is used for GPT-Live, Dictation, or video/screen share.
- Supported audio formats and session-length limits for the GA Realtime and GPT-Live APIs were not on the fetched pages; they are linked sub-guides I did not open.

## 7. Text-to-speech: Read Aloud and the TTS models and voices

### Takeaway
"Read Aloud" (launched Mar 4, 2024) lets users play any assistant reply in a ChatGPT voice. At launch it offered 5 voices and 37 languages with auto-detection. ChatGPT's voices (Arbor, Breeze, Cove, Ember, Juniper, Maple, Sol, Spruce, Vale) are different from the API's TTS voices (alloy … marin, cedar). On the API, `gpt-4o-mini-tts` (steerable with `instructions`) and `tts-1`/`tts-1-hd` are deprecated and shut down Jan 6, 2027, with the Realtime API's `gpt-realtime-2.1-mini` as the suggested replacement.

### Cited Findings
- **[Reported]** Mar 4, 2024: OpenAI launched **Read Aloud**. On mobile, users tap and hold a response and choose "Read Aloud"; on web, the button sits under the response. Playback can be paused or rewound. It offered **5 voices** and **37 languages** with auto-detected language, aimed at on-the-go use and accessibility. — [VentureBeat](https://venturebeat.com/ai/openai-adds-read-aloud-voiceover-to-chatgpt-allowing-it-to-speak-its-outputs); [MacRumors, Mar 5, 2024](https://macrumors.com/2024/03/05/chatgpt-read-aloud-feature-iphone-app); [TechRadar](https://techradar.com/computing/artificial-intelligence/chatgpt-takes-the-mic-as-openai-unveils-the-read-aloud-feature-for-your-listening-pleasure) (search snippets). Note: one aggregated snippet listed the voices as "Jupiter, Breeze, Ember, Cove and Sky." "Jupiter" is almost certainly a garbling of **Juniper**, which is in OpenAI's current voice list. **Sky** is not in today's list. — [Voice Mode FAQ](https://help.openai.com/en/articles/8400625-voice-mode-faq)
- **[Confirmed]** Sep 25, 2023: ChatGPT's TTS model generated "human-like audio from just text and a few seconds of sample speech," with voices made with professional voice actors (5 at launch). — [OpenAI: ChatGPT can now see, hear, and speak](https://openai.com/index/chatgpt-can-now-see-hear-and-speak/)
- **[Confirmed]** Jun 18, 2026: pronunciation guidance with audio and text for 60+ languages. Aug 31, 2026: tap to hear a word with a phonetic breakdown. — [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- **[Confirmed]** Current ChatGPT voice set: Arbor, Breeze, Cove, Ember, Juniper, Maple, Sol, Spruce, Vale, plus Live-only voices. Precise playback-speed controls aren't available in Voice. — [Voice Mode FAQ](https://help.openai.com/en/articles/8400625-voice-mode-faq)

**Public API TTS reference (Nov 2026)** — [OpenAI API docs: Text to speech](https://developers.openai.com/api/docs/guides/text-to-speech) **[Confirmed]**
- Models: `gpt-4o-mini-tts` (main), `tts-1` (lower latency), and `tts-1-hd` (higher quality). "The `tts-1`, `tts-1-hd`, and `gpt-4o-mini-tts` models are deprecated and will shut down on **January 6, 2027**." The suggested replacement is `gpt-realtime-2.1-mini` via the Realtime API, which is not supported on `/v1/audio/speech`.
- Voices: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer, verse, **marin**, **cedar**. "For best quality, we recommend using `marin` or `cedar`." `tts-1`/`tts-1-hd` support only 9 voices. The page is internally inconsistent: it says both "11 built-in voices" and "13 built-in voices." Voices are optimized for English but follow Whisper's roughly 60-language support. Realtime voices are "slightly different."
- `instructions` steers accent, emotion, intonation, speed, tone, and whispering (`gpt-4o-mini-tts`).
- Output formats: MP3 (default), Opus, AAC, FLAC, WAV, and PCM (24 kHz, 16-bit signed, little-endian, no header).
- Streaming uses chunked transfer encoding, so playback starts before the file is complete. "For the fastest response times, we recommend using `wav` or `pcm`."
- Policy requires "a clear disclosure" to end users that the voice is AI-generated. Custom voices require an approved consent recording.

### Inferences
- **[Inferred]** For a clone's "Read aloud" button, call `/v1/audio/speech` with streaming PCM or WAV and play the audio progressively (Web Audio API or MediaSource). Cache the audio per message so replays are free. Because the TTS models shut down Jan 6, 2027, a production clone should plan to migrate Read Aloud to a Realtime-based TTS path (`gpt-realtime-2.1-mini`) or a third-party TTS.

### Gaps
- OpenAI has not said which model currently produces Read Aloud audio in ChatGPT, or whether Read Aloud now uses the GPT-Live voices. No official 2026 Help Center article on Read Aloud was found in this session.
