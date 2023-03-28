import pandas as pd
from pathlib import Path
import os
from discord.ext import commands
from embed.embed_message import embed_message, embed_text_message
from embed.embed_pagination import Pagination

# from instance.pymongo_test_insert import MongoDb


class SearchInInventory:
    COLUMN_MAPPING = {
        0: "make",
        1: "model",
        2: "part",
        3: "color",
    }

    def __init__(self) -> None:
        """A class to search for items in the inventory by make, model, part, and color.

        This class uses a CSV file as the inventory data source, and provides a method to search for items
        based on the information provided in a Discord message. The expected format of the message is:
        '/search - <make> - <model> - <part> - <color>', where each field is optional.

        Attributes:
            COLUMN_MAPPING (dict): A mapping of column index to column name in the inventory CSV file.
            data (pandas.DataFrame): The inventory data loaded from the CSV file.

        Methods:
            load_csv(): Load the inventory data from the CSV file.
            format_item_text(count, item): Format a text item by capitalizing the first letter and handling
                some specific cases (e.g., iPhone, iPad).
            convert_message(discord_message): Convert a Discord message to a list of item fields, and print
                it for debugging purposes.
            assign_split_message_to_variables(): Assign the item fields to instance variables based on the
                COLUMN_MAPPING.
            search(): Search for items in the inventory based on the assigned item fields.
            no_items_message(search_result): Create a Discord embed message to inform the user that no items
                were found based on their search.
            items_found(items_list): Create a list of dictionary representations of the inventory items that
                were found based on the search.

        """
        # self.__path_to_file = (
        #     Path("trading_bot") / "inventory" / "inventory.csv"
        # )
        # # self.db = MongoDb()
        # self.data = self.load_csv()

    def load_csv(self):
        """
        Reads and loads the inventory.csv file.

        Returns
        -------
        pandas.DataFrame
            a dataframe of the inventory.csv file
        """
        self.data = pd.read_csv(self.__path_to_file, dtype=str)
        return self.data

    def format_item_text(self, count, item):
        """
        Formats an item of text by capitalizing the first letter and standardizing certain product names.

        Args:
            count (int): The index of the item in the input message.
            item (str): The item of text to format.

        Returns:
            str: The formatted item of text.
        """
        if count in range(7):
            item = item.capitalize()
            if count == 0 and "iphone" in item.lower():
                item = "iPhone"
            if count == 0 and "ipad" in item.lower():
                item = "iPad"
            # print(f"{count}:{item}")
        return item

    def convert_message(self, discord_message):
        """
        Converts a message received from a Discord server into a list of formatted items.

        Args:
            discord_message (str): The message received from the Discord server.

        Returns:
            list: A list of formatted items.
        """
        self.split_message = [
            self.format_item_text(count, word.strip().lower())
            for count, word in enumerate(discord_message.split("-")[1:])
        ]

    def search(self):
        if len(self.split_message) == 4:
            item_dict = {
                "make": self.split_message[0],
                "model": self.split_message[1],
                "part": self.split_message[2],
                "color": self.split_message[3],
            }
        elif len(self.split_message) == 3:
            item_dict = {
                "make": self.split_message[0],
                "model": self.split_message[1],
                "part": self.split_message[2],
            }
        elif len(self.split_message) == 2:
            item_dict = {
                "make": self.split_message[0],
                "model": self.split_message[1],
            }
        elif len(self.split_message) == 1:
            item_dict = {
                "make": self.split_message[0],
            }
        return item_dict

    def no_items_message(self, search_result):
        """
        Creates an embed message to display when no items are found that match the search criteria.

        Args:
            search_result (str): A message indicating that no items were found.

        Returns:
            dict: A dictionary containing the information for the embed message.
        """
        found_items = search_result
        print(found_items)
        if isinstance(found_items, str):
            title = "Try search again or narrow your query."
            description = "Check if your command is correct."
            fields = {
                "Command syntax": "\n/search - <make> - <model> - <part> - <color>\n",
                "Command example #1": "\nsearch - iphone - xs max - charge port - black\n",
                "Command example #2": "\n/search - Samsusng - A50\n",
            }

            embed = embed_text_message(found_items, title, description, fields)
            return embed

    def items_found(self, items_list):
        """
        Given a list of item IDs, return a list of dictionaries representing the items.

        Args:
            items_list (list): A list of item IDs to retrieve.

        Returns:
            list: A list of dictionaries representing the items.
        """
        items_dicts_list = []
        if isinstance(items_list, list):
            for id in items_list:
                item = self.data[self.data["id"] == id]
                items_dicts_list.append(item.to_dict(orient="records")[0])
            return items_dicts_list
