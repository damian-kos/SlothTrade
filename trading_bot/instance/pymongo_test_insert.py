from instance.pymongo_get_database import get_database


class MongoDb:
    def __init__(self):
        self.dbname = get_database()
        self.collection_name = self.dbname["guilds"]

    def guild_in_database(self, guild_id):
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
        #     print(item["items"])
        # for directory in directories:
        # if all(directory.get(key) == value for key, value in conditions.items() if value):
        #     filtered_directories.append(directory)
