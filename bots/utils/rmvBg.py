import random
import uuid

from removebg import RemoveBg

from bots.vars import Vars


async def rmvBg(imgPath):
    rmbg = RemoveBg(random.choice(Vars.RMVBG_API_KEY), "rmbg-error.log")
    uuid.uuid4()
    return rmbg.remove_background_from_img_file(imgPath)
