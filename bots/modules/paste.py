from os import remove

from aiohttp import ClientSession
from pyrogram.types import Message

from .. import app
from ..utils.joinCheck import joinCheck


@app.command("paste")
@joinCheck()
async def paste_bin(_, m: Message):
    statusMsg = await m.reply_text(
        "Pasting to Spacebin, Please wait for a while...",
    )
    content = None
    extension = "txt"
    if len(m.command) > 1:
        # TODO: Make a way to get the extension
        if m.command[1].startswith("py"):
            extension = "python"
        if m.command[1].startswith("js"):
            extension = "javascript"
        if m.command[1].startswith("ts") or m.command[1].startswith(
            "typescript",
        ):
            extension = "typescript"
        if m.command[1].startswith("go"):
            extension = "go"
        if m.command[1].startswith("java"):
            extension = "java"
        if m.command[1].startswith("crystal") or m.command[1].startswith(
            "cr",
        ):
            extension = "crystal"
        if m.command[1].startswith("c") or m.command[1].startswith("objc"):
            extension = "c"
        if (
            m.command[1].startswith("json")
            or m.command[1].startswith("yaml")
            or m.command[1].startswith("toml")
        ):
            extension = "json"
        if m.command[1].startswith("markdown") or m.command[1].startswith(
            "md",
        ):
            extension = "markdown"
        if (
            m.command[1].startswith("html")
            or m.command[1].startswith("css")
            or m.command[1].startswith("xml")
        ):
            extension = "markup"
        if m.command[1].startswith("css"):
            extension = "css"
        if m.command[1].startswith("bash") or m.command[1].startswith("sh"):
            extension = "bash"
        if m.command[1].startswith("rust") or m.command[1].startswith("rs"):
            extension = "rust"
        if m.command[1].startswith("ruby") or m.command[1].startswith("rb"):
            extension = "ruby"
        if m.command[1].startswith("php"):
            extension = "php"

    if m.reply_to_message:
        if m.reply_to_message.document:
            if m.reply_to_message.document.file_size > 400000:
                return await statusMsg.edit_text(
                    "Max file size that can be pasted is 400KB.",
                )
            uniqueId = f"paste_{str(m.chat.id).replace('-', '')}_{m.message_id}"
            file_ = await m.reply_to_message.download(uniqueId)
            with open(file_, "rb") as f:
                content = f.read().decode("UTF-8")
            remove(file_)
        else:
            try:
                content = m.reply_to_message.text.markdown
            except:
                pass

    if not content:
        return await statusMsg.edit_text("Reply to a Text or Document to Paste.")
    try:
        async with ClientSession() as session:
            async with session.post(
                "https://spaceb.in/api/v1/documents/",
                json={"content": content, "extension": extension},
                timeout=3,
            ) as response:
                key = (await response.json())["payload"].get("id")
                url = f"Spacebin Denied the Paste. \n{await response.json()}"
                if key:
                    url = f"https://spaceb.in/{key}"
    except Exception as e:
        return await statusMsg.edit_text(str(e))
    await statusMsg.edit_text(url, disable_web_page_preview=True)
