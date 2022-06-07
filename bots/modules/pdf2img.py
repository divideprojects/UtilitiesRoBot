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

from os import remove

from pdf2image import convert_from_path
from pyrogram.errors import MultiMediaTooLong
from pyrogram.types import InputMediaPhoto, Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars

MODULES.update(
    {
        "pdf2img": {
            "info": "To convert a PDF to images.",
            "usage": "/pdf2img [reply to pdf]",
        },
    },
)


@app.command("pdf2img", pm_only=True)
@joinCheck()
async def pdf2img(c, m: Message):
    if (
        m.reply_to_message and m.reply_to_message.document
    ) and m.reply_to_message.document.mime_type == "application/pdf":
        user_id = m.from_user.id
        rmsg = await m.reply_text("Converting PDF to image...")
        exact_file = await c.download_media(
            message=m.reply_to_message,
            file_name=f"{Vars.DOWN_PATH}/{user_id}/",
        )
        images = convert_from_path(exact_file)

        # empty list so that it can be used in the for loop to add the images
        # to the message
        media_photos = []

        for i in range(len(images)):
            page_no = i + 1  # lists work wierd way

            file_name = f"{Vars.DOWN_PATH}/{user_id}/page_{page_no}.jpg"
            images[i].save(file_name, "JPEG")
            media_photos.append(
                {
                    "file": file_name,
                    "caption": f"Page {page_no}",
                },
            )
        try:
            await c.send_media_group(
                user_id,
                [
                    InputMediaPhoto(i["file"], caption=i["caption"])
                    for i in media_photos
                ],
            )
        except MultiMediaTooLong:
            remove(exact_file)
            for i in media_photos:
                remove(i["file"])
            return await rmsg.edit_text("It's too big to send :(")
        await rmsg.delete()
        remove(exact_file)
        for i in media_photos:
            remove(i["file"])
    else:
        await m.reply_text(f"Usage: {MODULES.get('pdf2img').get('usage')}")

    return
