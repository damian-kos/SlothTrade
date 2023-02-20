from discord.ext import commands
from embed.embed_pagination import Pagination
from embed.embed_message import embed_message
from .search_in_inventory import SearchInInventory
from pathlib import Path
import discord
from error_handler.errors import handle_command_error, handle_error


class Search(commands.Cog):
    def __init__(self, bot):
        """
        A class representing the search functionality of the bot.

        Methods
        -------
        search(ctx)
            Searches for items in the bot's inventory based on user input.
        on_command_error(ctx, error)
            An error handler for the search command.
        """
        self.search = SearchInInventory()
        self.bot = bot
        self.path_to_inv_images = (
            Path("trading_bot") / "inventory" / "inventory_images"
        )

    @commands.command(name="search")
    async def search(self, ctx):
        """
        Searches for items in the bot's inventory based on user input.

        Parameters
        ----------
        ctx : Context
            The context of the message.
        """
        try:
            self.search.load_csv()
            self.search.convert_message(ctx.message.content)
            search_results = self.search.search()
            print(search_results)
            if isinstance(search_results, str):
                message = self.search.no_items_message(search_results)
                await ctx.send(
                    message[0],
                    embed=message[1],
                    file=message[2],
                )
            else:
                print(search_results)
                items_dicts = self.search.items_found(search_results)
                first_dict = items_dicts[0]
                embed = embed_message(
                    item_id=first_dict["id"],
                    image_path=f"{self.path_to_inv_images}",
                    item_dict=first_dict,
                )

                view = Pagination(items_dicts)
                view.response = await ctx.send(
                    "I've found these items for you.",
                    embed=embed[0],
                    files=embed[1],
                    view=view,
                )
        except Exception as e:
            await handle_command_error(ctx, e)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        An error handler for the search command.

        Parameters
        ----------
        ctx : Context
            The context of the message.
        error : Exception
            The error that occurred.
        """
        await handle_error(ctx, error)


async def setup(bot):
    await bot.add_cog(Search(bot))
