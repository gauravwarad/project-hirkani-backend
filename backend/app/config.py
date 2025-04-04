from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://gaurav:banana@localhost:5432/hirkani_v1"

    class Config:
        env_file = ".env"

settings = Settings()