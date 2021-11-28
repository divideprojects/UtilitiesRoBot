from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from minibots.logger import LOGGER
from minibots.utils.aiohttp_helper import AioHttp
from minibots.utils.common_funcs import funcs
from minibots.utils.common_text import Constants
from minibots.utils.custom_filters import command
from minibots.utils.ikb import ikb
from minibots.vars import Vars

# App for the bot
bincheckerbot_app = Client(
    "BinCheckerBot",
    api_id=Vars.API_ID,
    api_hash=Vars.API_HASH,
    bot_token=Vars.BOT_TOKEN_BINCHECKER,
    workers=Vars.WORKERS,
)
# Get username from bot itself
with bincheckerbot_app as app:
    BOT_USERNAME = app.get_me().username

# -- Constants -- #
class Pvt:
    START_TEXT = f"""
Hey {{}}!
I'm @{BOT_USERNAME}, a bot used to check \
information about bins!
"""
    HELP_TEXT = f"""
__**Commands:**__
{Vars.PRIMARY_HANDLER}start - Show Start message.
{Vars.PRIMARY_HANDLER}help - Check this help message.
{Vars.PRIMARY_HANDLER}bin `<bin>` - Check information about bin.
{Vars.PRIMARY_HANDLER}about - Get some info about me.
{Vars.PRIMARY_HANDLER}donate - Get info about donating my owner.

__**Example:**__
`{Vars.PRIMARY_HANDLER}bin 45717360`
Get information about bin `45717360`
"""


class Grp:
    START_TEXT = f"""
I'm Alive, start using me inline!
"""
    HELP_TEXT = f"""
`{Vars.PRIMARY_HANDLER}bin <bin>`: Check the bin using Command
`@{BOT_USERNAME} <bin>`: Check thebin in inline mode.
"""


# -- Constants End -- #

# -- Bot Function starts -- #
@bincheckerbot_app.on_message(command("start", BOT_USERNAME=BOT_USERNAME))
async def start_bot(_, m: Message):
    if m.chat.type == "private":
        await m.reply_text(
            Pvt.START_TEXT.format(m.from_user.mention),
            disable_web_page_preview=True,
            parse_mode="html",
            reply_markup=Constants.start_kb,
            quote=True,
        )
    else:
        await m.reply_text(Grp.START_TEXT, quote=True)
    return


@bincheckerbot_app.on_message(command("help", BOT_USERNAME=BOT_USERNAME))
async def help_bot(_, m: Message):
    if m.chat.type == "private":
        await m.reply_text(
            Pvt.HELP_TEXT,
            disable_web_page_preview=True,
            parse_mode="markdown",
            reply_markup=ikb([[(">>>", "help.callback.start")]]),
            quote=True,
        )
    else:
        await m.reply_text(Grp.HELP_TEXT, quote=True)
    return


@bincheckerbot_app.on_callback_query(filters.regex("^help.callback."))
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


# Common Functions
@bincheckerbot_app.on_message(command("donate", BOT_USERNAME=BOT_USERNAME))
async def donate_owner(_, m: Message):
    await funcs.common_donate(m)
    return


@bincheckerbot_app.on_message(command("ping", BOT_USERNAME=BOT_USERNAME))
async def ping(_, m: Message):
    await funcs.common_ping(m, LOGGER)
    return


@bincheckerbot_app.on_message(command("about", BOT_USERNAME=BOT_USERNAME))
async def about_owner(c: Client, m: Message):
    await funcs.common_about(c, m, BOT_USERNAME)
    return


# Bot Specific Commands
@bincheckerbot_app.on_message(
    command("bin", BOT_USERNAME=BOT_USERNAME) & (filters.private | filters.group),
)
async def chkBin(_, m: Message):
    if len(m.text.split()) == 1:
        await m.reply_text("Please type a bin after the command.", quote=True)
        return
    replymsg = await m.reply_text("Checking bin...", quote=True)
    CCBin = m.text.split(None, 1)[1]
    try:
        LOGGER.info(f"UserID {m.from_user.id} checking bin {CCBin}...")
        binInfo = await getBinInfo(CCBin)
        if binInfo == "notValid!":
            await replymsg.edit_text("This bin is not valid!")
            return
        await replymsg.edit_text(text=binInfo)
    except Exception as ef:
        await replymsg.edit_text(
            f"<b>Error:</b> <code>{ef}</code>\n\nReport to @{Vars.SUPPORT_GROUP}",
        )
        LOGGER.error(ef)
    return


async def getBinInfo(gbin: str or int):

    lookup_url = f"https://lookup.binlist.net/{gbin}"
    rInfo = (await AioHttp.get_json(lookup_url))[0]

    if not rInfo:
        return "notValid!"

    infoText = "<b>Valid Bin ✅</b>"

    for key, value in {
        "Bin": gbin,
        "Type": rInfo["type"],
        "Brand": rInfo["brand"],
        "Country": rInfo["country"]["name"] + " " + rInfo["country"]["emoji"],
        "Bank": rInfo["bank"]["name"],
    }.items():
        try:
            if value == gbin:
                value = f"<code>{value}</code>"
            infoText += f"\n<b>{key.capitalize()}</b>: {value}"
        except KeyError:
            pass
        except Exception as ef:
            LOGGER.error(ef)

    return infoText
