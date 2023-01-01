# Contains the source code used for the isobot New Years 2022 in-game special event. 

# Dummy imports
import asyncio
import discord
import framework.isobot.colors
from random import randint
from math import floor
import time
import json

colors = framework.isobot.colors.Colors()
client = discord.Bot()
color = discord.Color.random()

with open("database/special/new_years_2022.json", 'r') as f: presents = json.load(f)

def save():
    with open("database/special/new_years_2022.json", 'w+') as f: json.dump(presents, f)

# Discord UI Views
class PresentsDrop(discord.ui.View):
    @discord.ui.button(label="🎁 Collect Presents", style=discord.ButtonStyle.blurple)
    async def receive(self, button: discord.ui.Button, interaction: discord.Interaction):
        presents_bounty = randint(500, 1000)
        presents[str(interaction.user.id)] += presents_bounty
        save()
        button.disabled = True
        button.label = f"Presents Collected!"
        button.style = discord.ButtonStyle.grey
        newembed = discord.Embed(description=f"{interaction.user.name} collected **{presents_bounty} :gift: presents** from this drop!", color=discord.Color.green())
        await interaction.response.edit_message(embed=newembed, view=self)

async def on_ready():
    print("[main/Presents] Presents daemon started.")
    while True:
        print(f"[main/Presents] Dropping new presents in {colors.cyan}#general{colors.end} channel...")
        await asyncio.sleep(randint(450, 600))
        if floor(time.time()) > 1672511400:
            cyberspace_channel_context = await client.fetch_channel(880409977074888718)
            localembed = discord.Embed(title="**:gift: Presents have dropped in chat!**", description="Be the first one to collect them!", color=color)
            await cyberspace_channel_context.send(embed=localembed, view=PresentsDrop())


