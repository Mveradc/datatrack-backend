from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    # Security
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    
    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # MongoDB
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str

    class Config:
        env_file = ".env"

settings = Settings()
