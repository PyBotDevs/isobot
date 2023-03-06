"""The isobot cog file for the levelling system."""

# Imports
import discord
import json
import os.path
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
wdir = os.getcwd()
color = discord.Color.random()

with open(f"{wdir}/database/levels.json", 'r') as f: levels = json.load(f)

def save():
    with open(f"{wdir}/database/levels.json", 'w+') as f: json.dump(levels, f, indent=4)

# Functions
def get_xp(id: int) -> int:
    return levels[str(id)]["xp"]

def get_level(id: int) -> int:
    return levels[str(id)]["level"]

# Commands
class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="rank",
        description="Shows your rank or another user's rank"
    )
    @option(name="user", description="Who's rank do you want to view?", type=discord.User, default=None)
    async def rank(self, ctx: ApplicationContext, user:discord.User=None):
        if user == None: user = ctx.author
        try:
            localembed = discord.Embed(title=f"{user.display_name}'s rank", color=color)
            localembed.add_field(name="Level", value=levels[str(user.id)]["level"])
            localembed.add_field(name="XP", value=levels[str(user.id)]["xp"])
            localembed.set_footer(text="Keep chatting to earn levels!", icon_url=ctx.author.avatar_url)
            await ctx.respond(embed = localembed)
        except KeyError: return await ctx.respond("Looks like that user isn't indexed yet. Try again later.", ephemeral=True)

    @commands.slash_command(
        name="edit_rank",
        description="Edits a user's rank. (DEV ONLY)"
    )
    @option(name="user", description="Who's rank do you want to edit?", type=discord.User)
    @option(name="new_rank", description="The new rank you want to set for the user", type=int)
    async def edit_rank(self, ctx: ApplicationContext, user:discord.User, new_rank:int):
        if ctx.author.id != 738290097170153472: return await ctx.respond("This command isn't for you.", ephemeral=True)
        try:
            levels[str(user.id)]["level"] = new_rank
            await ctx.respond(f"{user.display_name}\'s rank successfully edited. `New Rank: {levels[str(user.id)]['level']}`")
        except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

    @commands.slash_command(
        name="edit_xp",
        description="Edits a user's XP. (DEV ONLY)"
    )
    @option(name="user", description="Who's rank do you want to edit?", type=discord.User)
    @option(name="new_xp", description="The new xp count you want to set for the user", type=int)
    async def edit_xp(self, ctx: ApplicationContext, user:discord.User, new_xp:int):
        if ctx.author.id != 738290097170153472: return await ctx.respond("This command isn't for you.", ephemeral=True)
        try:
            levels[str(user.id)]["xp"] = new_xp
            await ctx.respond(f"{user.display_name}\'s XP count successfully edited. `New XP: {levels[str(user.id)]['xp']}`")
        except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

def setup(bot):
    bot.add_cog(Levelling(bot))
