from asyncio.exceptions import TimeoutError as te
from contextlib import suppress
from gc import collect

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidURI, OperationFailure
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from redis import Redis
from redis.exceptions import ConnectionError as RConnectionError
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import close_all_sessions, scoped_session, sessionmaker

from bots import MODULES, app

MODULES.update(
    {
        "dbUrlMaker": {
            "info": "Make an URI for a database.",
            "usage": "/dburl",
        }
    }
)


@app.command("dburl")
async def dburl(_: app.__client__, m: Message):
    with suppress(RPCError):
        return await m.reply_text(
            "Select the database for which you want to make URL",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "MongoDB",
                            callback_data="call_mongo",
                        ),
                        InlineKeyboardButton(
                            "RedisDB",
                            callback_data="call_redis",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "PSQL",
                            callback_data="call_psql",
                        ),
                    ],
                ],
            ),
        )


@app.callback("call_")
async def callbacka(c: app.__client__, q: CallbackQuery):
    with suppress(RPCError):
        chat_id = q.message.chat.id
        await q.edit_message_text(
            "Ok, now send the parameters as asked!\nSend /cancel to cancel the process.\nEach asking will wait till 5 mins!",
        )
        passw = {"text": "", "mid": 0}
        if q.data == "call_redis":
            try:
                resp = await c.ask(
                    chat_id,
                    "Send me the redis db password.",
                    timeout=300,
                )
                while 1:
                    if not resp.text:
                        await resp.reply_text("No password received!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    if resp.text and resp.text.lower().startswith("/cancel"):
                        await resp.reply_text("Canceled!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    passw["text"], passw["mid"] = resp.text, resp.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not passw["mid"]:
                return
            endp = {"text": "", "mid": 0}
            try:
                endpr = await c.ask(
                    chat_id,
                    "Send me the redis db endpoint.",
                    timeout=300,
                )
                while 1:
                    if not endpr.text:
                        await endpr.reply_text("No endpoint received!")
                        endp["text"], endp["mid"] = "", 0
                        break
                    if endpr.text and endpr.text.lower().startswith("/cancel"):
                        await endpr.reply_text("Canceled!")
                        endp["text"], endp["mid"] = "", 0
                        break
                    endp["text"], endp["mid"] = endpr.text, endpr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not endp["mid"]:
                return
            isdef = {"text": "", "mid": 0}
            isde = 0
            try:
                isdefr = await c.ask(
                    chat_id,
                    "Is the user is default?\nReply with yes (for default) or the user name.",
                    timeout=300,
                )
                while 1:
                    if not isdefr.text:
                        await isdefr.reply_text(
                            "No user received!\nDefault will be used!", )
                        isde = 1
                        isdef["text"], isdef["mid"] = "", isdefr.id
                        break
                    if isdefr.text.lower().startswith("/cancel"):
                        await isdefr.reply_text("Canceled!")
                        isdef["text"], isdef["mid"] = "", 0
                        break
                    if isdefr.text.lower().startswith("yes"):
                        isdef["text"], isdef["mid"] = "", isdefr.id
                        break
                    isdef["text"], isdef["mid"] = isdefr.text, isdefr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not isdef["mid"]:
                return
            send = await q.message.reply_text(
                "Creating and verifying the url safely!")
            furl = f"redis://{isdef['text'] if isde else 'default'}:{passw['text']}@{endp['text']}"
            try:
                ur = Redis.from_url(furl)
                ur.ping()
                ur.close()
                ur.connection_pool.disconnect()
            except (ValueError, RConnectionError) as p:
                await send.edit_text(f"Error: {p}")
                return
        elif q.data == "call_psql":
            try:
                resp = await c.ask(
                    chat_id,
                    "Send me the psql db password.",
                    timeout=300,
                )
                while 1:
                    if not resp.text:
                        await resp.reply_text("No password received!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    if resp.text and resp.text.lower().startswith("/cancel"):
                        await resp.reply_text("Canceled!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    passw["text"], passw["mid"] = resp.text, resp.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not passw["mid"]:
                return
            hostt = {"text": "", "mid": 0}
            try:
                endpr = await c.ask(
                    chat_id,
                    "Send me the psql db host.",
                    timeout=300,
                )
                while 1:
                    if not endpr.text:
                        await endpr.reply_text("No host received!")
                        hostt["text"], hostt["mid"] = "", 0
                        break
                    if endpr.text and endpr.text.lower().startswith("/cancel"):
                        await endpr.reply_text("Canceled!")
                        hostt["text"], hostt["mid"] = "", 0
                        break
                    hostt["text"], hostt["mid"] = endpr.text, endpr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not hostt["mid"]:
                return
            portt = {"text": "", "mid": 0}
            try:
                isdefr = await c.ask(
                    chat_id,
                    "Now send me the port of the psql.",
                    timeout=300,
                )
                while 1:
                    if not isdefr.text:
                        await isdefr.reply_text("Got no port!", )
                        portt["text"], portt["mid"] = "", 0
                        break
                    if isdefr.text.lower().startswith("/cancel"):
                        await isdefr.reply_text("Canceled!")
                        portt["text"], portt["mid"] = "", 0
                        break
                    portt["text"], portt["mid"] = isdefr.text, isdefr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not portt["mid"]:
                return
            dbb = {"text": "", "mid": 0}
            try:
                isdefr = await c.ask(
                    chat_id,
                    "Ok now send me the database name.",
                    timeout=300,
                )
                while 1:
                    if not isdefr.text:
                        await isdefr.reply_text("Got no name.", )
                        dbb["text"], dbb["mid"] = "", 0
                        break
                    if isdefr.text.lower().startswith("/cancel"):
                        await isdefr.reply_text("Canceled!")
                        dbb["text"], dbb["mid"] = "", 0
                        break
                    dbb["text"], dbb["mid"] = isdefr.text, isdefr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not dbb["mid"]:
                return
            udb = {"text": "", "mid": 0}
            try:
                isdefr = await c.ask(
                    chat_id,
                    "Ok now send me the user name.",
                    timeout=300,
                )
                while 1:
                    if not isdefr.text:
                        await isdefr.reply_text("Got no name.", )
                        udb["text"], udb["mid"] = "", 0
                        break
                    if isdefr.text.lower().startswith("/cancel"):
                        await endpr.reply_text("Canceled!")
                        udb["text"], udb["mid"] = "", 0
                        break
                    udb["text"], udb["mid"] = isdefr.text, isdefr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not udb["mid"]:
                return
            send = await q.message.reply_text(
                "Creating and verifying the url safely!")
            furl = f"postgresql://{udb['text']}:{passw['text']}@{hostt['text']}:{portt['text']}/{dbb['text']}"
            try:
                engine = create_engine(furl)
                BASE = declarative_base()
                BASE.metadata.bind = engine
                BASE.metadata.create_all(engine)
                ur = scoped_session(sessionmaker(bind=engine))
                ur.close()
                ur.remove()
                close_all_sessions()
            except (ValueError, SQLAlchemyError) as p:
                await send.edit_text(f"Error: {p}")
                return
        else:
            try:
                resp = await c.ask(
                    chat_id,
                    "Send me the mongo db created cluster password.",
                    timeout=300,
                )
                while 1:
                    if not resp.text:
                        await resp.reply_text("No password received!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    if resp.text and resp.text.lower().startswith("/cancel"):
                        await resp.reply_text("Canceled!")
                        passw["text"], passw["mid"] = "", 0
                        break
                    passw["text"], passw["mid"] = resp.text, resp.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not passw["mid"]:
                return
            endp = {"text": "", "mid": 0}
            try:
                endpr = await c.ask(
                    chat_id,
                    "Send me the raw mongo db url that you have copied; for python3 version less than 3.11.",
                    timeout=300,
                )
                while 1:
                    if not endpr.text:
                        await endpr.reply_text("No raw db url received!")
                        endp["text"], endp["mid"] = "", 0
                        break
                    if endpr.text.lower().startswith("/cancel"):
                        await endpr.reply_text("Canceled!")
                        endp["text"], endp["mid"] = "", 0
                        break
                    if "<password>" not in endpr.text.lower():
                        await endpr.reply_text("Mal formatted url received!")
                        endp["text"], endp["mid"] = "", 0
                        break
                    endp["text"], endp["mid"] = endpr.text, endpr.id
                    break
            except te:
                await q.message.reply_text("Process exited automatically!")
                return
            if not endp["mid"]:
                return
            send = await q.message.reply_text(
                "Creating and verifying the url safely!")
            furl = endp["text"].replace("<password>", passw["text"])
            try:
                ur = MongoClient(furl)
                ur.admin.command("ping")
                ur.close()
            except (OperationFailure, InvalidURI, ConnectionFailure) as p:
                await send.edit_text(f"Error: {p}")
                return
        await send.edit_text(f"Success: <code>{furl}</code>",
                             parse_mode=ParseMode.HTML)
    collect()
    return
