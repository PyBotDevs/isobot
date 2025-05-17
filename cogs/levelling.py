"""The isobot cog file for the levelling system."""

# Imports
import discord
import json
from discord import option, ApplicationContext
from discord.ext import commands
from framework.isobot.db import levelling

# Variables
color = discord.Color.random()
levelling = levelling.Levelling()

# Commands
class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="rank",
        description="Shows your rank or another user's rank."
    )
    @option(name="user", description="Who's rank do you want to view?", type=discord.User, default=None)
    async def rank(self, ctx: ApplicationContext, user: discord.User=None):
        """Shows your rank or another user's rank."""
        if user is None: user = ctx.author
        try:
            xpreq = int()
            for level in range(levelling.get_level(ctx.author.id)):
                xpreq += 50
                if xpreq >= 5000: break
            localembed = discord.Embed(title=f"{user.display_name}'s rank", color=color)
            localembed.add_field(name="Level", value=levelling.get_level(user.id))
            localembed.add_field(name="XP", value=f"{levelling.get_xp(user.id)}/{xpreq} gained")
            localembed.set_footer(text="Keep chatting in servers to earn levels!\nYour rank is global across all servers.")
            await ctx.respond(embed=localembed)
        except KeyError: return await ctx.respond("Looks like that user isn't indexed yet. Try again later.", ephemeral=True)

    @commands.slash_command(
        name="leaderboard_levels",
        description="View the global leaderboard for user levelling ranks."
    )
    async def leaderboard_levels(self, ctx: ApplicationContext):
        await ctx.defer()
        levels = levelling.get_raw()
        levels_dict = dict()
        for person in levels:
            levels_dict[str(person)] = levels[str(person)]["level"]
        undicted_leaderboard = sorted(levels_dict.items(), key=lambda x:x[1], reverse=True)
        dicted_leaderboard = dict(undicted_leaderboard)
        parsed_output = str()
        y = 1
        for i in dicted_leaderboard:
            if y < 10:
                try:
                    if levels_dict[i] != 0:
                        user_context = await ctx.bot.fetch_user(i)
                        if not user_context.bot and levels_dict[i] != 0:
                            if y == 1: yf = ":first_place:"
                            elif y == 2: yf = ":second_place:"
                            elif y == 3: yf = ":third_place:"
                            else: yf = f"#{y}"
                            parsed_output += f"{yf} **{user_context.name}:** level {levels_dict[i]}\n"
                            y += 1
                except discord.errors.NotFound: continue
        localembed = discord.Embed(title="Global levelling leaderboard", description=parsed_output, color=color)
        await ctx.respond(embed=localembed)

    # User Commands
    @commands.user_command(name="View Rank")
    async def _view_rank(self, ctx: ApplicationContext, user: discord.User):
        await self.rank(ctx, user)

def setup(bot):
    bot.add_cog(Levelling(bot))
