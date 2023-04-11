from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import discord
import os
from pathlib import Path


load_dotenv()

# "DISCORD-TOKEN" imported from .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.all()
# message_content needs to be turned on on dev portal.
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

import logging
import sys

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


async def main():
    async with bot:
        # Load custom extensions for the bot
        await bot.load_extension("cogs.inventory.sell_command")
        await bot.load_extension("cogs.inventory.delete_command")
        await bot.load_extension("cogs.search.search_command")
        await bot.load_extension("cogs.join_guild.join")
        await bot.load_extension("cogs.settings.settings")

        # Start the bot with the specified token
        await bot.start(TOKEN)


# Run the main coroutine with asyncio
asyncio.run(main())
