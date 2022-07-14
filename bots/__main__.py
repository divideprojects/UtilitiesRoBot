import asyncio

from pyrogram import idle

from bots import app, MODULES

if __name__ == "__main__":
    async def main():
        await app.__client__.start()
        for i in MODULES.keys():
            print(f"{i} has been loaded.")
        print(
            f"\n@{(await app.__client__.get_me()).username}", "has been started."
        )
        await idle()

    app.__client__.run(main())
