from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .utils import ROOT


POLICY_DB = ROOT / "data" / "policy" / "catalog" / "policy_catalog.sqlite"
DOCUMENT_DB = ROOT / "data" / "catalog" / "document_catalog.sqlite"
WIKI_DB = ROOT / "data" / "wiki" / "wiki_agent.sqlite"
WIKI_COLLECTION_DIR = ROOT / "reports" / "company_markdown_wiki_final_collection_20260427"
WIKI_INDEX_MANIFEST = ROOT / "data" / "news_impact" / "wiki_index" / "wiki_index_manifest.json"


def _count_sqlite(path: Path, sql: str, params: tuple[Any, ...] = ()) -> int | None:
    if not path.exists():
        return None
    conn = sqlite3.connect(path)
    try:
        row = conn.execute(sql, params).fetchone()
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    return int(row[0] or 0) if row else 0


def daily_preflight(date_from: str, date_to: str) -> dict[str, Any]:
    return {
        "status": "completed",
        "date_from": date_from,
        "date_to": date_to,
        "databases": {
            "policy_db_exists": POLICY_DB.exists(),
            "document_db_exists": DOCUMENT_DB.exists(),
            "wiki_db_exists": WIKI_DB.exists(),
            "policy_docs_in_range": _count_sqlite(
                POLICY_DB,
                "select count(*) from policy_documents where status in ('ok','active') and publish_date_cn >= ? and publish_date_cn <= ?",
                (date_from, date_to),
            ),
            "company_documents_in_range": _count_sqlite(
                DOCUMENT_DB,
                "select count(*) from documents where status='ok' and coalesce(text_status,'')='ok' and substr(coalesce(publish_datetime, as_of_date, ''),1,10) >= ? and substr(coalesce(publish_datetime, as_of_date, ''),1,10) <= ?",
                (date_from, date_to),
            ),
            "wiki_company_count": _count_sqlite(WIKI_DB, "select count(*) from companies"),
        },
        "wiki_collection": {
            "dir": str(WIKI_COLLECTION_DIR),
            "manifest_exists": (WIKI_COLLECTION_DIR / "manifest.csv").exists(),
            "company_wiki_markdown_count": len(list(WIKI_COLLECTION_DIR.glob("[0-9]*__*.md"))) if WIKI_COLLECTION_DIR.exists() else 0,
        },
        "news_impact_index": {
            "manifest_exists": WIKI_INDEX_MANIFEST.exists(),
            "manifest_path": str(WIKI_INDEX_MANIFEST),
        },
    }
