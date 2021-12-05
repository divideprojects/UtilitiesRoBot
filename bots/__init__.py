#
# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2021 Divide Projects <https://github.com/DivideProjects>
#
# This file is part of Utilities Robot.
#
# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.
#
from os import getcwd

from pyrogram import Client
from tgEasy import tgClient
from tgEasy.config import config

SupportGroup = config("SupportGroup", default="@DivideProjectsDiscussion")
JoinChannel = config("JoinChannel", default="@DivideProjects")
JoinCheck = config("JOIN_CHECK", default=None, cast=config.boolean)
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
