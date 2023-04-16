from .add_to_inventory import AddToInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from embed.embed_message import embed_message
from instance.pymongo_operations import MongoDb


class Sell(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the Sell cog with a Discord bot instance, an
        AddToInventory instance, the path to the inventory
        images, a default message to send, and the ID of the channel to
        send messages to.
        """
        self.bot = bot
        self.db = MongoDb()
        self.path_to_inv_images = Path(__file__).parent / "inventory_images"
        self.message = "Just landed!"

    @commands.command(name="sell")
    async def sell_item(self, ctx):
        """
        A Discord command to sell an item by adding it to the inventory
        and sending an embedded message with information about the item
        to a specific channel.

        Args:
            ctx (Context): The context of the message.

        Returns:
            None
        """
        guild = self.db.guild_in_database(guild_id=ctx.guild.id)
        if guild is None:
            await ctx.send("Guild not found in database.")
            return

        item_properties = self.db.get_item_properties(guild_id=ctx.guild.id)
        if item_properties is None:
            await ctx.send("Item properties not found in database.")
            return

        sell_role = guild["can_sell"]
        if sell_role != "all":
            if sell_role not in [role.name for role in ctx.author.roles]:
                await ctx.send(
                    f"You need to have `{sell_role}` role to sell items."
                )
                return

        sell_channel = guild["sell_channel"]
        if ctx.channel.id != sell_channel:
            channel = ctx.guild.get_channel(sell_channel)
            await ctx.send(f"You can sell only on `{channel.name}`")
            return

        self.add_to_inventory = AddToInventory(item_properties=item_properties)
        self.add_to_inventory.convert_message(ctx.message.content)

        new_item_id = self.db.get_items_id()
        new_item_id = str(new_item_id).zfill(5)
        new_item_dict = self.add_to_inventory.create_item_dict(id=new_item_id)
        self.db.add_item(guild_id=ctx.guild.id, item=new_item_dict)

        # Download any attachments and save them to the inventory_images directory
        if not ctx.message.attachments:
            await ctx.send("To list an item attach a photo.")
            return
        for count, attachment in enumerate(ctx.message.attachments):
            attachment_filename = self.add_to_inventory.download(
                guild_id=ctx.guild.id, count=count
            )
            path_to_save = f"{self.path_to_inv_images}{attachment_filename}"
            await attachment.save(path_to_save)

        # React to the message with a money bag emoji
        await ctx.message.add_reaction("💷")

        # Generate an embedded message and send it to the specified channel
        embed = embed_message(
            item_id=self.add_to_inventory.attachment_filename,
            image_path=self.path_to_inv_images,
            item_dict=new_item_dict,
        )
        target_channel = self.bot.get_channel(guild["listing_channel"])
        await target_channel.send(self.message, embed=embed[0], files=embed[1])


async def setup(bot):
    await bot.add_cog(Sell(bot))
