from io import BytesIO

from kantex.html import Bold, Italic
from proxygrab import get_proxy
from pyrogram.types import CallbackQuery, Message
from tgEasy import array_chunk, ikb

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars

MODULES.update(
    {
        "proxy": {
            "info": "To generate available proxies.",
            "usage": "/proxy",
        },
    },
)

proxytypes = ("HTTP", "HTTPS", "Socks4", "Socks5")


@app.command("proxy", pm_only=True)
@joinCheck()
async def getProxy(_, m: Message):
    msg = await m.reply_text("...", quote=True)
    await msg.edit_text(
        "Choose the Proxy Type you Want.",
        reply_markup=ikb(await gen_proxy_kb()),
    )


@app.callback("getProxy")
async def getProxy(c, cb: CallbackQuery):
    ptype = cb.data.split(".")[1].lower()
    await cb.message.edit_text(f"Fetching {ptype} Proxies...")
    proxies_source = await get_proxy(ptype)
    proxies_fetched = "\n".join(proxies_source)
    caption = str(
        Bold(Italic(f"Proxies scrapped by:"))
        + f"@{(await c.get_me()).username}\n\n{Vars.JOIN_CHANNEL}",
    )
    with BytesIO(str.encode(proxies_fetched)) as output:
        output.name = f"{ptype}_{(await c.get_me()).username}.txt"
        await cb.message.reply_document(document=output, caption=caption)
    await cb.message.delete()
    await cb.answer("Done ✅")


async def gen_proxy_kb():
    cmds = [i for i in proxytypes]
    kb = [(cmd, f"getProxy.{cmd}") for cmd in cmds]
    return array_chunk(kb, 2)
