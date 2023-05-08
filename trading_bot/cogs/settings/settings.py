from discord.ext import commands
from embed.embed_message import embed_text_message
from instance.pymongo_operations import MongoDb
from .settings_methods import channel_settings, define_item_properties, role_can


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDb()
        self.title = "Settings"
        self.description = (
            "Use the subcommands to change the settings for this server."
        )

    @commands.command(name="settings")
    async def settings(self, ctx):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("You need to have `Manage Server` permission.")
            return
        guild = self.db.guild_in_database(guild_id=ctx.guild.id)
        system_channel = guild["guild_system_channel"]
        if ctx.channel.id != system_channel:
            system_channel_href = (
                f"https://discord.com/channels/{ctx.guild.id}/{system_channel}"
            )
            await ctx.send(f"This command works only on {system_channel_href}.")
            return
        settings_options = {
            "listing_channel": channel_settings,
            "logging": channel_settings,
            "remove_channel": channel_settings,
            "sell_channel": channel_settings,
            "search_channel": channel_settings,
            "item_properties": define_item_properties,
            "can_sell": role_can,
            "can_remove": role_can,
            "can_search": role_can,
        }
        message = ctx.message.content.split(" ")
        if len(message) == 1:
            embed_fields = {
                "🗂️Item Properties": "`/settings item_properties`",
                "🗣️Listing Channel": "`/settings listing_channel`",
                "📡Logging Channel": "`/settings logging`",
                "💰Sell Channel": "`/settings sell_channel`",
                "👀Search Channel": "`/settings search_channel`",
                "🗑️Remove Channel": "`/settings remove_channel`",
                "📤Can Remove": "`/settings can_remove`",
                "🔍Can Search": "`/settings can_search`",
                "📥Can Sell": "`/settings can_sell`",
            }
            embed = embed_text_message(
                text="",
                title=self.title,
                description=self.description,
                fields=embed_fields,
            )
            await ctx.send(embed[0], embed=embed[1])
        else:
            await settings_options[message[1]](ctx, self.db)


async def setup(bot):
    await bot.add_cog(Settings(bot))
