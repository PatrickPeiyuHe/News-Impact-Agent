# Full Wiki Build Agent

The full wiki build agent is the high-budget company onboarding path in this project. The daily production path uses the reduced wiki builder by default, while the full builder is reserved for cases where quality, auditability, and deep company understanding justify a slower run.

This module is important because it shows the system beyond a single prompt. It demonstrates graph orchestration, deep file research, tool-using planner agents, evidence persistence, critique and revision, and financial-domain controls.

## Position In The System

The News Impact Agent depends on an LLM company wiki: a durable company knowledge object that can be retrieved by policy-news RAG and read by final impact nodes.

There are two wiki build routes:

| Route | Default Use | Output | Cost Profile |
|---|---|---|---|
| Reduced wiki builder | Daily pipeline rebuilds after annual reports, prospectuses, or major disclosures | Compact 2000-4000 Chinese-character wiki | Fast enough for recurring updates |
| Full wiki builder | First-time onboarding, manual deep review, complex companies, showcase-quality research | Long-form company wiki with evidence bank, critique trail, and valuation lens | More expensive and slower |

The reduced builder is the operational default. The full builder is the optional extension path when budget and review time are available.

## Architecture Analogy

The full builder is architecturally similar to a LangGraph/ReAct hybrid:

- A deterministic DAG controls stage order, artifact contracts, and stop conditions.
- Inside research stages, router-assigned planner subagents run ReAct-style tool turns: choose tools, search local files, expand context, optionally use web search, commit evidence, update notes, and decide when gathering is done.
- The runtime merges every subagent turn into shared evidence banks and mutable research notes.
- Critic and final-writer stages close the loop by auditing the draft against evidence and valuation outputs.

This design gives the agent room to investigate while preserving reviewable intermediate artifacts.

## System Diagram

![Full wiki builder detail](open_source_assets/full_wiki_builder_detail.png)

The full build creates intermediate artifacts before the final wiki:

```text
anchor source bundle
  -> anchor memo
  -> company brief v1
  -> research goals v1
  -> company research loop v1
  -> evidence bank v1 + loop note v1
  -> draft_1
  -> valuation method selection
  -> valuation research loop v1
  -> valuation memo v1 + calculator outputs
  -> critic_1
  -> company brief v2
  -> company research loop v2
  -> evidence bank v2 + loop note v2
  -> valuation refresh v2
  -> final wiki writer
  -> company_wiki.md
```

## Research Loop Runtime

![Full wiki research loop detail](open_source_assets/full_wiki_research_loop_detail.png)

Each research loop has three layers:

| Layer | Responsibility |
|---|---|
| Router | Splits the research agenda into 1-4 owned subagents |
| Planner subagents | Run tool-using turns over the document corpus and selected web gaps |
| Runtime | Executes tools, merges evidence, updates notes, enforces max turns and done states |

Default company research tracks:

| Track | Mission |
|---|---|
| `company_map` | Identity surface, legal entities, aliases, facilities, ownership/control hooks, and scope boundaries |
| `business_engine` | Products, technology routes, capacity, customers, delivery path, and monetization mechanism |
| `economics_quality` | Revenue mix, margin/cash-flow anchors, concentration, capital intensity, impairment, and earnings quality |
| `recent_delta_and_risks` | Recent changes, unresolved issues, timing dependencies, and external triggers |

The loop is intentionally file-first. Local parsed filings, disclosures, prospectuses, and research reports are searched before web search. Web search is reserved for freshness-sensitive gaps or source verification.

## Tool Contract

Planner agents use a small tool surface:

| Tool | Purpose |
|---|---|
| `search_corpus` | Hybrid search over local parsed documents |
| `expand_corpus_context` | Pull surrounding section, table, or heading context |
| `web_search` | Fill freshness-sensitive or source-verification gaps |
| `commit_evidence` | Write source-backed facts into the shared evidence bank |
| `update_research_note` | Maintain a loop-level scratchpad for unresolved questions and next turns |
| `done_gathering` | Mark a subagent complete |

The valuation loop adds financial tools such as valuation fact packs, financial snapshots, peer comparison, metric series, forecast events, and dividend history.

## Evidence Model

The full builder separates temporary working memory from durable evidence:

- Subagent working memory holds the previous tool results for that subagent.
- Shared evidence bank stores committed facts with source locators and evidence boundaries.
- Loop mutable note stores open questions, conflicts, and cross-track findings.
- Final writer sees completed evidence banks and notes, then writes one coherent company wiki.

This separation reduces noisy context and makes the final answer auditable.

## Valuation Stage

The valuation stage is used as a business-quality and sensitivity lens. It is designed to avoid price-anchored output.

LLM-visible valuation packets exclude:

- current close price
- target prices
- own-company trading multiples
- market-cap-derived upside framing
- price momentum

Allowed valuation context includes company-sourced financial data, broker forecasts used cautiously, peer comparisons, and method-specific calculator outputs.

Method library:

| Method | Typical Role |
|---|---|
| `Forward_Earnings` | primary or secondary anchor |
| `Normalized_EV_EBIT_or_EBITDA` | cycle-aware cross-check |
| `Revenue_Multiple_with_Quality_Gate` | quality and growth lens |
| `SOTP_RNAV` | multi-asset or multi-segment companies |
| `Adjusted_PB_NAV` | asset-heavy and balance-sheet-driven companies |
| `Cycle_Normalized_Earnings_or_EBIT` | cyclical companies |
| `TTM_Adjusted_Earnings` | recent earnings reality check |
| `DCF_Sensitivity` | sensitivity-only mechanism |
| `Justified_PB_Check` | diagnostic cross-check |

The selector usually chooses three methods with roles such as primary anchor, secondary anchor, or cross-check. Deterministic calculators run after assumption JSON is produced.

## Prompt Contracts

The full builder uses prompts as stage contracts. Each node receives only the artifacts needed for its job.

### Anchor Memo

Purpose:

- Turn the anchor source bundle into a stable first business memo.
- Capture company scope, terms, segments, core products, obvious risk areas, and unresolved gaps.

Output:

- Long-form memo with factual boundaries.
- No final wiki prose.

Key prompt requirements:

```text
Read the anchor source bundle as the first serious company orientation.
Identify what the company actually sells, owns, operates, or controls.
Capture aliases, products, segments, facilities, customers, suppliers, projects, financial drivers, and uncertainty boundaries.
Mark facts that appear stale, incomplete, broker-only, or unsupported by primary filings.
Do not fill missing details from memory.
```

### Company Brief

Purpose:

- Create a compact repeated-read briefing for downstream nodes.
- Reduce context cost while preserving the company map and research questions.

Output:

- Short memo with identity, business lines, trigger terms, and open questions.

Key prompt requirements:

```text
Condense the anchor memo into a reusable company briefing.
Keep company-specific nouns and trigger terms.
Preserve scope boundaries and known gaps.
Write for other agents that will search a local document corpus.
```

### Research Goals

Purpose:

- Convert the initial company read into a research agenda.
- Prioritize questions that affect business understanding and future news impact.

Output:

- Research goals grouped by business mechanism, evidence need, and likely source type.

Key prompt requirements:

```text
Create a research agenda for building a durable LLM company wiki.
Prioritize questions that change business model, value-chain position, earnings drivers, risks, and retrieval handles.
Prefer primary filings and announcements for factual claims.
Treat broker research as secondary framing.
```

### Research Router

Purpose:

- Split the agenda into 1-4 owned subagents.
- Avoid overlapping work.

Output:

- JSON subagent assignments.

Key prompt requirements:

```text
Assign research work to 1-4 subagents.
Each subagent must have a clear mission, owned questions, likely search terms, source preferences, and done criteria.
Avoid duplicate ownership across subagents.
Output JSON only.
```

### Wiki Planner

Purpose:

- Run one tool-using research turn for one subagent.
- Choose searches, context expansion, evidence commits, note updates, or done state.

Output:

- Tool calls only.

Key prompt requirements:

```text
You are one planner subagent inside a company wiki research loop.
Use local corpus search before web search.
Commit only source-backed facts to the evidence bank.
Update the research note when a gap, conflict, or next action matters.
Call done_gathering when your owned questions are sufficiently answered or no useful next search remains.
```

### Round Draft Writer

Purpose:

- Synthesize first-pass business understanding from anchor and evidence bank v1.

Output:

- `draft_1`, a structured company wiki draft.

Key prompt requirements:

```text
Write a first company wiki draft from the anchor memo and committed evidence.
Explain the business mechanism, value-chain position, products, assets, customers, suppliers, economics, and risks.
Use evidence boundaries. Mark unresolved or stale facts clearly.
Do not overstate customer relationships, capacity status, or project progress.
```

### Critic

Purpose:

- Audit `draft_1` and valuation package.
- Identify unsupported claims, stale facts, missing mechanisms, weak retrieval handles, and final-wiki risks.

Output:

- Prioritized critique with repair instructions.

Key prompt requirements:

```text
Review the draft as a skeptical financial research editor.
Find unsupported inference, stale evidence, missing business mechanisms, vague risk language, and weak downstream retrieval terms.
Prioritize fixes that would change future news impact analysis.
```

### Valuation Method Selector

Purpose:

- Choose method roles before assumptions are generated.

Output:

- Method-selection memo.

Key prompt requirements:

```text
Select three valuation methods from the method library.
Explain each method's role: primary anchor, secondary anchor, cross-check, diagnostic, or sensitivity-only.
Base selection on the company's business model and financial structure.
Do not use current stock price, target price, market-cap-derived upside, or price momentum.
```

### Valuation Planner And Assumption Reasoner

Purpose:

- Gather method-specific inputs.
- Produce calculator-ready assumptions with source limits.

Output:

- Method-specific memo, then strict JSON for calculators.

Key prompt requirements:

```text
Reason through valuation assumptions as business sensitivities, not price targets.
Separate observable facts, inferred assumptions, and uncertainty ranges.
Use bear/base/bull where appropriate.
Avoid copying broker targets or market-price framing into assumptions.
```

### Valuation JSONizer

Purpose:

- Convert assumptions into strict method JSON.

Output:

- JSON only.

Key prompt requirements:

```text
Convert the assumption memo into the required JSON schema.
Preserve numeric values, units, scenario names, and missing-value markers.
Do not add prose.
Do not invent missing numbers.
```

### Valuation Synthesis Writer

Purpose:

- Turn calculators and assumptions into a business-quality memo.

Output:

- Valuation memo.

Key prompt requirements:

```text
Explain what the valuation work says about business quality, sensitivity, and fragility.
Discuss the assumptions that matter most.
Avoid target-price and short-term trading language.
```

### Final Wiki Writer

Purpose:

- Write the final durable wiki from all prior artifacts.

Output:

- `company_wiki.md`.

Key prompt requirements:

```text
Write one durable LLM company wiki.
Use anchor memo, draft, critic, evidence banks, research notes, valuation memos, and calculator summaries.
Prioritize facts that help future news impact analysis:
business model, value-chain role, products, assets, projects, customers, suppliers, economics, risks, recent deltas, aliases, and retrieval trigger terms.
Preserve uncertainty, disclosed stage words, and source limits.
Keep valuation discussion as business sensitivity and quality context.
```

## Reviewer Takeaways

The full builder is the strongest architecture showcase in the wiki system:

- It uses a graph of bounded nodes instead of one large prompt.
- It lets subagents investigate while maintaining evidence discipline.
- It preserves intermediate artifacts that a reviewer can audit.
- It combines qualitative company research with deterministic valuation calculations.
- It produces a richer wiki when onboarding time and API budget allow it.

Code entry points:

- [`daily_news_impact/wiki_build_agent/full.py`](daily_news_impact/wiki_build_agent/full.py)
- [`daily_news_impact/wiki_build_agent/orchestrator.py`](daily_news_impact/wiki_build_agent/orchestrator.py)
- [`show_wiki_build_plan.py`](show_wiki_build_plan.py)

Example full wiki outputs:

- [`examples/wikis/full/603162__full_wiki.md`](examples/wikis/full/603162__full_wiki.md)
- [`examples/wikis/full/688668__full_wiki.md`](examples/wikis/full/688668__full_wiki.md)
