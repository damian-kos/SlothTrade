from pathlib import Path
from embed.embed_message import embed_message
from instance.pymongo_operations import MongoDb
from webhook.webhook import new_listing_message
from datetime import datetime


async def has_permissions_to_sell(interaction):
    db = MongoDb()
    guild = db.guild_in_database(guild_id=interaction.guild_id)
    sell_role = guild["can_sell"]
    if sell_role != "everyone":
        if sell_role not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message(
                f"You need to have `{sell_role}` role to sell items."
            )
            return False


async def channel_check(interaction):
    db = MongoDb()
    guild = db.guild_in_database(guild_id=interaction.guild_id)
    sell_channel = guild["sell_channel"]
    if interaction.channel_id != sell_channel:
        channel = interaction.guild.get_channel(sell_channel)
        await interaction.response.send_message(
            f"You can sell only on `{channel.name}`"
        )
        return False


async def inventory_add(add_to_inv, interaction, item_values):
    db = MongoDb()
    guild = db.guild_in_database(guild_id=interaction.guild_id)
    add_to = add_to_inv
    new_item_id = db.get_items_id()
    new_item_id = str(new_item_id).zfill(5)
    user_id = interaction.user.id
    user_avatar = interaction.user.avatar.url
    new_item_dict = add_to.create_item_dict(
        id=new_item_id,
        guild=guild,
        item_values=item_values,
        user_id=user_id,
        user_avatar=user_avatar,
    )
    if not isinstance(new_item_dict, dict):
        # If new item can't be created it will create and embed
        # message instead
        await interaction.response.send_message(
            new_item_dict[0],
            embed=new_item_dict[1],
            file=new_item_dict[2],
        )
        return
    db.add_item(guild_id=interaction.guild_id, item=new_item_dict)


async def check_attachment(add_to_inv, interaction, attachment):
    add_to = add_to_inv
    path_to_inv_images = Path(__file__).parent.parent / "inventory_images"
    if attachment is None:
        await interaction.respond.send_message(
            "To list an item attach a photo."
        )
        return
    attachment_filename = add_to.download(
        guild_id=interaction.guild_id,
    )
    path_to_save = f"{path_to_inv_images}{attachment_filename}"
    await attachment.save(path_to_save)


async def send_new_listing(add_to_inv, interaction):
    db = MongoDb()
    guild = db.guild_in_database(guild_id=interaction.guild_id)
    path_to_inv_images = Path(__file__).parent.parent / "inventory_images"
    embed = embed_message(
        item_id=add_to_inv.attachment_filename,
        image_path=path_to_inv_images,
        item_dict=add_to_inv.new_row,
        interaction=interaction,
    )
    # target_channel = interaction.client.get_channel(guild["listing_channel"])
    listing_webhook_url = guild["listing_channel_webhook"]
    await new_listing_message(
        url=listing_webhook_url,
        message="Just landed!",
        embed_message=embed[0],
        file=embed[1],
    )
    # await target_channel.send("Just landed", embed=embed[0], files=embed[1])
