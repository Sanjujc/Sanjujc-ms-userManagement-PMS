from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.models import UserClass

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost/pms_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Initiating FastAPI startup')
    Base.metadata.create_all(bind=engine)  # Create tables on startup
    yield
    logger.info('Closing FastAPI application')

app = FastAPI(lifespan=lifespan)

@app.get('/')
def welcome_application():
    return 'Welcome to the User-management Microservice'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=1234)
