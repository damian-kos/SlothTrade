from instance.pymongo_get_database import get_database
from .levenshtein_algorithm import fuzz_test
from typing import Union, Dict, Any, List

class MongoDb:
    """
    A class that represents a connection to a MongoDB database and provides methods for interacting with it.

    Attributes:
        dbname (pymongo.database.Database): A connection to the MongoDB database.
        collection_name (pymongo.collection.Collection): The name of the collection within the database.

    Methods:
        guild_in_database(guild_id: int) -> dict or None:
            Searches for a guild with the given ID in the database.

    """

    def __init__(self):
        """
        Initializes a new instance of the MongoDb class and connects to 
        the MongoDB database.
        """
        self.dbname = get_database()
        self.collection_name = self.dbname["guilds"]

    def guild_in_database(self, guild_id: int) -> dict:
        """
        Searches for a guild with the given ID in the database.

        Args:
            guild_id: The ID of the guild to search for.

        Returns:
            dict or None: 
                A dictionary representing the guild if found, or None if 
                    not found.

        Examples:
            >>> db = MongoDb()
            >>> guild = db.guild_in_database(123456789)
            >>> print(guild)
            {'_id': 123456789, 'name': 'My Guild', 'members': 50}
        """
        self.guild = self.collection_name.find_one({"_id": guild_id})
        return self.guild

    def insert_guild(
        self, guild_id: int, guild_name: str, guild_system_channel: int
    ):
        """
        Inserts a new guild into the database with the given ID, name, 
        and system channel ID.

        Args:
            guild_id: The ID of the guild to be inserted.
            guild_name: The name of the guild to be inserted.
            guild_system_channel: The ID of the system channel of the 
                guild to be inserted.

        Returns:
            None.

        Examples:
            >>> db = MongoDb()
            >>> db.insert_guild(123456789, 'My Guild', 987654321)
        """
        guild_info = {
            "_id": guild_id,
            "guild_name": guild_name,
            "guild_system_channel": guild_system_channel,
        }
        self.collection_name.insert_one(guild_info)

    def delete_guild(self, guild_id: int):
        """
        Deletes the guild with the given ID from the database.

        Args:
            guild_id: The ID of the guild to be deleted.

        Returns:
            None.

        Examples:
            >>> db = MongoDb()
            >>> db.delete_guild(123456789)
        """
        guild = {
            "_id": guild_id,
        }
        self.collection_name.delete_one(guild)

    def set_channel(self, guild_id: int, channel_id: str, channel_type=""):
        """Sets the ID of the specified channel for the guild with the 
        given ID.

        Args:
            guild_id: The ID of the guild to be updated.
            channel_id: The ID of the channel to set.
            channel_type: The type of channel to set.

        Return:
            None
        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{channel_type}": channel_id}},
            )

    def delete_channel(self, guild_id: int, channel_type:str):
        """Removes the channel assigned to guild with the given ID.
        Removes webhook if present.

        Args:
            guild_id: The ID of the guild to be updated.
            channel_type: The type of channel to set.

        Return:
            None
        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$unset": {f"{channel_type}": ""}},
            )
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$unset": {f"{channel_type}_webhook": ""}},
            )

    def webhook_url(self, guild_id: int, webhook: str, webhook_url: str):
        """Sets the webhook and its url of the specified channel for the 
        guild with the given ID.

        Args:
            guild_id: The ID of the guild to be updated.
            webhook: The webhooks name.
            webhook_url: The discord webhooks url address.

        Return:
            None

        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{webhook}": webhook_url}},
            )

    def define_item_properties(self, guild_id:int, item_properties_tuple:tuple):
        """Sets the properties of an item of the guild with the given ID.

        Args:
            guild_id: The ID of the guild to be updated.
            item_properties_tuple: The properties of an item for the 
                guild.

        Return:
            None

        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"item_properties": item_properties_tuple}},
            )

    def define_item_properties_descriptions(
            self, 
            guild_id:int, 
            descriptions_tuple:tuple
            ):
        """Sets the descriptions of an item properties of the guild with 
        the given ID.

        Args:
            guild_id: The ID of the guild to be updated.
            descriptions_tuple: The properties of an item for the guild.

        Return:
            None

        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"item_params_description": descriptions_tuple}},
            )

    def get_item_properties(self, guild_id:int) -> list:
        """
        Retrieves the item properties of a guild from the database.

        Args:
            guild_id: The ID of the guild to retrieve the item 
            properties from.

        Returns:
            list: A list containing the item properties of the specified guild.
        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            return found["item_properties"]

    def allow_role_to(self, guild_id:int, function: str, role: str):
        """Allows a role of a guild to perform a specified function.

        Args:
            guild_id: The ID of the guild to be updated.
            function: The function which role can perform.
            role: The role which can perform a function.

        Return:
            None

        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{function}": role}},
            )

    def get_items_id(self):
        """
        Generates a new ID for an item in the guild's database.

        The ID is a string containing a five-digit number, starting with "00001" for the first item.
        If there are no items in the database, the ID of the first item will be "00001".

        Args:
            None.

        Returns:
            str: A five-digit string representing the ID of the next item to be added to the database.

        Example:
            If the guild's database contains two items with IDs "00001" and "00002", calling get_items_id()
            will return "00003", which can be used as the ID of the next item to be added to the database.
        """
        found = self.guild
        if found is not None:
            try:
                if len(found["items"]) == 0:
                    return "1"  # If no items in db, start with 00001
                return int(found["items"][-1]["id"]) + 1
            except:
                return "1"

    def add_item(self, guild_id:int, item:dict):
        """Push an item dictionary into database.

        Args:
            guild_id: The ID of the guild to be updated.
            item: The items dictionary. Dictionary is created with keys 
                of item_properties.

        Return:
            None

        """
        found = self.guild
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$push": {"items": item}},
            )

    def delete_item(self, guild_id:int, item_id:str) -> bool:
        """
        Deletes an item with the specified ID from the guild's database.

        If an item with the specified ID is found in the database, it is removed and the function returns True.
        If no item with the specified ID is found in the database, the function returns False.

        Args:
            guild_id: The ID of the guild to delete the item from.
            item_id: The ID of the item to delete.

        Returns:
            bool: True if an item with the specified ID was found and deleted from the database, False otherwise.

        Example:
            If the guild's database contains an item with ID "00001", calling delete_item(guild_id=1234, item_id="00001")
            will remove the item from the database and return True. If no such item exists in the database, the function
            will return False.
        """
        found = self.guild
        for item in found["items"]:
            if item_id in list(item.values()):
                self.collection_name.update_one(
                    {"_id": guild_id},
                    {"$pull": {"items": {"id": item_id}}},
                )
                return True
        return False

    def get_item(self, id: str, guild_id: int) ->  Union[Dict[str, Any], None]:
        """Returns a dictionary containing the item with the specified ID in the guild with the specified ID.
        If the item is not found, returns `None`.

        Args:
            id: The ID of the item to retrieve.
            guild_id: The ID of the guild to search for the item.

        Returns:
            Union[Dict[str, Any], None]: A dictionary containing the item with the specified ID,
            or `None` if the item is not found.
        """
        found = self.guild_in_database(guild_id)
        items = found["items"]
        for item in items:
            if item["id"] == id:
                return item
        return None

    def delete_all_items(self, guild_id:int):
        """
        Deletes all items from the guild's database.

        Args:
            guild_id: The ID of the guild to delete the item from.
        
        Returns:
            None
        """
        self.collection_name.update_one(
            {"_id": guild_id},
            {"$unset": {"items": ""}},
        )

    def __dict_to_string(self, item_dicts:dict, item_properties:list) -> str:
        """Converts a item_dicts to a string with the format like
                'make model part color'

        Args:
            item_dicts: Dictionary containing items.
            item_properties: List contating item_properites defined for 
                a guild.

        Returns:
            str: String of count words equals of length of item 
                propererties. If multiple words are under on parameter of
                an item. It will include all of them.
            
        """

        converted_string = " ".join(
            [
                f"{value.lower()}"
                for key, value in item_dicts.items()
                if key in item_properties
            ]
        )

        return converted_string
    
    def __compute_similarity(self, search_phrase, db_item):
        similarity = fuzz_test(query=search_phrase, db_item=db_item)
        return similarity

    def __sort_results(
        self, 
        items:List[Dict[str, Any]], 
        similarity_threshold:int, 
        search_phrase:str, 
        item_properties:list
    ):
        """
        Sorts a list of items based on their similarity to a search phrase.

        Args:
            items: A list of dictionaries representing items to search.
            similarity_threshold: The minimum similarity score required 
                to include an item in the results.
            search_phrase: The phrase to search for within the item 
                names.
            item_properties: A list of strings indicating the item 
                properties to use in the search.

        Returns:
            Union[str, List[Dict[str, Any]]]: If no items meet the 
                similarity threshold, returns the string "No items".
                Otherwise, returns a list of dictionaries containing the 
                reverse sorted search results.
            
        """

        leve_sorted_items = {}
        for item in items:
            item_in_db_as_string = self.__dict_to_string(
                item_dicts=item, 
                item_properties=item_properties
                )
            similarity = self.__compute_similarity(
                search_phrase=search_phrase,
                db_item=item_in_db_as_string,
            )
            leve_sorted_items.setdefault(similarity, []).append(item)
        sorted_items = sorted(
           ( (k, v)
            for k, v in leve_sorted_items.items()
            if k >= similarity_threshold)
        , reverse=True)
        if len(sorted_items) == 0:
            return "No items"
        unpacked_list = [
            item for sublist in (v for k, v in sorted_items) for item in sublist
        ]
        return unpacked_list

    def levenshtein_search(self, guild_id:int, search:str) -> Union[str, dict] :
        """
        Searches for an items within users query and sorts them.

        Args:
            guild_id (int): ID of guild.

        Returns:
            str: If no results were find.
            dict: If there are items to show.
        """
        guild = self.collection_name.find({"_id": guild_id})

        if not guild:
            return "No items"
        sorted_items = self.__sort_results(
            items=guild[0]["items"],
            item_properties=guild[0]["item_properties"],
            similarity_threshold=60,
            search_phrase=search,
        )
        return sorted_items
