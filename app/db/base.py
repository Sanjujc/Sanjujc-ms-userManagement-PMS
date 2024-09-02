from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.app_config import DATABASE_URL


class Base(DeclarativeBase):
    pass

