from pydantic_settings import BaseSettings
from typing import Optional, Union

class TelegramSettings(BaseSettings):
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    TELEGRAM_SESSION_NAME: str = "user_session"
    TELEGRAM_TARGET: Optional[str] = "me"   # destino padrão p/ envios
    TELEGRAM_CHANNEL_ID: Optional[Union[int, str]] = None     # CSV com @nomes ou IDs

    class Config:
        # por padrão lê um .env no diretório atual do processo
        env_file = ".env"
