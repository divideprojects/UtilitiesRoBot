from os import getcwd

from tgEasy.config import config


class Vars:
    SUPPORT_GROUP = config("SUPPORT_GROUP", default="@DivideProjectsDiscussion")
    JOIN_CHANNEL = config("JOIN_CHANNEL", default="@DivideProjects")
    JOIN_CHECK = bool(config("JOIN_CHECK", default=False))
    BOT_TOKEN = config("BOT_TOKEN", default="")
    API_ID = config("API_ID", default=6)
    API_HASH = config("API_HASH", default="")
    DOWN_PATH = f"{getcwd()}/bots/download"
    CAPTCHA_URL = config("CAPTCHA_URL", default="https://hcaptcha.jayantkageri.in")
    DEVS = (
        config(
            "DEVS",
            default="1205330619 1198820588 1594433798 1705132727 1561622308 5051444449 1689421763",
        )
        .strip()
        .split(" ")
    )
