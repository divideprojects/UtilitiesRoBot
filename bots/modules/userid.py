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
    text_unping = "<b>Chat ID:</b>"
    if message.chat.username:
        text_unping = (
            f'<a href="https://t.me/{message.chat.username}">{text_unping}</a>'
        )
    text_unping += f" <code>{message.chat.id}</code>\n"
    text = "<b>Message ID:</b>"
    if message.link:
        text = f'<a href="{message.link}">{text}</a>'
    text += f" <code>{message.message_id}</code>\n"
    text_unping += text
    if message.from_user:
        text_unping += f'<b><a href="tg://user?id={message.from_user.id}">Your ID:</a></b> <code>{message.from_user.id}</code>\n'
    if message.sender_chat:
        text_unping += '<b><a href="tg://user?id=1087968824">Your ID:</a></b> <code>1087968824</code>\n'
    text_ping = text_unping
    reply = message.reply_to_message
    if not getattr(reply, "empty", True):
        text_unping += "\n"
        text = "<b>Replied Message ID:</b>"
        if reply.link:
            text = f'<a href="{reply.link}">{text}</a>'
        text += f" <code>{reply.message_id}</code>\n"
        text_unping += text
        text_ping = text_unping
        if message.reply_to_message and message.reply_to_message.forward_from_chat:
            text_unping += f"\n<b>Forwarded channel ID:</b> <code>{message.reply_to_message.forward_from_chat.id}</code>\n"
            text_ping = text_unping
        if reply.from_user:
            tex = "<b>Replied User ID:</b>"
            if reply.from_user.username:
                text = f'<a href="https://t.me/{reply.from_user.username}">{text}</a>'
            text += f" <code>{reply.from_user.id}</code>\n"
            text_unping += text
            text_ping += f'<b><a href="tg://user?id={reply.from_user.id}">Replied User ID:</a></b> <code>{reply.from_user.id}</code>\n'
        if message.sender_chat:
            tex = "<b>Replied User ID:</b>"
            text = f'<a href="https://t.me/GroupAnonymousBot">{tex}</a>'
            text += f" <code>1087968824</code>\n"
            text_unping += text
            text_ping += '<b><a href="tg://user?id=1087968824">Replied User ID:</a></b> <code>1087968824</code>\n'
        if reply.forward_from:
            text_unping += "\n"
            text = "<b>Forwarded User ID:</b>"
            if reply.forward_from.username:
                text = (
                    f'<a href="https://t.me/{reply.forward_from.username}">{text}</a>'
                )
            text += f" <code>{reply.forward_from.id}</code>\n"
            text_unping += text
            text_ping += f'\n<b><a href="tg://user?id={reply.forward_from.id}">Forwarded User ID:</a></b> <code>{reply.forward_from.id}</code>\n'
        if message.reply_to_message and message.reply_to_message.sticker:
            text_unping += f"\n<b>Sticker ID:</b> <code>{message.reply_to_message.sticker.file_id}</code>\n\n"
            text_ping = text_unping
        if message.reply_to_message and message.reply_to_message.animation:
                text_unping += f"\n<b>GIF ID:</b> <code>{message.reply_to_message.animation.file_id}</code>\n"
                text_ping = text_unping
    reply = await message.reply_text(
        text_unping, disable_web_page_preview=True, parse_mode="html"
    )
    if text_unping != text_ping:
        await reply.edit_text(
            text_ping, disable_web_page_preview=True, parse_mode="html"
        )
        return
    return
