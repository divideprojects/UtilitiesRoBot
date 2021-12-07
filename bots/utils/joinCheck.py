from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bots.vars import Vars


def joinCheck():
    def wrapper(func):
        async def decorator(c, m):
            if not Vars.JOIN_CHECK:
                return await func(c, m)
            if m.sender_chat:
                return
            try:
                get = await c.get_chat_member(Vars.JOIN_CHANNEL, m.from_user.id)
            except UserNotParticipant:
                return await m.reply_text(
                    f"You need to Join {Vars.JOIN_CHANNEL} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{Vars.JOIN_CHANNEL.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            if get.status in ("restricted", "kicked"):
                return await m.reply_text(
                    f"You were banned from using me. If you think this is a mistake then report this at {Vars.SUPPORT_GROUP}",
                )
            if get.status not in ("creator", "administrator", "member"):
                return await m.reply_text(
                    f"You need to Join {Vars.JOIN_CHANNEL} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{Vars.JOIN_CHANNEL.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            return await func(c, m)

        return decorator

    return wrapper
