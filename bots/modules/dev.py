# Thanks to @SpEcHiDe/TerminalBot

import asyncio
import io
import os
import sys
import traceback

from kantex.html import Bold, Code
from pyrogram.types import Message

from bots import app
from bots.vars import Vars


@app.command("eval")
async def eval(client, message: Message):
    if not (await authorised(message)):
        return

    msg = await message.reply_text("...")
    if len(message.command) == 1:
        return await msg.edit_text(f"Usage: {Code('/eval [python code]')}")

    cmd = message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"{Bold('EVAL')}: {Code(cmd)}\n\n{Bold('OUTPUT')}:\n{Code(evaluation.strip())} \n"

    if len(final_output) > 4096:
        with open(f"eval_{message.id}.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await msg.reply_document(
            document=f"eval_{message.id}txt", caption=cmd, disable_notification=True
        )
        os.remove(f"eval_{message.id}.txt")
        await msg.delete()
    else:
        await msg.edit(final_output)


@app.command("exec")
async def shell(_, m: Message):
    if not (await authorised(m)):
        return
    msg = await m.reply_text("...")
    if len(m.command) == 1:
        return await msg.edit_text(f"Usage: {Code('/exec [shell command]')}")
    cmd = m.text.split(" ", maxsplit=1)[1]
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.path.abspath("."),
    )

    output = f"{Bold('COMMAND')}: {Code(cmd)}\n\n{Bold('OUTPUT')}: {Code((await process.communicate())[0].decode('utf-8'))}"

    if len(output) > 4096:
        with open(f"exec_{m.id}.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(output))
        await msg.reply_document(
            document=f"exec_{m.id}.txt", caption=cmd, disable_notification=True
        )
        os.remove(f"exec_{m.id}.txt")
        await msg.delete()
    else:
        await msg.edit(output)


async def aexec(code, client, message):
    exec(
        (
            "async def __aexec(client, message): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )

    return await locals()["__aexec"](client, message)


async def authorised(m: Message):
    return str(m.from_user.id) in Vars.DEVS
