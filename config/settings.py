from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CALENDAR_ID: str
    GOOGLE_CREDENTIALS_FILE: str
    OPENAI_API_KEY: str
    USER_ID: int
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    PHONE_NUMBER: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'