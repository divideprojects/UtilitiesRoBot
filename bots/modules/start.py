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
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.
#
from time import time

from kantex.html import Section
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from bots import SupportGroup, JoinChannel, app


@app.command("start", pm_only=True)
async def start(_, m: Message):
    await m.reply_text(
        f"""
Hi there, I am a Utilities Bot by {JoinChannel}
For my commands type /help

Channel: {JoinChannel}
Support: {SupportGroup}
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel",
                        url=f"https://telegram.me/{JoinChannel.replace('@', '')}",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url=f"https://telegram.me/{SupportGroup.replace('@', '')}",
                    )
                ]
            ]
        )
    )


@app.command("help", pm_only=True)
async def help_msg(_, m: Message):
    await m.reply_text(
        str(
            Section(
                "Available Commands",
                "/bin {bin} - To check a Bin is Valid or not.",
                "/genInfo {gender} - To generate a fake user Details.",
                "/proxy - To get some available Proxies.",
                "/paste - To paste file/replied message contents to a pastebin.",
                "/pyrogram - To generate Pyrogram String Session.",
                "/telethon - To generate Telethon String Session.",
                "/tinify - Compress a replied image.",
                "/json - Get json data of replied message.",
                "/github {username} - Get information about github user.",
                "/pdf2img - Convert replied pdf to images.",
                "/tts - Convert replied text to audio.",
                "/ping - Pings me up.",
                "/id - Gets every ids present in the message.",
            ),
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel",
                        url=f"https://telegram.me/{JoinChannel.replace('@', '')}",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url=f"https://telegram.me/{SupportGroup.replace('@', '')}",
                    )
                ]
            ],
        ),
    )


@app.command("ping", pm_only=False)
async def ping(_, m: Message):
    start = time()
    replymsg = await m.reply_text("Pinging ...", quote=True)
    delta_ping = time() - start
    await replymsg.edit_text(f"<b>Pong!</b>\n{delta_ping * 1000:.3f} ms")
    return
