"""The isobot cog file for utility commands."""

# Imports
import os
import math
import psutil
import openai
import discord
from api import auth
from framework.isobot import currency, embedengine, commands as cmds
from framework.isobot.db import levelling
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from framework.isobot.db.presence import Presence

# Variables
color = discord.Color.random()
currency = currency.CurrencyAPI("database/currency.json", "logs/currency.log")
levelling = levelling.Levelling()
_commands = cmds.Commands()
# openai.api_key = os.getenv("chatgpt_API_KEY")
openai.api_key = auth.ext_token('chatgpt')
chatgpt_conversation = dict()
_presence = Presence()

# Commands
class Utils(commands.Cog):
    """The utils cog class."""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='echo',
        description='Sends a bot message in the channel.'
    )
    @option(name="text", description="What do you want to send?", type=str)
    async def echo(self, ctx: ApplicationContext, text: str):
        """Sends a bot message in the channel."""
        await ctx.respond("Echoed!", ephemeral=True)
        await ctx.channel.send(text)

    @commands.slash_command(
        name="repo",
        description="Shows the open-source code links for isobot."
    )
    async def repo(self, ctx: ApplicationContext):
        """Shows the open-source code links for isobot."""
        localembed = discord.Embed(
            title="Source-code Repositories",
            description="See and contribute to **isobot's [GitHub repository](https://github.com/PyBotDevs/isobot)**\nSee our **[GitHub organization](https://github.com/PyBotDevs)**",
            color=color
        )
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="embedbuilder",
        description="Builds a custom embed however you want."
    )
    @option(name="title", description="The title of the embed", type=str)
    @option(name="description", description="The body of the embed", type=str)
    @option(name="image_url", description="The main image you want to show for the embed (URL ONLY)", type=str, default=None)
    @option(name="thumbnail_url", description="The thumbnail image you want to show for the embed (URL ONLY)", type=str, default=None)
    @option(name="color", description="The embed's accent color (Use -1 for random color)", type=int, default=None)
    @option(name="footer_text", description="The text at the footer of the embed", type=str, default=None)
    @option(name="footer_icon_url", description="The icon you want to show in the embed's footer (URL ONLY)", type=str, default=None)
    async def embedbuilder(self, ctx: ApplicationContext, title: str, description: str, image_url: str = None, thumbnail_url: str = None, color: int = None, footer_text: str = None, footer_icon_url: str = None):
        """Builds a custom embed however you want."""
        await ctx.respond("Embed Built!", ephemeral=True)
        await ctx.channel.send(
            embed=embedengine.embed(
                title,
                description,
                image=image_url,
                thumbnail=thumbnail_url,
                color=color,
                footer_text=footer_text,
                footer_img=footer_icon_url
            )
        )

    @commands.slash_command(
        name='whoami',
        description='Shows information on a user.'
    )
    @option(name="user", description="Who do you want to know about?", type=discord.User, default=None)
    async def whoami(self, ctx: ApplicationContext, user: discord.User=None):
        """Shows information on a user."""
        if user is None: user = ctx.author
        discrim = user.name.split("#")
        username = user.name
        if discrim[-1] == 0:
            username = user.name.replace("#0", "")
        displayname = user.display_name
        registered = user.joined_at.strftime("%b %d, %Y, %T")
        pfp = user.avatar
        localembed_desc = f"`AKA` {displayname}"
        presence = _presence.get_presence(ctx.guild.id, ctx.user.id)
        if presence != 1:
            localembed_desc += f"\n`🌙 AFK` {presence['response']} - <t:{math.floor(presence['time'])}>"
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
        for role in user.roles:
            if role != user.roles[0]:
                role_render += f"<@&{role.id}> "
        localembed.add_field(name='Roles', value=role_render, inline=False)
        localembed.add_field(name="Net worth", value=f"{currency.get_user_networth(user.id)} coins", inline=False)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="profile",
        description="Shows basic stats about your isobot profile, or someone else's profile stats."
    )
    @option(name="user", description="Whose isobot profile do you want to view?", type=discord.User, default=None)
    async def profile(self, ctx: ApplicationContext, user: discord.User = None):
        """Shows basic stats about your isobot profile, or someone else's profile stats."""
        if user is None:
            user = ctx.author
        localembed = discord.Embed(title=f"{user.display_name}'s isobot stats", color=color)
        localembed.set_thumbnail(url=user.avatar)
        localembed.add_field(
            name="Level",
            value=f"Level {levelling.get_level(user.id)} ({levelling.get_xp(user.id)} XP)",
            inline=False
        )
        localembed.add_field(
            name="Balance in Wallet",
            value=f"{currency.get_wallet(user.id)} coins",
            inline=True
        )
        localembed.add_field(
            name="Balance in Bank Account",
            value=f"{currency.get_bank(user.id)} coins",
            inline=True
        )
        localembed.add_field(
            name="Net-Worth",
            value=f"{currency.get_user_networth(user.id)} coins",
            inline=True
        )
        # More stats will be added later
        # Maybe I should make a userdat system for collecting statistical data to process and display here, coming in a future update.
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="status",
        description="Shows the current client info."
    )
    async def status(self, ctx: ApplicationContext):
        """Shows the current client info."""
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
        localembed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="chatgpt",
        description="Talk to ChatGPT and get a response back."
    )
    @option(name="message", description="What do you want to send to ChatGPT?", type=str)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def chatgpt(self, ctx: ApplicationContext, message: str):
        """Talk to ChatGPT and get a response back."""
    #    if str(ctx.author.id) not in chatgpt_conversation:
    #        chatgpt_conversation[str(ctx.author.id)] = [
    #                {
    #                    "role": "system",
    #                    "content": "You are a intelligent assistant."
    #                }
    #            ]
    #    await ctx.defer()
    #    try:
    #        chatgpt_conversation[str(ctx.author.id)].append({"role": "user", "content": message})
    #        _chat = openai.ChatCompletion.create(
    #            model="gpt-3.5-turbo",
    #            messages=chatgpt_conversation[str(ctx.author.id)]
    #        )
    #        _reply = _chat.choices[0].message.content
    #        chatgpt_conversation[str(ctx.author.id)].append({"role": "assistant", "content": _reply})
    #    except openai.error.RateLimitError as e:
    #        print(f"Rate limit for OpenAI exceeded: {e}")
    #        return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
    #    except openai.error.ServiceUnavailableError:
    #        return await ctx.respond("The ChatGPT service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
    #    except openai.error.APIError:
    #        return await ctx.respond("ChatGPT encountered an internal error. Please try again.", ephemeral=True)
    #    except openai.error.Timeout:
    #        return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
    #    localembed = discord.Embed(description=f"{_reply}", color=discord.Color.random())
    #    localembed.set_author(name="ChatGPT", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
    #    localembed.set_footer(text="Powered by OpenAI")
    #    await ctx.respond(embed=localembed)
        localembed = discord.Embed(title="Discontinuation of isobot AI commands", description="Thank you for showing your interest in the isobot AI commands!\nUnfortunately, due to prolonged issues with OpenAI integration, we are temporarily discontinuing all AI-related commands.\nDon't worry, because sometime, in the (not so distant) future, isobot AI commands will be making a sure return for everyone to enjoy.\n\n- NKA Development Team")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="generate_image",
        description="Generate an image of your choice using the DALL-E modal."
    )
    @option(name="prompt", description="What image do you want the bot to generate?", type=str)
    @option(name="resolution", description="Set a custom resolution for your generated image", type=str, default="512x512", choices=["256x256", "512x512", "1024x1024"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def generate_image(self, ctx: ApplicationContext, prompt: str, resolution: str = "512x512"):
        """Generate an image of your choice using the DALL-E modal."""
    #    parsed_resolution: list = resolution.split("x")
    #    max_index: int = 0
    #    for index in parsed_resolution:
    #        max_index += 1
    #    if max_index < 2 or max_index > 2:
    #        return await ctx.respond("Your resolution format is malformed. Please check it and try again.", ephemeral=True)
    #    res_width = int(parsed_resolution[0])
    #    res_height = int(parsed_resolution[1])
    #    if res_width < 256 or res_height < 256:
    #        return await ctx.respond("Your custom resolution needs to be at least 256p or higher.", ephermeral=True)
    #    if res_width > 1024 or res_height > 1024:
    #        return await ctx.respond("Your image output resolution cannot exceed 1024p.", ephemeral=True)
    #    await ctx.defer()
    #    try:
    #        response = openai.Image.create(
    #            prompt=prompt,
    #            n=1,
    #            size=resolution
    #        )
    #        generated_image_url = response['data'][0]['url']
    #    except openai.error.RateLimitError:
    #        return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
    #    except openai.error.ServiceUnavailableError:
    #        return await ctx.respond("The OpenAI service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
    #    except openai.error.APIError:
    #        return await ctx.respond("DALL-E encountered an internal error. Please try again.", ephemeral=True)
    #    except openai.error.Timeout:
    #        return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
    #    localembed = discord.Embed(title="Here's an image generated using your prompt.", color=discord.Color.random())
    #    localembed.set_image(url=generated_image_url)
    #    localembed.set_author(name="DALL-E", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
    #    localembed.set_footer(text="Powered by OpenAI")
    #    await ctx.respond(embed=localembed)
        localembed = discord.Embed(title="Discontinuation of isobot AI commands", description="Thank you for showing your interest in the isobot AI commands!\nUnfortunately, due to prolonged issues with OpenAI integration, we are temporarily discontinuing all AI-related commands.\nDon't worry, because sometime, in the (not so distant) future, isobot AI commands will be making a sure return for everyone to enjoy.\n\n- NKA Development Team")
        await ctx.respond(embed=localembed)

    commandmanager = SlashCommandGroup("commandmanager", "Manage isobot's command registry.")

    @commandmanager.command(
        name="list_all_commands",
        description="Lists all of isobot's commands."
    )
    async def list_all_commands(self, ctx: ApplicationContext):
        if ctx.author.id != 738290097170153472:
            return await ctx.respond("You can't use this command!", ephemeral=True)
        all_cmds = _commands.list_commands()
        parsed_output = str()
        for cmd in all_cmds:
            parsed_output += f"\n`{cmd}`"
        await ctx.respond(parsed_output)

    @commandmanager.command(
        name="switch_flag",
        description="Switches a flag for a specific command."
    )
    @option(name="command", description="The command entry that you want to manipulate", type=str)
    @option(name="flag", description="The flag that you want to enable", type=str, choices=["disabled", "bugged"])
    @option(name="status", description="Choose whether you want the flag to be True or False.", type=bool)
    async def switch_flag(self, ctx: ApplicationContext, command: str, flag: str, status: bool):
        if ctx.author.id != 738290097170153472:
            return await ctx.respond("You can't use this command!", ephemeral=True)
        if flag == "disabled": _commands.command_disabled_flag(command, status)
        elif flag == "bugged": _commands.command_bugged_flag(command, status)
        await ctx.respond(f":white_check_mark: Flag edited successfully for `/{command}`.")

    @commandmanager.command(
        name="remove",
        description="Removes a command permanently from the command registry."
    )
    @option(name="command", description="The command that you want to remove.", type=str)
    async def _remove(self, ctx: ApplicationContext, command: str):
        if ctx.author.id != 738290097170153472:
            return await ctx.respond("You can't use this command!", ephemeral=True)
        _commands.remove_command(command)
        await ctx.respond(f":white_check_mark: Command `/{command}` successfully removed from database.")

    @commandmanager.command(
        name="add",
        description="Add new command to the command registry."
    )
    @option(name="command_name", description="What is the actual command name?", type=str)
    @option(name="stylized_name", description="Enter a good-looking version of the command name.", type=str)
    @option(name="description", description="Enter a description for this command.", type=str)
    @option(name="command_type", description="What category does this command belong to?", type=str)
    @option(name="usable_by", description="Who can use this command?", type=str)
    @option(name="cooldown", description="How many seconds is the command cooldown for?", type=int, default=None)
    async def _add(self, ctx: ApplicationContext, command_name: str, stylized_name: str, description: str, command_type: str, usable_by: str, cooldown: int = None):
        if ctx.author.id != 738290097170153472:
            return await ctx.respond("You can't use this command!", ephemeral=True)
        _commands.add_command(
            command_name,
            stylized_name,
            description,
            command_type,
            usable_by,
            cooldown=cooldown
        )
        localembed = discord.Embed(title=":white_check_mark: New Command Successfully Added!", description=f"`/{command_name}\n\n{description}`", color=discord.Color.green())
        localembed.add_field(name="Command Type", value=command_type)
        localembed.add_field(name="Usable By", value=usable_by)
        localembed.add_field(name="Cooldown", value=cooldown)
        await ctx.respond(embed=embed)

# Cog Initialization
def setup(bot):
    """Initializes the cog."""
    bot.add_cog(Utils(bot))
