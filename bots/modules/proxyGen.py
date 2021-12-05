#
# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2021 Divide Projects <https://github.com/DivideProjects>
#
# This file is part of Utilities Robot.
#
# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.#
from io import BytesIO

from proxygrab import get_proxy
from pyrogram.types import CallbackQuery, Message
from tgEasy import array_chunk, ikb

from bots import JoinChannel, app
from bots.utils.joinCheck import joinCheck

proxytypes = {"HTTP", "HTTPS", "Socks4", "Socks5"}


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
    caption = f"<b><i>Proxies scrapped by:</i></b> @{(await c.get_me()).username}\n\n{JoinChannel}"
    with BytesIO(str.encode(proxies_fetched)) as output:
        output.name = f"{ptype}_{(await c.get_me()).username}.txt"
        await cb.message.reply_document(document=output, caption=caption)
    await cb.message.delete()
    await cb.answer("Done ✅")


async def gen_proxy_kb():
    cmds = [i for i in proxytypes]
    kb = [(cmd, f"getProxy.{cmd}") for cmd in cmds]
    return array_chunk(kb, 2)
