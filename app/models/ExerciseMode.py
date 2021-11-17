from typing import Optional
from pydantic import BaseModel


class ExerciseModel(BaseModel):
    id:  Optional[int] = 1
    title: str
    points: int
    text_content: str
    time: int
    status: Optional[int] = 1
    category: int
    difficulty: int
