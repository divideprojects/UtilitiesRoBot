from kantex.html import Code
from pyrogram.types import Message

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("json", pm_only=True)
@joinCheck()
async def json(_, m: Message):
    msg = m if not m.replied_to_message else m.replied_to_message
    if len(length) < 4095:
        return await message.reply_text(str(Code(msg)))
    fName = f"json_{m.from_user.id}_{m.message_id}.json"
    with open(fName, "w+") as file:
        file.write(msg)
        file.close()
    await message.reply_document(fName)