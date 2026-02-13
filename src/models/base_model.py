"""Base model with common attributes for all entities."""
from dataclasses import dataclass


@dataclass
class BaseModel:
    """Abstract base providing primary key for all data models."""
    id: int
