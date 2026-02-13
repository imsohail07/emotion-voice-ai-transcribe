from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Emotion Voice AI"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "*"

    class Config:
        env_file = ".env"

settings = Settings()
