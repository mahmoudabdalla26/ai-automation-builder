import logging
from typing import Any

from app.services.gemini_client import gemini_client

logger = logging.getLogger(__name__)

_REVIEWER_PROMPT = """You are a senior AI automation reviewer. Evaluate and improve the workflow below.

Original User Idea:
{idea}

Proposed Workflow:
{workflow}

Tasks:
1. Validate the workflow is coherent and complete for the user's idea.
2. Fill any missing steps, integrations, or ai_tasks.
3. Improve naming clarity if needed.
4. Assign a confidence_score between 0.0 and 1.0 reflecting how well the workflow addresses the idea.

Return ONLY a valid JSON object — no markdown, no explanation — with this exact schema:
{{
  "automation_name": "<final name>",
  "trigger": "<final trigger>",
  "steps": ["<step 1>", "<step 2>", "..."],
  "integrations": ["<tool 1>", "<tool 2>"],
  "ai_tasks": ["<task_1>", "<task_2>"],
  "confidence_score": 0.0
}}

confidence_score guidelines:
- 0.9–1.0: idea is very clear, workflow is complete and accurate
- 0.7–0.89: minor gaps or ambiguities
- 0.5–0.69: moderate ambiguity or missing elements
- below 0.5: very vague idea or major gaps
"""


class ReviewerAgent:
    """Validates and improves the workflow, assigns a confidence score."""

    def run(self, idea: str, workflow: dict[str, Any]) -> dict[str, Any]:
        logger.info("ReviewerAgent.run | automation_name=%s", workflow.get("automation_name"))
        prompt = _REVIEWER_PROMPT.format(idea=idea, workflow=workflow)
        result = gemini_client.generate(prompt)
        logger.info(
            "ReviewerAgent result: confidence_score=%s",
            result.get("confidence_score"),
        )
        return result
