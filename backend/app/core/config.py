from pydantic import BaseSettings, Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Student Management System"
    
    # Security Settings
    SECRET_KEY: str = Field(default_factory=lambda: os.urandom(32).hex())
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Database Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "student_management"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # QR Code Settings
    QR_CODE_EXPIRY_MINUTES: int = 5
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
