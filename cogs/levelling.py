"""The isobot cog file for the levelling system."""

# Imports
import discord
import json
import os.path
import framework.isobot.db.Levels
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
wdir = os.getcwd()
color = discord.Color.random()
levels = framework.isobot.db.Levels(f"{wdir}/database/levels.json", None)

# with open(f"{wdir}/database/levels.json", 'r', encoding="utf-8") as f: levels = json.load(f)

# def save():
#     with open(f"{wdir}/database/levels.json", 'w+', encoding="utf-8") as f: json.dump(levels, f, indent=4)

# Functions
# def get_xp(id: int) -> int:
#     return levels[str(id)]["xp"]

# def get_level(id: int) -> int:
#     return levels[str(id)]["level"]

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
        if user is None: user = ctx.author
        try:
            localembed = discord.Embed(title=f"{user.display_name}'s rank", color=color)
            localembed.add_field(name="Level", value=levels.get_level(user.id))
            localembed.add_field(name="XP", value=levels.get_xp(user.id))
            localembed.set_footer(text="Keep chatting to earn levels!")
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
            levels.edit_level(user.id) = new_rank
            await ctx.respond(f"{user.display_name}\'s rank successfully edited. `New Rank: {levels.get_level(user.id)}`")
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
            levels.edit_xp(user.id) = new_xp
            await ctx.respond(f"{user.display_name}\'s XP count successfully edited. `New XP: {levels.get_xp(user.id)}`")
        except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

    @commands.slash_command(
        name="leaderboard_levels", 
        description="View the global leaderboard for user levelling ranks."
    )
    async def leaderboard_levels(self, ctx: ApplicationContext):
        levels_dict = dict()
        for person in levels:
            levels_dict[str(person)] = levels.get_level(person)
        undicted_leaderboard = sorted(levels_dict.items(), key=lambda x:x[1], reverse=True)
        dicted_leaderboard = dict(undicted_leaderboard)
        parsed_output = str()
        y = 1
        for i in dicted_leaderboard:
            if y < 10:
                try:
                    if levels_dict[i] != 0:
                        user_context = await commands.fetch_user(i)
                        if not user_context.bot and levels_dict[i] != 0:
                            print(i, levels_dict[i])
                            if y == 1: yf = ":first_place:"
                            elif y == 2: yf = ":second_place:"
                            elif y == 3: yf = ":third_place:"
                            else: yf = f"#{y}"
                            parsed_output += f"{yf} **{user_context.name}:** level {levels_dict[i]}\n"
                            y += 1
                except discord.errors.NotFound: continue
        localembed = discord.Embed(title="Global levelling leaderboard", description=parsed_output, color=color)
        await ctx.respond(embed=localembed)

def setup(bot):
    bot.add_cog(Levelling(bot))
