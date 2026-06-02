from app.db.models import UserInDB
from app.core.database import get_database
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime

class UserService:
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return UserInDB(**user)
        return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        user = await db.users.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None
    
    @staticmethod
    async def get_users(skip: int = 0, limit: int = 100) -> List[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        users = []
        cursor = db.users.find().skip(skip).limit(limit)
        async for user in cursor:
            users.append(UserInDB(**user))
        return users
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[UserInDB]:
        db: AsyncIOMotorClient = await get_database()
        update_data["updated_at"] = datetime.utcnow()
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await UserService.get_user_by_id(user_id)
        return None
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        db: AsyncIOMotorClient = await get_database()
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
