# Imports
import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from framework.isobot.db import serverconfig

# Variables
serverconf = serverconfig.ServerConfig()

# Functions
class ServerConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    serverconfig_cmds = SlashCommandGroup(name="serverconfig", description="Commands related to server customization and configuration.")

    @serverconfig_cmds.command(
        name="autorole",
        description="Set a role to provide to all newly-joined members of the server."
    )
    @option(name="role", description="The role that you want to automatically give to all new members.", type=discord.Role, default=None)
    async def autorole(self, ctx: ApplicationContext, role: discord.Role = None):
        """Set a role to provide to all newly-joined members of the server."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        if role != None:
            serverconf.set_autorole(ctx.guild.id, role.id)
            localembed = discord.Embed(
                title=f":white_check_mark: Autorole successfully set for **{ctx.guild.name}**!",
                description=f"From now onwards, all new members will receive the {role.mention} role.",
                color=discord.Color.green()
            )
        else:
            serverconf.set_autorole(ctx.guild.id, None)
            localembed = discord.Embed(
                title=f":white_check_mark: Autorole successfully disabled for **{ctx.guild.name}**",
                description="New members will not automatically receive any roles anymore.",
                color=discord.Color.green()
            )
        await ctx.respond(embed=localembed)

def setup(bot):
    bot.add_cog(ServerConfig(bot))
    