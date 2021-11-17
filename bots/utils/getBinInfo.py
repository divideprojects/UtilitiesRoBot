from kantex.html import *

from .aiohttp import AioHttp


async def getBinInfo(gbin: str or int):
    lookup_url = f"https://lookup.binlist.net/{gbin}"
    rInfo = (await AioHttp.get_json(lookup_url))[0]
    if not rInfo:
        return "❌ Invalid Bin"
    try:
        info = str(Section(
            "✅ Valid Bin",
            str(Italic("Bin: ") + Code(gbin)),
            str(Italic("Type: ") + Code(rInfo["type"])),
            str(Italic("Brand: ") + Code(rInfo["brand"])),
            str(Italic("Country: ") +
                Code(rInfo["country"]["name"] + "(" + rInfo["country"]["alpha2"] + ")")),
            str(Italic("Bank: ") + Code(rInfo["bank"]["name"])),
        ))
    except (KeyError, TypeError):
        return "❌ Invalid Bin"
