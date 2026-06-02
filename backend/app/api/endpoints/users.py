from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models import UserInDB, UserCreate
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.api.deps import get_current_active_user, get_current_admin
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    current_admin: UserInDB = Depends(get_current_admin)
):
    user = await AuthService.create_user(user_in)
    return UserResponse(**user.dict())

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_admin: UserInDB = Depends(get_current_admin)
):
    users = await UserService.get_users(skip=skip, limit=limit)
    return [UserResponse(**user.dict()) for user in users]

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: UserInDB = Depends(get_current_active_user)
):
    return UserResponse(**current_user.dict())

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Users can only view their own profile unless they're admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.dict())

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: dict,
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Users can only update their own profile unless they're admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user = await UserService.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.dict())

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_admin: UserInDB = Depends(get_current_admin)
):
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
