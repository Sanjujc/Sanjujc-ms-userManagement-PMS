import traceback

from fastapi import HTTPException
from loguru import logger
import bcrypt
from starlette import status

from app.api.v1.models.user_model import ResponseUserRegistration
from app.constant import UserResponseMessage
from app.db.models import UserClass, RoleDetails
import re

class UserService:

    def __str__(self):
        return 'User service class invoked'

    @staticmethod
    def hash_password(password):
        logger.info('Hashing the password')
        try:
            encoded_password = password.encode('utf-8')
            password_salt = bcrypt.gensalt()
            hash_password =  bcrypt.hashpw(encoded_password,password_salt)
            logger.info('Password hashing successful')
            return hash_password
        except Exception as e:
            logger.error(f'Error occurred while hashing password: {e}')
            traceback.print_exc()
            raise e

    @staticmethod
    def email_validation(email):
        logger.info('Validating email format')
        try:
            regex_mail = r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b'
            regex_match = bool(re.match(regex_mail,email))
            if regex_match:
                logger.info('Email is valid')
                return True
            logger.warning(f'Invalid email format: {email}')
            return False
        except Exception as e:
            logger.error(f'Error occurred during email validation: {e}')
            traceback.print_exc()
            raise e
    @staticmethod
    def check_constrains(key_check,table_col,db_session):
        logger.info(f'Checking constraints: looking for {key_check} in column {table_col}')
        try:
            check_exist = db_session.query(UserClass).filter(table_col == key_check).first()
            if check_exist:
                logger.info(f'{key_check} already present')
                return True
            return False
        except Exception as e:
            logger.error(f'Error occurred while checking constraints: {e}')
            raise e
    @staticmethod
    def user_registration(user_name, email, role_id, password, db_session):
        try:
            if UserService().check_constrains(user_name,UserClass.user_name,db_session):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=UserResponseMessage.user_name_exist
                )
            if  UserService().check_constrains(email,UserClass.email,db_session):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=UserResponseMessage.email_exist
                )
            user_email_validation = UserService().email_validation(email)
            if not user_email_validation:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=UserResponseMessage.user_registration_email_validation_failed
                )
            role_details = db_session.query(RoleDetails).filter(RoleDetails.role_id == role_id).first()
            if not role_details:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role not found"
                )
            hashed_password = UserService().hash_password(password)
            new_user = UserClass(user_name=user_name,email=email,role_id=role_id,hashed_password=hashed_password)
            db_session.add(new_user)
            db_session.commit()
            return ResponseUserRegistration(user_name=user_name, status=UserResponseMessage.user_registration_success)
        except HTTPException as http_exc:
            logger.error(f"HTTPException occurred during user registration: {http_exc.detail}")
            raise http_exc
        except Exception as e:
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during user registration"
            ) from e