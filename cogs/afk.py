"""The isobot cog file for the AFK system."""

# Imports
import discord
import json
import time
from discord import option, ApplicationContext, SlashCommandGroup
from discord.ext import commands

# Variables
with open("database/presence.json", 'r') as f: presence = json.load(f)

def save():
    with open("database/presence.json", 'w+') as f: json.dump(presence, f)

# Functions
def get_presence(user_id: int, guild_id: int) -> dict:
    """Returns a `dict` of the specified user's current AFK status in the guild."""
    if str(user_id) in presence[str(guild_id)]:
        return {
            "afk": True, 
            "response": presence[str(guild_id)][str(user_id)]['response'], 
            "time": presence[str(guild_id)][str(user_id)]['time']
        }
    else:
        return False

# Commands
class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    afk_system = SlashCommandGroup("afk", "Commands for interacting with the AFK system.")

    @afk_system.command(
        name="set",
        description="Sets your AFK status with a custom response"
    )
    @option(name="response", description="What do you want your AFK response to be?", type=str, default="I'm AFK")
    async def afk_set(self, ctx: ApplicationContext, response:str="I'm AFK"):
        exctime = time.time()
        if str(ctx.guild.id) not in presence: presence[str(ctx.guild.id)] = {}
        presence[str(ctx.guild.id)][str(ctx.author.id)] = {"type": "afk", "time": exctime, "response": response}
        save()
        localembed = discord.Embed(title=f"{ctx.author.display_name} is now AFK.", description=f"Response: {response}", color=discord.Color.dark_orange())
        await ctx.respond(embed=localembed)

    @afk_system.command(
        name="remove",
        description="Removes your AFK status"
    )
    async def afk_remove(self, ctx: ApplicationContext):
        try:
            del presence[str(ctx.guild.id)][str(ctx.author.id)]
            save()
            await ctx.respond(f"Alright {ctx.author.mention}, I've removed your AFK.")
        except KeyError: return await ctx.respond("You weren't previously AFK.", ephemeral=True)

    @afk_system.command(
        name="mod_remove",
        description="Removes an AFK status for someone else"
    )
    @option(name="user", description="Whose AFK status do you want to remove?", type=discord.User)
    async def afk_mod_remove(self, ctx: ApplicationContext, user:discord.User):
        if not ctx.author.guild_permissions.manage_messages: return await ctx.respond("You don't have the required permissions to use this.", ephemeral=True)
        try:
            del presence[str(ctx.guild.id)][str(user.id)]
            save()
            await ctx.respond(f"{user.display_name}'s AFK has been removed.")
        except KeyError: return await ctx.respond("That user isn't AFK.", ephemeral=True)

# Cog Initialization
def setup(bot): bot.add_cog(Presence(bot))
