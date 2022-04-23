from email.policy import default
from os import getcwd

from tgEasy.config import config


class Vars:
    SUPPORT_GROUP = config(
        "SUPPORT_GROUP", default="@DivideProjectsDiscussion")
    JOIN_CHANNEL = config("JOIN_CHANNEL", default="@DivideProjects")
    JOIN_CHECK = bool(config("JOIN_CHECK", default=None))
    BOT_TOKEN = config(
        "BOT_TOKEN", default="1612223289:AAFhYTXD1dQ7W7BMT7Qng88w6PPwCgeiQ74")
    API_ID = config("API_ID", default=1615152)
    API_HASH = config("API_HASH", default="dc9a964e4f31331859dc7d4df007e8d5")
    DOWN_PATH = f"{getcwd()}/bots/download"
    CAPTCHA_URL = config(
        "CAPTCHA_URL", default="https://hcaptcha.jayantkageri.in")
