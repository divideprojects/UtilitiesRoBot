from html import escape
from re import compile as compilere
from re import sub


# HTML
async def cleanhtml(raw_html: str):
    cleanr = compilere("<.*?>")
    cleantext = sub(cleanr, "", raw_html)
    return cleantext


async def mention_html(name: str, user_id: int):
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'


# Markdown
async def escape_markdown(text: str):
    escape_chars = r"\*_`\["
    return sub(r"([%s])" % escape_chars, r"\\\1", text)


async def mention_markdown(name: str, user_id: int):
    return f"[{(await escape_markdown(name))}](tg://user?id={user_id})"
