from pyrogram.types import Message

from .. import SupportGroup, app
from ..utils.genFakeInfo import genFakeInfo


@app.command("geninfo", pm_only=True)
async def genInfo(_, m: Message):
    gender = None
    msg = await m.reply_text("...")
    chkUrl = "https://randomuser.me/api/1.3/"
    if len(m.command) < 0:
        if m.command[1] in ("male", "female"):
            gender = m.command[1]
            chkUrl += f"?gender={gender}"
            text = f"Generating a Fake {m.command[1]} user data."
        else:
            text = f"Generating a Fake user data."
    else:
        text = f"Generating a Fake user data."
    await msg.edit_text(text)
    infoText, userPic = await genFakeInfo(chkUrl)
    if infoText == "API Unreachable":
        return await msg.edit_text("API Unreachable at the Moment, Try again Later")
    if not (infoText or userPic):
        return await msg.edit_text(
            f"error generating fake data{f': gender ' if gender else ''} \nReport this at {SupportGroup}",
        )
    await m.reply_document(userPic, caption=infoText)
    await msg.delete()
