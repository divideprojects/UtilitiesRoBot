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
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.#
from pyrogram.types import Message

from bots import SupportGroup, app
from bots.utils.genFakeInfo import genFakeInfo
from bots.utils.joinCheck import joinCheck


@app.command("geninfo", pm_only=True)
@joinCheck()
async def genInfo(_, m: Message):
    gender = None
    msg = await m.reply_text("...")
    chkUrl = "https://randomuser.me/api/1.3/"
    if len(m.command) != 0:
        if m.command[1] in ("male", "female"):
            gender = m.command[1]
            chkUrl += f"?gender={gender}"
            text = f"Generating a Fake {m.command[1]} user data."
        else:
            text = f"Generating a Fake user data."
    else:
        text = f"Generating a Fake user data."
    await msg.edit_text(text)
    infoText, userPic = await genFakeInfo(chkUrl)
    if infoText == "API Unreachable":
        return await msg.edit_text("API Unreachable at the Moment, Try again Later")
    if not (infoText or userPic):
        return await msg.edit_text(
            f"error generating fake data{f': gender ' if gender else ''} \nReport this at {SupportGroup}",
        )
    await m.reply_document(userPic, caption=infoText)
    await msg.delete()
