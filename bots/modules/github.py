from kantex.html import Bold, Code, Link, Section
from pypers.url_helpers import AioHttp
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "github": {
            "info": "To get the GitHub user info.",
            "usage": "/github [username]",
        },
    },
)


@app.command("github")
@joinCheck()
async def github(_, m: Message):
    args = m.text.split()

    if len(args) == 1:
        await m.reply_text(f"Usage: {MODULES.get('github').get('usage')}")
        return
    if len(args) == 2:
        rMsg = await m.reply_text("Fetching data...")
        username = args[1]
        url = f"https://api.github.com/users/{username}"
        result, resp = await AioHttp.get_json(url)
        if resp == 404:
            await rMsg.edit_text(
                f"User {username} not found.",
                disable_web_page_preview=True,
            )
            return
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
            await rMsg.edit_text(reply_str, disable_web_page_preview=True)
            return
        result, resp = await AioHttp.get_json(result.get("repos_url", None))

        # if no repos found
        if resp.status == 404:
            await rMsg.edit_text(reply_str, disable_web_page_preview=True)
            return
        reply_str += str(Bold("\n\nRepositories:\n\n"))

        for i in range(len(result)):
            reply_str += f"{Link(result[i].get('name', None),result[i].get('html_url', None))}\n"

        await rMsg.edit_text(reply_str, disable_web_page_preview=True)
        return
