from __future__ import annotations

import logging
from pathlib import Path

from .config import OUTPUTS_DIR


def setup_logging() -> None:
    log_dir = OUTPUTS_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "run.log"

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    file_handler = logging.FileHandler(Path(log_path), encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
