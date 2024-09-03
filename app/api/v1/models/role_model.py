from pydantic import BaseModel


class RoleDetailsModel(BaseModel):
    role_name:str


class RoleResponseModel(BaseModel):
    role:str
    status:str