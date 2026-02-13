"""Repository for user entity with authentication lookup methods."""
from typing import Optional

from .base_repository import BaseRepository
from models import User


class UserRepository(BaseRepository[User]):
    """Handles database operations for user accounts with lookup by credentials."""
    
    def __init__(self):
        """Initialize repository with User model and users table."""
        super().__init__(User, "users")
    
    def _row_to_model(self, row) -> User:
        """Convert database row to User model instance."""
        return User(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            full_name=row['full_name'],
            email=row['email'],
            profile_path=row['profile_path'] or '',
            resume_path=row['resume_path'] or '',
            bio=row['bio'] or '',
            skills_text=row['skills_text'] or ''
        )
    
    def _model_to_dict(self, model: User) -> dict:
        """Convert User model to dictionary for database operations."""
        return {
            'id': model.id,
            'username': model.username,
            'password': model.password,
            'full_name': model.full_name,
            'email': model.email,
            'profile_path': model.profile_path,
            'resume_path': model.resume_path,
            'bio': model.bio,
            'skills_text': model.skills_text
        }
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by unique username for login authentication."""
        from database import get_db
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email address."""
        from database import get_db
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
