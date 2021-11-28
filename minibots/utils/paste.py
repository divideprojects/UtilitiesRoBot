from aiohttp import ClientSession


async def paste(content: str):
    NEKOBIN_URL = "https://nekobin.com/"
    async with ClientSession() as session:
        async with session.post(
            NEKOBIN_URL + "api/documents",
            json={"content": content},
        ) as response:
            if response.status == 201:
                response_json = await response.json()
                key = response_json["result"]["key"]
                final_url = f"{NEKOBIN_URL}{key}.txt"
                raw = f"{NEKOBIN_URL}raw/{key}.txt"
            else:
                raise Exception("Error Pasting to Nekobin")

    return final_url, raw
