from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Any

from .utils import ROOT, iter_dates, read_json, safe_rel, write_csv, write_json, write_md_table, write_text


WIKI_COLLECTION_DIR = ROOT / "reports" / "company_markdown_wiki_final_collection_20260427"


ACTION_COLUMNS = [
    "date",
    "ticker",
    "company",
    "source_type",
    "source_id",
    "title",
    "action_type",
    "impact_direction",
    "certainty",
    "impact_nature",
    "wiki_action",
    "wiki_path",
    "archive_path",
    "impact_report_path",
    "url",
    "notes",
]

COVERAGE_COLUMNS = [
    "date",
    "ticker",
    "company",
    "has_action",
    "action_count",
    "policy_impact_count",
    "company_disclosure_impact_count",
    "wiki_change_count",
    "wiki_path",
    "action_titles",
]


def _resolve(path_text: str | None) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def _read_company_decision(disclosure_dir_text: str | None) -> dict[str, Any]:
    disclosure_dir = _resolve(disclosure_dir_text)
    if not disclosure_dir:
        return {}
    path = disclosure_dir / "04_company_disclosure_impact" / "wiki_update_decision.json"
    if path.exists():
        try:
            return read_json(path)
        except (OSError, json.JSONDecodeError):
            return {}
    output_path = disclosure_dir / "04_company_disclosure_impact" / "output.json"
    if output_path.exists():
        try:
            payload = read_json(output_path)
            decision = payload.get("decision")
            return decision if isinstance(decision, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def _company_disclosure_actions(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in summary.get("disclosure_summaries", []):
        if item.get("status") != "completed":
            continue
        decision = _read_company_decision(item.get("disclosure_dir"))
        wiki_action = str(item.get("wiki_update_decision") or decision.get("wiki_update_decision") or "")
        applied = bool(item.get("wiki_update_applied"))
        deferred = bool(item.get("wiki_update_deferred"))
        action_type = "impact_analysis"
        if applied:
            action_type = "impact_analysis_and_wiki_patch"
        elif deferred:
            action_type = "impact_analysis_and_deferred_wiki_patch"
        elif wiki_action == "force_rebuild":
            action_type = "impact_analysis_and_force_rebuild_marker"
        rows.append(
            {
                "date": item.get("publish_date") or "",
                "ticker": item.get("ticker") or "",
                "company": item.get("company") or "",
                "source_type": "company_disclosure",
                "source_id": item.get("doc_id") or "",
                "title": item.get("title") or "",
                "action_type": action_type,
                "impact_direction": decision.get("impact_direction") or "",
                "certainty": decision.get("certainty") or "",
                "impact_nature": decision.get("impact_nature") or "",
                "wiki_action": wiki_action,
                "wiki_path": item.get("updated_wiki_path") or "",
                "archive_path": item.get("archived_wiki_path") or "",
                "impact_report_path": item.get("impact_report_path") or "",
                "url": item.get("url") or "",
                "notes": item.get("wiki_update_deferred_reason") or item.get("wiki_update_reason") or "",
            }
        )
    return rows


def _policy_actions(policy_summary: dict[str, Any]) -> list[dict[str, Any]]:
    run_dir = _resolve(policy_summary.get("run_dir"))
    if not run_dir:
        return []
    path = run_dir / "final_impacted_stocks.csv"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "date": row.get("publish_date", ""),
                    "ticker": row.get("ticker", ""),
                    "company": row.get("company", ""),
                    "source_type": "policy",
                    "source_id": row.get("policy_id", ""),
                    "title": row.get("policy_title", ""),
                    "action_type": "impact_analysis",
                    "impact_direction": "",
                    "certainty": "",
                    "impact_nature": "",
                    "wiki_action": "no_update",
                    "wiki_path": "",
                    "archive_path": "",
                    "impact_report_path": row.get("impact_report_path", ""),
                    "url": row.get("policy_url", ""),
                    "notes": row.get("issuer", ""),
                }
            )
    return rows


def _rebuild_actions(force_summary: dict[str, Any], date_to: str) -> list[dict[str, Any]]:
    apply_payload = force_summary.get("apply") if isinstance(force_summary, dict) else {}
    applied = apply_payload.get("applied") if isinstance(apply_payload, dict) else []
    rows: list[dict[str, Any]] = []
    for item in applied or []:
        rows.append(
            {
                "date": date_to,
                "ticker": item.get("ticker", ""),
                "company": item.get("company", ""),
                "source_type": "wiki_rebuild",
                "source_id": "",
                "title": "force rebuild reduced company wiki",
                "action_type": "wiki_rebuild_applied",
                "impact_direction": "",
                "certainty": "",
                "impact_nature": "",
                "wiki_action": "force_rebuild",
                "wiki_path": item.get("target_path", ""),
                "archive_path": ";".join(item.get("archive_paths") or []),
                "impact_report_path": "",
                "url": "",
                "notes": f"previous_file={item.get('previous_file','')}; writer_output={item.get('writer_output','')}",
            }
        )
    return rows


def _copy_if_exists(source: Path | None, target: Path) -> None:
    if source and source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _manifest_companies() -> list[dict[str, str]]:
    manifest = WIKI_COLLECTION_DIR / "manifest.csv"
    if not manifest.exists():
        return []
    companies: list[dict[str, str]] = []
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            ticker = str(row.get("ticker") or "").strip().zfill(6)
            if not ticker:
                continue
            companies.append(
                {
                    "ticker": ticker,
                    "company": str(row.get("company") or ""),
                    "wiki_path": str(WIKI_COLLECTION_DIR / str(row.get("file") or "")),
                }
            )
    companies.sort(key=lambda item: item["ticker"])
    return companies


def _coverage_rows_for_day(day: str, actions: list[dict[str, Any]], companies: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_ticker: dict[str, list[dict[str, Any]]] = {}
    for action in actions:
        if str(action.get("date") or "")[:10] != day:
            continue
        ticker = str(action.get("ticker") or "").strip().zfill(6)
        if ticker:
            by_ticker.setdefault(ticker, []).append(action)
    rows: list[dict[str, Any]] = []
    for company in companies:
        ticker = company["ticker"]
        items = by_ticker.get(ticker, [])
        wiki_changes = [item for item in items if str(item.get("wiki_action") or "") in {"small_update", "force_rebuild"} and str(item.get("action_type") or "") != "impact_analysis"]
        rows.append(
            {
                "date": day,
                "ticker": ticker,
                "company": company["company"],
                "has_action": bool(items),
                "action_count": len(items),
                "policy_impact_count": len([item for item in items if item.get("source_type") == "policy"]),
                "company_disclosure_impact_count": len([item for item in items if item.get("source_type") == "company_disclosure"]),
                "wiki_change_count": len(wiki_changes),
                "wiki_path": company["wiki_path"],
                "action_titles": "；".join(str(item.get("title") or "") for item in items[:12]),
            }
        )
    return rows


def write_wiki_snapshots(*, date_from: str, date_to: str, output_root: Path) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for day in iter_dates(date_from, date_to):
        snapshot_dir = output_root / "daily_wiki_snapshots" / day
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        copied = 0
        manifest = WIKI_COLLECTION_DIR / "manifest.csv"
        if manifest.exists():
            shutil.copy2(manifest, snapshot_dir / "manifest.csv")
        for md in sorted(WIKI_COLLECTION_DIR.glob("*.md")):
            shutil.copy2(md, snapshot_dir / md.name)
            copied += 1
        write_json(
            snapshot_dir / "snapshot_meta.json",
            {
                "date": day,
                "source_collection_dir": safe_rel(WIKI_COLLECTION_DIR),
                "wiki_count": copied,
                "note": "Snapshot was captured after the one-click run completed. For date ranges, run one date at a time when historical end-of-day wiki states must differ by date.",
            },
        )
        snapshots.append({"date": day, "snapshot_dir": safe_rel(snapshot_dir), "wiki_count": copied})
    return snapshots


def build_daily_outputs(
    *,
    output_root: Path,
    date_from: str,
    date_to: str,
    policy_summary: dict[str, Any] | None,
    company_summary: dict[str, Any] | None,
    force_rebuild_summary: dict[str, Any] | None,
    create_wiki_snapshot: bool = True,
) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    actions: list[dict[str, Any]] = []
    if policy_summary:
        actions.extend(_policy_actions(policy_summary))
    if company_summary:
        actions.extend(_company_disclosure_actions(company_summary))
    if force_rebuild_summary:
        actions.extend(_rebuild_actions(force_rebuild_summary, date_to))
    actions.sort(key=lambda row: (str(row.get("date") or ""), str(row.get("ticker") or ""), str(row.get("source_type") or ""), str(row.get("source_id") or "")))

    write_csv(output_root / "daily_all_company_actions.csv", actions, ACTION_COLUMNS)
    write_md_table(output_root / "daily_all_company_actions.md", actions, ACTION_COLUMNS, max_chars=360)
    by_date_dir = output_root / "by_date"
    companies = _manifest_companies()
    all_coverage_rows: list[dict[str, Any]] = []
    for day in iter_dates(date_from, date_to):
        daily_rows = [row for row in actions if str(row.get("date") or "")[:10] == day]
        day_dir = by_date_dir / day
        write_csv(day_dir / "company_actions.csv", daily_rows, ACTION_COLUMNS)
        write_md_table(day_dir / "company_actions.md", daily_rows, ACTION_COLUMNS, max_chars=360)
        coverage_rows = _coverage_rows_for_day(day, actions, companies)
        all_coverage_rows.extend(coverage_rows)
        write_csv(day_dir / "company_coverage.csv", coverage_rows, COVERAGE_COLUMNS)
        write_md_table(day_dir / "company_coverage.md", coverage_rows, COVERAGE_COLUMNS, max_chars=360)
    write_csv(output_root / "daily_company_coverage.csv", all_coverage_rows, COVERAGE_COLUMNS)
    write_md_table(output_root / "daily_company_coverage.md", all_coverage_rows, COVERAGE_COLUMNS, max_chars=360)

    report_parts: list[str] = []
    for label, summary in (("Policy", policy_summary), ("Company Disclosure", company_summary)):
        if not summary:
            continue
        run_dir = _resolve(summary.get("run_dir"))
        report_path = run_dir / "impact_report_all.md" if run_dir else None
        if report_path and report_path.exists():
            report_parts.append(f"# {label} Impact\n\n" + report_path.read_text(encoding="utf-8", errors="ignore").strip())
    write_text(output_root / "daily_all_impacts.md", "\n\n".join(part for part in report_parts if part).strip() + ("\n" if report_parts else ""))
    snapshots = write_wiki_snapshots(date_from=date_from, date_to=date_to, output_root=output_root) if create_wiki_snapshot else []

    summary = {
        "status": "completed",
        "date_from": date_from,
        "date_to": date_to,
        "action_count": len(actions),
        "paths": {
            "daily_all_company_actions_csv": safe_rel(output_root / "daily_all_company_actions.csv"),
            "daily_all_company_actions_md": safe_rel(output_root / "daily_all_company_actions.md"),
            "daily_company_coverage_csv": safe_rel(output_root / "daily_company_coverage.csv"),
            "daily_company_coverage_md": safe_rel(output_root / "daily_company_coverage.md"),
            "daily_all_impacts_md": safe_rel(output_root / "daily_all_impacts.md"),
            "by_date_dir": safe_rel(by_date_dir),
        },
        "wiki_snapshots": snapshots,
    }
    write_json(output_root / "daily_outputs_summary.json", summary)
    return summary
