# Daily News Impact Pipeline

This folder contains the one-click daily orchestration layer for News Impact Agent.

The pipeline takes a date range and a covered stock universe, updates the source database, runs policy and company-disclosure impact analysis, updates LLM company wikis when needed, rebuilds the final wiki index, and publishes daily company action tables.

## What The Pipeline Does

```text
date range + covered stock universe
  -> source crawl / parse / ingest / index
  -> policy news impact branch
  -> company disclosure impact branch
  -> wiki patch or reduced rebuild
  -> final wiki index refresh
  -> daily company action tables and wiki snapshots
```

Source categories:

| Category | Role |
|---|---|
| `policy` | Policy news crawl and parsing. Policy text is analyzed directly and does not require embedding by default. |
| `cninfo` | Company disclosures, financial reports, prospectuses, and announcements. |
| `eastmoney` | Broker research reports. |
| `ingest` | Load company disclosures and research reports into the wiki/document database. |
| `index` | Build or refresh searchable indexes. Embedding jobs should use CUDA when available. |

## Architecture

![News Impact Agent architecture](open_source_assets/news_impact_agent_architecture.png)

The daily run has four layers:

1. **Source update**: crawl, parse, ingest, and index newly available information.
2. **Policy impact branch**: use gates, two-round hybrid RAG, initial match, and final per-company impact analysis.
3. **Company disclosure branch**: analyze disclosures directly against the mapped company's wiki and decide wiki action.
4. **Publishing**: apply wiki changes, archive old versions, rebuild final index, and write daily outputs.

## Entry Point

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py `
  --date-from 2026-04-25 `
  --date-to 2026-04-28 `
  --device cuda `
  --run-id daily_news_impact_20260425_20260428_r1 `
  --continue-on-error
```

Dry run:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py `
  --date-from 2026-04-28 `
  --date-to 2026-04-28 `
  --run-id daily_news_impact_20260428_dryrun `
  --dry-run `
  --skip-wiki-snapshot
```

Impact-only run after sources are already ingested:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py `
  --date-from 2026-04-28 `
  --date-to 2026-04-28 `
  --run-id daily_news_impact_20260428_impact_only_r1 `
  --skip-source-update `
  --device cuda `
  --continue-on-error
```

## Runnability Evidence

This repository includes evidence that the pipeline is executable:

- [`run_daily_news_impact_one_click.py`](run_daily_news_impact_one_click.py) exposes the one-click CLI.
- [`daily_news_impact/cli.py`](daily_news_impact/cli.py) implements stage orchestration, resume behavior, and run summaries.
- [`examples/smoke_runs/dry_run_20260428_summary.json`](examples/smoke_runs/dry_run_20260428_summary.json) records a completed dry-run smoke test.
- [`examples/news_impact/`](examples/news_impact/) contains real policy and disclosure impact traces.
- [`examples/wiki_rebuild/`](examples/wiki_rebuild/) contains a reduced wiki rebuild trace.
- [`RUNNABILITY_EVIDENCE.md`](RUNNABILITY_EVIDENCE.md) maps code paths, smoke commands, and intermediate artifacts.

Offline verification commands:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py --help
python daily_news_impact_pipeline\show_wiki_build_plan.py --describe-modes
```

The full live pipeline requires local crawlers, parsed document databases, and LLM provider keys. Those dependencies are isolated behind source and impact adapters, so the orchestration and output contracts remain reviewable in the open repo.

## Directory Map

```text
daily_news_impact_pipeline/
  run_daily_news_impact_one_click.py
  show_wiki_build_plan.py
  README.md
  REVIEW_GUIDE.md
  RUNNABILITY_EVIDENCE.md
  PROMPTS.md
  WIKI_BUILD_AGENT.md
  FULL_WIKI_BUILD_AGENT.md
  examples/
  daily_news_impact/
    cli.py
    source_update.py
    preflight.py
    impact.py
    force_rebuild.py
    reports.py
    utils.py
    wiki_build_agent/
      contracts.py
      source_selection.py
      reduced.py
      full.py
      orchestrator.py
```

## Policy News Impact Branch

![Policy news impact branch](open_source_assets/policy_news_branch_detail.png)

Policy news starts without a known ticker. The branch uses:

1. source usability gate,
2. optional compression,
3. round-1 hybrid search over the company wiki index,
4. round-2 company-filtered search,
5. initial match as the expensive narrowing point,
6. final impact analysis only for matched companies.

If the initial match returns no company, the final impact node is skipped.

## Company Disclosure Impact Branch

![Company disclosure impact branch](open_source_assets/company_disclosure_branch_detail.png)

Company disclosures already map to one ticker. The branch skips policy-style RAG matching and runs:

1. source loading,
2. length gate and optional compression,
3. company-specific impact analysis,
4. wiki action decision,
5. optional wiki patch or rebuild after impact is saved.

Wiki decisions:

| Decision | Meaning |
|---|---|
| `no_update` | Save impact analysis only. This is the default for most routine announcements. |
| `small_update` | Apply a local wiki patch after impact analysis. |
| `force_rebuild` | Save impact analysis, then run reduced wiki rebuild from the updated document database. |

When one ticker has a `force_rebuild` marker in the same run, smaller wiki patches for that ticker are deferred because the rebuild supersedes them.

## Wiki Build Agents

The LLM company wiki is the durable knowledge object used by both impact branches. It captures business model, value-chain role, products, assets, projects, customers, suppliers, risks, financial drivers, aliases, and retrieval trigger terms.

### Reduced Builder

![Reduced wiki builder detail](open_source_assets/reduced_wiki_builder_detail.png)

Reduced is the default daily route. It is used after `force_rebuild` decisions, usually when a new annual report, prospectus, or major disclosure changes the best source set.

Core flow:

```text
document catalog
  -> source selection
  -> retrieval brainstormer
  -> hybrid source package
  -> reduced wiki writer
  -> archive / apply / manifest / index
```

Implementation entry points:

- [`daily_news_impact/wiki_build_agent/source_selection.py`](daily_news_impact/wiki_build_agent/source_selection.py)
- [`daily_news_impact/wiki_build_agent/reduced.py`](daily_news_impact/wiki_build_agent/reduced.py)
- [`daily_news_impact/force_rebuild.py`](daily_news_impact/force_rebuild.py)

### Full Builder Extension

Full wiki build is the optional high-budget route for first-time onboarding and manual deep review. It produces richer long-form wikis and demonstrates the most advanced agent architecture in this project: deterministic graph stages, ReAct-style planner subagents, shared evidence banks, critic/revision loops, and valuation calculators.

The daily one-click pipeline defaults to reduced rebuilds. Full builder details are documented separately:

- [`FULL_WIKI_BUILD_AGENT.md`](FULL_WIKI_BUILD_AGENT.md)
- [`WIKI_BUILD_AGENT.md`](WIKI_BUILD_AGENT.md)
- [`PROMPTS.md`](PROMPTS.md)

Offline plan inspection:

```powershell
python daily_news_impact_pipeline\show_wiki_build_plan.py --mode reduced --ticker 002796 --company 世嘉科技
python daily_news_impact_pipeline\show_wiki_build_plan.py --mode full --ticker 688668 --company 鼎通科技
```

## Outputs

Default run directory:

```text
reports/daily_news_impact_runs/<run_id>/
```

Important stage folders:

```text
run_config.json
run_summary.json
01_source_update/
02_preflight/
03_policy_impact/
04_company_disclosure_impact/
05_force_rebuild_wiki/
06_final_wiki_index/
07_daily_outputs/
```

Final daily outputs:

```text
07_daily_outputs/outputs/daily_all_company_actions.csv
07_daily_outputs/outputs/daily_all_company_actions.md
07_daily_outputs/outputs/daily_company_coverage.csv
07_daily_outputs/outputs/daily_company_coverage.md
07_daily_outputs/outputs/daily_all_impacts.md
07_daily_outputs/outputs/by_date/<YYYY-MM-DD>/company_actions.csv
07_daily_outputs/outputs/by_date/<YYYY-MM-DD>/company_coverage.csv
07_daily_outputs/outputs/daily_wiki_snapshots/<YYYY-MM-DD>/
```

The daily action table is the main product surface. It lets a reviewer see, per date and per company:

- source type and source id,
- title and URL,
- impact direction and certainty,
- impact nature,
- wiki action,
- wiki path and archive path,
- impact report path.

## Resume Behavior

Every stage writes:

```text
input.json
output.json
status.json
```

When the same `--run-id` is used again:

- completed and skipped stages reuse their outputs,
- failed stages rerun,
- force-rebuild batch stages reuse existing batch manifests and writer outputs when possible.

Disable resume:

```powershell
--no-resume
```

## Quality Constraints

- Impact analysis always runs before wiki patch or rebuild.
- Small patches and force rebuilds archive the previous wiki.
- Force rebuild uses the updated document database, so newly ingested annual reports can become the selected source.
- Policy news skips final impact when no company passes initial match.
- Company disclosure defaults to `no_update`; most announcements should not change the wiki.
- Final wiki index refresh should use `--device cuda` when available.

## Review Links

- [Reviewer Guide](REVIEW_GUIDE.md)
- [Prompt Contracts](PROMPTS.md)
- [Wiki Build Agent Design](WIKI_BUILD_AGENT.md)
- [Full Wiki Build Agent](FULL_WIKI_BUILD_AGENT.md)
- [Curated Examples](examples/README.md)
