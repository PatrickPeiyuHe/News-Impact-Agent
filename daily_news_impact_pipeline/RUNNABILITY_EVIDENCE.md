# Runnability And Evidence

This document explains how a reviewer can verify that the project is an executable pipeline rather than a static architecture write-up.

The open repository includes three kinds of evidence:

1. **Executable orchestration code**: CLI, stage runner, source adapters, impact adapters, force-rebuild path, reporting layer.
2. **Offline smoke-test artifacts**: commands that run without LLM calls and produce stage outputs.
3. **Curated real-run traces**: representative intermediate artifacts from policy impact, company disclosure impact, wiki patch, and wiki rebuild cases.

## Executable Entry Points

| File | What It Proves |
|---|---|
| [`run_daily_news_impact_one_click.py`](run_daily_news_impact_one_click.py) | One-click CLI entry point with date range, dry-run, resume, device, and branch controls |
| [`daily_news_impact/cli.py`](daily_news_impact/cli.py) | Stage orchestration, input/output folders, resume behavior, and run summary construction |
| [`daily_news_impact/source_update.py`](daily_news_impact/source_update.py) | Concrete crawler/parser/ingest/index command plan and adapter boundary |
| [`daily_news_impact/impact.py`](daily_news_impact/impact.py) | Policy and company-disclosure impact runner boundary |
| [`daily_news_impact/force_rebuild.py`](daily_news_impact/force_rebuild.py) | Reduced wiki rebuild execution path: brainstormer input, batch writer, archive/apply, manifest/index |
| [`daily_news_impact/reports.py`](daily_news_impact/reports.py) | Daily company action tables, coverage tables, impact summaries, and wiki snapshots |
| [`show_wiki_build_plan.py`](show_wiki_build_plan.py) | Offline inspection of reduced and full wiki build plans |

## Offline Smoke Test

The daily pipeline supports a dry-run mode that avoids live crawler writes and LLM calls while still building a real stage plan, running preflight checks when local databases exist, and writing daily output artifacts.

Command:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py `
  --date-from 2026-04-28 `
  --date-to 2026-04-28 `
  --run-id open_source_smoke_dryrun_20260428 `
  --dry-run `
  --skip-wiki-snapshot `
  --continue-on-error
```

Observed result from the local workspace:

| Field | Value |
|---|---|
| status | `completed` |
| policy docs in range | `12` |
| selected company disclosures | `38` |
| wiki database company count | `93` |
| final wiki markdown count | `41` |
| daily output stage | `completed` |

Curated smoke artifact:

- [`examples/smoke_runs/dry_run_20260428_summary.json`](examples/smoke_runs/dry_run_20260428_summary.json)

Standalone clone smoke artifact:

- [`examples/smoke_runs/standalone_repo_dry_run_summary.json`](examples/smoke_runs/standalone_repo_dry_run_summary.json)

The standalone artifact shows the open-source repo completing dry-run orchestration even when production databases are absent. In that mode, source-update commands are planned, branch summaries are written, and daily output files are created with zero live documents.

## Wiki Build Plan Smoke Test

The wiki build agent plan can be inspected without database access or LLM calls.

Command:

```powershell
python daily_news_impact_pipeline\show_wiki_build_plan.py --describe-modes
```

Observed modes:

- `reduced`: default daily source-package rebuild.
- `full`: high-budget research-loop build for onboarding and manual deep review.

Curated artifact:

- [`examples/smoke_runs/wiki_build_plan_modes.json`](examples/smoke_runs/wiki_build_plan_modes.json)

## Real-Run Intermediate Artifacts

The examples folder includes selected outputs from completed runs. These are the most useful review targets because they show model nodes, retrieval evidence, skip behavior, wiki update decisions, and final reports.

### Policy Matched Case

Directory:

- [`examples/news_impact/policy_matched_energy_carbon/`](examples/news_impact/policy_matched_energy_carbon/)

Evidence:

| File | Node |
|---|---|
| `working_news_text.md` | normalized source text |
| `02_analysis_gate_output.txt` | low-signal gate |
| `04_llm_compressor_output.txt` | source compressor |
| `05_brainstormer_round1_output.txt` | round-1 direct and semantic search plan |
| `06_round1_evidence_compact.txt` | compact rendered RAG evidence |
| `07_round2_search_planner_output.txt` | round-2 company-filtered search plan |
| `08_round2_evidence_compact.txt` | second-round evidence |
| `09_initial_match_output.txt` | matched companies and reasons |
| `10_impact_report.md` | final company impact analysis |

### Policy Skip Case

Directory:

- [`examples/news_impact/policy_no_initial_match/`](examples/news_impact/policy_no_initial_match/)

This case shows the token-saving path: the policy branch reaches `initial_match`, finds no concrete company path, and skips final company-by-company impact calls.

### Company Disclosure Cases

Directories:

- [`examples/news_impact/company_disclosure_no_update/`](examples/news_impact/company_disclosure_no_update/)
- [`examples/news_impact/company_disclosure_small_update/`](examples/news_impact/company_disclosure_small_update/)
- [`examples/news_impact/company_disclosure_force_rebuild/`](examples/news_impact/company_disclosure_force_rebuild/)

These cover the three wiki actions:

| Action | Evidence |
|---|---|
| `no_update` | impact analysis runs; wiki remains unchanged |
| `small_update` | impact analysis runs; wiki patch output, validation, and archive record are saved |
| `force_rebuild` | impact analysis runs; reduced rebuild is deferred to the rebuild stage |

### Reduced Wiki Rebuild

Directory:

- [`examples/wiki_rebuild/reduced_force_rebuild_002796/`](examples/wiki_rebuild/reduced_force_rebuild_002796/)

Evidence:

| File | Stage |
|---|---|
| `01_brainstormer_inputs_summary.json` | ticker selection and input construction summary |
| `02_brainstormer_output.json` | retrieval terms and selected source hints |
| `03_writer_model_input.md` | deterministic source package passed to writer |
| `05_writer_output.md` | rebuilt reduced wiki |
| `05_writer_usage.json` | batch writer token usage |
| `06_apply_rebuild_summary.json` | archive/apply/index summary |

### Daily User-Facing Outputs

Directory:

- [`examples/daily_outputs/`](examples/daily_outputs/)

Evidence:

| File | Meaning |
|---|---|
| `daily_all_company_actions.csv` | all policy, disclosure, and wiki actions in the sample range |
| `daily_company_coverage.csv` | fixed company coverage table, including no-action companies |
| `2026-04-27/company_actions.csv` | one-day user review table |
| `2026-04-27/company_coverage.csv` | one-day coverage table |

## What Requires Production Access

The open repo keeps production dependencies behind adapters:

| Dependency | Boundary |
|---|---|
| live crawler credentials and state | `source_update.py` command adapters |
| local document databases | preflight and source update stages |
| private LLM provider keys | impact and wiki rebuild runners |
| raw provider request/response payloads | excluded from public examples |
| internal production runner modules | called through explicit adapter paths |

The public code still shows where those dependencies attach and what outputs each stage must produce.

## Reviewer Verification Path

A reviewer can verify the project in three steps:

1. Run `python daily_news_impact_pipeline\run_daily_news_impact_one_click.py --help` to inspect CLI controls.
2. Run the dry-run command above to produce a stage plan and daily output files without LLM calls.
3. Inspect the curated real-run traces in `examples/` to verify the model-node behavior and intermediate artifacts.

This combination gives both executable proof and behavioral evidence.
