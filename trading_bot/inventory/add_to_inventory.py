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
    assign_split_message_to_variables():
        Assign item properties to instance variables.
    __save_to_csv():
        Save the new item to the CSV file.
    add():
        Add a new item to the inventory.
    download(count):
        Download an attachment and return its filename.
    """

    def __init__(self) -> None:
        """
        Initializes the instance of the class.
        """
        self.__path_to_file = Path(__file__).parent / "inventory.csv"
        self.data = self.load_csv()
        self.fresh_list = []

    def load_csv(self):
        """
        Load the inventory data from the CSV file.

        Returns
        -------
        pandas.DataFrame
            The inventory data.
        """
        self.data = pd.read_csv(self.__path_to_file, dtype=str)
        return self.data

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

    def assign_split_message_to_variables(self):
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
        print(self.split_message)

    def __save_to_csv(self):
        """
        Save the new item to the CSV file.
        """
        self.data.to_csv(self.__path_to_file, index=False)

    def add(self):
        """
        Add a new item to the inventory.
        """

        # Generate the next unique ID
        try:
            # Get the last item's ID in the DataFrame and add 1 to it
            self.new_id = str(int(self.data["id"].iloc[-1]) + 1).zfill(5)
        except IndexError:
            # If no item is found, set new_id to 00001
            self.new_id = "00001"

        self.assign_split_message_to_variables()
        # inventory.csv
        # id,make,model,part,color,description,price
        self.new_row = {
            "id": self.new_id,
            "make": self.make,
            "model": self.model,
            "part": self.part,
            "color": self.color,
            "description": self.description,
            "price": self.price,
        }
        self.data = pd.concat(
            [self.data, pd.DataFrame(self.new_row, index=[0])],
            ignore_index=True,
        )
        self.__save_to_csv()
        print("Saved_to_csv")

    def download(self, count):
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
        attachment_filename = f"/{self.new_id}"
        # If the count is not zero, add the count to the file name.
        if count == 0:
            attachment_filename += ".png"
        # Otherwise append .png for the single file.
        else:
            attachment_filename += f"_{count}.png"
        return attachment_filename
