"""The isobot cog file for utility commands."""

# Imports
import os
import math
import psutil
import openai
import discord
import json
import time
import datetime
from api import auth
from framework.isobot import currency, commands as cmds
from framework.isobot.db import levelling, embeds as _embeds
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from framework.isobot.db.presence import Presence

# Variables
color = discord.Color.random()
currency = currency.CurrencyAPI("database/currency.json", "logs/currency.log")
levelling = levelling.Levelling()
_commands = cmds.Commands()
_embeds = _embeds.Embeds()
# openai.api_key = os.getenv("chatgpt_API_KEY")
openai.api_key = auth.ext_token('chatgpt')
chatgpt_conversation = dict()
_presence = Presence()

# Commands
class Utils(commands.Cog):
    """The utils cog class."""

    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

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
        name="ping",
        description="Get the server latency."
    )
    async def ping(self, ctx: ApplicationContext):
        localembed = discord.Embed(
            title=":ping_pong: Pong!",
            description=f"Current server latency is **{round(self.bot.latency * 1000, 2)} ms**.",
            color=discord.Color.random()
        )
        await ctx.respond(embed=localembed)

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
        name='whoami',
        description='Shows information on a user.'
    )
    @commands.guild_only()
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
            title=f"User Info on {username} {'`BOT`' if user.bot else ''}",
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
        name="avatar",
        description="Return a user's profile avatar."
    )
    @option(name="user", description="Who's profile avatar do you want to see?", type=discord.User, default=None)
    async def avatar(self, ctx: ApplicationContext, user: discord.User = None):
        """Return a user's profile avatar."""
        if user is None:
            user = ctx.author
        localembed = discord.Embed(title=f"{user.display_name}'s Profile Avatar", description=f"[avatar link]({user.avatar})", color=discord.Color.random())
        localembed.set_image(url=user.avatar)
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
        total_users = int()
        for guild in self.bot.guilds:
            total_users += guild.member_count
        localembed = discord.Embed(title="Client Info")
        localembed.add_field(name="Uptime", value=str(datetime.timedelta(seconds=int(round(time.time()-self.start_time)))))
        localembed.add_field(name="OS Name", value=os_name, inline=True)
        localembed.add_field(name="RAM Available", value=sys_ram)
        localembed.add_field(name="CPU Usage", value=sys_cpu)
        localembed.add_field(name="Registered Users", value=f"{bot_users} users", inline=True)
        localembed.add_field(name="Total Users", value=f"{total_users} users")
        localembed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000, 2)} ms", inline=True)
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
        if str(ctx.author.id) not in chatgpt_conversation:
            chatgpt_conversation[str(ctx.author.id)] = [
                    {
                        "role": "system",
                        "content": "You are a intelligent assistant."
                    }
                ]
        await ctx.defer()
        try:
            chatgpt_conversation[str(ctx.author.id)].append({"role": "user", "content": message})
            _chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chatgpt_conversation[str(ctx.author.id)]
            )
            _reply = _chat.choices[0].message.content
            chatgpt_conversation[str(ctx.author.id)].append({"role": "assistant", "content": _reply})
        except openai.error.RateLimitError as e:
            print(f"Rate limit for OpenAI exceeded: {e}")
            return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
        except openai.error.ServiceUnavailableError:
            return await ctx.respond("The ChatGPT service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
        except openai.error.APIError:
            return await ctx.respond("ChatGPT encountered an internal error. Please try again.", ephemeral=True)
        except openai.error.Timeout:
            return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
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
        """Generate an image of your choice using the DALL-E modal."""
        parsed_resolution: list = resolution.split("x")
        max_index: int = 0
        for index in parsed_resolution:
            max_index += 1
        if max_index < 2 or max_index > 2:
            return await ctx.respond("Your resolution format is malformed. Please check it and try again.", ephemeral=True)
        res_width = int(parsed_resolution[0])
        res_height = int(parsed_resolution[1])
        if res_width < 256 or res_height < 256:
            return await ctx.respond("Your custom resolution needs to be at least 256p or higher.", ephermeral=True)
        if res_width > 1024 or res_height > 1024:
            return await ctx.respond("Your image output resolution cannot exceed 1024p.", ephemeral=True)
        await ctx.defer()
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=resolution
            )
            generated_image_url = response['data'][0]['url']
        except openai.error.RateLimitError:
            return await ctx.respond("The OpenAI API is currently being rate-limited. Try again after some time.", ephemeral=True)
        except openai.error.ServiceUnavailableError:
            return await ctx.respond("The OpenAI service is currently unavailable.\nTry again after some time, or check it's status at https://status.openai.com", ephemeral=True)
        except openai.error.APIError:
            return await ctx.respond("DALL-E encountered an internal error. Please try again.", ephemeral=True)
        except openai.error.Timeout:
            return await ctx.respond("Your request timed out. Please try again, or wait for a while.", ephemeral=True)
        localembed = discord.Embed(title="Here's an image generated using your prompt.", color=discord.Color.random())
        localembed.set_image(url=generated_image_url)
        localembed.set_author(name="DALL-E", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png")
        localembed.set_footer(text="Powered by OpenAI")
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="vote",
        description="Vote for isobot on Top.gg and DBL."
    )
    async def vote(self, ctx: ApplicationContext):
        """Vote for isobot on Top.gg and DBL."""
        localembed = discord.Embed(title="Vote for isobot!", description="**Top.gg:** https://top.gg/bot/896437848176230411 \n**DBL:** https://discordbotlist.com/bots/halloween-isobot", color=discord.Color.random())
        localembed.set_footer(text="Thank you for your support!")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="nuke",
        description="Completely wipes a text channel in the server."
    )
    @commands.guild_only()
    @option(name="channel", description="The channel you want to nuke.", type=discord.TextChannel)
    async def nuke(self, ctx: ApplicationContext, channel: discord.TextChannel):
        """Completely wipes a text channel in the server."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(
                "You can't use this command! You need the `Administrator` permission in this server to run this command.",
                ephemeral=True
            )
        localembed = discord.Embed(
            description=f":white_check_mark: Channel `#{channel.name}` successfully nuked.",
            color=discord.Color.green()
        )
        new_channel = await channel.clone(reason=f"Channel has been nuked by {ctx.author.name}")
        await channel.delete(reason=f"Channel has been nuked by {ctx.author.name}")
        await new_channel.send(f"Channel nuked by **{ctx.author.name}**!")
        await ctx.respond(embed=localembed, ephemeral=True)

    @commands.slash_command(
        name="serverinfo",
        description="Get detailed information about the server."
    )
    @commands.guild_only()
    async def serverinfo(self, ctx: ApplicationContext):
        """Get detailed information about the server."""
        localembed = discord.Embed(
            title=f"Server info on **{ctx.guild.name}**",
            description=f"*{ctx.guild.description}*" if ctx.guild.description is not None else '',
            color=discord.Color.random()
        )
        localembed.set_thumbnail(url=ctx.guild.icon)
        localembed.set_footer(text=f"Server ID: {ctx.guild.id}")
        if ctx.guild.banner is not None:
            localembed.set_image(url=ctx.guild.banner)
        
        # Server Info Fields
        localembed.add_field(name="Server Created On", value=ctx.guild.created_at.strftime("%b %d, %Y, %T"))
        localembed.add_field(name="Member Count", value=f"{ctx.guild.member_count} members")
        localembed.add_field(name="Server Owner", value=f"<@!{ctx.guild.owner_id}>")
        localembed.add_field(
            name="Total Number of Channels",
            value=f"{len(ctx.guild.channels)-len(ctx.guild.categories)} channels\n({len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice | {len(ctx.guild.forum_channels)} Forums)",
            inline=True
        )
        localembed.add_field(name="Total Number of Roles", value=f"{len(ctx.guild.roles)-1} roles")
        threads = await ctx.guild.active_threads()
        threads_display_list = str()
        if len(threads) <= 4:  # Display threads if total threads count is under 5
            for thread in threads:
                threads_display_list += f"<#{thread.id}>, "
            threads_display_list = threads_display_list.rstrip(", ")  # Removing the final "," from the string
        localembed.add_field(
            name="Currently Active Threads",
            value=f"{len(await ctx.guild.active_threads())} threads {f'({threads_display_list})' if threads_display_list != '' else ''}"
        )
        localembed.add_field(
            name="Active Invite Links",
            value=f"{len(await ctx.guild.invites())} links {'(invites disabled)' if ctx.guild.invites_disabled else ''}"
        )
        localembed.add_field(name="Server Verification Level", value=ctx.guild.verification_level, inline=True)
        localembed.add_field(
            name="Custom Expressions (emojis/stickers)",
            value=f"{len(await ctx.guild.fetch_emojis())} emojis | {len(await ctx.guild.fetch_stickers())} stickers"
        )
        await ctx.respond(embed=localembed)

    # Server Embed System Manager Commands
    embed_system = SlashCommandGroup("embeds", "Commands used to add, edit and remove custom bot embeds for server-wide use.")

    # TODO: Add commands for managing server embeds

    @embed_system.command(
        name="create",
        description="Create a new custom embed for the server."
    )
    @commands.guild_only()
    @option(name="embed_name", description="What do you want your embed's name to be?")
    @option(name="title", description="Set a title for your embed", type=str, default=None)
    @option(name="description", description="Set a description for your embed", type=str, default=None)
    @option(name="color", description="Format: 0x{replace with hex code} (-1 = random color)", type=int, default=None)
    @option(name="timestamp_enabled", description="Choose whether to display timestamps on the embed or not", type=bool, default=False)
    @option(name="title_url", description="Attach a url to your embed title (https:// only)", type=str, default=None)
    @option(name="image_url", description="Add an image to your embed (https:// only)", type=str, default=None)
    @option(name="thumbnail", description="Add a thumbnail image to your embed (https:// only)", type=str, default=None)
    async def embeds_create(self, ctx: ApplicationContext, embed_name: str, title: str = None, description: str = None, color: int = None, timestamp_enabled: bool = False, title_url: str = None, image_url: str = None, thumbnail: str = None):
        """Create a new custom embed for the server."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        _embeds.generate_embed(
            server_id=ctx.guild.id,
            embed_name=embed_name,
            title=title,
            description=description,
            color=color,
            timestamp_enabled=timestamp_enabled,
            title_url=title_url,
            image_url=image_url,
            thumbnail=thumbnail
        )
        await ctx.respond(
            f"## :white_check_mark: Embed Successfully Created.\nThe name of this custom embed is `{embed_name}`. You can use this embed name to reference this custom embed in other commands.\n\nHere's a preview of your new embed:",
            embed=_embeds.build_embed(ctx.guild.id, embed_name)
        )
    
    @embed_system.command(
        name="delete",
        description="Delete a custom embed from the server."
    )
    @commands.guild_only()
    @option(name="embed_name", description="The specific embed you want to delete.", type=str)
    async def embeds_delete(self, ctx: ApplicationContext, embed_name: str):
        """Delete a custom embed from the server."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        result_code = _embeds.delete_embed(ctx.guild.id, embed_name=embed_name)
        if result_code == 1:
            localembed = discord.Embed(
                title=":x: Failed to delete embed",
                description=f"This server does not have an embed with the name `{embed_name}`.",
                color=discord.Color.red()
            )
            return await ctx.respond(embed=localembed, ephemeral=True)
        else:
            localembed = discord.Embed(
                title=":white_check_mark: Custom embed successfully deleted",
                description=f"The custom server embed `{embed_name}` has been deleted.\n\nMake sure to remove any references of this embed from any other serverconfig features in the bot.",
                color=discord.Color.green()
            )
            return await ctx.respond(embed=localembed)
    
    @embed_system.command(
        name="list",
        description="View a list of all the custom embeds in this server."
    )
    @commands.guild_only()
    async def embeds_list(self, ctx: ApplicationContext):
        """View a list of all the custom embeds in this server."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        embeds_list = _embeds.get_embeds_list()
        num = 0
        parsed_output = str()
        for embed in embeds_list.keys():
            num += 1
            parsed_output += f"{num}. `{embed}`\n"
        if parsed_output == "":
            parsed_output = "*Nothing to see here...*"
        localembed = discord.Embed(
            title=f"Custom Server Embeds for **{ctx.guild.name}**",
            description=parsed_output
        )
        await ctx.respond(embed=localembed)
    
    @embed_system.command(
        name="add_embed_field",
        description="Appends a new field to an existing server embed."
    )
    @commands.guild_only()
    @option(name="embed_name", description="The server embed to which you want to add the field.", type=str)
    @option(name="name", description="The name of the field.", type=str)
    @option(name="value", description="The value of the field.", type=str)
    @option(name="inline", description="Whether you want the field to be in-line or not.", type=bool, default=False)
    async def embeds_add_embed_field(self, ctx: ApplicationContext, embed_name: str, name: str, value: str, inline: bool = False):
        """Appends a new field to an existing server embed."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        result_code = _embeds.add_embed_field(ctx.guild.id, embed_name=embed_name, name=name, value=value, inline=inline)
        if result_code == 1:
            localembed = discord.Embed(
                title=":x: Failed to add new field to embed",
                description=f"This server does not have an embed with the name `{embed_name}`.",
                color=discord.Color.red()
            )
            return await ctx.respond(embed=localembed, ephemeral=True)
        else:
            localembed = _embeds.build_embed(ctx.guild.id, embed_name=embed_name)
            await ctx.respond(f"## :white_check_mark: New field successfully added to server embed `{embed_name}\nHere's a preview of your modified embed:`", embed=localembed)

    @embed_system.command(
        name="add_embed_author",
        description="Add or replace the author section of an existing server embed."
    )
    @commands.guild_only()
    @option(name="embed_name", description="The server embed to which you want to add the author", type=str)
    @option(name="author_name", description="The name of the author.", type=str)
    @option(name="url", description="Attach a url to the author name. (https:// only)", type=str, default=None)
    @option(name="icon_url", description="Add an icon next to the author (https:// only)", type=str, default=None)
    async def embeds_add_embed_author(self, ctx: ApplicationContext, embed_name: str, author_name: str, url: str = None, icon_url: str = None):
        """Add or replace the author section of an existing server embed."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        result_code = _embeds.add_embed_author(ctx.guild.id, embed_name=embed_name, name=author_name, url=url, icon_url=icon_url)
        if result_code == 1:
            localembed = discord.Embed(
                title=":x: Failed to add author to embed",
                description=f"This server does not have an embed with the name `{embed_name}`.",
                color=discord.Color.red()
            )
            return await ctx.respond(embed=localembed, ephemeral=True)
        else:
            localembed = _embeds.build_embed(ctx.guild.id, embed_name=embed_name)
            await ctx.respond(f"## :white_check_mark: Author section successfully added to server embed `{embed_name}\nHere's a preview of your modified embed:`", embed=localembed)

    @embed_system.command(
        name="add_embed_footer",
        description="Add or replace the footer of an existing server embed."
    )
    @commands.guild_only()
    @option(name="embed_name", description="The server embed to which you want to add the author", type=str)
    @option(name="text", description="The text you want to display in the footer.", type=str)
    @option(name="icon_url", description="Add an icon in the footer of the embed. (https:// only)", type=str, default=None)
    async def embeds_add_embed_author(self, ctx: ApplicationContext, embed_name: str, text: str, icon_url: str = None):
        """Add or replace the footer of an existing server embed."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond(
                "You can't use this command! You need the `Manage Messages` permission in this server to run this command.",
                ephemeral=True
            )
        result_code = _embeds.add_embed_footer(ctx.guild.id, embed_name=embed_name, text=text, icon_url=icon_url)
        if result_code == 1:
            localembed = discord.Embed(
                title=":x: Failed to add footer to embed",
                description=f"This server does not have an embed with the name `{embed_name}`.",
                color=discord.Color.red()
            )
            return await ctx.respond(embed=localembed, ephemeral=True)
        else:
            localembed = _embeds.build_embed(ctx.guild.id, embed_name=embed_name)
            await ctx.respond(f"## :white_check_mark: Footer section successfully added to server embed `{embed_name}\nHere's a preview of your modified embed:`", embed=localembed)

    # TODO: Make the following bot commands:
    #   - create new embed (done)
    #   - delete embed (done)
    #   - show embeds list (done)
    #   - add embed field (done)
    #   - add embed author (done)
    #   - add embed footer (done)

    # Isobot Command Registry Management System
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
        await ctx.respond(embed=localembed)
    
    # User Commands
    @commands.user_command(name="Show User Information")
    async def _whoami(self, ctx: ApplicationContext, user: discord.User):
        await self.whoami(ctx, user)

    @commands.user_command(name="View isobot Profile")
    async def _profile(self, ctx: ApplicationContext, user: discord.User):
        await self.profile(ctx, user)

# Cog Initialization
def setup(bot):
    """Initializes the cog."""
    bot.add_cog(Utils(bot))
