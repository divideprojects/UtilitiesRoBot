from .. import app
from ..utils.getBinInfo import getBinInfo


@app.command("bin", pm_only=True)
async def binChecker(client, message):
    msg = await message.reply_text("...")
    if len(message.text.split()) == 1:
        return await msg.edit_text("Please type a bin after the command.")
    CCBin = message.text.split(None, 1)[1]
    await msg.edit_text((await getBinInfo(CCBin)))
