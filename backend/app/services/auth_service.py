from app.db.models import UserInDB, UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.database import get_database
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

class AuthService:
    @staticmethod
    async def create_user(user_in: UserCreate) -> UserInDB:
        db: AsyncIOMotorClient = await get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_in.email})
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = get_password_hash(user_in.password)
        
        # Create user document
        user_dict = user_in.dict()
        user_dict["password_hash"] = hashed_password
        del user_dict["password"]
        
        # Insert user
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        
        return UserInDB(**user_dict)
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": email})
        if not user:
            return None
        
        # Verify password
        if not verify_password(password, user["password_hash"]):
            return None
        
        return UserInDB(**user)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        user = await db.users.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        from bson import ObjectId
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return UserInDB(**user)
        return None
