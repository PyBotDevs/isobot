"""Isobot, the bot to make your server (a little bit) better.\n\nisobot (C) NKA 2022-2024.\nRun `/credits` in the Discord bot to see the credits.\n\nWARNING: This client is meant to be run standalone. Not as a Python import."""
# Imports
import os
import os.path
import json
import time
import datetime
import discord, discord.errors
import asyncio
import api.auth
from utils import logger, ping
from math import floor
from random import randint
from framework.isobot import currency, colors, settings
from framework.isobot.db import levelling, items, userdata, automod, presence as _presence
from discord import ApplicationContext, option
from discord.ext import commands
from cogs.isocoin import create_isocoin_key

# Variables
client = discord.Bot()
color = discord.Color.random()

# Pre-Initialization Commands
def initial_setup():
    """Runs the initial setup for isobot's directories.\nThis creates missing directories, new log files, as well as new databases for any missing `.json` database files."""
    try:
        paths = ["database", "config", "logs", "themes"]
        for p in paths:
            if not os.path.isdir(p):
                logger.warn(f"'{p}' directory appears to be missing. Created new directory for '{p}'.", module="main/Setup", nolog=True)
                os.mkdir(p)
    except: logger.error(f"Failed to make directory: {e}", module="main/Setup")
    try:
        databases = ["automod", "currency", "isocard", "isotokens", "items", "levels", "presence", "user_data", "weather"]
        for f in databases:
            if not os.path.isfile(f"database/{f}.json"):
                logger.warn(f"[main/Setup] '{f}.json' was not found in database directory. Creating new database...", module="main/Setup", nolog=True)
                if f == "currency": open(f"database/{f}.json", 'x', encoding="utf-8").write('{"treasury": 1000000, "wallet": {}, "bank": {}}')
                else: open(f"database/{f}.json", 'x', encoding="utf-8").write("{}")
                time.sleep(0.5)
    except IOError as e: logger.error(f"Failed to make database file: {e}", module="main/Setup")
    try:
        if not os.path.isfile("logs/info-log.txt"):
            open('logs/info-log.txt', 'x', encoding="utf-8")
            logger.info("Created info log", module="main/Setup", nolog=True)
            time.sleep(0.5)
        if not os.path.isfile("logs/error-log.txt"):
            open('logs/error-log.txt', 'x', encoding="utf-8")
            logger.info("Created error log", module="main/Setup", nolog=True)
            time.sleep(0.5)
        if not os.path.isfile("logs/currency.log"):
            open('logs/currency.log', 'x', encoding="utf-8")
            logger.info("Created currency log", module="main/Setup", nolog=True)
            time.sleep(0.5)
    except IOError as e: logger.error(f"Failed to make log file: {e}", module="main/Setup", nolog=True)

# Framework Module Loader
colors = colors.Colors()
currency = currency.CurrencyAPI("database/currency.json", "logs/currency.log")
settings = settings.Configurator()
levelling = levelling.Levelling()
items = items.Items()
userdata = userdata.UserData()
automod = automod.Automod()
_presence = _presence.Presence()

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
else: color = discord.Color.random()

# Events
@client.event
async def on_ready():
    """This event is fired when the bot client is ready"""
    print("""
Isobot  Copyright (C) 2022  PyBotDevs/NKA
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
__________________________________________________""")
    time.sleep(1)
    print(f'[main/Client] Logged in as {client.user.name}.\n[main/Client] Ready to accept commands.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="GitHub"), status=discord.Status.idle)
    print(f'[main/Log] {colors.green}Status set to IDLE. Rich presence set.{colors.end}')
    print("[main/Flask] Starting pinger service...")
    ping.host()
    time.sleep(5)

@client.event
async def on_message(ctx):
    """This event is fired whenever a message is sent (in a readable channel)"""
    currency.new_wallet(ctx.author.id)
    currency.new_bank(ctx.author.id)
    create_isocoin_key(ctx.author.id)
    userdata.generate(ctx.author.id)
    settings.generate(ctx.author.id)
    items.generate(ctx.author.id)
    levelling.generate(ctx.author.id)
    automod.generate(ctx.guild.id)
    uList = list()
    presence = _presence.get_raw()
    if str(ctx.guild.id) in presence:
        for userid in presence[str(ctx.guild.id)].keys(): uList.append(userid)
    else: pass
    for user in uList:
        if user in ctx.content and not ctx.author.bot:
            fetch_user = client.get_user(id(user))
            await ctx.channel.send(f"{fetch_user.display_name} went AFK <t:{floor(presence[str(ctx.guild.id)][str(user)]['time'])}:R>: {presence[str(ctx.guild.id)][str(user)]['response']}")
    if str(ctx.guild.id) in presence and str(ctx.author.id) in presence[str(ctx.guild.id)]:
        _presence.remove_afk(ctx.guild.id, ctx.author.id)
        m1 = await ctx.channel.send(f"Welcome back {ctx.author.mention}. Your AFK has been removed.")
        await asyncio.sleep(5)
        await m1.delete()
    if not ctx.author.bot:
        levelling.add_xp(ctx.author.id, randint(1, 5))
        xpreq = 0
        for level in range(levelling.get_level(ctx.author.id)):
            xpreq += 50
            if xpreq >= 5000: break
        if levelling.get_xp(ctx.author.id) >= xpreq:
            levelling.set_xp(ctx.author.id, 0)
            levelling.add_levels(ctx.author.id, 1)
            if settings.fetch_setting(ctx.author.id, "levelup_messages") is True:
                await ctx.author.send(f"{ctx.author.mention}, you just ranked up to **level {levelling.get_level(ctx.author.id)}**. Nice!")
        save()
        if automod_config[str(ctx.guild.id)]["swear_filter"]["enabled"] is True:
            if automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["use_default"] and any(x in ctx.content.lower() for x in automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["default"]):
                await ctx.delete()
                await ctx.channel.send(f'{ctx.author.mention} watch your language.', delete_after=5)
            elif automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["custom"] != [] and any(x in ctx.content.lower() for x in automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["custom"]):
                await ctx.delete()
                await ctx.channel.send(f'{ctx.author.mention} watch your language.', delete_after=5)

# Error handler
@client.event
async def on_application_command_error(ctx: ApplicationContext, error: discord.DiscordException):
    """An event handler to handle command exceptions when things go wrong.\n\nSome exceptions may be pre-handled, but any unhandable exceptions will be logged as an error."""
    current_time = datetime.time().strftime("%H:%M:%S")
    if not api.auth.get_runtime_options()["debug_mode"]:
        if isinstance(error, commands.CommandOnCooldown): await ctx.respond(f":stopwatch: Not now! Please try after **{str(datetime.timedelta(seconds=int(round(error.retry_after))))}**")
        elif isinstance(error, commands.MissingPermissions): await ctx.respond(":warning: You don't have the required server permissions to run this command!", ephemeral=True)
        elif isinstance(error, commands.BadArgument): await ctx.respond(":x: Invalid argument.", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions): await ctx.respond(":x: I don\'t have the required permissions to use this.\nIf you think this is a mistake, please go to server settings and fix isobot's role permissions.")
        elif isinstance(error, commands.BadBoolArgument): await ctx.respond(":x: Invalid true/false argument.", ephemeral=True)
        else:
            logger.error(f"Command failure: An uncaught error occured while running the command.\n   >>> {error}", module="main/Client")
            await ctx.respond(f"An uncaught error occured while running the command. (don't worry, developers will fix this soon)\n```\n{error}\n```")

# Commands
@client.slash_command(
    name="help",
    description="Gives you help with a specific command, or shows a list of all commands"
)
@option(name="command", description="Which command do you need help with?", type=str, default=None)
async def help(ctx: ApplicationContext, command: str = None):
    """Gives you help with a specific command, or shows a list of all commands"""
    commandsdb = _commands.fetch_raw()
    if command is not None:
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
    else:
        commands_list = ""
        for _command in commandsdb:
            if commandsdb[_command]["type"] != "DevTools": commands_list += f"`/{_command}`\n"
        localembed = discord.Embed(title="Isobot Command Help", description=f"**Bot Commands:**\n{commands_list}", color=color)
        await ctx.author.send(embed=localembed)
        await ctx.respond("Check your direct messages.", ephemeral=True)

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
                description="Cog does not exist.",
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

# Initialization
initial_setup()  # Check for any missing sub-directories or databases in bot directory
active_cogs = [
    "economy",
    "maths",
    "reddit",
    "moderation",
    "minigames",
    "automod",
    "isobank",
    "levelling",
    "fun",
    "utils",
    "afk",
    # "osu",  Disabled due to ossapi library metadata issues. (will probably remove osu cog anyway, because cog code is outdated with ossapi library)
    "weather",
    "isocard"
]
i = 1
cog_errors = 0
for x in active_cogs:
    print(f"[main/Cogs] Loading isobot Cog ({i}/{len(active_cogs)})")
    i += 1
    try: client.load_extension(f"cogs.{x}")
    except discord.errors.ExtensionFailed as e:
        cog_errors += 1
        print(f"[main/Cogs] {colors.red}ERROR: Cog '{x}' failed to load: {e}{colors.end}")
if cog_errors == 0: print(f"[main/Cogs] {colors.green}All cogs successfully loaded.{colors.end}")
else: print(f"[main/Cogs] {colors.yellow}{cog_errors}/{len(active_cogs)} cogs failed to load.{colors.end}")
print("--------------------")
if api.auth.get_mode():
    print(f"[main/Client] Starting client in {colors.cyan}Replit mode{colors.end}...")
    client.run(os.getenv("TOKEN"))
else:
    print(f"[main/Client] Starting client in {colors.orange}local mode{colors.end}...")
    client.run(api.auth.get_token())




# btw i use arch
