import os
import pathlib
import sys
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from telethon import TelegramClient
from .config import TelegramSettings

_settings: Optional[TelegramSettings] = None
_client: Optional[TelegramClient] = None

def _load_env_once():
    # tenta carregar .env do CWD ou subindo diretórios; se já tiver vars, não faz nada
    if os.getenv("TELEGRAM_API_ID") and os.getenv("TELEGRAM_API_HASH"):
        return
    path = find_dotenv(usecwd=True)
    if not path:
        # plano B: pasta do script principal
        try:
            path = pathlib.Path(sys.argv[0]).resolve().parent / ".env"
            if not path.exists():
                path = ""
        except Exception:
            path = ""
    if path:
        load_dotenv(path, override=False)

def get_settings() -> TelegramSettings:
    global _settings
    if _settings is None:
        _load_env_once()
        _settings = TelegramSettings()
    return _settings

def get_client() -> TelegramClient:
    global _client
    if _client is None:
        s = get_settings()
        _client = TelegramClient(s.TELEGRAM_SESSION_NAME, s.TELEGRAM_API_ID, s.TELEGRAM_API_HASH)
    return _client
