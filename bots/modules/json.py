from kantex.html import Code
from pyrogram.types import Message
from pyrogram.types.messages_and_media import message

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("json", pm_only=True)
@joinCheck()
async def json(_, m: Message):
    await m.reply_text(Code(m if not m.reply_to_message else m.reply_to_message), quote=True)
