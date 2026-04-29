from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import ROOT, safe_rel


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
