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

## Usage

After bot will be invited it will send a message to first channel he has permissions to message to:

![image](https://user-images.githubusercontent.com/106775028/236808147-8e38eef2-76c0-41cf-be93-17343c5bef5c.png)

From that point you can setup a bot with `/settings` command. This command will work only on server's system channel.

##  Settings command
- `/settings`
This command will return avaiable settings options. 

![image](https://user-images.githubusercontent.com/106775028/236813472-9355a37b-b836-4755-ae1a-b8a6a6fb5c13.png)

We can use one of this listed options to get detailed info about the option. 
Let's use `logging`

- `/settings [option]`

![image](https://user-images.githubusercontent.com/106775028/236813421-a8c7e468-99b1-43ce-b74f-c632ac6fb974.png)

Last thing we can use with `/settings [option]` is a parameter hinted in previous message. We will use `general` as a channel's name.

- `/settings [option] [parameter]`
We will get a confirmation prompt. After confirmation chosen setting will be updated.

![image](https://user-images.githubusercontent.com/106775028/236813948-11a210d0-5ebd-4f90-bb01-3d4c65089194.png)

After confirmation messages can be send:
One will be always send on server's system channel.

![image](https://user-images.githubusercontent.com/106775028/236810318-aff97e17-1f12-454d-b11d-b95c9c60c832.png)

Other will be send if setup `logging` option. This will be sending logs about changes to options.

![image](https://user-images.githubusercontent.com/106775028/236810494-9ac70d8f-8731-4d1d-a10f-9f6124d19413.png)

- **Note:**
    This message is send by `Trading Logging` webhook. `Trading Listing` `Trading Search` `Trading Selling` will be created during setup as well.

## Other commands
- `/remove`
    - `/remove 00017` 
        - Accepts ID  `00001` and `99999`. Leading zeros are necessary. Each item listed on each server once posted will also have it's own unique ID. 
    - `/remove everything`
        - Accepts keyword `everything`. This can be activated only by server members with `Manage Server` permission. Confirmation message will be send first.
 
- `/search`
    - `/search very cool thing`
        - Accepts any sentence.

## Sell slash command
This command is created by `/settings item_properties`, use this function to get detailed information about it's usage.
- `/settings item_properties`
    - `/settings item_properties - title:Title of a book? - year:Release year?`
        - This will create a item property with it's description. Both, property and description are necessary. It accepts up to **4** `property:description` pairs.
        - `-` between pairs are necessary.
        - **Note** `price` property doesn't need to be created because it will be always created.
        - ![image](https://user-images.githubusercontent.com/106775028/236825732-640564cd-5b1f-4294-aa07-9887133986e8.png)


After this command will run your slash command will be activated. If you setup logging beforhand it will let you know once command would be activated.
        
     





