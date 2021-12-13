from pyrogram.types import Message

from bots import app
from bots.utils.getBinInfo import getBinInfo
from bots.utils.joinCheck import joinCheck


@app.command("bin", pm_only=True)
@joinCheck()
async def binChecker(_, m: Message):
    msg = await m.reply_text("...")
    if len(m.command) == 0:
        return await msg.edit_text("Please type a bin after the command.")
    CCBin = m.command[1]
    await msg.edit_text(await getBinInfo(CCBin))
