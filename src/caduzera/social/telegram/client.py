import os, pathlib, sys, asyncio
from typing import Optional
from dotenv import load_dotenv
from telethon import TelegramClient
from .config import TelegramSettings

_client: Optional[TelegramClient] = None

def _auto_load_env():
    """Carrega .env do CWD ou da pasta do script principal, se existir."""
    if os.getenv("TELEGRAM_API_ID") and os.getenv("TELEGRAM_API_HASH"):
        return
    candidates = [pathlib.Path.cwd() / ".env"]
    try:
        candidates.append(pathlib.Path(sys.argv[0]).resolve().parent / ".env")
    except Exception:
        pass
    for p in candidates:
        if p.exists():
            load_dotenv(p)
            break

def settings() -> TelegramSettings:
    _auto_load_env()
    return TelegramSettings()

# --------- Modo síncrono “one-shot” (cria, conecta, usa, desconecta) ---------
def run_once(coro):
    """Executa um coroutine em um loop novo (one-shot)."""
    return asyncio.run(coro)

def new_client() -> TelegramClient:
    """Cria um client NOVO (não compartilhado). Use em one-shot."""
    s = settings()
    return TelegramClient(s.TELEGRAM_SESSION_NAME, s.TELEGRAM_API_ID, s.TELEGRAM_API_HASH)

# --------- Modo assíncrono “longo” (um loop seu) ---------
def get_client() -> TelegramClient:
    """Singleton para uso assíncrono (receivers/serviços)."""
    global _client
    if _client is None:
        s = settings()
        _client = TelegramClient(s.TELEGRAM_SESSION_NAME, s.TELEGRAM_API_ID, s.TELEGRAM_API_HASH)
    return _client

async def ensure_started() -> TelegramClient:
    """Garante que o singleton está conectado (para uso em apps async)."""
    c = get_client()
    if not c.is_connected():
        await c.start()  # 1ª vez pede login
    return c
