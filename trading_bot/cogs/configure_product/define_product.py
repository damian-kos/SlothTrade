from discord.ext import commands
from embed.embed_pagination import Pagination
from embed.embed_message import embed_message
from pathlib import Path
import discord
from instance.pymongo_operations import MongoDb


class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_db = MongoDb()
        self.title = "Trading Bot has been updated"
        self.description = "‣ You can configure me using: `/settings`"

    @commands.command(name="define")
    async def define(self, ctx):
        item = ctx.message.content.split("-")[1:]
        item = tuple(column.strip() for column in item)
        self.guild_db.define_item_properties(
            guild_id=ctx.guild.id,
            item_properties_tuple=item,
        )


async def setup(bot):
    await bot.add_cog(Define(bot))
