#Imports
import os
import os.path
import psutil
import json
import time, datetime
import discord
import asyncio
import random
import praw
import api.auth
import utils.logger, utils.ping
from framework import *
from math import floor, sqrt
from random import randint
import framework.isobot.currency, framework.isobot.colors, framework.isobank.authorize, framework.isobank.manager, framework.isobot.embedengine
from discord import ApplicationContext, option
from discord.ext import commands, tasks
from discord.ext.commands import *
from threading import Thread

# Slash option types:
# Just use variable types to define option types.
# For example, if the option has to be only str:
# @option(name="something", description="A description", type=str)

#Variables
client = discord.Bot()
color = discord.Color.random()
wdir = os.getcwd()
reddit = praw.Reddit(client_id='_pazwWZHi9JldA', client_secret='1tq1HM7UMEGIro6LlwtlmQYJ1jB4vQ', user_agent='idk', check_for_async=False)
with open('database/currency.json', 'r') as f: currency = json.load(f)
with open('database/warnings.json', 'r') as f: warnings = json.load(f)
with open('database/items.json', 'r') as f: items = json.load(f)
with open('config/shop.json', 'r') as f: shopitem = json.load(f)
with open('database/presence.json', 'r') as f: presence = json.load(f)
with open('database/levels.json', 'r') as f: levels = json.load(f)
with open('config/commands.json', 'r') as f: commandsdb = json.load(f)
with open('database/automod.json', 'r') as f: automod_config = json.load(f)

with open('database/special/new_years_2022.json', 'r') as f: presents = json.load(f)  # Temp

#Pre-Initialization Commands
def timenow(): datetime.datetime.now().strftime("%H:%M:%S")
def save():
    with open('database/currency.json', 'w+') as f: json.dump(currency, f, indent=4)
    with open('database/warnings.json', 'w+') as f: json.dump(warnings, f, indent=4)
    with open('database/items.json', 'w+') as f: json.dump(items, f, indent=4)
    with open('database/presence.json', 'w+') as f: json.dump(presence, f, indent=4)
    with open('database/levels.json', 'w+') as f: json.dump(levels, f, indent=4)
    with open('database/automod.json', 'w+') as f: json.dump(automod_config, f, indent=4)
    with open('database/special/new_years_2022.json', 'w+') as f: json.dump(presents, f, indent=4)  # Temp

def get_user_networth(user_id:int):
    nw = currency["wallet"][str(user_id)] + currency["bank"][str(user_id)]
    #for e in items[str(user_id)]:
    #    if e != 0: nw += shopitem[e]["sell price"]
    return nw

if not os.path.isdir("logs"):
    os.mkdir('logs')
    try:
        open('logs/info-log.txt', 'x')
        utils.logger.info("Created info log", nolog=True)
        time.sleep(0.5)
        open('logs/error-log.txt', 'x')
        utils.logger.info("Created error log", nolog=True)
        time.sleep(0.5)
        open('logs/currency.log', 'x')
        utils.logger.info("Created currency log", nolog=True)
    except Exception as e: utils.logger.error(f"Failed to make log file: {e}", nolog=True)

#Classes
class plugins:
    economy = True
    moderation = True
    levelling = False
    music = False

class ShopData:
    def __init__(self, db_path: str):
        self.db_path = db_path 
        with open(db_path, 'r') as f: self.config = json.load(f)
        
    def get_item_ids(self) -> list:
        json_list = list()
        for h in self.config: json_list.append(str(h))
        return json_list
    
    def get_item_names(self) -> list:
        json_list = list()
        for h in self.config: json_list.append(str(h["stylized name"]))
        return json_list

#Framework Module Loader
colors = framework.isobot.colors.Colors()
currency_unused = framework.isobot.currency.CurrencyAPI(f'{wdir}/database/currency.json', f"{wdir}/logs/currency.log")  # Initialize part of the framework (Currency)
# isobank = framework.isobank.manager.IsoBankManager(f"{wdir}/database/isobank/accounts.json", f"{wdir}/database/isobank/auth.json")
isobankauth = framework.isobank.authorize.IsobankAuth(f"{wdir}/database/isobank/auth.json", f"{wdir}/database/isobank/accounts.json")
shop_data = ShopData(f"{wdir}/config/shop.json")

all_item_ids = shop_data.get_item_ids()

#Theme Loader
with open("themes/halloween.theme.json", 'r') as f:
    theme = json.load(f)
    try:
        color_loaded = theme["theme"]["embed_color"]
        color = int(color_loaded, 16)
    except KeyError:
        print(f"{colors.red}The theme file being loaded might be broken. Rolling back to default configuration...{colors.end}")
        color = discord.Color.random()

# Discord UI Views
class PresentsDrop(discord.ui.View):
    @discord.ui.button(label="🎁 Collect Presents", style=discord.ButtonStyle.blurple)
    async def receive(self, button: discord.ui.Button, interaction: discord.Interaction):
        presents_bounty = randint(500, 1000)
        presents[str(interaction.user.id)] += presents_bounty
        save()
        button.disabled = True
        button.label = f"Presents Collected!"
        button.style = discord.ButtonStyle.grey
        newembed = discord.Embed(description=f"{interaction.user.name} collected **{presents_bounty} :gift: presents** from this drop!", color=discord.Color.green())
        await interaction.response.edit_message(embed=newembed, view=self)

#Events
@client.event
async def on_ready():
    print("""
Isobot  Copyright (C) 2022  PyBotDevs/NKA
This program comes with ABSOLUTELY NO WARRANTY; for details run `/w'.
This is free software, and you are welcome to redistribute it
under certain conditions; run `/c' for details.
__________________________________________________""")
    time.sleep(2)
    print(f'Logged in as {client.user.name}.')
    print('Ready to accept commands.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"GitHub"), status=discord.Status.idle)
    print(f'[main/LOG] {colors.green}Status set to IDLE. Rich presence set.{colors.end}')
    print("[main/FLASK] Starting pinger service...")
    utils.ping.host()
    time.sleep(5)
    print("[main/Presents] Presents daemon started.")
    while True:
        print(f"[main/Presents] Dropping new presents in {colors.cyan}#general{colors.end} channel...")
        await asyncio.sleep(randint(180, 300))
        cyberspace_channel_context = await client.fetch_channel(880409977074888718)
        localembed = discord.Embed(title="**:gift: Presents have dropped in chat!**", description="Be the first one to collect them!", color=color)
        await cyberspace_channel_context.send(embed=localembed, view=PresentsDrop()) 

@client.event
async def on_message(ctx):
    if str(ctx.author.id) not in currency['wallet']: currency['wallet'][str(ctx.author.id)] = 5000
    if str(ctx.author.id) not in currency['bank']: currency['bank'][str(ctx.author.id)] = 0
    if str(ctx.guild.id) not in warnings: warnings[str(ctx.guild.id)] = {}
    if str(ctx.author.id) not in warnings[str(ctx.guild.id)]: warnings[str(ctx.guild.id)][str(ctx.author.id)] = []
    if str(ctx.author.id) not in items: items[str(ctx.author.id)] = {}
    if str(ctx.author.id) not in levels: levels[str(ctx.author.id)] = {"xp": 0, "level": 0}
    if str(ctx.guild.id) not in automod_config: automod_config[str(ctx.guild.id)] = \
    {
        "swear_filter": {
            "enabled": False,
            "keywords": {
                "use_default": True,
                "default": ["fuck", "shit", "pussy", "penis", "cock", "vagina", "sex", "moan", "bitch", "hoe", "nigga", "nigger", "xxx", "porn"],
                "custom": []
            }
        }
    }
    for z in shopitem:
        if z in items[str(ctx.author.id)]: pass
        else: items[str(ctx.author.id)][str(z)] = 0
    if str(ctx.author.id) not in presents: presents[str(ctx.author.id)] = 0  # Temp
    save()
    uList = list()
    if str(ctx.guild.id) in presence:
        for x in presence[str(ctx.guild.id)].keys(): uList.append(x)
    else: pass
    for i in uList:
        if i in ctx.content and not ctx.author.bot:
            fetch_user = client.get_user(id(i))
            await ctx.channel.send(f"{fetch_user.display_name} went AFK <t:{floor(presence[str(ctx.guild.id)][str(i)]['time'])}:R>: {presence[str(ctx.guild.id)][str(i)]['response']}")
    if str(ctx.guild.id) in presence and str(ctx.author.id) in presence[str(ctx.guild.id)]:
        del presence[str(ctx.guild.id)][str(ctx.author.id)]
        save()
        m1 = await ctx.channel.send(f"Welcome back {ctx.author.mention}. Your AFK has been removed.")
        await asyncio.sleep(5)
        await m1.delete()
    if not ctx.author.bot:
        levels[str(ctx.author.id)]["xp"] += randint(1, 5)
        xpreq = 0
        for level in range(int(levels[str(ctx.author.id)]["level"])):
            xpreq += 50
            if xpreq >= 5000: break
        if levels[str(ctx.author.id)]["xp"] >= xpreq:
            levels[str(ctx.author.id)]["xp"] = 0
            levels[str(ctx.author.id)]["level"] += 1
            await ctx.author.send(f"{ctx.author.mention}, you just ranked up to **level {levels[str(ctx.author.id)]['level']}**. Nice!")
        save()
        if automod_config[str(ctx.guild.id)]["swear_filter"]["enabled"] == True:
            if automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["use_default"] and any(x in ctx.content.lower() for x in automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["default"]):
                await ctx.delete()
                await ctx.channel.send(f'{ctx.author.mention} watch your language.', delete_after=5)
            elif automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["custom"] is not [] and any(x in ctx.content.lower() for x in automod_config[str(ctx.guild.id)]["swear_filter"]["keywords"]["custom"]):
                await ctx.delete()
                await ctx.channel.send(f'{ctx.author.mention} watch your language.', delete_after=5)

#Error handler
@client.event
async def on_command_error(ctx, error):
    current_time = floor(time.time()).strftime("%H:%M:%S")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f':stopwatch: Not now! Please try after **{str(datetime.timedelta(seconds=int(round(error.retry_after))))}**')
        print(f'[{current_time}] Ignoring exception at {colors.cyan}CommandOnCooldown{colors.end}. Details: This command is currently on cooldown.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.channel.send('You don\'t have permission to do this!', ephemeral=True)
        print(f'[{current_time}] Ignoring exception at {colors.cyan}MissingPermissions{colors.end}. Details: The user doesn\'t have the required permissions.')
    elif isinstance(error, commands.BadArgument):
        await ctx.channel.send(':x: Invalid argument.', delete_after=8)
        print(f'[{current_time}] Ignoring exception at {colors.cyan}BadArgument{colors.end}.')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.channel.send(':x: I don\'t have the required permissions to use this.')
        print(f'[{current_time}] Ignoring exception at {colors.cyan}BotMissingPremissions{colors.end}. Details: The bot doesn\'t have the required permissions.')
    elif isinstance(error, commands.BadBoolArgument):
        await ctx.channel.send(':x: Invalid true/false argument.', delete_after=8)
        print(f'[{current_time}] Ignoring exception at {colors.cyan}BadBoolArgument{colors.end}.')

#Commands
@client.slash_command(
    name="help",
    description="Gives you help with a specific command, or shows a list of all commands"
)
@option(name="command", description="Which command do you need help with?", type=str, default=None)
async def help(ctx: ApplicationContext, command:str=None):
    if command is not None:
        try:
            localembed = discord.Embed(title=f"{commandsdb[command]['name']} Command (/{command})", description=commandsdb[command]['description'], color=color)
            localembed.add_field(name="Command Type", value=commandsdb[command]['type'], inline=False)
            if commandsdb[command]['cooldown'] is not None: localembed.add_field(name="Cooldown", value=f"{str(datetime.timedelta(seconds=commandsdb[command]['cooldown']))}", inline=False)
            localembed.add_field(name="Usable By", value=commandsdb[command]['usable_by'], inline=False)
            if commandsdb[command]['args'] is not None:
                r = ""
                for x in commandsdb[command]['args']: r += f"`{x}` "
                localembed.add_field(name="Arguments", value=r, inline=False)
            if commandsdb[command]['bugged'] == True: localembed.set_footer(text="⚠ This command might be bugged (experiencing issues), but will be fixed later.")
            if commandsdb[command]['disabled'] == True: localembed.set_footer(text="⚠ This command is currently disabled")
            await ctx.respond(embed=localembed)
        except KeyError: return await ctx.respond(embed=discord.Embed(description=f"No results found for {command}."), ephemeral=True)
    else:
        r = ""
        for x in commandsdb: 
            if commandsdb[x]["type"] != "DevTools": r += f"`/{x}`\n"
        localembed = discord.Embed(title="Isobot Command Help", description=f"**Bot Commands:**\n{r}", color = color)
        user = client.fetch_user(ctx.author.id)
        await user.send(embed=localembed)
        await ctx.respond("Check your direct messages.", ephemeral=True)

@client.slash_command(
    name='balance', 
    description='Shows your own or another user\'s balance.'
)
@option(name="user", description="Which user do you want to view information on?", type=discord.User, default=None)
async def balance(ctx: ApplicationContext, user=None):
    try:
        if user == None: user = ctx.author
        try:
            e = discord.Embed(title=f'{user.display_name}\'s balance', color=color)
            e.add_field(name="🎁 Presents", value=f'{presents[str(user.id)]} presents', inline=False)
            e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(user.id)]} coin(s)', inline=True)
            e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(user.id)]} coin(s)', inline=True)
            e.add_field(name="Networth", value=f"{get_user_networth(user.id)} coin(s)", inline=True)
            await ctx.respond(embed=e)
        except: await ctx.respond('Looks like that user is not indexed in our server. Try again later.', ephemeral=True)
    except Exception as e: await ctx.respond(f'An error occured: `{e}`. This has automatically been reported to the devs.')

@client.slash_command(
    name='deposit',
    description='Deposits a specified amount of cash into the bank.'
)
@option(name="amount", description="Specify an amount to deposit (use 'max' for everything)", type=str)
async def deposit(ctx: ApplicationContext, amount):
    if plugins.economy:
        if not amount.isdigit():
            if str(amount) == "max": amount = currency["wallet"][str(ctx.author.id)]
            else: return await ctx.respond("The amount must be a number, or `max`.", ephemeral=True)
        elif currency['bank'] == 0: return await ctx.respond('You don\'t have anything in your bank account.', ephemeral=True)
        elif int(amount) <= 0: return await ctx.respond('The amount to deposit must be more than `0` coins!', ephemeral=True)
        elif int(amount) > currency["wallet"][str(ctx.author.id)]: return await ctx.respond('The amount to deposit must not be more than what you have in your wallet!', ephemeral=True)
        currency["wallet"][str(ctx.author.id)] -= int(amount)
        currency["bank"][str(ctx.author.id)] += int(amount)
        localembed = discord.Embed(title="Deposit successful", description=f"You deposited `{amount}` coin(s) to your bank account.", color=color)
        localembed.add_field(name="You previously had", value=f"`{currency['bank'][str(ctx.author.id)]} coins` in your bank account")
        localembed.add_field(name="Now you have", value=f"`{currency['bank'][str(ctx.author.id)] + amount} coins` in your bank account")
        await ctx.respond(embed=localembed)
        save()

@client.slash_command(
    name='withdraw',
    description='Withdraws a specified amount of cash from the bank.'
)
@option(name="amount", description="Specify an amount to withdraw (use 'max' for everything)", type=str)
async def withdraw(ctx: ApplicationContext, amount):
    if plugins.economy:
        if not amount.isdigit():
            if str(amount) == "max": amount = currency["wallet"][str(ctx.author.id)]
            else: return await ctx.respond("The amount must be a number, or `max`.", ephemeral=True)
        elif currency['bank'] == 0: return await ctx.respond('You don\'t have anything in your bank account.', ephemeral=True)
        elif int(amount) <= 0: return await ctx.respond('The amount to withdraw must be more than `0` coins!', ephemeral=True)
        elif int(amount) > currency["bank"][str(ctx.author.id)]: return await ctx.respond('The amount to withdraw must not be more than what you have in your bank account!', ephemeral=True)
        currency["wallet"][str(ctx.author.id)] += int(amount)
        currency["bank"][str(ctx.author.id)] -= int(amount)
        localembed = discord.Embed(title="Withdraw successful", description=f"You withdrew `{amount}` coin(s) from your bank account.", color=color)
        localembed.add_field(name="You previously had", value=f"`{currency['wallet'][str(ctx.author.id)]} coins` in your wallet")
        localembed.add_field(name="Now you have", value=f"`{currency['wallet'][str(ctx.author.id)] + amount} coins` in your wallet")
        await ctx.respond(embed=localembed)
        await ctx.respond(f'You withdrew `{amount}` coin(s) from your bank account.')
        save()

@client.slash_command(
    name='work',
    description='Work for a 30-minute shift and earn cash.'
)
@commands.cooldown(1, 1800, commands.BucketType.user)
async def work(ctx: ApplicationContext):
    if plugins.economy:
        i = randint(10000, 20000)
        currency['wallet'][str(ctx.author.id)] += i
        save()
        await ctx.respond(f'{ctx.author.mention} worked for a 30-minute shift and earned {i} coins.')

@client.slash_command(
    name='daily',
    description='Claims your daily (every 24 hours)'
)
@commands.cooldown(1, 43200, commands.BucketType.user)
async def daily(ctx: ApplicationContext):
    if plugins.economy:
        currency['wallet'][str(ctx.author.id)] += 10000
        save()
        await ctx.respond(f'You claimed 10000 coins from the daily reward. Check back in 24 hours for your next one!')

@client.slash_command(
    name='weekly',
    description='Claims your weekly (every 7 days)'
)
@commands.cooldown(1, 302400, commands.BucketType.user)
async def weekly(ctx: ApplicationContext):
    if plugins.economy:
        currency['wallet'][str(ctx.author.id)] += 45000
        save()
        await ctx.respond(f'You claimed 45000 coins from the weekly reward. Check back in 7 days for your next one!')

@client.slash_command(
    name='monthly',
    description='Claims your monthly (every 31 days)'
)
@commands.cooldown(1, 1339200, commands.BucketType.user)
async def monthly(ctx: ApplicationContext):
    if plugins.economy:
        currency['wallet'][str(ctx.author.id)] += 1000000
        save()
        await ctx.respond(f'You claimed 1000000 coins from the monthly reward. Check back in 1 month for your next one!')

@client.slash_command(
    name='beg', 
    description='Begs for some quick cash'
)
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx: ApplicationContext):
    if not plugins.economy: return
    names = [
        "A random person",
        "Your friend",
        "Your boss",
        "The quiet kid",  # bruh i dont like giving money to others
        "Your mom",
        "The fart you have been holding for way too long",
        "Notch",
        "Jeff Bezos",
        "Elon Musk",
        "peppy",
        "Steve Jobs",
        "MrBeast",
        "Pewdiepie",
        "Archie",
        "Archisha",
        "notsniped",
        "Discord",
        "notsniped's imaginary gf",
        "Technoblade"
    ]
    fail_responses = [
        "Maybe another day.",
        "Hell nah.",
        "Sorry I don't have any cash on me.",
        "The atm was out of order.",
        "I have nothing to spare.",
        "I'd rather spend my money to buy some airpods rather than giving it to you.",
        "Stop begging. It makes you look like a baby.",
        "Go get a life.",
        "Stop begging. Get a job.",
        "I think I know what you're gonna do with that money.",
        "Debloat notsniped's code and he will probably give you money."
    ]
    if (randint(1, 100) >= 50):
        x = randint(10, 100)
        currency["wallet"][str(ctx.author.id)] += x
        save()
        await ctx.respond(embed=discord.Embed(title=random.choice(names), description=f'"Oh you poor beggar, here\'s {x} coin(s) for you. Hope it helps!"'))
    else: await ctx.respond(embed=discord.Embed(title=random.choice(names), description=f'"{random.choice(fail_responses)}"'))

@client.slash_command(
    name='scout', 
    description='Scouts your area for coins'
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def scout(ctx: ApplicationContext):
    if not plugins.economy: return
    chance = randint(1, 100)
    if (randint(1, 100) <= 90):
        x = randint(550, 2000)
        if items[str(ctx.author.id)]['binoculars'] >= 1:
            x *= 1.425
            x = floor(x)
        else: pass
        currency["wallet"][str(ctx.author.id)] += x
        save()
        await ctx.respond(embed=discord.Embed(title='What you found', description=f'You searched your area and found {x} coin(s)!'))
    else: await ctx.respond(embed=discord.Embed(title='What you found', description='Unfortunately no coins for you :('))

@client.slash_command(
    name='give',
    description='Gives any amount of cash to someone else'
)
@option(name="user", description="Who do you want to give cash to?", type=discord.User)
@option(name="amount", description="How much do you want to give?", type=int)
async def give(ctx: ApplicationContext, user:discord.User, amount:int):
    if not plugins.economy: return
    if amount <= 0: return await ctx.respond('The amount you want to give must be greater than `0` coins!', ephemeral=True)
    if amount > int(currency['wallet'][str(ctx.author.id)]): return await ctx.respond('You don\'t have enough coins in your wallet to do this.', ephemeral=True)
    else:
        currency['wallet'][str(ctx.author.id)] -= amount
        currency['wallet'][str(user.id)] += amount
        save()
        await ctx.respond(f':gift: {ctx.author.mention} just gifted {amount} coin(s) to {user.display_name}!')

@client.slash_command(
    name='rob',
    description='Robs someone for their money'
)
@option(name="user", description="Who do you want to rob?", type=discord.User)
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx: ApplicationContext, user:discord.User):
    if not plugins.economy: return
    if currency['wallet'][str(user.id)] < 5000: return await ctx.respond('They has less than 5000 coins on them. Don\'t waste your time...') 
    elif currency['wallet'][str(ctx.author.id)] < 5000: return await ctx.respond('You have less than 5k coins in your wallet. Play fair dude.')
    if randint(1, 100) <= 50:
        x = randint(5000, currency['wallet'][str(user.id)])
        currency['wallet'][str(ctx.author.id)] += x
        currency['wallet'][str(user.id)] -= x
        await ctx.respond(f'You just stole {x} coins from {user.display_name}! Feels good, doesn\'t it?')
    else:
        x = randint(5000, currency['wallet'][str(ctx.author.id)])
        currency['wallet'][str(ctx.author.id)] -= x
        currency['wallet'][str(user.id)] += x
        await ctx.respond(f'LOL YOU GOT CAUGHT! You paid {user.display_name} {x} coins as compensation for your action.')
    save()

@client.slash_command(
    name='bankrob',
    description='Raids someone\'s bank account'
)
@option(name="user", description="Whose bank account do you want to raid?", type=discord.User)
@commands.cooldown(1, (60*5), commands.BucketType.user)
async def bankrob(ctx: ApplicationContext, user:discord.User):
    if not plugins.economy: return
    if currency['wallet'][str(user.id)] < 10000: return await ctx.respond('You really want to risk losing your life to a poor person? (imagine robbing someone with < 10k net worth)')
    elif currency['wallet'][str(ctx.author.id)] < 10000: return await ctx.respond('You have less than 10k in your wallet. Don\'t be greedy.')
    if randint(1, 100) <= 20:
        x = randint(10000, currency['wallet'][str(user.id)])
        currency['wallet'][str(ctx.author.id)] += x
        currency['bank'][str(user.id)] -= x
        await ctx.respond(f'You raided {user.display_name}\'s bank and ended up looting {x} coins from them! Now thats what I like to call *success*.')
    else:
        x = 10000
        currency['wallet'][str(ctx.author.id)] -= x
        await ctx.respond(f'Have you ever thought of this as the outcome? You failed AND ended up getting caught by the police. You just lost {x} coins, you absolute loser.')

@client.slash_command(
    name='inventory', 
    description='Shows the items you (or someone else) own'
)
@option(name="user", description="Whose inventory you want to view?", type=discord.User, default=None)
async def inventory(ctx: ApplicationContext, user:discord.User = None):
    if not plugins.economy: return
    if user == None: user = ctx.author
    localembed = discord.Embed(title=f'{user.display_name}\'s Inventory')
    localembed.add_field(name='Utility', value=f'Hunting Rifle `ID: rifle`: {items[str(user.id)]["rifle"]}\nFishing Rod `ID: fishingpole`: {items[str(user.id)]["fishingpole"]}\nShovel `ID: shovel`: {items[str(user.id)]["shovel"]}', inline=False)
    localembed.add_field(name='Sellables', value=f'Rock `ID: rock`: {items[str(user.id)]["rock"]}\nAnt `ID: ant`: {items[str(user.id)]["ant"]}\nStickbug `ID: stickbug`: {items[str(user.id)]["stickbug"]}\nSkunk `ID: skunk`: {items[str(user.id)]["skunk"]}\nBoar `ID: boar`: {items[str(user.id)]["boar"]}\nDeer `ID: deer`: {items[str(user.id)]["deer"]}\nDragon `ID: dragon`: {items[str(user.id)]["dragon"]}\nGold `ID: gold`: {items[str(user.id)]["gold"]}', inline=False)
    localembed.add_field(name='Power-ups', value=f'Binoculars `ID: binoculars`: {items[str(user.id)]["binoculars"]}', inline=False)
    await ctx.respond(embed=localembed)

@client.slash_command(
    name='shop',
    description='Views and buys items from the shop'
)
@option(name="item", description="Specify an item to view.", type=str, default=None, choices=all_item_ids)
async def shop(ctx: ApplicationContext, item:str=None):
    if not plugins.economy: return
    if item == None:
        localembed = discord.Embed(
            title='The Shop!', 
            description='**Tools**\n\n1) Hunting Rifle `ID: rifle`: A tool used for hunting animals. (10000 coins)\n2) Fishing Pole `ID: fishingpole`: A tool used for fishing. It lets you use /fish command. (6500 coins)\n3) Shovel `ID: shovel`: You can use this tool to dig stuff from the ground. (3000 coins)\n4) Binoculars `ID: binoculars`: Try scouting with these binoculars, maybe you can find more with it. (14850 coins)'
        )
        localembed.set_footer(text='Page 1 | Tools | This command is in development. More items will be added soon!')
        await ctx.respond(embed=localembed)
    else:
        try:
            localembed = discord.Embed(
                title=shopitem[item]['stylized name'],
                description=shopitem[item]['description']
            )
            localembed.add_field(name='Buying price', value=shopitem[item]['buy price'], inline=True)
            localembed.add_field(name='Selling price', value=shopitem[item]['sell price'], inline=True)
            localembed.add_field(name='In-store', value=shopitem[item]['available'], inline=True)
            localembed.add_field(name='ID', value=f'`{item}`', inline=True)
            await ctx.respond(embed=localembed)
        except KeyError: await ctx.respond('That item isn\'t in the shop, do you are have stupid?')

@client.slash_command(
    name='buy',
    description='Buys an item from the shop'
)
@option(name="name", description="What do you want to buy?", type=str, choices=all_item_ids)
@option(name="quantity", description="How many do you want to buy?", type=int, default=1)
async def buy(ctx: ApplicationContext, name: str, quantity: int=1):
    if not plugins.economy: return
    try:
        amt = shopitem[name]['buy price'] * quantity
        if (currency['wallet'][str(ctx.author.id)] < amt): return await ctx.respond('You don\'t have enough balance to buy this.')
        if (shopitem[name]['available'] == False): return await ctx.respond('You can\'t buy this item **dood**')
        if (quantity <= 0): return await ctx.respond('The specified quantity cannot be less than `1`!')
        currency['wallet'][str(ctx.author.id)] -= int(amt)
        items[str(ctx.author.id)][str(name)] += quantity
        save()
        await ctx.respond(embed=discord.Embed(title=f'You just bought {quantity} {shopitem[name]["stylized name"]}!', description='Thank you for your purchase.', color=discord.Color.green()))
    except KeyError: await ctx.respond('That item doesn\'t exist.')

@client.slash_command(
    name='sell',
    description='Sells an item from your inventory in exchange for cash'
)
@option(name="name", description="What do you want to sell?", type=str, choices=all_item_ids)
@option(name="quantity", description="How many do you want to sell?", type=int, default=1)
async def sell(ctx: ApplicationContext, name: str, quantity: int=1):
    try:
        if shopitem[name]["sellable"] != True: return await ctx.respond('Dumb, you can\'t sell this item.')
        if quantity > items[str(ctx.author.id)][str(name)]: return await ctx.respond('You can\'t sell more than you have.')
        items[str(ctx.author.id)][str(name)] -= quantity
        ttl = shopitem[name]["sell price"]*quantity
        currency["wallet"][str(ctx.author.id)] += int(ttl)
        save()
        localembed = discord.Embed(title='Item sold', description=f'You successfully sold {quantity} {name} for {ttl} coins!', color=color)
        localembed.set_footer(text='Thank you for your business.')
        await ctx.respond(embed=localembed)
    except KeyError: await ctx.respond('what are you doing that item doesn\'t even exist')
    except Exception as e: await ctx.respond(f'An error occured while processing this request. ```{e}```')

@client.slash_command(
    name='hunt',
    description='Pull out your rifle and hunt down animals'
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def hunt(ctx: ApplicationContext):
    if not plugins.economy: return
    if items[str(ctx.author.id)]['rifle'] == 0: return await ctx.respond('I\'d hate to see you hunt with your bare hands. Please buy a hunting rifle from the shop. ||/buy rifle||')
    loot = ['rock', 'ant', 'skunk', 'boar', 'deer', 'dragon', 'nothing', 'died']
    choice = random.choice(loot)
    if choice != "nothing" and choice != "died":
        items[str(ctx.author.id)][choice] += 1
        await ctx.respond(f"You found a {choice} while hunting!")
        save()
    elif (choice == "nothing"): await ctx.respond('You found absolutely **nothing** while hunting.')
    elif (choice == "died"):
        currency[str(ctx.author.id)]['wallet'] -= 1000
        save()
        await ctx.respond('Stupid, you died while hunting and lost 1000 coins...')

@client.slash_command(
    name='fish',
    description='Prepare your fishing rod and catch some fish'
)
@commands.cooldown(1, 45, commands.BucketType.user)
async def fish(ctx: ApplicationContext):
    if not plugins.economy: return
    if (items[str(ctx.author.id)]['fishingpole'] == 0): return await ctx.respond('I don\'t think you can fish with your bare hands... or you can just put yo hands in the water bro **giga chad moment**\nAnyway it\'s just better to buy a fishing pole from the shop. ||/buy fishingpole||')
    loot = ['shrimp', 'fish', 'rare fish', 'exotic fish', 'jellyfish', 'shark', 'nothing']
    choice = random.choice(loot)
    if choice != "nothing":
        items[str(ctx.author.id)][choice] += 1
        save()
        await ctx.respond(f'You found a {choice} while hunting!')
    else: await ctx.respond('Looks like the fish were weary of your rod. You caught nothing.')

@client.slash_command(
    name='dig',
    description='Take your shovel and dig in the ground for some cool stuff!'
)
@commands.cooldown(1, 45, commands.BucketType.user)
async def dig(ctx: ApplicationContext):
    if not plugins.economy: return
    if (items[str(ctx.author.id)]['shovel'] == 0): return await ctx.respond('You\'re too good to have to dig with your bare hands..... at least I hope so. Please buy a shovel from the shop. ||/buy shovel||')
    loot = [
        'coins',
        'shovel',
        'ant',
        'stickbug',
        'rock',
        'gold',
        'coinbomb',
        'rare lootbox',
        'nothing',
        'died',
    ]
    choice = random.choice(loot)
    if (choice == "coins"):
        currency['wallet'][str(ctx.author.id)] += random.randint('1000', '5000')
        save()
        await ctx.respond(f'You went digging and found a bunch of coins. Nice!')
    elif choice != "nothing" and choice != "died":
        items[str(ctx.author.id)][choice] += 1
        save()
        await ctx.respond(f'You found a {choice} while digging ')
    elif (choice == "nothing"): await ctx.respond('After some time of digging you eventually gave up. You got nothing.')
    elif (choice == "died"):
        currency['wallet'][str(ctx.author.id)] -= 2000
        save()
        await ctx.respond('YOU FELL INTO YOUR OWN TRAP AND DIED LMFAO\nYou lost 2000 coins in the process.')

#need help cuz i only got the idea (aka the logic) and not the code detail and stuff
@client.slash_command(
    name='openlootbox',
    description='Opens lootbox(es) in your inventory'
)
@option(name="lootbox", description="What lootbox do you want to open?", type=str, choices=["normal lootbox", "large lootbox", "special lootbox"])
@option(name="amount", description="How many do you want to open?", type=int)
async def openlootbox(ctx: ApplicationContext, lootbox:str, amount:int):
    types = ["normal lootbox", "large lootbox", "special lootbox"]
    if amount <= 0: return await ctx.respond("You can't open 0 or below lootboxes! Don't be stupid.", ephemeral=True)
    if lootbox not in types: return await ctx.respond(f"wtf is {lootbox}?", ephemeral=True)
    ie = shopitem.keys()
    normal_loot = [
        randint(10000, 25000),
        random.choice(list(ie)),
        random.choice(list(ie))
    ]
    large_loot = [
        randint(50000, 75000),
        random.choice(list(ie)),
        random.choice(list(ie)),
        random.choice(list(ie))
    ]
    special_loot = [
        randint(100000, 500000),
        random.choice(list(ie)),
        random.choice(list(ie)),
        random.choice(list(ie)),
        random.choice(list(ie)),
        random.choice(list(ie))
    ]
    localembed = discord.Embed(title="You opened a lootbox!", description=f"The amazing rewards of your {lootbox} lootbox behold you...", color=discord.Color.gold())
    if lootbox == "normal lootbox":
        currency["wallet"][str(ctx.author.id)] += normal_loot[0]
        items[str(ctx.author.id)][normal_loot[1]] += 1
        items[str(ctx.author.id)][normal_loot[2]] += 1
        localembed.add_field(name="Coins gained", value=f"**{normal_loot[0]}** coins", inline=False)
        localembed.add_field(name="Items recieved", value=f"You got **1 {normal_loot[1]}**!\nYou got **1 {normal_loot[2]}**!", inline=False)
    if lootbox == "large lootbox":
        currency["wallet"][str(ctx.author.id)] += large_loot[0]
        items[str(ctx.author.id)][large_loot[1]] += 1
        items[str(ctx.author.id)][large_loot[2]] += 1
        items[str(ctx.author.id)][large_loot[3]] += 1
        localembed.add_field(name="Coins gained", value=f"**{large_loot[0]}** coins", inline=False)
        localembed.add_field(name="Items recieved", value=f"You got **1 {large_loot[1]}**!\nYou got **1 {large_loot[2]}**!\nYou got **1 {large_loot[3]}**!", inline=False)
    if lootbox == "special lootbox":
        currency["wallet"][str(ctx.author.id)] += special_loot[0]
        items[str(ctx.author.id)][special_loot[1]] += 1
        items[str(ctx.author.id)][special_loot[2]] += 1
        items[str(ctx.author.id)][special_loot[3]] += 1
        items[str(ctx.author.id)][special_loot[4]] += 1
        items[str(ctx.author.id)][special_loot[5]] += 1
        localembed.add_field(name="Coins gained", value=f"**{special_loot[0]}** coins", inline=False)
        localembed.add_field(name="Items recieved", value=f"You got **1 {special_loot[1]}**!\nYou got **1 {special_loot[2]}**!\nYou got **1 {special_loot[3]}**!\nYou got **1 {special_loot[4]}**!\nYou got **1 {special_loot[5]}**!", inline=False)
    await ctx.respond(embed=localembed)
    save()

@client.slash_command(
  name='echo',
  description='Sends a bot message in the channel'
)
@option(name="text", description="What do you want to send?", type=str)
async def echo(ctx: ApplicationContext, text:str): 
    await ctx.respond("Echoed!", ephemeral=True)
    await ctx.channel.send(text)

@client.slash_command(
    name='whoami',
    description='Shows information on a user'
)
@option(name="user", description="Who do you want to know about?", type=discord.User, default=None)
async def whoami(ctx: ApplicationContext, user: discord.User=None):
    if user == None: user = ctx.author
    username = user
    displayname = user.display_name
    registered = user.joined_at.strftime("%b %d, %Y, %T")
    pfp = user.avatar_url
    localembed_desc = f"`AKA` {displayname}"
    if str(user.id) in presence[str(ctx.guild.id)]: localembed_desc += f"\n`🌙 AFK` {presence[str(ctx.guild.id)][str(user.id)]['response']} - <t:{floor(presence[str(ctx.guild.id)][str(user.id)]['time'])}>"
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

# DevTools commands
@client.slash_command(
    name='sync',
    description='Syncs all of the local databases with their latest version'
)
async def sync(ctx: ApplicationContext):
    if ctx.author.id != 738290097170153472: return await ctx.respond('Sorry, this command is only for my developer\'s use.')
    try:
        with open('database/currency.json', 'r') as f: currency = json.load(f)
        with open('database/warnings.json', 'r') as f: warnings = json.load(f)
        with open('database/items.json', 'r') as f: items = json.load(f)
        with open('config/shop.json', 'r') as f: shopitem = json.load(f)
        await ctx.respond('Databases resynced.', ephemeral=True)
    except Exception as e:
        print(e)
        await ctx.respond('An error occured while resyncing. Check console.', ephemeral=True)

@client.slash_command(
    name='stroketranslate',
    description='Gives you the ability to make full words and sentences from a cluster of letters'
)
@option(name="strok", description="What do you want to translate?", type=str)
async def stroketranslate(ctx: ApplicationContext, strok: str):
        try:
            if len(strok) > 300: return await ctx.respond("Please use no more than `300` character length", ephemeral=True)
            else:
                with open(f"{os.getcwd()}/config/words.json", "r") as f: words = json.load(f)
                var = str()
                s = strok.lower()
                for i, c in enumerate(s): var += random.choice(words[c])
                return await ctx.respond(f"{var}")
        except Exception as e: return await ctx.respond(f"{type(e).__name__}: {e}")
        var = ''.join(arr)
        await ctx.respond(f"{var}")

@client.slash_command(
    name='prediction',
    description='Randomly predicts a yes/no question.'
)
@option(name="question", description="What do you want to predict?", type=str)
async def prediction(ctx: ApplicationContext, question:str): await ctx.respond(f"My prediction is... **{random.choice(['Yes', 'No'])}!**")

@client.slash_command(
    name='donate',
    description="Donate money to whoever you want"
)
@option(name="id", description="The ID of the user you are donating to", type=str)
@option(name="amount", description="How much do you want to donate?", type=int)
async def donate(ctx: ApplicationContext, id:str, amount):
    if plugins.economy:
        reciever_info = client.get_user(int(id))
        if id not in currency["wallet"]: return await ctx.respond("Unfortunately, we couldn't find that user in our server. Try double-checking the ID you've provided.", ephemeral=True)
        # Prevent self-donations
        if id == ctx.author.id: return await ctx.respond("You can't donate to yourself stupid.", ephemeral=True)
        # Check for improper amount argument values
        if amount < 1: return await ctx.respond("The amount has to be greater than `1`!", ephemeral=True)
        elif amount > 1000000000: return await ctx.respond("You can only donate less than 1 billion coins!", ephemeral=True)
        elif amount > currency["wallet"][str(ctx.author.id)]: return await ctx.respond("You're too poor to be donating that much money lmao")
        # If no improper values, proceed with donation
        try:
            currency["wallet"][str(id)] += amount
            currency["wallet"][str(ctx.author.id)] -= amount
            save()
        except Exception as e: return await ctx.respond(e) 
        localembed = discord.Embed(title="Donation Successful", description=f"You successfully donated {amount} coins to {reciever_info.name}!", color=discord.Color.green())
        localembed.add_field(name="Your ID", value=ctx.author.id, inline=True)
        localembed.add_field(name="Reciever's ID", value=id, inline=True)
        localembed2 = discord.Embed(title="You Recieved a Donation!", description=f"{ctx.author} donated {amount} coins to you!", color=discord.Color.green())
        localembed2.add_field(name="Their ID", value=ctx.author.id, inline=True)
        localembed2.add_field(name="Your ID", value=id, inline=True)
        await ctx.respond(embed=localembed)
        await reciever_info.send(embed=localembed2)
    
@client.slash_command(
    name='modify_balance',
    description="Modifies user balance (Normal Digit: Adds Balance; Negative Digit: Removes Balance)"
)
@option(name="user", description="Specify the user to change their balance", type=discord.User)
@option(name="modifier", description="Specify the balance to modify", type=int)
async def modify_balance(ctx: ApplicationContext, user:discord.User, modifier:int):
    if ctx.author.id != 738290097170153472: return ctx.respond("Sorry, but this command is only for my developer's use.", ephemeral=True)
    try:
        currency["wallet"][str(user.id)] += modifier
        save()
        await ctx.respond(f"{user.name}\'s balance has been modified by {modifier} coins.\n\n**New Balance:** {currency['wallet'][str(user.id)]} coins", ephemeral=True)
    except KeyError: await ctx.respond("That user doesn't exist in the database.", ephemeral=True)

@client.slash_command(
    name="status",
    description="Shows the current client info"
)
async def status(ctx: ApplicationContext):
    os_name = os.name
    sys_ram = str(f"{psutil.virtual_memory()[2]}GiB")
    sys_cpu = str(f"{psutil.cpu_percent(1)}%")
    bot_users = 0
    for x in currency["wallet"].keys(): bot_users += 1
    localembed = discord.Embed(title="Client Info")
    localembed.add_field(name="OS Name", value=os_name)
    localembed.add_field(name="RAM Available", value=sys_ram)
    localembed.add_field(name="CPU Usage", value=sys_cpu)
    localembed.add_field(name="Registered Users", value=f"{bot_users} users", inline=True)
    localembed.add_field(name="Uptime History", value="[here](https://stats.uptimerobot.com/PlKOmI0Aw8)")
    localembed.add_field(name="Release Notes", value="[latest](https://github.com/PyBotDevs/isobot/releases/latest)")
    localembed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.respond(embed=localembed)

@client.slash_command(
    name="gift",
    description="Gifts a (giftable) item to anyone you want"
)
@option(name="user", description="Who do you want to gift to?", type=discord.User)
@option(name="item", description="What do you want to gift?", type=str, choices=all_item_ids)
@option(name="amount", description="How many of these do you want to gift?", type=int, default=1)
async def gift(ctx: ApplicationContext, user:discord.User, item:str, amount:int=1):
    try:
        if amount < 1: return await ctx.respond("You can't gift less than 1 of those!", ephemeral=True)
        elif items[str(ctx.author.id)][item] < amount: return await ctx.respond("You don't have enough of those to gift!", ephemeral=True)
        elif shopitem[item]["giftable"] == False: return await ctx.respond("You can't sell that item!", ephemeral=True)
        items[str(user.id)][item] += amount
        items[str(ctx.author.id)][item] -= amount
        save()
        localembed = discord.Embed(
            title="Gift successful!",
            description=f"You just gifted {amount} **{item}**s to {user.display_name}!",
            color=discord.Color.green()
        )
        localembed.add_field(name="Now they have", value=f"**{items[str(user.id)][item]} {item}**s")
        localembed.add_field(name="and you have", value=f"**{items[str(ctx.author.id)][item]} {item}**s")
        await ctx.respond(embed=localembed)
    except KeyError as e: 
        utils.logger.error(e)
        await ctx.respond(f"wtf is {item}?")
        
@client.slash_command(
    name="afk_set",
    description="Sets your AFK status with a custom response"
)
@option(name="response", description="What do you want your AFK response to be?", type=str, default="I'm AFK")
async def afk_set(ctx: ApplicationContext, response:str="I'm AFK"):
    exctime = time.time()
    if str(ctx.guild.id) not in presence: presence[str(ctx.guild.id)] = {}
    presence[str(ctx.guild.id)][str(ctx.author.id)] = {"type": "afk", "time": exctime, "response": response}
    save()
    localembed = discord.Embed(title=f"{ctx.author.display_name} is now AFK.", description=f"Response: {response}", color=discord.Color.dark_orange())
    await ctx.respond(embed=localembed)

@client.slash_command(
    name="afk_remove",
    description="Removes your AFK status"
)
async def afk_remove(ctx: ApplicationContext):
    try: 
        del presence[str(ctx.guild.id)][str(ctx.author.id)]
        save()
        await ctx.respond(f"Alright {ctx.author.mention}, I've removed your AFK.")
    except KeyError: return await ctx.respond("You weren't previously AFK.", ephemeral=True)

@client.slash_command(
    name="afk_mod_remove",
    description="Removes an AFK status for someone else"
)
@option(name="user", description="Whose AFK status do you want to remove?", type=discord.User)
async def afk_mod_remove(ctx: ApplicationContext, user:discord.User):
    if not ctx.author.guild_permissions.manage_messages: return await ctx.respond("You don't have the required permissions to use this.", ephemeral=True)
    try: 
        del presence[str(ctx.guild.id)][str(user.id)]
        save()
        await ctx.respond(f"{user.display_name}'s AFK has been removed.")
    except KeyError: return await ctx.respond("That user isn't AFK.", ephemeral=True)

@client.slash_command(
    name="autogrind",
    description="Automatically grinds coins and items for you"
)
@commands.cooldown(1, 3600, commands.BucketType.user)
async def autogrind(ctx: ApplicationContext):
    await ctx.respond("Autogrind has started. Please check back in an hour for your rewards.")
    await asyncio.sleep(3600)
    coins_reward = randint(10000, 35000)
    ie = shopitem.keys()
    items_reward = [random.choice(list(ie)), random.choice(list(ie)), random.choice(list(ie))]
    currency["wallet"][str(ctx.author.id)] += coins_reward
    items[str(ctx.author.id)][items_reward[0]] += 1
    items[str(ctx.author.id)][items_reward[1]] += 1
    items[str(ctx.author.id)][items_reward[2]] += 1
    save()
    localembed = discord.Embed(title="Autogrind has completed!", description=f"**Your rewards**\n\nYou got **{coins_reward}** coins!\nYou got **1 {shopitem[items_reward[0]]['stylized name']}**!\nYou got **1 {shopitem[items_reward[1]]['stylized name']}**!\nYou got **1 {shopitem[items_reward[2]]['stylized name']}!**", color=discord.Color.green())
    await ctx.author.send(embed = localembed)

@client.slash_command(
    name="rank",
    description="Shows your rank or another user's rank"
)
@option(name="user", description="Who's rank do you want to view?", type=discord.User, default=None)
async def rank(ctx: ApplicationContext, user:discord.User=None):
    if user == None: user = ctx.author
    try:
        localembed = discord.Embed(title=f"{user.display_name}'s rank", color=color)
        localembed.add_field(name="Level", value=levels[str(user.id)]["level"])
        localembed.add_field(name="XP", value=levels[str(user.id)]["xp"])
        localembed.set_footer(text="Keep chatting to earn levels!", icon_url=ctx.author.avatar_url)
        await ctx.respond(embed = localembed)
    except KeyError: return await ctx.respond("Looks like that user isn't indexed yet. Try again later.", ephemeral=True)

@client.slash_command(
    name="edit_rank",
    description="Edits a user's rank. (DEV ONLY)"
)
@option(name="user", description="Who's rank do you want to edit?", type=discord.User)
@option(name="new_rank", description="The new rank you want to set for the user", type=int)
async def edit_rank(ctx: ApplicationContext, user:discord.User, new_rank:int):
    if ctx.author.id != 738290097170153472: return await ctx.respond("This command isn't for you.", ephemeral=True)
    try:
        levels[str(user.id)]["level"] = new_rank
        await ctx.respond(f"{user.display_name}\'s rank successfully edited. `New Rank: {levels[str(user.id)]['level']}`")
    except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

@client.slash_command(
    name="edit_xp",
    description="Edits a user's XP. (DEV ONLY)"
)
@option(name="user", description="Who's rank do you want to edit?", type=discord.User)
@option(name="new_xp", description="The new xp count you want to set for the user", type=int)
async def edit_xp(ctx: ApplicationContext, user:discord.User, new_xp:int):
    if ctx.author.id != 738290097170153472: return await ctx.respond("This command isn't for you.", ephemeral=True)
    try:
        levels[str(user.id)]["xp"] = new_xp
        await ctx.respond(f"{user.display_name}\'s XP count successfully edited. `New XP: {levels[str(user.id)]['xp']}`")
    except KeyError: return await ctx.respond("That user isn't indexed yet.", ephemeral=True)

@client.slash_command(
    name="repo",
    description="Shows the open-source code links for isobot."
)
async def repo(ctx: ApplicationContext):
    localembed = discord.Embed(title="Source-code Repositories", description="See and contribute to **isobot's [GitHub repository](https://github.com/PyBotDevs/isobot)**\nSee our **[GitHub organization](https://github.com/PyBotDevs)**", color=color)
    await ctx.respond(embed=localembed)

@client.slash_command(
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
async def embedbuilder(ctx: ApplicationContext, title: str, description: str, image_url: str = None, thumbnail_url: str = None, color: int = None, footer_text: str = None, footer_icon_url: str = None):
    await ctx.respond("Embed Built!", ephemeral=True)
    await ctx.channel.send(embed=framework.isobot.embedengine.embed(title, description, image=image_url, thumbnail=thumbnail_url, color=color, footer_text=footer_text, footer_img=footer_icon_url))

@client.slash_command(
    name="networth",
    description="Get your networth, or another user's networth"
)
@option(name="user", description="Whose networth do you want to find?", type=discord.User, default=None)
async def networth(ctx: ApplicationContext, user: discord.User=None):
    if user == None: user = ctx.author
    try:
        ntw = get_user_networth(user.id)
        localembed = discord.Embed(name=f"{user.display_name}'s networth", description=f"{ntw} coins", color=color)
        await ctx.respond(embed=localembed)
    except KeyError: return await ctx.respond("Looks like that user isn't cached yet. Please try again later.", ephemeral=True)

@client.slash_command(
    name="profile",
    description="Shows basic stats about your isobot profile, or someone else's profile stats"
)
@option(name="user", description="Whose isobot profile do you want to view?", type=discord.User, default=None)
async def profile(ctx:  ApplicationContext, user: discord.User = None):
    if user == None: user = ctx.author
    localembed = discord.Embed(title=f"{user.display_name}'s isobot stats", color=color)
    localembed.set_thumbnail(url=user.avatar_url)
    localembed.add_field(name="Level", value=f"Level {levels[str(user.id)]['level']} ({levels[str(user.id)]['xp']} XP)", inline=False)
    localembed.add_field(name="Balance in Wallet", value=f"{currency['wallet'][str(user.id)]} coins", inline=True)
    localembed.add_field(name="Balance in Bank Account", value=f"{currency['bank'][str(user.id)]} coins", inline=True)
    localembed.add_field(name="Net-Worth", value=f"{get_user_networth(user.id)} coins", inline=True)
    # More stats will be added later
    # Maybe I should make a userdat system for collecting statistical data to process and display here, coming in a future update.
    await ctx.respond(embed=localembed)

# New Year's in-game Event Commands
special_event = client.create_group("event", "Commands related to the New Years special in-game event.")

@special_event.command(
    name="leaderboard", 
    description="View the global leaderboard for the special in-game event."
)
async def leaderboard(ctx: ApplicationContext):
    undicted_leaderboard = sorted(presents.items(), key=lambda x:x[1], reverse=True)
    dicted_leaderboard = dict(undicted_leaderboard)
    parsed_output = str()
    y = 1
    for i in dicted_leaderboard:
        if y < 10:
            try:
                if presents[i] != 0:
                    user_context = await client.fetch_user(i)
                    if not user_context.bot and presents[i] != 0:
                        print(i, presents[i])
                        if y == 1: yf = ":first_place:"
                        elif y == 2: yf = ":second_place:"
                        elif y == 3: yf = ":third_place:"
                        else: yf = f"#{y}"
                        parsed_output += f"{yf} **{user_context.name}:** {presents[i]} presents\n"
                        y += 1
            except discord.errors.NotFound: continue
    localembed = discord.Embed(title="New Years Special Event global leaderboard", description=parsed_output, color=color)
    await ctx.respond(embed=localembed)

# Initialization
active_cogs = ["maths", "moderation", "reddit", "minigames", "automod", "isobank"]
i = 1
cog_errors = 0
for x in active_cogs:
    print(f"[main/Cogs] Loading isobot Cog ({i}/{len(active_cogs)})")
    i += 1
    try: client.load_extension(x)
    except Exception as e:
        cog_errors += 1 
        print(f"[main/Cogs] {colors.red}ERROR: Cog \"{x}\" failed to load: {e}{colors.end}")
if cog_errors == 0: print(f"[main/Cogs] {colors.green}All cogs successfully loaded.{colors.end}")
else: print(f"[main/Cogs] {colors.yellow}{cog_errors}/{len(active_cogs)} cogs failed to load.{colors.end}")
print("--------------------")
client.run(api.auth.get_token())




# btw i use arch
