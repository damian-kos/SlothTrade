from .delete_from_inventory import DeleteFromInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from error_handler.errors import handle_command_error, handle_error


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
        self.delete_from_inventory = DeleteFromInventory()
        self.path_to_inv_images = Path(__file__).parent / "inventory_images"

    @commands.command(name="remove")
    @commands.has_role("Admin")
    async def delete_item(self, ctx):
        """
        Deletes an item from the inventory.

        Args:
        ctx (Context): The context in which the 'remove' command was called.
        """
        try:
            # This channel should be available only for users we want them to
            # have possibility to list items.
            if ctx.channel.id == 1061730004515430542:
                self.delete_from_inventory.load_csv()
                item_id = self.delete_from_inventory.get_id_from_message(
                    ctx.message.content
                )
                self.delete_from_inventory.delete(item_id)
                self.delete_from_inventory.item_has_attachments()
        except Exception as e:
            await handle_command_error(ctx, e)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Handles errors that occur when the 'remove' command is called.

        Args:
        ctx (Context): The context in which the error occurred.
        error (Exception): The error that occurred.
        """
        await handle_error(ctx, error)


async def setup(bot):
    await bot.add_cog(Remove(bot))
