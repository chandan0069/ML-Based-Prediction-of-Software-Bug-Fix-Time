from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class BugInput(BaseModel):
    summary: str = Field(..., example="NPE in TaskScheduler when job queue is empty")
    description: str = Field(default="", example="Detailed description of the bug...")
    priority: Literal["Blocker", "Critical", "Major", "Minor", "Trivial"] = Field(
        ..., example="Major"
    )
    components: str = Field(
        default="",
        example="Scheduler, Core",
        description="Comma-separated or list string, e.g. 'Scheduler, Core' or \"['Scheduler']\""
    )
    created_date: datetime = Field(
        default_factory=datetime.utcnow,
        example="2024-03-15T10:30:00"
    )


class PredictionOutput(BaseModel):
    prediction: Literal["Short (< 8 days)", "Long (>= 8 days)"]
    confidence: float = Field(..., example=0.73, description="Probability of short resolution")
    label: int = Field(..., example=1, description="1 = Short, 0 = Long")
