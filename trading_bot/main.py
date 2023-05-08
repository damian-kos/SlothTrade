from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import discord
import os
import tracemalloc

tracemalloc.start()
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


async def main():
    async with bot:
        # Load custom extensions for the bot
        await bot.load_extension("cogs.inventory.remove.remove_command")
        await bot.load_extension("cogs.search.search_command")
        await bot.load_extension("cogs.join_guild.join")
        await bot.load_extension("webhook.logging_webhook")
        await bot.load_extension("cogs.settings.settings")
        await bot.load_extension("cogs.test.test")
        await bot.start(TOKEN)


asyncio.run(main())
