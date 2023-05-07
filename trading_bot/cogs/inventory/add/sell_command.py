from discord.ext import commands
import discord
from discord import app_commands
from instance.pymongo_operations import MongoDb
from typing import Optional
from cogs.inventory.add.sell_checks import (
    has_permissions_to_sell,
    channel_check,
    inventory_add,
    check_attachment,
    send_new_listing,
)
from cogs.inventory.add.add_to_inventory import AddToInventory


def create_sell_app_command(bot, dict_with_names, dict_with_descriptions):
    if len(dict_with_names) == 2:

        @app_commands.command()
        @app_commands.rename(**dict_with_names)
        @app_commands.describe(**dict_with_descriptions, price="Your offer")
        async def sell(
            interaction: discord.Interaction,
            param0: str,
            param1: str,
            image: discord.Attachment,
            price: Optional[str],
        ):
            add_to = AddToInventory(item_properties=[*dict_with_names.values()])
            if await has_permissions_to_sell(interaction=interaction) == False:
                return

            if await channel_check(interaction=interaction) == False:
                return

            await inventory_add(
                add_to_inv=add_to,
                interaction=interaction,
                item_values=[param0, param1, price],
            )
            await check_attachment(
                add_to_inv=add_to, interaction=interaction, attachment=image
            )

            await send_new_listing(add_to_inv=add_to, interaction=interaction)
            await interaction.response.send_message(
                f"Listed successfully.",
            )

        return sell

    if len(dict_with_names) == 3:

        @app_commands.command()
        @app_commands.rename(**dict_with_names)
        @app_commands.describe(**dict_with_descriptions)
        async def sell(
            interaction: discord.Interaction,
            param0: str,
            param1: str,
            param2: str,
            image: discord.Attachment,
            price: Optional[str],
        ):
            add_to = AddToInventory(item_properties=[*dict_with_names.values()])
            if await has_permissions_to_sell(interaction=interaction) == False:
                return

            if await channel_check(interaction=interaction) == False:
                return

            await inventory_add(
                add_to_inv=add_to,
                interaction=interaction,
                item_values=[param0, param1, param2, price],
            )
            await check_attachment(
                add_to_inv=add_to, interaction=interaction, attachment=image
            )

            await send_new_listing(add_to_inv=add_to, interaction=interaction)
            await interaction.response.send_message(
                f"Listed successfully.",
            )

        return sell

    if len(dict_with_names) == 4:

        @app_commands.command()
        @app_commands.rename(**dict_with_names)
        @app_commands.describe(**dict_with_descriptions)
        async def sell(
            interaction: discord.Interaction,
            param0: str,
            param1: str,
            param2: str,
            param3: str,
            image: discord.Attachment,
            price: Optional[str],
        ):
            add_to = AddToInventory(item_properties=[*dict_with_names.values()])
            if await has_permissions_to_sell(interaction=interaction) == False:
                return

            if await channel_check(interaction=interaction) == False:
                return

            await inventory_add(
                add_to_inv=add_to,
                interaction=interaction,
                item_values=[param0, param1, param2, param3, price],
            )
            await check_attachment(
                add_to_inv=add_to, interaction=interaction, attachment=image
            )

            await send_new_listing(add_to_inv=add_to, interaction=interaction)
            await interaction.response.send_message(
                f"Listed successfully.",
            )

        return sell
