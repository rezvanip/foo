"""Repository for job offer entity with company filtering."""
from typing import List

from .base_repository import BaseRepository
from models import Offer


class OfferRepository(BaseRepository[Offer]):
    """Handles job posting data with filtering by company."""
    
    def __init__(self):
        """Initialize repository with Offer model and offers table."""
        super().__init__(Offer, "offers")
    
    def _row_to_model(self, row) -> Offer:
        """Convert database row to Offer model instance."""
        return Offer(
            id=row['id'],
            company_id=row['company_id'],
            title=row['title'],
            skill_tags=row['skill_tags'] or '',
            salary=row['salary'] or 0.0,
            description=row['description'] or '',
            created_at=row['created_at'] or 0
        )
    
    def _model_to_dict(self, model: Offer) -> dict:
        """Convert Offer model to dictionary for database operations."""
        return {
            'id': model.id,
            'company_id': model.company_id,
            'title': model.title,
            'skill_tags': model.skill_tags,
            'salary': model.salary,
            'description': model.description,
            'created_at': model.created_at
        }
    
    def get_by_company(self, company_id: int) -> List[Offer]:
        """Retrieve all job offers posted by specific company."""
        from database import get_db
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM offers WHERE company_id = ?",
                (company_id,)
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]
