import traceback

import requests
from cachetools import TTLCache
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bots import client as app
from bots.vars import Vars

CACHE = TTLCache(maxsize=250, ttl=30)


def hcaptcha(**args):
    def wrapper(func):
        async def decorator(c: Client, m: Message):
            username = (await c.get_me()).username.replace("@", "")
            id = str(m.chat.id) + "_" + str(m.id)

            CACHE[id] = (
                m,
                func,
            )

            return await m.reply_text(
                "Solve the hCaptcha to Continue",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                url=f"{Vars.CAPTCHA_URL}/?id={id}&username={username}&redirect=false",
                                text="Goto hCaptcha",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="Check",
                                callback_data=f"hcaptcha_{id}",
                            ),
                        ],
                    ],
                ),
            )

        return decorator

    return wrapper


@app.on_callback_query(filters.regex("^hcaptcha"))
async def hcaptcha_callback(c: Client, query: CallbackQuery):
    id = query.data.split("_", maxsplit=1)[1]
    req = requests.get(f"{Vars.CAPTCHA_URL}/api/info?id={id}").json()
    if not req["success"]:
        return await query.answer("Please Solve the Captcha", show_alert=True)
    try:
        data = CACHE.pop(id)
        await query.message.delete()
        return await data[1](c, data[0])
    except Exception as e:
        print(traceback.format_exc())
        await query.answer(str(e), show_alert=True)
