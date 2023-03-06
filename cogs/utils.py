# Imports
import discord
import framework.isobot.embedengine
from discord import option, ApplicationContext
from discord.ext import commands
from cogs.economy import get_wallet, get_bank, get_user_networth
from cogs.levelling import get_level, get_xp

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
    
# Cog Initialization
def setup(bot): bot.add_cog(Utils(bot))
