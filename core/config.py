from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
