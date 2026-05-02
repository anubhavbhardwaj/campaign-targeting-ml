from pydantic import BaseModel, field_validator
from typing import List, Dict


class GroupFeatures(BaseModel):
    values: List[float]

    @field_validator("values")
    def check_values(cls, v):
        if len(v) != 20:
            raise ValueError(f"values must be a list of 20 floats, got {len(v)}")
        return v


class ComparatorFeatures(BaseModel):
    values: List[float]

    @field_validator("values")
    def check_values(cls, v):
        if len(v) != 27:
            raise ValueError(f"values must be a list of 27 floats, got {len(v)}")
        return v


class PredictionRequest(BaseModel):
    group1: GroupFeatures
    group2: GroupFeatures
    comparator: ComparatorFeatures


class PredictionResponse(BaseModel):
    prediction: int
    recommendation: str
    confidence: float
    probabilities: Dict[str, float]