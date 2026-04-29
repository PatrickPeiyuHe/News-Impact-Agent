from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

PIPELINE_ROOT = Path(__file__).resolve().parent
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from daily_news_impact.wiki_build_agent import DocumentRecord, build_wiki_build_plan, describe_wiki_build_modes


def _load_documents(path: Path | None) -> list[DocumentRecord]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("documents_json_must_be_list")
    return [DocumentRecord(**item) for item in payload]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the wiki build agent plan without calling LLM APIs.")
    parser.add_argument("--mode", choices=["reduced", "full"], default="reduced")
    parser.add_argument("--ticker", default="000000")
    parser.add_argument("--company", default="示例公司")
    parser.add_argument("--documents-json", type=Path, default=None, help="Optional list[DocumentRecord] JSON for reduced source selection.")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    parser.add_argument("--describe-modes", action="store_true")
    args = parser.parse_args(argv)

    if args.describe_modes:
        payload: dict[str, Any] = {"modes": describe_wiki_build_modes()}
    else:
        plan = build_wiki_build_plan(
            mode=args.mode,
            ticker=args.ticker,
            company=args.company,
            documents=_load_documents(args.documents_json),
        )
        payload = plan.to_dict()

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
