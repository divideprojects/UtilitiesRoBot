from os import environ as env


def load_var(var_name: str, def_var=None):
    return env.get(var_name, def_var)


class Vars:
    """variables for bots and other functions."""

    # Bot Tokens
    BOT_TOKEN_PROXYBOT = load_var(
        "BOT_TOKEN_PROXYBOT",
        "1145082296:AAEg_LqK0XmHumgaLRTQgqejoChDLUi-IVc",
    )
    BOT_TOKEN_SHORTNER = load_var(
        "BOT_TOKEN_SHORTNER",
        "1463214430:AAGLy1VvRMVJs-uWKFj8SS2RgOBTe_3IHBQ",
    )
    BOT_TOKEN_TAGADMIN = load_var(
        "BOT_TOKEN_TAGADMIN",
        "1227603843:AAGCDHpH2mtvkoVvHSFJhUzTI6Bxxx-E0pw",
    )
    BOT_TOKEN_BINCHECKER = load_var(
        "BOT_TOKEN_BINCHECKER",
        "1486307956:AAFneK5q73pY916K1srUA9LJZGTcu4zQEaE",
    )
    BOT_TOKEN_INFOGEN = load_var(
        "BOT_TOKEN_INFOGEN",
        "1489878332:AAEe1cG0W_6Q1qGUC-CjLYAT5J7fo2qcGHQ",
    )
    BOT_TOKEN_TOOLSBOT = load_var(
        "BOT_TOKEN_TOOLSBOT",
        "1585810097:AAG7K3UkyAsI_Qa6WaEciIIoK8K9qfjNRJw",
    )
    BOT_TOKEN_SESSIONBOT = load_var(
        "BOT_TOKEN_SESSIONBOT",
        "1740985033:AAH4oL6_0ZfcGxysekXvHsZS3t5MS2Ut6Fo",
    )

    # Database
    DB_NAME = load_var("DB_NAME", "minibotspython")
    DB_URI = load_var(
        "DB_URI",
        "mongodb+srv://minibotspython:minibotspython@alitamain.itmz5.mongodb.net/minibotspython?retryWrites=true&w=majority",
    )

    # Common Things
    API_ID = int(load_var("API_ID", 1629442))
    API_HASH = load_var("API_HASH", "6d51f911b14837d4522be8f486841421")
    SUPPORT_CHANNEL = load_var("SUPPORT_CHANNEL", "DivideProjects")
    SUPPORT_GROUP = load_var("SUPPORT_GROUP", "DivideProjectsDiscussion")
    CMD_HANDLER = load_var("CMD_HANDLER", "/ !").split()
    PRIMARY_HANDLER = CMD_HANDLER[0]  # First item of cmd handler!
    MESSAGE_DUMP = int(load_var("MESSAGE_DUMP", -1001333593960))
    OWNER_ID = int(load_var("OWNER_ID", 1198820588))
    CONTACT_OWNER = load_var("CONTACT_OWNER" "DivideProjectsBot")
    SERVER_HOST = load_var("SERVER_HOST", "Azure")
    WORKERS = int(load_var("WORKERS", 32))
    DEV_USERS = [int(i) for i in load_var("DEV_USERS", "").split()]

    # Auth Group - CheckUser
    AUTH_GROUP_USERNAME = load_var("AUTH_GROUP_USERNAME", "DivideProjects")
    AUTH_GROUP = int(load_var("AUTH_GROUP", -1001218203939))

    # ShortLinkBot
    URLSHORTX_API = load_var(
        "URLSHORTX_API",
        "935440ad654afeb880f22342223a01734c439cfd",
    )
    SHORTNER_BLACKLIST = load_var("SHORTNER_BLACKLIST", "").split()
