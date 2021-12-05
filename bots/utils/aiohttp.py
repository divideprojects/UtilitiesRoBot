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
from aiohttp import ClientSession


class AioHttp:
    @staticmethod
    async def get_json(link: str, **kwargs):
        async with ClientSession() as session:
            async with session.get(link, **kwargs) as resp:
                return await resp.json(), resp

    @staticmethod
    async def get_text(link: str, **kwargs):
        async with ClientSession() as session:
            async with session.get(link, **kwargs) as resp:
                return await resp.text(), resp

    @staticmethod
    async def get_raw(link: str, **kwargs):
        async with ClientSession() as session:
            async with session.get(link, **kwargs) as resp:
                return await resp.read(), resp

    @staticmethod
    async def post_json(link: str, data: dict, **kwargs):
        async with ClientSession() as session:
            async with session.post(link, json=data, **kwargs) as resp:
                return await resp.json(), resp
