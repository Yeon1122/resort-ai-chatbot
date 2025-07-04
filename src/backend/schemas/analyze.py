from pydantic import BaseModel, Field

class AnalyzeResponse(BaseModel):
    item: str = Field(..., example="")
    confidence: float = Field(..., example=0)
    answer: str = Field(..., example="")
