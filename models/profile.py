from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience: str
from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    email: str
    linkedin: str | None = None
    github: str | None = None
    skills: list[str]
    experience: str
