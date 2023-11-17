from typing import List, Optional
from pydantic import BaseModel, validator


class PredictionData(BaseModel):
    x0: Optional[float]
    x1: Optional[float]
    x2: Optional[float]
    x3: Optional[float]
    x4: Optional[float]
    x5: Optional[str]  # Categorical
    x6: Optional[float]
    x7: Optional[float]
    x8: Optional[float]
    x9: Optional[float]
    x10: Optional[float]
    x11: Optional[float]
    x12: Optional[str]  # Monetary
    x13: Optional[float]
    x14: Optional[float]
    x15: Optional[float]
    x16: Optional[float]
    x17: Optional[float]
    x18: Optional[float]
    x19: Optional[float]
    x20: Optional[float]
    x21: Optional[float]
    x22: Optional[float]
    x23: Optional[float]
    x24: Optional[float]
    x25: Optional[float]
    x26: Optional[float]
    x27: Optional[float]
    x28: Optional[float]
    x29: Optional[float]
    x30: Optional[float]
    x31: Optional[str]  # Categorical
    x32: Optional[float]
    x33: Optional[float]
    x34: Optional[float]
    x35: Optional[float]
    x36: Optional[float]
    x37: Optional[float]
    x38: Optional[float]
    x39: Optional[float]
    x40: Optional[float]
    x41: Optional[float]
    x42: Optional[float]
    x43: Optional[float]
    x44: Optional[float]
    x45: Optional[float]
    x46: Optional[float]
    x47: Optional[float]
    x48: Optional[float]
    x49: Optional[float]
    x50: Optional[float]
    x51: Optional[float]
    x52: Optional[float]
    x53: Optional[float]
    x54: Optional[float]
    x55: Optional[float]
    x56: Optional[float]
    x57: Optional[float]
    x58: Optional[float]
    x59: Optional[float]
    x60: Optional[float]
    x61: Optional[float]
    x62: Optional[float]
    x63: Optional[str]  # Percentage
    x64: Optional[float]
    x65: Optional[float]
    x66: Optional[float]
    x67: Optional[float]
    x68: Optional[float]
    x69: Optional[float]
    x70: Optional[float]
    x71: Optional[float]
    x72: Optional[float]
    x73: Optional[float]
    x74: Optional[float]
    x75: Optional[float]
    x76: Optional[float]
    x77: Optional[float]
    x78: Optional[float]
    x79: Optional[float]
    x80: Optional[float]
    x81: Optional[str]  # Categorical
    x82: Optional[str]  # Categorical
    x83: Optional[float]
    x84: Optional[float]
    x85: Optional[float]
    x86: Optional[float]
    x87: Optional[float]
    x88: Optional[float]
    x89: Optional[float]
    x90: Optional[float]
    x91: Optional[float]
    x92: Optional[float]
    x93: Optional[float]
    x94: Optional[float]
    x95: Optional[float]
    x96: Optional[float]
    x97: Optional[float]
    x98: Optional[float]
    x99: Optional[float]

    # This is great we can do things to the data or write it for all the columns this is a take home showing I know
    @validator("x5")
    def validate_x5(cls, value):
        allowed_values = [
            "monday",
            "tuesday",
            "friday",
            "saturday",
            "sunday",
            "thursday",
            "wednesday",
        ]
        if value is not None and value not in allowed_values:
            raise ValueError(f"x5 must be one of {', '.join(allowed_values)}")
        return value


class PredictionRequest(BaseModel):
    data: PredictionData


class BatchPredictionRequest(BaseModel):
    data: List[PredictionData]
