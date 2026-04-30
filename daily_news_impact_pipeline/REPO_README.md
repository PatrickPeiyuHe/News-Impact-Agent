# News Impact Agent

News Impact Agent is an agentic financial research system that turns daily policy news, company disclosures, filings, and broker research into stock-level impact analysis and continuously maintained LLM company wikis.

Given a date range and a covered stock universe, the system:

1. collects and parses new information,
2. identifies which companies are plausibly affected,
3. analyzes impact against durable company knowledge,
4. patches or rebuilds the company wiki when the source changes investable understanding,
5. publishes daily company action tables for review.

The implementation focuses on Chinese A-share workflows, while the architecture is general: source ingestion, document indexing, hybrid RAG, evidence-grounded company matching, per-company impact reasoning, conservative wiki updates, and resumable daily outputs.

## Why This Project Exists

Most financial-news agents fail at two points: they lack durable company memory, and they over-analyze low-signal sources. This project treats the company wiki as a first-class LLM artifact and uses gates, retrieval, and update decisions to spend model budget where the signal is strongest.

The repository is also an engineering showcase. It demonstrates:

- graph-style pipeline orchestration with resume-safe stage outputs,
- hybrid search and two-round policy-company matching,
- direct company-disclosure impact analysis,
- conservative wiki patch and rebuild decisions,
- a reduced wiki builder used by default in the daily pipeline,
- an optional full wiki build agent for deep file research and higher-quality onboarding,
- curated intermediate artifacts that make model behavior reviewable.

## Architecture

![News Impact Agent architecture](daily_news_impact_pipeline/open_source_assets/news_impact_agent_architecture.png)

The daily pipeline has four main layers:

| Layer | Role |
|---|---|
| Source update | Crawl, parse, ingest, and index policy news, disclosures, filings, and research reports |
| Policy impact branch | Run gates, two-round hybrid RAG, initial match, and final company impact analysis |
| Company disclosure branch | Analyze mapped company disclosures directly and decide wiki action |
| Wiki and daily outputs | Apply small patches or reduced rebuilds, archive old wikis, rebuild index, publish daily tables |

## Runnability Evidence

The repository includes executable entry points and curated run artifacts so reviewers can verify that the agent has a real operating path:

- one-click CLI: [`daily_news_impact_pipeline/run_daily_news_impact_one_click.py`](daily_news_impact_pipeline/run_daily_news_impact_one_click.py)
- stage orchestrator: [`daily_news_impact_pipeline/daily_news_impact/cli.py`](daily_news_impact_pipeline/daily_news_impact/cli.py)
- dry-run smoke result: [`daily_news_impact_pipeline/examples/smoke_runs/dry_run_20260428_summary.json`](daily_news_impact_pipeline/examples/smoke_runs/dry_run_20260428_summary.json)
- real policy/disclosure/wiki traces: [`daily_news_impact_pipeline/examples/`](daily_news_impact_pipeline/examples/)
- execution proof guide: [`daily_news_impact_pipeline/RUNNABILITY_EVIDENCE.md`](daily_news_impact_pipeline/RUNNABILITY_EVIDENCE.md)

Quick verification commands:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py --help
python daily_news_impact_pipeline\show_wiki_build_plan.py --describe-modes
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py `
  --date-from 2026-04-28 `
  --date-to 2026-04-28 `
  --run-id review_dry_run `
  --dry-run `
  --skip-wiki-snapshot
```

## Wiki Build Agents

The LLM company wiki is the system's durable knowledge object. It stores business model, value-chain role, products, projects, customers, suppliers, financial drivers, risks, aliases, and retrieval trigger terms.

Two build routes are documented:

- **Reduced Wiki Builder**: the default daily route. It selects a compact source set, builds a hybrid source package, and writes a 2000-4000 Chinese-character wiki suitable for recurring updates.
- **Full Wiki Build Agent**: an optional high-budget route for first-time onboarding and deep review. It uses a graph-controlled research process with ReAct-style planner subagents, evidence banks, critic/revision stages, and valuation calculators.

Start here:

- [Wiki Build Agent Design](daily_news_impact_pipeline/WIKI_BUILD_AGENT.md)
- [Full Wiki Build Agent](daily_news_impact_pipeline/FULL_WIKI_BUILD_AGENT.md)

## Main Documents

- [Daily Pipeline README](daily_news_impact_pipeline/README.md)
- [Reviewer Guide](daily_news_impact_pipeline/REVIEW_GUIDE.md)
- [Runnability And Evidence](daily_news_impact_pipeline/RUNNABILITY_EVIDENCE.md)
- [Prompt Contracts](daily_news_impact_pipeline/PROMPTS.md)
- [Wiki Build Agent Design](daily_news_impact_pipeline/WIKI_BUILD_AGENT.md)
- [Full Wiki Build Agent](daily_news_impact_pipeline/FULL_WIKI_BUILD_AGENT.md)
- [Curated Examples](daily_news_impact_pipeline/examples/README.md)

## Code Map

```text
daily_news_impact_pipeline/
  run_daily_news_impact_one_click.py
  show_wiki_build_plan.py
  daily_news_impact/
    cli.py
    source_update.py
    preflight.py
    impact.py
    force_rebuild.py
    reports.py
    wiki_build_agent/
      contracts.py
      source_selection.py
      reduced.py
      full.py
      orchestrator.py
  examples/
```

## Example Outputs

The `examples/` directory includes:

- sample full and reduced company wikis,
- a matched policy-news impact trace,
- a policy no-match skip trace,
- company-disclosure no-update, small-update, and force-rebuild cases,
- reduced wiki rebuild intermediate artifacts,
- daily action and coverage tables.

These examples are curated from real pipeline runs and keep the important execution artifacts while excluding raw API requests, raw provider responses, private credentials, and production database state.

## How To Review

Start with the [Reviewer Guide](daily_news_impact_pipeline/REVIEW_GUIDE.md). It gives 5-minute, 15-minute, 30-minute, and 60-minute reading paths.

For LLM behavior, read [Prompt Contracts](daily_news_impact_pipeline/PROMPTS.md). It summarizes node roles, schemas, gates, and conservative wiki-update rules.

For the strongest architecture showcase, read [Full Wiki Build Agent](daily_news_impact_pipeline/FULL_WIKI_BUILD_AGENT.md). It explains the deep file research loop, graph orchestration, planner subagents, valuation stage, and final writer contract.

## Status

This is a design-and-engineering showcase repository. Some source collectors and database adapters are represented as explicit interfaces or command adapters because the original production environment depends on local data sources, credentials, and private databases.
