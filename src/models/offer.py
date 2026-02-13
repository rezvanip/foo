"""Offer model representing job postings from companies."""
from dataclasses import dataclass
from typing import List

from .base_model import BaseModel


@dataclass
class Offer(BaseModel):
    """Job posting with requirements, salary, and company association."""
    company_id: int
    title: str
    skill_tags: str
    salary: float
    description: str
    created_at: int

    def get_skills(self) -> List[str]:
        """Parse skill_tags into list of required skills."""
        return self.skill_tags.split(', ') if self.skill_tags else []
