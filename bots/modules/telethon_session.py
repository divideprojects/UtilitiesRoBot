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
from pyrogram.types import Message
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import (
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("telethon", pm_only=True)
@joinCheck()
async def telethonSession(c, m: Message):
    apiId = await m.chat.ask("Enter your API_ID.\nSend /cancel to Cancel.")
    if await is_cancel(apiId):
        return
    if not apiId.text.isdigit():
        return await m.reply_text(
            "Invalid API_ID \nSend /telethon to Restart the Process",
        )
    apiHash = await m.chat.ask("Enter your API_HASH.\nSend /cancel to Cancel.")
    if await is_cancel(apiHash):
        return
    number = await m.chat.ask("Enter your Phone Number.\nSend /cancel to Cancel.")
    if await is_cancel(number):
        return
    tclient = TelegramClient(StringSession(), apiId.text, apiHash.text)
    try:
        if not tclient.is_connected():
            await tclient.connect()
        await tclient.disconnect()
        await tclient.connect()
    except Exception as e:
        return await c.send_message(m.chat.id, f"Error: {e}")
    while 1:
        try:
            code = await tclient.send_code_request(number.text)
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
                await tclient.sign_in(number, code=received_code, password=None)
            except PhoneCodeInvalidError:
                return await m.reply_text(
                    "Invalid OTP.\nSend /telethon to ReStart.",
                )
            except SessionPasswordNeededError:
                twoStepPass = await m.chat.ask(
                    "Enter your 2-Step Verification Password.\nSend /cancel to Cancel.",
                )
                if await is_cancel(twoStepPass):
                    return
                await tclient.sign_in(password=twoStepPass.text)
                pass
            session_string = tclient.session.save()
            try:
                await c(JoinChannelRequest("@DivideProjects"))
            except BaseException:
                pass
            reply = await c.send_message(
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
                f"Your Telethon String Session.\nNOTE: STRING SESSIONS ARE CONFIDENTIAL, IT MUST AND SHOULN'T BE SHARED WITH ANYONE.\n@{(await c.get_me()).username}",
            )
            await tclient.disconnect()
            break
        except Exception as e:
            return await c.send_message(m.chat.id, f"Error: {e}")


async def is_cancel(m: Message):
    if m.text.startswith("/cancel"):
        await m.reply("The process has been cancelled")
        return True
    return False
