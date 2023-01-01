# Contains the source code used for the isobot New Years 2022 in-game special event. 

# Dummy imports
import asyncio
import discord
import framework.isobot.colors
from random import randint
from math import floor
import time
import json
from discord import ApplicationContext, option

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

# Commands
special_event = client.create_group("event", "Commands related to the New Years special in-game event.")

@special_event.command(
    name="leaderboard", 
    description="View the global leaderboard for the special in-game event."
)
async def leaderboard(ctx: ApplicationContext):
    undicted_leaderboard = sorted(presents.items(), key=lambda x:x[1], reverse=True)
    dicted_leaderboard = dict(undicted_leaderboard)
    parsed_output = str()
    y = 1
    for i in dicted_leaderboard:
        if y < 10:
            try:
                if presents[i] != 0:
                    user_context = await client.fetch_user(i)
                    if not user_context.bot and presents[i] != 0:
                        print(i, presents[i])
                        if y == 1: yf = ":first_place:"
                        elif y == 2: yf = ":second_place:"
                        elif y == 3: yf = ":third_place:"
                        else: yf = f"#{y}"
                        parsed_output += f"{yf} **{user_context.name}:** {presents[i]} presents\n"
                        y += 1
            except discord.errors.NotFound: continue
    localembed = discord.Embed(title="New Years Special Event global leaderboard", description=parsed_output, color=color)
    await ctx.respond(embed=localembed)

@special_event.command(
    name="stats",
    description="See your current stats in the special in-game event."
)
@option(name="user", description="Who's event stats do you want to view?", type=discord.User, default=None)
async def stats(ctx: ApplicationContext, user: discord.User):
    if user == None: user = ctx.author
    localembed = discord.Embed(title=f"{user.display_name}'s New Years Special Event stats", description="Event ends on **1st January 2023**.", color=color)
    localembed.add_field(name=":gift: Presents", value=presents[str(user.id)], inline=True)
    await ctx.respond(embed=localembed)
