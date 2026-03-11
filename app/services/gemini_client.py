import logging
import json
import re
from typing import Any

import google.generativeai as genai

from app.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self) -> None:
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=genai.GenerationConfig(
                temperature=settings.gemini_temperature,
                response_mime_type="application/json",
            ),
        )
        logger.info("GeminiClient initialized with model=%s", settings.gemini_model)

    def generate(self, prompt: str) -> dict[str, Any]:
        logger.info("Sending prompt to Gemini (length=%d)", len(prompt))
        try:
            response = self._model.generate_content(prompt)
            raw = response.text.strip()
            logger.debug("Raw Gemini response: %s", raw[:500])
            return self._parse_json(raw)
        except Exception as exc:
            logger.error("Gemini API call failed: %s", exc, exc_info=True)
            raise

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        # Strip markdown fences if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("JSON parse error: %s | raw=%s", exc, raw[:300])
            raise ValueError(f"LLM returned invalid JSON: {exc}") from exc


gemini_client = GeminiClient()
