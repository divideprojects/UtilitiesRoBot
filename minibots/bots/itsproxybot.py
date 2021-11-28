from io import BytesIO

from proxygrab import get_proxy
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers.helpers import array_chunk

from minibots.logger import LOGGER
from minibots.utils.common_funcs import funcs
from minibots.utils.common_text import Constants
from minibots.utils.custom_filters import command, user_check
from minibots.utils.ikb import ikb
from minibots.vars import Vars

# App for the bot
itsproxybot_app = Client(
    "ItsProxyBot",
    api_id=Vars.API_ID,
    api_hash=Vars.API_HASH,
    bot_token=Vars.BOT_TOKEN_PROXYBOT,
    workers=Vars.WORKERS,
)

with itsproxybot_app as app:
    BOT_USERNAME = app.get_me().username

# Types of proxies available in bot
proxytypes = {"HTTP", "HTTPS", "Socks4", "Socks5"}


class Pvt:
    START_TEXT = f"""
I'm @{BOT_USERNAME}, to provide you with proxies!
I'll fetch proxies from different sites \
and give you here as a file.

All the proxies are new and fast!
"""
    HELP_TEXT = f"""
__**Commands:**__
{Vars.PRIMARY_HANDLER}start - Show Start message.
{Vars.PRIMARY_HANDLER}help - Check this help message.
{Vars.PRIMARY_HANDLER}proxies - Show a inline keyboard menu to choose which proxies you want.
{Vars.PRIMARY_HANDLER}about - Get some info about me.
{Vars.PRIMARY_HANDLER}donate - Get info about donating my owner.

**Available Proxies:**
{', '.join(['`'+i+'`' for i in proxytypes])}

Proxies scrapped using [ProxyGrab](https://pypi.org/project/proxygrab) module!
"""


# -- Constants End -- #


# -- Bot Function starts -- #
@itsproxybot_app.on_message(command("start", BOT_USERNAME=BOT_USERNAME))
async def start_bot(_, m: Message):
    await m.reply_text(
        Pvt.START_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        parse_mode="html",
        reply_markup=Constants.start_kb,
        quote=True,
    )
    return


@itsproxybot_app.on_message(command("help", BOT_USERNAME=BOT_USERNAME))
async def help_bot(_, m: Message):
    await m.reply_text(
        Pvt.HELP_TEXT,
        disable_web_page_preview=True,
        parse_mode="markdown",
        reply_markup=ikb([[(">>>", "help.callback.start")]]),
        quote=True,
    )
    return


@itsproxybot_app.on_callback_query(filters.regex("^help.callback."))
async def help_bot_callback(_, q: CallbackQuery):
    qdata = q.data.split(".", 2)[2]
    if qdata == "help":
        qhelp = Pvt.HELP_TEXT
        qkb = ikb([Constants.back_help_start])
    elif qdata == "start":
        qhelp = Pvt.START_TEXT.format(q.message.from_user.mention)
        qkb = Constants.start_kb
    await q.message.edit_text(qhelp, reply_markup=qkb, disable_web_page_preview=True)
    await q.answer()
    return


# Common funcs
@itsproxybot_app.on_message(command("donate", BOT_USERNAME=BOT_USERNAME))
async def donate_owner(_, m: Message):
    await funcs.common_donate(m)
    return


@itsproxybot_app.on_message(command("ping", BOT_USERNAME=BOT_USERNAME))
async def ping(_, m: Message):
    await funcs.common_ping(m, LOGGER)
    return


@itsproxybot_app.on_message(command("about", BOT_USERNAME=BOT_USERNAME))
async def about_owner(c: Client, m: Message):
    await funcs.common_about(c, m, BOT_USERNAME)
    return


# Bot specific funcs
@itsproxybot_app.on_callback_query(filters.regex("^getProxy."))
async def get_proxytype_callabcak(_, q: CallbackQuery):
    ptype = q.data.split(".")[1].lower()

    await q.message.edit_text(f"Fetching {ptype} Proxies...")
    LOGGER.info(f"UserID {q.message.from_user.id} scrapping {ptype} proxies...")

    proxies_source = await get_proxy(ptype)  # Get proxies as list!
    proxies_fetched = "\n".join(proxies_source)
    caption = f"<b><i>Proxies scrapped by:</i></b> @{BOT_USERNAME}\n\nIf you'd like to keep this service alive 😊, please /donate"
    with BytesIO(str.encode(proxies_fetched)) as output:
        output.name = f"{ptype}_{BOT_USERNAME}.txt"
        await q.message.reply_document(document=output, caption=caption)

    await q.message.delete()
    await q.answer("Done ✅", show_alert=True)
    return


@itsproxybot_app.on_message(
    command("proxies", BOT_USERNAME=BOT_USERNAME) & user_check,
)
async def get_proxies(_, m: Message):
    kb = await gen_proxy_kb()
    kb.append(Constants.back_help_start)
    await m.reply_text(
        "<b><i>Which type of proxylist do you want?</i></b>",
        reply_to_message_id=m.message_id,
        reply_markup=ikb(kb),
    )

    return


async def gen_proxy_kb():
    # Copy, so that main list is not removed!
    cmds = [i for i in proxytypes]
    kb = [(cmd, f"getProxy.{cmd}") for cmd in cmds]
    return array_chunk(kb, 2)
