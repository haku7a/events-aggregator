from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USERNAME: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE_NAME: str = "dbname"

    EVENTS_PROVIDER_BASE_URL: str
    EVENTS_PROVIDER_API_KEY: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE_NAME}"


settings = Settings()
