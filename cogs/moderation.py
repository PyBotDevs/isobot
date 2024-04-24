# Imports
import discord
import time
from framework.isobot.db.warnings import Warnings
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
warningsdb = Warnings()

# Commands
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='kick', 
        description='Kicks a member from this server.'
    )
    @option(name="user", description="Who do you want to kick?", type=discord.User)
    @option(name="reason", description="Why do you want to kick the user?", type=str, default=None)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx: ApplicationContext, user, reason=None):
        if not ctx.author.guild_permissions.kick_members: return await ctx.respond('https://tenor.com/view/oh-yeah-high-kick-take-down-fight-gif-14272509')
        else:
            if reason is None: await user.kick()
            else: await user.kick(reason=reason)
            await ctx.respond(embed=discord.Embed(title=f'{user} has been kicked.', description=f'Reason: {str(reason)}'))

    @commands.slash_command(
        name='ban', 
        description='Bans a member from this server.'
    )
    @option(name="user", description="Who do you want to ban?", type=discord.User)
    @option(name="reason", description="Why you want to ban the user?", type=str, default=None)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx: ApplicationContext, user, reason=None):
        if not ctx.author.guild_permissions.ban_members: return await ctx.respond('https://tenor.com/view/thor-strike-admin-ban-admin-ban-gif-22545175')
        else:
            try:
                if reason is None: await user.ban()
                else: await user.ban(reason=reason)
                await ctx.respond(embed=discord.Embed(title=f'{user} has been banned.', description=f'Reason: {str(reason)}'))
            except Exception: await ctx.respond(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

    @commands.slash_command(
        name="warn",
        description="Warns the specified user, with a specific reason."
    )
    @option(name="user", description="Who do you want to warn?", type=discord.Member)
    @option(name="reason", description="The reason why you are warning the user", type=str)
    async def warn(self, ctx: ApplicationContext, user: discord.Member, reason: str):
        """Warns the specified user, with a specific reason."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                """You can't use this command! You need the `Manage Messages` permission to run this.
                If you think this is a mistake, contact your server administrator.""",
                ephemeral=True
            )
        warningsdb.add_warning(ctx.guild.id, user.id, ctx.author.id, round(time.time()), reason)
        warnembed = discord.Embed(
            title=f":warning: You have been warned in **{ctx.guild.name}**",
            description=f"Reason: {reason}",
            color=discord.Color.red()
        )
        await user.send(embed=warnembed)
        localembed = discord.Embed(
            description=f":white_check_mark: **{user.display_name}** has been successfully warned.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="clear_all_warnings",
        description="Clears all the warnings from the specified user."
    )
    @option(name="user", description="The user whose warnings you want to clear.", type=discord.Member)
    async def clear_all_warning(self, ctx: ApplicationContext, user: discord.Member):
        """Clears all the warnings from the specified user."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                """You can't use this command! You need the `Manage Messages` permission to run this.
                If you think this is a mistake, contact your server administrator.""",
                ephemeral=True
            )
        warningsdb.clear_all_warnings(ctx.guild.id, user.id)
        localembed = discord.Embed(
            description=f":white_check_mark: Successfully cleared all server warnings for **{user.display_name}**.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)
# Initialization
def setup(bot): bot.add_cog(Moderation(bot))
