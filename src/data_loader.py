from __future__ import annotations

import json

from .config import DATA_DIR
from .models import Inequality


def load_inequalities() -> list[Inequality]:
    raw = json.loads((DATA_DIR / "inequalities.json").read_text(encoding="utf-8"))
    return [Inequality(**item) for item in raw]


def get_inequality(inequality_id: str) -> Inequality:
    for item in load_inequalities():
        if item.id == inequality_id:
            return item
    raise KeyError(f"Unknown inequality id: {inequality_id}")
