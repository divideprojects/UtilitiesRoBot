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
from os import remove, rename

from PIL import Image

from bots import OCR_SPACE_API_KEY
from bots.utils.aiohttp import AioHttp


async def conv_image(image: str):
    im = Image.open(image)
    im.save(image, "PNG")
    new_file_name = image + ".png"
    rename(image, new_file_name)
    remove(image)  # remove old file
    return new_file_name


async def ocr_space_file(
    filename,
    overlay=False,
    api_key=OCR_SPACE_API_KEY,
    language="eng",
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        rjson, resp = await AioHttp.post_json(
            "https://api.ocr.space/parse/image",
            data=payload,
            files={filename: f},
        )

    return rjson if resp.status == 200 else None
