from discord.ext import commands
from instance.pymongo_operations import MongoDb
from cogs.inventory.add.sell_command import create_sell_app_command


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDb()

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        print(event_type)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.is_ready():
            guilds = self.bot.guilds
        for guild in guilds:
            try:
                current_guild = self.db.guild_in_database(guild_id=guild.id)
                parameter_names = {
                    f"param{count}": name
                    for count, name in enumerate(
                        current_guild["item_properties"]
                    )
                }
                parameter_descriptions = {
                    f"param{count}": desc
                    for count, desc in enumerate(
                        current_guild["item_params_description"]
                    )
                }
                new_command = create_sell_app_command(
                    bot=self.bot,
                    dict_with_names=parameter_names,
                    dict_with_descriptions=parameter_descriptions,
                )
                self.bot.tree.add_command(new_command, guild=guild)
                sync = await self.bot.tree.sync(guild=guild)
            except KeyError:
                print("sell")


async def setup(bot):
    await bot.add_cog(Logging(bot))
