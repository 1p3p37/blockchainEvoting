from typing import Any, Optional

import pyotp
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUD
from app.models.admin import Admin


class CRUDAdmin(CRUD):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.email == email).first()

    def create(self, db: Session, *, obj_in: dict[str, Any]) -> Admin:
        db_obj = Admin(
            email=obj_in["email"],
            hashed_password=get_password_hash(obj_in["password"]),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Admin, obj_in: dict[str, Any]) -> Admin:
        if obj_in["password"]:
            hashed_password = get_password_hash(obj_in["password"])
            del obj_in["password"]
            obj_in["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[Admin]:
        admin = self.get_by_email(db, email=email)
        if not admin:
            return None
        if not verify_password(password, admin.hashed_password):
            return None
        return admin

    def totp_verify(self, admin: Admin, key: str) -> Optional[Admin]:
        totp = pyotp.totp.TOTP(admin.auth_token)
        return totp.verify(key)


admin = CRUDAdmin(Admin)
