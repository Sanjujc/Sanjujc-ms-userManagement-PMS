from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.models import UserClass
from app.db.session import get_db


class LoginService:


    def __str__(self):
        return 'Login service is initiated'


    def authenticate_user(self):
        try:
            pass
        except Exception as e:
            pass

    def authenticate_password(self):
        try:
            pass
        except Exception as e:
            pass

    def login_user(self,user_name,user_email,user_password,db_session):
        try:
            user_details = db_session.query(UserClass).filter(UserClass.user_name== user_name).first()
            if not user_details:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Username not found')

            return user_details
        except HTTPException as http:
            raise http
        except Exception as e:
            raise e