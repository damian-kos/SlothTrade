from .webhook import channel_set_message
from instance.pymongo_operations import MongoDb


async def create_webhook_(ctx, channel_id, new_webhook_name):
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
    print(f"create_webhook: {new_webhook.url}")
    await channel_set_message(
        message=message, url=new_webhook.url, username=new_webhook_name
    )
