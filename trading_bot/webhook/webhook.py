from discord import Webhook
import aiohttp


async def channel_set_message(url, username, message):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url,
            session=session,
        )
        await webhook.send(message, username=username)


async def new_listing_message(url, message, embed_message, file):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url,
            session=session,
        )
        await webhook.send(message, embed=embed_message, files=file)


async def guild_role_create_log(url, embed_message):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url,
            session=session,
        )
        await webhook.send(embed=embed_message)
