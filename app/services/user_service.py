import traceback
from loguru import logger
from select import error
import bcrypt

from app.api.v1.models.user_model import ResponseUserRegistration
from app.constant import ResponseMessage
from app.db.models import UserClass, RoleDetails


class UserService:

    def __str__(self):
        return 'User service class invoked'

    @staticmethod
    def hash_password(password):
        try:
            logger.info('hashing the password')
            encoded_password = password.encode('utf-8')
            password_salt = bcrypt.gensalt()
            hash_password =  bcrypt.hashpw(encoded_password,password_salt)
            logger.info('hashing is success')
            return hash_password
        except Exception as e:
            logger.error('Error occurred hashing password')
            traceback.print_exc()
            raise e

    @staticmethod
    def user_registration(user_name, email, role_id, password, db_session):
        try:
            role_details = db_session.query(RoleDetails).filter(RoleDetails.role_id == role_id).first()
            if role_details:
                hashed_password = UserService().hash_password(password)
                new_user = UserClass(user_name=user_name,email=email,role_id=role_id,hashed_password=hashed_password)
                db_session.add(new_user)
                db_session.commit()
                return ResponseUserRegistration(user_name=user_name,status=ResponseMessage.user_registration_success)
        except Exception as e:
            db_session.rollback()
            raise