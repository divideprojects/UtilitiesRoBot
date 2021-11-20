from os import remove, rename

from PIL import Image

from bots import OCR_SPACE_API_KEY
from bots.utils.aiohttp import Aiohttp


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
        rjson, resp = await Aiohttp.post_json(
            "https://api.ocr.space/parse/image",
            data=payload,
            files={filename: f},
        )

    return rjson if resp.status == 200 else None
