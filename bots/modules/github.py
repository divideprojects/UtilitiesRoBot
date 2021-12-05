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
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.
#
from kantex.html import Bold, Code, Link, Section
from pyrogram.types import Message

from bots.utils.aiohttp import AioHttp

from bots import app
from bots.utils.joinCheck import joinCheck


@app.command("github", pm_only=True)
@joinCheck()
async def github(_, m: Message):
    args = m.text.split()

    if len(args) == 1:
        return await m.reply_text("Usage: /github <username>")

    elif len(args) == 2:
        rMsg = await m.reply_text("Fetching data...")
        username = args[1]
        url = f"https://api.github.com/users/{username}"
        result, resp = await AioHttp.get_json(url)
        if resp == 404:
            return await rMsg.edit_text(
                f"User {username} not found.",
                disable_web_page_preview=True,
            )

        url = result.get("html_url", None)
        name = result.get("name", None)
        company = result.get("company", None)
        bio = result.get("bio", None)
        created_at = result.get("created_at", "Not Found")

        reply_str = str(
            Section(
                f"{Bold('GitHub Info for')} {Code(username)}\n"
                f"{Bold('Name:')} {Code(name)}\n"
                f"{Bold('Username:')} {Code(username)}\n"
                f"{Bold('Bio:')} {Code(bio)}\n"
                f"{Bold('URL:')} {Code(url)}\n"
                f"{Bold('Company:')} {Code(company)}\n"
                f"{Bold('Created at:')} {Code(created_at)}",
            ),
        )

        if not result.get("repos_url", None):
            return await rMsg.edit_text(reply_str, disable_web_page_preview=True)

        result, resp = await AioHttp.get_json(result.get("repos_url", None))

        # if no repos found
        if resp.status == 404:
            return await rMsg.edit_text(reply_str, disable_web_page_preview=True)

        reply_str += str(Bold("\n\nRepositories:\n"))

        for i in range(len(result)):
            reply_str += (
                f"{Link(result[i].get('name', None),result[i].get('html_url', None))}\n"
            )

        return await rMsg.edit_text(reply_str, disable_web_page_preview=True)
