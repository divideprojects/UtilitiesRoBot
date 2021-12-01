from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bots import JoinChannel, JoinCheck, SupportGroup


def joinCheck():
    def wrapper(func):
        async def decorator(c, m):
            if not JoinCheck:
                return await func(c, m)
            if m.sender_chat:
                return
            try:
                get = await c.get_chat_member(JoinChannel, m.from_user.id)
            except UserNotParticipant:
                return await m.reply_text(
                    f"You need to Join {JoinChannel} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{JoinChannel.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            if get.status in ("restricted", "kicked"):
                return await m.reply_text(
                    f"You were banned from using me. If you think this is a mistake then report this at {SupportGroup}",
                )
            if not get.status in ("creator", "administrator", "member"):
                return await m.reply_text(
                    f"You need to Join {JoinChannel} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{JoinChannel.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            return await func(c, m)

        return decorator

    return wrapper
