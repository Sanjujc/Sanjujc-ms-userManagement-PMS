from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, select

from app.core.permission import permissions
from app.db.base import Base
from app.db.models import UserClass, RoleDetails

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost/pms_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    admin_user = (insert(RoleDetails).values(role='admin', permission=permissions))
    with engine.connect() as conn:
        check_admin = select(RoleDetails).where(RoleDetails.role == "admin")
        admin_details =  conn.execute(check_admin)
        if not admin_details:
            conn.execute(admin_user)
            conn.commit()
            print("Admin role created successfully.")
        else:
            print("Admin role already exists.")