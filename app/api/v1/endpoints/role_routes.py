from loguru import logger
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.v1.models.role_model import RoleDetailsModel
from app.db.models import RoleDetails
from app.db.session import get_db
from app.services.role_service import RoleServiceClass

role_routes = APIRouter(prefix='/role_details',tags=['RoleSection'])

@role_routes.post('/')
def add_user_role(role_model:RoleDetailsModel,db:Session=Depends(get_db)):
    try:
        role_name = role_model.role_name
        final_json = RoleServiceClass().add_new_role(role_name,db)
        return final_json
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding role: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

