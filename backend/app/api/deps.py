from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_database
from app.db.models import UserInDB
from app.core.security import verify_token
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    db: AsyncIOMotorClient = await get_database()
    user = await db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return UserInDB(**user)

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Role-based dependencies
def get_current_admin(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_teacher(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_student(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role not in ["student", "teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_parent(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role not in ["parent", "admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
