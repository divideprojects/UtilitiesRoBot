from .. import app, SupportGroup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from kantex.html import *


@app.command("start", pm_only=True)
async def start(client, message):
    await message.reply_text(
        f"""
Hi there, I am a Utilities Bot by @DivideProjects
For my commands type /help

Channel: @DivideProjects
Support: {SupportGroup}
        """,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Channel",
                    url="https://telegram.me/DivideProjects"
                ),
                InlineKeyboardButton(
                    "Group",
                    url="https://telegram.me/DivideProjectsDiscussion"
                )
            ]
        ])
    )


@app.command("help", pm_only=True)
async def _help(client, message):
    await message.reply_text(str(
        Section(
            "Available Commands",
            "/bin {bin} - To check a Bin is Valid or not.",
            "/genInfo {gender} - To generate a fake user Details.",
            "/proxy - To get some available Proxies.",
            "/pyrogram - To generate Pyrogram String Session.",
            "/telethon - To generate Telethon String Session."
        )
    ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Channel",
                    url="https://telegram.me/DivideProjects"
                ),
                InlineKeyboardButton(
                    "Group",
                    url="https://telegram.me/DivideProjectsDiscussion"
                )
            ]
        ])
    )
