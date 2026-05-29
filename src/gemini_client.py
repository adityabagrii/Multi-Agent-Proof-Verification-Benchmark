from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from .config import get_gemini_api_key, get_gemini_call_buffer_seconds, get_gemini_model


logger = logging.getLogger(__name__)


class GeminiConfigurationError(RuntimeError):
    pass


@dataclass
class GeminiClient:
    model: str | None = None
    max_retries: int = 4
    retry_delay_seconds: float = 4.0
    call_buffer_seconds: float | None = None

    def __post_init__(self) -> None:
        self.api_key = get_gemini_api_key()
        self.model = self.model or get_gemini_model()
        self.call_buffer_seconds = (
            get_gemini_call_buffer_seconds() if self.call_buffer_seconds is None else self.call_buffer_seconds
        )
        if not self.api_key:
            raise GeminiConfigurationError("GEMINI_API_KEY is empty. Add it to .env before precomputing proofs.")
        try:
            from google import genai  # type: ignore
        except Exception as exc:  # pragma: no cover - depends on local installation
            raise GeminiConfigurationError("Install dependencies with: pip install -r requirements.txt") from exc
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("Calling Gemini proof generator attempt %s/%s", attempt, self.max_retries)
                response = self._client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={"temperature": temperature},
                )
                text = getattr(response, "text", "") or ""
                self._sleep_after_call()
                return text
            except Exception as exc:  # pragma: no cover - live API
                last_error = exc
                logger.warning("Gemini call failed on attempt %s/%s: %s", attempt, self.max_retries, exc)
                self._sleep_after_call()
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay_seconds * attempt)
        raise RuntimeError(f"Gemini call failed after retries: {last_error}")

    def _sleep_after_call(self) -> None:
        assert self.call_buffer_seconds is not None
        if self.call_buffer_seconds > 0:
            time.sleep(self.call_buffer_seconds)
