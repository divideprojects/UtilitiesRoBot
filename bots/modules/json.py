# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2022 Divide Projects <https://github.com/DivideProjects>

# This file is part of Utilities Robot.

# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Utilities Robot.  If not, see <https://www.gnu.org/licenses/>.

from html import escape
from os import remove

from kantex.html import Code
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "json": {
            "info": "To get the json data of the message.",
            "usage": "/json [optional: reply]",
        },
    },
)


@app.command("json", pm_only=False)
@joinCheck()
async def json(_, m: Message):
    ms = m.reply_to_message or m
    if len(str(ms)) > 4020:
        filen = f"json_{m.chat.id}_{m.id}.json"
        with open(filen, "w+") as _file:
            _file.write(str(ms).strip())
            _file.flush()
        await m.reply_document(filen)
        remove(filen)
    else:
        await m.reply_text(Code(escape(str(ms))))
    return
