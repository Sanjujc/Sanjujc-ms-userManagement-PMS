from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.v1.endpoints.role_routes import role_routes
from app.api.v1.endpoints.user_routes import user_routes

from app.db.session import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        logger.info('Initiating FastAPI startup', application)
        init_db()
        yield
    finally:
        logger.info('Closing FastAPI application')

app = FastAPI(lifespan=lifespan)

app.include_router(role_routes)
app.include_router(user_routes)


@app.get('/')
def welcome_application():
    return 'Welcome to the User-management Microservice'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=1234)
