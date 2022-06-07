# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2022 Divide Projects <https://github.com/DivideProjects>

# This file is part of Utilities Robot.

# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Utilities Robot.  If not, see <https://www.gnu.org/licenses/>.

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
    extension = "txt"
    sendAsFile = False
    fileToSend = None
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
            uniqueId = f"paste_{str(m.chat.id).replace('-', '')}_{m.id}"
            file_ = await m.reply_to_message.download(uniqueId)
            with open(file_, "rb") as f:
                content = f.read().decode("UTF-8")
            remove(file_)
        elif m.reply_to_message.audio:
            content = m.reply_to_message.caption
        elif m.reply_to_message.photo:
            content = m.reply_to_message.caption
        elif m.reply_to_message.video:
            content = m.reply_to_message.caption
        elif m.reply_to_message.voice:
            content = m.reply_to_message.caption
        else:
            with contextlib.suppress(BaseException):
                content = m.reply_to_message.text.markdown
                sendAsFile = True
    if not content:
        return await statusMsg.edit_text(f"Usage: {MODULES.get('paste').get('usage')}")
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
    if sendAsFile:
        with open(f"paste_{m.chat.id}_{m.id}.txt", "w+") as file:
            file.write(content)
            file.flush()
        await m.reply_document(f"paste_{m.chat.id}_{m.id}.txt", caption=url)
        remove(f"paste_{m.chat.id}_{m.id}.txt")
        return await statusMsg.delete()
    await statusMsg.edit_text(url, disable_web_page_preview=True)
