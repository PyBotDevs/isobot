# Imports
import discord
from discord import option, ApplicationContext
from discord.ext import commands

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

# Initialization
def setup(bot): bot.add_cog(Moderation(bot))
