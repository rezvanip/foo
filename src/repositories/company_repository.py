"""Repository for company entity with basic CRUD operations."""
from .base_repository import BaseRepository
from models import Company


class CompanyRepository(BaseRepository[Company]):
    """Manages employer company data and branding information."""
    
    def __init__(self):
        """Initialize repository with Company model and companies table."""
        super().__init__(Company, "companies")
    
    def _row_to_model(self, row) -> Company:
        """Convert database row to Company model instance."""
        return Company(
            id=row['id'],
            name=row['name'],
            logo_path=row['logo_path'] or '',
            location=row['location'] or '',
            description=row['description'] or ''
        )
    
    def _model_to_dict(self, model: Company) -> dict:
        """Convert Company model to dictionary for database operations."""
        return {
            'id': model.id,
            'name': model.name,
            'logo_path': model.logo_path,
            'location': model.location,
            'description': model.description
        }
