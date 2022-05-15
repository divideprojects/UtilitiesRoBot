from kantex.html import Code
from pyrogram.client import Client
from pyrogram.errors import PhoneCodeExpired, PhoneCodeInvalid, SessionPasswordNeeded
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import (
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from bots import MODULES, app

from bots.utils.captcha import hcaptcha
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "sessions": {
            "info": "To generate Pyrogram/Telethon String Sessions.",
            "usage": "/session",
        },
    },
)


async def get_details(m: Message):
    apiId = await m.chat.ask("Enter your API_ID.\nSend /cancel to Cancel.")
    if await is_cancel(apiId):
        return
    if not apiId.text.isdigit():
        return await m.reply_text(
            "Invalid API_ID \nSend /session to Restart the Process",
        )
    apiHash = await m.chat.ask("Enter your API_HASH.\nSend /cancel to Cancel.")
    if await is_cancel(apiHash):
        return
    number = await m.chat.ask("Enter your Phone Number.\nSend /cancel to Cancel.")
    if await is_cancel(number):
        return
    return apiId.text, apiHash.text, number.text


async def generate_pyrogram_session(
    m: Message,
    api_id: int,
    api_hash: str,
    phone_number,
):
    pclient = Client(":memory:", api_id=api_id, api_hash=api_hash)
    try:
        await pclient.connect()
    except ConnectionError:
        await pclient.disconnect()
        await pclient.connect()
    try:
        code = await pclient.send_code(phone_number)
        otp = await m.chat.ask(
            f"""
You will receive a OTP in from Telegram.
Send it by adding space after an charecter.

Like, if your OTP is 123456, send it like {str(Code("1 2 3 4 5 6"))} otherwise Telegram will revoke the Code.

Send /cancel to cancel the process.
            """,
        )
        if await is_cancel(otp):
            return
        received_code = otp.text.strip()
        received_code = "".join(received_code.split(" "))
        try:
            await pclient.sign_in(
                phone_number,
                code.phone_code_hash,
                phone_code=received_code,
            )
        except (PhoneCodeExpired, PhoneCodeInvalid):
            return await m.reply_text("Invalid OTP.\nSend /session to ReStart.")
        except SessionPasswordNeeded:
            password = await m.chat.ask(
                "Enter your Password.\nSend /cancel to Cancel.",
            )
        if await is_cancel(password):
            return
        await pclient.check_password(password=password.text)
        await password.delete()
        session = await pclient.export_session_string()
        await pclient.join_chat("@DivideProjects")
        reply = await m.reply_text(str(Code(session)))
        await reply.reply_text(
            f"Your Pyrogram String Session, Same can be found in your Saved Messages.",
        )
        sent = await pclient.send_message("me", str(Code(session)))
        await sent.reply_text(
            f"Your Pyrogram String Session.\nNOTE: STRING SESSIONS ARE CONFIDENTIAL, IT MUST AND SHOULN'T BE SHARED WITH ANYONE.\n@{(await m._client.get_me()).username}",
        )
        await pclient.disconnect()
    except Exception as e:
        return await m._client.send_message(m.chat.id, str(e))


async def generate_telethon_session(
    m: Message,
    api_id: int,
    api_hash: str,
    phone_number,
):
    tclient = TelegramClient(StringSession(), api_id, api_hash)
    try:
        if not tclient.is_connected():
            await tclient.connect()
        await tclient.disconnect()
        await tclient.connect()
    except Exception as e:
        return await m._client.send_message(m.chat.id, f"Error: {e}")
    while 1:
        try:
            code = await tclient.send_code_request(phone_number)
            otp = await m.chat.ask(
                f"""
You will receive a OTP in from Telegram.
Send it by adding space after an charecter.

Like, if your OTP is 123456, send it like {str(Code("1 2 3 4 5 6"))} otherwise Telegram will revoke the Code.

Send /cancel to cancel the process.
            """,
            )
            if await is_cancel(otp):
                return
            received_code = otp.text.strip()
            received_code = "".join(received_code.split(" "))
            try:
                await tclient.sign_in(phone_number, code=received_code, password=None)
            except PhoneCodeInvalidError:
                return await m.reply_text(
                    "Invalid OTP.\nSend /session to ReStart.",
                )
            except SessionPasswordNeededError:
                twoStepPass = await m.chat.ask(
                    "Enter your 2-Step Verification Password.\nSend /cancel to Cancel.",
                )
                if await is_cancel(twoStepPass):
                    return
                await tclient.sign_in(password=twoStepPass.text)
                await twoStepPass.delete()
                pass
            session_string = tclient.session.save()
            try:
                await m._client(JoinChannelRequest("@DivideProjects"))
            except BaseException:
                pass
            reply = await m._client.send_message(
                m.chat.id,
                str(Code(session_string)),
            )
            await reply.reply_text(
                f"Your Telethon String Session, Same can be found in your Saved Messages.",
            )
            sent = await tclient.send_message(
                "me",
                str(Code(session_string)),
                parse_mode="html",
            )
            await sent.reply(
                f"Your Telethon String Session.\nNOTE: STRING SESSIONS ARE CONFIDENTIAL, IT MUST AND SHOULN'T BE SHARED WITH ANYONE.\n@{(await m._client.get_me()).username}",
            )
            await tclient.disconnect()
            break
        except Exception as e:
            return await m._client.send_message(m.chat.id, f"Error: {e}")


async def is_cancel(m: Message):
    if m.text.startswith("/cancel"):
        await m.reply("The process has been cancelled")
        return True
    return False


@app.command("session")
@joinCheck()
@hcaptcha()
async def genSession(_, message):
    return await message.reply_text(
        "Choose a Session to Generate",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Pyrogram", callback_data="pyro"),
                    InlineKeyboardButton("Telethon", callback_data="tele"),
                ],
            ],
        ),
    )


@app.callback(["pyro", "tele"])
async def genPyroSession(_, cb: CallbackQuery):
    api_id, api_hash, number = await get_details(cb.message)
    if isinstance(api_id, Message):
        return
    if cb.data == "pyro":
        await cb.message.edit_text("Generating Pyrogram Session...")
        return await generate_pyrogram_session(cb.message, api_id, api_hash, number)
    if cb.data == "tele":
        await cb.message.edit_text("Generating Telethon Session...")
        return await generate_telethon_session(cb.message, api_id, api_hash, number)
