from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PORT: int


settings = Settings()
