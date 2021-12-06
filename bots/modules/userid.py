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
from asyncio import sleep

from pyrogram.errors import FloodWait, RPCError
from pyrogram.types.messages_and_media.message import Message

from bots import app


@app.command("id", pm_only=False)
async def getid(c: app, message: Message):
    if len(message.command) >= 2:
        k = message.text.split(None, 1)[1]
        try:
            username = int(k)
            name = 1
        except ValueError:
            username = k
            name = 0
        try:
            if message.entities:
                for u in message.entities:
                    offset = int(u["offset"])
                    lenn = int(int(u["length"]) + offset)
                if str(u["type"]) == "mention":
                    userr = message.text[offset:lenn]
                elif str(u["type"]) == "text_mention":
                    userr = int(u.user.id)
                else:
                    userr = message.text.split(None, 1)[1]
            u = await c.get_chat(userr)
        except FloodWait as s:
            await sleep(s.x)
            u = await c.get_chat(userr)
        except RPCError as e:
            await message.reply_text(f"Error: {e}")
            return
        if name:
            use = u.first_name
        else:
            use = username
        text = f"<b>{use}'s ID:</b> <code>{u.id}</code>\n<b>Chat ID:</b> <code>{message.chat.id}</code>"
        await message.reply_text(text, parse_mode="html")
        return
    if message.chat.username:
        text_ping = f'<a href="https://t.me/{message.chat.username}"><b>Chat ID:</b></a> <code>{message.chat.id}</code>\n'
    else:
        text_ping = f"<b>Chat ID:</b> <code>{message.chat.id}</code>\n"
    if message.link:
        text_ping += f'<a href="{message.link}"><b>Message ID:</b></a> <code>{message.message_id}</code>\n'
    else:
        text_ping += f"<b>Message ID:</b> <code>{message.message_id}</code>\n"
    if message.from_user:
        text_ping += f'<b><a href="tg://user?id={message.from_user.id}">Your ID:</a></b> <code>{message.from_user.id}</code>\n'
    elif message.sender_chat:
        text_ping += '<b><a href="tg://user?id=1087968824">Your ID:</a></b> <code>1087968824</code>\n'
    reply = message.reply_to_message
    if not getattr(reply, "empty", True):
        if reply.link:
            text_ping += f'\n<a href="{reply.link}"><b>Replied Message ID:</b></a> <code>{reply.message_id}</code>\n'
        else:
            text_ping += (
                f"\n<b>Replied Message ID:</b> <code>{reply.message_id}</code>\n"
            )
        if message.reply_to_message and message.reply_to_message.forward_from_chat:
            text_ping += f"\n<b>Forwarded channel ID:</b> <code>{message.reply_to_message.forward_from_chat.id}</code>\n"
        if reply.from_user:
            if reply.from_user.username:
                text_ping += f'<a href="https://t.me/{reply.from_user.username}"><b>Replied User ID:</b></a> <code>{reply.from_user.id}</code>\n'
            else:
                text_ping += f'<b><a href="tg://user?id={reply.from_user.id}">Replied User ID:</a></b> <code>{reply.from_user.id}</code>\n'
        elif reply.sender_chat:
            text_ping += '<a href="https://t.me/GroupAnonymousBot"><b>Replied User ID:</b></a> <code>1087968824</code>\n'
        if reply.forward_from:
            if reply.forward_from.username:
                text_ping += f'\n<a href="https://t.me/{reply.forward_from.username}"><b>Forwarded User ID:</b></a> <code>{reply.forward_from.id}</code>\n'
            else:
                text_ping += f'\n<b><a href="tg://user?id={reply.forward_from.id}">Forwarded User ID:</a></b> <code>{reply.forward_from.id}</code>\n'
        if message.reply_to_message and message.reply_to_message.sticker:
            text_ping += f"\n<b>Sticker ID:</b> <code>{message.reply_to_message.sticker.file_id}</code>\n\n"
        if message.reply_to_message and message.reply_to_message.animation:
            text_ping += f"\n<b>GIF ID:</b> <code>{message.reply_to_message.animation.file_id}</code>\n"
    await message.reply_text(
        text_ping,
        disable_web_page_preview=True,
        parse_mode="html",
    )
    return
