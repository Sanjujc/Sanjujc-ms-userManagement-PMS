from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from loguru import logger
from app.constant import UserResponseMessage, LoginResponseMessage
from app.db.models import UserClass
from passlib.context import CryptContext


class LoginService:

    def __str__(self):
        return 'Login service is initiated'

    @staticmethod
    def authenticate_user_details(key_check, table_col, db_session):
        logger.info(f'Checking constraints: looking for {key_check} in column {table_col}')
        try:
            check_exist = db_session.query(UserClass).filter(table_col == key_check).first()
            if check_exist:
                logger.info(f'{key_check} is present')
                return check_exist
        except Exception as e:
            logger.error(f'Error occurred while checking constraints: {e}')
            raise e

    @staticmethod
    def authenticate_password(user_password, hashed_password):
        try:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if not pwd_context.verify(user_password, hashed_password):
                logger.warning("Password verification failed.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=LoginResponseMessage.invalid_credentials
                )
            return True
        except Exception as e:
            logger.error(f'Error occurred during password verification: {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during password verification"
            )

    @staticmethod
    def login_user(user_name, user_email, user_password, db_session):
        try:
            # Authenticate user by username or email (you may want to allow both)
            user_details = LoginService().authenticate_user_details(user_name, UserClass.user_name, db_session)
            if not user_details:
                logger.warning("User not found.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=LoginResponseMessage.user_not_found
                )
            hashed_password = user_details.hashed_password
            # Authenticate password
            LoginService().authenticate_password(user_password, hashed_password)

            # Return successful login response (customize as needed)
            return {"status": "success", "message": "Login successful"}
        except HTTPException as http:
            raise http
        except Exception as e:
            logger.error(f'Unexpected error during login: {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
