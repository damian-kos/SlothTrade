from discord import Embed, File, Color
from pathlib import Path


def embed_simple_message(msg_title, msg_desc, rgb_color=(255, 255, 0)):
    embed = Embed(
        title=msg_title,
        description=msg_desc,
        color=Color.from_rgb(*rgb_color),
    )
    return embed


def embed_settings_message(
    msg_title,
    msg_desc,
    current_value_field,
    edit_field,
    accepted_value,
    rgb_color,
):
    embed = Embed(
        title=msg_title,
        color=Color.from_rgb(*rgb_color),
        description=msg_desc,
    )

    embed.add_field(
        name="📄 Current value",
        value=current_value_field,
        inline=False,
    )
    embed.add_field(name="📝 Edit", value=edit_field, inline=False)
    embed.add_field(
        name="☑ Accepted values",
        value=accepted_value,
        inline=False,
    )

    return embed


def embed_message(
    item_id: str, image_path: str, item_dict=None, interaction=None, ctx=None
):
    """
    Creates a Discord Embed message containing information about an item and its associated image.

    Args:
    - item_id (str): The unique identifier of the item.
    - image_path (str): The path to the directory containing the image file of the item.
    - item_dict (dict, optional): A dictionary containing the item's details, including its make, model, price, and description.

    Returns:
    - embed (discord.Embed): The Embed message object containing the item's details and image.
    - files (List[discord.File]): A list of file objects containing the thumbnail, author icon, and item image.
    """
    if item_dict is not None:
        list(item_dict.values())
        item_title = list(item_dict.keys())[1]
        item_subtitle = list(item_dict.values())[1]

        embed = Embed(
            title=item_title.capitalize(),
            description=item_subtitle.capitalize(),
            color=Color.green(),
            timestamp=item_dict["date"],
        )

        for key, value in list(item_dict.items())[2:]:
            if key == "price" and value == "":
                break

            key = key.capitalize()
            value = value.capitalize()
            embed.add_field(name=key, value=value, inline=True)

    file = File("trading_bot\embed\logo.png", filename="thumbnail.png")
    author_icon = File("trading_bot\embed\logo.png", filename="author_icon.png")
    item_image = File(f"{image_path}/{item_id}", filename="item_image.png")

    embed.set_thumbnail(url="attachment://thumbnail.png")
    embed.set_author(
        name="Trade Octopus",
        icon_url="attachment://author_icon.png",
        url="https://www.google.com",
    )
    embed.set_image(url="attachment://item_image.png")
    footer_text = item_id.replace(".png", "").split("_")[1]
    if interaction:
        user = interaction.guild.get_member(item_dict["user_id"])
        if user.avatar:
            user_avatar = user.avatar.url
    if ctx:
        user = ctx.guild.get_member(item_dict["user_id"])
        if user.avatar:
            user_avatar = user.avatar.url
    embed.set_footer(
        text=f"{user} • {footer_text} ",
        icon_url=user_avatar,
    )

    return embed, [file, author_icon, item_image]


def embed_text_message(
    text: str,
    title: str,
    description: str,
    rgb_color=(255, 255, 0),
    fields=None,
):
    """
        Creates a Discord Embed message containing text, a title, a description, and an optional set of fields.

        Args:
        - text (str): The text to include in the message.
        - title (str): The title of the message.
        - description (str): A description of the message.
        - fields (dict, optional): A dictionary of key-value pairs to add as fields to the message.

        Returns:
        - text (str): The original text input.
        - embed (discord.Embed): The Embed message object containing the text and other details.
        - author_icon (discord.File): A file object containing the author icon for the message.
    a"""
    embed = Embed(
        description=description,
        color=Color.from_rgb(*rgb_color),
        title=title,
    )

    if fields is not None:
        for key, value in fields.items():
            embed.add_field(
                name=key,
                value=value,
                inline=True,
            )

    author_icon = File("trading_bot\embed\logo.png", filename="author_icon.png")
    embed.set_author(
        name="Trade Octopus",
        icon_url="attachment://author_icon.png",
        url="https://www.google.com",
    )

    return text, embed, author_icon
