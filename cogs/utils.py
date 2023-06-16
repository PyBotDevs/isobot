"""The isobot cog file for utility commands."""

# Imports
import discord
import os
import psutil
import math
import openai
import framework.isobot.embedengine
import framework.isobot.currency
from discord import option, ApplicationContext
from discord.ext import commands
from cogs.levelling import get_level, get_xp
from cogs.afk import get_presence

# Variables
color = discord.Color.random()
currency = framework.isobot.currency.CurrencyAPI("database/currency.json", "logs/currency.log")
openai.api_key = os.getenv("chatgpt_API_KEY")
chatgpt_conversation = dict()

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
        if user is None: user = ctx.author
        username = user
        displayname = user.display_name
        registered = user.joined_at.strftime("%b %d, %Y, %T")
        pfp = user.avatar
        localembed_desc = f"`AKA` {displayname}"
        presence = get_presence(ctx.author.id, ctx.guild.id)
        if presence is not False: localembed_desc += f"\n`🌙 AFK` {presence['response']} - <t:{math.floor(presence['time'])}>"
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
        localembed.add_field(name="Net worth", value=f"{currency.get_user_networth(user.id)} coins", inline=False)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="profile",
        description="Shows basic stats about your isobot profile, or someone else's profile stats"
    )
    @option(name="user", description="Whose isobot profile do you want to view?", type=discord.User, default=None)
    async def profile(self, ctx: ApplicationContext, user: discord.User = None):
        if user is None: user = ctx.author
        localembed = discord.Embed(title=f"{user.display_name}'s isobot stats", color=color)
        localembed.set_thumbnail(url=user.avatar)
        localembed.add_field(name="Level", value=f"Level {get_level(user.id)} ({get_xp(user.id)} XP)", inline=False)
        localembed.add_field(name="Balance in Wallet", value=f"{currency.get_wallet(user.id)} coins", inline=True)
        localembed.add_field(name="Balance in Bank Account", value=f"{currency.get_bank(user.id)} coins", inline=True)
        localembed.add_field(name="Net-Worth", value=f"{currency.get_user_networth(user.id)} coins", inline=True)
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
        bot_users = currency.get_user_count()
        localembed = discord.Embed(title="Client Info")
        localembed.add_field(name="OS Name", value=os_name)
        localembed.add_field(name="RAM Available", value=sys_ram)
        localembed.add_field(name="CPU Usage", value=sys_cpu)
        localembed.add_field(name="Registered Users", value=f"{bot_users} users", inline=True)
        localembed.add_field(name="Uptime History", value="[here](https://stats.uptimerobot.com/PlKOmI0Aw8)")
        localembed.add_field(name="Release Notes", value="[latest](https://github.com/PyBotDevs/isobot/releases/latest)")
        localembed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="chatgpt",
        description="Talk to ChatGPT and get a response back."
    )
    @option(name="message", description="What do you want to send to ChatGPT?", type=str)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def chatgpt(self, ctx: ApplicationContext, message: str):
        if str(ctx.author.id) not in chatgpt_conversation: chatgpt_conversation[str(ctx.author.id)] = [{"role": "system", "content": "You are a intelligent assistant."}]
        await ctx.defer()
        try:
            chatgpt_conversation[str(ctx.author.id)].append({"role": "user", "content": message})
            _chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chatgpt_conversation[str(ctx.author.id)])
            _reply = _chat.choices[0].message.content
            chatgpt_conversation[str(ctx.author.id)].append({"role": "assistant", "content": _reply})
        except openai.error.RateLimitError: return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
        except openai.error.ServiceUnavailableError: return await ctx.respond("The ChatGPT service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
        except openai.error.APIError: return await ctx.respond("ChatGPT encountered an internal error. Please try again.", ephemeral=True)
        except openai.error.Timeout: return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
        localembed = discord.Embed(description=f"{_reply}", color=discord.Color.random())
        localembed.set_author(name="ChatGPT", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
        localembed.set_footer(text="Powered by OpenAI")
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="generate_image",
        description="Generate an image of your choice using the DALL-E modal."
    )
    @option(name="prompt", description="What image do you want the bot to generate?", type=str)
    @option(name="resolution", description="Set a custom resolution for your generated image", type=str, default="512x512", choices=["256x256", "512x512", "1024x1024"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def generate_image(self, ctx: ApplicationContext, prompt: str, resolution: str = "512x512"):
        parsed_resolution: list = resolution.split("x")
        max_index: int = 0
        for index in parsed_resolution: max_index += 1
        if max_index < 2 or max_index > 2: return await ctx.respond("Your resolution format is malformed. Please check it and try again.", ephemeral=True)
        res_width = int(parsed_resolution[0])
        res_height = int(parsed_resolution[1])
        if res_width < 256 or res_height < 256: return await ctx.respond("Your custom resolution needs to be at least 256p or higher.", ephermeral=True)
        if res_width > 1024 or res_height > 1024: return await ctx.respond("Your image output resolution cannot be higher than 1024p.", ephemeral=True)
        await ctx.defer()
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=resolution
            )
            generated_image_url = response['data'][0]['url']
        except openai.error.RateLimitError: return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
        except openai.error.ServiceUnavailableError: return await ctx.respond("The OpenAI service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
        except openai.error.APIError: return await ctx.respond("DALL-E encountered an internal error. Please try again.", ephemeral=True)
        except openai.error.Timeout: return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
        localembed = discord.Embed(title="Here's an image generated using your prompt.", color=discord.Color.random())
        localembed.set_image(url=generated_image_url)
        localembed.set_author(name="DALL-E", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
        localembed.set_footer(text="Powered by OpenAI")
        await ctx.respond(embed=localembed)

# Cog Initialization
def setup(bot): bot.add_cog(Utils(bot))
