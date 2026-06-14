from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Инвистиции'
    database_url: str | None = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'root@admin.ru'
    first_superuser_password: Optional[str] = 'root'

    project_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
