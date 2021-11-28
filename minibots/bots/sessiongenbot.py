from asyncio import sleep
from asyncio.exceptions import TimeoutError

import telethon
from pyrogram import Client, filters
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import CallbackQuery, Message

from minibots.logger import LOGGER
from minibots.utils.common_funcs import funcs
from minibots.utils.common_text import Constants
from minibots.utils.custom_filters import command, user_check
from minibots.utils.ikb import ikb
from minibots.vars import Vars

# App for the bot
stringgenbot_app = Client(
    "StringGeneratorBot",
    api_id=Vars.API_ID,
    api_hash=Vars.API_HASH,
    bot_token=Vars.BOT_TOKEN_SESSIONBOT,
    workers=Vars.WORKERS,
)

with stringgenbot_app as app:
    BOT_USERNAME = app.get_me().username


# -- Constants -- #
class Pvt:
    START_TEXT = f"""
Hey {{}},
I'm @{BOT_USERNAME}, a simple bot used to generate string session for \
<a href='https://pypi.org/project/Pyrogram/'>pyrogram</a>.
"""
    HELP_TEXT = f"""
I will give you `STRING_SESSION` for your UserBot.

It needs `API_ID`, `API_HASH`, Phone Number and One Time Verification Code.
Which will be sent to your Phone Number.
You have to put **OTP** in `1 2 3 4 5` this format. __(Space between each number!)__

**NOTE:** If bot not Sending OTP to your Phone Number then /cancel and again Start the Process again.
"""


ASK_API_ID = f"""
Now send your <code>API_ID</code> same as <code>APP_ID</code> to Start Generating Session.
Press /cancel to stop the current process.
"""
HASH_TEXT = "Now send your <code>API_HASH</code>.\n\nPress /cancel to Cancel Task."
PHONE_NUMBER_TEXT = (
    "Now send your Telegram account's Phone number in International Format.\n"
    "Including Country code. Example: <b>+14154566376</b>\n\n"
    "Press /cancel to Cancel Task."
)
# -- Constants -- #


@stringgenbot_app.on_message(command("start", BOT_USERNAME=BOT_USERNAME))
async def start_bot(_, m: Message):
    await m.reply_text(
        Pvt.START_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        parse_mode="html",
        reply_markup=Constants.start_kb,
        quote=True,
    )
    return


@stringgenbot_app.on_message(command("help", BOT_USERNAME=BOT_USERNAME))
async def help_bot(_, m: Message):
    await m.reply_text(
        Pvt.HELP_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        parse_mode="markdown",
        reply_markup=ikb([Constants.back_help_start]),
        quote=True,
    )
    return


@stringgenbot_app.on_callback_query(filters.regex("^help.callback."))
async def help_bot_callback(_, q: CallbackQuery):
    qdata = q.data.split(".", 2)[2]
    if qdata == "help":
        qhelp = Pvt.HELP_TEXT
        qkb = ikb(
            [Constants.back_help_start],
        )
    elif qdata == "start":
        qhelp = Pvt.START_TEXT.format(q.message.from_user.mention)
        qkb = Constants.start_kb
    await q.message.edit_text(qhelp, reply_markup=qkb, disable_web_page_preview=True)
    await q.answer()
    return


# Common funcs
@stringgenbot_app.on_message(command("donate", BOT_USERNAME=BOT_USERNAME))
async def donate_owner(_, m: Message):
    await funcs.common_donate(m)
    return


@stringgenbot_app.on_message(command("ping", BOT_USERNAME=BOT_USERNAME))
async def ping(_, m: Message):
    await funcs.common_ping(m, LOGGER)
    return


@stringgenbot_app.on_message(command("about", BOT_USERNAME=BOT_USERNAME))
async def about_owner(c: Client, m: Message):
    await funcs.common_about(c, m, BOT_USERNAME)
    return


# Bot specific funcs


@stringgenbot_app.on_message(
    command("pyrogram", BOT_USERNAME=BOT_USERNAME) & user_check,
)
async def genStrPyrogram(_, m: Message):
    chat = m.chat
    api = await stringgenbot_app.ask(chat.id, ASK_API_ID)
    if await is_cancel(m, api.text):
        return

    # Check if API_ID is correct or not
    try:
        _ = int(api.text)
    except ValueError:
        await m.reply(
            "<code>API_ID</code> is not a valid Integer.\nPress /pyrogram to Start again.",
        )
        return

    api_id = api.text
    api_hash = await stringgenbot_app.ask(chat.id, HASH_TEXT)
    if await is_cancel(m, api_hash.text):
        return

    # Check if API_ID is correct or not
    if not len(api_hash.text) >= 30:
        await m.reply(
            "<code>API_HASH</code> is Invalid.\nPress /pyrogram to Start again.",
        )
        return

    api_hash = api_hash.text

    while True:
        number = await stringgenbot_app.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(m, number.text):
            return
        phone = number.text

        confirm = await stringgenbot_app.ask(
            chat.id,
            f'`Is "{phone}" correct? (y/n):` \n\nSend: `y` (If Yes)\nSend: `n` (If No)',
        )

        if await is_cancel(m, confirm.text):
            return
        if confirm.text.lower() == "y":
            break
        elif confirm.text.lower() == "n":
            return

    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await stringgenbot_app.send_message(
            chat.id,
            f"**ERROR:** `{str(e)}`\nPress /pyrogram to Start again.",
        )
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()

    try:
        code = await client.send_code(phone)
        await sleep(1)
    except FloodWait as e:
        await m.reply(f"You have Floodwait of {e.x} Seconds")
        return
    except ApiIdInvalid:
        await m.reply(
            "API ID and API Hash are Invalid.\nPress /pyrogram to Start again.",
        )
        return
    except PhoneNumberInvalid:
        await m.reply("Your Phone Number is Invalid.\nPress /pyrogram to Start again.")
        return

    try:
        otp = await stringgenbot_app.ask(
            chat.id,
            (
                "An OTP is sent to your phone number, "
                "Please enter OTP in `1 2 3 4 5` format. __(Space between each number!)__ \n\n"
                "If Bot not sending OTP then try and Start Task again with /pyrogram command to Bot.\n"
                "Press /cancel to Cancel."
            ),
            timeout=300,
        )

    except TimeoutError:
        await m.reply("Time limit reached of 5 min.\nPress /pyrogram to Start again.")
        return

    if await is_cancel(m, otp.text):
        return

    otp_code = otp.text

    try:
        await client.sign_in(
            phone,
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid:
        await m.reply("Invalid Code.\nPress /pyrogram to Start again.")
        return
    except PhoneCodeExpired:
        await m.reply("Code is Expired.\nPress /pyrogram to Start again.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await stringgenbot_app.ask(
                chat.id,
                "Your account have Two-Step Verification.\nPlease enter your Password.\n\nPress /cancel to Cancel.",
                timeout=300,
            )
        except TimeoutError:
            await m.reply(
                "`Time limit reached of 5 min.\n\nPress /pyrogram to Start again.`",
            )
            return
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await m.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await stringgenbot_app.send_message(chat.id, f"**ERROR:** `{str(e)}`")
        return

    try:
        session_string = await client.export_session_string()
        await client.send_message(
            "me",
            f"#PYROGRAM #STRING_SESSION\n\n```{session_string}``` \n\nBy @{BOT_USERNAME}\nA Bot By @DivideProjects",
        )
        await client.disconnect()
        await stringgenbot_app.send_message(
            chat.id,
            "String Session is Successfully Generated.\nClick on Below Button.",
            reply_markup=ikb(
                [
                    [
                        (
                            "Show String Session",
                            f"tg://openmessage?user_id={chat.id}",
                            "url",
                        ),
                    ],
                ],
            ),
        )
    except Exception as e:
        await stringgenbot_app.send_message(chat.id, f"**ERROR:** `{str(e)}`")
        return


@stringgenbot_app.on_message(
    command("telethon", BOT_USERNAME=BOT_USERNAME) & user_check,
)
async def genStrTelethon(_, m: Message):
    chat = m.chat
    api = await stringgenbot_app.ask(chat.id, ASK_API_ID)
    if await is_cancel(m, api.text):
        return

    # Check if API_ID is correct or not
    try:
        _ = int(api.text)
    except ValueError:
        await m.reply(
            "<code>API_ID</code> is not a valid Integer.\nPress /telethon to Start again.",
        )
        return

    api_id = api.text
    api_hash = await stringgenbot_app.ask(chat.id, HASH_TEXT)
    if await is_cancel(m, api_hash.text):
        return

    # Check if API_ID is correct or not
    if not len(api_hash.text) >= 30:
        await m.reply(
            "<code>API_HASH</code> is Invalid.\nPress /telethon to Start again.",
        )
        return
    api_hash = api_hash.text
    number_ask = await stringgenbot_app.ask(chat.id, PHONE_NUMBER_TEXT)
    number = number_ask.text
    current_client = telethon.TelegramClient(
        telethon.sessions.StringSession(),
        api_id=api_id,
        api_hash=api_hash,
    )
    while True:
        await current_client.connect()
        sent = await current_client.send_code_request(number)
        otp = await stringgenbot_app.ask(
            chat.id,
            (
                "An OTP is sent to your phone number, "
                "Please enter OTP in `1 2 3 4 5` format. __(Space between each number!)__ \n\n"
                "If Bot not sending OTP then try and Start Task again with /telethon command to Bot.\n"
                "Press /cancel to Cancel."
            ),
            timeout=300,
        )
        received_code = otp.text.strip()
        received_tfa_code = None
        received_code = "".join(received_code.split(" "))
        try:
            await current_client.sign_in(
                number,
                code=received_code,
                password=received_tfa_code,
            )
        except telethon.errors.rpcerrorlist.PhoneCodeInvalidError:
            await m.reply("Invalid Code.\nPress /telethon to Start again.")
            return
        except telethon.errors.rpcerrorlist.SessionPasswordNeededError:
            try:
                two_step_code = await stringgenbot_app.ask(
                    chat.id,
                    "Your account have Two-Step Verification.\nPlease enter your Password.\n\nPress /cancel to Cancel.",
                    timeout=300,
                )
                await current_client.sign_in(password=two_step_code.text)
                pass
            except TimeoutError:
                await m.reply(
                    "Time limit reached of 5 min.\nPress /telethon to Start again.",
                )
                return

        except TimeoutError:
            await m.reply(
                "Time limit reached of 5 min.\nPress /telethon to Start again.",
            )
            return

        me = await current_client.get_me()
        session = current_client.session.save()
        await m.reply_text(
            f"Successfully Signed in as {me.username}\nTelethon session has been sent to your PM",
        )
        omk = await current_client.send_message("me", f"```{session}```")
        await omk.reply("👆 This is your Telethon String Session")
        await current_client.disconnect()
        current_client = ""


async def is_cancel(m: Message, text: str):
    if text.startswith("/cancel"):
        await m.reply("Process Cancelled.")
        return True
    return False
