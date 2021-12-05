#
# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2021 Divide Projects <https://github.com/DivideProjects>
#
# This file is part of Utilities Robot.
#
# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.#
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
            if get.status not in ("creator", "administrator", "member"):
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
