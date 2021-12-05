#
# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2021 Divide Projects <https://github.com/DivideProjects>
#
# This file is part of Utilities Robot.
#
# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.
#
from kantex.html import Code
from pyrogram.client import Client
from pyrogram.errors import PhoneCodeExpired, PhoneCodeInvalid, SessionPasswordNeeded
from pyrogram.types import Message

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("pyrogram", pm_only=True)
@joinCheck()
async def pyrogram_session(c, m: Message):
    apiId = await m.chat.ask("Enter your API_ID.\nSend /cancel to Cancel.")
    if await is_cancel(apiId):
        return
    if not apiId.text.isdigit():
        return await m.reply_text(
            "Invalid API_ID \nSend /pyrogram to Restart the Process",
        )
    apiHash = await m.chat.ask("Enter your API_HASH.\nSend /cancel to Cancel.")
    if await is_cancel(apiHash):
        return
    number = await m.chat.ask("Enter your Phone Number.\nSend /cancel to Cancel.")
    if await is_cancel(number):
        return
    pclient = Client(":memory:", api_id=apiId.text, api_hash=apiHash.text)
    try:
        await pclient.connect()
    except ConnectionError:
        await pclient.disconnect()
        await pclient.connect()
    try:
        code = await pclient.send_code(number.text)
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
                number.text,
                code.phone_code_hash,
                phone_code=received_code,
            )
        except (PhoneCodeExpired, PhoneCodeInvalid):
            return await m.reply_text("Invalid OTP.\nSend /pyrogram to ReStart.")
        except SessionPasswordNeeded:
            password = await m.chat.ask(
                "Enter your Password.\nSend /cancel to Cancel.",
            )
        if await is_cancel(password):
            return
        await pclient.check_password(password=password.text)
        session = await pclient.export_session_string()
        await pclient.join_chat("@DivideProjects")
        reply = await m.reply_text(str(Code(session)))
        await reply.reply_text(
            f"Your Pyrogram String Session, Same can be found in your Saved Messages.",
        )
        sent = await pclient.send_message("me", str(Code(session)))
        await sent.reply_text(
            f"Your Pyrogram String Session.\nNOTE: STRING SESSIONS ARE CONFIDENTIAL, IT MUST AND SHOULN'T BE SHARED WITH ANYONE.\n@{(await c.get_me()).username}",
        )
        await pclient.disconnect()
    except Exception as e:
        return await c.send_message(m.chat.id, str(e))


async def is_cancel(m: Message):
    if m.text.startswith("/cancel"):
        await m.reply("The process has been cancelled")
        return True
    return False
