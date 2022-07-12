from gc import collect

from pyrogram import enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bots.vars import Vars


def joinCheck(**args):
    def wrapper(func):
        async def decorator(c, m: Message):
            collect()
            if not Vars.JOIN_CHECK:
                return await func(c, m)
            if m.sender_chat:
                return 0
            try:
                get = await c.get_chat_member(
                    Vars.JOIN_CHANNEL, m.from_user.id
                )
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
            if get.status in (
                enums.ChatMemberStatus.BANNED,
                enums.ChatMemberStatus.RESTRICTED,
            ):
                return await m.reply_text(
                    f"You were banned from using me. If you think this is a mistake then report this at {Vars.SUPPORT_GROUP}",
                )
            if get.status not in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.MEMBER,
            ):
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
