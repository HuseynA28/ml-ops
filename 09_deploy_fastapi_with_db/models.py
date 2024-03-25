from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Advertising(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tv: float
    radio: float
    newspaper: float
    prediction: float
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str

class Iris(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    prediction: str
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str

class CreateUpdateIris(SQLModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }


class CreateUpdateAdvertising(SQLModel):
    tv: float
    radio: float
    newspaper: float

    class Config:
        schema_extra = {
            "example": {
                "tv": 230.1,
                "radio": 37.8,
                "newspaper": 69.2,
            }
        }
