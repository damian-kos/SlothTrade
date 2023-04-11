from discord.ext import commands
from embed.embed_message import embed_text_message
from instance.pymongo_operations import MongoDb
from .settings_methods import set_channel, define_item_properties, role_can


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_db = MongoDb()
        self.title = "Settings"
        self.description = (
            "Use the subcommands to change the settings for this server."
        )

    @commands.command(name="settings")
    async def settings(self, ctx):
        settings_options = {
            "sell_channel": set_channel,
            "search_channel": set_channel,
            "listing_channel": set_channel,
            "item_properties": define_item_properties,
            "can_sell": role_can,
            "can_remove": role_can,
            "can_search": role_can,
        }
        message = ctx.message.content.split(" ")
        if len(message) == 1:
            embed_fields = {
                "🗣️Listing Channel": "`/settings listing_channel`",
                "💰Sell Channel": "`/settings sell_channel`",
                "👀Search Channel": "`/settings search_channel`",
                "🗂️Item Properties": "`/settings item_properties`",
            }
            embed = embed_text_message(
                text="",
                title=self.title,
                description=self.description,
                fields=embed_fields,
            )
            await ctx.send(embed[0], embed=embed[1])
        elif len(message) == 2:
            await settings_options[message[1]](ctx, self.guild_db)
        else:
            await settings_options[message[1]](ctx, self.guild_db)


async def setup(bot):
    await bot.add_cog(Settings(bot))
