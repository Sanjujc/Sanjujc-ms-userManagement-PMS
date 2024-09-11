from venv import logger
from zipfile import error

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.constant import UserResponseMessage, LoginResponseMessage
from app.db.models import UserClass
from app.db.session import get_db


class LoginService:


    def __str__(self):
        return 'Login service is initiated'

    @staticmethod
    def authenticate_user_details(key_check, table_col, db_session):
        logger.info(f'Checking constraints: looking for {key_check} in column {table_col}')
        try:
            check_exist = db_session.query(UserClass).filter(table_col == key_check).first()
            if check_exist:
                logger.info(f'{key_check} already present')
                return check_exist
            return False
        except Exception as e:
            logger.error(f'Error occurred while checking constraints: {e}')
            raise e

    def authenticate_password(self):
        try:
            pass
        except Exception as e:
            pass

    @staticmethod
    def login_user(user_name, user_email, user_password, db_session):
        try:
            user_details = LoginService().authenticate_user_details(user_name, UserClass.user_name, db_session)
            if not user_details :
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=LoginResponseMessage.user_name
                )
            return user_details
        except HTTPException as http:
            raise http
        except Exception as e:
            raise e