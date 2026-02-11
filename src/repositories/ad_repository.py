from .base_repository import BaseRepository
from models import Ad


class AdRepository(BaseRepository[Ad]):
    """Repository for Ad entity."""
    
    def __init__(self):
        super().__init__(Ad, "ads")
    
    def _row_to_model(self, row) -> Ad:
        return Ad(
            id=row['id'],
            sponsor=row['sponsor'],
            image_path=row['image_path'] or '',
            duration=row['duration'] or 0
        )
    
    def _model_to_dict(self, model: Ad) -> dict:
        return {
            'id': model.id,
            'sponsor': model.sponsor,
            'image_path': model.image_path,
            'duration': model.duration
        }
