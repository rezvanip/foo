"""Repository for job application entity with user and offer filtering."""
from typing import List, Optional

from .base_repository import BaseRepository
from models import Application, Status

from database import get_db

class ApplicationRepository(BaseRepository[Application]):
    """Manages job applications linking users to offers with status tracking."""
    
    def __init__(self):
        """Initialize repository with Application model and applications table."""
        super().__init__(Application, "applications")
    
    def _row_to_model(self, row) -> Application:
        """Convert database row to Application model instance."""
        return Application(
            id=row['id'],
            user_id=row['user_id'],
            offer_id=row['offer_id'],
            status=Status(row['status']) if row['status'] else Status.Applied
        )
    
    def _model_to_dict(self, model: Application) -> dict:
        """Convert Application model to dictionary for database operations."""
        return {
            'id': model.id,
            'user_id': model.user_id,
            'offer_id': model.offer_id,
            'status': model.status.value
        }
    
    def get_by_user(self, user_id: int) -> List[Application]:
        """Retrieve all applications submitted by specific user."""

        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE user_id = ?",
                (user_id,)
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def get_by_offer(self, offer_id: int) -> List[Application]:
        """Retrieve all applications for specific job offer."""

        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE offer_id = ?",
                (offer_id,)
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def get_by_user_and_offer(self, user_id: int, offer_id: int) -> Optional[Application]:
        """Check if user already applied to specific offer."""

        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM applications WHERE user_id = ? AND offer_id = ?",
                (user_id, offer_id)
            )
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
