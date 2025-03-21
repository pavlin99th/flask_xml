from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load and validate env settings."""

    model_config = SettingsConfigDict(env_file=find_dotenv())

    sqlite_db: str = "db.sqlite"
    sqlite_folder: str = "database"
    sqlalchemy_echo: bool = True


settings = Settings()
