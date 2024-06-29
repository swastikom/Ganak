from enum import Enum
import json
from fastapi import APIRouter,HTTPException
from functions.auth import get_password_hash
from pydantic import BaseModel,EmailStr
from schemas.schemas import User

from functions.password_reset import generate_otp, get_saved_otp_from_database, send_email
from models.password_reset_model import RequestData, newPasswordSave

router = APIRouter()

class Tags(Enum):
    password_reset = "Password Reset Routes"



@router.post("/password_reset/request", tags=[Tags.password_reset])
def request_password_reset(request_data: RequestData):
    email = request_data.email
    print(f"Received request with email: {email}")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="User with specified email not found")

    otp = generate_otp()
    user.otp = otp 
    user.save()  

    message = f"Your OTP for password reset is: {otp}"
    send_email(email, message)

    return json.loads(user.to_json())




@router.post("/password_reset/verify", tags=[Tags.password_reset])
def verify_otp(request_data: newPasswordSave):

    otp = request_data.otp

    # Retrieve the saved OTP from your database or cache for verification
    saved_otp = get_saved_otp_from_database(request_data.email)

    if otp == saved_otp:
        otp = "NULL"
        user = User.objects.get(email=request_data.email)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid User")
        user.otp = otp
        new_password = request_data.newPassword
        user.password = get_password_hash(new_password)
        user.save()
        newly_saved_user = json.loads(user.to_json())
        return {"Updated User": newly_saved_user,"Message": "OTP Verified"}

    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    

