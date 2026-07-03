"""
Base repository module.

Implements the Repository Pattern with a generic base class providing
common CRUD operations, reducing duplication across concrete repositories.
"""

from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations for a given model.

    Attributes:
        model: The SQLAlchemy ORM model class this repository manages.
        db: The active database session.
    """

    def __init__(self, model: Type[ModelType], db: Session) -> None:
        """
        Initialize the repository with a model type and DB session.

        Args:
            model: SQLAlchemy ORM model class.
            db: Active SQLAlchemy session.
        """
        self.model = model
        self.db = db

    def get_by_id(self, record_id: int) -> Optional[ModelType]:
        """
        Retrieve a single record by its primary key.

        Args:
            record_id: Primary key value.

        Returns:
            Optional[ModelType]: The matching record, or None if not found.
        """
        return self.db.get(self.model, record_id)

    def create(self, instance: ModelType) -> ModelType:
        """
        Persist a new record to the database.

        Args:
            instance: A new, unsaved ORM model instance.

        Returns:
            ModelType: The persisted instance, refreshed with DB defaults.
        """
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance