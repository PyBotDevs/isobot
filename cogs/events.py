# Imports
import discord
from discord import option, ApplicationContext
from discord.ext import commands
from discord.commands import SlashCommandGroup

# Add code for event database here

# Commands
class SpecialEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    special_event = SlashCommandGroup("event", "Commands related to any ongoing special in-game event.")

    @special_event.command(
        name="leaderboard", 
        description="View the global leaderboard for the special in-game event."
    )
    async def leaderboard(self, ctx: ApplicationContext):
        ctx.respond("This event has been concluded! Come back to this command later for new events!", ephemeral=True)

    @special_event.command(
        name="stats",
        description="See your current stats in the special in-game event."
    )
    @option(name="user", description="Who's event stats do you want to view?", type=discord.User, default=None)
    async def stats(self, ctx: ApplicationContext, user: discord.User):
        if user == None: user = ctx.author
        ctx.respond("This event has been concluded! Come back to this command later for new events!", ephemeral=True)

# Initialization
def setup(bot): bot.add_cog(SpecialEvents(bot))
