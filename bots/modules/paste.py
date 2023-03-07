import contextlib
from os import remove

from aiohttp import ClientSession
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "paste": {
            "info": "To paste a text/file in pastebin.",
            "usage": "/paste [reply/text]",
        },
    },
)


@app.command("paste")
@joinCheck()
async def paste_bin(_, m: Message):  # sourcery skip: low-code-quality
    statusMsg = await m.reply_text(
        "Pasting to Spacebin, Please wait for a while...",
    )
    content = None
    sendAsFile = 0

    if m.reply_to_message:
        if m.reply_to_message.document:
            if m.reply_to_message.document.file_size > 400000:
                return await statusMsg.edit_text(
                    "Max file size that can be pasted is 400KB.",
                )
            uniqueId = f"paste_{str(m.chat.id).replace('-', '')}_{m.id}"
            file_ = await m.reply_to_message.download(uniqueId)
            with open(file_, "rb") as f:
                content = f.read().decode("UTF-8")
            remove(file_)

        elif m.reply_to_message.caption or m.reply_to_message.text:
            content = m.reply_to_message.caption or m.reply_to_message.text
            sendAsFile = 1

        else:
            with contextlib.suppress(BaseException):
                content = m.reply_to_message.text
                sendAsFile = 1

    if not content:
        return await statusMsg.edit_text(f"Usage: {MODULES.get('paste').get('usage')}")

    try:
        async with ClientSession() as session:
            async with session.post(
                "https://spaceb.in/api/v1/documents/",
                json={"content": content, "extension": "txt"},
                timeout=3,
            ) as response:
                key = (await response.json())["payload"].get("id")
                url = f"Spacebin Denied the Paste. \n{await response.json()}"
                if key:
                    url = f"https://spaceb.in/{key}"

    except Exception as e:
        return await statusMsg.edit_text(str(e))

    if sendAsFile:
        uniqueId = f"paste_{m.chat.id}_{m.id}.txt"
        with open(uniqueId, "w+") as file:
            file.write(content)
        await m.reply_document(uniqueId, caption=url)
        remove(uniqueId)
        return await statusMsg.delete()

    return await statusMsg.edit_text(url, disable_web_page_preview=True)
