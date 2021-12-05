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
from datetime import datetime

from kantex.html import Code, Section, SubSection

from .aiohttp import AioHttp


async def genFakeInfo(chkUrl: str):
    rData, resp = await AioHttp.get_json(chkUrl)
    if not resp.status == 200:
        return "API Unreachable", None

    user = rData["results"][0]

    dobTime = datetime.strptime(user["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    userPic = user["picture"]["large"]

    infoText = str(
        Section(
            "Fake User Information",
            str(f"Name: {Code(user['name']['title'])}"),
            str(f"Gender: {Code(user['gender'])}"),
            SubSection(
                "Location",
                str(
                    f"Street: {Code(user['location']['street']['number'])}, {user['location']['street']['name']}",
                ),
                str(f"City: {Code(user['location']['city'])}"),
                str(f"State: {Code(user['location']['state'])}"),
                str(f"Country: {Code(user['location']['country'])}"),
                str(f"Postcode: {Code(user['location']['postcode'])}"),
            ),
            str(f"Email: {Code(user['email'])}"),
            str(f"Date of Birth: {Code(dobTime.strftime('%B %m, %Y'))}"),
            str(f"Age: {Code(user['dob']['age'])}"),
            str(f"Cellphone: {Code(user['cell'])}"),
            str(f"Phone: {Code(user['phone'])}"),
        ),
    )
    return infoText, userPic
