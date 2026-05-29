from __future__ import annotations

import json
import re
from typing import Any


def _extract_json_candidate(text: str) -> str:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1)

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    raise ValueError(f"Could not find JSON object in response: {text[:200]}")


def _repair_common_json_issues(candidate: str) -> str:
    """Repair common LLM JSON issues without changing the object structure."""
    repaired = candidate.strip()
    # LLMs sometimes emit LaTeX commands such as \ge inside JSON strings.
    # JSON only allows a small set of backslash escapes, so preserve the slash
    # by doubling unsupported escapes.
    repaired = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", repaired)
    # Remove trailing commas before an object/array close.
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    return repaired


def safe_json_loads(text: str) -> dict[str, Any]:
    candidates = [text]
    try:
        candidates.append(_extract_json_candidate(text))
    except ValueError:
        pass

    errors: list[str] = []
    for candidate in candidates:
        for attempt in (candidate, _repair_common_json_issues(candidate)):
            try:
                value = json.loads(attempt)
                return value if isinstance(value, dict) else {"raw": value}
            except json.JSONDecodeError as exc:
                errors.append(str(exc))

    raise ValueError(f"Could not parse JSON response. Errors: {' | '.join(errors[:3])}. Raw: {text[:500]}")
