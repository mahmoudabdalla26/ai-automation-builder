import logging
from typing import Any

from app.services.gemini_client import gemini_client

logger = logging.getLogger(__name__)

_BUILDER_PROMPT = """You are an AI automation workflow builder. Using the structured intent below, design a detailed automation workflow.

Structured Intent:
{plan}

Original Idea:
{idea}

Return ONLY a valid JSON object — no markdown, no explanation — with this exact schema:
{{
  "automation_name": "<concise, descriptive name for this automation>",
  "trigger": "<specific trigger event, e.g. File Upload, Scheduled Daily, Webhook, Email Received>",
  "steps": [
    "<step 1: action description>",
    "<step 2: action description>",
    "<step 3: action description>"
  ],
  "integrations": ["<external tool or service 1>", "<external tool or service 2>"],
  "ai_tasks": ["<ai task identifier 1>", "<ai task identifier 2>"]
}}

Rules:
- steps must be ordered, actionable, and specific (3–8 steps)
- integrations must be real tools (e.g. Gmail, Slack, Excel, Salesforce, Google Sheets)
- ai_tasks must use snake_case identifiers (e.g. sentiment_analysis, data_extraction, report_generation)
"""


class BuilderAgent:
    """Builds the full automation workflow from planner output."""

    def run(self, idea: str, plan: dict[str, Any]) -> dict[str, Any]:
        logger.info("BuilderAgent.run | domain=%s | complexity=%s", plan.get("domain"), plan.get("complexity"))
        prompt = _BUILDER_PROMPT.format(plan=plan, idea=idea)
        result = gemini_client.generate(prompt)
        logger.info("BuilderAgent result: %s", result)
        return result
