from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.v1.models.login_model import LoginUser
from app.db.session import get_db
from app.services.login_service import LoginService

login_routes = APIRouter(prefix='/auth',tags=['Authentication'])


@login_routes.post('/login')
def login_user(request:LoginUser,db:Session=Depends(get_db)):
    try:
        user_name = request.user_name
        user_email = request.email
        user_password = request.user_password
        user_details = LoginService().login_user(user_name,user_email,user_password,db)
        return user_details
    except HTTPException as http:
        raise http
    except Exception as e:
        raise HTTPException(status_code=500,detail='Internal server Error')
