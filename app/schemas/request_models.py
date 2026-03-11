from pydantic import BaseModel, Field, field_validator


class AutomationRequest(BaseModel):
    idea: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Natural language description of the automation idea",
        examples=["Build automation that analyzes sales Excel reports and generates a summary"],
    )

    @field_validator("idea")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()
