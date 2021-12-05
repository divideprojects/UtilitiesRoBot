from kantex.html import Section
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from bots import SupportGroup, JoinChannel app


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
                "/tts - Convert replied text to audio",
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
