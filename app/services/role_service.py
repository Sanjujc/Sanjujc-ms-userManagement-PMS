import traceback
from distutils.command.check import check
from fastapi import HTTPException
from loguru import logger

from app.api.v1.models.role_model import RoleResponseModel
from app.db.models import RoleDetails, UserClass


class RoleServiceClass:
    def __str__(self):
        return 'Role class is initialized '

    @staticmethod
    def check_role(db_session, role_name):
        try:
            logger.info('Checking role already mapped or not')
            role_details = db_session.query(RoleDetails).filter(RoleDetails.role == role_name).first()
            if role_details:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Error checking role: \n" + traceback.format_exc())
            raise e

    @staticmethod
    def add_new_role(role_name:str, db_session):
        try:
            if RoleServiceClass().check_role(db_session,role_name):
                raise HTTPException(status_code=400, detail="Role already exists")
            new_role = RoleDetails(role=role_name.lower())
            logger.info(f'Role mapping initiated for:{new_role}')
            db_session.add(new_role)
            db_session.commit()
            role_data = {
                "role": role_name,
                "status":'Active'
            }
            return RoleResponseModel(**role_data)
        except Exception as e:
            logger.error('Error mapping roles', e)
            raise