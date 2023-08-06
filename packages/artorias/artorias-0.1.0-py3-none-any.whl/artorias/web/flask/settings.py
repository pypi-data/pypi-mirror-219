from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    UNKNOWN_EXCEPTION_MESSAGE: str = "Server error"
    LOGGER_FORMAT_STRING: str = "[%(asctime)s] [%(levelname)-7s] %(thread)s in [%(module)-30s]: %(message)s"
    SQLALCHEMY_DATABASE_URI: str = "sqlite://"
    CACHE_TYPE: str = "SimpleCache"
