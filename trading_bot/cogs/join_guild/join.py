from discord.ext import commands
from embed.embed_message import embed_simple_message
from instance.pymongo_operations import MongoDb


class Join(commands.Cog):
    def __init__(self, bot):
        """
        Creates an event listener on_guild_join. Whenever bot joins a
        guild it searches for available text channels and sends a message
        to first channel he has permissions to.
        """
        self.bot = bot
        self.db = MongoDb()
        self.title = "Trading Bot has joined the server"
        self.description = (
            "Hi, I've been added to this server.\n"
            "Some things you should know:"
            "‣ You can configure me using: `/settings`\n"
            "During that you will setup your database, sell, listing and search channels.\n"
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await guild.system_channel.send("I'm ready to go!")
        embed = embed_simple_message(
            msg_title=self.title,
            mgs_desc=self.description,
            rgb_color=(88, 101, 242),  # blurple,
        )
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
            break
        self.db.insert_guild(
            guild_id=guild.id,
            guild_name=guild.name,
            guild_system_channel=guild.system_channel.id,
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.db.delete_guild(guild_id=guild.id)


async def setup(bot):
    await bot.add_cog(Join(bot))
