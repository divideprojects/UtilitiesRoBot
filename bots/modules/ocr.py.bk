from kantex._base.styles import Italic
from kantex.html import Bold, Code
from pyrogram.types import Message
from ujson import dumps

from bots import DownPath, SupportGroup, app
from bots.utils.joinCheck import joinCheck
from bots.utils.ocr import conv_image, ocr_space_file


@app.command("ocr", pm_only=True)
@joinCheck()
async def ocr(c, m: Message):
    user_id = m.from_user.id
    if m.reply_to_message.document or m.reply_to_message.photo:
        rMsg = await m.reply_text("Extracting text from document...")

        dl_file = await c.download_media(
            message=m.reply_to_message,
            file_name=f"{DownPath}/{user_id}/",
        )
        if dl_file.endswith(".webp"):
            dl_file = await conv_image(dl_file)

        result = await ocr_space_file(dl_file, language="eng")

        try:
            ParsedText = result["ParsedResults"][0]["ParsedText"]
            ProcessingTimeInMilliseconds = str(
                int(result["ProcessingTimeInMilliseconds"]) // 1000,
            )
        except Exception as e:
            await rMsg.edit_text(
                Bold("Error:"),
                "\n",
                Code(str(e)),
                f"Report This to {SupportGroup}",
                "\n\n",
                f"{Code(dumps(result, sort_keys=True, indent=4))}",
            )
        else:
            await rMsg.edit_text(
                Bold("OCR Results:"),
                "\n\n",
                f"`{ParsedText}`\n\n",
                Bold("OCR Processing Time"),
                "\n\n",
                Italic(f"{ProcessingTimeInMilliseconds} ms"),
            )
    return
