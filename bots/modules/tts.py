from os import remove

from gtts import gTTS
from pyrogram.types import Message

from bots import app
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars


@app.command("tts", pm_only=True)
@joinCheck()
async def tts(_, m: Message):
    if m.reply_to_message and m.reply_to_message.text:
        save_file_name = f"{Vars.DOWN_PATH}/tts_{m.from_user.id}_{m.message_id}.mp3"
        rmsg = await m.reply_text("Converting Text to Speech...")
        text_to_convert = m.reply_to_message.text
        if "|" in text_to_convert:
            text_split = text_to_convert.split("|")
            text = text_split[0].strip()
            lang = text_split[1].strip()
        else:
            text = text_to_convert
            lang = "en"

        tts = gTTS(text=text, lang=lang)
        tts.save(save_file_name)
        await m.reply_audio(save_file_name, caption="Text converted to Audio.")

        # Remove the files and msg
        remove(save_file_name)
        return await rmsg.delete()
    return await m.reply_text("Reply to a text message.")
