from enum import Enum
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from functions.auth import get_current_user, get_password_hash
from schemas.schemas import User
from datetime import datetime
from fastapi import status
from functions.auth import authenticate_user, create_access_token
from datetime import timedelta
from models.user_model import CreateUserRequest, UpdateUserRequest


router = APIRouter()

class Tags(Enum):
    user = "User CRUD Routes"
    user_auth = "User Authentication Routes"
    

@router.post("/users/create", tags=[Tags.user])
async def create_user(request_data: CreateUserRequest):
    try:
        # Check if a user with the same email already exists
        
        existing_user = User.objects(email=request_data.email).first()
        
        
        if existing_user:
            print("User with this email already exists")
            return HTTPException(status_code=400, detail="User with this email already exists")
        else:
            # Hash the user's password
            hashed_password = get_password_hash(request_data.password)

            # Create a new user
            new_user = User(
                firstname = request_data.firstname,
                secondname = request_data.secondname,
                email = request_data.email,
                password = hashed_password,  
                age = request_data.age,
                address = request_data.address,
                gender = request_data.gender,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )

            new_user.save()

            return {"message": "User created successfully", "user_id": str(new_user.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/users/me", tags=[Tags.user])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return json.loads(current_user.to_json())

    
@router.put("/users/me/update", tags=[Tags.user])
async def update_user_info(
    update_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        

        # Update user information based on the provided data
        current_user.update(**update_data.model_dump(exclude_unset=True))
        current_user.updatedAt = datetime.now()
        current_user.save()

        

        return {"message": "User information updated successfully", "user_id": str(current_user.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.delete("/users/me/delete", tags=[Tags.user])
async def delete_current_user(current_user: User = Depends(get_current_user)):
    try:
        
        # Delete the current user from the database
        current_user.delete()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", tags=[Tags.user_auth])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


