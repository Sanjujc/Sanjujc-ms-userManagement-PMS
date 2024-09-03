from datetime import datetime

from pydantic import BaseModel


class UserRegistrationDetails(BaseModel):
    user_name: str
    email: str
    hashed_password: str
    role_id: str
    created_time: datetime
    updated_time: datetime


class ResponseUserRegistration(BaseModel):
    user_name:str
    status:str