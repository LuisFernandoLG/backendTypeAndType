from typing import Optional
from pydantic import BaseModel


class ScoreModel(BaseModel):
    id:  Optional[int] = 1
    last_date: str
    total_score: int
    user_id: int
    exercise_id: int
    time_taken: int
    status: Optional[int] = 1
