from discord.ext import commands
from instance.pymongo_operations import MongoDb
from embed.embed_message import embed_simple_message
from .webhook import guild_role_create_log


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        print(event_type)

    # @commands.Cog.listener()
    # async def on_audit_log_entry_create(self, entry):
    #     print(f"AUDIT: {entry}")

    # @commands.Cog.listener()
    # async def on_member_update(self, before, after):
    #     db = MongoDb()
    #     guild = db.guild_in_database(guild_id=before.guild.id)
    #     webhook_url = guild["logging_webhook"]
    #     embed = embed_simple_message(
    #         msg_title="Member updated",
    #         msg_desc=f"Before: {before.nick}\n After: {after.nick}",
    #         rgb_color=(88, 101, 242),
    #     )
    #     await guild_role_create_log(
    #         url=webhook_url, username="Trading Logging", embed_message=embed
    #     )


async def setup(bot):
    await bot.add_cog(Logging(bot))
