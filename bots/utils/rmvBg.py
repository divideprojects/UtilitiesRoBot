import random
from removebg import RemoveBg
from bots.vars import Vars
import uuid


async def rmvBg(imgPath):
    rmbg = RemoveBg(random.choice(Vars.RMVBG_API_KEY), "rmbg-error.log")
    new_file_name = uuid.uuid4()
    return rmbg.remove_background_from_img_file(imgPath)
