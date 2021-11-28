from re import compile as compile_re
from re import escape, search
from shlex import split
from typing import List

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.filters import create
from pyrogram.types import Message

from minibots.logger import LOGGER
from minibots.utils.ikb import ikb
from minibots.vars import Vars

DEV_LEVEL = set(Vars.DEV_USERS + [int(Vars.OWNER_ID)])

# -- Constants --  #
def keyboard_no_join(iurl):
    return ikb([[("Join Channel", iurl, "url")]])


NO_JOIN_START_TEXT = """
You must be a member of the Channel to use the bot, \
this step ensure that you know about bot status \
and latest updates.
This step is also taken to prevent misuse of bot as \
all users will be logged.
"""
# -- Constants --  #


def command(
    commands: str or List[str],
    prefixes: str or List[str] = Vars.CMD_HANDLER,
    case_sensitive: bool = False,
    BOT_USERNAME: str = "",
):
    async def func(flt, _, m: Message):

        if not m.from_user:
            return False

        text: str = m.text or m.caption
        m.command = None
        if not text:
            return False
        regex = "^({prefix})+\\b({regex})\\b(\\b@{bot_name}\\b)?(.*)".format(
            prefix="|".join(escape(x) for x in flt.prefixes),
            regex="|".join(flt.commands),
            bot_name=BOT_USERNAME,
        )

        matches = search(compile_re(regex), text)
        if matches:
            m.command = [matches.group(2)]
            for arg in split(matches.group(4).strip()):
                m.command.append(arg)
            return True
        return False

    commands = commands if type(commands) is list else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}
    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if type(prefixes) is list else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}
    return create(
        func,
        "NormalCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
    )


def dev_command(
    commands: str or List[str],
    prefixes: str or List[str] = Vars.CMD_HANDLER,
    case_sensitive: bool = False,
    BOT_USERNAME: str = "",
):
    async def func(flt, _, m: Message):

        if not m.from_user:
            return False

        # Only devs allowed to use this...!
        if m.from_user.id not in DEV_LEVEL:
            return False

        text: str = m.text or m.caption
        m.command = None
        if not text:
            return False
        regex = "^({prefix})+\\b({regex})\\b(\\b@{bot_name}\\b)?(.*)".format(
            prefix="|".join(escape(x) for x in flt.prefixes),
            regex="|".join(flt.commands),
            bot_name=BOT_USERNAME,
        )

        matches = search(compile_re(regex), text)
        if matches:
            m.command = [matches.group(2)]
            for arg in split(matches.group(4).strip()):
                m.command.append(arg)
            return True
        return False

    commands = commands if type(commands) is list else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}
    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if type(prefixes) is list else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}
    return create(
        func,
        "DevCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
    )


async def user_check_filter(_, c: Client, m: Message):
    user_id = m.from_user.id

    # if user is dev or owner, return true
    if user_id in DEV_LEVEL:
        LOGGER.info("Dev User detected, skipping check")
        return True

    try:
        user_member = await c.get_chat_member(int(Vars.AUTH_GROUP), user_id)
        if user_member:
            LOGGER.info(f"User {user_id} already a member of chat, passing check!")
            return True

    except UserNotParticipant:
        i_url = await c.export_chat_invite_link(int(Vars.AUTH_GROUP))
        await m.reply_text(
            NO_JOIN_START_TEXT,
            disable_web_page_preview=True,
            parse_mode="markdown",
            reply_markup=keyboard_no_join(i_url),
        )
        return False

    except Exception as ef:
        LOGGER.error(ef)
        return False


user_check = filters.create(user_check_filter)
