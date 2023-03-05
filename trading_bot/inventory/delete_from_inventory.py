import pandas as pd
from pathlib import Path
import os
from discord.ext import commands


class DeleteFromInventory:
    def __init__(self) -> None:
        """
        A class for managing the inventory.csv file and deleting items from the inventory.

        ...

        Attributes
        ----------
        __path_to_file : pathlib.Path
            the path to the inventory.csv file
        __path_to_inv_images : pathlib.Path
            the path to the inventory_images directory
        data : pandas.DataFrame
            a dataframe of the inventory.csv file

        Methods
        -------
        load_csv():
            Reads and loads the inventory.csv file.
        get_id_from_message(discord_message):
            Parses the item ID from a given Discord message.
        __save_to_csv():
            Saves changes made to the inventory.csv file.
        delete():
            Deletes an item from the inventory.csv file.
        item_has_attachments():
            Deletes the corresponding image file for an item from the inventory_images directory.
        """
        self.__path_to_file = Path(__file__).parent / "inventory.csv"
        self.__path_to_inv_images = Path(__file__).parent / "inventory_images"
        self.data = self.load_csv()

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

    def get_id_from_message(self, discord_message: str) -> str:
        """
        Parses the item ID from a given Discord message.

        Parameters
        ----------
        discord_message : str
            the Discord message to parse

        Returns
        -------
        str
            a str contatining item_id
        """
        self.message_to_format = discord_message.split(" ")[1:]
        return self.message_to_format[0]

    def __save_to_csv(self):
        """
        Saves changes made to the inventory.csv file.

        Returns
        -------
        None
        """
        self.data.to_csv(self.__path_to_file, index=False)

    def delete(self, item_id: str):
        """
        Deletes an item from the inventory.csv file.

        Args:
            item_id (str): A item IDs to remove.

        Returns
        -------
        None
        """
        row_to_delete = self.data.loc[self.data["id"] == item_id]
        self.data = self.data.drop(row_to_delete.index)
        self.__save_to_csv()

    def item_has_attachments(self, guild_id, item_id):
        """
        Deletes the corresponding image file for an item from the inventory_images directory.

        Returns
        -------
        None
        """
        files = os.listdir(self.__path_to_inv_images)
        for file in files:
            if str(guild_id) in file and item_id in file:
                __file_path = os.path.join(self.__path_to_inv_images, file)
                os.remove(__file_path)
