"""The isobot cog file for the AFK system."""

# Imports
import discord
import json
import os
from discord import option, ApplicationContext, SlashCommandGroup
from discord.ext import commands
from framework.isobot.db.presence import Presence

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"
with open(f"{client_data_dir}/database/presence.json", 'r', encoding="utf-8") as f: presence = json.load(f)
presence = Presence()

# Commands
class PresenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    afk_system = SlashCommandGroup("afk", "Commands for interacting with the AFK system.")

    @afk_system.command(
        name="set",
        description="Sets your AFK status with a custom response"
    )
    @commands.guild_only()
    @option(name="response", description="What do you want your AFK response to be?", type=str, default="I'm AFK")
    async def afk_set(self, ctx: ApplicationContext, response: str="I'm AFK"):
        presence.add_afk(ctx.guild.id, ctx.user.id, response)
        localembed = discord.Embed(title=f"{ctx.author.display_name} is now AFK.", description=f"Response: {response}", color=discord.Color.dark_orange())
        await ctx.respond(embed=localembed)

    @afk_system.command(
        name="remove",
        description="Removes your AFK status"
    )
    @commands.guild_only()
    async def afk_remove(self, ctx: ApplicationContext):
        status = presence.remove_afk(ctx.guild.id, ctx.author.id)
        if status == 0: return await ctx.respond(f"Alright {ctx.author.mention}, I've removed your AFK.")
        elif status == 1: return await ctx.respond("You weren't previously AFK.", ephemeral=True)

    @afk_system.command(
        name="mod_remove",
        description="Removes an AFK status for someone else"
    )
    @commands.guild_only()
    @option(name="user", description="Whose AFK status do you want to remove?", type=discord.User)
    async def afk_mod_remove(self, ctx: ApplicationContext, user:discord.User):
        if not ctx.author.guild_permissions.manage_messages: return await ctx.respond("You don't have the required permissions to use this.", ephemeral=True)
        status = presence.remove_afk(ctx.guild.id, user.id)
        if status == 0: return await ctx.respond(f"{user.display_name}'s AFK has been removed.")
        elif status == 1: return await ctx.respond("That user isn't AFK.", ephemeral=True)

# Cog Initialization
def setup(bot): bot.add_cog(PresenceCog(bot))
