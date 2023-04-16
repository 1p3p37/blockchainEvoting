from uuid import uuid4

import pyotp
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.config import settings
from app.db.base_class import Base


class Admin(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    auth_token = Column(String, nullable=False, default=pyotp.random_base32())

    def get_qr_code_link(self):
        return pyotp.totp.TOTP(self.auth_token).provisioning_uri(
            name=self.email, issuer_name=settings.project_name
        )
