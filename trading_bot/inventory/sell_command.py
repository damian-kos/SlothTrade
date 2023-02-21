from .add_to_inventory import AddToInventory
from discord.ext import commands
from discord.ext.commands import Bot
from pathlib import Path
from embed.embed_message import embed_message


class Sell(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the Sell cog with a Discord bot instance, an
        AddToInventory instance, the path to the inventory
        images, a default message to send, and the ID of the channel to
        send messages to.
        """
        self.bot = bot
        self.add_to_inventory = AddToInventory()
        self.path_to_inv_images = Path(__file__).parent / "inventory_images"
        self.message = "Just landed!"
        # This channel ID defines to what channel we will be sending
        # posts of items we just added to our inventory. 
        self.sell_channel = 1076493112542765106

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
        # Check if the message was sent in the correct channel
        # This channel should be available only for users we want them to
        # have possibility to list items.
        if ctx.channel.id == 1061730004515430542:
            self.add_to_inventory.load_csv()
            self.add_to_inventory.convert_message(ctx.message.content)
            self.add_to_inventory.add()
            # Download any attachments and save them to the
            # inventory_images directory
            if ctx.message.attachments:
                for count, attachment in enumerate(ctx.message.attachments):
                    attachment_filename = self.add_to_inventory.download(count)
                    path_to_save = (
                        f"{self.path_to_inv_images}{attachment_filename}"
                    )
                    await attachment.save(path_to_save)
                # React to the message with a money bag emoji
                await ctx.message.add_reaction("💷")
                # Generate an embedded message and send it to the specified channel
                embed = embed_message(
                    item_id=self.add_to_inventory.new_id,
                    image_path=self.path_to_inv_images,
                    item_dict=self.add_to_inventory.new_row,
                )
                target_channel = self.bot.get_channel(self.sell_channel)
                await target_channel.send(
                    self.message, embed=embed[0], files=embed[1]
                )
        else:
            # React to the message with a poop emoji if it was sent in the wrong channel
            # Item won't be added to inventory nor attachments will be 
            # downloaded.
            await ctx.message.add_reaction("💩")


async def setup(bot):
    await bot.add_cog(Sell(bot))
