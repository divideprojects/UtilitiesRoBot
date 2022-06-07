# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2022 Divide Projects <https://github.com/DivideProjects>

# This file is part of Utilities Robot.

# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Utilities Robot.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bots.vars import Vars


def joinCheck(**args):
    def wrapper(func):
        async def decorator(c, m: Message):
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
