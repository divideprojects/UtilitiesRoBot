from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck
from bots.utils.translator import translate

MODULES.update(
    {
        "translate": {
            "info": "To translate the text.",
            "usage": "/tr [optional: translate to language] [reply/text]",
        },
    },
)


@app.command("tr")
@joinCheck()
async def translate(_, message: Message):
    msg = await message.reply_text("....")
    if len(message.command) == 1:
        toLanguage = "en"
        if not message.reply_to_message:
            return await msg.edit_text(
                f"Usage: /{MODULES.get('translate').get('usage')}",
            )
        text = message.reply_to_message.text.markdown

    if len(message.command) == 2:
        toLanguage = message.command[1]
        if not message.reply_to_message:
            return await msg.edit(f"Usage: {MODULES.get('translate').get('usage')}")
        text = message.reply_to_message.text.markdown

    if len(message.command) == 3:
        toLanguage = message.command[1]
        text = message.command[2]

    await msg.edit_text(translate(text, toLanguage))
