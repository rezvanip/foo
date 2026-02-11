from dataclasses import dataclass


@dataclass
class BaseModel:
    """Base class for all models with common functionality."""
    id: int
