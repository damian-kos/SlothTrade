import pandas as pd
from pathlib import Path
from discord.ext import commands
from collections import namedtuple
from embed.embed_message import embed_text_message
from datetime import datetime


class AddToInventory:
    """
    A class to add new items to the inventory.

    ...

    Methods
    -------
    format_item_text(count, item):
        Format an item's text.
    convert_message(discord_message):
        Convert a Discord message to a list of item properties.
    __price_handler():
        Assign item properties to instance variables.
    create_item_dict():
        Assign values to keys in dictionary. Returns new item's dict.
    download(count):
        Download an attachment and return its filename.
    """

    def __init__(self, item_properties=None) -> None:
        """
        Initializes the instance of the class.
        """
        if item_properties is not None:
            self.Item = namedtuple(
                "Item",
                (*item_properties, "price", "user_id", "user_avatar", "date"),
            )
        self.current_item_properties = item_properties

    def format_item_text(self, count, item) -> str:
        """
        Format an item's text.

        Parameters
        ----------
        count : int
            The index of the current item in the list of item properties.
        item : str
            The item property to format.

        Returns
        -------
        str
            The formatted item property.
        """
        if count in range(7):
            item = item.capitalize()
            if count == 0 and "iphone" in item.lower():
                item = "iPhone"
            if count == 0 and "ipad" in item.lower():
                item = "iPad"
        return item

    def convert_message(self, discord_message):
        """
        Convert a Discord message to a list of item properties.

        Parameters
        ----------
        discord_message : str
            The Discord message to convert.
        """
        # discord_message = "/sell - iPhone - 7 - Screen - Black - Description"
        self.message_to_format = discord_message
        self.split_message = self.message_to_format.split("-")[1:]
        self.split_message = [word.strip() for word in self.split_message]
        for count, item in enumerate(self.split_message):
            self.split_message[count] = self.format_item_text(count, item)

    def __price_handler(self, item_values):
        """
        Checks if given message as a list is longer than item's
        attribute. Assigns price value if so.
        """
        self.price = ""
        if len(self.item_values) == len(self.current_item_properties) + 1:
            if self.item_values[-1] is not None:
                self.price = self.item_values[-1]
                self.item_values.pop()
            if self.item_values[-1] is None:
                self.item_values.pop()

    def create_item_dict(
        self,
        id,
        item_values,
        user_id,
        user_avatar,
        guild=None,
    ) -> dict:
        """
        Generates a new unique ID for the item, assigns the values of
        make, model, part, color, description, and price to instance variables,
        and creates a new dictionary with these values.
        """
        self.item_values = item_values
        self.new_id = id
        self.timestamp = datetime.now()
        self.__price_handler(self.item_values)
        try:
            item = self.Item(
                *item_values, self.price, user_id, user_avatar, self.timestamp
            )
            self.new_row = {"id": id, **item._asdict()}
            return self.new_row
        except TypeError:
            item_properties = guild["item_properties"]
            properties_are = (
                f"{' '.join([f'`{item}`' for item in item_properties])}"
            )
            command_syntax = f"\n/sell {' '.join([f'`{item}`' for item in item_properties])}\n"
            command_example = f"\n/sell {' '.join([f'property{i}' for i in range(len(item_properties))])}\n"
            title = "To list an item you need to follow this server's listing scheme."
            description = (
                "Follow the rule and check if your command is correct."
            )
            fields = {
                "Item listed on this server should have": f"{len(item_properties)} properties",
                "These properties are": properties_are,
                "Command syntax to list an item": command_syntax,
                "Command example #1": command_example,
            }

            embed = embed_text_message(
                text="",
                title=title,
                description=description,
                rgb_color=(255, 0, 0),
                fields=fields,
            )
            return embed

    def download(self, guild_id):
        """
        Download an attachment and return its filename.

        Parameters
        ----------
        count : int
            The index of the current attachment being downloaded.

        Returns
        -------
        str
            The filename of the downloaded attachment.
        """
        self.attachment_filename = f"/{guild_id}_{self.new_id}"
        # If the count is not zero, add the count to the file name.

        self.attachment_filename += ".png"

        return self.attachment_filename
