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

from pyrogram.types import Message

from bots import DownPath, app
from bots.utils.compressImage import compress_image
from bots.utils.joinCheck import joinCheck


@app.command("tinify", pm_only=True)
@joinCheck()
async def tinify(c, m: Message):
    try:
        if m.reply_to_message.photo or (
            m.reply_to_message.document
            and m.reply_to_message.document.mime_type.startswith("image/")
        ):
            rmsg = await m.reply_text("Compressing photo...")
            exact_file = await c.download_media(
                message=m.reply_to_message,
                file_name=f"{DownPath}/{m.from_user.id}/",
            )
            new_filename = await compress_image(exact_file)
            await m.reply_document(
                new_filename,
                caption="Compressed image.",
            )
            await rmsg.delete()
            remove(new_filename)
            remove(exact_file)
        else:
            await m.reply_text("Reply to a photo or a document.")
    except AttributeError:
        pass

    return
