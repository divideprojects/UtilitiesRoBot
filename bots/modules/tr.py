from kantex.html import Section

from bots import app
from bots.utils.joinCheck import joinCheck
from bots.utils.translator import translate


@app.command("tr")
@joinCheck()
async def translate(client, message):
    usage = str(
        Section(
            "Usage",
            "/tr - <toLanguage (optional) (default: en)> <text/reply to message>",
        ),
    )
    msg = await message.reply_text("....")
    if len(message.command) == 0:
        toLanguage = "en"
        if not message.reply_to_message:
            return msg.edit_text(usage)
        text = message.reply_to_message.text.markdown

    if len(message.command) == 1:
        toLanguage = message.command[1]
        if not message.reply_to_message:
            return msg.edit(usage)
        text = message.reply_to_message.text.markdown

    if len(message.command) == 2:
        toLanguage = message.command[1]
        text = message.command[2]

    await msg.edit_text(translate(text, toLanguage))
