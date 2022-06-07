# Utilities Robot - All in one Utilities Bot of Telegram
# Copyright (C) 2022 Divide Projects <https://github.com/DivideProjects>

# This file is part of Utilities Robot.

# Utilities Robot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Utilities Robot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Utilities Robot.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import Client
from pyrogram.enums import ParseMode
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
client.set_parse_mode(ParseMode.HTML)
app = tgClient(client)
