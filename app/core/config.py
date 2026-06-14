from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Инвистиции'
    database_url: str | None = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'root@admin.ru'
    first_superuser_password: Optional[str] = 'root'

    # OAuth 2.0
    # project_id_oauth: Optional[str] = None
    # client_id_oauth: Optional[str] = None
    # client_secret_oauth: Optional[str] = None

    # Service Account
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env', extra="ignore")


settings = Settings()
