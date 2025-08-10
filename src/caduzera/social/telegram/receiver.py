from telethon import TelegramClient, events
from typing import Iterable, Optional

def _normalize_allowed(allowed: Optional[Iterable[str|int]]) -> Optional[set]:
    if not allowed: return None
    s = set()
    for x in allowed:
        if x is None: continue
        try:
            s.add(int(x))
        except (ValueError, TypeError):
            u = str(x)
            if not u.startswith("@"): u = "@" + u
            s.add(u)
    return s

def attach_group_receiver(
    client: TelegramClient,
    on_message,                         # Callable[[dict], None|bool]
    allowed_chats: Optional[Iterable[str|int]] = None
):
    """Registra handler para grupos/canais onde SUA CONTA participa."""
    allowed = _normalize_allowed(allowed_chats)

    @client.on(events.NewMessage)
    async def _handler(event: events.NewMessage.Event):
        chat = await event.get_chat()
        is_group_like = getattr(chat, "title", None) or getattr(chat, "megagroup", False) or getattr(chat, "broadcast", False)
        if not is_group_like:
            return

        chat_id = event.chat_id
        username = getattr(chat, "username", None)
        if allowed:
            ok = (chat_id in allowed) or (username and ("@" + username) in allowed)
            if not ok:
                return

        sender = await event.get_sender()
        payload = {
            "chat_id": chat_id,
            "chat_title": getattr(chat, "title", None),
            "sender_id": getattr(sender, "id", None),
            "sender_username": getattr(sender, "username", None),
            "text": event.raw_text or "",
            "date": event.date,
            "message_id": event.id,
        }
        cont = on_message(payload)
        if cont is False:
            await client.disconnect()
