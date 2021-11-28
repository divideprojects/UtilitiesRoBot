from asyncio import get_event_loop, set_event_loop_policy

import pyromod.listen  # skipcq:PYL-W0611
from pyrogram import idle

# Import bot scripts
from minibots.bots import bot_list
from minibots.logger import LOGGER
from minibots.vars import Vars


# Function to start all bots
async def startBots():
    """Function to start the bots."""
    LOGGER.info("Starting All Bots...!")
    for bot in bot_list:
        await bot.start()
        await bot.send_message(Vars.MESSAGE_DUMP, "Bot Started!")
        LOGGER.info(f"Started {(await bot.get_me()).username}")
    LOGGER.info("Started all bots!")
    LOGGER.info("Idililing all instances...")
    await idle()


# Set loop
loop = get_event_loop()

# Run bots
if __name__ == "__main__":
    loop.run_until_complete(startBots())
    LOGGER.info("Bots Started!!")
