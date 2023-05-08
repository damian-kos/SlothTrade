from .webhook import channel_set_message, guild_role_create_log
from instance.pymongo_operations import MongoDb
from discord import Embed, Color
from datetime import datetime


async def create_webhook_(
    ctx, channel_id, new_webhook_name, guild, channel_link
):
    db = MongoDb()

    channel_for_web = ctx.guild.get_channel(channel_id)
    channel_being_set = ctx.message.content.split(" ")[1]
    webhooks = await ctx.guild.webhooks()
    webhooks_names = [web.name for web in webhooks]
    logos = {
        "Trading Listing": "listing.png",
        "Trading Logging": "logging.png",
        "Trading Search": "search.png",
        "Trading Selling": "selling.png",
    }
    with open(f"trading_bot\embed\{logos[new_webhook_name]}", "rb") as file:
        png_bytes = file.read()
    if new_webhook_name not in webhooks_names:
        new_webhook = await channel_for_web.create_webhook(
            name=new_webhook_name, avatar=png_bytes
        )
    elif new_webhook_name in webhooks_names:
        for webhook in webhooks:
            if new_webhook_name == webhook.name:
                new_webhook = await webhook.edit(
                    name=new_webhook_name,
                    channel=channel_for_web,
                    avatar=png_bytes,
                )

                break
    message = f"This channel will be used as the {channel_being_set}."
    db.webhook_url(
        guild_id=ctx.guild.id,
        webhook=f"{channel_being_set}_webhook",
        webhook_url=new_webhook.url,
    )
    await channel_set_message(
        message=message, url=new_webhook.url, username=new_webhook_name
    )
    if new_webhook_name == "Trading Logging":
        logging_webhook_url = new_webhook.url
    else:
        logging_webhook_url = logging_webhook_exists(guild)
    if logging_webhook_url:
        embed = Embed(
            title=f"{new_webhook_name} webhook created",
            description=f"{channel_link} will be used as the {channel_being_set}",
            color=Color.from_rgb(88, 101, 242),
            timestamp=datetime.now(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar.url,
            text=f"{ctx.author}",
        )

        await guild_role_create_log(
            url=logging_webhook_url,
            embed_message=embed,
        )
    else:
        return


def logging_webhook_exists(guild):
    try:
        logging_webhook_url = guild["logging_webhook"]
    except KeyError:
        return None
    if logging_webhook_url:
        return logging_webhook_url


async def channel_updated(guild, channel, channel_link, ctx):
    channel_being_set = ctx.message.content.split(" ")[1]
    logging_webhook_url = logging_webhook_exists(guild)
    if logging_webhook_url:
        embed = Embed(
            title=f"{channel} is now updated",
            description=f"{channel_link} will be used as the {channel_being_set}",
            color=Color.from_rgb(88, 101, 242),
            timestamp=datetime.now(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar.url,
            text=f"{ctx.author}",
        )

        await guild_role_create_log(
            url=logging_webhook_url,
            embed_message=embed,
        )
    else:
        return


async def channel_removed(guild, channel, ctx):
    logging_webhook_url = logging_webhook_exists(guild)
    if logging_webhook_url:
        embed = Embed(
            title=f"{channel} is now removed",
            description=f"{channel} is now not active.",
            color=Color.from_rgb(88, 101, 242),
            timestamp=datetime.now(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar.url,
            text=f"{ctx.author}",
        )

        await guild_role_create_log(
            url=logging_webhook_url,
            embed_message=embed,
        )
    else:
        return


async def delete_webhook_(ctx, webhook_name_to_delete, guild):
    db = MongoDb()
    # channel_for_web = ctx.guild.get_channel(channel_id)
    channel_to_remove = ctx.message.content.split(" ")[1]
    webhooks = await ctx.guild.webhooks()
    webhooks_names = [web.name for web in webhooks]
    if webhook_name_to_delete in webhooks_names:
        webhook_index = webhooks_names.index(webhook_name_to_delete)
        webhook_to_delete = webhooks[webhook_index]
        await webhook_to_delete.delete()
        if webhook_name_to_delete != "Trading Logging":
            logging_webhook_url = logging_webhook_exists(guild)
            if logging_webhook_url:
                embed = Embed(
                    title=f"{webhook_name_to_delete} webhook removed",
                    description=f"The {channel_to_remove} was removed",
                    color=Color.from_rgb(88, 101, 242),
                    timestamp=datetime.now(),
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar.url,
                    text=f"{ctx.author}",
                )

                await guild_role_create_log(
                    url=logging_webhook_url,
                    embed_message=embed,
                )
            else:
                return


# async def channel_updated(guild):
#     try:
#         logging_webhook_url = guild["logging_webhook"]
#     except KeyError:
#         return
#     if logging_webhook_url:
#         embed = Embed(
#             title=f"{webhook_name_to_delete} webhook removed",
#             description=f"The {channel_to_remove} was removed",
#             color=Color.from_rgb(88, 101, 242),
#             timestamp=datetime.now(),
#         )
#         embed.set_footer(
#             icon_url=ctx.author.avatar.url,
#             text=f"{ctx.author}",
#         )

#         await guild_role_create_log(
#             url=logging_webhook_url,
#             embed_message=embed,
#         )


async def removed_everything_from_database(ctx, guild):
    logging_webhook_url = guild["logging_webhook"]
    if logging_webhook_url:
        embed = Embed(
            title=f"All items and images from database were removed ",
            description=f"That's it they are gone",
            color=Color.from_rgb(255, 0, 0),
            timestamp=datetime.now(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar.url,
            text=f"{ctx.author}",
        )

        await guild_role_create_log(
            url=logging_webhook_url,
            embed_message=embed,
        )
