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
from os import remove

from kantex.html import Code
from pyrogram.types import Message

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("json", pm_only=True)
@joinCheck()
async def json(_, m: Message):
    msg = m if not m.reply_to_message else m.reply_to_message
    if len(str(msg)) < 4095:
        return await m.reply_text(str(Code(str(msg))))
    fName = f"json_{m.from_user.id}_{m.message_id}.json"
    with open(fName, "w+") as file:
        file.write(str(msg))
    await m.reply_document(fName)
    remove(fName)
