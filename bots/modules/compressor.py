from shutil import rmtree

from pyrogram.types import Message

from .. import DownPath, app
from ..utils.compressImage import compress_image
from ..utils.joinCheck import joinCheck


@app.command("tinify", pm_only=True)
@joinCheck()
async def binChecker(c, m: Message):
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
            rmtree(new_filename)
        else:
            await m.reply_text("Reply to a photo or a document.")
    except AttributeError:
        pass

    return
