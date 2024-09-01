import datetime
import uuid

from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.dialects.mssql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class UserClass(Base):
    __tablename__  = "userDetails"
    user_id : Mapped[str] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_name : Mapped[str] = mapped_column(String(50),nullable=False)
    email : Mapped[str] = mapped_column(String(50),nullable=False)
    hashed_password : Mapped[str] =  mapped_column(String(50),nullable=False)
    # role_id: Mapped[str] = mapped_column(UUID(as_uuid=True),ForeignKey('role_details.role_id'),nullable=False)
    created_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.utcnow,
                                                            onupdate=datetime.datetime.utcnow())
