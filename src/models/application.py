"""Application model linking users to job offers with status tracking."""
from dataclasses import dataclass
from enum import Enum

from .base_model import BaseModel


class Status(Enum):
    """Application lifecycle states from submission to decision."""
    Applied = 'applied'
    Pending = 'pending'
    Rejected = 'rejected'
    Accepted = 'accepted'


@dataclass
class Application(BaseModel):
    """User's job application linking them to a specific offer."""
    user_id: int
    offer_id: int
    status: Status
