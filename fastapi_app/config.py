"""
FastAPI application settings.
Mirrored from Django settings using Pydantic.
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Django-like settings
    PROJECT_NAME: str = "idmitra_django"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # Security
    SECRET_KEY: str = Field(default="django-insecure-dev-key", alias="DJANGO_SECRET_KEY")
    DEBUG: bool = Field(default=True)
    ALLOWED_HOSTS: list = Field(default=["*"])
    
    # Database - Use SQLite by default, MySQL optional
    DB_ENGINE: str = Field(default="sqlite")  # "sqlite" or "mysql"
    DB_NAME: str = Field(default="db.sqlite3")
    DB_USER: str = Field(default="root")
    DB_PASSWORD: str = Field(default="password")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=3306)
    
    # Internationalization
    LANGUAGE_CODE: str = "en-us"
    TIME_ZONE: str = "UTC"
    USE_I18N: bool = True
    USE_TZ: bool = True
    
    # Static files
    STATIC_URL: str = "/static/"
    
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from settings."""
        if self.DB_ENGINE.lower() == "sqlite":
            # SQLite - no server needed, local file
            db_path = self.BASE_DIR.parent / self.DB_NAME
            return f"sqlite:///{db_path}"
        elif self.DB_ENGINE.lower() == "mysql":
            # MySQL - requires running server
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        else:
            raise ValueError(f"Unsupported DB_ENGINE: {self.DB_ENGINE}")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        populate_by_name = True
        extra = "ignore"


# Create settings instance
settings = Settings()
