from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings using Pydantic Settings"""
    
    # Database Configuration
    db_name: str = os.getenv("DB_NAME", "bookstore.db")
    
    # Server Configuration
    port: int = int(os.getenv("PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Application Configuration
    app_name: str = "FastAPI Book Management API"
    app_version: str = "1.0.0"
    app_description: str = "Book Management API with SQLite database"
    
    # Database URL
    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.db_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings() 