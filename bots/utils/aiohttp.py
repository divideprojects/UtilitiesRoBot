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
