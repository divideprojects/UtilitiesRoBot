from bots import JoinChannel, JoinCheck, SupportGroup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join():
    def wrapper(func):
        async def decorator(client, message):
            if not JoinCheck:
                return await func(client, message)
            if message.sender_chat:
                return
            get = await client.get_chat_member(JoinChannel, message.from_user.id)
            if get.status in ("restricted", "kicked"):
                return await message.reply_text(f"You were banned from using me. If you think this is a mistake then report this at {SupportGroup}")
            if not get.status in ("creator", "administrator", "member"):
                return await message.reply_text(f"You need to Join {JoinChannel} to use me.", reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("Join Channel", url=f"https://t.me/{JoinChannel.replace('@', '')}")]))
            await func(client, message)
        return decorator
    return wrapper
