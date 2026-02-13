"""Abstract base repository providing generic CRUD operations."""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Type

from database import get_db
from models import BaseModel


T = TypeVar('T', bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Generic repository abstracting database operations for any model type."""
    
    def __init__(self, model_class: Type[T], table_name: str):
        """Initialize with model class and database table name."""
        self.model_class = model_class
        self.table_name = table_name
    
    @abstractmethod
    def _row_to_model(self, row) -> T:
        """Convert SQLite row to model instance."""
        pass
    
    @abstractmethod
    def _model_to_dict(self, model: T) -> dict:
        """Convert model to dictionary for SQL operations."""
        pass
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve single entity by primary key."""
        with get_db() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self.table_name} WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
    
    def get_all(self) -> List[T]:
        """Fetch all entities from table."""
        with get_db() as conn:
            cursor = conn.execute(f"SELECT * FROM {self.table_name}")
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def create(self, model: T) -> T:
        """Insert new entity and populate generated ID."""
        data = self._model_to_dict(model)
        # Remove 'id' if it's 0 or None (let SQLite auto-generate)
        if 'id' in data and (data['id'] == 0 or data['id'] is None):
            del data['id']
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        
        with get_db() as conn:
            cursor = conn.execute(
                f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
                tuple(data.values())
            )
            # Update model with generated ID
            if cursor.lastrowid is not None:
                model.id = cursor.lastrowid
        
        return model
    
    def update(self, model: T) -> T:
        """Update existing entity by ID."""
        data = self._model_to_dict(model)
        id_value = data.pop('id')
        
        set_clause = ', '.join(f"{k} = ?" for k in data.keys())
        
        with get_db() as conn:
            conn.execute(
                f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?",
                tuple(data.values()) + (id_value,)
            )
        
        return model
    
    def delete(self, id: int) -> bool:
        """Remove entity by ID, returning success status."""
        with get_db() as conn:
            cursor = conn.execute(
                f"DELETE FROM {self.table_name} WHERE id = ?",
                (id,)
            )
            return cursor.rowcount > 0
