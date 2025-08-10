import asyncio
from typing import Optional, Union
from telethon import TelegramClient
from .client import get_settings

def send_text_once(text: str, target: Optional[Union[int, str]] = None):
    """
    Conecta, envia e desconecta em um único loop (ideal p/ relatórios/alertas).
    Usa TELEGRAM_TARGET como padrão se 'target' não for passado.
    """
    s = get_settings()
    t = target or s.TELEGRAM_TARGET or "me"

    async def _run():
        client = TelegramClient(s.TELEGRAM_SESSION_NAME, s.TELEGRAM_API_ID, s.TELEGRAM_API_HASH)
        await client.start()
        await client.send_message(t, text)
        await client.disconnect()

    asyncio.run(_run())
