import logging
from typing import Any

from app.services.gemini_client import gemini_client

logger = logging.getLogger(__name__)

_PLANNER_PROMPT = """You are an AI automation architect. Analyze the user idea below and extract structured intent.

User Idea:
{idea}

Return ONLY a valid JSON object — no markdown, no explanation — with this exact schema:
{{
  "core_goal": "<one-sentence description of the main objective>",
  "trigger_hint": "<what event should trigger this automation>",
  "domain": "<business domain, e.g. sales, marketing, HR, finance>",
  "key_entities": ["<list of main data objects or concepts involved>"],
  "complexity": "<low | medium | high>"
}}
"""


class PlannerAgent:
    """Understands the user's idea and extracts structured intent."""

    def run(self, idea: str) -> dict[str, Any]:
        logger.info("PlannerAgent.run | idea_length=%d", len(idea))
        prompt = _PLANNER_PROMPT.format(idea=idea)
        result = gemini_client.generate(prompt)
        logger.info("PlannerAgent result: %s", result)
        return result
