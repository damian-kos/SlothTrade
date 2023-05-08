# SlothTrade

Sloth Trade is a discord bot that uses [Rapptz's discord.py](https://github.com/Rapptz/discord.py). It allows to create your own item listing system where you and your server users can list items to sell or offer.

## Features

- Custom item properies. 
- Custom `/sell` app command.
- Remove items from database.
- Role assigning to determine who `can_sell` `can_remove` `can_search`
- Channels assigning `sell_channel` `remove_channel` `listing_channel` `search_channel`
- Searching feature
- Listings supports images

### Usage

After bot will be invited it will send a message to first channel he has permissions to message to:

![image](https://user-images.githubusercontent.com/106775028/236808147-8e38eef2-76c0-41cf-be93-17343c5bef5c.png)

From that point you can setup a bot with `/settings` command. This command will work only on server's system channel.

####  `/settings` 
This command will return avaiable settings options.

![image](https://user-images.githubusercontent.com/106775028/236808542-fb748f51-cb97-460c-bbeb-6e07e495da93.png)

We can use one of this listed options to get detailed info about the option. 
Let's use `logging`

#####  `/settings logging`

![image](https://user-images.githubusercontent.com/106775028/236809449-382dc395-165d-4b13-9625-c6baadf26cd0.png)

Last thing we can use with `/settings [option]` is a parameter hinted in previous message. We will use `general` as a channel's name.

######  `/settings logging general`
We will get a confirmation prompt. After confirmation chosen setting will be updated.

![image](https://user-images.githubusercontent.com/106775028/236809963-ce96c23d-1527-4764-9926-cb3c876b8fce.png)


