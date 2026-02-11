from dataclasses import dataclass
from enum import Enum

from .base_model import BaseModel


class Status(Enum):
    Applied = 'applied'
    Pending = 'pending'
    Rejected = 'rejected'
    Accepted = 'accepted'


@dataclass
class Application(BaseModel):
    user_id: int
    offer_id: int
    status: Status
