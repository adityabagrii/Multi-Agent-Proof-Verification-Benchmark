from __future__ import annotations

from dataclasses import dataclass

from .config import (
    get_dspy_max_tokens,
    get_dspy_model,
    get_dspy_temperature,
    get_nvidia_api_key,
    get_nvidia_nim_base_url,
    load_dotenv,
)


class DSPyConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class DSPyRuntimeConfig:
    model: str
    api_base: str
    temperature: float
    max_tokens: int


def configure_dspy(
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
):
    """Configure DSPy to use NVIDIA NIM's OpenAI-compatible endpoint."""
    load_dotenv()
    api_key = get_nvidia_api_key()
    if not api_key:
        raise DSPyConfigurationError("NVIDIA_API_KEY is empty. Add it to .env before running DSPy workflows.")

    try:
        import dspy  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local installation
        raise DSPyConfigurationError("DSPy is not installed. Run: pip install -r requirements.txt") from exc

    runtime = DSPyRuntimeConfig(
        model=model or get_dspy_model(),
        api_base=get_nvidia_nim_base_url(),
        temperature=get_dspy_temperature() if temperature is None else temperature,
        max_tokens=get_dspy_max_tokens() if max_tokens is None else max_tokens,
    )
    lm = dspy.LM(
        runtime.model,
        api_key=api_key,
        api_base=runtime.api_base,
        temperature=runtime.temperature,
        max_tokens=runtime.max_tokens,
        timeout=120,
        num_retries=3,
    )
    dspy.configure(lm=lm)
    return lm, runtime
