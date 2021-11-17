from kantex.html import *

from .. import app, SupportGroup
from ..utils.genFakeInfo import genFakeInfo


@app.command("geninfo", pm_only=True)
async def genInfo(client, message):
    gender = None
    msg = await message.reply_text("...")
    chkUrl = "https://randomuser.me/api/1.3/"
    if len(message.command) < 0:
        if message.command[1] in ("male", "female"):
            gender = message.command[1]
            chkUrl += f"?gender={gender}"
            text = f"Generating a Fake {message.command[1]} user data."
        else:
            text = f"Generating a Fake user data."
    else:
        text = f"Generating a Fake user data."
    await msg.edit_text(text)
    infoText, userPic = await genFakeInfo(chkUrl)
    if infoText == "API Unreachable":
        return await msg.edit_text("API Unreachable at the Moment, Try again Later")
    if not (infoText or userPic):
        return await msg.edit_text(f"error generating fake data{f': gender ' if gender else ''} \nReport this at {SupportGroup}")
    await message.reply_document(userPic, caption=infoText)
    await msg.delete()
