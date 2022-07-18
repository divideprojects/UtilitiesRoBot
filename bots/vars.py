from os import getcwd

from tgEasy.config import config


class Vars:
    SUPPORT_GROUP = config(
        "SUPPORT_GROUP", default="@DivideProjectsDiscussion"
    )
    JOIN_CHANNEL = config("JOIN_CHANNEL", default="@DivideProjects")
    JOIN_CHECK = bool(config("JOIN_CHECK", default=False))
    BOT_TOKEN = config("BOT_TOKEN", default="")
    API_ID = config("API_ID", default=6)
    API_HASH = config("API_HASH", default="")
    DOWN_PATH = f"{getcwd()}/bots/download"
    DEVS = (
        config(
            "DEVS",
            default="1205330619 1198820588 1594433798 1705132727 1561622308",
        )
        .strip()
        .split(" ")
    )
    RMVBG_API_KEY = (
        config(
            "RMVBG_API_KEY",
            default="gvJj41pqvzk2DXFJuTriLJFw gXs1ND17zC9yAWixeoXVq5va gjgujBeCxf5xZ6fKuwnNHx6Z uanfq1YZQG5YYRK3k3KpJ3Pf ovs4EWPn7GXCokc6feRkiVR7 qxFU4o96resMGaHBT7r53sAN",
        )
        .strip()
        .split(" ")
    )
