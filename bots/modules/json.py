from kantex.html import Code
from pyrogram.types import Message

from .. import app
from ..utils.joinCheck import joinCheck


@app.command("json", pm_only=True)
@joinCheck()
async def json(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a message to get the JSON.")
        return

    json_details = m.reply_to_message.__dict__
    await m.reply_text(Code(json_details), quote=True)
