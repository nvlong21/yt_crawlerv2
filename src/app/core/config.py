import os
from enum import Enum

from pydantic import SecretStr, computed_field, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "Crawler"
    APP_DESCRIPTION: str | None = None
    APP_VERSION: str | None = None
    LICENSE_NAME: str | None = None
    CONTACT_NAME: str | None = None
    DATA_DIR: str  = Field(default="/tmp", env="DATA_DIR")


class CryptSettings(BaseSettings):
    SECRET_KEY: SecretStr = SecretStr("secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class DatabaseSettings(BaseSettings):
    pass


class SQLiteSettings(DatabaseSettings):
    SQLITE_URI: str = "./sql_app.db"
    SQLITE_SYNC_PREFIX: str = "sqlite:///"
    SQLITE_ASYNC_PREFIX: str = "sqlite+aiosqlite:///"


class S3Settings(DatabaseSettings):
    S3_ENABLE: bool = Field(default=False, env="S3_ENABLED")
    S3_ACCESSKEY: str = Field(default="", env="S3_ACCESSKEY")
    S3_SECRETKEY: str = Field(default="", env="S3_SECRETKEY")
    S3_USESSL: bool = Field(default=True, env="S3_USESSL")
    S3_BUCKETNAME: str = Field(default="", env="S3_BUCKETNAME")
    S3_USEIAM: bool = Field(default=False, env="S3_USEIAM")
    S3_CLOUDPROVIDER: str = Field(default="aws", env="S3_CLOUDPROVIDER")
    S3_ROOTPATH: str = Field(default="", env="S3_ROOTPATH")
    S3_IAM_ENDPOINT: str = Field(default="", env="S3_IAM_ENDPOINT")
    S3_REGION: str = Field(default="", env="S3_REGION")
    S3_USEVIRTUALHOST: bool = Field(default=False, env="S3_USEVIRTUALHOST")

    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def MYSQL_URI(self) -> str:
    #     credentials = f"{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
    #     location = f"{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
    #     return f"{credentials}@{location}"


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="postgres", env="POSTGRES_DB")
    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    POSTGRES_URL: str | None = Field(default="postgres", env="POSTGRES_URL")
    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_URI(self) -> str:
        credentials = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        location = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"{credentials}@{location}"



class Settings(
    AppSettings,
    SQLiteSettings,
    PostgresSettings,
    S3Settings
):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

settings = Settings()
