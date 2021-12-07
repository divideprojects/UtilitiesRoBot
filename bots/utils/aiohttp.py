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
