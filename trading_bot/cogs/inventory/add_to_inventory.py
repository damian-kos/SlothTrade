import pandas as pd
from pathlib import Path
from discord.ext import commands


class AddToInventory:
    """
    A class to add new items to the inventory.

    ...

    Attributes
    ----------
    __path_to_file : str
        The path to the CSV file containing the inventory data.
    data : pandas.DataFrame
        The inventory data.
    fresh_list : list
        An empty list to store new items.

    Methods
    -------
    load_csv():
        Load the inventory data from the CSV file.
    format_item_text(count, item):
        Format an item's text.
    convert_message(discord_message):
        Convert a Discord message to a list of item properties.
    __assign_split_message_to_variables():
        Assign item properties to instance variables.
    create_item_dict():
        Assign values to keys in dictionary. Returns new item's dict.
    download(count):
        Download an attachment and return its filename.
    """

    def __init__(self) -> None:
        """
        Initializes the instance of the class.
        """
        # self.__path_to_file = Path(__file__).parent / "inventory.csv"
        # self.data = self.load_csv()
        self.fresh_list = []

    # def load_csv(self):
    #     """
    #     Load the inventory data from the CSV file.

    #     Returns
    #     -------
    #     pandas.DataFrame
    #         The inventory data.
    #     """
    #     self.data = pd.read_csv(self.__path_to_file, dtype=str)
    #     return self.data

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

            print(f"{count}:{item}")
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

    def __assign_split_message_to_variables(self):
        """
        Assigns the split message to separate variables.
        """
        self.price = ""
        if len(self.split_message) == 6:
            self.price = self.split_message[-1]
            self.split_message.pop()
        (
            self.make,
            self.model,
            self.part,
            self.color,
            self.description,
        ) = self.split_message

    def create_item_dict(self, id) -> dict:
        """

        This method generates a new unique ID for the item, assigns the values of
        make, model, part, color, description, and price to instance variables,
        and creates a new dictionary with these values.

        """
        self.new_id = id
        self.__assign_split_message_to_variables()

        self.new_row = {
            "id": self.new_id,
            "make": self.make,
            "model": self.model,
            "part": self.part,
            "color": self.color,
            "description": self.description,
            "price": self.price,
        }
        return self.new_row

    def download(self, guild_id, count):
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
        if count == 0:
            self.attachment_filename += ".png"
        # Otherwise append .png for the single file.
        else:
            self.attachment_filename += f"_{count}.png"
        return self.attachment_filename
