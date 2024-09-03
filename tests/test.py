import datetime
import uuid

from sqlalchemy import create_engine, Integer, String, UUID, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost/pms_db"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL logging

Base = declarative_base()

class UserClass(Base):
    __tablename__ = "userDetails"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(50), nullable=False)
    # role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('role_details.role_id'), nullable=False)
    created_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow,
                                                            onupdate=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)  # This should create the table

