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

import contextlib
from os import remove

from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.compressImage import compress_image
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars

MODULES.update(
    {
        "tinify": {
            "info": "To compress an image.",
            "usage": "/tinify [reply to image]",
        },
    },
)


@app.command("tinify", pm_only=True)
@joinCheck()
async def tinify(c, m: Message):
    with contextlib.suppress(AttributeError):
        if m.reply_to_message.photo or (
            m.reply_to_message.document
            and m.reply_to_message.document.mime_type.startswith("image/")
        ):
            rmsg = await m.reply_text("Compressing photo...")
            exact_file = await c.download_media(
                message=m.reply_to_message,
                file_name=f"{Vars.DOWN_PATH}/{m.from_user.id}/",
            )
            try:
                new_filename = await compress_image(exact_file)
            except ValueError as e:
                await rmsg.edit_text(f"Error: {e}")
                return
            await m.reply_document(
                new_filename,
                caption="Compressed image.",
            )
            await rmsg.delete()
            remove(new_filename)
            remove(exact_file)
        else:
            await m.reply_text(f"Usage: {MODULES.get('tinify').get('usage')}")
    return
