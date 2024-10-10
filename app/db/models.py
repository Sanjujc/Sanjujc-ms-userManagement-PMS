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
    is_active:Mapped[Boolean] = mapped_column(BOOLEAN,nullable=False,default=True)
    is_valid :Mapped[Boolean] = mapped_column(BOOLEAN,nullable=False,default=False)
    created_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow,
                                                            onupdate=datetime.datetime.utcnow)
    login_attempts :Mapped[int] = mapped_column(Integer,nullable=True,default=0)
    last_login: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roleMapping.role_id'), nullable=False)

    role = relationship("RoleDetails", back_populates="users")
    sessions = relationship("UserSessionTable", back_populates="user")
    password_resets = relationship("PasswordReset",back_populates="user")
    login_attempt = relationship("LoginAttemptsTable",back_populates="user")


class RoleDetails(Base):
    __tablename__ = "roleMapping"

    role_id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    role: Mapped[str] = mapped_column(String(50),nullable=False)
    permission: Mapped[JSON] = mapped_column(JSON,nullable=False)

    users = relationship("UserClass", back_populates="role")


class UserSessionTable(Base):
    __tablename__ = 'userSession'
    session_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    token: Mapped[Text] = mapped_column(Text,nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    created_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    expired_at: Mapped[datetime.datetime] = mapped_column(DateTime,nullable=True)

    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('userDetails.user_id'), nullable=False)


    user = relationship("UserClass", back_populates="sessions")

#
class PasswordReset(Base):
    __tablename__ = 'password_reset'

    reset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('userDetails.user_id'), nullable=False)
    reset_token: Mapped[Text] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserClass", back_populates="password_resets")

#
class LoginAttemptsTable(Base):
    __tablename__ = "loginAttempts"

    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('userDetails.user_id'), nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    was_successful: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user = relationship("UserClass", back_populates="login_attempt")

