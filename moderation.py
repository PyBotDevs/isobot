# Imports
import discord
import json
import os.path
from discord.ext import commands
from discord import ApplicationContext, option
from discord.ext.commands.errors import MissingPermissions

# Variables
color = discord.Color.random()
wdir = os.getcwd()

with open(f"{wdir}/database/warnings.json", 'r') as f: warnings = json.load(f)

# Functions
def save():
    with open(f"{wdir}/database/warnings.json", 'w+') as f: json.dump(warnings, f)

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
            try:
                if reason == None: await user.kick()
                else: await user.kick(reason=reason)
                await ctx.respond(embed=discord.Embed(title=f'{user} has been kicked.', description=f'Reason: {str(reason)}'))
            except Exception: await ctx.respond(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

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
                if reason == None: await user.ban()
                else: await user.ban(reason=reason)
                await ctx.respond(embed=discord.Embed(title=f'{user} has been banned.', description=f'Reason: {str(reason)}'))
            except Exception: await ctx.respond(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

    @commands.slash_command(
        name='warn',
        description='Warns someone in your server.'
    )
    @option(name="user", description="Who do you want to warn?", type=discord.User)
    @option(name="reason", description="Why are you warning the user?", type=str)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def warn(self, ctx: ApplicationContext, user, reason):
        if not ctx.author.guild_permissions.manage_messages: raise MissingPermissions
        warnings[str(ctx.guild.id)][str(user.id)].append('reason')
        save()
        target=commands.get_user(user.id)
        try:
            await target.send(embed=discord.Embed(title=f':warning: You\'ve been warned in {ctx.guild} ({ctx.guild.id})', description=f'Reason {reason}'))
            await ctx.respond(embed=discord.Embed(description=f'{user} has been warned.'))
        except Exception: await ctx.respond(embed=discord.Embed(description=f'{user} has been warned. I couldn\'t DM them, but their warning is logged.'))

    @commands.slash_command(
        name='warns_clear',
        description='Clears someone\'s warnings.'
    )
    @option(name="user", description="Who do you want to remove warns from?", type=discord.User)
    async def warns_clear(self, ctx: ApplicationContext, user):
        if not ctx.author.guild_permissions.manage_messages: raise MissingPermissions
        warnings[str(ctx.guild.id)][str(user.id)] = []
        save()
        await ctx.respond(embed=discord.Embed(description=f'All {user}\'s warnings have been cleared.'))

# Cog Initialization
def setup(bot): bot.add_cog(Moderation(bot))
