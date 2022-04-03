from pyrogram.types import Message

from bots import app
from bots.utils.getBinInfo import getBinInfo
from bots.utils.joinCheck import joinCheck
from bots.utils.captcha import hcaptcha


@app.command("bin", pm_only=True)
@joinCheck()
@hcaptcha()
async def binChecker(_, m: Message):
    msg = await m.reply_text("...")
    if len(m.command) == 1:
        return await msg.edit_text("Please type a bin after the command.")
    try:
        CCBin = int(m.command[1])
    except ValueError:
        return await msg.edit_text("Please give a valid bin!")
    await msg.edit_text(await getBinInfo(CCBin))
