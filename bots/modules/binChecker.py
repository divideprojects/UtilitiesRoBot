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

from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.getBinInfo import getBinInfo
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "binChecker": {
            "info": "To get the bin info.",
            "usage": "/bin [bin]",
        },
    },
)


@app.command("bin", pm_only=True)
@joinCheck()
async def binChecker(_, m: Message):
    msg = await m.reply_text("...")
    if len(m.command) == 1:
        return await msg.edit_text(f"Usage: {MODULES.get('binChecker').get('usage')}")
    try:
        CCBin = int(m.command[1])
    except ValueError:
        return await msg.edit_text("Please give a valid bin!")
    await msg.edit_text(await getBinInfo(CCBin))
