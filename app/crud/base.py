from typing import Any, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUD:
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_for_update(self, db: Session, id: Any) -> ModelType:
        return (
            db.query(self.model).filter(self.model.id == id).with_for_update().first()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: dict[str, Any]) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_or_create(
        self, db: Session, *, obj_in: dict[str, Any], defaults=None
    ) -> tuple[ModelType, bool]:
        try:
            return db.query(self.model).filter_by(**obj_in).one(), False
        except NoResultFound:
            if defaults is not None:
                obj_in.update(defaults)
            try:
                db_obj = self.model(**obj_in)
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
                return db_obj, True
            except IntegrityError:
                return db.query(self.model).filter_by(**obj_in).one(), False

    def update_or_create(
        self,
        db: Session,
        *,
        obj_in: dict[str, Any],
        defaults: dict[str, Any],
    ) -> tuple[ModelType, bool]:
        db_obj, created = self.get_or_create(db, obj_in=obj_in, defaults=defaults)
        if not created:
            self.update(db, db_obj=db_obj, obj_in=defaults)

        return db_obj, created
