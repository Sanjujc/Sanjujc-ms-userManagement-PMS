import datetime
import uuid

from sqlalchemy import String, ForeignKey, UUID, DateTime, Text, Boolean, BOOLEAN, Integer, JSON
from sqlalchemy.dialects.mysql import Insert
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.permission import permissions
from app.db.base import Base

class UserClass(Base):
    __tablename__ = "userDetails"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roleMapping.role_id'), nullable=False)
    is_active:Mapped[Boolean] = mapped_column(BOOLEAN,nullable=False,default=True)
    is_valid :Mapped[Boolean] = mapped_column(BOOLEAN,nullable=False,default=False)
    created_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow,
                                                            onupdate=datetime.datetime.utcnow)
    login_attempts :Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    last_login: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)


    role = relationship("RoleDetails", back_populates="users")

class RoleDetails(Base):
    __tablename__ = "roleMapping"

    role_id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    role: Mapped[str] = mapped_column(String(50),nullable=False)
    permission: Mapped[JSON] = mapped_column(JSON,nullable=False)
    users = relationship("UserClass", back_populates="role")

