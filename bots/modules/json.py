from os import remove

from kantex.html import Code
from pyrogram.types import Message

from bots import app, MODULES
from bots.utils.joinCheck import joinCheck

MODULES.update({
    "json": {
        "info": "To get the json data of the message.",
        "usage": "/geninfo [optional: reply]",
    }
})


@app.command("json", pm_only=False)
@joinCheck()
async def json(_, m: Message):
    msg = m if not m.reply_to_message else m.reply_to_message
    if len(str(msg)) < 4095:
        return await m.reply_text(str(Code(str(msg))))
    fName = f"json_{m.from_user.id}_{m.message_id}.json"
    with open(fName, "w+") as file:
        file.write(str(msg))
    await m.reply_document(fName)
    remove(fName)
