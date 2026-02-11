from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Ad(BaseModel):
    sponsor: str
    image_path: str
    duration: int
