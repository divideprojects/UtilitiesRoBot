from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.getBinInfo import getBinInfo
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "binChecker": {
            "info": "To get the bin info.",
            "usage": "/bin [bin]",
        },
    },
)


@app.command("bin")
@joinCheck()
async def binChecker(_, m: Message):
    msg = await m.reply_text("...")
    if len(m.command) == 1:
        await msg.edit_text(
            f"Usage: {MODULES.get('binChecker').get('usage')}"
        )
        return
    try:
        CCBin = int(m.command[1])
    except ValueError:
        await msg.edit_text("Please give a valid bin!")
        return
    await msg.edit_text(await getBinInfo(CCBin))
