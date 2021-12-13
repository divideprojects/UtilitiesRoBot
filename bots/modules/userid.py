from asyncio import sleep
from html import escape

from pyrogram.errors import FloodWait, RPCError
from pyrogram.types.messages_and_media.message import Message

from bots import app


@app.command("id", pm_only=False)
async def getid(c: app, m: Message):
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
                    offset = int(u["offset"])
                    lenn = int(int(u["length"]) + offset)
                if str(u["type"]) == "mention":
                    userr = m.text[offset:lenn]
                elif str(u["type"]) == "text_mention":
                    userr = int(u.user.id)
                else:
                    userr = k
            else:
                userr = username
            u = await c.get_chat(userr)
        except FloodWait as s:
            await sleep(s.x)
            u = await c.get_chat(userr)
        except RPCError as e:
            await m.reply_text(f"Error: {e}")
            return
        if name:
            use = escape(
                u.first_name or u.title
                if isinstance(u.first_name or u.title, str)
                else str(k)
            )
        else:
            use = escape(username if isinstance(username, str) else str(k))
        te = f"<b>{use}'s ID:</b> <code>{u.id}</code>\n<b>Chat ID:</b> <code>{m.chat.id}</code>"
        await m.reply_text(te, parse_mode="html")
        return
    if m.chat.username:
        text_ping = f'<a href="https://t.me/{m.chat.username}"><b>Chat ID:</b></a> <code>{m.chat.id}</code>\n'
    else:
        text_ping = f"<b>Chat ID:</b> <code>{m.chat.id}</code>\n"
    if m.link:
        text_ping += (
            f'<a href="{m.link}"><b>Message ID:</b></a> <code>{m.message_id}</code>\n'
        )
    else:
        text_ping += f"<b>Message ID:</b> <code>{m.message_id}</code>\n"
    if m.from_user:
        text_ping += f'<b><a href="tg://user?id={m.from_user.id}">Your ID:</a></b> <code>{m.from_user.id}</code>\n'
    elif m.sender_chat:
        if m.forward_from_chat and m.sender_chat.type == "channel":
            text_ping += "<b>Your ID:</b> <code>777000</code>\n"
            text_ping += f"<b>Your Channel ID:</b> <code>{m.sender_chat.id}</code>\n"
        elif m.sender_chat.id == m.chat.id and m.sender_chat.type == "supergroup":
            text_ping += "<b>Your ID:</b> <code>1087968824</code>\n"
        elif m.sender_chat.id != m.chat.id and m.sender_chat.type == "channel":
            text_ping += "<b>Your ID:</b> <code>136817688</code>\n"
            text_ping += f"<b>Your Channel ID:</b> <code>{m.sender_chat.id}</code>\n"
    reply = m.reply_to_message
    if reply:
        if reply.link:
            text_ping += f'<a href="{reply.link}"><b>Replied Message ID:</b></a> <code>{reply.message_id}</code>\n'
        else:
            text_ping += f"<b>Replied Message ID:</b> <code>{reply.message_id}</code>\n"
        if reply.forward_from_chat:
            text_ping += f"<b>Forwarded channel ID:</b> <code>{reply.forward_from_chat.id}</code>\n"
        if reply.from_user:
            if reply.from_user.username:
                text_ping += f'<a href="https://t.me/{reply.from_user.username}"><b>Replied User ID:</b></a> <code>{reply.from_user.id}</code>\n'
            else:
                text_ping += f'<b><a href="tg://user?id={reply.from_user.id}">Replied User ID:</a></b> <code>{reply.from_user.id}</code>\n'
        elif reply.sender_chat:
            if reply.forward_from_chat and reply.sender_chat.type == "channel":
                text_ping += "<b>Replied User ID:</b> <code>777000</code>\n"
                text_ping += (
                    f"<b>Replied Channel ID:</b> <code>{reply.sender_chat.id}</code>\n"
                )
            elif (
                reply.sender_chat.id == reply.chat.id
                and reply.sender_chat.type == "supergroup"
            ):
                text_ping += "<b>Replied User ID:</b> <code>1087968824</code>\n"
            elif (
                reply.sender_chat.id != reply.chat.id
                and reply.sender_chat.type == "channel"
            ):
                text_ping += "<b>Replied User ID:</b> <code>136817688</code>\n"
                text_ping += (
                    f"<b>Replied Channel ID:</b> <code>{reply.sender_chat.id}</code>\n"
                )
        if reply.forward_from:
            if reply.forward_from.username:
                text_ping += f'<a href="https://t.me/{reply.forward_from.username}"><b>Forwarded User ID:</b></a> <code>{reply.forward_from.id}</code>\n'
            else:
                text_ping += f'<b><a href="tg://user?id={reply.forward_from.id}">Forwarded User ID:</a></b> <code>{reply.forward_from.id}</code>\n'
        if reply.sticker:
            text_ping += f"<b>Sticker ID:</b> <code>{reply.sticker.file_id}</code>\n"
        if reply.animation:
            text_ping += f"<b>GIF ID:</b> <code>{reply.animation.file_id}</code>\n"
    await m.reply_text(text_ping, disable_web_page_preview=True, parse_mode="html")
    return
