"""
Base repository module.

Implements the Repository Pattern with a generic base class providing
common CRUD and pagination operations, reducing duplication across
concrete repositories.
"""

from typing import Any, Generic, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD and pagination operations.

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

    def delete(self, instance: ModelType) -> None:
        """
        Delete a record from the database.

        Args:
            instance: The ORM model instance to delete.

        Returns:
            None
        """
        self.db.delete(instance)
        self.db.commit()

    def count(self) -> int:
        """
        Count the total number of records for this model.

        Returns:
            int: Total record count.
        """
        statement = select(func.count()).select_from(self.model)
        return self.db.execute(statement).scalar_one()

    def list_paginated(self, offset: int, limit: int, order_desc: bool = True) -> Sequence[ModelType]:
        """
        Retrieve a page of records, ordered by primary key descending by default.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.
            order_desc: Whether to order results in descending order.

        Returns:
            Sequence[ModelType]: The requested page of records.
        """
        pk_column = self.model.__mapper__.primary_key[0]
        order_clause = pk_column.desc() if order_desc else pk_column.asc()
        statement = select(self.model).order_by(order_clause).offset(offset).limit(limit)
        return self.db.execute(statement).scalars().all()
