
from enum import Enum
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from functions.auth import get_current_user, get_password_hash
from pydantic import BaseModel,EmailStr
from schemas.schemas import User
from datetime import datetime
from fastapi import status
from functions.auth import authenticate_user, create_access_token
from datetime import timedelta

class CreateUserRequest(BaseModel):
    firstname: str
    secondname: str
    email: EmailStr
    password: str
    age: int
    address: str
    gender: str

class LoginData(BaseModel):
    email: EmailStr
    password: str

class UpdateUserRequest(BaseModel):
    firstname: str
    secondname: str
    email: EmailStr
    age: int
    address: str
    gender: str