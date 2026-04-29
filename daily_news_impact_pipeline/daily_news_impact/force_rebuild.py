from __future__ import annotations

import csv
import json
import os
import requests
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .utils import ROOT, api_key, now_iso, safe_rel, write_json


WIKI_DB = ROOT / "data" / "wiki" / "wiki_agent.sqlite"
WIKI_COLLECTION_DIR = ROOT / "reports" / "company_markdown_wiki_final_collection_20260427"
WIKI_MANIFEST = WIKI_COLLECTION_DIR / "manifest.csv"


def normalize_ticker(value: str) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if not digits:
        raise ValueError(f"invalid_ticker:{value}")
    return digits.zfill(6)


def _request_json(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return {"_non_json_body": response.text}


def _ensure_ok(response: requests.Response, *, label: str) -> Any:
    payload = _request_json(response)
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(f"{label}_failed:http_{response.status_code}:{payload}")
    return payload


def _strip_reasoning(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {k: _strip_reasoning(v) for k, v in payload.items() if k != "reasoning_content"}
    if isinstance(payload, list):
        return [_strip_reasoning(item) for item in payload]
    return payload


def _extract_chat_content(payload: dict[str, Any]) -> tuple[str, str]:
    choices = payload.get("choices") or []
    if not choices:
        return "", ""
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        content = "\n".join(str(part.get("text") or part) for part in content)
    return str(content or ""), str(message.get("reasoning_content") or "")


def _extract_json_object(text: str) -> dict[str, Any]:
    raw = str(text or "").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].lstrip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start < 0 or end <= start:
            raise
        payload = json.loads(raw[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("json_output_not_object")
    return payload


def _split_brainstormer_input(text: str) -> tuple[str, str, str]:
    cache_marker = "\n\nCACHED FIXED CONTEXT\n"
    user_marker = "\n\nUSER PROMPT\n"
    if not text.startswith("SYSTEM PROMPT\n") or cache_marker not in text or user_marker not in text:
        raise ValueError("unexpected_brainstormer_input_shape")
    system_end = text.index(cache_marker)
    cache_start = system_end + len(cache_marker)
    cache_end = text.index(user_marker, cache_start)
    return (
        text[len("SYSTEM PROMPT\n") : system_end].strip(),
        text[cache_start:cache_end].strip(),
        text[cache_end + len(user_marker) :].strip(),
    )


def _qwen_config(model: str) -> tuple[str, str]:
    key = api_key("QWEN_API_KEY", "qwen_api_key")
    if not key:
        raise RuntimeError("missing_qwen_api_key")
    base_url = (
        os.getenv("QWEN_BASE_URL")
        or os.getenv("qwen_base_url")
        or "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    ).strip().strip("\"'").rstrip("/")
    if model.endswith("-us"):
        base_url = "https://dashscope-us.aliyuncs.com/compatible-mode/v1"
    return key, base_url


def _moonshot_config() -> tuple[str, str]:
    key = api_key("MOONSHOT_API_KEY", "moonshot_api_key")
    if not key:
        raise RuntimeError("missing_moonshot_api_key")
    base_url = (os.getenv("MOONSHOT_BASE_URL") or "https://api.moonshot.cn/v1").strip().strip("\"'").rstrip("/")
    return key, base_url


def run_brainstormer(
    *,
    tickers: list[str],
    input_root: Path,
    output_root: Path,
    model: str = "qwen3.5-plus",
    max_tokens: int = 8192,
    timeout_seconds: int = 360,
) -> dict[str, Any]:
    from comm_profile.wiki.reduced_wiki_brainstormer import build_brainstormer_request_payload

    output_root.mkdir(parents=True, exist_ok=True)
    api, base_url = _qwen_config(model)
    runs: list[dict[str, Any]] = []
    for ticker in tickers:
        ticker = normalize_ticker(ticker)
        item_dir = output_root / ticker
        item_dir.mkdir(parents=True, exist_ok=True)
        input_path = input_root / ticker / "brainstormer_input.md"
        text = input_path.read_text(encoding="utf-8")
        system_prompt, cache_context, user_prompt = _split_brainstormer_input(text)
        payload = build_brainstormer_request_payload(
            system_prompt=system_prompt,
            static_cache_context=cache_context,
            user_prompt=user_prompt,
            model=model,
            max_tokens=max_tokens,
        )
        write_json(item_dir / "request_payload.json", payload)
        started = time.monotonic()
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api}", "Content-Type": "application/json"},
            json=payload,
            timeout=timeout_seconds,
        )
        body = _ensure_ok(response, label=f"qwen_brainstormer:{ticker}")
        content, reasoning = _extract_chat_content(body if isinstance(body, dict) else {})
        if not content.strip():
            raise RuntimeError(f"empty_brainstormer_output:{ticker}:{str(body)[:500]}")
        parsed = _extract_json_object(content)
        write_json(item_dir / "raw_response.json", _strip_reasoning(body))
        (item_dir / "output.txt").write_text(content, encoding="utf-8")
        (item_dir / "reasoning.md").write_text(reasoning, encoding="utf-8")
        write_json(item_dir / "brainstormer_output.json", parsed)
        runs.append(
            {
                "ticker": ticker,
                "ok": True,
                "output_dir": safe_rel(item_dir),
                "usage": body.get("usage") if isinstance(body, dict) else {},
                "elapsed_sec": round(time.monotonic() - started, 3),
            }
        )
    summary = {"status": "completed", "output_root": safe_rel(output_root), "model": model, "runs": runs}
    write_json(output_root / "summary.json", summary)
    return summary


def _split_writer_input(text: str) -> tuple[str, str]:
    marker = "\n\nUSER PROMPT\n"
    if not text.startswith("SYSTEM PROMPT\n") or marker not in text:
        raise ValueError("unexpected_writer_input_shape")
    system_end = text.index(marker)
    return text[len("SYSTEM PROMPT\n") : system_end].strip(), text[system_end + len(marker) :].strip()


def _upload_batch_file(*, base_url: str, api_key_value: str, jsonl_path: Path, timeout_seconds: int) -> Any:
    with jsonl_path.open("rb") as handle:
        response = requests.post(
            f"{base_url}/files",
            headers={"Authorization": f"Bearer {api_key_value}"},
            data={"purpose": "batch"},
            files={"file": (jsonl_path.name, handle, "application/jsonl")},
            timeout=timeout_seconds,
        )
    return _ensure_ok(response, label="moonshot_file_upload")


def _create_batch(*, base_url: str, api_key_value: str, input_file_id: str, completion_window: str, timeout_seconds: int) -> Any:
    response = requests.post(
        f"{base_url}/batches",
        headers={"Authorization": f"Bearer {api_key_value}", "Content-Type": "application/json"},
        json={"input_file_id": input_file_id, "endpoint": "/v1/chat/completions", "completion_window": completion_window},
        timeout=timeout_seconds,
    )
    return _ensure_ok(response, label="moonshot_batch_create")


def _retrieve_batch(*, base_url: str, api_key_value: str, batch_id: str, timeout_seconds: int) -> Any:
    response = requests.get(f"{base_url}/batches/{batch_id}", headers={"Authorization": f"Bearer {api_key_value}"}, timeout=timeout_seconds)
    return _ensure_ok(response, label="moonshot_batch_retrieve")


def _download_file(*, base_url: str, api_key_value: str, file_id: str, timeout_seconds: int) -> str:
    response = requests.get(f"{base_url}/files/{file_id}/content", headers={"Authorization": f"Bearer {api_key_value}"}, timeout=timeout_seconds)
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(f"moonshot_file_download_failed:http_{response.status_code}:{_request_json(response)}")
    return response.content.decode("utf-8", errors="replace")


def create_writer_batch(
    *,
    tickers: list[str],
    input_dir: Path,
    batch_dir: Path,
    model: str = "kimi-k2.6",
    max_tokens: int = 16384,
    completion_window: str = "24h",
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    batch_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = batch_dir / "batch_requests.jsonl"
    request_rows: list[dict[str, Any]] = []
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as handle:
        for ticker in tickers:
            ticker = normalize_ticker(ticker)
            input_path = input_dir / f"{ticker}_model_input.md"
            system_prompt, user_prompt = _split_writer_input(input_path.read_text(encoding="utf-8"))
            body = {
                "model": model,
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                "max_tokens": max_tokens,
                "thinking": {"type": "enabled"},
            }
            row = {"custom_id": f"{ticker}__wiki_writer__{model}", "method": "POST", "url": "/v1/chat/completions", "body": body}
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            request_rows.append({"ticker": ticker, "custom_id": row["custom_id"], "input_path": safe_rel(input_path), "input_chars": len(system_prompt) + len(user_prompt)})

    api, base_url = _moonshot_config()
    file_payload = _upload_batch_file(base_url=base_url, api_key_value=api, jsonl_path=jsonl_path, timeout_seconds=timeout_seconds)
    input_file_id = str(file_payload.get("id") or "")
    if not input_file_id:
        raise RuntimeError(f"file_upload_missing_id:{file_payload}")
    batch_payload = _create_batch(
        base_url=base_url,
        api_key_value=api,
        input_file_id=input_file_id,
        completion_window=completion_window,
        timeout_seconds=timeout_seconds,
    )
    batch_id = str(batch_payload.get("id") or "")
    if not batch_id:
        raise RuntimeError(f"batch_create_missing_id:{batch_payload}")
    status = _retrieve_batch(base_url=base_url, api_key_value=api, batch_id=batch_id, timeout_seconds=timeout_seconds)
    manifest = {
        "created_at": now_iso(),
        "model": model,
        "provider": "moonshot",
        "base_url": base_url,
        "completion_window": completion_window,
        "max_tokens": max_tokens,
        "thinking": "enabled",
        "request_count": len(request_rows),
        "tickers": [normalize_ticker(item) for item in tickers],
        "request_jsonl": safe_rel(jsonl_path),
        "requests": request_rows,
        "input_file_id": input_file_id,
        "batch_id": batch_id,
        "batch_status": status.get("status"),
        "batch_request_counts": status.get("request_counts"),
    }
    write_json(batch_dir / "file_upload_response.json", file_payload)
    write_json(batch_dir / "batch_create_response.json", batch_payload)
    write_json(batch_dir / "batch_status.json", status)
    write_json(batch_dir / "batch_manifest.json", manifest)
    return manifest


def fetch_writer_batch(
    *,
    batch_dir: Path,
    output_root: Path,
    poll_seconds: float = 30.0,
    timeout_seconds: float = 3600.0,
    request_timeout_seconds: int = 120,
) -> dict[str, Any]:
    manifest = json.loads((batch_dir / "batch_manifest.json").read_text(encoding="utf-8"))
    batch_id = str(manifest.get("batch_id") or "")
    model = str(manifest.get("model") or "kimi-k2.6")
    api, base_url = _moonshot_config()
    deadline = time.monotonic() + max(0.0, timeout_seconds)
    status: dict[str, Any]
    while True:
        status = _retrieve_batch(base_url=base_url, api_key_value=api, batch_id=batch_id, timeout_seconds=request_timeout_seconds)
        write_json(batch_dir / "batch_status_latest.json", status)
        if status.get("status") == "completed":
            break
        if status.get("status") in {"failed", "expired", "cancelled"}:
            raise RuntimeError(f"writer_batch_failed:{status}")
        if time.monotonic() >= deadline:
            return {"status": "timeout", "batch_status": status}
        time.sleep(max(1.0, poll_seconds))

    output_file_id = str(status.get("output_file_id") or "")
    if not output_file_id:
        raise RuntimeError(f"completed_batch_missing_output_file_id:{status}")
    output_text = _download_file(base_url=base_url, api_key_value=api, file_id=output_file_id, timeout_seconds=request_timeout_seconds)
    (batch_dir / "batch_output.jsonl").write_text(output_text, encoding="utf-8")

    materialized: dict[str, Any] = {"status": "completed", "model": model, "tickers": {}}
    for raw_line in output_text.splitlines():
        if not raw_line.strip():
            continue
        line = json.loads(raw_line)
        custom_id = str(line.get("custom_id") or line.get("id") or "")
        ticker = custom_id.split("__", 1)[0]
        model_dir = output_root / ticker / model
        model_dir.mkdir(parents=True, exist_ok=True)
        write_json(model_dir / "batch_response_line.json", line)
        response = line.get("response") or {}
        body = response.get("body") or {}
        status_code = int(response.get("status_code") or 0)
        error_payload = line.get("error")
        if error_payload or not isinstance(body, dict) or not body.get("choices"):
            write_json(model_dir / "error.json", {"custom_id": custom_id, "status_code": status_code, "error": error_payload})
            materialized["tickers"][ticker] = {"ok": False, "status_code": status_code}
            continue
        content, reasoning = _extract_chat_content(body)
        if not content.strip():
            write_json(model_dir / "error.json", {"custom_id": custom_id, "status_code": status_code, "error": "empty_content"})
            materialized["tickers"][ticker] = {"ok": False, "status_code": status_code, "error": "empty_content"}
            continue
        write_json(model_dir / "response.json", _strip_reasoning(body))
        (model_dir / "output.md").write_text(content, encoding="utf-8")
        (model_dir / "reasoning.md").write_text(reasoning, encoding="utf-8")
        write_json(model_dir / "usage.json", body.get("usage") or {})
        materialized["tickers"][ticker] = {"ok": True, "output_path": safe_rel(model_dir / "output.md"), "status_code": status_code}
    write_json(batch_dir / "materialized_summary.json", materialized)
    return materialized


def _load_manifest(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return [{k: str(v or "") for k, v in row.items()} for row in reader], fields


def _write_manifest(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _validate_wiki(text: str, ticker: str, company: str) -> dict[str, Any]:
    stripped = text.strip()
    checks = {
        "not_empty": bool(stripped),
        "starts_with_heading": stripped.startswith("#"),
        "has_ticker": ticker in stripped,
        "has_company": company in stripped,
        "length_ok": len(stripped) >= 1800,
        "not_code_fenced": not stripped.startswith("```"),
    }
    return {"accepted": all(checks.values()), "checks": checks, "chars": len(stripped), "first_line": stripped.splitlines()[0] if stripped else ""}


def apply_rebuilt_wikis(
    *,
    tickers: list[str],
    writer_output_root: Path,
    apply_dir: Path,
    model: str = "kimi-k2.6",
    collection_dir: Path = WIKI_COLLECTION_DIR,
    manifest_path: Path = WIKI_MANIFEST,
    rebuild_index: bool = True,
    index_device: str = "auto",
) -> dict[str, Any]:
    from comm_profile.news_impact.wiki_index import build_news_impact_wiki_index

    rows, fields = _load_manifest(manifest_path)
    by_ticker = {normalize_ticker(row.get("ticker", "")): row for row in rows if row.get("ticker")}
    archive_root = collection_dir / "_archive"
    applied: list[dict[str, Any]] = []
    for ticker in [normalize_ticker(item) for item in tickers]:
        row = by_ticker.get(ticker)
        if row is None:
            raise ValueError(f"ticker_not_in_manifest:{ticker}")
        company = row.get("company", "")
        output_path = writer_output_root / ticker / model / "output.md"
        output_text = output_path.read_text(encoding="utf-8").strip() + "\n"
        validation = _validate_wiki(output_text, ticker, company)
        if not validation["accepted"]:
            raise ValueError(f"rebuilt_wiki_failed_validation:{ticker}:{validation}")
        current_path = collection_dir / row.get("file", f"{ticker}__reduced_wiki.md")
        target_path = collection_dir / f"{ticker}__reduced_wiki.md"
        archive_paths: list[str] = []
        archive_dir = archive_root / ticker
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if current_path.exists():
            archive_path = archive_dir / f"{stamp}__before_rebuild__{current_path.name}"
            shutil.copy2(current_path, archive_path)
            archive_paths.append(safe_rel(archive_path))
        if target_path.exists() and target_path.resolve() != current_path.resolve():
            archive_path = archive_dir / f"{stamp}__existing_target__{target_path.name}"
            shutil.copy2(target_path, archive_path)
            archive_paths.append(safe_rel(archive_path))
        target_path.write_text(output_text, encoding="utf-8")
        removed_files: list[str] = []
        if current_path.exists() and current_path.resolve() != target_path.resolve():
            current_path.unlink()
            removed_files.append(safe_rel(current_path))
        row["type"] = "reduced_wiki"
        row["file"] = target_path.name
        row["source_path"] = str(output_path.resolve())
        row["selected_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        applied.append(
            {
                "ticker": ticker,
                "company": company,
                "writer_output": safe_rel(output_path),
                "target_path": safe_rel(target_path),
                "previous_file": current_path.name,
                "archive_paths": archive_paths,
                "removed_files": removed_files,
                "validation": validation,
            }
        )
    _write_manifest(manifest_path, rows, fields)
    index_summary: dict[str, Any] = {}
    if rebuild_index:
        index_summary = build_news_impact_wiki_index(collection_dir=collection_dir, manifest_path=manifest_path, embedding_device=index_device)
    summary = {
        "status": "completed",
        "applied_at": now_iso(),
        "tickers": [normalize_ticker(item) for item in tickers],
        "applied": applied,
        "index_rebuild": index_summary,
    }
    write_json(apply_dir / "apply_rebuild_summary.json", summary)
    return summary


@dataclass(frozen=True)
class ForceRebuildConfig:
    tickers: tuple[str, ...]
    run_dir: Path
    dry_run: bool = False
    model: str = "kimi-k2.6"
    index_device: str = "auto"
    rebuild_index: bool = True
    poll_seconds: float = 30.0
    timeout_seconds: float = 3600.0


def run_force_rebuild(config: ForceRebuildConfig) -> dict[str, Any]:
    tickers = [normalize_ticker(item) for item in config.tickers]
    tickers = sorted(dict.fromkeys(tickers))
    config.run_dir.mkdir(parents=True, exist_ok=True)
    if not tickers:
        summary = {"status": "skipped", "reason": "no_force_rebuild_tickers", "tickers": []}
        write_json(config.run_dir / "force_rebuild_summary.json", summary)
        return summary
    if config.dry_run:
        summary = {"status": "completed", "dry_run": True, "tickers": tickers}
        write_json(config.run_dir / "force_rebuild_summary.json", summary)
        return summary

    from comm_profile.wiki.reduced_wiki_brainstormer import write_brainstormer_inputs
    from comm_profile.wiki.reduced_wiki_builder import write_model_inputs

    brainstormer_inputs = config.run_dir / "01_brainstormer_inputs"
    brainstormer_outputs = config.run_dir / "02_brainstormer_outputs"
    writer_inputs = config.run_dir / "03_writer_inputs"
    batch_dir = config.run_dir / "04_kimi_batch" / config.model
    writer_outputs = config.run_dir / "05_writer_outputs"
    apply_dir = config.run_dir / "06_apply_rebuild"

    input_summary_path = brainstormer_inputs / "summary.json"
    input_summary = json.loads(input_summary_path.read_text(encoding="utf-8")) if input_summary_path.exists() else write_brainstormer_inputs(tickers, db_path=WIKI_DB, output_dir=brainstormer_inputs)

    brainstorm_done = all((brainstormer_outputs / ticker / "brainstormer_output.json").exists() for ticker in tickers)
    brainstorm_summary = (
        json.loads((brainstormer_outputs / "summary.json").read_text(encoding="utf-8"))
        if brainstorm_done and (brainstormer_outputs / "summary.json").exists()
        else run_brainstormer(tickers=tickers, input_root=brainstormer_inputs, output_root=brainstormer_outputs)
    )

    writer_input_summary_path = writer_inputs / "summary.json"
    writer_inputs_done = all((writer_inputs / f"{ticker}_model_input.md").exists() for ticker in tickers)
    if writer_inputs_done and writer_input_summary_path.exists():
        writer_input_summary = json.loads(writer_input_summary_path.read_text(encoding="utf-8"))
    else:
        writer_input_summary = write_model_inputs(tickers, db_path=WIKI_DB, output_dir=writer_inputs, brainstormer_output_root=brainstormer_outputs)
        write_json(writer_input_summary_path, writer_input_summary)

    batch_manifest_path = batch_dir / "batch_manifest.json"
    if batch_manifest_path.exists():
        batch_summary = json.loads(batch_manifest_path.read_text(encoding="utf-8"))
    else:
        batch_summary = create_writer_batch(tickers=tickers, input_dir=writer_inputs, batch_dir=batch_dir, model=config.model)

    outputs_done = all((writer_outputs / ticker / config.model / "output.md").exists() for ticker in tickers)
    if outputs_done:
        fetch_summary = {"status": "completed", "reused_existing_outputs": True, "output_root": safe_rel(writer_outputs)}
    else:
        fetch_summary = fetch_writer_batch(
            batch_dir=batch_dir,
            output_root=writer_outputs,
            poll_seconds=config.poll_seconds,
            timeout_seconds=config.timeout_seconds,
        )
    if fetch_summary.get("status") == "timeout":
        summary = {
            "status": "timeout",
            "tickers": tickers,
            "batch": batch_summary,
            "fetch": fetch_summary,
            "resume_instruction": "rerun the daily pipeline with the same run_id; it will fetch the existing batch if stage resume is enabled",
        }
        write_json(config.run_dir / "force_rebuild_summary.json", summary)
        return summary
    apply_summary = apply_rebuilt_wikis(
        tickers=tickers,
        writer_output_root=writer_outputs,
        apply_dir=apply_dir,
        model=config.model,
        rebuild_index=config.rebuild_index,
        index_device=config.index_device,
    )
    summary = {
        "status": "completed",
        "tickers": tickers,
        "brainstormer_inputs": input_summary,
        "brainstormer": brainstorm_summary,
        "writer_inputs": writer_input_summary,
        "batch": batch_summary,
        "fetch": fetch_summary,
        "apply": apply_summary,
    }
    write_json(config.run_dir / "force_rebuild_summary.json", summary)
    return summary
