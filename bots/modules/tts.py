from os import remove

from gtts import gTTS
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars

MODULES.update(
    {
        "text-to-speech": {
            "info": "To convert a text to audio.",
            "usage": "/tts [reply/text]",
        },
    },
)


@app.command("tts")
@joinCheck()
async def tts(_, m: Message):
    if m.reply_to_message and m.reply_to_message.text:
        text_to_convert = m.reply_to_message.text
    elif len(m.command) > 1:
        text_to_convert = m.text.split(" ", 1)[1]
    else:
        await m.reply_text(
            f"Usage: {MODULES.get('text-to-speech').get('usage')}",
        )
        return

    save_file_name = f"{Vars.DOWN_PATH}/tts_{m.from_user.id}_{m.id}.mp3"
    rmsg = await m.reply_text("Converting Text to Speech...")
    if "|" in text_to_convert:
        text_split = text_to_convert.split("|")
        text = text_split[0].strip()
        lang = text_split[1].strip()
    else:
        text = text_to_convert
        lang = "en"

    stts = gTTS(text=text, lang=lang)
    stts.save(save_file_name)
    await m.reply_audio(save_file_name, caption="Text converted to Audio.")

    # Remove the files and msg
    remove(save_file_name)
    await rmsg.delete()
