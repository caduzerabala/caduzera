from typing import Iterable, Optional
from telethon import events
from .client import get_client, get_settings

def _norm_allowed(allowed: Optional[Iterable[str|int]]):
    if not allowed:
        return None
    out = set()
    for x in allowed:
        if x is None: 
            continue
        try:
            out.add(int(x))
        except (ValueError, TypeError):
            u = str(x)
            if not u.startswith("@"):
                u = "@" + u
            out.add(u)
    return out

class Receiver:
    """
    Receiver plug-and-play:
      r = Receiver(callback, allowed_chats=None)
      r.start()  # bloqueante; Ctrl+C para parar
    """
    def __init__(self, callback, allowed_chats: Optional[Iterable[str|int]] = None):
        self.callback = callback
        s = get_settings()
        if allowed_chats is None and s.ALLOWED_CHATS:
            allowed_chats = [t.strip() for t in s.ALLOWED_CHATS.split(",") if t.strip()]
        self.allowed = _norm_allowed(allowed_chats)
        # se TELEGRAM_CHANNEL_ID estiver setado e allowed vazio, usa como filtro único
        if not self.allowed and s.TELEGRAM_CHANNEL_ID:
            self.allowed = _norm_allowed([s.TELEGRAM_CHANNEL_ID])
        self.client = get_client()

    async def _run_async(self):
        if not self.client.is_connected():
            await self.client.start()

        @self.client.on(events.NewMessage)
        async def _handler(event):
            chat = await event.get_chat()
            is_group_like = getattr(chat, "title", None) or getattr(chat, "megagroup", False) or getattr(chat, "broadcast", False)
            if not is_group_like:
                return
            if self.allowed:
                username = getattr(chat, "username", None)
                if (event.chat_id not in self.allowed) and not (username and ("@" + username) in self.allowed):
                    return

            sender = await event.get_sender()
            payload = {
                "chat_id": event.chat_id,
                "chat_title": getattr(chat, "title", None),
                "sender_id": getattr(sender, "id", None),
                "sender_username": getattr(sender, "username", None),
                "text": event.raw_text or "",
                "date": event.date,
                "message_id": event.id,
            }

            try:
                ret = self.callback(payload)
                if ret is False:
                    await self.client.disconnect()
            except Exception as e:
                print("[receiver] erro no callback:", e)

        print("📡 Receiver iniciado. Aguardando mensagens...")
        await self.client.run_until_disconnected()

    def start(self):
        import asyncio
        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            print("\n🚪 Receiver encerrado.")
