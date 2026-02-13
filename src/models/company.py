"""Company model representing employers posting job offers."""
from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Company(BaseModel):
    """Employer organization with branding and location details."""
    name: str
    logo_path: str
    location: str
    description: str
