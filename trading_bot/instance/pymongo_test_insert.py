from instance.pymongo_get_database import get_database
from .levenshtein_algorithm import levenshtein_similarity


class MongoDb:
    def __init__(self):
        self.dbname = get_database()
        self.collection_name = self.dbname["guilds"]

    def guild_in_database(self, guild_id):
        """
        Sets the guild attribute to the result of a MongoDB find_one query for a guild with the given ID.

        Args:
            guild_id (int): ID of guild.

        Returns:
            None. The method assigns the result of the query to the self.guild attribute.
        """
        self.guild = self.collection_name.find_one({"_id": guild_id})

    def insert_guild(self, guild_id, guild_name, guild_system_channel):
        guild = {
            "_id": guild_id,
            "guild_name": guild_name,
            "guild_system_channel": guild_system_channel,
        }
        self.collection_name.insert_one(guild)

    def delete_guild(self, guild_id):
        guild = {
            "_id": guild_id,
        }
        self.collection_name.delete_one(guild)

    def set_channel(self, guild_id, channel_id, channel_type=""):
        found = self.collection_name.find_one({"_id": guild_id})
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$set": {f"{channel_type}_channel": channel_id}},
            )

    def get_items_id(self, guild_id):
        found = self.collection_name.find_one({"_id": guild_id})
        try:
            return int(found["items"][-1]["id"]) + 1
        except KeyError:
            return "1"
        except IndexError:
            return "1"

    def add_item(self, guild_id, item):
        found = self.collection_name.find_one({"_id": guild_id})
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$push": {"items": item}},
            )

    def delete_item(self, guild_id, item_id):
        found = self.collection_name.find_one({"_id": guild_id})
        if found is not None:
            self.collection_name.update_one(
                {"_id": guild_id},
                {"$pull": {"items": {"id": item_id}}},
            )

    def search_item(self, guild_id, search_dict):
        items = self.collection_name.find({"_id": guild_id})
        sorted_items = []
        for item in items[0]["items"]:
            match = True
            for key, value in search_dict.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                sorted_items.append(item)
        if len(sorted_items) == 0:
            return "No items"
        return sorted_items

    def __dict_to_string(self, dictionary):
        """
        Converts a dictionary to a string with the format 'make model part color description price'
        """
        return (
            f"{dictionary['make'].lower()} {dictionary['model']} "
            f"{dictionary['part'].lower()} {dictionary['color'].lower()} "
        )

    def read_models(self):
        with open("trading_bot\instance\models.txt", "r") as file:
            self.models = [word.replace("\n", "") for word in file.readlines()]

    def levenshtein_search(self, guild_id, search):
        self.read_models()
        leve_sorted_items = {}
        items = self.collection_name.find({"_id": guild_id})
        if not items:
            return "No items"

        for item in items[0]["items"]:
            item_in_db_as_string = self.__dict_to_string(item)
            similarity = levenshtein_similarity(
                search_phrase=search, db_item=item_in_db_as_string
            )

            for model in self.models:
                if model in search and model in item_in_db_as_string:
                    similarity -= 5
            leve_sorted_items.setdefault(similarity, []).append(item)
        sorted_items = sorted(
            (k, v) for k, v in leve_sorted_items.items() if k <= 15
        )
        if len(sorted_items) == 0:
            return "No items"
        unpacked_list = [
            item for sublist in (v for k, v in sorted_items) for item in sublist
        ]
        return unpacked_list
