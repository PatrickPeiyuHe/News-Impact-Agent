from __future__ import annotations

from pathlib import Path
from typing import Any

from .preflight import daily_preflight
from .utils import ROOT, now_iso, safe_rel, write_json, write_text


def _impact_run_dir(kind: str, run_id: str) -> Path:
    if kind == "policy":
        return ROOT / "reports" / "policy_news_impact_runs" / run_id
    if kind == "company_disclosure":
        return ROOT / "reports" / "company_disclosure_impact_runs" / run_id
    raise ValueError(f"unknown_impact_kind:{kind}")


def _write_dry_run_report(run_dir: Path, title: str, payload: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "run_summary.json", payload)
    lines = [
        f"# {title}",
        "",
        "This is a dry-run artifact. No LLM calls were made.",
        "",
        f"- status: `{payload.get('status')}`",
        f"- date_from: `{payload.get('date_from')}`",
        f"- date_to: `{payload.get('date_to')}`",
    ]
    if "policy_count" in payload:
        lines.append(f"- policy_count: `{payload.get('policy_count')}`")
    if "selected_disclosure_count" in payload:
        lines.append(f"- selected_disclosure_count: `{payload.get('selected_disclosure_count')}`")
    write_text(run_dir / "impact_report_all.md", "\n".join(lines).strip() + "\n")


def run_policy_impact(
    *,
    date_from: str,
    date_to: str,
    run_id: str,
    max_impact_companies: int,
    dry_run: bool,
    continue_on_error: bool,
    resume: bool,
) -> dict[str, Any]:
    if dry_run:
        run_dir = _impact_run_dir("policy", run_id)
        preflight = daily_preflight(date_from, date_to)
        policy_count = preflight.get("databases", {}).get("policy_docs_in_range")
        summary = {
            "run_id": run_id,
            "run_dir": safe_rel(run_dir),
            "date_from": date_from,
            "date_to": date_to,
            "policy_count": int(policy_count or 0),
            "selected_policies_path": safe_rel(run_dir / "selected_policies.json"),
            "status": "dry_run_completed",
            "dry_run": True,
            "finished_at": now_iso(),
        }
        write_json(run_dir / "selected_policies.json", {"dry_run": True, "policy_count": summary["policy_count"], "policies": []})
        _write_dry_run_report(run_dir, "Policy Impact Dry Run", summary)
        return summary

    from comm_profile.news_impact.date_range_runner import run_policy_news_impact_date_range

    return run_policy_news_impact_date_range(
        date_from=date_from,
        date_to=date_to,
        run_id=run_id,
        resume=resume,
        max_impact_companies=max_impact_companies,
        dry_run=dry_run,
        continue_on_error=continue_on_error,
    )


def run_company_disclosure_impact(
    *,
    date_from: str,
    date_to: str,
    run_id: str,
    scope: str,
    wiki_update_mode: str,
    dry_run: bool,
    continue_on_error: bool,
    resume: bool,
    index_device: str,
    rebuild_index_after_apply: bool,
) -> dict[str, Any]:
    if dry_run:
        run_dir = _impact_run_dir("company_disclosure", run_id)
        preflight = daily_preflight(date_from, date_to)
        disclosure_count = preflight.get("databases", {}).get("company_documents_in_range")
        summary = {
            "run_id": run_id,
            "run_dir": safe_rel(run_dir),
            "date_from": date_from,
            "date_to": date_to,
            "selected_disclosure_count": int(disclosure_count or 0),
            "disclosure_summaries": [],
            "status": "dry_run_completed",
            "dry_run": True,
            "finished_at": now_iso(),
        }
        write_json(run_dir / "selected_disclosures.json", {"dry_run": True, "selected_disclosure_count": summary["selected_disclosure_count"], "disclosures": []})
        _write_dry_run_report(run_dir, "Company Disclosure Impact Dry Run", summary)
        return summary

    from comm_profile.news_impact.company_disclosure_runner import run_company_disclosure_impact_date_range

    return run_company_disclosure_impact_date_range(
        date_from=date_from,
        date_to=date_to,
        run_id=run_id,
        scope=scope,
        resume=resume,
        wiki_update_mode=wiki_update_mode,
        dry_run=dry_run,
        continue_on_error=continue_on_error,
        index_device=index_device,
        rebuild_index_after_apply=rebuild_index_after_apply,
    )


def force_rebuild_tickers_from_company_summary(summary: dict[str, Any]) -> list[str]:
    tickers = {
        str(item.get("ticker") or "").strip().zfill(6)
        for item in summary.get("disclosure_summaries", [])
        if str(item.get("wiki_update_decision") or "") == "force_rebuild"
    }
    tickers.discard("")
    return sorted(tickers)


def resolve_run_path(path_text: str | None) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def compact_impact_location(summary: dict[str, Any]) -> dict[str, Any]:
    run_dir = resolve_run_path(summary.get("run_dir"))
    return {
        "run_dir": safe_rel(run_dir) if run_dir else "",
        "run_summary": safe_rel(run_dir / "run_summary.json") if run_dir else "",
        "impact_report_all": safe_rel(run_dir / "impact_report_all.md") if run_dir else "",
        "status": summary.get("status"),
    }
