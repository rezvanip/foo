from .base_repository import BaseRepository
from models import Company


class CompanyRepository(BaseRepository[Company]):
    """Repository for Company entity."""
    
    def __init__(self):
        super().__init__(Company, "companies")
    
    def _row_to_model(self, row) -> Company:
        return Company(
            id=row['id'],
            name=row['name'],
            logo_path=row['logo_path'] or '',
            location=row['location'] or '',
            description=row['description'] or ''
        )
    
    def _model_to_dict(self, model: Company) -> dict:
        return {
            'id': model.id,
            'name': model.name,
            'logo_path': model.logo_path,
            'location': model.location,
            'description': model.description
        }
