from operator import ge
from select import kevent
from sys import modules
from time import time
from webbrowser import get

from kantex.html import Bold, Section
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from bots import app, MODULES
from bots.vars import Vars

MODULES.update({
    "start": {
        "command": "start",
        "info": "To start the bot.",
        "usage": "/start",
    },
    "help": {
        "command": "help",
        "info": "To list the available commands.",
        "usage": "/help",
    }
})


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
                str(
                    f"/{MODULES.get(i)['usage']} - {MODULES.get(i)['info']}" for i in list(MODULES.keys())
                )
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
    return await replymsg.edit_text(
        Bold(f"Pong!\n{delta_ping * 1000: .3f} ms"),
    )
