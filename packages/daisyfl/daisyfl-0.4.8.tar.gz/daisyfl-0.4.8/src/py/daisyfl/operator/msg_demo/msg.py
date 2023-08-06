from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

# keys
WHO_CREATE_THIS_DEMO = "WHO_CREATE_THIS_DEMO"
TIME = "TIME"
STUDENT = "STUDENT"

# Enum
class Time(Enum):
    """Type of the SecAgg stages."""
    SAY_HI = 0
    TRAIN = 1

# dataclass
@dataclass_json
@dataclass
class Student:
    name: str
    age: int
    graduate: bool
