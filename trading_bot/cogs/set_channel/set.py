from discord.ext import commands
from embed.embed_pagination import Pagination
from embed.embed_message import embed_message
from pathlib import Path
import discord
from instance.pymongo_operations import MongoDb


class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_db = MongoDb()
        self.title = "Trading Bot has been updated"
        self.description = "‣ You can configure me using: `/settings`"

    @commands.command(name="set")
    async def set_channel(self, ctx):
        channel_to_set = ctx.message.content.split(" ")[-1]
        print(ctx.guild.id)
        print(ctx.channel.id)
        channel_types = ["sell", "search", "listing"]
        if channel_to_set in channel_types:
            self.guild_db.set_channel(
                guild_id=ctx.guild.id,
                channel_id=ctx.channel.id,
                channel_type=channel_to_set,
            )
            # await ctx.channel.send("Channel set ")


async def setup(bot):
    await bot.add_cog(Set(bot))
