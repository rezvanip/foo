from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Company(BaseModel):
    name: str
    logo_path: str
    location: str
    description: str
