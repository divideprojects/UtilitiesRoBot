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

from kantex.html import Code, Italic, Section
from pypers.url_helpers import AioHttp


async def getBinInfo(gbin: str or int):
    lookup_url = f"https://lookup.binlist.net/{gbin}"
    rInfo = (await AioHttp.get_json(lookup_url))[0]
    if not rInfo:
        return "❌ Invalid Bin"
    try:
        info = str(
            Section(
                "✅ Valid Bin",
                str(Italic("Bin: ") + Code(gbin)),
                str(Italic("Type: ") + Code(rInfo["type"])),
                str(Italic("Brand: ") + Code(rInfo["brand"])),
                str(
                    Italic("Country: ")
                    + Code(
                        rInfo["country"]["name"]
                        + "("
                        + rInfo["country"]["alpha2"]
                        + ")",
                    ),
                ),
                str(Italic("Bank: ") + Code(rInfo["bank"]["name"])),
            ),
        )
    except (KeyError, TypeError):
        return "❌ Invalid Bin"
