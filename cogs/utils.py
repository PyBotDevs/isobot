# Imports
import discord
import os
import psutil
import math
import framework.isobot.embedengine
from discord import option, ApplicationContext
from discord.ext import commands
from cogs.economy import get_wallet, get_bank, get_user_networth, get_user_count
from cogs.levelling import get_level, get_xp
from cogs.afk import get_presence

# Variables
color = discord.Color.random()

# Commands
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='echo',
        description='Sends a bot message in the channel'
    )
    @option(name="text", description="What do you want to send?", type=str)
    async def echo(self, ctx: ApplicationContext, text:str):
        await ctx.respond("Echoed!", ephemeral=True)
        await ctx.channel.send(text)

    @commands.slash_command(
        name="repo",
        description="Shows the open-source code links for isobot."
    )
    async def repo(self, ctx: ApplicationContext):
        localembed = discord.Embed(title="Source-code Repositories", description="See and contribute to **isobot's [GitHub repository](https://github.com/PyBotDevs/isobot)**\nSee our **[GitHub organization](https://github.com/PyBotDevs)**", color=color)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="embedbuilder",
        description="Builds a custom embed however you want"
    )
    @option(name="title", description="The title of the embed", type=str)
    @option(name="description", description="The body of the embed", type=str)
    @option(name="image_url", description="The main image you want to show for the embed (URL ONLY)", type=str, default=None)
    @option(name="thumbnail_url", description="The thumbnail image you want to show for the embed (URL ONLY)", type=str, default=None)
    @option(name="color", description="The embed's accent color (Use -1 for random color)", type=int, default=None)
    @option(name="footer_text", description="The text at the footer of the embed", type=str, default=None)
    @option(name="footer_icon_url", description="The icon you want to show in the embed's footer (URL ONLY)", type=str, default=None)
    async def embedbuilder(self, ctx: ApplicationContext, title: str, description: str, image_url: str = None, thumbnail_url: str = None, color: int = None, footer_text: str = None, footer_icon_url: str = None):
        await ctx.respond("Embed Built!", ephemeral=True)
        await ctx.channel.send(embed=framework.isobot.embedengine.embed(title, description, image=image_url, thumbnail=thumbnail_url, color=color, footer_text=footer_text, footer_img=footer_icon_url))

    @commands.slash_command(
        name='whoami',
        description='Shows information on a user'
    )
    @option(name="user", description="Who do you want to know about?", type=discord.User, default=None)
    async def whoami(self, ctx: ApplicationContext, user: discord.User=None):
        if user == None: user = ctx.author
        username = user
        displayname = user.display_name
        registered = user.joined_at.strftime("%b %d, %Y, %T")
        pfp = user.avatar
        localembed_desc = f"`AKA` {displayname}"
        presence = get_presence(ctx.author.id, ctx.guild.id)
        if presence != False: localembed_desc += f"\n`🌙 AFK` {presence['response']} - <t:{math.floor(presence['time'])}>"
        localembed = discord.Embed(
            title=f'User Info on {username}',
            description=localembed_desc
        )
        localembed.set_thumbnail(url=pfp)
        localembed.add_field(name='Username', value=username, inline=True)
        localembed.add_field(name='Display Name', value=displayname, inline=True)
        localembed.add_field(name='Joined Discord on', value=registered, inline=False)
        localembed.add_field(name='Avatar URL', value=f"[here!]({pfp})", inline=True)
        role_render = ""
        for p in user.roles:
            if p != user.roles[0]: role_render += f"<@&{p.id}> "
        localembed.add_field(name='Roles', value=role_render, inline=False)
        localembed.add_field(name="Net worth", value=f"{get_user_networth(user.id)} coins", inline=False)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="profile",
        description="Shows basic stats about your isobot profile, or someone else's profile stats"
    )
    @option(name="user", description="Whose isobot profile do you want to view?", type=discord.User, default=None)
    async def profile(self, ctx: ApplicationContext, user: discord.User = None):
        if user == None: user = ctx.author
        localembed = discord.Embed(title=f"{user.display_name}'s isobot stats", color=color)
        localembed.set_thumbnail(url=user.avatar)
        localembed.add_field(name="Level", value=f"Level {get_level(user.id)} ({get_xp(user.id)} XP)", inline=False)
        localembed.add_field(name="Balance in Wallet", value=f"{get_wallet(user.id)} coins", inline=True)
        localembed.add_field(name="Balance in Bank Account", value=f"{get_bank(user.id)} coins", inline=True)
        localembed.add_field(name="Net-Worth", value=f"{get_user_networth(user.id)} coins", inline=True)
        # More stats will be added later
        # Maybe I should make a userdat system for collecting statistical data to process and display here, coming in a future update.
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="status",
        description="Shows the current client info"
    )
    async def status(self, ctx: ApplicationContext):
        os_name = os.name
        sys_ram = str(f"{psutil.virtual_memory()[2]}GiB")
        sys_cpu = str(f"{psutil.cpu_percent(1)}%")
        bot_users = get_user_count()
        localembed = discord.Embed(title="Client Info")
        localembed.add_field(name="OS Name", value=os_name)
        localembed.add_field(name="RAM Available", value=sys_ram)
        localembed.add_field(name="CPU Usage", value=sys_cpu)
        localembed.add_field(name="Registered Users", value=f"{bot_users} users", inline=True)
        localembed.add_field(name="Uptime History", value="[here](https://stats.uptimerobot.com/PlKOmI0Aw8)")
        localembed.add_field(name="Release Notes", value="[latest](https://github.com/PyBotDevs/isobot/releases/latest)")
        localembed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.respond(embed=localembed)

# Cog Initialization
def setup(bot): bot.add_cog(Utils(bot))
