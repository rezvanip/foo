"""Repository for advertisement entity with basic CRUD operations."""
from .base_repository import BaseRepository
from models import Ad


class AdRepository(BaseRepository[Ad]):
    """Manages advertisement data for sponsored content."""
    
    def __init__(self):
        """Initialize repository with Ad model and ads table."""
        super().__init__(Ad, "ads")
    
    def _row_to_model(self, row) -> Ad:
        """Convert database row to Ad model instance."""
        return Ad(
            id=row['id'],
            sponsor=row['sponsor'],
            image_path=row['image_path'] or '',
            duration=row['duration'] or 0
        )
    
    def _model_to_dict(self, model: Ad) -> dict:
        """Convert Ad model to dictionary for database operations."""
        return {
            'id': model.id,
            'sponsor': model.sponsor,
            'image_path': model.image_path,
            'duration': model.duration
        }
