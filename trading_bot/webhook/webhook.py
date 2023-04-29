from discord import Webhook
import aiohttp


async def channel_set_message(url, username, message):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url,
            session=session,
        )
        await webhook.send(message, username=username)


async def guild_role_create_log(url, embed_message):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url,
            session=session,
        )
        await webhook.send(embed=embed_message)
