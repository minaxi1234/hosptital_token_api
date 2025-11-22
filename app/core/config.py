from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # REDIS_HOST: str 
    # REDIS_PORT: int 

    class Config:
        env_file = ".env"


settings = Settings()


