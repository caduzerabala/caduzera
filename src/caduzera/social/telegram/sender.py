from telethon import TelegramClient
from typing import Optional
from .client import new_client, run_once, settings

# -------- one-shot (síncrono) ----------
def send_text_once(text: str, target: Optional[str] = None):
    """Cria client, envia e fecha (ideal para relatórios/alertas)."""
    s = settings()
    t = target or s.TELEGRAM_TARGET or "me"

    async def _run():
        c = new_client()
        await c.start()
        await c.send_message(t, text)
        await c.disconnect()

    return run_once(_run())

# -------- assíncrono (usar com ensure_started) ----------
async def a_send_text(client: TelegramClient, text: str, target: Optional[str] = None):
    """Usar quando seu bot já tem um loop rodando (receiver, etc.)."""
    from .client import settings
    s = settings()
    await client.send_message(target or s.TELEGRAM_TARGET or "me", text)
