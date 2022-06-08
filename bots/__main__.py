import asyncio

from pyrogram import idle

from bots import app

if __name__ == "__main__":

    async def main():
        await app.__client__.start()
        print(f"@{(await app.__client__.get_me()).username}", "has been started.")
        await idle()

    asyncio.run(main())
