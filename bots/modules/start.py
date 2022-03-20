from time import time

from kantex.html import Section, Bold
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from bots import app
from bots.vars import Vars


@app.command("start", pm_only=True)
async def start(_, m: Message):
    return await m.reply_text(
        f"""
Hi there, I am a Utilities Bot by {Vars.JOIN_CHANNEL}
For my commands type /help

Channel: {Vars.JOIN_CHANNEL}
Support: {Vars.SUPPORT_GROUP}
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel",
                        url=f"https://telegram.me/{Vars.JOIN_CHANNEL.replace('@', '')}",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url=f"https://telegram.me/{Vars.SUPPORT_GROUP.replace('@', '')}",
                    ),
                ],
            ],
        ),
    )


@app.command("help", pm_only=True)
async def help_msg(_, m: Message):
    return await m.reply_text(
        str(
            Section(
                "Available Commands",
                "/bin {bin} - To check a Bin is Valid or not.",
                "/genInfo {gender} - To generate a fake user Details.",
                "/proxy - To get some available Proxies.",
                "/paste - To paste file/replied message contents to a pastebin.",
                "/session - To generate Pyrogram/Telethon String Session.",
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
                        url=f"https://telegram.me/{Vars.JOIN_CHANNEL.replace('@', '')}",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url=f"https://telegram.me/{Vars.SUPPORT_GROUP.replace('@', '')}",
                    ),
                ],
            ],
        ),
    )


@app.command("ping", pm_only=False)
async def ping(_, m: Message):
    start = time()
    replymsg = await m.reply_text("Pinging ...", quote=True)
    delta_ping = time() - start
    return await replymsg.edit_text(str(Bold(f"Pong!") + "\n{delta_ping * 1000: .3f} ms"))
