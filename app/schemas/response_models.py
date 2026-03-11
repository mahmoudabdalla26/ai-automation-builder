from pydantic import BaseModel, Field


class AutomationResponse(BaseModel):
    automation_name: str = Field(..., description="Human-readable name of the automation")
    trigger: str = Field(..., description="Event or condition that starts the automation")
    steps: list[str] = Field(..., description="Ordered list of automation steps")
    integrations: list[str] = Field(..., description="External tools or services required")
    ai_tasks: list[str] = Field(..., description="AI-specific tasks within the workflow")
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Reviewer confidence score (0–1)"
    )


class ErrorResponse(BaseModel):
    detail: str
    code: str
