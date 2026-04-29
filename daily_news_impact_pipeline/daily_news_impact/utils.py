from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_ymd(value: str) -> str:
    return datetime.strptime(value, "%Y-%m-%d").date().isoformat()


def iter_dates(date_from: str, date_to: str) -> list[str]:
    start = date.fromisoformat(parse_ymd(date_from))
    end = date.fromisoformat(parse_ymd(date_to))
    if start > end:
        raise ValueError(f"date_from_after_date_to:{date_from}>{date_to}")
    out: list[str] = []
    current = start
    while current <= end:
        out.append(current.isoformat())
        current += timedelta(days=1)
    return out


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_rel(path: Path, *, root: Path = ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def load_dotenv(path: Path | None = None) -> dict[str, str]:
    env_path = path or (ROOT / ".env")
    if not env_path.exists():
        return {}
    values: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def api_key(*names: str) -> str:
    env = load_dotenv()
    for name in names:
        value = os.getenv(name) or env.get(name)
        if value:
            return value.strip().strip("\"'")
    return ""


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: csv_value(row.get(col)) for col in columns})


def md_cell(value: Any, *, max_chars: int = 260) -> str:
    text = csv_value(value).replace("\n", "<br>").replace("|", "\\|")
    if len(text) > max_chars:
        return text[: max_chars - 3] + "..."
    return text


def write_md_table(path: Path, rows: list[dict[str, Any]], columns: list[str], *, max_chars: int = 260) -> None:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(col), max_chars=max_chars) for col in columns) + " |")
    write_text(path, "\n".join(lines) + "\n")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: str(value or "") for key, value in row.items()} for row in csv.DictReader(handle)]


def write_rows_csv_like(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("no rows to write")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout_path: str
    stderr_path: str
    started_at: str
    finished_at: str


def run_command(*, command: list[str], cwd: Path, stage_dir: Path, timeout: int | None = None) -> CommandResult:
    stage_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = stage_dir / "stdout.log"
    stderr_path = stage_dir / "stderr.log"
    started_at = now_iso()
    write_json(stage_dir / "command.json", {"command": command, "cwd": str(cwd), "started_at": started_at})
    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open("w", encoding="utf-8") as stderr_handle:
        completed = subprocess.run(
            command,
            cwd=cwd,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
            timeout=timeout,
            check=False,
        )
    result = CommandResult(
        command=command,
        returncode=int(completed.returncode),
        stdout_path=str(stdout_path.resolve()),
        stderr_path=str(stderr_path.resolve()),
        started_at=started_at,
        finished_at=now_iso(),
    )
    write_json(stage_dir / "result.json", result.__dict__)
    if result.returncode != 0:
        tail = ""
        if stderr_path.exists():
            tail = stderr_path.read_text(encoding="utf-8", errors="ignore")[-4000:]
        raise RuntimeError(f"stage_command_failed:returncode={result.returncode}:cmd={' '.join(command)}\n{tail}")
    return result


class StageRunner:
    def __init__(self, run_dir: Path, *, resume: bool = True) -> None:
        self.run_dir = run_dir
        self.resume = resume
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def stage_dir(self, name: str) -> Path:
        return self.run_dir / name

    def completed(self, name: str) -> bool:
        if not self.resume:
            return False
        status_path = self.stage_dir(name) / "status.json"
        if not status_path.exists():
            return False
        try:
            status = read_json(status_path)
        except (OSError, json.JSONDecodeError):
            return False
        return status.get("status") in {"completed", "skipped"}

    def run(self, name: str, payload: dict[str, Any], fn: Callable[[Path], dict[str, Any]]) -> dict[str, Any]:
        stage_dir = self.stage_dir(name)
        stage_dir.mkdir(parents=True, exist_ok=True)
        output_path = stage_dir / "output.json"
        if self.completed(name) and output_path.exists():
            return read_json(output_path)
        write_json(stage_dir / "input.json", payload)
        write_json(stage_dir / "status.json", {"status": "running", "started_at": now_iso()})
        try:
            result = fn(stage_dir)
        except BaseException as exc:
            write_json(stage_dir / "status.json", {"status": "failed", "error": repr(exc), "failed_at": now_iso()})
            raise
        write_json(output_path, result)
        write_json(stage_dir / "status.json", {"status": result.get("status", "completed"), "finished_at": now_iso()})
        return result


def project_python() -> str:
    return sys.executable
