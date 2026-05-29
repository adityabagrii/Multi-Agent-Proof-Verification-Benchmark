from __future__ import annotations

from pathlib import Path
from string import Template

from .config import PROMPTS_DIR


def render_prompt(template_name: str, **values: object) -> str:
    path = PROMPTS_DIR / template_name
    text = path.read_text(encoding="utf-8")
    clean_values = {key: "" if value is None else str(value) for key, value in values.items()}
    return Template(text).safe_substitute(clean_values)
