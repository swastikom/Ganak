
from pydantic import BaseModel,EmailStr


class RequestData(BaseModel):
    email: EmailStr
    

class otpVerifyData(BaseModel):
    email: EmailStr
    otp: str


class newPasswordSave(BaseModel):
    otp: str
    email: EmailStr
    newPassword: str