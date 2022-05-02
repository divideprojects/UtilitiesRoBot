from time import time

from kantex.html import Bold
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from bots import MODULES, app
from bots.vars import Vars

MODULES.update(
    {
        "start": {
            "info": "To start the bot.",
            "usage": "/start",
        },
        "help": {
            "info": "To list the available commands.",
            "usage": "/help",
        },
    },
)


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
    msg = str(Bold("Available Commands"))
    for i in list(MODULES.keys()):
        msg += f"\n    {MODULES.get(i).get('usage')}- {MODULES.get(i).get('info')}"

    return await m.reply_text(
        str(msg),
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
