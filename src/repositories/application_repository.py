from typing import List, Optional

from .base_repository import BaseRepository, get_db
from models import Application, Status


class ApplicationRepository(BaseRepository[Application]):
    """Repository for Application entity."""
    
    def __init__(self):
        super().__init__(Application, "applications")
    
    def _row_to_model(self, row) -> Application:
        return Application(
            id=row['id'],
            user_id=row['user_id'],
            offer_id=row['offer_id'],
            status=Status(row['status']) if row['status'] else Status.Applied
        )
    
    def _model_to_dict(self, model: Application) -> dict:
        return {
            'id': model.id,
            'user_id': model.user_id,
            'offer_id': model.offer_id,
            'status': model.status.value
        }
    
    def get_by_user(self, user_id: int) -> List[Application]:
        """Get all applications for a specific user."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE user_id = ?",
                (user_id,)
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def get_by_offer(self, offer_id: int) -> List[Application]:
        """Get all applications for a specific offer."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE offer_id = ?",
                (offer_id,)
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def get_by_user_and_offer(self, user_id: int, offer_id: int) -> Optional[Application]:
        """Get application by user and offer."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE user_id = ? AND offer_id = ?",
                (user_id, offer_id)
            )
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
