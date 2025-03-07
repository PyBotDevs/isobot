"""Isobot, the bot to make your server (a little bit) better.\n\nisobot (C) NKA 2022-2024.\nRun `/credits` in the Discord bot to see the credits.\n\nWARNING: This client is meant to be run standalone. Not as a Python import."""
# Core Imports
import os
import os.path
import json
import time
import datetime
import discord, discord.errors
import asyncio
import api.auth
import config_updater

# Run Config Updater 
config_updater.check_for_updates()

# Client Module Imports
from utils import logger, ping
from math import floor
from random import randint
from framework.isobot import currency, colors, settings, commands as _commands, isocard
from framework.isobot.shop import ShopData
from framework.isobot.db import levelling, items, userdata, automod, weather, warnings, presence as _presence, serverconfig, embeds
from discord import ApplicationContext, option
from discord.ext import commands
from cogs.isocoin import create_isocoin_key

# Variables
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Bot(intents=intents)
color = discord.Color.random()
start_time = ""

# Pre-Initialization Commands
def initial_setup():
    """Runs the initial setup for isobot's directories.\nThis creates missing directories, new log files, as well as new databases for any missing `.json` database files."""
    # Create required client directories
    try:
        paths = ("database", "database/isobank", "config", "logs", "themes")
        for p in paths:
            if not os.path.isdir(p):
                logger.warn(f"'{p}' directory appears to be missing. Created new directory for '{p}'.", module="main/Setup", nolog=True)
                os.mkdir(p)
    except OSError:
        logger.error(f"Failed to make directory: {e}", module="main/Setup")

    # Generating database files
    try:
        databases = (
            "automod",
            "currency",
            "isocard",
            "items",
            "levels",
            "serverconfig",
            "serververification",
            "warnings",
            "presence",
            "user_data",
            "weather",
            "embeds",
            "isocard_transactions",
            "isocard_transaction_history",
            "isobank/accounts",
            "isobank/auth"
        )
        for _file in databases:
            if not os.path.isfile(f"database/{_file}.json"):
                logger.warn(f"[main/Setup] '{_file}.json' was not found in database directory. Creating new database...", module="main/Setup", nolog=True)
                with open(f"database/{_file}.json", 'x', encoding="utf-8") as f:
                    if _file == "currency":
                        json.dump({"treasury": 100000000, "wallet": {}, "bank": {}}, f)
                    else:
                        json.dump({}, f)
                    f.close()
                time.sleep(0.5)
    except IOError as e:
        logger.error(f"Failed to make database file: {e}", module="main/Setup")
    
    # Generating other files
    try:
        if not os.path.isfile(f"config/settings.json"):
            logger.warn(f"[main/Setup] Settings database file was not found in config directory. Creating new database...", module="main/Setup", nolog=True)
            with open(f"config/settings.json", 'x', encoding="utf-8") as f:
                json.dump({}, f)
                f.close()
    except IOError as e:
        logger.error(f"Failed to make settings database file: {e}", module="main/Setup")

    # Generating client log files
    try:
        if not os.path.isfile("logs/info-log.txt"):
            with open('logs/info-log.txt', 'x', encoding="utf-8") as this:
                this.write("# All information and warnings will be logged here!\n")
                this.close()
            logger.info("Created info log", module="main/Setup", nolog=True)
            time.sleep(0.5)
        if not os.path.isfile("logs/error-log.txt"):
            with open('logs/error-log.txt', 'x', encoding="utf-8") as this:
                this.write("# All exceptions will be logged here!\n")
                this.close()
            logger.info("Created error log", module="main/Setup", nolog=True)
            time.sleep(0.5)
        if not os.path.isfile("logs/currency.log"):
            with open('logs/currency.log', 'x', encoding="utf-8") as this:
                this.close()
            logger.info("Created currency log", module="main/Setup", nolog=True)
            time.sleep(0.5)
        if not os.path.isfile("logs/startup-log.txt"):
            with open("logs/startup-log.txt", 'x', encoding="utf-8") as this:
                this.close()
            time.sleep(0.5)
        if not os.path.isfile("logs/isocard_transactions.log"):
            with open("logs/isocard_transactions.log", 'x', encoding="utf-8") as this:
                this.write("# All IsoCard transaction updates will be logged here.\n")
                this.close()
            time.sleep(0.5)
    except IOError as e:
        logger.error(f"Failed to make log file: {e}", module="main/Setup", nolog=True)

initial_setup()  # Check for any missing sub-directories or databases in bot directory

# Framework Module Loader
colors = colors.Colors()
s = logger.StartupLog("logs/startup-log.txt", clear_old_logs=True)
currency = currency.CurrencyAPI("database/currency.json", "logs/currency.log")
settings = settings.Configurator()
levelling = levelling.Levelling()
items = items.Items()
serverconfig = serverconfig.ServerConfig()
warningsdb = warnings.Warnings()
userdata = userdata.UserData()
automod = automod.Automod()
_presence = _presence.Presence()
weather = weather.Weather()
embeds = embeds.Embeds()
_commands = _commands.Commands()
shop_data = ShopData("config/shop.json")

# Theme Loader
if api.auth.get_runtime_options()["themes"]:
    with open("themes/halloween.theme.json", 'r', encoding="utf-8") as f:
        theme = json.load(f)
        try:
            color_loaded = theme["theme"]["embed_color"]
            color = int(color_loaded, 16)
        except KeyError:
            logger.warn("The theme file being loaded might be broken. Rolling back to default configuration...", module="main/Themes")
            color = discord.Color.random()
else:
    color = discord.Color.random()

# Events
@client.event
async def on_ready():
    """This event is fired when the bot client is ready"""
    start_time = datetime.datetime.now()
    s.log(f"[main/Client] {colors.green}Client ready!{colors.end}")
    s.log("""
Isobot  Copyright (C) 2022-2024  NKA
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
__________________________________________________""")
    time.sleep(1)
    if api.auth.get_runtime_options()["show_ping_on_startup"]:
        s.log("Client Information:")
        s.log(f"   Latency/Ping: {round((client.latency * 1000), 2)} ms")
        s.log("--------------------")
    s.log(f'[main/Client] Logged in as {client.user.name}. Start time: {start_time.strftime("%H:%M:%S")}\n[main/Client] Ready to accept commands. Click Ctrl+C to shut down the bot.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="I-I-I be poppin bottles 🗣🗣🔥"), status=discord.Status.idle)
    s.log(f'[main/Log] {colors.green}Status set to IDLE. Rich presence set.{colors.end}')
    # Deploy IsoCard Payments Server
    isocard.deploy_server()
    time.sleep(0.5)
    # Start and Deploy Ping Server
    if api.auth.get_mode() or api.auth.get_runtime_options()["ping_server_override"]:
        # If ping_server_override is set to true, it will start the pinging server no matter what. If it's set to false, it will only start if client mode is set to replit.
        s.log(f"[main/Flask] {f'{colors.yellow}Ping server override.{colors.end} ' if api.auth.get_runtime_options()['ping_server_override'] else ''}Starting pinger service...")
        ping.host()
    time.sleep(5)

@client.event
async def on_member_join(ctx):
    """This event is fired whenever a new member joins a server."""
    # Automatically assigning roles to new members (autorole)
    autorole = serverconfig.fetch_autorole(ctx.guild.id)
    if autorole is not None:
        role = discord.Guild.get_role(ctx.guild, int(autorole))
        await ctx.add_roles(role, reason="Role assigned due to autoroles.")

    # Welcome Message Autoresponder
    welcome_message = serverconfig.fetch_welcome_message(ctx.guild.id)
    if welcome_message["message"] is not None:
        welcome_message_autoresponder_channel = client.get_channel(welcome_message["channel"])

        # Perform attribute formatting for welcome message
        welcome_message_formatted = welcome_message["message"]
        welcome_message_formatted = welcome_message_formatted.replace("[user.nickname]", str(ctx.author.display_name))
        welcome_message_formatted = welcome_message_formatted.replace("[user.username]", str(ctx.author.name))
        welcome_message_formatted = welcome_message_formatted.replace("[user.mention]", str(ctx.author.mention))
        welcome_message_formatted = welcome_message_formatted.replace("[server.name]", str(ctx.guild.name))
        welcome_message_formatted = welcome_message_formatted.replace("[server.membercount]", str(ctx.guild.member_count))

        await welcome_message_autoresponder_channel.send(welcome_message_formatted)

@client.event
async def on_member_leave(ctx):
    """This event is fired whenever a member leaves a server."""
    # Goodbye Message Autoresponder
    goodbye_message = serverconfig.fetch_goodbye_message(ctx.guild.id)
    if goodbye_message["message"] is not None:
        goodbye_message_autoresponder_channel = client.get_channel(goodbye_message["channel"])

        # Perform attribute formatting for goodbye message
        goodbye_message_formatted = goodbye_message["message"]
        goodbye_message_formatted = goodbye_message_formatted.replace("[user.nickname]", str(ctx.author.display_name))
        goodbye_message_formatted = goodbye_message_formatted.replace("[user.username]", str(ctx.author.name))
        goodbye_message_formatted = goodbye_message_formatted.replace("[user.mention]", str(ctx.author.mention))
        goodbye_message_formatted = goodbye_message_formatted.replace("[server.name]", str(ctx.guild.name))
        goodbye_message_formatted = goodbye_message_formatted.replace("[server.membercount]", str(ctx.guild.member_count))

        await goodbye_message_autoresponder_channel.send(goodbye_message_formatted)

@client.event
async def on_message(ctx):
    """This event is fired whenever a message is sent (in a readable channel)."""
    runtimeconf = api.auth.get_runtime_options()

    # Server Activity Logger
    if runtimeconf["log_messages"]:
        _user = str(ctx.author).split('#')[0]
        _discrim = str(ctx.author).split('#')[-1]
        try:
            if str(ctx.guild.id) not in runtimeconf["guild_log_blacklist"]:
                if _discrim == "0000":
                    logger.info(f"[{ctx.guild.name} -> #{ctx.channel.name}] New message received from {_user}[webhook] ({ctx.author.display_name})", timestamp=True)
                elif _discrim == "0":
                    logger.info(f"[{ctx.guild.name} -> #{ctx.channel.name}] New message received from @{_user} ({ctx.author.display_name})", timestamp=True)
                else:
                    logger.info(f"[{ctx.guild.name} -> #{ctx.channel.name}] New message received from {ctx.author} ({ctx.author.display_name})", timestamp=True)
        except AttributeError:
            if _discrim == "0":
                logger.info(f"[DM] New message received from @{_user} ({ctx.author.display_name})", timestamp=True)
            elif _discrim == "0000":
                logger.info(f"[DM] New message received from {_user}[webhook] ({ctx.author.display_name})", timestamp=True)
            else:
                logger.info(f"[DM] New message received from {ctx.author} ({ctx.author.display_name})", timestamp=True)

    if not ctx.author.bot:
        # Check and initialize databases with new data for user.
        currency.new_wallet(ctx.author.id)
        currency.new_bank(ctx.author.id)
        create_isocoin_key(ctx.author.id)
        userdata.generate(ctx.author.id)
        settings.generate(ctx.author.id)
        items.generate(ctx.author.id)
        levelling.generate(ctx.author.id)
        try:
            automod.generate(ctx.guild.id)
            serverconfig.generate(ctx.guild.id)
            embeds.generate_server_key(ctx.guild.id)
            warningsdb.generate(ctx.guild.id, ctx.author.id)
        except AttributeError: pass

        try:
            # AFK System Checker
            presence_user_list = list()
            presence = _presence.get_raw()
            if str(ctx.guild.id) in presence:
                for userid in presence[str(ctx.guild.id)].keys():
                    presence_user_list.append(userid)
            for user in presence_user_list:
                if str(user) in ctx.content and not ctx.author.bot:
                    fetch_user = await client.fetch_user(int(user))
                    await ctx.channel.send(f"{fetch_user.display_name} went AFK <t:{floor(presence[str(ctx.guild.id)][str(user)]['time'])}:R>: {presence[str(ctx.guild.id)][str(user)]['response']}")
            if str(ctx.guild.id) in presence and str(ctx.author.id) in presence[str(ctx.guild.id)]:
                _presence.remove_afk(ctx.guild.id, ctx.author.id)
                afk_cleared_message = await ctx.channel.send(f"Welcome back {ctx.author.mention}. Your AFK has been removed.")
                await asyncio.sleep(5)
                await afk_cleared_message.delete()

            # Swear-Filter
            automod_config = automod.fetch_config(ctx.guild.id)
            if (automod_config["swear_filter"]["enabled"]) and (not ctx.channel.is_nsfw()):
                if (automod_config["swear_filter"]["keywords"]["use_default"] and any(x in ctx.content.lower() for x in automod_config["swear_filter"]["keywords"]["default"])) or (automod_config["swear_filter"]["keywords"]["custom"] != [] and any(x in ctx.content.lower() for x in automod_config["swear_filter"]["keywords"]["custom"])):
                    await ctx.delete()
                    await ctx.channel.send(f'{ctx.author.mention} watch your language.', delete_after=5)

            # Link Blocker
            if ("http://" in ctx.content.lower()) or ("https://" in ctx.content.lower()):
                automod_config = automod.fetch_config(ctx.guild.id)
                if automod_config["link_blocker"]["enabled"]:
                    if automod_config["link_blocker"]["use_whitelist_only"]:
                        if not any(x in ctx.content.lower() for x in automod_config["link_blocker"]["whitelisted"]["default"]):
                            await ctx.delete()
                            await ctx.channel.send(f'{ctx.author.mention} This link is not allowed in this server.', delete_after=5)
                    else:
                        if any(x in ctx.content.lower() for x in automod_config["link_blocker"]["blacklisted"]["default"]):
                            await ctx.delete()
                            await ctx.channel.send(f'{ctx.author.mention} This link is not allowed in this server.', delete_after=5)
        except AttributeError: pass  # Raised if the message isn't from a guild.

        # Levelling System
        levelling.add_xp(ctx.author.id, randint(1, 5))
        xpreq = 0
        for level in range(levelling.get_level(ctx.author.id)):
            xpreq += 50
            if xpreq >= 5000: break
        if levelling.get_xp(ctx.author.id) >= xpreq:
            levelling.set_xp(ctx.author.id, 0)
            levelling.add_levels(ctx.author.id, 1)
            if settings.fetch_setting(ctx.author.id, "levelup_messages") is True:
                try:
                    if serverconfig.fetch_levelup_override_channel(ctx.guild.id) is None:
                        await ctx.author.send(f"{ctx.author.mention}, you just ranked up to **level {levelling.get_level(ctx.author.id)}**. Nice!\n\n{':bulb: Tip: This is your global message level and is the same across all servers. If you want to disable DMs for levelling up, run `/settings levelup_messages enabled: False`' if levelling.get_level(ctx.author.id) == 1 else ''}")
                    else:
                        channel = await client.get_channel(int(serverconfig.fetch_levelup_override_channel(ctx.guild.id)))
                        await channel.send(f"{ctx.author.mention}, you just ranked up to **level {levelling.get_level(ctx.author.id)}**. Nice!\n\n{':bulb: Tip: This is your global message level and is the same across all servers. If you want to disable messages for levelling up, run `/settings levelup_messages enabled: False`' if levelling.get_level(ctx.author.id) == 1 else ''}")
                except discord.errors.Forbidden:
                    # Error is raised when the user isnt accepting DMs (or has blocked isobot)
                    # In that case isobot will automatically stop sending levelup messages to them
                    logger.warn(f"Unable to send level up message to {ctx.author} ({ctx.author.id}), as they are not accepting DMs from isobot. This ID has been added to `levelup_messages` blacklist.", module="main/Levelling")
                    settings.edit_setting(ctx.author.id, "levelup_messages", False)
        
        # Autoresponder System
        server_autoresponder_config: dict = serverconfig.fetch_autoresponder_configuration(ctx.guild.id)

        for config in server_autoresponder_config.keys():
            if server_autoresponder_config[config]["active_channel"] == None or server_autoresponder_config[config]["active_channel"] == ctx.channel.id:
                if server_autoresponder_config[config]["match_case"]:
                    if server_autoresponder_config[config]["autoresponder_trigger_condition"] == "MATCH_MESSAGE":
                        if ctx.content == server_autoresponder_config[config]["autoresponder_trigger"]:
                            await ctx.channel.send(server_autoresponder_config[config]["autoresponder_text"])
                    elif server_autoresponder_config[config]["autoresponder_trigger_condition"] == "WITHIN_MESSAGE":
                        if server_autoresponder_config[config]["autoresponder_trigger"] in ctx.content:
                            await ctx.channel.send(server_autoresponder_config[config]["autoresponder_text"])
                else:
                    if server_autoresponder_config[config]["autoresponder_trigger_condition"] == "MATCH_MESSAGE":
                        if ctx.content.lower() == server_autoresponder_config[config]["autoresponder_trigger"]:
                            await ctx.channel.send(server_autoresponder_config[config]["autoresponder_text"])
                    elif server_autoresponder_config[config]["autoresponder_trigger_condition"] == "WITHIN_MESSAGE":
                        if server_autoresponder_config[config]["autoresponder_trigger"] in ctx.content.lower():
                            await ctx.channel.send(server_autoresponder_config[config]["autoresponder_text"])

# Error handler
@client.event
async def on_application_command_error(ctx: ApplicationContext, error: discord.DiscordException):
    """An event handler to handle command exceptions when things go wrong.\n\nSome exceptions may be pre-handled, but any unhandable exceptions will be logged as an error."""
    if not api.auth.get_runtime_options()["debug_mode"]:
        if isinstance(error, commands.CommandOnCooldown): await ctx.respond(f":stopwatch: Not now! Please try after **{str(datetime.timedelta(seconds=int(round(error.retry_after))))}**")
        elif isinstance(error, commands.MissingPermissions): await ctx.respond(":warning: You don't have the required server permissions to run this command!", ephemeral=True)
        elif isinstance(error, commands.BadArgument): await ctx.respond(":x: Invalid argument.", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions): await ctx.respond(":x: I don\'t have the required permissions to use this.\nIf you think this is a mistake, please go to server settings and fix isobot's role permissions.")
        elif isinstance(error, commands.BadBoolArgument): await ctx.respond(":x: Invalid true/false argument.", ephemeral=True)
        elif isinstance(error, commands.NoPrivateMessage): await ctx.respond(":x: You can only use this command in a server!", ephemeral=True)
        elif isinstance(error, commands.PrivateMessageOnly): await ctx.respond(":x: You can only use this command in isobot's DMs!", ephemeral=True)
        else:
            logger.error(f"Command failure: An uncaught error occured while running the command.\n   >>> {error}", module="main/Client")
            await ctx.respond(f"An uncaught error occured while running the command. (don't worry, developers will fix this soon)\n```\n{error}\n```")

# Help Commands
help_cmds = client.create_group("help", "Commands used for getting command help in the bot.")

@help_cmds.command(
    name="list",
    description="Get a list of all bot commands, or search for specific commands."
)
@option(name="search", description="Search query for looking-up commands", type=str, default=None)
async def help_list(ctx: ApplicationContext, search: str = None):
    """Get a list of all bot commands, or search for specific commands."""
    commandsdb = _commands.fetch_raw()
    commands_list = str()
    localembed = None

    if search is not None:
        for _command in commandsdb:
            if (search in _command) and (commandsdb[_command]["type"] != "DevTools"):
                commands_list += f"`/{_command}` "
        if commands_list == "":
            commands_list = "*No commands were found*"
        localembed = discord.Embed(title="Isobot Command Help", description=f"**Bot Commands:**\n{commands_list}", color=color)
        localembed.set_footer(text=f"Search results for \"{search}\"")
    
    else:
        economy_commands = str()
        levelling_commands = str()
        utility_commands = str()
        fun_commands = str()
        reddit_commands = str()
        afk_commands = str()
        automod_moderation_commands = str()
        serverconfig_commands = str()
        maths_commands = str()
        other_commands = str()
        for _command in commandsdb:
            command_type = commandsdb[_command]["type"]
            if commandsdb[_command]["type"] != "DevTools":
                if command_type == "economy system" or command_type == "minigames": economy_commands += f"`/{_command}` "
                elif command_type == "levelling": levelling_commands += f"`/{_command}` "
                elif command_type == "general utilities": utility_commands += f"`/{_command}` "
                elif command_type == "fun": fun_commands += f"`/{_command}` "
                elif command_type == "reddit media": reddit_commands += f"`/{_command}` "
                elif command_type == "AFK system": afk_commands += f"`/{_command}` "
                elif command_type == "automod" or command_type == "moderation": automod_moderation_commands += f"`/{_command}` "
                elif command_type == "serverconfig": serverconfig_commands += f"`/{_command}` "
                elif command_type == "maths": maths_commands += f"`/{_command}` "
                else: other_commands += f"`/{_command}` "
                
        commands_list = f"**:money_with_wings: Economy System:**\n{economy_commands}\n\n**:arrow_up: Levelling System:**\n{levelling_commands}\n\n**:toolbox: Utilities:**\n{utility_commands}\n\n**:joy: Fun Commands:**\n{fun_commands}\n\n**:crescent_moon: AFK System**\n{afk_commands}\n\n**:tools: Moderation and Automod:**\n{automod_moderation_commands}\n\n**:gear: Server Configuration:**\n{serverconfig_commands}\n\n**:1234: Maths Commands:**\n{maths_commands}\n\n**:frame_photo: Reddit Media Commands:**\n{reddit_commands}\n\n**:sparkles: Miscellaneous:**\n{other_commands}"
        localembed = discord.Embed(title="Isobot Command Help", description=commands_list, color=color)
        localembed.set_footer(text="Run \"/help info\" to get more information on a command.")
    await ctx.respond(embed=localembed)

@help_cmds.command(
    name="info",
    description="Get detailed information on a specific isobot command."
)
@option(name="command", description="The name of the command you want help on.", type=str)
async def help_info(ctx: ApplicationContext, command: str):
    """Get detailed information on a specific isobot command."""
    commandsdb = _commands.fetch_raw()
    try:
        localembed = discord.Embed(
            title=f"{commandsdb[command]['name']} Command (/{command})",
            description=commandsdb[command]['description'],
            color=color
        )
        localembed.add_field(name="Command Type", value=commandsdb[command]['type'], inline=False)
        if commandsdb[command]['cooldown'] is not None:
            localembed.add_field(name="Cooldown", value=f"{str(datetime.timedelta(seconds=commandsdb[command]['cooldown']))}", inline=False)
        localembed.add_field(name="Usable By", value=commandsdb[command]['usable_by'], inline=False)
        if commandsdb[command]['args'] is not None:
            args = ""
            for arg in commandsdb[command]['args']: args += f"`{arg}` "
            localembed.add_field(name="Arguments", value=args, inline=False)
        if commandsdb[command]['bugged'] is True:
            localembed.set_footer(text="⚠ This command might be bugged (experiencing issues), but will be fixed later.")
        if commandsdb[command]['disabled'] is True:
            localembed.set_footer(text="⚠ This command is currently disabled")
        await ctx.respond(embed=localembed)
    except KeyError:
        return await ctx.respond(
            embed=discord.Embed(description=f"No results found for {command}."),
            ephemeral=True
        )

# Cog Commands (these cannot be moved into a cog)
cogs = client.create_group("cog", "Commands for working with isobot cogs.")

@cogs.command(
    name="load",
    description="Loads a cog."
)
@option(name="cog", description="What cog do you want to load?", type=str)
async def load(ctx: ApplicationContext, cog: str):
    """Loads a cog."""
    if ctx.author.id != 738290097170153472:
        return await ctx.respond("You can't use this command!", ephemeral=True)
    try:
        client.load_extension(f"cogs.{cog}")
        await ctx.respond(
            embed=discord.Embed(
                description=f"{cog} cog successfully loaded.",
                color=discord.Color.green()
            )
        )
    except discord.errors.ExtensionNotFound:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"{cog} failed to load",
                description="Cog does not exist.",
                color=discord.Color.red()
            )
        )
    except discord.errors.ExtensionAlreadyLoaded:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"{cog} failed to load",
                description="Cog is already loaded to the client.",
                color=discord.Color.red()
            )
        )

@cogs.command(
    name="disable",
    description="Disables a cog."
)
@option(name="cog", description="What cog do you want to disable?", type=str)
async def disable(ctx: ApplicationContext, cog: str):
    """Disables a cog."""
    if ctx.author.id != 738290097170153472:
        return await ctx.respond("You can't use this command!", ephemeral=True)
    try:
        client.unload_extension(f"cogs.{cog}")
        await ctx.respond(
            embed=discord.Embed(
                description=f"{cog} cog successfully disabled.",
                color=discord.Color.green()
            )
        )
    except discord.errors.ExtensionNotFound:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"{cog} failed to disable",
                description="Cog does not exist.",
                color=discord.Color.red()
            )
        )

@cogs.command(
    name="reload",
    description="Reloads a cog."
)
@option(name="cog", description="What cog do you want to reload?", type=str)
async def reload(ctx: ApplicationContext, cog: str):
    """Reloads a cog."""
    if ctx.author.id != 738290097170153472:
        return await ctx.respond("You can't use this command!", ephemeral=True)
    try:
        client.reload_extension(f"cogs.{cog}")
        await ctx.respond(
            embed=discord.Embed(
                description=f"{cog} cog successfully reloaded.",
                color=discord.Color.green()
            )
        )
    except discord.errors.ExtensionNotFound:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"{cog} failed to reload",
                description="Cog does not exist.",
                color=discord.Color.red()
            )
        )

# Settings commands
config = client.create_group("settings", "Commands used to change bot settings.")

@config.command(
    name="levelup_messages",
    description="Configure whether you want to be notified for level ups or not."
)
@option(name="enabled", description="Do you want this setting enabled?", type=bool)
async def levelup_messages(ctx: ApplicationContext, enabled: bool):
    """Configure whether you want to be notified for level ups or not."""
    if settings.fetch_setting(ctx.author.id, "levelup_messages") == enabled:
        return await ctx.respond("This is already done.", ephemeral=True)
    settings.edit_setting(ctx.author.id, "levelup_messages", enabled)
    localembed = discord.Embed(
        description="Setting successfully updated.",
        color=discord.Color.green()
    )
    await ctx.respond(embed=localembed)

# Extra commands
@client.slash_command(
    name="delete_my_data",
    description="Deletes all of your isobot data permanently."
)
async def delete_my_data(ctx: ApplicationContext):
    """Deletes all of your isobot data permanently."""
    currency.delete_user(ctx.author.id)
    levelling.delete_user(ctx.author.id)
    items.delete_user(ctx.author.id)
    userdata.delete_user(ctx.author.id)
    weather.delete_user(ctx.author.id)
    localembed = discord.Embed(title=":white_check_mark: Successfully deleted all of your isobot data.", color=discord.Color.green())
    localembed.add_field(
        name="What has been deleted",
        value="- Your currency wallet and bank data\n- Your user levels\n- Items in your inventory\n- Weather save data\n- All of your isobot user settings"
    )
    localembed.add_field(
        name="What has not been deleted",
        value="- Any isobot data relating to your servers"
    )
    await ctx.respond(embed=localembed, ephemeral=True)

@client.slash_command(
    name="credits",
    description="See the credits for isobot's development."
)
async def credits(ctx: ApplicationContext):
    """See the credits for isobot's development."""
    localembed = discord.Embed(
        title="Credits",
        description="A very big thank you to everyone who has helped support the isobot project's development! :)\n\n**Head Devs:**\n- @notsniped (owner)\n- @dtxc (head-dev)\n- @XyrenChess (head-dev)\n\nisobot (C) 2020-2024\nNKA (C) 2022-2024",
        color=color
    )
    await ctx.respond(embed=localembed)

# Initialization
active_cogs = (
    "economy",
    "maths",
    "reddit",
    "moderation",
    "minigames",
    "automod",
    "serverconfig",
    "isobank",
    "levelling",
    "fun",
    "utils",
    "afk",
    # "osu",  Disabled due to ossapi library metadata issues. (will probably remove osu cog anyway, because cog code is outdated with ossapi library)
    "weather",
    "isocard"
)
i = 1
cog_errors = 0
for x in active_cogs:
    s.log(f"[main/Cogs] Loading isobot '{x}' Cog ({i}/{len(active_cogs)})")
    i += 1
    try: client.load_extension(f"cogs.{x}")
    except discord.errors.ExtensionFailed as e:
        cog_errors += 1
        logger.error(f"Cog '{x}' failed to load: {e}", module="main/Cogs")
if cog_errors == 0: s.log(f"[main/Cogs] {colors.green}All cogs successfully loaded.{colors.end}")
else: s.log(f"[main/Cogs] {colors.yellow}{cog_errors}/{len(active_cogs)} cogs failed to load.{colors.end}")
s.log("--------------------")
s.log(f"[main/Client] Starting client in {f'{colors.cyan}Replit mode{colors.end}' if api.auth.get_mode() else f'{colors.orange}local mode{colors.end}'}...")
if api.auth.get_mode(): client.run(os.getenv("TOKEN"))
else: client.run(api.auth.get_token())




# btw i use arch
