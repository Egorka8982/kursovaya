from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    # База данных
    DATABASE_URL: str = "sqlite:///./animal_hospital.db"
    
    # Настройки приложения
    APP_TITLE: str = "Veterinary Service API"
    APP_DESCRIPTION: str = "API for managing veterinary clinic operations"
    APP_VERSION: str = "1.0.0"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

