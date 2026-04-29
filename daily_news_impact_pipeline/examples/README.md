# Examples

This directory contains curated outputs from real pipeline runs. The goal is to show the project design and execution trace without requiring a live database, crawler, or LLM API call.

The examples are intentionally selective. They keep representative outputs and key intermediate artifacts, while excluding raw API responses and request payloads.

## Directory Map

```text
examples/
  wikis/
    full/                  # sample full wikis
    reduced/               # sample reduced wikis
  news_impact/
    policy_matched_energy_carbon/
    policy_no_initial_match/
    company_disclosure_small_update/
    company_disclosure_force_rebuild/
    company_disclosure_no_update/
  wiki_rebuild/
    reduced_force_rebuild_002796/
  daily_outputs/
    daily_all_company_actions.csv
    daily_company_coverage.csv
    2026-04-27/
```

## Wiki Samples

| Path | Type | Why It Is Included |
|---|---|---|
| `wikis/full/603162__full_wiki.md` | full wiki | Long-form company wiki sample with richer business context |
| `wikis/full/688668__full_wiki.md` | full wiki | Full wiki sample for a component company with AI/data-center relevance |
| `wikis/reduced/002796__reduced_wiki.md` | reduced wiki | Rebuilt daily-pipeline wiki after annual-report force rebuild |
| `wikis/reduced/300504__reduced_wiki.md` | reduced wiki | Reduced wiki after a sequence of small patches |
| `wikis/reduced/300308__reduced_wiki.md` | reduced wiki | Compact wiki for a high-relevance optical module company |

## Policy News Impact Examples

### `policy_matched_energy_carbon/`

This is a matched policy case:

- Policy title: `国家发展改革委有关负责同志和相关专家解读——更高水平更高质量做好节能降碳工作`
- Date: `2026-04-26`
- Result: initial match found companies in the 41-stock wiki pool, then final impact analysis was produced.

Key files:

| File | Node |
|---|---|
| `working_news_text.md` | normalized policy text used downstream |
| `02_analysis_gate_output.txt` | low-signal / usable-news gate |
| `03_length_gate_output.json` | compression decision |
| `04_llm_compressor_output.txt` | compressed policy text when needed |
| `05_brainstormer_round1_output.txt` | round-1 direct/semantic search strategy |
| `06_round1_evidence_compact.txt` | compact rendered evidence returned by hybrid search |
| `07_round2_search_planner_output.txt` | round-2 company-filtered search plan |
| `08_round2_evidence_compact.txt` | second-round compact evidence |
| `09_initial_match_output.txt` | initial matched companies and reasons |
| `10_impact_report.md` | final policy impact analysis |

### `policy_no_initial_match/`

This is a clean skip case:

- Policy title: `中共中央办公厅 国务院办公厅关于加强新就业群体服务管理的意见`
- Date: `2026-04-26`
- Result: analysis and search completed, but `initial_match` found no concrete company path in the 41-stock wiki pool. The pipeline skipped final GPT impact analysis.

This sample shows the token-saving behavior: no matched company means no expensive company-by-company final impact call.

## Company Disclosure Impact Examples

Company disclosure is one-to-one with a ticker, so it does not run the policy RAG initial-match loop.

### `company_disclosure_small_update/`

Example:

- Company: `300504 天邑股份`
- Disclosure: `2026年一季度报告`
- Result: impact analysis was produced, then the wiki update node generated a small wiki patch.

Key files:

| File | Node |
|---|---|
| `working_disclosure_text.md` | normalized disclosure text |
| `02_length_gate_output.json` | compression decision |
| `03_llm_compressor_output.txt` | compact disclosure text |
| `04_company_disclosure_impact_output.txt` | impact analysis and wiki decision |
| `04_wiki_update_decision.json` | machine-readable wiki action |
| `05_wiki_update_output.md` | patched wiki |
| `05_applied_update.json` | apply result |
| `05_update_validation.json` | post-update validation |
| `05_wiki_archive_record.json` | old-wiki archive record |

### `company_disclosure_force_rebuild/`

Example:

- Company: `002796 世嘉科技`
- Disclosure: `2025年年度报告`
- Result: impact analysis ran first, then the disclosure was marked `force_rebuild`. The actual rebuild is handled by the reduced wiki builder in `wiki_rebuild/reduced_force_rebuild_002796/`.

### `company_disclosure_no_update/`

Example:

- Company: `002796 世嘉科技`
- Disclosure: `关于举行2025年度网上业绩说明会的公告`
- Result: impact analysis ran, and the wiki decision was `no_update`.

This sample shows the expected default posture: most announcements should not modify the wiki.

## Wiki Rebuild Example

`wiki_rebuild/reduced_force_rebuild_002796/` shows a reduced wiki rebuild triggered by an annual report.

Key files:

| File | Stage |
|---|---|
| `01_brainstormer_inputs_summary.json` | selected tickers and input construction summary |
| `02_brainstormer_output.json` | retrieval terms, semantic queries, optional source selections |
| `03_writer_model_input.md` | final source package passed to the writer |
| `05_writer_output.md` | rebuilt reduced wiki |
| `05_writer_usage.json` | batch writer token usage |
| `06_apply_rebuild_summary.json` | archive/apply/index summary |

## Daily Output Examples

`daily_outputs/` shows the final user-facing output shape.

| File | Meaning |
|---|---|
| `daily_all_company_actions.csv` | all policy, disclosure, and wiki actions in the sample date range |
| `daily_company_coverage.csv` | fixed 41-company coverage table per date, including no-action companies |
| `2026-04-27/company_actions.csv` | one-day action table |
| `2026-04-27/company_coverage.csv` | one-day 41-company coverage table |

The daily tables are the main product surface. A user can open them to see which companies had impact analysis, which had wiki updates, and which had no action.
