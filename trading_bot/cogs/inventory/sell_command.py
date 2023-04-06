from .add_to_inventory import AddToInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from embed.embed_message import embed_message
from instance.pymongo_test_insert import MongoDb


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
        self.add_to_inventory = AddToInventory()
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
        if guild is not None:
            self.sell_channel = guild["sell_channel"]
            self.listing_channel = guild["listing_channel"]
            # Check if the message was sent in the correct channel
            # This channel should be available only for users we want them to
            # have possibility to list items.
            if ctx.channel.id == self.sell_channel:
                self.add_to_inventory.convert_message(ctx.message.content)
                new_item_id = self.db.get_items_id(guild_id=ctx.guild.id)
                new_item_id = str(new_item_id).zfill(5)
                new_item_dict = self.add_to_inventory.create_item_dict(
                    id=new_item_id
                )
                self.db.add_item(guild_id=ctx.guild.id, item=new_item_dict)
                # Download any attachments and save them to the
                # inventory_images directory
                if ctx.message.attachments:
                    for count, attachment in enumerate(ctx.message.attachments):
                        attachment_filename = self.add_to_inventory.download(
                            guild_id=ctx.guild.id, count=count
                        )
                        path_to_save = (
                            f"{self.path_to_inv_images}{attachment_filename}"
                        )
                        await attachment.save(path_to_save)
                    # React to the message with a money bag emoji
                    await ctx.message.add_reaction("💷")
                    #  Generate an embedded message and send it to the specified channel
                    embed = embed_message(
                        item_id=self.add_to_inventory.attachment_filename,
                        image_path=self.path_to_inv_images,
                        item_dict=self.add_to_inventory.new_row,
                    )
                    target_channel = self.bot.get_channel(self.listing_channel)
                    await target_channel.send(
                        self.message, embed=embed[0], files=embed[1]
                    )


async def setup(bot):
    await bot.add_cog(Sell(bot))
