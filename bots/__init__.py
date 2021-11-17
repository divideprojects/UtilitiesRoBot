from tgEasy import tgClient
from pyrogram import Client

SupportGroup = '@DivideProjectsDiscussion'

client = Client(
    "bots",
    api_id=1615152,
    api_hash="dc9a964e4f31331859dc7d4df007e8d5",
    bot_token="2126891045:AAETy6VIZSStCLbIuKd2TcLOs1qJVoR_Y9w",
    plugins={"root": "bots/modules"}
)
client.set_parse_mode("html")
app = tgClient(client)
