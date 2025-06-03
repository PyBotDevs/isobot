# Imports
import discord
import os
from api import auth
from framework.isobot.currency import CurrencyAPI
from framework.isobot.db import levelling
from discord import option, ApplicationContext, SlashCommandGroup
from discord.ext import commands

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Framework Module Initialization
currency = CurrencyAPI(f"{client_data_dir}/database/currency.json", f"{client_data_dir}/logs/currency.log")
levelling = levelling.Levelling()

# Bot Superusers List
def fetch_superusers() -> list:
    """Fetches a list of all of the superusers' Discord IDs registered in isobot."""
    return list(auth.get_runtime_options["superusers"])

# Commands
class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    devtools = SlashCommandGroup("devtools", "Developer-only configuration commands for the bot.")

    @devtools.command(
        name='modify_balance',
        description="Modifies user balance. (Normal Digit: Adds Balance; Negative Digit: Removes Balance)"
    )
    @option(name="user", description="Specify the user to change their balance", type=discord.User)
    @option(name="modifier", description="Specify the balance to modify", type=int)
    async def modify_balance(self, ctx: ApplicationContext, user: discord.User, modifier: int):
        """Modifies user balance. (Normal Digit: Adds Balance; Negative Digit: Removes Balance)"""
        if str(ctx.author.id) not in fetch_superusers(): return ctx.respond("This command is usable only by **developers** and **bot superusers**.", ephemeral=True)
        try:
            currency.add(user.id, modifier)
            await ctx.respond(f"{user.name}\'s balance has been modified by {modifier} coins.\n\n**New Balance:** {currency.get_wallet(user.id)} coins", ephemeral=True)
        except KeyError: await ctx.respond("That user doesn't exist in the database.", ephemeral=True)

    @devtools.command(
        name="edit_rank",
        description="Edits a user's rank."
    )
    @option(name="user", description="Who's rank do you want to edit?", type=discord.User)
    @option(name="new_rank", description="The new rank you want to set for the user", type=int)
    async def edit_rank(self, ctx: ApplicationContext, user: discord.User, new_rank: int):
        """Edits a user's rank."""
        if str(ctx.author.id) not in fetch_superusers(): return await ctx.respond("This command is usable only by **developers** and **bot superusers**.", ephemeral=True)
        try:
            levelling.set_level(user.id, new_rank)
            await ctx.respond(f"{user.display_name}\'s rank successfully edited. `New Rank: {levelling.get_level(user.id)}`")
        except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

    @devtools.command(
        name="edit_xp",
        description="Edits a user's XP."
    )
    @option(name="user", description="Who's rank do you want to edit?", type=discord.User)
    @option(name="new_xp", description="The new xp count you want to set for the user", type=int)
    async def edit_xp(self, ctx: ApplicationContext, user: discord.User, new_xp: int):
        """Edits a user's XP."""
        if str(ctx.author.id) not in fetch_superusers(): return await ctx.respond("This command is usable only by **developers** and **bot superusers**.", ephemeral=True)
        try:
            levelling.set_xp(user.id, new_xp)
            await ctx.respond(f"{user.display_name}\'s XP count successfully edited. `New XP: {levelling.get_xp(user.id)}`")
        except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)


# Initialization
def setup(bot):
    bot.add_cog(DevTools(bot))
