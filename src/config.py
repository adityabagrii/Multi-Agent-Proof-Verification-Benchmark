from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
PROJECT_ENV_PATH = ROOT / ".env"


def _strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return value[:index].strip()
    return value.strip()


def get_project_env_path() -> Path:
    return PROJECT_ENV_PATH


def load_dotenv(path: Path | None = None, override: bool = True) -> Path:
    """Load this project's .env file.

    override=True is intentional: IDEs and shells often already have variables
    from another project. This assignment should use Assignment-3/.env.
    """
    env_path = path or PROJECT_ENV_PATH
    if not env_path.exists():
        return env_path
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = _strip_inline_comment(value).strip('"').strip("'")
        if override or key not in os.environ:
            os.environ[key] = value
    return env_path


def get_nvidia_api_key() -> str:
    load_dotenv()
    return os.getenv("NVIDIA_API_KEY", os.getenv("NIM_API_KEY", "")).strip()


def get_gemini_api_key() -> str:
    load_dotenv()
    return os.getenv("GEMINI_API_KEY", "").strip()


def get_gemini_model() -> str:
    load_dotenv()
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()


def get_gemini_call_buffer_seconds() -> float:
    load_dotenv()
    raw_value = os.getenv("GEMINI_CALL_BUFFER_SECONDS", "0").strip()
    try:
        return max(0.0, float(raw_value))
    except ValueError:
        return 0.0


def get_nvidia_nim_base_url() -> str:
    load_dotenv()
    return os.getenv(
        "NVIDIA_NIM_BASE_URL",
        os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1"),
    ).strip().rstrip("/")


def get_nvidia_nim_model() -> str:
    load_dotenv()
    return os.getenv(
        "NVIDIA_NIM_MODEL",
        os.getenv("DSPY_MODEL", "mistralai/mistral-nemotron"),
    ).strip()


def get_dspy_model() -> str:
    load_dotenv()
    return os.getenv("DSPY_MODEL", "mistralai/mistral-nemotron").strip()


def get_dspy_max_tokens() -> int:
    load_dotenv()
    raw_value = os.getenv("DSPY_MAX_TOKENS", "2200").strip()
    try:
        return max(256, int(raw_value))
    except ValueError:
        return 2200


def get_dspy_temperature() -> float:
    load_dotenv()
    raw_value = os.getenv("DSPY_TEMPERATURE", "0.1").strip()
    try:
        return max(0.0, float(raw_value))
    except ValueError:
        return 0.1
