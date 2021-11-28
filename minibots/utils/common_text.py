from platform import python_version

from pyrogram import __version__

from minibots.utils.ikb import ikb
from minibots.vars import Vars


class Constants:
    """Constants used in various places in all bots."""

    back_help_start = [("Back", "help.callback.start")]
    start_kb = ikb(
        [
            [
                ("How to use?", "help.callback.help"),
                ("Help & Support", f"https://t.me/{Vars.SUPPORT_GROUP}", "url"),
            ],
        ],
    )

    DONATE_TEXT = f"""
Glad you'd like to donate!

You can donate my Owner by contacting him >>> @{Vars.CONTACT_OWNER} \
If you donate, the performance of all the bots will increase \
and it would also motivate my developer to maintain \
his hobbies such as building bots and other projects!

You can donate by these methods:
Bitcoin: `bc1qfvatfx5xkn6tysyldc7mz0zl88xfg4dzywa886`
"""
    about_me_text = f"""
<b>Creator:</b> <a href='tg://user?id={Vars.OWNER_ID}'>{{}}</a>
<b>Credits:</b> <a href='https://t.me/haskell'>Dan</a> for his pyrogram library, each and everyone who made this project possible!
<b>Made using:</b> <a href='https://python.org'>Python v{python_version()}</a>
<b>Library:</b> <a href='https://docs.pyrogram.org'>Pyrogram v{__version__}</a>
<b>Server:</b> <i>{Vars.SERVER_HOST}</i>

<b>Bot Username:</b> @{{}}
"""
