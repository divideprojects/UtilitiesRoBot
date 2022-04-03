from os import getcwd

from tgEasy.config import config


class Vars:
    SUPPORT_GROUP = config(
        "SUPPORT_GROUP", default="@DivideProjectsDiscussion")
    JOIN_CHANNEL = config("JOIN_CHANNEL", default="@DivideProjects")
    JOIN_CHECK = config("JOIN_CHECK", default=None)
    BOT_TOKEN = config("BOT_TOKEN", default="")
    API_ID = config("API_ID", default=123456)
    API_HASH = config("API_HASH", default="")
    DOWN_PATH = f"{getcwd()}/bots/download"
