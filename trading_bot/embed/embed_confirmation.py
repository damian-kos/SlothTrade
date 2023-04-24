import discord
from pathlib import Path
from embed.embed_message import embed_message


class Confirmation(discord.ui.View):
    def __init__(self):
        super().__init__()
        # super().__init__(timeout=5)

        self.response = None

        self.value = None

    # async def on_timeout(self):
    #     self.clear_items()
    #     await self.response.edit(view=self)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def menu1(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.message.delete()
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.grey)
    async def menu2(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.message.delete()
        self.value = False
        self.stop()
