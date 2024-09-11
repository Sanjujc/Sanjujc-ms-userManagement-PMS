from pydantic import BaseModel


class LoginUser(BaseModel):
    user_name:str
    user_password:str
    email:str

