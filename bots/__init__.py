from os import getcwd

from pyrogram import Client
from tgEasy import tgClient
from tgEasy.config import config

SupportGroup = config("SupportGroup", default="@DivideProjectsDiscussion")
JoinChannel = config("JoinChannel", default="@DivideProjects")
JoinCheck = (
    True if config("JoinCheck", default=True).lower() in ("true", "yes") else False
)
BotToken = config("BotToken", default="2126891045:AAETy6VIZSStCLbIuKd2TcLOs1qJVoR_Y9w")
ApiId = config("ApiId", default=1615152)
ApiHash = config("ApiHash", default="dc9a964e4f31331859dc7d4df007e8d5")
OCR_SPACE_API_KEY = config("OCR_SPACE_API_KEY", default="")
DownPath = f"{getcwd()}/bots/download"

client = Client(
    "bots",
    api_id=ApiId,
    api_hash=ApiHash,
    bot_token=BotToken,
    plugins={"root": "bots/modules"},
)
client.set_parse_mode("html")
app = tgClient(client)
