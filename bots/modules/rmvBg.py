import contextlib
from os import remove

from kantex.html import Code
from pyrogram import Client
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck
from bots.utils.rmvBg import rmvBg
from bots.vars import Vars

MODULES.update(
    {
        "removebg": {
            "info": "To remove the background of an image.",
            "usage": "/rmbg [reply to image]",
        },
    },
)


@app.command("rmbg")
@joinCheck()
async def rmvbg(c: Client, m: Message):
    with contextlib.suppress(AttributeError):
        if m.reply_to_message.photo or (
            m.reply_to_message.document
            and m.reply_to_message.document.mime_type.startswith("image/")
        ):
            rmsg = await m.reply_text("...")
            exact_file = await c.download_media(
                message=m.reply_to_message,
                file_name=f"{Vars.DOWN_PATH}/{m.from_user.id}/",
            )
            try:
                new_filename = await rmvBg(exact_file)
                new_filename = f"{exact_file}_no_bg.png"

            except ValueError as e:
                await rmsg.edit_text(f"Error: {e}")
                return

            await m.reply_document(
                new_filename,
                caption=f"{Code(m.reply_to_message.document.file_name)} background removed by {m.from_user.mention}\n\nBackground removed using @{(await c.get_me()).username} by @DivideProjects",
            )
            await rmsg.delete()
            remove(new_filename)
            remove(exact_file)
        else:
            await m.reply_text(f"Usage: {MODULES.get('removebg').get('usage')}")
    return
