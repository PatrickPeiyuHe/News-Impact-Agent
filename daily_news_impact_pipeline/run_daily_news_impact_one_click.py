from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
PACKAGE_ROOT = Path(__file__).resolve().parent
for item in (str(SRC_ROOT), str(PACKAGE_ROOT)):
    if item not in sys.path:
        sys.path.insert(0, item)

from daily_news_impact.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
