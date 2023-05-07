from discord.ext import commands
from embed.embed_pagination import Pagination
from embed.embed_message import embed_message
from .search_in_inventory import SearchInInventory
from pathlib import Path
from error_handler.errors import handle_command_error, handle_error
from instance.pymongo_operations import MongoDb


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
        self.search_in_inventory = SearchInInventory()
        self.bot = bot
        self.db = MongoDb()
        self.path_to_inv_images = (
            Path("trading_bot") / "cogs" / "inventory" / "inventory_images"
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
        guild = self.db.guild_in_database(guild_id=ctx.guild.id)

        search_role = guild["can_search"]
        if search_role != "everyone":
            if search_role not in [role.name for role in ctx.author.roles]:
                await ctx.send(
                    f"You need to have `{search_role}` role to remove items."
                )
                return

        search_channel = guild["search_channel"]
        if ctx.channel.id != search_channel:
            channel = ctx.guild.get_channel(search_channel)
            await ctx.send(f"You can search only on `{channel.name}`")
            return

        search_query = self.search_in_inventory.convert_message(
            ctx.message.content
        )
        print(search_query)
        search_results = self.db.levenshtein_search(
            guild_id=ctx.guild.id, search=search_query
        )
        if isinstance(search_results, str):
            message = self.search_in_inventory.no_items_message(search_results)
            await ctx.send(
                message[0],
                embed=message[1],
                file=message[2],
            )
        else:
            items_dicts = search_results
            first_dict = items_dicts[0]
            embed = embed_message(
                item_id=(f"{ctx.guild.id}_{first_dict['id']}.png"),
                image_path=f"{self.path_to_inv_images}",
                item_dict=first_dict,
                ctx=ctx,
            )

            if len(items_dicts) > 1:
                view = Pagination(
                    guild_id=ctx.guild.id, found_items=items_dicts
                )
                view.response = await ctx.send(
                    "I've found these items for you.",
                    embed=embed[0],
                    files=embed[1],
                    view=view,
                )
            elif len(items_dicts) == 1:
                await ctx.send(
                    "I've found these items for you.",
                    embed=embed[0],
                    files=embed[1],
                )


async def setup(bot):
    await bot.add_cog(Search(bot))
