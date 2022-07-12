from asyncio import sleep

from kantex.html import *
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types.messages_and_media.message import Message

from bots import MODULES, app

MODULES.update(
    {
        "id": {
            "info": "To get all of the IDs present in a message.",
            "usage": "/id [optional: reply]",
        },
    },
)


@app.command("id", pm_only=False)
async def getid(c: Client, m: Message):
    if len(m.command) >= 2:
        k = m.text.split(None, 1)[1]
        try:
            username = int(k)
            name = 1
        except ValueError:
            username = str(k)
            name = 0
        try:
            if m.entities:
                for u in m.entities:
                    if str(u.type) == enums.MessageEntityType.MENTION:
                        offset = int(u.offset)
                        lenn = int(int(u.length) + offset)
                        userr = m.text[offset:lenn]
                    elif str(u.type) == enums.MessageEntityType.TEXT_MENTION:
                        userr = int(u.user.id)
                    else:
                        userr = username
            else:
                userr = k
            u = await c.get_chat(userr)
        except FloodWait as s:
            await sleep(s.value)
            u = await c.get_chat(userr)
        except RPCError as e:
            await m.reply_text(f"Error: {e}")
            return
        if name:
            use = Code(
                u.first_name or u.title
                if isinstance(u.first_name or u.title, str)
                else str(k),
            )
        else:
            use = username if isinstance(username, str) else str(k)
        te = f"""
{Bold(f"{use}'s ID:")} {Code(u.id)}
{Bold("Chat ID:")} {Code(m.chat.id)}"""
        await m.reply_text(te)
        return
    if m.chat.username:
        text_ping = f'{Link(Bold("Chat ID:"), f"https://t.me/{m.chat.username}")} {Code(m.chat.id)}\n'
    else:
        text_ping = f"{Bold('Chat ID: ')} {Code(m.chat.id)}\n"
    if m.link:
        text_ping += f'{Link(Bold("Message ID:"), m.link)} {Code(m.id)}\n'
    else:
        text_ping += f"{Bold('Message ID:')} {Code(m.id)}\n"
    if m.from_user:
        text_ping += f'{Bold(Link("Your ID:", f"tg://user?id={m.from_user.id}"))} {Code(m.from_user.id)}\n'
    elif m.sender_chat:
        if (
            m.forward_from_chat
            and m.sender_chat.type == enums.ChatType.CHANNEL
        ):
            text_ping += f"{Bold('Your ID:')} {Code(777000)}\n"
            text_ping += (
                f"{Bold('Your Channel ID:')} {Code(m.sender_chat.id)}\n"
            )
        elif (
            m.sender_chat.id == m.chat.id
            and m.sender_chat.type == enums.ChatType.SUPERGROUP
        ):
            text_ping += f"{Bold('Your ID:')} {Code(1087968824)}\n"
        elif (
            m.sender_chat.id != m.chat.id
            and m.sender_chat.type == enums.ChatType.CHANNEL
        ):
            text_ping += f"{Bold('Your ID:')} {Code(136817688)}\n"
            text_ping += (
                f"{Bold('Your Channel ID:')} {Code(m.sender_chat.id)}\n"
            )
    if reply := m.reply_to_message:
        if reply.link:
            text_ping += f'{Link(Bold("Replied Message ID:"), reply.link)} {Code(reply.id)}\n'
        else:
            text_ping += f"{Bold('Replied Message ID:')} {Code(reply.id)}\n"
        if reply.forward_from_chat:
            text_ping += f"{Bold('Forwarded channel ID:')} {Code(reply.forward_from_chat.id)}\n"
        if reply.from_user:
            if reply.from_user.username:
                text_ping += f'{Link(Bold("Replied User ID:"), f"https://t.me/{reply.from_user.username}")} {Code(reply.from_user.id)}\n'
            else:
                text_ping += f'{Bold(Link("Replied User ID:", f"tg://user?id={reply.from_user.id}"))} {Code(reply.from_user.id)}\n'
        elif reply.sender_chat:
            if (
                reply.forward_from_chat
                and reply.sender_chat.type == enums.ChatType.CHANNEL
            ):
                text_ping += f"{Bold('Replied User ID:')} {Code(777000)}\n"
                text_ping += f"{Bold('Replied Channel ID:')} {Code(reply.sender_chat.id)}\n"
            elif (
                reply.sender_chat.id == reply.chat.id
                and reply.sender_chat.type == enums.ChatType.SUPERGROUP
            ):
                text_ping += f"{Bold('Replied User ID:')} {Code(1087968824)}\n"
            elif (
                reply.sender_chat.id != reply.chat.id
                and reply.sender_chat.type == enums.ChatType.CHANNEL
            ):
                text_ping += f"{Bold('Replied User ID:')} {Code(136817688)}\n"
                text_ping += f"{Bold('Replied Channel ID:')} {Code(reply.sender_chat.id)}\n"
        if reply.forward_from:
            if reply.forward_from.username:
                text_ping += f'{Link(Bold("Forwarded User ID:"), f"https://t.me/{reply.forward_from.username}")} {Code(reply.forward_from.id)}\n'
            else:
                text_ping += f'{Link(Bold("Forwarded User ID: "), f"tg://user?id={reply.forward_from.id})")} {Code(reply.forward_from.id)}\n'
        if reply.sticker:
            text_ping += (
                f"{Bold('Sticker ID:')} {Code(reply.sticker.file_id)}\n"
            )
        if reply.animation:
            text_ping += f"{Bold('GIF ID:')} {Code(reply.animation.file_id)}\n"
    await m.reply_text(str(text_ping), disable_web_page_preview=True)
