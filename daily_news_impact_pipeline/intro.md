# Daily News Impact Agent: A Real-World Event Understanding Layer For Quant Trading

## English Version

Daily News Impact Agent is a daily event-understanding system for A-share research. It monitors policy news, company disclosures, financial reports, prospectuses, and stock research reports, maps them to a focused company universe, analyzes their likely impact, updates a durable company knowledge layer, and produces daily action tables for downstream investment review.

I built this project in about one month as a companion system to SignalForge. SignalForge monitors price, volume, microstructure, market regime, and execution risk. Daily News Impact Agent adds a real-world context layer: what happened recently, which listed companies may be affected, how strong the impact is, and whether the company memory needs to be updated before future analysis.

## Why It Exists

Price-volume models are strong at detecting abnormal behavior. Event attribution requires a second layer that reads news, disclosures, and company context. A strong portfolio workflow needs both layers:

- a quantitative signal layer that finds unusual technical and statistical setups;
- an event-understanding layer that reads policy, disclosures, reports, and company context;
- a bridge between the two, so a candidate stock can be reviewed through recent catalysts, risks, and company-specific facts.

This agent was designed for that bridge. For a daily Top 10, watchlist, or focused sector universe, it can answer: what changed recently, whether the event is likely positive or negative, how certain the conclusion is, and whether the signal is supported by a concrete catalyst or exposed to a disclosure risk.

## System Overview

The system runs as a staged daily pipeline over a Chinese natural-date range:

1. Crawl and parse policy news.
2. Crawl and parse company disclosures, annual reports, quarterly reports, prospectuses, and stock research reports.
3. Ingest company documents into a local document database and rebuild retrieval indexes.
4. Run policy-news impact analysis through a multi-stage RAG workflow.
5. Run company-disclosure impact analysis for ticker-mapped events.
6. Decide whether each company wiki needs no update, a small patch, or a reduced rebuild.
7. Refresh the 41-company wiki RAG index.
8. Write daily action tables, coverage tables, impact summaries, and latest wiki snapshots.

The main product surface is the daily output package. A sample run for `2026-04-25` to `2026-04-28` completed successfully and produced `118` action rows across the 41-company coverage universe.

## Agent Architecture

The pipeline is organized around several cooperating agents and deterministic stages:

- **Source update stage:** wraps existing crawlers, parsers, document ingestion, and index refresh into one daily command.
- **Preflight stage:** checks policy database, company document database, wiki database, and retrieval index readiness before expensive model calls.
- **Policy impact branch:** filters low-signal news, compresses long policy text when needed, plans retrieval queries, performs hybrid search over company wikis, runs an initial company-match gate, and produces final company-level impact reports.
- **Company disclosure branch:** analyzes ticker-mapped announcements and reports directly against the current company wiki, then outputs impact direction, certainty, impact nature, and wiki action.
- **Wiki update branch:** applies small wiki patches for incremental events and triggers reduced rebuilds for major source changes such as annual reports or prospectus-like documents.
- **Reporting stage:** writes machine-readable CSV/JSON artifacts and human-readable Markdown summaries for review.

This architecture is intentionally staged. Each step leaves intermediate artifacts, so the pipeline can be reviewed, resumed, debugged, and presented while keeping raw API payloads and production credentials private.

## LLM Company Wiki Memory

The LLM wiki layer is one of the most important design choices in this project. The motivation came from a practical limitation: general-purpose models often have incomplete or stale knowledge about specific A-share companies, especially smaller listed companies, recent disclosures, supply-chain relationships, aliases, projects, and segment-level operating variables.

Naive RAG over raw company documents can retrieve useful fragments. Those fragments alone often fail to form a stable company model. For investment reasoning, the agent needs to understand what the company actually does, where it sits in the value chain, which events matter, which metrics drive earnings or risk, which claims are primary-source facts, and which details remain uncertain. Running deep research for every company on every news item would be too expensive in tokens, latency, and human review effort.

The company wiki solves this by turning repeated research into durable memory. Each wiki is a compact, evidence-bound company object that stores the business model, products, assets, customers, suppliers, technologies, projects, aliases, value-chain position, recent changes, risk points, and information freshness. Downstream impact agents can retrieve this memory before judging policy news or company disclosures.

The full wiki path is also a small agent project inside the project. I built a file research agent that selects local filings and reports, plans retrieval objectives, reads evidence, builds an evidence bank, writes a company wiki, and runs a critic/revision loop before publishing. The loop is close to a ReAct-style workflow: plan, retrieve, read, write, critique, revise, and archive. The daily pipeline then uses a lighter wiki maintenance path for incremental updates and major-source refreshes.

From an agent-engineering perspective, this is the main technical point: the system treats memory as a first-class product surface. It separates raw documents, retrieved evidence, durable company understanding, event-level reasoning, and final user outputs. That separation improves reliability, lowers repeated research cost, and makes the agent easier to inspect.

## Output Surface

The final daily outputs are designed for both manual review and downstream integration:

- `daily_all_company_actions.csv`: all policy, disclosure, and wiki actions in the run.
- `daily_company_coverage.csv`: fixed 41-company coverage per date, including companies with no action.
- per-date `company_actions.csv`: daily event impact table for review.
- per-date `company_coverage.csv`: daily coverage table for the whole universe.
- impact reports: Markdown summaries explaining direction, certainty, mechanism, horizon, and risk.
- wiki archive and snapshot records: traceable changes to the company memory layer.

Representative fields include date, ticker, company, source type, title, action type, impact direction, certainty, impact nature, wiki action, impact report path, wiki path, source URL, and notes.

## Integration With SignalForge

Daily News Impact Agent can sit next to SignalForge in the investment workflow:

- review recent 3-5 day news and disclosure context for each daily Top 10 candidate;
- flag negative announcements, delayed risks, or policy-sensitive exposures before execution;
- explain why a technical signal may have strengthened, weakened, or become crowded;
- create event tags that can later become model features or selector constraints;
- maintain a company memory layer for focused sectors such as communication equipment, AI infrastructure, optical modules, and data-center supply chains.

The current version is already useful as a research and review assistant. The next natural step is to convert impact direction, certainty, catalyst type, and wiki freshness into structured features that can be joined with the quantitative pipeline.

## What This Demonstrates

This project shows my ability to build an AI-native research agent around a real investment workflow:

- **Agent workflow design:** multi-stage gating, retrieval planning, compression, initial matching, final impact reasoning, memory updates, critic-style review, and report generation.
- **RAG and memory engineering:** company-level long-term memory, hybrid retrieval, evidence packaging, source selection, index refresh, and artifact traceability.
- **File research agent design:** local document selection, iterative evidence reading, evidence-bank construction, long-form wiki writing, critique, revision, and publishing.
- **Financial reasoning:** translating policy and disclosure text into company-level impact direction, certainty, horizon, mechanism, and risk.
- **System engineering:** one-click daily execution, preflight checks, resumable stages, structured outputs, examples, and open-source presentation assets.
- **Product judgment:** balancing model capability, token cost, latency, inspectability, and human review effort in a real investment workflow.

Together with SignalForge, this project shows a broader direction: quantitative models identify candidate opportunities, while LLM agents maintain real-world company context and explain recent event risk.

---

## 中文版本

Daily News Impact Agent 是一套面向 A 股研究的日度事件理解系统。它每天监测政策新闻、公司公告、财报、招股书和个股研报，将事件映射到重点公司池，分析潜在影响，更新长期公司知识层，并生成可供投资复盘和下游系统使用的日度 action table。

我用大约一个月时间搭建了这个项目，把它作为 SignalForge 的配套系统。SignalForge 负责监测价格、成交量、盘中微观结构、市场环境和执行风险；Daily News Impact Agent 补充真实世界上下文：最近发生了什么、哪些上市公司可能受影响、影响强度如何、是否需要更新公司记忆，再让后续分析站在新的事实基础上继续推理。

## 项目动机

价格成交量模型擅长发现异常行为。事件归因还需要一层能阅读新闻、公告和公司上下文的系统。一个更完整的投资工作流需要同时覆盖三层信息：

- 量化信号层：发现异常技术形态和统计机会；
- 事件理解层：阅读政策、公告、研报和公司上下文；
- 连接层：把候选股票放回最近催化、风险和公司事实中审视。

这个 Agent 就是为这条连接层设计的。对于 daily Top 10、watchlist 或重点行业股票池，它可以回答：最近发生了什么，事件方向偏正面还是负面，结论置信度如何，以及当前量化信号是否有明确催化或披露风险。

## 系统概览

系统按中国自然日期区间运行，采用分阶段日度 pipeline：

1. 抓取和解析政策新闻。
2. 抓取和解析公司公告、年报、季报、招股书和个股研报。
3. 将公司文档写入本地文档库并重建检索索引。
4. 通过多阶段 RAG workflow 分析政策新闻影响。
5. 对已经映射到 ticker 的公司披露做影响分析。
6. 判断公司 wiki 需要保持不变、小补丁更新，还是 reduced rebuild。
7. 刷新 41 家公司 wiki RAG index。
8. 写出日度 action table、coverage table、impact summary 和最新 wiki snapshot。

最终产物是一个日度输出包。样例运行覆盖 `2026-04-25` 到 `2026-04-28`，已完成执行，并在 41 家公司覆盖池中生成 `118` 条 action rows。

## Agent 架构

这个 pipeline 由多个 Agent 节点和确定性工程阶段协作完成：

- **Source update stage：** 把已有 crawler、parser、document ingest 和 index refresh 封装成一个日度命令。
- **Preflight stage：** 在昂贵模型调用前检查 policy DB、company document DB、wiki DB 和 retrieval index 状态。
- **Policy impact branch：** 过滤低信号新闻，必要时压缩长政策文本，规划检索 query，在公司 wiki 中做 hybrid search，先做公司匹配门控，再生成公司级 impact report。
- **Company disclosure branch：** 对已映射 ticker 的公告和报告，直接结合当前公司 wiki 分析影响方向、置信度、影响性质和 wiki action。
- **Wiki update branch：** 对增量事件执行小补丁；对年报、招股书、重大信息源变化触发 reduced rebuild。
- **Reporting stage：** 输出 CSV/JSON 机器可读结果和 Markdown 人类可读报告。

这种分阶段设计让每一步都有中间产物，便于 review、resume、debug 和开源展示，同时避免暴露原始 API payload 和生产凭证。

## LLM Company Wiki Memory

LLM wiki 是这个项目里的一个关键亮点。我的设计出发点很实际：通用模型对 A 股中小公司、最新披露、产业链细节、别名关系和项目进展的掌握经常滞后；普通 RAG 每次从公司数据库里搜索片段，容易拿到局部事实，也经常缺少对公司本质、产业链位置和影响变量的稳定理解；每次针对每家公司做 deep research，token、延迟和人工 review 成本都很高。

因此，LLM wiki 承担公司级长期记忆的角色。每家公司都有一个紧凑、基于证据的公司对象，记录商业模式、核心产品、资产项目、客户供应商、关键技术、别名、产业链位置、近期变化、风险点和信息新鲜度。后续 policy impact agent 或 disclosure impact agent 在判断事件影响前，会先读取这个公司记忆。

Full wiki 路径本身也是一个小型 Agent 项目。我手搓了一个 file research agent：它会选择本地公告、财报和研报文件，规划检索目标，读取证据，构建 evidence bank，生成公司 wiki，再通过 critic/revision loop 做质量检查后发布。这个循环接近 ReAct 风格：plan、retrieve、read、write、critique、revise、archive。日度 pipeline 则使用更轻的维护路径处理增量更新和重大信息源刷新。

从 Agent Engineer 的角度看，这里的技术亮点是把 memory 当成一等系统对象来设计。系统区分 raw documents、retrieved evidence、durable company understanding、event-level reasoning 和 final user outputs。这样的分层降低重复研究成本，提高影响判断稳定性，也让每次输出更容易审查。

## 输出形态

日度输出同时面向人工 review 和下游系统接入：

- `daily_all_company_actions.csv`：一次运行中所有 policy、disclosure 和 wiki actions。
- `daily_company_coverage.csv`：每天固定 41 家公司覆盖表，包含无动作公司。
- 按日期拆分的 `company_actions.csv`：当天事件影响表。
- 按日期拆分的 `company_coverage.csv`：当天完整 coverage 表。
- impact reports：解释方向、置信度、机制、影响周期和风险的 Markdown 报告。
- wiki archive 和 snapshot records：记录公司记忆层的每一次变化。

代表性字段包括 date、ticker、company、source type、title、action type、impact direction、certainty、impact nature、wiki action、impact report path、wiki path、source URL 和 notes。

## 与 SignalForge 的结合

Daily News Impact Agent 可以放在 SignalForge 旁边，形成更完整的投资工作流：

- 为 daily Top 10 候选股检查最近 3-5 天新闻和公告上下文；
- 在执行前标记负面公告、滞后风险或政策敏感暴露；
- 解释某个技术信号可能增强、减弱或变得拥挤的事件原因；
- 生成 event tags，未来可以转化为模型特征或 selector 约束；
- 为通信设备、AI 基础设施、光模块、数据中心供应链等重点方向维护公司记忆层。

当前版本已经可以作为研究和 review assistant 使用。下一步可以把 impact direction、certainty、catalyst type 和 wiki freshness 结构化后接入量化 pipeline。

## 这个项目体现的能力

这个项目展示了我围绕真实投资工作流构建 AI-native research agent 的能力：

- **Agent workflow design：** 多阶段门控、检索规划、文本压缩、初始匹配、最终影响推理、长期记忆更新、critic-style review 和报告生成。
- **RAG and memory engineering：** 公司级长期记忆、hybrid retrieval、证据打包、source selection、index refresh 和 artifact traceability。
- **File research agent design：** 本地文档选择、迭代式证据阅读、evidence bank 构建、长文 wiki 写作、critique、revision 和 publishing。
- **金融推理：** 把政策和披露文本转化为公司级影响方向、置信度、周期、机制和风险。
- **系统工程：** 一键日度运行、preflight checks、可恢复 stages、结构化输出、样例集和开源展示材料。
- **产品判断：** 在真实投资工作流里平衡模型能力、token 成本、延迟、可审查性和人工 review 负担。

和 SignalForge 放在一起看，这个项目展示了一个更完整的方向：量化模型发现候选机会，LLM Agent 维护真实世界公司上下文，并解释近期事件风险。
