import traceback

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from  loguru import logger
from app.api.v1.models.user_model import UserRegistrationDetails
from app.db.session import get_db
from app.services.user_service import UserService

user_routes= APIRouter(prefix='/user_management',tags=['UserRegistration'])

@user_routes.post('/')
def user_registration(user_details:UserRegistrationDetails,db:Session=Depends(get_db)):
    try:
        logger.info('User registration service')
        user_name = user_details.user_name
        email = user_details.email
        role_id = user_details.role_id
        hashed_password = user_details.hashed_password
        final_json = UserService().user_registration(user_name,email,role_id,hashed_password,db)
        if final_json :
            return final_json
    except HTTPException as http_exc:
        logger.error(f"HTTPException occurred: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error('Error registering user',e)
        logger.error(traceback.print_exc())
        raise HTTPException(status_code=500,detail='Internal server Error')

