from discord.ext import commands
from instance.pymongo_operations import MongoDb
from embed.embed_message import embed_simple_message
from .webhook import guild_role_create_log


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        db = MongoDb()
        guild = db.guild_in_database(guild_id=channel.guild.id)
        webhook_url = guild["logging_webhook"]
        embed = embed_simple_message(
            msg_title="New webhook created",
            msg_desc="Lorem ipsum.",
            rgb_color=(88, 101, 242),
        )
        await guild_role_create_log(
            url=webhook_url, username="Trading Logging", embed_message=embed
        )

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        print(event_type)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        print(f"AUDIT: {entry}")


async def setup(bot):
    await bot.add_cog(Logging(bot))
