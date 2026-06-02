from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.models import UserResponse, UserCreate

# User schemas (reuse models for now)
UserCreateSchema = UserCreate
UserResponseSchema = UserResponse
