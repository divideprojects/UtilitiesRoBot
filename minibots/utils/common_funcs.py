from time import time

from pyrogram import Client
from pyrogram.types import Message

from minibots.utils.common_text import Constants
from minibots.vars import Vars


class funcs:
    """common functions to be executed on all bots."""

    @staticmethod
    async def common_donate(m: Message):
        if m.chat.type == "private":
            await m.reply_text(
                Constants.DONATE_TEXT,
                disable_web_page_preview=True,
                parse_mode="markdown",
                quote=True,
            )
        else:
            await m.reply_text(
                "To get information regarding donating to my owner, PM me and send /donate command",
                quote=True,
            )
        return

    @staticmethod
    async def common_ping(m: Message, LOGGER):
        start = time()
        reply = await m.reply_text("Pinging...", quote=True)
        delta_ping = time() - start
        await reply.edit_text(
            f"**Pong!**\n`{delta_ping * 1000:.3f} ms`",
            parse_mode="markdown",
        )
        ping_executor = "Owner" if m.from_user.id == int(Vars.OWNER_ID) else "Dev"
        LOGGER.info(f"Ping Executed by {ping_executor}")
        return

    @staticmethod
    async def common_about(c: Client, m: Message, bt_u: str):
        if m.chat.type == "private":
            owner = await c.get_users(Vars.OWNER_ID)
            await m.reply_text(
                Constants.about_me_text.format(
                    owner.first_name,
                    bt_u,
                ),
                disable_web_page_preview=True,
                quote=True,
                parse_mode="html",
            )
        else:
            await m.reply_text(
                "To get information regarding me, PM me and send /about command",
                quote=True,
            )
        return
