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
    DEVS = (
        config(
            "DEVS",
            default="1205330619 1198820588 1594433798 1705132727 1561622308 5051444449 1689421763",
        )
        .strip()
        .split(" ")
    )
