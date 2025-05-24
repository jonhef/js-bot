from pydantic_settings import BaseSettings

from os import path

class Settings(BaseSettings):
    GOOGLE_CALENDAR_ID: str
    GOOGLE_CREDENTIALS_FILE: str
    OPENAI_API_KEY: str
    USER_ID: int
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    PHONE_NUMBER: str
    EMAIL: str
    PASSWORD: str
    NAME: str

    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'