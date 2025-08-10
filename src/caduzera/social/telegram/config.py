from typing import Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict

class TelegramSettings(BaseSettings):
    # tolerante: ignora extras e case-insensitive
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    TELEGRAM_SESSION_NAME: str = "user_session"
    TELEGRAM_TARGET: Optional[Union[int, str]] = "me"
    TELEGRAM_CHANNEL_ID: Optional[Union[int, str]] = None
    ALLOWED_CHATS: Optional[str] = None  # CSV (ex.: -100..., @canal)

