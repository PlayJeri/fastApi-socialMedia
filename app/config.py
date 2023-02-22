from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_uri: str
    test_database_uri: str
    oauth_secret: str
    oauth_algorithm: str
    access_token_expire_time: int
    cors_origins: str

    class Config:
        env_file = ".env"

settings = Settings()
