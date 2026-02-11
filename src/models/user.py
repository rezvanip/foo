from typing import List
from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class User(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    profile_path: str
    resume_path: str
    bio: str
    skills_text: str

    def get_skills(self) -> List[str]:
        return self.skills_text.split(', ') if self.skills_text else []
