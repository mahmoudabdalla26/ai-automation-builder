import logging
from typing import Any

from pydantic import ValidationError

from app.agents.builder_agent import BuilderAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.schemas.response_models import AutomationResponse

logger = logging.getLogger(__name__)


class WorkflowGenerator:
    """
    Orchestrates the multi-agent pipeline:
        PlannerAgent → BuilderAgent → ReviewerAgent → AutomationResponse
    """

    def __init__(self) -> None:
        self._planner = PlannerAgent()
        self._builder = BuilderAgent()
        self._reviewer = ReviewerAgent()

    def generate(self, idea: str) -> AutomationResponse:
        logger.info("WorkflowGenerator.generate | idea=%s", idea[:80])

        # Stage 1 – Plan
        plan = self._planner.run(idea)

        # Stage 2 – Build
        workflow = self._builder.run(idea, plan)

        # Stage 3 – Review
        reviewed = self._reviewer.run(idea, workflow)

        # Stage 4 – Validate & return
        return self._to_response(reviewed)

    @staticmethod
    def _to_response(data: dict[str, Any]) -> AutomationResponse:
        # Normalise confidence_score type safety
        raw_score = data.get("confidence_score", 0.75)
        try:
            score = float(raw_score)
            score = max(0.0, min(1.0, score))
        except (TypeError, ValueError):
            logger.warning("Invalid confidence_score=%r — defaulting to 0.75", raw_score)
            score = 0.75

        payload = {
            "automation_name": str(data.get("automation_name", "Unnamed Automation")),
            "trigger": str(data.get("trigger", "Manual Trigger")),
            "steps": _ensure_list(data.get("steps")),
            "integrations": _ensure_list(data.get("integrations")),
            "ai_tasks": _ensure_list(data.get("ai_tasks")),
            "confidence_score": score,
        }

        try:
            return AutomationResponse(**payload)
        except ValidationError as exc:
            logger.error("Response validation failed: %s", exc)
            raise ValueError(f"Workflow validation error: {exc}") from exc


def _ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return []


workflow_generator = WorkflowGenerator()
