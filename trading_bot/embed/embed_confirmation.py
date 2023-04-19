import discord
from pathlib import Path
from embed.embed_message import embed_message


class Confirmation(discord.ui.View):
    def __init__(self, guild_id, found_items):
        super().__init__(timeout=5)
        self.path_to_inv_images = (
            Path("trading_bot") / "cogs" / "inventory" / "inventory_images"
        )
        self.guild_id = guild_id
        self.response = None
        self.items = found_items
        self.current_page = 0
        self.pages = len(self.items)

    async def on_timeout(self):
        self.clear_items()
        await self.response.edit(view=self)

    @discord.ui.button(
        label="Yes", style=discord.ButtonStyle.green, disabled=True
    )
    async def menu1(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(
            embed=embed[0],
            attachments=embed[1],
            view=self,
        )

    @discord.ui.button(label="No", style=discord.ButtonStyle.grey)
    async def menu2(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(
            embed=embed[0],
            attachments=embed[1],
            view=self,
        )
