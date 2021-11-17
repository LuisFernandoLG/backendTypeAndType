from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: Optional[int] = 1
    name: str
    surname: str
    second_surname: str
    email: str
    password: str
    typeUser: Optional[int] = 2
