from enum import Enum
import json
from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import User
from functions.clinic_function import getClinic
from functions.auth import get_current_user 

router = APIRouter()

class Tags(Enum):
    clinics = "Find nearest clinics"
    
@router.get("/users/find_clinic", tags=[Tags.clinics])
async def delete_current_user(current_user: User = Depends(get_current_user)):
    try:
        
        clinics_got = getClinic("Mental health clincs near"+current_user.address)
        return json.loads(clinics_got)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))