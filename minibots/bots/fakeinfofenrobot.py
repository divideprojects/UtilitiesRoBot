from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from minibots.logger import LOGGER
from minibots.utils.aiohttp_helper import AioHttp
from minibots.utils.common_funcs import funcs
from minibots.utils.common_text import Constants
from minibots.utils.custom_filters import command, user_check
from minibots.utils.ikb import ikb
from minibots.vars import Vars

# App for the bot
fakeinfogenbot_app = Client(
    "FakeInfoGen",
    api_id=Vars.API_ID,
    api_hash=Vars.API_HASH,
    bot_token=Vars.BOT_TOKEN_INFOGEN,
    workers=Vars.WORKERS,
)
with fakeinfogenbot_app as app:
    BOT_USERNAME = app.get_me().username


# -- Constants -- #
class Pvt:
    START_TEXT = f"""
Hey {{}}!
I'm @{BOT_USERNAME}, a bot used to generate \
random fake data!
"""
    HELP_TEXT = f"""
__**Commands:**__
{Vars.PRIMARY_HANDLER}start - Show Start message.
{Vars.PRIMARY_HANDLER}help - Check this help message.
{Vars.PRIMARY_HANDLER}geninfo <gender> - Generate a new fake user with random details.
Specify gender as 'male' or 'female' to get customised profile!
{Vars.PRIMARY_HANDLER}about - Get some info about me.
{Vars.PRIMARY_HANDLER}donate - Get info about donating my owner.
"""


# -- Constants End -- #

# -- Bot Function starts -- #
@fakeinfogenbot_app.on_message(command("start", BOT_USERNAME=BOT_USERNAME))
async def start_bot(_, m: Message):
    await m.reply_text(
        Pvt.START_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        parse_mode="html",
        reply_markup=Constants.start_kb,
        quote=True,
    )
    return


@fakeinfogenbot_app.on_message(command("help", BOT_USERNAME=BOT_USERNAME))
async def help_bot(_, m: Message):
    await m.reply_text(
        Pvt.HELP_TEXT,
        disable_web_page_preview=True,
        parse_mode="markdown",
        reply_markup=ikb([Constants.back_help_start]),
        quote=True,
    )
    return


@fakeinfogenbot_app.on_callback_query(filters.regex("^help.callback."))
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


# Common Commands
@fakeinfogenbot_app.on_message(command("donate", BOT_USERNAME=BOT_USERNAME))
async def donate_owner(_, m: Message):
    await funcs.common_donate(m)
    return


@fakeinfogenbot_app.on_message(command("ping", BOT_USERNAME=BOT_USERNAME))
async def ping(_, m: Message):
    await funcs.common_ping(m, LOGGER)
    return


@fakeinfogenbot_app.on_message(command("about", BOT_USERNAME=BOT_USERNAME))
async def about_owner(c: Client, m: Message):
    await funcs.common_about(c, m, BOT_USERNAME)
    return


# Bot specific command
@fakeinfogenbot_app.on_message(
    command("geninfo", BOT_USERNAME=BOT_USERNAME) & filters.private & user_check,
)
async def send_random_data(_, m: Message):

    chkUrl = "https://randomuser.me/api/1.3/"

    if len(m.command) == 2:
        if m.command[1] in ("male", "female"):
            gender = m.command[1]
            textrply = f"<code>Generating fake <b>{gender}</b> profile</code>"
            chkUrl += f"?gender={gender}"
        else:
            pass
    else:
        textrply = "Making random fake user data..."

    replymsg = await m.reply_text(textrply, quote=True)

    try:
        # LOGGER.info(f"UserID {m.from_user.id} generating fake data...")
        infoText, userPic = await genFakeInfo(chkUrl)
        if infoText == "API Unreachable":
            await replymsg.edit_text("API Unreachable, please try again")
        elif not (infoText or userPic):
            await replymsg.edit_text(
                f"Error Generating data, if problem persistes contact @{Vars.SUPPORT_GROUP}",
                quote=True,
            )
        else:
            await m.reply_document(userPic, caption=infoText)
            await replymsg.delete()  # Delete old message
    except Exception as ef:
        await replymsg.edit_text(
            f"<b>Error:</b> <code>{ef}</code>\n\nReport to @{Vars.SUPPORT_GROUP}",
            quote=True,
        )
        LOGGER.error(ef)
    return


async def genFakeInfo(chkUrl):

    rData, resp = await AioHttp.get_json(chkUrl)
    if not resp.status == 200:
        return "API Unreachable", None

    user = rData["results"][0]

    # Begin parsing data
    dobTime = datetime.strptime(user["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    userPic = user["picture"]["large"]

    infoText = f"""
<b>Name:</b> <code>{user['name']['title']} {user['name']['first']} {user['name']['last']}</code>
<b>Gender:</b> <code>{user['gender']}</code>
<b>Location:</b>
    <b>Street:</b> <code>{user['location']['street']['number']}, {user['location']['street']['name']}</code>
    <b>City:</b> <code>{user['location']['city']}</code>
    <b>State:</b> <code>{user['location']['state']}</code>
    <b>Country:</b> <code>{user['location']['country']}</code>
    <b>Postcode:</b> <code>{user['location']['postcode']}</code>
<b>Email:</b> <code>{user['email']}</code>
<b>DOB:</b> <code>{dobTime.strftime("%B %m, %Y")}</code>
<b>Age:</b> <code>{user['dob']['age']}</code>
<b>Cellphone:</b> <code>{user['cell']}</code>
<b>Phone:</b> <code>{user['phone']}</code>
"""

    return infoText, userPic
