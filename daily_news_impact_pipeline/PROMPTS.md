# Prompt Contracts

This document summarizes the public prompt contracts used by the News Impact Agent. It is written for review and explanation. The production runner stores full request payloads and provider responses outside the public repo; the examples directory keeps curated inputs and outputs that show representative behavior.

The design goal is high signal per token:

- keep JSON schemas small when structured output is required
- prefer markdown for reasoning outputs that humans read
- gate low-value sources before expensive nodes
- separate search planning from final impact reasoning
- keep LLM company wiki updates conservative

## Model Roles

| Node | Typical Model Class | Output Type | Why |
|---|---|---|---|
| Analysis gate | low-cost reasoning model | short text / decision | Skip low-signal or incomplete sources |
| Compressor | low-cost reasoning model | markdown text | Preserve investable facts while shortening long sources |
| Search planner | reasoning model with JSON discipline | JSON | Convert news into direct and semantic search terms |
| Initial match | stronger reasoning model | JSON | Narrow matched companies before final impact calls |
| Final impact | strongest reasoning model | markdown | Explain mechanism, direction, horizon, and certainty |
| Wiki update | strong editing model | markdown or decision JSON | Patch the LLM company wiki only when needed |
| Reduced wiki builder | planner + writer models | JSON then markdown | Build source package first, write wiki second |

## Policy News Branch

Policy news starts without a known ticker. The branch first decides whether the source is worth analyzing, then uses two rounds of hybrid retrieval against the final company wiki index.

### 1. Policy Analysis Gate

Purpose:

- reject incomplete crawls
- reject tiny administrative notices with no plausible company-level effect
- reject broad political commentary without concrete economic or industry mechanism

Inputs:

- policy title
- source URL
- publish date
- normalized text

Prompt contract:

```text
You are the first gate in a policy news impact pipeline.

Decide whether this source is worth company-level impact analysis for a covered A-share stock universe.

Skip when:
- the crawled text is incomplete or mostly boilerplate
- the source has too little concrete policy content
- the item is procedural, ceremonial, or too broad to map to companies
- the likely impact path is too generic for stock-level analysis

Analyze when:
- the text contains a concrete policy, regulation, funding direction, industry constraint, subsidy, demand driver, procurement signal, compliance requirement, or macro/sector mechanism
- the source could plausibly affect products, costs, demand, capacity, supply chain, financing, or risk perception

Return a short decision:
ANALYZE or SKIP
Then give one concise reason.
```

Representative output:

- [`examples/news_impact/policy_matched_energy_carbon/02_analysis_gate_output.txt`](examples/news_impact/policy_matched_energy_carbon/02_analysis_gate_output.txt)

### 2. Policy Compressor

Purpose:

- run only when the source is long
- preserve policy mechanism and investable details
- avoid summary fluff

Inputs:

- original policy text
- target length range

Prompt contract:

```text
Compress this policy source for downstream company-impact analysis.

Keep:
- policy measures, regulators, dates, target industries, numeric thresholds, timelines
- affected products, infrastructure, supply chains, costs, subsidies, demand signals, compliance requirements
- wording that changes certainty, scope, implementation status, or enforcement strength

Remove:
- ceremony, repeated background, generic slogans, duplicated paragraphs
- media framing that does not change the policy mechanism

Write 1500-2000 Chinese characters when possible.
Keep concrete nouns and trigger terms.
Do not add external facts.
```

Representative output:

- [`examples/news_impact/policy_matched_energy_carbon/04_llm_compressor_output.txt`](examples/news_impact/policy_matched_energy_carbon/04_llm_compressor_output.txt)

### 3. Round-1 Search Planner

Purpose:

- convert policy text into direct and semantic search terms
- search the full 41-company LLM wiki index
- produce terms, not conclusions

Inputs:

- policy text or compressed policy text
- short context explaining that the search target is an LLM company wiki database

JSON schema:

```json
{
  "direct_search_terms": ["..."],
  "semantic_search_terms": ["..."],
  "terms_to_downweight": ["..."]
}
```

Prompt contract:

```text
You are planning the first retrieval round for a policy news impact agent.

The search target is a database of LLM company wikis. Each wiki describes one listed company: products, assets, customers, suppliers, projects, technologies, value-chain role, financial drivers, and event trigger terms.

Read the policy. Produce search terms that can find companies plausibly affected by this policy.

Rules:
- direct_search_terms should contain exact nouns, industry phrases, policy objects, product names, and infrastructure words
- semantic_search_terms should describe business mechanisms and value-chain exposure
- terms_to_downweight should reduce generic policy words, government boilerplate, and broad slogans
- do not name companies unless the policy text directly gives company names
- output JSON only
```

Representative output:

- [`examples/news_impact/policy_matched_energy_carbon/05_brainstormer_round1_output.txt`](examples/news_impact/policy_matched_energy_carbon/05_brainstormer_round1_output.txt)

### 4. Round-2 Search Planner

Purpose:

- use first-round evidence to refine search
- only search companies returned by round one
- produce company-filtered direct and semantic queries

Inputs:

- policy text
- first-round compact evidence
- candidate companies from round one

JSON schema:

```json
{
  "company_queries": [
    {
      "ticker": "000000",
      "company": "company name",
      "direct_search_terms": ["..."],
      "semantic_search_terms": ["..."],
      "terms_to_downweight": ["..."]
    }
  ]
}
```

Prompt contract:

```text
You are planning the second retrieval round for a policy news impact agent.

The first round searched all company wikis. Now search only the companies already returned by round one. Use the first-round evidence to test whether the policy mechanism really touches each company's business.

Rules:
- keep only companies with a plausible mechanism worth checking
- use company-specific direct terms from the evidence
- use semantic terms that test the actual impact path
- do not expand to new companies
- output JSON only
```

Representative output:

- [`examples/news_impact/policy_matched_energy_carbon/07_round2_search_planner_output.txt`](examples/news_impact/policy_matched_energy_carbon/07_round2_search_planner_output.txt)

### 5. Initial Match

Purpose:

- combine first- and second-round evidence
- produce a narrower company list
- skip final impact if no company clears the bar

Inputs:

- policy text
- compact evidence from both rounds

JSON schema:

```json
{
  "matched_companies": [
    {
      "ticker": "000000",
      "company": "company name",
      "reason": "short mechanism"
    }
  ]
}
```

Prompt contract:

```text
You are the initial match node in a policy news impact pipeline.

Your job is to decide which companies from the retrieved evidence deserve final impact analysis.

Apply a slightly strict soft gate:
- include companies with a concrete policy-to-business mechanism
- include companies when the evidence shows product, asset, cost, demand, compliance, financing, or risk exposure
- exclude generic industry adjacency
- exclude companies where the only link is a broad theme
- exclude weak "maybe relevant" cases when the mechanism is not visible in the evidence

Target 0-8 companies in normal cases. Use up to 15 only for unusually broad but concrete policies.

Return JSON only: company name, ticker, and one concise reason.
```

Representative outputs:

- matched: [`examples/news_impact/policy_matched_energy_carbon/09_initial_match_output.txt`](examples/news_impact/policy_matched_energy_carbon/09_initial_match_output.txt)
- skipped: [`examples/news_impact/policy_no_initial_match/09_initial_match_output.txt`](examples/news_impact/policy_no_initial_match/09_initial_match_output.txt)

### 6. Policy Final Impact

Purpose:

- analyze one policy against one company wiki
- output concise markdown
- explain investable mechanism rather than summarize the source

Inputs:

- policy text or compressed policy text
- full company wiki
- optional cautious web search when evidence is insufficient

Prompt contract:

```text
You are analyzing one policy source against one company's LLM wiki.

First understand:
- the company's business model and value-chain position
- revenue/cost/risk drivers that matter for stock impact
- what the policy actually changes beneath the surface wording

Then write a concise markdown impact analysis under 800 Chinese characters.

Cover:
- likely direction and mechanism
- short-, medium-, and long-term paths when relevant
- certainty level and what would confirm or weaken the thesis
- impact nature: demand, cost, supply chain, capex, financing, regulation, sentiment, or valuation perception
- why this company is more or less exposed than a generic industry participant

Use company wiki evidence first. Web search may be used only when evidence is insufficient, and external sources must be treated cautiously.
Do not force a strong conclusion when the source only supports weak or indirect exposure.
```

Representative output:

- [`examples/news_impact/policy_matched_energy_carbon/10_impact_report.md`](examples/news_impact/policy_matched_energy_carbon/10_impact_report.md)

## Company Disclosure Branch

Company disclosures already map to a ticker. The branch skips policy-style initial matching.

### 1. Disclosure Compressor

Purpose:

- compress long financial reports, announcements, and quarterly reports
- preserve facts that change impact analysis or wiki update decisions

Prompt contract:

```text
Compress this company disclosure for impact analysis and possible LLM company wiki update.

Keep:
- document type, company, date, reporting period
- revenue, profit, margin, cash flow, debt, impairment, backlog, orders, capex, capacity, projects
- business-segment changes, customer/supplier changes, risk events, financing, control changes
- wording that determines whether the wiki needs no update, small patch, or rebuild

Remove:
- repeated accounting boilerplate
- governance routine text
- legal disclaimers that do not affect business understanding

Do not add external facts.
Preserve uncertainty and disclosed stage words.
```

Representative output:

- [`examples/news_impact/company_disclosure_small_update/03_llm_compressor_output.txt`](examples/news_impact/company_disclosure_small_update/03_llm_compressor_output.txt)

### 2. Disclosure Impact And Wiki Decision

Purpose:

- analyze the company-specific impact
- decide whether the LLM company wiki should remain unchanged, receive a small patch, or be rebuilt

Output:

- markdown impact analysis
- machine-readable wiki action

Prompt contract:

```text
You are analyzing one company disclosure against that company's existing LLM wiki.

First understand:
- the company's core business model
- which business lines, projects, customers, costs, financial metrics, or risks drive investable understanding
- what this disclosure changes compared with the existing wiki

Write a concise impact analysis:
- direction and mechanism
- short/medium/long-term relevance
- certainty and key caveats
- whether the disclosure changes stock-level interpretation

Then decide wiki action:
- no_update: most routine announcements and repeated information
- small_update: new but local information that changes a section of the wiki
- force_rebuild: annual report, prospectus, or a very major disclosure that changes the best source set

Default posture:
- most disclosures do not update the wiki
- most updates are small patches
- annual reports and prospectuses usually force a reduced rebuild after impact is saved
```

Representative outputs:

- no update: [`examples/news_impact/company_disclosure_no_update/04_company_disclosure_impact_output.txt`](examples/news_impact/company_disclosure_no_update/04_company_disclosure_impact_output.txt)
- small update: [`examples/news_impact/company_disclosure_small_update/04_company_disclosure_impact_output.txt`](examples/news_impact/company_disclosure_small_update/04_company_disclosure_impact_output.txt)
- force rebuild: [`examples/news_impact/company_disclosure_force_rebuild/04_company_disclosure_impact_output.txt`](examples/news_impact/company_disclosure_force_rebuild/04_company_disclosure_impact_output.txt)

### 3. Wiki Small Patch

Purpose:

- update the existing LLM company wiki only where new disclosure facts change durable company understanding
- preserve the wiki's structure and evidence discipline

Prompt contract:

```text
You are editing an existing LLM company wiki.

Inputs:
- current wiki
- new disclosure text
- wiki update decision

Task:
- apply a small patch only where the new disclosure changes durable company understanding
- preserve the current wiki structure unless a local section needs a clearer rewrite
- keep old facts when the new disclosure does not contradict or supersede them
- update freshness, financial deltas, projects, risks, and trigger terms when supported
- do not add unsupported interpretation
- do not rewrite the whole wiki for a small_update

Output the complete updated markdown wiki.
```

Representative artifacts:

- [`examples/news_impact/company_disclosure_small_update/05_wiki_update_output.md`](examples/news_impact/company_disclosure_small_update/05_wiki_update_output.md)
- [`examples/news_impact/company_disclosure_small_update/05_update_validation.json`](examples/news_impact/company_disclosure_small_update/05_update_validation.json)
- [`examples/news_impact/company_disclosure_small_update/05_wiki_archive_record.json`](examples/news_impact/company_disclosure_small_update/05_wiki_archive_record.json)

## Reduced Wiki Build Branch

Reduced wiki rebuild is used after a disclosure marks `force_rebuild`, usually because a new annual report or prospectus changes the source set.

### 1. Reduced Wiki Brainstormer

Purpose:

- select retrieval terms and optional high-value source documents
- improve source package construction
- avoid writing facts directly

JSON output:

```json
{
  "company_terms": ["..."],
  "semantic_queries": ["..."],
  "selected_doc_ids": ["..."],
  "terms_to_downweight": ["..."]
}
```

Prompt contract:

```text
You are the retrieval brainstormer for a reduced LLM company wiki builder.

You receive:
- company identity
- fixed retrieval sessions
- selected source availability
- small primer snippets

Produce JSON that helps the deterministic retrieval executor build a source package.

Rules:
- focus on company-specific products, technologies, assets, customers, suppliers, projects, risks, and stage words
- select only a small number of optional documents with high expected value
- do not write wiki prose
- do not invent facts
- output JSON only
```

Representative output:

- [`examples/wiki_rebuild/reduced_force_rebuild_002796/02_brainstormer_output.json`](examples/wiki_rebuild/reduced_force_rebuild_002796/02_brainstormer_output.json)

### 2. Reduced Wiki Writer

Purpose:

- turn deterministic source package into a compact wiki
- keep retrieval handles visible for downstream search
- preserve evidence boundaries

Prompt contract:

```text
You are writing a reduced LLM company wiki from the provided source package.

Use only the source package.

Write a compact markdown wiki that helps future news impact agents understand:
- what the company sells, owns, operates, or controls
- value-chain position and business model
- products, technologies, assets, projects, customers, suppliers, counterparties
- financial segments, quality, obligations, risks, and recent changes
- aliases, stage words, and trigger terms useful for retrieval

Rules:
- primary filings and disclosures control factual wording
- broker research is secondary context
- preserve uncertainty and disclosed stages
- avoid unsupported competitive claims
- when selected text lacks a detail, state the limitation instead of filling the gap
```

Representative artifacts:

- writer input: [`examples/wiki_rebuild/reduced_force_rebuild_002796/03_writer_model_input.md`](examples/wiki_rebuild/reduced_force_rebuild_002796/03_writer_model_input.md)
- writer output: [`examples/wiki_rebuild/reduced_force_rebuild_002796/05_writer_output.md`](examples/wiki_rebuild/reduced_force_rebuild_002796/05_writer_output.md)
- apply summary: [`examples/wiki_rebuild/reduced_force_rebuild_002796/06_apply_rebuild_summary.json`](examples/wiki_rebuild/reduced_force_rebuild_002796/06_apply_rebuild_summary.json)

## Full Wiki Build Branch

Full wiki build is the heavier onboarding route. It is slower and more expensive than reduced rebuild, and it is designed for deep company understanding.

The full builder uses a graph-controlled research process with tool-using planner subagents. It is described in detail in [`FULL_WIKI_BUILD_AGENT.md`](FULL_WIKI_BUILD_AGENT.md).

Core prompt contracts:

| Node | Prompt Role | Output |
|---|---|---|
| Anchor memo | Read the anchor source bundle and create a stable first business memo with scope, terms, segments, gaps, and factual boundaries | Long memo |
| Company brief | Compress the anchor memo into a repeated-read briefing for other agents | Short memo |
| Research goals | Turn the initial read into a company-specific research agenda | Goal list |
| Research router | Allocate 1-4 subagents with owned missions, source preferences, and done criteria | JSON |
| Wiki planner | Run one ReAct-style tool turn: local search, expand context, optional web search, commit evidence, update notes, or finish | Tool calls |
| Round draft writer | Synthesize first-pass business understanding from anchor and committed evidence | `draft_1` markdown |
| Critic | Find unsupported inference, stale facts, missing mechanisms, weak retrieval handles, and downstream usefulness gaps | Prioritized critique |
| Valuation selector | Choose three method roles from the valuation method library without price anchoring | Method memo |
| Valuation planner | Gather method-specific assumptions and missing inputs | Tool calls |
| Assumption reasoner | Produce calculator-ready assumptions with source limits and scenarios | Method memo |
| JSONizer | Convert assumptions into strict method JSON | JSON only |
| Valuation synthesis writer | Explain business quality, sensitivity, and fragility from calculator outputs | Valuation memo |
| Final wiki writer | Audit all prior artifacts and write one durable LLM company wiki | Final markdown wiki |

Representative prompt requirements:

```text
Use local corpus search before web search.
Commit only source-backed facts to the evidence bank.
Preserve aliases, products, projects, customers, suppliers, financial drivers, risks, and retrieval trigger terms.
Mark stale, incomplete, broker-only, or unsupported facts.
Use valuation as business-quality and sensitivity context.
Do not use current stock price, target price, market-cap-derived upside, or price momentum.
```

Detailed architecture:

- [`FULL_WIKI_BUILD_AGENT.md`](FULL_WIKI_BUILD_AGENT.md)
- [`WIKI_BUILD_AGENT.md`](WIKI_BUILD_AGENT.md)
- [`open_source_assets/full_wiki_builder_detail.png`](open_source_assets/full_wiki_builder_detail.png)
- [`open_source_assets/full_wiki_research_loop_detail.png`](open_source_assets/full_wiki_research_loop_detail.png)

## Prompt Design Principles

- The model sees only inputs that matter for its node.
- Search planners output JSON because downstream retrieval needs structured terms.
- Final impact nodes output markdown because humans review them.
- Evidence compact rendering happens before the initial match node to reduce noise and context length.
- Wiki update prompts use conservative defaults to avoid unnecessary churn.
- Force rebuild follows impact analysis, so business impact is recorded before the wiki source set changes.
