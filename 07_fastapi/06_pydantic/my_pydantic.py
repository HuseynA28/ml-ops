import json

from pydantic import BaseModel, ValidationError, Field
from typing import List
from enum import Enum


class Classes(str, Enum):
    PHYS101 = "Physics I"
    PHYS125 = "Calculational Methods In Physics"
    PHYS150 = "Information and Entropy"


class Student(BaseModel):
    name: str=Field(default=None, max_length=50, min_length=3)
    email: str=Field(default=None, max_length=50, min_length=3)
    faculty: str=Field(default=None, max_length=50, min_length=3)
    classes: List[Classes]=[]
    grade: int=Field(default=1, gt=0, lt=5)


student1_data = {
    "name": "student1",
    "email": "user1@example.com",
    "faculty": "Physics",
    "classes": [Classes.PHYS101, Classes.PHYS150],
    "grade": 4
}

try:
    student1 = Student(**student1_data)

    schema = student1.schema()
    print(json.dumps(schema))
except ValidationError as e:
    print(e.json())