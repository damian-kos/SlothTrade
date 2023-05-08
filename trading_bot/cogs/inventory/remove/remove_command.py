from .remove_from_inventory import RemoveFromInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from instance.pymongo_operations import MongoDb
from embed.embed_message import embed_simple_message
from embed.embed_confirmation import Confirmation
from webhook.create_webhook import removed_everything_from_database


class Remove(commands.Cog):
    def __init__(self, bot):
        """
        A class representing the 'remove' command.

        This command allows administrators to remove an item from the inventory.

        Attributes:
        bot (Bot): The Discord bot that this cog is associated with.
        remove_from_inventory (RemoveFromInventory): An instance of the RemoveFromInventory class.
        path_to_inv_images (Path): A pathlib Path object representing the directory where inventory images are stored.
        """
        self.bot = bot
        self.db = MongoDb()
        self.remove_from_inventory = RemoveFromInventory()
        self.path_to_inv_images = (
            Path(__file__).parent / "remove" / "inventory_images"
        )

    @commands.command(name="remove")
    async def delete_item(self, ctx):
        """
        Removes an item from the inventory.

        Args:
        ctx (Context): The context in which the 'remove' command was called.
        """
        guild = self.db.guild_in_database(guild_id=ctx.guild.id)
        # if guild is not None:
        remove_role = guild["can_remove"]
        if remove_role != "everyone":
            if remove_role not in [role.name for role in ctx.author.roles]:
                await ctx.send(
                    f"You need to have `{remove_role}` role to remove items."
                )
                return
        system_channel = guild["guild_system_channel"]
        system_channel_link = (
            f"https://discord.com/channels/{ctx.guild.id}/{system_channel}"
        )
        try:
            remove_channel = guild["remove_channel"]
            remove_channel_link = (
                f"https://discord.com/channels/{ctx.guild.id}/{remove_channel}"
            )
            if (
                ctx.channel.id != system_channel
                and ctx.channel.id != remove_channel
            ):
                await ctx.send(
                    f"This command works only on {system_channel_link} or {remove_channel_link}.",
                    ephemeral=True,
                )
                return
        except KeyError:
            if ctx.channel.id != system_channel:
                await ctx.send(
                    f"This command works only on {system_channel_link}.",
                    ephemeral=True,
                )
                return
        item_id = self.remove_from_inventory.get_id_from_message(
            ctx.message.content
        )
        item_dict = self.db.get_item(id=item_id, guild_id=ctx.guild.id)
        if item_id == "everything":
            if not ctx.author.guild_permissions.manage_guild:
                await ctx.send("You need to have `Manage Server` permission.")
                return
            confirmation_view = Confirmation()
            confirmation_view.response = await ctx.send(
                content="‼️ Are you sure you want remove all items from this server?  ‼️ This action can't be reversed.  ‼️",
                view=confirmation_view,
                delete_after=20,
            )
            await confirmation_view.wait()
            if confirmation_view.value:
                self.db.delete_all_items(guild_id=ctx.guild.id)
                self.remove_from_inventory.delete_all_images(
                    guild_id=ctx.guild.id
                )
                await ctx.send("✅ All items removed from database.")
                await removed_everything_from_database(ctx=ctx, guild=guild)
                return

        if not item_dict:
            embed = embed_simple_message(
                msg_title=f"Item Not Found - ID: {item_id}",
                msg_desc="No item with such ID in database.",
                rgb_color=(255, 0, 0),
            )  # red
            await ctx.send(embed=embed)
            return
        if (
            item_dict["user_id"] != ctx.author.id
            and not ctx.author.guild_permissions.manage_guild
        ):
            await ctx.send(
                "You can't delete an item which wasn't listed by you."
            )
            return
        if self.db.delete_item(guild_id=ctx.guild.id, item_id=item_id):
            self.remove_from_inventory.item_has_attachments(
                guild_id=ctx.guild.id, item_id=item_id
            )
            embed = embed_simple_message(
                msg_title=f"Item Removed - ID: {item_id}",
                msg_desc="Successfuly removed item",
                rgb_color=(102, 255, 51),
            )  # green
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Remove(bot))
