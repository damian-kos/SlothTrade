from instance.pymongo_get_database import get_database
from .levenshtein_algorithm import fuzz_test


class MongoDb:
    def __init__(self):
        """
        A class for accessing a MongoDB database containing information
        about guilds and their items.

        Attributes:
            dbname (pymongo.database.Database): The database to connect
            to.
            collection_name (pymongo.collection.Collection):
            The collection within the database to interact with.

        Methods:
            guild_in_database(guild_id):
                Returns the result of a MongoDB find_one query for
                a guild with the given ID.

            insert_guild(guild_id, guild_name, guild_system_channel):
                Inserts a new guild with the given ID, name, and
                system channel into the collection.

            delete_guild(guild_id):
                Deletes the guild with the given ID from the collection.

            set_channel(guild_id, channel_id, channel_type=""):
                Sets the system or voice channel ID of the guild with the
                  given ID in the collection.

            get_items_id(guild_id):
                Returns the ID of the next item to be added to the guild
                with the given ID.

            add_item(guild_id, item):
                Adds a new item to the guild with the given ID in the
                collection.

            delete_item(guild_id, item_id):
                Deletes the item with the given ID from the guild with
                the given ID in the collection.

            __compute_similarity(search_phrase, db_item, models):
                Computes the Levenshtein similarity between a search
                phrase and an item in the database.

            sort_results(items, similarity_threshold, search_phrase):
                Sorts a list of items by Levenshtein similarity to
                a search phrase and by model priority.

            levenshtein_search(guild_id, search):
                Searches for items within a guild using a Levenshtein
                algorithm and returns them sorted by similarity to the search phrase.


        """
        self.dbname = get_database()
        self.collection_name = self.dbname["guilds"]

    def guild_in_database(self, guild_id: int):
        """
        Sets the guild attribute to the result of a MongoDB find_one
        query for a guild with the given ID.

        Args:
            guild_id (int): ID of guild.

        Returns:
            The result of the query as a dictionary, or None if no guild
            is found.
        """
        self.guild = self.collection_name.find_one({"_id": guild_id})
        return self.guild

    def insert_guild(
        self, guild_id: int, guild_name: str, guild_system_channel: int
    ):
        """
        Inserts a new guild into the MongoDB.

        Args:
            guild_id (int): ID of guild.
            guild_name (str): Name of guild.
            guild_system_channel (int): ID of system channel.

        Returns:
            None
        """
        guild_info = {
            "_id": guild_id,
            "guild_name": guild_name,
            "guild_system_channel": guild_system_channel,
        }
        self.collection_name.insert_one(guild_info)

    def delete_guild(self, guild_id: int):
        """
        Deletes a guild from the MongoDB.

        Args:
            guild_id (int): ID of guild.

        Returns:
            None
        """
        guild = {
            "_id": guild_id,
        }
        self.collection_name.delete_one(guild)

    def set_channel(self, guild_id, channel_id, channel_type=""):
        """
        Sets the channel attribute of a guild in the MongoDB.

        Args:
            guild_id (int): ID of guild.
            channel_id (int): ID of channel to set.
            channel_type (str): Type of channel to set.

        Returns:
            None
        """
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{channel_type}": channel_id}},
            )

    def define_item_properties(self, guild_id, item_properties_tuple):
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"item_properties": item_properties_tuple}},
            )

    def get_item_properties(self, guild_id):
        found = self.guild_in_database(guild_id)
        if found is not None:
            return found["item_properties"]

    def allow_role_to(self, guild_id, function: str, role: str):
        found = self.guild_in_database(guild_id)
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{function}": role}},
            )

    def get_items_id(self):
        """
        Gets the ID for the next item to be added to the MongoDB.

        Args:
            guild_id (int): ID of guild.

        Returns:
            int: The next item ID, or "1" if no items are found.
        """
        found = self.guild
        if found is not None:
            if len(found["items"]) == 0:
                return "1"  # If no items in db, start with 00001
            return int(found["items"][-1]["id"]) + 1

    def add_item(self, guild_id, item):
        """
        Adds an item to the MongoDB.

        Args:
            guild_id (int): ID of guild.
            item (dict): The item to add.

        Returns:
            None
        """
        found = self.guild
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$push": {"items": item}},
            )

    def delete_item(self, guild_id, item_id):
        """
        Deletes an item from the MongoDB.

        Args:
            guild_id (int): ID of guild.
            item_id (int): ID of item to delete.

        Returns:
            None
        """
        found = self.guild
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$pull": {"items": {"id": item_id}}},
            )

    def __dict_to_string(self, dictionary, item_properties):
        """
        Converts a dictionary to a string with the format 'make model part color description price'
        """
        return " ".join(
            [
                f"{value.lower()}"
                for key, value in dictionary.items()
                if key in item_properties
            ]
        )

    def __compute_similarity(self, search_phrase, db_item):
        similarity = fuzz_test(query=search_phrase, db_item=db_item)
        return similarity

    def __sort_results(
        self, items, similarity_threshold, search_phrase, item_properties
    ):
        leve_sorted_items = {}
        for item in items:
            item_in_db_as_string = self.__dict_to_string(item, item_properties)
            similarity = self.__compute_similarity(
                search_phrase=search_phrase,
                db_item=item_in_db_as_string,
            )
            leve_sorted_items.setdefault(similarity, []).append(item)
        sorted_items = sorted(
            (k, v)
            for k, v in leve_sorted_items.items()
            if k >= similarity_threshold
        )
        if len(sorted_items) == 0:
            return "No items"
        unpacked_list = [
            item for sublist in (v for k, v in sorted_items) for item in sublist
        ]
        return unpacked_list

    def levenshtein_search(self, guild_id, search):
        """
        Searches for an items within users query and sorts them. Prioritizes items included in .txt file.

        Args:
            guild_id (int): ID of guild.

        Returns:
            str: If no results were find.
            dict: If there are items to show.
        """
        items = self.collection_name.find({"_id": guild_id})

        if not items:
            return "No items"
        sorted_items = self.__sort_results(
            items=items[0]["items"],
            item_properties=items[0]["item_properties"],
            similarity_threshold=60,
            search_phrase=search,
        )
        return sorted_items
