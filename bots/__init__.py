from pyrogram import Client
from tgEasy import tgClient

from bots.vars import Vars

MODULES = {}

client = Client(
    "bots",
    api_id=Vars.API_ID,
    api_hash=Vars.API_HASH,
    bot_token=Vars.BOT_TOKEN,
    plugins={"root": "bots/modules"},
)
client.set_parse_mode("html")
app = tgClient(client)
