from .delete_from_inventory import DeleteFromInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from error_handler.errors import handle_command_error, handle_error
from instance.pymongo_operations import MongoDb


class Remove(commands.Cog):
    def __init__(self, bot):
        """
        A class representing the 'remove' command.

        This command allows administrators to remove an item from the inventory.

        Attributes:
        bot (Bot): The Discord bot that this cog is associated with.
        delete_from_inventory (DeleteFromInventory): An instance of the DeleteFromInventory class.
        path_to_inv_images (Path): A pathlib Path object representing the directory where inventory images are stored.
        """
        self.bot = bot
        self.db = MongoDb()
        self.delete_from_inventory = DeleteFromInventory()
        self.path_to_inv_images = Path(__file__).parent / "inventory_images"

    @commands.command(name="remove")
    async def delete_item(self, ctx):
        """
        Deletes an item from the inventory.

        Args:
        ctx (Context): The context in which the 'remove' command was called.
        """
        guild = self.db.guild_in_database(guild_id=ctx.guild.id)
        # if guild is not None:

        remove_role = guild["can_remove"]
        if remove_role != "all":
            if remove_role not in [role.name for role in ctx.author.roles]:
                await ctx.send(
                    f"You need to have `{remove_role}` role to remove items."
                )
                return

        system_channel = guild["guild_system_channel"]
        if ctx.channel.id != system_channel:
            await ctx.send(f"This command works only on `system channel`.")
            return

        item_id = self.delete_from_inventory.get_id_from_message(
            ctx.message.content
        )
        self.db.delete_item(guild_id=ctx.guild.id, item_id=item_id)
        self.delete_from_inventory.item_has_attachments(
            guild_id=ctx.guild.id, item_id=item_id
        )


async def setup(bot):
    await bot.add_cog(Remove(bot))
