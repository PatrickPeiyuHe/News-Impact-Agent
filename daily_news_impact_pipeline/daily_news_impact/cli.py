from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .force_rebuild import ForceRebuildConfig, run_force_rebuild
from .impact import compact_impact_location, force_rebuild_tickers_from_company_summary, run_company_disclosure_impact, run_policy_impact
from .preflight import daily_preflight
from .reports import build_daily_outputs
from .source_update import SourceUpdateConfig, run_source_update
from .utils import ROOT, StageRunner, iter_dates, now_compact, now_iso, parse_ymd, safe_rel, write_json


DEFAULT_RUN_ROOT = ROOT / "reports" / "daily_news_impact_runs"


@dataclass(frozen=True)
class DailyPipelineConfig:
    date_from: str
    date_to: str
    run_id: str
    run_root: Path
    targets_csv: Path
    tickers: tuple[str, ...]
    source_categories: tuple[str, ...]
    device: str
    workers: int
    dry_run: bool
    resume: bool
    continue_on_error: bool
    skip_source_update: bool
    skip_policy_impact: bool
    skip_company_disclosure_impact: bool
    skip_force_rebuild: bool
    skip_final_index: bool
    skip_wiki_snapshot: bool
    policy_max_impact_companies: int
    company_scope: str
    company_wiki_update_mode: str
    force_rebuild_poll_seconds: float
    force_rebuild_timeout_seconds: float

    @property
    def run_dir(self) -> Path:
        return self.run_root / self.run_id


def _default_run_id(date_from: str, date_to: str) -> str:
    left = date_from.replace("-", "")
    right = date_to.replace("-", "")
    return f"daily_news_impact_{left}_{right}_{now_compact()}"


def _stage_skip(stage_dir: Path, reason: str) -> dict[str, Any]:
    return {"status": "skipped", "reason": reason, "stage_dir": safe_rel(stage_dir)}


def _run_final_index(*, config: DailyPipelineConfig, company_summary: dict[str, Any] | None, force_summary: dict[str, Any] | None) -> dict[str, Any]:
    if config.dry_run:
        return {"status": "completed", "dry_run": True}
    if config.skip_final_index:
        return {"status": "skipped", "reason": "skip_final_index"}
    force_index = (((force_summary or {}).get("apply") or {}).get("index_rebuild") or {})
    if force_index:
        return {"status": "skipped", "reason": "force_rebuild_stage_already_rebuilt_index", "index_rebuild": force_index}
    company_updates = int((company_summary or {}).get("wiki_updates_applied") or 0)
    if company_updates <= 0:
        return {"status": "skipped", "reason": "no_wiki_changes"}
    from comm_profile.news_impact.wiki_index import build_news_impact_wiki_index

    collection_dir = ROOT / "reports" / "company_markdown_wiki_final_collection_20260427"
    result = build_news_impact_wiki_index(
        collection_dir=collection_dir,
        manifest_path=collection_dir / "manifest.csv",
        embedding_device=config.device,
    )
    return {"status": "completed", "index_rebuild": result}


def run_daily_pipeline(config: DailyPipelineConfig) -> dict[str, Any]:
    config.run_dir.mkdir(parents=True, exist_ok=True)
    runner = StageRunner(config.run_dir, resume=config.resume)
    write_json(
        config.run_dir / "run_config.json",
        {
            "run_id": config.run_id,
            "date_from": config.date_from,
            "date_to": config.date_to,
            "dates": iter_dates(config.date_from, config.date_to),
            "targets_csv": str(config.targets_csv),
            "tickers": list(config.tickers),
            "source_categories": list(config.source_categories),
            "device": config.device,
            "workers": config.workers,
            "dry_run": config.dry_run,
            "resume": config.resume,
            "continue_on_error": config.continue_on_error,
            "company_scope": config.company_scope,
            "company_wiki_update_mode": config.company_wiki_update_mode,
            "started_at": now_iso(),
        },
    )

    stage_summaries: dict[str, Any] = {}

    def source_stage(stage_dir: Path) -> dict[str, Any]:
        if config.skip_source_update:
            return _stage_skip(stage_dir, "skip_source_update")
        return run_source_update(
            SourceUpdateConfig(
                start_date=config.date_from,
                end_date=config.date_to,
                output_root=stage_dir / "source_update",
                targets_csv=config.targets_csv,
                tickers=config.tickers,
                categories=config.source_categories,
                workers=config.workers,
                device=config.device,
                dry_run=config.dry_run,
            ),
            stage_dir,
        )

    stage_summaries["source_update"] = runner.run(
        "01_source_update",
        {"date_from": config.date_from, "date_to": config.date_to, "categories": list(config.source_categories)},
        source_stage,
    )

    stage_summaries["preflight"] = runner.run(
        "02_preflight",
        {"date_from": config.date_from, "date_to": config.date_to},
        lambda _stage_dir: daily_preflight(config.date_from, config.date_to),
    )

    def policy_stage(stage_dir: Path) -> dict[str, Any]:
        if config.skip_policy_impact:
            return _stage_skip(stage_dir, "skip_policy_impact")
        return run_policy_impact(
            date_from=config.date_from,
            date_to=config.date_to,
            run_id=f"{config.run_id}__policy",
            max_impact_companies=config.policy_max_impact_companies,
            dry_run=config.dry_run,
            continue_on_error=config.continue_on_error,
            resume=config.resume,
        )

    policy_summary = runner.run(
        "03_policy_impact",
        {"date_from": config.date_from, "date_to": config.date_to, "max_impact_companies": config.policy_max_impact_companies},
        policy_stage,
    )
    stage_summaries["policy_impact"] = policy_summary

    def company_stage(stage_dir: Path) -> dict[str, Any]:
        if config.skip_company_disclosure_impact:
            return _stage_skip(stage_dir, "skip_company_disclosure_impact")
        return run_company_disclosure_impact(
            date_from=config.date_from,
            date_to=config.date_to,
            run_id=f"{config.run_id}__company_disclosure",
            scope=config.company_scope,
            wiki_update_mode=config.company_wiki_update_mode,
            dry_run=config.dry_run,
            continue_on_error=config.continue_on_error,
            resume=config.resume,
            index_device=config.device,
            rebuild_index_after_apply=False,
        )

    company_summary = runner.run(
        "04_company_disclosure_impact",
        {"date_from": config.date_from, "date_to": config.date_to, "scope": config.company_scope, "wiki_update_mode": config.company_wiki_update_mode},
        company_stage,
    )
    stage_summaries["company_disclosure_impact"] = company_summary

    force_tickers = force_rebuild_tickers_from_company_summary(company_summary)

    def force_stage(stage_dir: Path) -> dict[str, Any]:
        if config.skip_force_rebuild:
            return _stage_skip(stage_dir, "skip_force_rebuild")
        return run_force_rebuild(
            ForceRebuildConfig(
                tickers=tuple(force_tickers),
                run_dir=stage_dir / "force_rebuild",
                dry_run=config.dry_run,
                index_device=config.device,
                rebuild_index=not config.skip_final_index,
                poll_seconds=config.force_rebuild_poll_seconds,
                timeout_seconds=config.force_rebuild_timeout_seconds,
            )
        )

    force_summary = runner.run("05_force_rebuild_wiki", {"tickers": force_tickers}, force_stage)
    stage_summaries["force_rebuild_wiki"] = force_summary

    final_index_summary = runner.run(
        "06_final_wiki_index",
        {"device": config.device},
        lambda _stage_dir: _run_final_index(config=config, company_summary=company_summary, force_summary=force_summary),
    )
    stage_summaries["final_wiki_index"] = final_index_summary

    daily_outputs = runner.run(
        "07_daily_outputs",
        {"date_from": config.date_from, "date_to": config.date_to},
        lambda stage_dir: build_daily_outputs(
            output_root=stage_dir / "outputs",
            date_from=config.date_from,
            date_to=config.date_to,
            policy_summary=policy_summary if policy_summary.get("status") != "skipped" else None,
            company_summary=company_summary if company_summary.get("status") != "skipped" else None,
            force_rebuild_summary=force_summary if force_summary.get("status") != "skipped" else None,
            create_wiki_snapshot=not config.skip_wiki_snapshot,
        ),
    )
    stage_summaries["daily_outputs"] = daily_outputs

    result = {
        "status": "completed",
        "run_id": config.run_id,
        "run_dir": safe_rel(config.run_dir),
        "date_from": config.date_from,
        "date_to": config.date_to,
        "dry_run": config.dry_run,
        "policy": compact_impact_location(policy_summary) if policy_summary.get("status") != "skipped" else policy_summary,
        "company_disclosure": compact_impact_location(company_summary) if company_summary.get("status") != "skipped" else company_summary,
        "force_rebuild_tickers": force_tickers,
        "daily_outputs": daily_outputs,
        "stages": stage_summaries,
        "finished_at": now_iso(),
    }
    write_json(config.run_dir / "run_summary.json", result)
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One-click daily pipeline for source update, policy/disclosure impact, wiki update, and daily reports.")
    parser.add_argument("--date-from", required=True, type=parse_ymd)
    parser.add_argument("--date-to", required=True, type=parse_ymd)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-root", default=str(DEFAULT_RUN_ROOT))
    parser.add_argument("--targets-csv", default=str(ROOT / "configs" / "targets.csv"))
    parser.add_argument("--tickers", nargs="*", default=[])
    parser.add_argument(
        "--source-categories",
        nargs="*",
        default=["policy", "cninfo", "eastmoney", "ingest", "index"],
        help="Source update categories/doc families. Defaults to policy cninfo eastmoney ingest index.",
    )
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--skip-source-update", action="store_true")
    parser.add_argument("--skip-policy-impact", action="store_true")
    parser.add_argument("--skip-company-disclosure-impact", action="store_true")
    parser.add_argument("--skip-force-rebuild", action="store_true")
    parser.add_argument("--skip-final-index", action="store_true")
    parser.add_argument("--skip-wiki-snapshot", action="store_true")
    parser.add_argument("--policy-max-impact-companies", type=int, default=5)
    parser.add_argument("--company-scope", choices=["material", "core_financial", "all"], default="material")
    parser.add_argument("--company-wiki-update-mode", choices=["off", "propose", "apply"], default="apply")
    parser.add_argument("--force-rebuild-poll-seconds", type=float, default=30.0)
    parser.add_argument("--force-rebuild-timeout-seconds", type=float, default=3600.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_id = args.run_id or _default_run_id(args.date_from, args.date_to)
    config = DailyPipelineConfig(
        date_from=args.date_from,
        date_to=args.date_to,
        run_id=run_id,
        run_root=Path(args.run_root),
        targets_csv=Path(args.targets_csv),
        tickers=tuple(args.tickers or ()),
        source_categories=tuple(args.source_categories or ()),
        device=args.device,
        workers=args.workers,
        dry_run=bool(args.dry_run),
        resume=not args.no_resume,
        continue_on_error=bool(args.continue_on_error),
        skip_source_update=bool(args.skip_source_update),
        skip_policy_impact=bool(args.skip_policy_impact),
        skip_company_disclosure_impact=bool(args.skip_company_disclosure_impact),
        skip_force_rebuild=bool(args.skip_force_rebuild),
        skip_final_index=bool(args.skip_final_index),
        skip_wiki_snapshot=bool(args.skip_wiki_snapshot),
        policy_max_impact_companies=int(args.policy_max_impact_companies),
        company_scope=args.company_scope,
        company_wiki_update_mode=args.company_wiki_update_mode,
        force_rebuild_poll_seconds=float(args.force_rebuild_poll_seconds),
        force_rebuild_timeout_seconds=float(args.force_rebuild_timeout_seconds),
    )
    result = run_daily_pipeline(config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
