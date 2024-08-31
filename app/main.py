
import uvicorn
from fastapi import FastAPI
from app.core.app_config import port_number

app = FastAPI()

@app.get('/')
def welcome_application():
    return 'Welcome to the User-management Microservice'


if __name__ == '__main__':
    uvicorn.run(app,host='localhost',port=port_number)

