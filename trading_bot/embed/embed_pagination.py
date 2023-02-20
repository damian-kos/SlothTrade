import discord
from pathlib import Path
from embed.embed_message import embed_message


class Pagination(discord.ui.View):
    """Defines a pagination view for displaying a list of items in a Discord embed message.
    The Pagination class is a subclass of discord.ui.View, and it provides two buttons for
    navigating the pages of the list: "Previous" and "Next". Each button triggers a
    corresponding method that updates the current page index and displays the item at the
    new index in an embed message. The embed_message() function from the embed.embed_message
    module is used to generate the embed message based on the item dictionary at the current
    page index.

    Attributes:
        found_items (list): A list of dictionaries representing the items to be paginated.

    Methods:
        on_timeout(self): A coroutine that gets called when the view times out. It clears
            the items from the view and updates the message.
        menu1(self, interaction, button): A coroutine that handles the "Previous" button
            click event. It updates the current page index, disables the button if necessary,
            generates the embed message for the new item, and updates the message.
        menu2(self, interaction, button): A coroutine that handles the "Next" button click
            event. It updates the current page index, disables the button if necessary,
            generates the embed message for the new item, and updates the message.
    """

    def __init__(self, found_items):
        super().__init__(timeout=5)
        self.path_to_inv_images = (
            Path("trading_bot") / "inventory" / "inventory_images"
        )
        self.response = None
        self.items = found_items
        self.current_page = 0
        self.pages = len(self.items)

    async def on_timeout(self):
        self.clear_items()
        await self.response.edit(view=self)

    @discord.ui.button(
        label="Previous", style=discord.ButtonStyle.grey, disabled=True
    )
    async def menu1(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page -= 1
        if self.current_page == 0:
            button.disabled = True
        self.children[-1].disabled = False
        current_item_dict = self.items[self.current_page]

        embed = embed_message(
            item_id=current_item_dict["id"],
            image_path=self.path_to_inv_images,
            item_dict=current_item_dict,
        )

        await interaction.response.edit_message(
            content=f"{current_item_dict}",
            embed=embed[0],
            attachments=embed[1],
            view=self,
        )

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def menu2(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page += 1
        if self.current_page == self.pages - 1:
            button.disabled = True
        self.children[0].disabled = False
        current_item_dict = self.items[self.current_page]
        print(current_item_dict)

        embed = embed_message(
            item_id=current_item_dict["id"],
            image_path=self.path_to_inv_images,
            item_dict=current_item_dict,
        )

        await interaction.response.edit_message(
            content=f"{current_item_dict}",
            embed=embed[0],
            attachments=embed[1],
            view=self,
        )
