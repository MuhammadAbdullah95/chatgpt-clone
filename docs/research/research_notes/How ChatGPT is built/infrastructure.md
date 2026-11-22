# How ChatGPT Is Built: Infrastructure and Platform Engineering (state as of 2026-11-22)

Confidence tags used on every claim: **[Confirmed]** = OpenAI said it officially (blog, status-page write-up, job posting, exec statement). **[Reported]** = credible third party (press, vendor case study, independent reverse engineering, interview). **[Inferred]** = my reasoning from indirect evidence. Dates are publication or incident dates. Note: several status-page write-ups below were read in full; a few 2026 ones were only seen via search summaries and are marked "(summary only)".

---

## 1. Cloud providers and compute: what actually serves ChatGPT?

### Takeaway
ChatGPT was born on Microsoft Azure and Azure is still a core base, but since 2025 it is contractually and operationally multi-cloud: Microsoft lost its right of first refusal (Oct 2025), OpenAI's shared Kubernetes platform behind ChatGPT now spans OCI, AWS and Azure, AWS says its deal covers ChatGPT inference, Google Cloud and CoreWeave add GPU capacity, and Cerebras (Jan 2026) is being added specifically for low-latency inference.

### Cited Findings
- **[Confirmed, 2021-01-25]** OpenAI's research Kubernetes clusters were built on Azure VM Scale Sets (VMSS); that is the only cloud identifier in the post. — [OpenAI: Scaling Kubernetes to 7,500 nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)
- **[Reported, 2024-02-20]** Evan Morikawa (led OpenAI's Applied engineering group through ChatGPT's launch) said ChatGPT ran on Microsoft Azure, with GPUs in many regions and data centers, and was "multi-region, multi-cluster, and globally distributed from day one." Hardware described: NVIDIA H100s, 8 per node, HBM, NVLink between GPUs, InfiniBand to the outside network. — [The Pragmatic Engineer: Scaling ChatGPT](https://newsletter.pragmaticengineer.com/p/scaling-chatgpt)
- **[Confirmed, 2025-01-23]** A ChatGPT incident's root cause was "a failure with Cosmos DB in ChatGPT"; "the service provider recovered the affected databases at 4:25am PT." (Cosmos DB is Azure's managed NoSQL database.) — [OpenAI Status: Increased errors for ChatGPT (Jan 23, 2025)](https://status.openai.com/incidents/01JMYB40J9DVR9D13RJN1W5SWV)
- **[Reported, Jan 2025]** Microsoft's exclusive data-center arrangement with OpenAI ended in January 2025, around the Stargate announcement (Stargate = $500B infrastructure initiative with SoftBank and Oracle). — [Reuters via The Star, 2025-07-17](https://www.thestar.com.my/tech/tech-news/2025/07/17/openai-lists-google-as-cloud-partner-amid-growing-demand-for-computing-capacity); [Reuters via The Star, 2025-06-11](https://www.thestar.com.my/tech/tech-news/2025/06/11/exclusive-openai-taps-google-in-unprecedented-cloud-deal-despite-ai-rivalry-sources-say)
- **[Reported, 2025-06-10/11]** Reuters (unnamed sources): OpenAI added Google Cloud to supply capacity "for training and running its AI models"; deal reportedly finalized in May 2025. — [Reuters via The Star](https://www.thestar.com.my/tech/tech-news/2025/06/11/exclusive-openai-taps-google-in-unprecedented-cloud-deal-despite-ai-rivalry-sources-say); [Business Today](https://www.businesstoday.in/amp/technology/news/story/openai-taps-google-cloud-to-power-chatgpt-as-demand-surges-reducing-reliance-on-microsoft-report-479956-2025-06-11)
- **[Reported, 2025-06-12]** CoreWeave capacity is resold through Google Cloud to OpenAI. — [Reuters via The Star](https://www.thestar.com.my/tech/tech-news/2025/06/12/coreweave-to-offer-compute-capacity-in-google039s-new-cloud-deal-with-openai-sources-say); [DCD](https://www.datacenterdynamics.com/en/news/coreweave-to-provide-compute-capacity-for-googles-openai-deal-report/)
- **[Reported, 2025-07-16/17]** OpenAI updated the supplier list on its website to include Google Cloud next to Microsoft, Oracle and CoreWeave; SiliconANGLE framed it as Google Cloud GPUs "for ChatGPT." — [Reuters via The Star](https://www.thestar.com.my/tech/tech-news/2025/07/17/openai-lists-google-as-cloud-partner-amid-growing-demand-for-computing-capacity); [SiliconANGLE](https://siliconangle.com/2025/07/16/openai-taps-google-cloud-access-much-needed-gpus-chatgpt/)
- **[Reported, 2025]** CoreWeave–OpenAI contracts: about $22.4B maximum value across three 2025 deals; the first was a five-year, $11.9B contract (March 2025). — [Built In: OpenAI cloud deals](https://builtin.com/articles/openai-cloud-deals); [Reuters via The Star](https://www.thestar.com.my/tech/tech-news/2025/06/12/coreweave-to-offer-compute-capacity-in-google039s-new-cloud-deal-with-openai-sources-say)
- **[Reported, Jul–Sep 2025]** Oracle: more than $300B over five years, up to 4.5 GW, mostly at Stargate sites; about 618 MW delivered at Abilene, TX. Terms are not fully disclosed by the parties. — [Fierce Network AI deals encyclopedia](https://www.fierce-network.com/cloud/fierce-networks-encyclopedia-ai-deals); [Built In](https://builtin.com/articles/openai-cloud-deals)
- **[Confirmed, 2025-10-28]** New Microsoft–OpenAI agreement: Microsoft no longer has a right of first refusal to be OpenAI's compute provider; OpenAI contracted to buy an incremental $250B of Azure services; Microsoft keeps Azure API exclusivity until AGI; non-API products may be served on any cloud provider. — [OpenAI: The next chapter of the Microsoft–OpenAI partnership](https://openai.com/index/next-chapter-of-microsoft-openai-partnership/); [Microsoft blog](https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/)
- **[Confirmed, 2025-11-03]** AWS partnership: "hundreds of thousands" of NVIDIA GB200/GB300 GPUs on Amazon EC2 UltraServers, the ability to scale to "tens of millions of CPUs," all capacity targeted for deployment by end of 2026. Amazon said the workloads include serving ChatGPT inference as well as training. — [OpenAI: AWS and OpenAI partnership](https://openai.com/index/aws-and-openai-partnership/); [About Amazon](https://www.aboutamazon.com/news/aws/aws-open-ai-workloads-compute-infrastructure)
- **[Reported, 2025-11]** The AWS deal is valued at $38B over seven years. — [DCD](https://www.datacenterdynamics.com/en/news/openai-signs-38bn-multi-year-agreement-with-aws-for-access-to-nvidia-gb200s-and-gb300s/)
- **[Reported, Feb 2026]** The AWS commitment was reportedly expanded to about $138B in total ($100B over eight years). Secondary source; not verified against a primary announcement. — [Built In](https://builtin.com/articles/openai-cloud-deals)
- **[Confirmed, 2026-01-14]** Cerebras: a multi-year deal for 750 MW of "low-latency" compute that OpenAI is integrating into its inference stack in phases, delivered from 2026 through 2028. OpenAI's Sachin Katti: "faster responses, more natural interactions and a stronger foundation to scale real-time AI to many more people." — [OpenAI: Cerebras partnership](https://openai.com/index/cerebras-partnership/); [Cerebras blog](https://cerebras.ai/blog/openai-partners-with-cerebras-to-bring-high-speed-inference-to-the-mainstream)
- **[Reported, 2026-01-14]** The Cerebras deal is reportedly worth about $10B or more. — [TechCrunch](https://techcrunch.com/2026/01/14/openai-signs-deal-reportedly-worth-10-billion-for-compute-from-cerebras/); [The Register](https://www.theregister.com/2026/01/15/openai_cerebras_ai/)
- **[Confirmed, job posting, read 2026-11]** OpenAI's Cloud Infrastructure team "builds the shared platforms behind ChatGPT and the OpenAI API." Its Kubernetes Foundations group operates a "multi-cloud compute platform that other teams build on" and builds "across OCI, AWS and Azure." The focus is "the shared CPU compute foundation" (not GPU optimization), supporting "API and chat products, data systems, observability and online serving." GCP is not named. — [OpenAI Careers: Software Engineer, Cloud Infrastructure (SF)](https://openai.com/careers/software-engineer-cloud-infrastructure-san-francisco/)

### Inferences
- **[Inferred]** The Oct 2025 terms split the estate in two. The OpenAI API is tied to Azure (Azure API exclusivity), while ChatGPT, a non-API product, may run on any cloud. This is the contractual basis for ChatGPT's multi-cloud footprint (OCI, AWS, Azure, Google, CoreWeave, Cerebras).
- **[Inferred]** The "CPU platform" (web/API front-ends, data systems, online serving glue) is a multi-cloud Kubernetes layer on OCI, AWS and Azure. Google Cloud and CoreWeave appear mainly as GPU capacity sources, since GCP is absent from the Kubernetes Foundations posting. Low-to-medium confidence.
- **[Inferred]** Cerebras is the first publicly confirmed non-NVIDIA accelerator dedicated to ChatGPT-style serving. The inference control plane therefore has to route across heterogeneous backends with different latency and cost profiles.
- **[Inferred]** Azure-managed data services (Cosmos DB) were in ChatGPT's critical path as of Jan 2025, so ChatGPT's "Azure-ness" goes beyond GPUs.

### Gaps
- No public breakdown of what share of ChatGPT inference runs on each cloud, or whether Google TPUs (versus GPUs) serve ChatGPT traffic.
- NVIDIA (10 GW LOI), AMD (6 GW) and Broadcom (custom accelerator) deals from late 2025 were not researched here. They are mainly long-horizon supply, not confirmed ChatGPT serving today.
- Delivered-versus-contracted capacity as of Nov 2026 is not public. Dollar figures for Oracle, CoreWeave and the AWS expansion are reported, not confirmed.

---

## 2. Kubernetes: from 7,500-node research clusters to "hundreds of clusters" serving ChatGPT

### Takeaway
OpenAI's famous Kubernetes scaling posts (2018: 2,500 nodes; 2021: 7,500 nodes) describe research and training clusters, not ChatGPT. ChatGPT, including model inference, also runs on Kubernetes, across "hundreds of Kubernetes clusters globally" (confirmed Dec 2024), now run as a multi-cloud platform built with Terraform-style infrastructure as code.

### Cited Findings
- **[Confirmed, 2021-01-25]** The 7,500-node post (Eric Sigler, Benjamin Chess) covers research workloads: GPT-3, CLIP, DALL·E and Scaling Laws experiments. It explicitly describes little HTTPS traffic and no A/B testing, blue/green or canary deploys. It follows an earlier 2,500-node post. — [OpenAI: Scaling Kubernetes to 7,500 nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)
- **[Confirmed, 2021-01-25]** Architecture details from the same post:
  - Large jobs run one pod per node, using all of the node's hardware (NVLink, GPUDirect). The largest jobs use MPI and restart from checkpoints.
  - API servers and etcd run outside the cluster on dedicated nodes: 5 API servers and 5 etcd nodes in the largest clusters, with up to 70 GB of heap per API server.
  - Kubernetes Events were moved to a separate etcd cluster. EndpointSlices cut Endpoints WATCH load by about 1000x (it had reached 1 GB/s or more).
  - Flannel was replaced by native pod networking using alias IPs on Azure VMSS. About 200,000 IPs can be in use at once.
  - Hub-and-spoke access: clusters cannot reach each other, to keep failures isolated.
  - Team quotas use taints (`openai.com/team=teamname:NoSchedule`) set by a "team-resource-manager", plus an admission webhook that adds tolerations.
  - Low-priority "balloon" Deployments keep cluster-autoscaler from scaling down idle nodes. The Coscheduling plugin provides gang scheduling.
  - Lessons: avoid DaemonSets that talk to the API server, and stagger node joins.
  — [OpenAI: Scaling Kubernetes to 7,500 nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)
- **[Reported, 2024-02-20]** On ChatGPT's own fleet: "Our kubernetes clusters very quickly went from being treated like pets, to more like cattle." — [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/scaling-chatgpt)
- **[Confirmed, 2024-12-11 incident]** OpenAI runs "hundreds of Kubernetes clusters globally." The control plane handles administration, while "the data plane serves workloads such as model inference." DNS-based service discovery depends on the control plane: services "don't know how to contact one another without the Kubernetes control plane." — [OpenAI Status write-up, Dec 11, 2024](https://status.openai.com/incidents/ctrsv3lwd797/write-up)
- **[Confirmed, 2025-01-23 incident]** "Web service pods crash-looping due to their health checks failing" left too few resources to serve requests. The fix was to change the web server's health-checking logic. — [OpenAI Status, Jan 23, 2025](https://status.openai.com/incidents/01JMYB40J9DVR9D13RJN1W5SWV)
- **[Confirmed, job posting, read 2026-11]** Kubernetes Foundations covers "cluster creation and lifecycle management, upgrades, patching, compliance," "safe upgrades," "capacity management, autoscaling and resource allocation, including namespace management and quotas," "multi-cluster mobility," and "Terraform or comparable tooling." — [OpenAI Careers: Cloud Infrastructure](https://openai.com/careers/software-engineer-cloud-infrastructure-san-francisco/)
- **[Confirmed, job postings, via search snippets]** Fleet Infrastructure covers GPU scheduling, quotas and automated cluster provisioning, with "experience working in public clouds (especially Azure)." Infrastructure Reliability (London) asks for Kubernetes, Terraform, and Prometheus/Grafana. — [OpenAI Careers: Fleet Infrastructure](https://openai.com/careers/software-engineer-fleet-infrastructure-san-francisco/); [OpenAI Careers: Infrastructure Reliability](https://openai.com/careers/software-engineer-infrastructure-reliability/)
- **[Reported, posting dated 2025-08-15 per aggregator]** Engineering Manager, Infrastructure (USD 325k–405k) covers multi-region Kubernetes and "Automate everything — from provisioning to upgrades to failover — using Terraform, CI/CD, and custom tooling." — [Thrive Capital job board](https://jobs.thrivecap.com/companies/openai/jobs/56626976-engineering-manager-infrastructure)

### Inferences
- **[Inferred]** The 7,500-node lessons (API-server load from per-node agents, DaemonSets hammering the API) foreshadow the Dec 2024 outage almost exactly: a per-node telemetry agent issuing expensive API calls in very large clusters. The lesson was documented in 2021 but not enforced as a pre-deploy guardrail.
- **[Inferred]** The platform is split into a CPU/K8s layer (Kubernetes Foundations: front-ends, API services, data systems) and a GPU fleet layer (Fleet Infrastructure: GPU scheduling, quotas, provisioning). ChatGPT requests cross both.
- **[Inferred]** The Dec 2024 recovery steps (scaling down clusters, firewalling admin APIs, scaling up API servers) show OpenAI controls API-server sizing directly. Whether it uses managed AKS/EKS/OKE or self-managed control planes is not public. A Chinese press headline called it "self-built K8s" ([36Kr](https://www.36kr.com/p/3083766956652936)), but I could not verify this.

### Gaps
- No public current cluster count, per-cluster node count, CNI choice, service mesh (Envoy/Istio or other) or ingress stack for ChatGPT.
- Whether DNS service discovery has since been decoupled from the control plane (a Dec 2024 action item) is not publicly confirmed.

---

## 3. Model serving and inference: how a ChatGPT request reaches a GPU

### Takeaway
OpenAI has never published an end-to-end ChatGPT serving architecture. The public evidence is an interview (2024), the GPT-5 router (2025), capacity statements, and incident write-ups. Together they show:
- Requests go to inference workloads on Kubernetes data planes spread across many clusters and regions.
- Traffic is shifted between clusters and regions on failure.
- The GPU fleet is balanced for throughput rather than placed near users.
- The binding constraints are GPU memory (KV cache) and supply, not CPU autoscaling.
- Overload is handled by rate limits and plan tiers, not by elastic scale.

### Cited Findings
- **[Reported, 2024-02-20]** Morikawa interview on the serving constraints:
  - "GPU RAM, not compute resource, is the most frequent bottleneck for LLM operations."
  - The KV cache lives in GPU RAM, and idle conversations can be evicted. A cache miss forces recomputation of the whole conversation.
  - The team's primary metrics became batch size and KV-cache utilization, because plain GPU utilization "was found to be misleading."
  - The team could not autoscale into more GPUs because none were available to buy or rent. The "We are at capacity" message meant all GPUs were in use.
  - A well-balanced GPU fleet was prioritized over placing GPUs near users, since token-streaming speed mattered more than network round-trip time.
  — [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/scaling-chatgpt)
- **[Confirmed, 2024-12-11]** During the outage, engineers began "moving traffic away from impacted clusters" at 3:27 PM PST and shifted traffic to healthy clusters where possible. ChatGPT and Sora fully recovered at 7:01 PM PST, and the API across all models at 7:38 PM. — [OpenAI Status write-up](https://status.openai.com/incidents/ctrsv3lwd797/write-up)
- **[Confirmed, 2025-03-27/28]** After native image generation launched in ChatGPT, Sam Altman wrote: "our GPUs are melting... We are going to temporarily introduce some rate limits while we work on making it more efficient." — [Fortune](https://fortune.com/2025/03/28/sam-altman-chatgpt-gpus-melting-ai-images/)
- **[Reported, 2025-03]** OpenAI limited image generation and delayed the rollout to free accounts. — [TechRadar](https://www.techradar.com/computing/artificial-intelligence/our-gpus-are-melting-openai-puts-limits-on-image-creation-and-delays-rollout-to-free-accounts)
- **[Reported, 2025-04-01]** Altman posted asking anyone with "GPU capacity in 100k chunks" to call. — [Yahoo Tech](https://tech.yahoo.com/articles/recent-openai-launches-limited-gpu-182959652.html)
- **[Confirmed, 2025-06-10 incident]** A routine host-OS update on GPU VMs restarted `systemd-networkd`, which conflicted with a networking agent on production nodes and "removed all routes" from impacted nodes.
  - Errors were about 5% at 1:45 AM PDT "while capacity is rebalanced."
  - Peak errors were about 35% for ChatGPT and about 25% for the API.
  - Recovery required large-scale re-imaging of GPU nodes plus recovery automation. The lack of "break-glass tooling" slowed it.
  - Fixes: automatic daily updates on GPU VMs were disabled.
  — [OpenAI Status write-up, Jun 10, 2025](https://status.openai.com/incidents/01JXCAW3K3JAE0EP56AEZ7CBG3/write-up)
- **[Confirmed, 2025-08-07]** GPT-5 in ChatGPT is "a unified system" with a fast model, a deeper reasoning model, and "a real-time router that quickly decides which model to use." The router decides based on conversation type, complexity, tool needs and explicit intent (e.g. "think hard about this"). It is continuously trained on real signals: users switching models, response preference rates, and measured correctness. — [OpenAI: GPT-5 System Card](https://openai.com/index/gpt-5-system-card)
- **[Reported, 2025-08]** The router malfunctioned at launch, and OpenAI reinstated earlier models for paid users. — [DeepLearning.AI The Batch](https://www.deeplearning.ai/the-batch/openais-new-model-hits-turbulence-with-cost-performance-and-api-complaints); [Fortune](https://fortune.com/2025/08/12/openai-gpt-5-model-router-backlash-ai-future/)
- **[Reported, opinion piece]** GPT-5 in the API is not routed, so the router appears to be ChatGPT-only. — [Where's Your Ed At](https://wheresyoured.at/how-does-gpt-5-work)
- **[Confirmed, 2025-11-03]** AWS capacity includes serving ChatGPT inference. — [About Amazon](https://www.aboutamazon.com/news/aws/aws-open-ai-workloads-compute-infrastructure)
- **[Confirmed, 2026-01-14]** Cerebras capacity is being integrated "into our inference stack in phases" for low-latency responses. — [OpenAI: Cerebras partnership](https://openai.com/index/cerebras-partnership/)
- **[Confirmed, 2026-02-03 incident]** During a feature-gate failure, "Free and Go tiers were hit hardest at peak." — [OpenAI Status write-up, Feb 3, 2026](https://status.openai.com/incidents/01KGJK9Q6PDB3C3VX6MPCY6106/write-up)
- **[Confirmed, 2026-07-19 incident, summary only]** Cloud maintenance cut capacity for an internal service in one region, so ChatGPT could not load conversations. Engineers rerouted traffic away from that region. — [OpenAI Status write-up, Jul 19, 2026](https://status.openai.com/incidents/01KXXDNEAKEPRGFM661SBJJAM6/write-up)

### Inferences
- **[Inferred]** Plausible request path, assembled from the evidence above:
  1. Browser or app.
  2. Cloudflare edge (web only; see section 4).
  3. OpenAI front-end and API services on the CPU Kubernetes platform: auth, conversation state, feature gates, rate limits.
  4. Product-level model routing (GPT-5 router, plan entitlements).
  5. Region or cluster selection with failover (traffic shifting is confirmed in 2024 and 2026).
  6. Inference replicas on GPU nodes in a Kubernetes data plane, using continuous batching and KV-cache management.
  7. Tokens streamed back.

  None of these stages beyond the ones marked confirmed above has been described end to end by OpenAI.
- **[Inferred]** "At capacity" has shifted from a hard global gate (2022–23) to softer controls: per-plan message and image caps, temporary rate limits during launches (Mar 2025), tier-differentiated degradation (Free/Go hit hardest, Feb 2026), and model-routing downshifts. This is classic admission control under a fixed GPU supply.
- **[Inferred]** KV-cache economics (recomputing a conversation on a cache miss) strongly suggest conversation- or prefix-affinity routing to replicas. OpenAI has not described its ChatGPT routing policy.
- **[Inferred]** Inference runs on Kubernetes data planes, but serving depends on non-GPU control-path services (DNS service discovery, auth, config/feature gates, conversation storage). Most major ChatGPT outages since 2024 came from those dependencies, not from model servers.

### Gaps
- No official detail on the inference engine (in-house versus vLLM or TensorRT-LLM), the scheduler or queueing design, the load balancer or L7 proxy, the streaming transport, or how requests are spread across clouds or accelerator types.
- No official current statement of what triggers ChatGPT "at capacity" or "high demand" messages in 2026.

---

## 4. Networking, CDN and bot protection

### Takeaway
chatgpt.com (web) is fronted by Cloudflare. This is near-certain from public evidence: the Nov 18, 2025 Cloudflare outage took down ChatGPT web, and users saw "Please unblock challenges.cloudflare.com." OpenAI's own write-up only names "an upstream third-party networking provider." Cloudflare Turnstile reportedly runs on every ChatGPT message, as one layer of an OpenAI "Sentinel" anti-abuse system. OpenAI has never officially described its CDN or bot stack.

### Cited Findings
- **[Confirmed, 2025-11-18, OpenAI]**
  - The root cause was "a faulty configuration rollout by an upstream third-party networking provider."
  - Users saw HTTP 403 or 504 errors on ChatGPT Web, platform.openai.com, sora.com and openai.com from about 3:30 AM PST.
  - Recovery began about 6:40 AM PST, when the provider rolled back.
  - The iOS and Android apps, API traffic and backend services were not affected.
  - Fix: OpenAI is "pursuing measures to improve the resilience of the authentication system."
  - The incident page listed the ChatGPT and API "Login" components and was labeled "Full outage."
  — [OpenAI Status write-up, Nov 18, 2025](https://status.openai.com/incidents/01KABE2437NJYKBFHT22SD3H92/write-up); [Incident page](https://status.openai.com/incidents/01KABE2437NJYKBFHT22SD3H92)
- **[Confirmed, 2025-11-18, Cloudflare]** Cloudflare's outage began about 11:20 UTC (3:20 AM PST). A ClickHouse permissions change made the Bot Management "feature file" double in size. That crashed Cloudflare's core proxies, and full restoration came at 17:06 UTC. — [Cloudflare blog: 18 November 2025 outage](https://blog.cloudflare.com/18-november-2025-outage/)
- **[Reported, 2025-11-18]** The press widely reported ChatGPT down because of the Cloudflare outage, with users seeing "Please unblock challenges.cloudflare.com to proceed." — [Fox Business](https://www.foxbusiness.com/technology/cloudflare-chatgpt-x-among-sites-affected-global-network-issues); [PCWorld](https://www.pcworld.com/article/2976097/worldwide-cloudflare-outage-disrupts-x-chatgpt-paypal-uber-and-other-sites.html); [Free Press Journal](https://www.freepressjournal.in/tech/chatgpt-down-for-several-users-due-to-cloudflare-outage)
- **[Reported, 2026-03-29 original; GIGAZINE 2026-05-02]** Independent reverse engineering (Buchodi, "ChatGPT Won't Let You Type Until Cloudflare Reads Your React State") found that:
  - every ChatGPT message triggers a Cloudflare Turnstile program in the browser;
  - it checks 55 properties across three layers: browser (WebGL, screen, fonts, DOM, storage), Cloudflare edge headers, and whether the ChatGPT React app is fully rendered and hydrated;
  - Turnstile is one of three challenges in an OpenAI "Sentinel" system. The other two are a "Signal Orchestrator" (behavioral biometrics such as keystroke timing and mouse speed, via `window.__oai_so_*`) and a SHA-256 Proof-of-Work, which "may not be a primary defense" (72% solved in under 5 ms);
  - the sample was 377 requests from 32 users.

  Neither OpenAI nor Cloudflare responded. — [GIGAZINE](https://gigazine.net/gsc_news/en/20260502-chatgpt-cloudflare/); [Penligent analysis](https://www.penligent.ai/hackinglabs/chatgpt-and-cloudflare-turnstile-what-the-react-state-analysis-actually-shows/)
- **[Confirmed via secondary quote]** OpenAI's Help Center says ChatGPT uses CAPTCHAs to reduce bot activity and spam on web and mobile, and mentions Cloudflare verification loops. I did not read the Help Center page directly. — [Penligent, citing OpenAI Help Center](https://www.penligent.ai/hackinglabs/chatgpt-and-cloudflare-turnstile-what-the-react-state-analysis-actually-shows/)
- **[Confirmed, OpenAI Help Center]** The reverse direction: ChatGPT's agent cloud browser signs its outbound requests with Web Bot Auth. Cloudflare lists it as a signed agent (bot tag `chatgpt-agent`, detection ID 129220581). The article also covers allowlisting on Akamai and HUMAN. — [OpenAI Help: ChatGPT agent cloud browser allowlisting](https://help.openai.com/articles/11845367)
- **[Reported, 2025-12-02]** A ChatGPT outage for some users was attributed by OpenAI to a routing misconfiguration. — [CNBC](https://www.cnbc.com/2025/12/02/chatgpt-down-outage-open-ai-chatbot.html)
- **[Confirmed, 2026-09-29 incident]** A feature rollout "exhausted shared network connection capacity, preventing otherwise healthy services from reliably communicating." Remediation includes expanding network capacity. — [OpenAI Status write-up, Sep 29, 2026](https://status.openai.com/incidents/01M3Q4RK1SM4EMK445GGPG7C0N/write-up)

### Inferences
- **[Inferred, high confidence]** The unnamed Nov 18, 2025 "third-party networking provider" is Cloudflare. The timing matches (Cloudflare 11:20 UTC, OpenAI about 3:30 AM PST), challenges.cloudflare.com errors appeared on ChatGPT, and the failing component was Cloudflare's bot-management module.
- **[Inferred]** Web (chatgpt.com) and native apps take different edge paths: the apps and the API stayed up on Nov 18. Cloudflare's proxy and bot management sit in front of the web app and its auth/login flow, so they are a single point of failure for web login.
- **[Inferred]** Bot defense is layered: Cloudflare edge bot management, then a per-message Turnstile token, then OpenAI's own Sentinel signals (behavioral and proof-of-work), then backend rate limits. The per-message check targets scripted, free-tier scraping of a GPU-expensive endpoint.

### Gaps
- No official OpenAI–Cloudflare case study or statement. Not confirmed whether api.openai.com also sits behind Cloudflare, or which DNS and CDN serve static assets.
- I found no reliable 2025–2026 source on other bot vendors (e.g. Arkose Labs) at ChatGPT login or signup.
- I did not research whether the Dec 5, 2025 Cloudflare incident affected ChatGPT.

---

## 5. Feature flags and experimentation: Statsig

### Takeaway
OpenAI was a Statsig customer before it announced the acquisition on Sep 2, 2025 (reported $1.1B, all-stock). Statsig's founder became CTO of Applications, owning ChatGPT and Codex engineering including infrastructure. Status write-ups through 2026 show "feature gates" and feature rollouts are both a central release mechanism and a recurring source of outages, with gates also used as kill switches.

### Cited Findings
- **[Confirmed, 2025-09-02]**
  - OpenAI announced it is acquiring Statsig, "an experimentation platform for A/B testing, feature flagging, and real-time decisioning."
  - The platform "has already played a central role in how we ship and learn quickly," and OpenAI was a Statsig customer.
  - Vijaye Raji (Statsig founder) became CTO of Applications, reporting to Fidji Simo. He heads "product engineering for ChatGPT and Codex," with responsibilities spanning "core systems and product lines including infrastructure and Integrity."
  - Statsig continues to operate independently from Seattle, and OpenAI takes "a measured approach to any future integration."
  - Closing was subject to regulatory approval.
  — [OpenAI announcement](https://openai.com/index/vijaye-raji-to-become-cto-of-applications-with-acquisition-of-statsig/)
- **[Reported, 2025-09-02]** Price about $1.1B in an all-stock deal. Srinivas Narayanan moved to CTO of B2B Applications. — [TechCrunch](https://techcrunch.com/2025/09/02/openai-acquires-product-testing-startup-statsig-and-shakes-up-its-leadership-team/); [TechRepublic](https://www.techrepublic.com/article/news-openai-statsig-acquisition/)
- **[Reported, 2025-09]** About 150 Statsig employees were to join OpenAI. — [Built In](https://builtin.com/articles/openai-acquires-statsig-hires-cto-applications-20250903)
- **[Confirmed, 2026-02-03 incident]**
  - The rollout "introduced a new caching path for feature gate and configuration evaluation in production," which "introduced an unexpected data type in a critical execution path." Staging missed it.
  - Impact: ChatGPT conversations on all plans (Free and Go hit hardest), plus login and account creation.
  - Timeline: started 12:12 PM PST; recovery began at 1:01 PM after the responsible feature gate was disabled; full recovery at 3:05 PM after delayed config propagation in one region.
  - "Elevated login failures led to increased retry behavior from clients," which amplified load.
  - Planned fixes: stronger validation for configuration and feature-flag APIs, production rollout safeguards, config-health alerting, circuit breakers against retry amplification, and an internal rollout playbook for "high-blast-radius systems."
  — [OpenAI Status write-up, Feb 3, 2026](https://status.openai.com/incidents/01KGJK9Q6PDB3C3VX6MPCY6106/write-up)
- **[Confirmed, 2026-09-29 incident]** A feature rollout made routine settings requests trigger repeated background checks. Most customer impact was mitigated at 11:00 AM PDT "after engineers disable the rollout." — [OpenAI Status write-up, Sep 29, 2026](https://status.openai.com/incidents/01M3Q4RK1SM4EMK445GGPG7C0N/write-up)
- **[Confirmed, 2026-07-25 incident]** A production configuration update contained routing changes incompatible with the deployed version of an internal auth-supporting service. "A separate undetected bug in the deployment system" failed to block it, so an automated redeploy re-applied the bad config and caused a second disruption. — [OpenAI Status write-up, Jul 25, 2026](https://status.openai.com/incidents/01KYC921K145JTR1JK7DYKGWH1/write-up)

### Inferences
- **[Inferred]** "Feature gate" is Statsig's product term for a boolean flag. Its use in the Feb 2026 write-up suggests ChatGPT's flagging is built on Statsig or derived from it, but OpenAI has not said so. Medium confidence.
- **[Inferred]** ChatGPT runs flags on the server side, in the request's critical path (gate and config evaluation on every request, cached). A new caching path there could break conversations and login globally, which makes the flag system itself a tier-0 dependency.
- **[Inferred]** Since Dec 2024, OpenAI's stated release discipline has converged on: phased rollouts that also watch cluster and control-plane health, feature gates as kill switches, config validation against deployed versions, and circuit breakers for client retries.

### Gaps
- No public date for the closing of the Statsig deal, and no detail on how far Statsig has been integrated into OpenAI's internal stack by Nov 2026.
- No official description of how ChatGPT runs percentage rollouts or A/B tests (e.g. model variants, UI experiments) on Statsig. That would require logged-in traffic inspection, which was out of scope.

---

## 6. Observability, incidents and what postmortems reveal about the architecture

### Takeaway
OpenAI's public observability stack has moved from Prometheus/Grafana on research clusters (2021) to a petabyte-per-day ClickHouse logging platform fed by Fluent Bit (2025). Its status-page write-ups (Dec 2024 through Sep 2026) repeatedly show that ChatGPT's largest outages come from control-plane and shared dependencies, not from GPUs failing:
- Kubernetes API/DNS
- host OS networking
- the CDN
- auth
- feature gates and config
- shared network connections and the database

### Cited Findings
- **[Confirmed, 2021-01-25]** Research-cluster monitoring used:
  - Prometheus, Grafana and kube-prometheus;
  - dcgm-exporter (`DCGM_FI_DEV_XID_ERRORS`) and NVML for GPU health;
  - iptables-exporter for per-namespace network accounting.

  Healthchecks cordon bad nodes automatically, and "preflight" GPU tests run at node boot. OpenAI patched Prometheus for query timeouts and was moving to "a different Prometheus-compatible storage and query engine." — [OpenAI: Scaling Kubernetes to 7,500 nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)
- **[Reported, 2025-06-30, vendor case study with OpenAI speakers]**
  - OpenAI ingests petabytes of logs per day. Logs flow from Fluent Bit agents into a ClickHouse cluster of 90 shards with 2 replicas each.
  - Storage is tiered: about 80% of queries touch only the last two days of data, and older data goes to blob storage.
  - The Mar 2025 GPT-4o image-generation launch spiked logging CPU by 50%. OpenAI responded with a query-dedicated replica and aggressive sampling.
  - Reasons for choosing ClickHouse: open source (no lock-in), horizontal scale, and SQL usable by humans and AI agents.
  - Speakers: Akshay Nanavati and Poom Chiarawongse (OpenAI).
  — [ClickHouse blog](https://clickhouse.com/blog/why-openai-chose-clickhouse-for-petabyte-scale-observability); [ClickHouse video](https://clickhouse.com/videos/openai)
- **[Confirmed, job posting]** Infrastructure Reliability roles ask for Prometheus and Grafana. — [OpenAI Careers](https://openai.com/careers/software-engineer-infrastructure-reliability/)
- **[Confirmed]** Notable ChatGPT incidents with official root causes. Times are as stated in the write-ups. Database issues are noted only where they appear in an incident.

| Date | Official root cause (summary) | Architectural signal | Source |
|---|---|---|---|
| 2023-03-20 | ChatGPT taken offline after a bug exposed other users' chat titles; OpenAI published "here's what happened" | Early caching-layer bug; first public ChatGPT postmortem | [HN thread on OpenAI's write-up](https://news.ycombinator.com/item?id=35291112) |
| 2024-12-11 (3:16–7:38 PM PST) | New telemetry service (Kubernetes control-plane metrics) made "every node in each cluster" run expensive K8s API operations. API servers fell over, and DNS service discovery failed once node DNS caches expired (about 20 min). Fix needed control-plane access, so workstreams scaled down clusters, blocked admin API access and scaled up API servers. Staging was too small to show it. | Hundreds of clusters; inference in the data plane; DNS coupled to the control plane. Action items: phased rollouts watching the control plane, fault injection, break-glass API access, decoupling DNS, startup rate limiters, whole-cluster replacement drills | [Write-up](https://status.openai.com/incidents/ctrsv3lwd797/write-up); [TechCrunch](https://techcrunch.com/2024/12/13/openai-blames-its-massive-chatgpt-outage-on-a-new-telemetry-service) |
| 2025-01-23 | Cosmos DB failure in ChatGPT, then web pods crash-looping on failing health checks | Azure-managed DB in the critical path; health-check design matters | [Status](https://status.openai.com/incidents/01JMYB40J9DVR9D13RJN1W5SWV) |
| 2025-03 (image-gen launch) | Demand overload: "GPUs are melting," temporary rate limits | Fixed GPU supply → rate limits; observability load spike | [Fortune](https://fortune.com/2025/03/28/sam-altman-chatgpt-gpus-melting-ai-images/) |
| 2025-06-09/10 | Daily host-OS update restarted systemd-networkd, which conflicted with a networking agent and wiped routes on GPU VMs. ChatGPT peak about 35% errors; full restore 3:00 PM PDT. | GPU fleet on cloud VMs; re-imaging as the recovery path; lack of break-glass tooling | [Write-up](https://status.openai.com/incidents/01JXCAW3K3JAE0EP56AEZ7CBG3/write-up) |
| 2025-11-18 | Faulty config rollout at an upstream networking provider (Cloudflare, inferred). Web 403/504; apps and API fine. | CDN/bot layer is a web-only single point of failure; auth resilience work | [Write-up](https://status.openai.com/incidents/01KABE2437NJYKBFHT22SD3H92/write-up) |
| 2025-12-02 | Routing misconfiguration (Reported) | Routing config as a failure mode | [CNBC](https://www.cnbc.com/2025/12/02/chatgpt-down-outage-open-ai-chatbot.html) |
| 2026-02-03 | New feature-gate/config caching path, an unexpected data type, then client retry amplification | Flags in the critical path; need for circuit breakers | [Write-up](https://status.openai.com/incidents/01KGJK9Q6PDB3C3VX6MPCY6106/write-up) |
| 2026-02-04 | A database read replica taken offline for maintenance caused 403 errors (summary only) | DB replica topology in the auth/read path | [Write-up](https://status.openai.com/incidents/01KGMVV926ZSCD1MSDBS07AWYA/write-up) |
| 2026-02-12 | A deployment removed a routing configuration resource (summary only) | Routing config managed as deployable resources | [Write-up](https://status.openai.com/incidents/01KH9WCWZ41K9ST9FGB1V15DFC/write-up) |
| 2026-07-19 | Cloud maintenance cut capacity for an internal service in one region; traffic rerouted away (summary only) | Regional failover; dependence on cloud provider maintenance | [Write-up](https://status.openai.com/incidents/01KXXDNEAKEPRGFM661SBJJAM6/write-up) |
| 2026-07-25 | Config incompatible with the deployed auth-supporting service version, plus a deploy-system bug that re-applied it. Two disruptions (1:59–2:50 and 4:24–4:58 AM PDT) hit ChatGPT, the API Platform and Codex. | Config/version skew; deploy blocks must actually block | [Write-up](https://status.openai.com/incidents/01KYC921K145JTR1JK7DYKGWH1/write-up) |
| 2026-09-02 | A config update to enable one service removed access needed by existing Work Mode services (summary only) | Permission and config coupling between services | [Write-up](https://status.openai.com/incidents/avwnvk1f/write-up) |
| 2026-09-29 | A feature rollout caused repeated background checks and retries, which exhausted shared network connection capacity across ChatGPT, Codex and the API (incl. Agents API). Mitigation: disable the rollout, fix expensive DB queries, add DB cache capacity, route around unhealthy infrastructure. | Shared connection pools and DB as blast-radius amplifiers | [Write-up](https://status.openai.com/incidents/01M3Q4RK1SM4EMK445GGPG7C0N/write-up) |

- **[Reported, low-credibility source, 2026-10]** A third-party blog counted 14 OpenAI status-page incidents between Oct 5 and Oct 7, 2026. — [chatgptdisaster.com](https://chatgptdisaster.com/openai-status-page-fourteen-incidents-three-days-chatgpt-codex-desktop-app-october-2026.html)
- **Source conflict:** The Dec 11, 2024 write-up's own timeline lists the change as "applied to all clusters" from 2:51 to 3:20 PM while also saying the service was "deployed" at 3:12 PM. Secondary sources differ on exact times. Treat 3:16–7:38 PM PST as the authoritative impact window. — [Write-up](https://status.openai.com/incidents/ctrsv3lwd797/write-up)

### Inferences
- **[Inferred]** The failure pattern 2024–2026 is dominated by change management (deploys, config, flags, OS updates) plus amplification (DNS cache expiry, client retries, shared connection exhaustion). GPU or model-server faults are rarely the root cause. Change management is OpenAI's main reliability lever, as stated in the repeated action items on phased rollouts, validation, break-glass access and circuit breakers.
- **[Inferred]** Auth and login appear in at least four of these incidents (Nov 2025, Feb 3 2026, Feb 4 2026, Jul 25 2026). Authentication is ChatGPT's highest-blast-radius non-GPU dependency.
- **[Inferred]** Observability at OpenAI's scale is a capacity problem in itself: the 2024 outage was caused by a telemetry agent, and the 2025 image launch spiked log-pipeline CPU. Telemetry needs the same staged rollout and budget limits as product code.

### Gaps
- I found no official OpenAI post on its metrics, tracing or alerting stack after 2021 (e.g. whether it uses OpenTelemetry, Datadog, or an in-house Prometheus-compatible engine for ChatGPT). The 2021 post names the Datadog Cluster Agent only as an example caching pattern.
- I did not research a Dec 26, 2024 incident (reportedly cloud-provider power related) or other early-2025 incidents beyond Jan 23.
- The Feb 4, Feb 12, Jul 19 and Sep 2, 2026 write-ups were seen only via search summaries.

---

## 7. What a much smaller ChatGPT clone actually needs

### Takeaway
Almost everything that makes ChatGPT's infrastructure hard comes from owning GPU inference at the scale of hundreds of millions of users: KV-cache management, a global GPU fleet, multi-cloud capacity contracts, and hundreds of Kubernetes clusters. A clone that calls a hosted model API skips all of that. What still applies at small scale is the control-path discipline that OpenAI's postmortems keep returning to: an edge and bot layer, auth, rate limits, feature flags with kill switches, staged config rollouts, retry and circuit-breaker hygiene, and enough observability to see it.

### Cited Findings
- **[Reported, 2024]** GPU memory and supply, not CPU autoscaling, are what bind an LLM chat service that hosts its own models. — [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/scaling-chatgpt)
- **[Confirmed, 2024-12]** Coupling service discovery (DNS) to a shared control plane turned a telemetry deploy into a total outage. — [OpenAI Status write-up](https://status.openai.com/incidents/ctrsv3lwd797/write-up)
- **[Confirmed, 2026-02]** Client retry amplification extended an outage, and OpenAI planned circuit breakers. — [OpenAI Status write-up](https://status.openai.com/incidents/01KGJK9Q6PDB3C3VX6MPCY6106/write-up)
- **[Confirmed, 2025-11]** A CDN/bot-layer config rollout at a third party took down web login, while the apps and API stayed up. — [OpenAI Status write-up](https://status.openai.com/incidents/01KABE2437NJYKBFHT22SD3H92/write-up)
- **[Confirmed, 2025-09]** OpenAI treats experimentation and feature flagging as core enough to acquire Statsig. — [OpenAI announcement](https://openai.com/index/vijaye-raji-to-become-cto-of-applications-with-acquisition-of-statsig/)

### Inferences
Each of these maps an OpenAI-scale concern to its small-clone equivalent. All are **[Inferred]**.

- **Cloud and compute.**
  - At OpenAI scale: multi-cloud GPU contracts measured in GW.
  - For a clone: one region on one PaaS or a managed container platform, calling a hosted LLM API. Plan for provider fallback (a second model provider) instead of a second cloud.
- **Kubernetes.**
  - At OpenAI scale: hundreds of clusters.
  - For a clone: not needed. A serverless or container PaaS covers it. If you do use Kubernetes, keep the 2021 and 2024 lessons: no per-node agents hammering the API server, and do not make service discovery depend on a fragile control plane.
- **Inference routing.**
  - At OpenAI scale: KV-cache-aware batching and regional failover.
  - For a clone: a thin model-routing layer, such as a cheap or fast model by default and an expensive model on intent (a mini GPT-5 router). Add per-user and per-plan token and message quotas, and stream responses over SSE. "At capacity" becomes provider 429 handling with backoff and a friendly UI message.
- **Edge and bot protection.**
  - Put Cloudflare (free tier) or similar in front of the web app.
  - Gate expensive endpoints (send message, signup) with Turnstile plus server-side token validation, IP and user rate limits, and abuse signals. LLM endpoints are expensive targets for scraping and free-tier abuse.
  - Know that your login can fail if the edge provider fails.
- **Feature flags.**
  - Use a hosted or open-source flag service (Statsig, GrowthBook, Unleash, or a DB-backed table) with server-side evaluation, cached locally, with a safe default when the flag service is unreachable.
  - Keep a kill switch for every risky feature.
  - Validate config types. The Feb 2026 "unexpected data type" outage is exactly this class of bug.
- **Rollouts.**
  - Stage infrastructure and config changes (canary, then percentage, then all).
  - Make deploy blocks really block, so nothing auto-redeploys a blocked config (Jul 25, 2026 lesson).
  - Disable unattended OS updates on critical hosts (Jun 2025 lesson).
- **Resilience.**
  - Exponential backoff with jitter on clients.
  - Circuit breakers on calls between services and to the LLM provider.
  - Health checks that do not crash-loop pods under load (Jan 2025 lesson).
  - Bounded connection pools (Sep 2026 lesson).
- **Observability.**
  - Structured logs, metrics and traces (OpenTelemetry to any backend), error tracking, and per-request token and cost accounting.
  - A public status page with honest postmortems.
  - Sample logs aggressively during launches (the ClickHouse lesson from Mar 2025).
- **Database.** One managed Postgres with read replicas covers a clone. The database-scaling details are covered by another researcher. Incidents here show DB replicas and expensive queries can still take down auth and settings paths (Feb 4 and Sep 29, 2026).

### Gaps
- No public OpenAI guidance exists for small-scale deployments. Everything in this section is extrapolation from OpenAI's incident record and general practice.
