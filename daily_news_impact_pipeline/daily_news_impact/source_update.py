from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .utils import ROOT, load_csv, project_python, run_command, safe_rel, write_json, write_rows_csv_like


COMPANY_CORPUS_POLICY_V2 = "company_corpus_v2"

SOURCE_CATEGORIES = {"policy", "cninfo", "sina", "eastmoney", "tushare"}
CONTROL_CATEGORIES = {"ingest", "index"}
CNINFO_FAMILIES = {
    "announcement",
    "annual_report",
    "semiannual_report",
    "quarterly_report_q1",
    "quarterly_report_q3",
    "prospectus",
    "prospectus_related",
}
EASTMONEY_FAMILIES = {"stock_report"}
DOC_FAMILY_ALIASES = {
    "announcement": "announcement",
    "announcements": "announcement",
    "公告": "announcement",
    "annual": "annual_report",
    "annual_report": "annual_report",
    "年报": "annual_report",
    "年度报告": "annual_report",
    "semiannual": "semiannual_report",
    "semiannual_report": "semiannual_report",
    "半年报": "semiannual_report",
    "半年度报告": "semiannual_report",
    "quarterly": "quarterly_report_q1,quarterly_report_q3",
    "quarterly_report": "quarterly_report_q1,quarterly_report_q3",
    "季报": "quarterly_report_q1,quarterly_report_q3",
    "一季报": "quarterly_report_q1",
    "三季报": "quarterly_report_q3",
    "q1": "quarterly_report_q1",
    "q3": "quarterly_report_q3",
    "quarterly_report_q1": "quarterly_report_q1",
    "quarterly_report_q3": "quarterly_report_q3",
    "prospectus": "prospectus,prospectus_related",
    "招股书": "prospectus,prospectus_related",
    "招股说明书": "prospectus,prospectus_related",
    "stock_report": "stock_report",
    "研报": "stock_report",
}
ALL_CATEGORIES = ["policy", "cninfo", "sina", "eastmoney", "tushare", "ingest", "index"]


@dataclass(frozen=True)
class SourceUpdateConfig:
    start_date: str
    end_date: str
    output_root: Path
    targets_csv: Path = ROOT / "configs" / "targets.csv"
    tickers: tuple[str, ...] = ()
    categories: tuple[str, ...] = ("policy", "cninfo", "eastmoney", "ingest", "index")
    workers: int = 2
    device: str = "auto"
    force_reparse: bool = False
    policy_with_embedding: bool = False
    sina_only_missing_orgid: bool = True
    dry_run: bool = False


def _cn_since(start_date: str) -> str:
    return f"{start_date}T00:00:00+08:00"


def _cn_until(end_date: str) -> str:
    return f"{end_date}T23:59:59+08:00"


def _lookback_days(start_date: str, end_date: str) -> int:
    return max(1, (date.fromisoformat(end_date) - date.fromisoformat(start_date)).days + 1)


def _normalize_ticker(ticker: str) -> str:
    digits = "".join(ch for ch in str(ticker or "") if ch.isdigit())
    return digits.zfill(6) if digits else ""


def _normalize_categories(raw_categories: tuple[str, ...]) -> tuple[set[str], set[str]]:
    source_and_control: set[str] = set()
    doc_families: set[str] = set()
    for raw in raw_categories:
        token = str(raw or "").strip()
        if not token:
            continue
        lower = token.lower()
        if lower == "all" or token == "全部":
            source_and_control.update(ALL_CATEGORIES)
            continue
        if lower in SOURCE_CATEGORIES or lower in CONTROL_CATEGORIES:
            source_and_control.add(lower)
            continue
        if lower in DOC_FAMILY_ALIASES:
            doc_families.update(item for item in DOC_FAMILY_ALIASES[lower].split(",") if item)
            continue
        if token in DOC_FAMILY_ALIASES:
            doc_families.update(item for item in DOC_FAMILY_ALIASES[token].split(",") if item)
            continue
        raise ValueError(f"unsupported_category:{token}")

    if doc_families:
        if doc_families & CNINFO_FAMILIES:
            source_and_control.add("cninfo")
        if doc_families & EASTMONEY_FAMILIES:
            source_and_control.add("eastmoney")
        source_and_control.update({"ingest", "index"})
    return source_and_control, doc_families


def _selected_targets(config: SourceUpdateConfig) -> tuple[list[dict[str, str]], list[str]]:
    rows = load_csv(config.targets_csv)
    wanted = {_normalize_ticker(item) for item in config.tickers if _normalize_ticker(item)}
    if wanted:
        rows = [row for row in rows if _normalize_ticker(row.get("ticker", "")) in wanted]
    if not rows:
        raise ValueError("no_target_rows_selected")
    tickers = [_normalize_ticker(row.get("ticker", "")) for row in rows]
    return rows, tickers


def build_source_update_plan(config: SourceUpdateConfig) -> dict[str, Any]:
    selected_rows, selected_tickers = _selected_targets(config)
    selected_targets_csv = config.output_root / "selected_targets.csv"
    write_rows_csv_like(selected_targets_csv, selected_rows)

    source_and_control, doc_families = _normalize_categories(config.categories)
    py = project_python()
    stages: list[dict[str, Any]] = []
    notes: list[str] = []

    if "policy" in source_and_control:
        stages.append(
            {
                "name": "01_policy",
                "command": [py, "scripts/update_policy_corpus.py", "--force-start-date", config.start_date, "--force-end-date", config.end_date],
            }
        )
        parse_cmd = [py, "scripts/parse_policy_documents.py", "--start-date", config.start_date, "--end-date", config.end_date]
        if config.force_reparse:
            parse_cmd.append("--force")
        if not config.policy_with_embedding:
            parse_cmd.append("--no-embedding")
            notes.append("policy parse uses --no-embedding by default; company disclosures and research still keep embedding during wiki ingest/index.")
        stages.append({"name": "01b_policy_parse", "command": parse_cmd})

    if "cninfo" in source_and_control:
        stages.append(
            {
                "name": "02_cninfo",
                "command": [
                    py,
                    "scripts/update_cninfo_corpus.py",
                    "--targets-csv",
                    str(selected_targets_csv),
                    "--docs-dir",
                    "data/docs",
                    "--state-root",
                    "data/cninfo",
                    "--db-path",
                    "data/catalog/document_catalog.sqlite",
                    "--force-since-utc",
                    _cn_since(config.start_date),
                    "--force-until-utc",
                    _cn_until(config.end_date),
                ],
            }
        )

    if "sina" in source_and_control:
        command = [
            py,
            "scripts/bootstrap_sina_announcements.py",
            "--targets-csv",
            str(selected_targets_csv),
            "--docs-dir",
            "data/docs",
            "--coverage-dir",
            str(config.output_root / "03_sina" / "coverage"),
            "--reference-date",
            config.end_date,
            "--announcement-lookback-days",
            str(_lookback_days(config.start_date, config.end_date)),
        ]
        command.append("--only-missing-orgid" if config.sina_only_missing_orgid else "--no-only-missing-orgid")
        stages.append({"name": "03_sina", "command": command})
        notes.append("Sina is retained as a coverage fallback and currently does not upsert to the main catalog by itself.")

    if "eastmoney" in source_and_control:
        stages.append(
            {
                "name": "04_eastmoney",
                "command": [
                    py,
                    "scripts/update_eastmoney_reports.py",
                    "--targets-csv",
                    str(selected_targets_csv),
                    "--reports-root",
                    "data/research_reports",
                    "--state-root",
                    "data/research_reports",
                    "--db-path",
                    "data/research_reports/catalog/research_report_catalog.sqlite",
                    "--force-since-utc",
                    _cn_since(config.start_date),
                    "--force-until-utc",
                    _cn_until(config.end_date),
                ],
            }
        )

    should_ingest = "ingest" in source_and_control and bool({"cninfo", "eastmoney"} & source_and_control or doc_families)
    if should_ingest:
        command = [
            py,
            "scripts/rebuild_wiki_database.py",
            "--db-path",
            "data/wiki/wiki_agent.sqlite",
            "--parse-root",
            "data/wiki/parse_outputs",
            "--targets-csv",
            str(selected_targets_csv),
            "--tickers",
            *selected_tickers,
            "--workers",
            str(config.workers),
            "--device",
            config.device,
            "--corpus-policy",
            COMPANY_CORPUS_POLICY_V2,
            "--reference-date",
            config.end_date,
            "--prune-unselected-for-tickers",
            "--summary-path",
            str(config.output_root / "05_wiki_ingest" / "summary.json"),
        ]
        if doc_families:
            command.extend(["--doc-families", ",".join(sorted(doc_families))])
        if config.force_reparse:
            command.append("--force-reparse")
        stages.append({"name": "05_wiki_ingest", "command": command})

    if "index" in source_and_control and should_ingest:
        stages.append(
            {
                "name": "06_index_preflight",
                "command": [
                    py,
                    "scripts/wiki_db_preflight.py",
                    "--tickers",
                    *selected_tickers,
                    "--ensure-index",
                    "--out-json",
                    str(config.output_root / "06_index_preflight" / "preflight.json"),
                ],
            }
        )

    if "tushare" in source_and_control:
        stages.append(
            {
                "name": "07_tushare",
                "command": [
                    py,
                    "scripts/sync_tushare_valuation_data.py",
                    "--tickers",
                    *selected_tickers,
                    "--as-of-date",
                    config.end_date.replace("-", ""),
                    "--report-dir",
                    str(config.output_root / "07_tushare"),
                ],
            }
        )

    return {
        "start_date": config.start_date,
        "end_date": config.end_date,
        "source_and_control_categories": sorted(source_and_control),
        "doc_families": sorted(doc_families),
        "selected_targets_csv": safe_rel(selected_targets_csv),
        "tickers": selected_tickers,
        "notes": notes,
        "stages": stages,
    }


def run_source_update(config: SourceUpdateConfig, stage_dir: Path) -> dict[str, Any]:
    config.output_root.mkdir(parents=True, exist_ok=True)
    plan = build_source_update_plan(config)
    write_json(config.output_root / "execution_plan.json", plan)
    if config.dry_run:
        result = {"status": "completed", "dry_run": True, "output_root": safe_rel(config.output_root), "plan": plan}
        write_json(config.output_root / "run_status.json", result)
        return result

    results: list[dict[str, Any]] = []
    for item in plan["stages"]:
        command_result = run_command(command=list(item["command"]), cwd=ROOT, stage_dir=config.output_root / str(item["name"]))
        results.append(command_result.__dict__)
    result = {"status": "completed", "dry_run": False, "output_root": safe_rel(config.output_root), "plan": plan, "results": results}
    write_json(config.output_root / "run_status.json", result)
    return result
