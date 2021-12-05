from kantex.html import Code
from pyrogram.types import Message

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("json", pm_only=True)
@joinCheck()
async def json(_, m: Message):
    msg = m if not m.reply_to_message else m.reply_to_message
    if len(str(msg)) < 4095:
        return await message.reply_text(str(Code(str(msg))))
    fName = f"json_{m.from_user.id}_{m.message_id}.json"
    with open(fName, "w+") as file:
        file.write(str(msg))
        file.close()
    await message.reply_document(fName)