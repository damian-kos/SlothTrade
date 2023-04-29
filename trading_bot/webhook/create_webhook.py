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
    logging_webhook_url = guild["logging_webhook"]
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
            username=new_webhook_name,
        )


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
        logging_webhook_url = guild["logging_webhook"]
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
                username=webhook_name_to_delete,
            )
