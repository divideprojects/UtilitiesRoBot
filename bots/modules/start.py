from kantex.html import Section
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.messages_and_media.message import Message

from .. import SupportGroup, app


@app.command("start", pm_only=True)
async def start(_, m: Message):
    await m.reply_text(
        f"""
Hi there, I am a Utilities Bot by @DivideProjects
For my commands type /help

Channel: @DivideProjects
Support: {SupportGroup}
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel",
                        url="https://telegram.me/DivideProjects",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url="https://telegram.me/DivideProjectsDiscussion",
                    ),
                ],
            ],
        ),
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
            ),
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel",
                        url="https://telegram.me/DivideProjects",
                    ),
                    InlineKeyboardButton(
                        "Group",
                        url="https://telegram.me/DivideProjectsDiscussion",
                    ),
                ],
            ],
        ),
    )
