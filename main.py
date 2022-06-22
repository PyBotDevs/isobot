#Imports
import discord
from discord.ext import commands, tasks
from discord.ext.commands import *
import os, os.path
import json
import time, datetime
import asyncio
import random
import math
import praw
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import api.auth
import utils.logger
import utils.ping

# Slash option types:
# sub command: 1
# sub command group: 2
# string: 3
# int: 4
# bool: 5
# user: 6
# channel: 7
# role: 8

#Variables
client = commands.Bot(command_prefix='s!', intents=discord.Intents.all())  #Saving for later incase needed
#client = discord.Client()
slash = SlashCommand(client, sync_commands=True)
color = discord.Color.random()
wdir = os.getcwd()
reddit = praw.Reddit(client_id='_pazwWZHi9JldA', client_secret='1tq1HM7UMEGIro6LlwtlmQYJ1jB4vQ', user_agent='idk', check_for_async=False)
with open(f'{wdir}/database/currency.json', 'r') as f:
    global currency
    currency = json.load(f)
with open(f'{wdir}/database/warnings.json', 'r') as f:
    global warnings
    warnings = json.load(f)
with open(f'{wdir}/database/items.json', 'r') as f:
    global items
    items = json.load(f)
with open(f'{wdir}/config/shop.json', 'r') as f:
    global shopitem
    shopitem = json.load(f)

#Pre-Initialization Commands
def timenow(): 
    datetime.datetime.now().strftime("%H:%M:%S")
def save():
    with open(f'{wdir}/database/currency.json', 'w+') as f:
        json.dump(currency, f, indent=4)
    with open(f'{wdir}/database/warnings.json', 'w+') as f:
        json.dump(warnings, f, indent=4)
    with open(f'{wdir}/database/items.json', 'w+') as f:
        json.dump(items, f, indent=4)

if os.path.isdir(f'{wdir}/logs'): 
  pass
else:
  try:
    os.mkdir(f'{wdir}/logs')
  except Exception as e:
    utils.logger.error(f"Error while making logs directory: {e} (temporarily skipping dir creation)", nolog=True)
  try:
    open(f'{wdir}/logs/info-log.txt', 'x')
    utils.logger.info("Created info log", nolog=True)
    time.sleep(0.5)
    open(f'{wdir}/logs/error-log.txt', 'x')
    utils.logger.info("Created error log", nolog=True)
  except Exception as e:
    utils.logger.error(f"Failed to make log file: {e}", nolog=True)

#Classes
class colors:
    cyan = '\033[96m'
    red = '\033[91m'
    green = '\033[92m'
    end = '\033[0m'

class plugins:
    economy:bool = True
    moderation:bool = True
    levelling:bool = False
    music:bool = False

#Events
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}.')
    print('Ready to accept commands.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Salad"), status=discord.Status.idle)
    print(f'[main/LOG] {colors.green}Status set to IDLE. Rich presence set.{colors.end}')

@client.event
async def on_message(ctx):
    if (str(ctx.author.id) in currency['wallet']):
        pass
    else:
        currency['wallet'][str(ctx.author.id)] = 5000
    if (str(ctx.author.id) in currency['bank']):
        pass
    else:
        currency['bank'][str(ctx.author.id)] = 0
    if str(ctx.guild.id) in warnings:
        pass
    else:
        warnings[str(ctx.guild.id)] = {}
    if str(ctx.author.id) in warnings[str(ctx.guild.id)]:
        pass
    else:
        warnings[str(ctx.guild.id)][str(ctx.author.id)] = []
    if str(ctx.author.id) in items:
        pass
    else:
        items[str(ctx.author.id)] = {}
        items[str(ctx.author.id)]['rifle'] = 0
        items[str(ctx.author.id)]['fishingpole'] = 0
        items[str(ctx.author.id)]['shovel'] = 0
        items[str(ctx.author.id)]['rock'] = 0
        items[str(ctx.author.id)]['ant'] = 0
        items[str(ctx.author.id)]['skunk'] = 0
        items[str(ctx.author.id)]['boar'] = 0
        items[str(ctx.author.id)]['deer'] = 0
        items[str(ctx.author.id)]['dragon'] = 0
        items[str(ctx.author.id)]['binoculars'] = 0
        items[str(ctx.author.id)]['shark'] = 0
        items[str(ctx.author.id)]['stickbug'] = 0
        items[str(ctx.author.id)]['gold'] = 0
        items[str(ctx.author.id)]['coinbomb'] = 0
        items[str(ctx.author.id)]['jellyfish'] = 0
    save()

#Error handler
@client.event
async def on_command_error(ctx, error):
    current_time = timenow()
    if isinstance(error, CommandNotFound):
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at CommandNotFound. Details: This command does not exist.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}CommandNotFound{colors.end}. Details: This command does not exist.')
        else:
            pass
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(f':stopwatch: Not now! Please try after **{str(datetime.timedelta(seconds=int(round(error.retry_after))))}**')
        if os.name == 'nt':
            print(f'[{current_time}] Ignoring exception at {colors.cyan}CommandOnCooldown{colors.end}. Details: This command is currently on cooldown.')
        else:
            pass
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You don\'t have permission to do this!', hidden=True)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at MissingPermissions. Details: The user doesn\'t have the required permissions.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}MissingPermissions{colors.end}. Details: The user doesn\'t have the required permissions.')
        else:
            pass
    elif isinstance(error, commands.BadArgument):
        await ctx.send(':x: Invalid argument.', delete_after=8)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BadArgument.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BadArgument{colors.end}.')
        else:
            pass
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(':x: I don\'t have the required permissions to use this.')
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BotMissingPermissions.\n Details: The bot doesn\'t have the required permissions.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BotMissingPremissions{colors.end}. Details: The bot doesn\'t have the required permissions.')
        else:
            pass
    elif isinstance(error, commands.BadBoolArgument):
        await ctx.send(':x: Invalid true/false argument.', delete_after=8)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BadBoolArgument.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BadBoolArgument{colors.end}.')
        else:
            pass

#Commands
@slash.slash(
    name='load',
    description='Loads the specified module to the bot',
    options=[
        create_option(name='module', description='Which module do you want to load? (only in cogs folder)', option_type=3, required=True)
    ]
)
async def load(ctx:SlashContext, module:str):
    if ctx.author.id != 738290097170153472: return ctx.send("Sorry, but this command is only for my developer's use.", hidden=True)
    try:
        utils.logger.info(f"Attempting to load module \"{module}\".")
        client.load_extension(module)
        utils.logger.info("Success loading module!")
        await ctx.reply("Module loaded!")
    except Exception as e:
        utils.logger.error(f"Error while loading module: {e}")
        await ctx.reply("Module failed to load. Check console for info.")

@slash.slash(
    name='unload',
    description='Removes the specified module from the bot',
    options=[
        create_option(name='module', description='Which module do you want to unload? (only in cogs folder)', option_type=3, required=True)
    ]
)
async def unload(ctx:SlashContext, module:str):
    if ctx.author.id != 738290097170153472: return ctx.send("Sorry, but this command is only for my developer's use.", hidden=True)
    try:
        utils.logger.info(f"Attempting to unload module \"{module}\".")
        client.unload_extension(module)
        utils.logger.info("Success removing module!")
        await ctx.reply("Module unloaded!")
    except Exception as e:
        utils.logger.error(f"Error while unloading module: {e}")
        await ctx.reply("Module failed to unload. Check console for info.")

@slash.slash(name='balance', description='Shows your own or another user\'s balance.', options=[create_option(name='user', description='Which user?', option_type=6, required=False)])
async def balance(ctx:SlashContext, user=None):
    try:
        if user == None:
            e = discord.Embed(title=f'{ctx.author.display_name}\'s balance', color=color)
            e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(ctx.author.id)]} coin(s)', inline=True)
            e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(ctx.author.id)]} coin(s)', inline=True)
            await ctx.send(embed=e)
        else:
            try:
                e = discord.Embed(title=f'{user.display_name}\'s balance', color=color)
                e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(user.id)]} coin(s)', inline=True)
                e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(user.id)]} coin(s)', inline=True)
                await ctx.send(embed=e)
            except:
                await ctx.reply('Looks like that user is not indexed in our server. Try again later.')
                return
    except Exception as e:
        await ctx.send(f'An error occured: `{e}`. This has automatically been reported to the devs.')

@slash.slash(
    name='kick', 
    description='Kicks a member from this server.', 
    options=[
        create_option(name='user', description='Who do you want to kick?', option_type=6, required=True), 
        create_option(name='reason', description='Why you want to kick the user?', option_type=3, required=False)
    ]
)
@commands.cooldown(1, 3, commands.BucketType.user)
async def kick(ctx:SlashContext, user, reason=None):
    if plugins.moderation == False: pass
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply('https://tenor.com/view/oh-yeah-high-kick-take-down-fight-gif-14272509')
        return
    else:
        try:
            if reason == None: await user.kick()
            else: await user.kick(reason=reason)
            await ctx.send(embed=discord.Embed(title=f'{user} has been kicked.', description=f'Reason: {str(reason)}'))
        except:
            await ctx.send(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

@slash.slash(
    name='ban', 
    description='Bans a member from this server.', 
    options=[
        create_option(name='user', description='Who do you want to ban?', option_type=6, required=True), 
        create_option(name='reason', description='Why you want to ban the user?', option_type=3, required=False)
    ]
)
@commands.cooldown(1, 3, commands.BucketType.user)
async def ban(ctx:SlashContext, user, reason=None):
    if plugins.moderation == False: pass
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply('https://tenor.com/view/thor-strike-admin-ban-admin-ban-gif-22545175')
        return
    else:
        try:
            if reason == None: await user.ban()
            else: await user.ban(reason=reason)
            await ctx.send(embed=discord.Embed(title=f'{user} has been banned.', description=f'Reason: {str(reason)}'))
        except:
            await ctx.send(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

@slash.slash(
    name='warn',
    description='Warns someone in your server.',
    options=[
        create_option(name='user', description='Who do you want to warn?', option_type=6, required=True),
        create_option(name='reason', description='Why are you warning the user?', option_type=3, required=True)
    ]
)
@commands.cooldown(1, 2, commands.BucketType.user)
async def warn(ctx:SlashContext, user, reason):
    if plugins.moderation == False: pass
    if not ctx.author.guild_permissions.manage_messages:
        raise MissingPermissions
    warnings[str(ctx.guild.id)][str(user.id)].append('reason')
    save()
    target=client.get_user(user.id)
    try:
        await target.send(embed=discord.Embed(title=f':warning: You\'ve been warned in {ctx.guild} ({ctx.guild.id})', description=f'Reason {reason}'))
        await ctx.send(embed=discord.Embed(description=f'{user} has been warned.'))
    except:
        await ctx.send(embed=discord.Embed(description=f'{user} has been warned. I couldn\'t DM them, but their warning is logged.'))

@slash.slash(
    name='warns_clear',
    description='Clears someone\'s warnings.',
    options=[
        create_option(name='user', description='Who do you want to remove warns from?', option_type=6, required=True)
    ]
)
async def warns_clear(ctx:SlashContext, user):
    if plugins.moderation == False: pass
    if not ctx.author.guild_permissions.manage_messages:
        raise MissingPermissions
    warnings[str(ctx.guild.id)][str(user.id)] = []
    save()
    await ctx.send(embed=discord.Embed(description=f'All {user}\'s warnings have been cleared.'))

@slash.slash(
    name='deposit',
    description='Deposits a specified amount of cash into the bank.',
    options=[
        create_option(name='amount', description='Specify an amount to deposit (leave blank for max)', option_type=4, required=False)
    ]
)
async def deposit(ctx:SlashContext, amount=None):
    if plugins.economy == False: pass
    if amount == None:
        amount = currency["wallet"][str(ctx.author.id)]
    elif currency['bank'] == 0:
        await ctx.reply('You don\'t have anything in your bank account.', hidden=True)
        return
    elif amount <= 0:
        await ctx.reply('The amount to deposit must be more than `0` coins!', hidden=True)
        return
    elif amount > currency["wallet"][str(ctx.author.id)]:
        await ctx.reply('The amount to deposit must not be more than what you have in your wallet!', hidden=True)
        return
    else:
        pass
    currency["wallet"][str(ctx.author.id)] -= int(amount)
    currency["bank"][str(ctx.author.id)] += int(amount)
    await ctx.send(f'You deposited `{amount}` coin(s) to your bank account.')
    save()

@slash.slash(
    name='withdraw',
    description='Withdraws a specified amount of cash from the bank.',
    options=[
        create_option(name='amount', description='Specify an amount to withdraw (leave blank for max)', option_type=4, required=False)
    ]
)
async def withdraw(ctx:SlashContext, amount=None):
    if plugins.economy == False: pass
    if amount == None:
        amount = currency["bank"][str(ctx.author.id)]
    elif currency['bank'] == 0:
        await ctx.reply('You don\'t have anything in your bank account.', hidden=True)
        return
    elif amount <= 0:
        await ctx.reply('The amount to withdraw must be more than `0` coins!', hidden=True)
        return
    elif amount > currency["bank"][str(ctx.author.id)]:
        await ctx.reply('The amount to withdraw must not be more than what you have in your bank account!', hidden=True)
        return
    else:
        pass
    currency["wallet"][str(ctx.author.id)] += int(amount)
    currency["bank"][str(ctx.author.id)] -= int(amount)
    await ctx.send(f'You withdrew `{amount}` coin(s) from your bank account.')
    save()

@slash.slash(
    name='work',
    description='Work for a 30-minute shift and earn cash.'
)
@commands.cooldown(1, (30*60), commands.BucketType.user)
async def work(ctx:SlashContext):
    if plugins.economy == False: pass
    i = random.randint(10000, 20000)
    currency['wallet'][str(ctx.author.id)] += i
    save()
    await ctx.send(f'{ctx.author.mention} worked for a 30-minute shift and earned {i} coins.')

@slash.slash(
    name='daily',
    description='Claims your daily (every 24 hours)'
)
@commands.cooldown(1, 24*(60*60), commands.BucketType.user)
async def daily(ctx:SlashContext):
    if plugins.economy == False: pass
    currency['wallet'][str(ctx.author.id)] += 10000
    save()
    await ctx.reply(f'You claimed 10000 coins from the daily reward. Check back in 24 hours for your next one!')

@slash.slash(
    name='weekly',
    description='Claims your weekly (every 7 days)'
)
@commands.cooldown(1, 7*(24*(60*60)), commands.BucketType.user)
async def weekly(ctx:SlashContext):
    if plugins.economy == False: pass
    currency['wallet'][str(ctx.author.id)] += 45000
    save()
    await ctx.reply(f'You claimed 45000 coins from the weekly reward. Check back in 7 days for your next one!')

@slash.slash(
    name='monthly',
    description='Claims your monthly (every 31 days)'
)
@commands.cooldown(1, 31*(24*(60*60)), commands.BucketType.user)
async def monthly(ctx:SlashContext):
    if plugins.economy == False: pass
    currency['wallet'][str(ctx.author.id)] += 1000000
    save()
    await ctx.reply(f'You claimed 1000000 coins from the monthly reward. Check back in 1 month for your next one!')

@slash.slash(
    name='beg', 
    description='Begs for some quick cash'
)
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx:SlashContext):
    if plugins.economy == False: pass
    names = [
        "A random person",
        "Your friend",
        "Your boss",
        "The quiet kid",
        "Your mom",
        "The fart you have been holding for way too long",
        "Notch",
        "Jeff Bezos",
        "Elon Musk",
        "peppy",
        "Steve Jobs",
        "MrBeast",
        "Pewdiepie"
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
        "I think I know what you're gonna do with that money."
    ]
    sel1 = random.choice(names)
    sel2 = random.choice(fail_responses)
    chance:int = random.randint(1, 100)
    if (chance >= 50):
        x:int = random.randint(10, 100)
        currency["wallet"][str(ctx.author.id)] += x
        save()
        await ctx.send(embed=discord.Embed(title=str(sel1), description=f'"Oh you poor beggar, here\'s {x} coin(s) for you. Hope it helps!"'))
    else:
        await ctx.send(embed=discord.Embed(title=str(sel1), description=f'"{sel2}"'))

@slash.slash(
    name='scout', 
    description='Scouts your area for coins'
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def scout(ctx:SlashContext):
    if plugins.economy == False: pass
    chance:int = random.randint(1, 100)
    if (chance <= 90):
        x = random.randint(550, 2000)
        if items[str(ctx.author.id)]['binoculars'] >= 1:
            x *= 1.425
            x = math.floor(x)
        else:
            pass
        currency["wallet"][str(ctx.author.id)] += x
        save()
        await ctx.send(embed=discord.Embed(title='What you found', description=f'You searched your area and found {x} coin(s)!'))
    else:
        await ctx.send(embed=discord.Embed(title='What you found', description='Unfortunately no coins for you :('))

@slash.slash(
    name='give',
    description='Gives any amount of cash to someone else',
    options=[
        create_option(name='user', description='Who do you want to give cash to?', option_type=6, required=True),
        create_option(name='amount', description='How much do you want to give?', option_type=4, required=True)
    ]
)
async def give(ctx:SlashContext, user:discord.User, amount:int):
    if plugins.economy == False: pass
    if (amount <= 0):
        await ctx.send('The amount you want to give must be greater than `0` coins!', hidden=True)
        return
    if (amount > int(currency['wallet'][str(ctx.author.id)])):
        await ctx.send('You don\'t have enough coins in your wallet to do this.', hidden=True)
        return
    else:
        currency['wallet'][str(ctx.author.id)] -= amount
        currency['wallet'][str(user.id)] += amount
        save()
        await ctx.send(f':gift: {ctx.author.mention} just gifted {amount} coin(s) to {user.display_name}!')

@slash.slash(
    name='rob',
    description='Robs someone for their money',
    options=[
        create_option(name='user', description='Who do you want to rob?', option_type=6, required=True)
    ]
)
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx:SlashContext, user:discord.User):
    if plugins.economy == False: pass
    chance:int = random.randint(1, 100)
    if (currency['wallet'][str(user.id)] < 5000):
        await ctx.reply('They has less than 5000 coins on them. Don\'t waste your time...')
        return
    elif (currency['wallet'][str(ctx.author.id)] < 5000):
        await ctx.reply('You have less than 5k coins in your wallet. Play fair dude.')
        return
    if (chance <= 50):
        x:int = random.randint(5000, currency['wallet'][str(user.id)])
        currency['wallet'][str(ctx.author.id)] += x
        currency['wallet'][str(user.id)] -= x
        await ctx.reply(f'You just stole {x} coins from {user.display_name}! Feels good, doesn\'t it?')
    else:
        x:int = random.randint(5000, currency['wallet'][str(ctx.author.id)])
        currency['wallet'][str(ctx.author.id)] -= x
        currency['wallet'][str(user.id)] += x
        await ctx.reply(f'LOL YOU GOT CAUGHT! You paid {user.display_name} {x} coins as compensation for your action.')
    save()

@slash.slash(
    name='bankrob',
    description='Raids someone\'s bank account',
    options=[
        create_option(name='user', description='Whose bank account you want to raid?', option_type=6, required=True)
    ]
)
@commands.cooldown(1, (60*5), commands.BucketType.user)
async def bankrob(ctx:SlashContext, user:discord.User):
    if plugins.economy == False: pass
    chance:int = random.randint(1, 100)
    if (currency['wallet'][str(user.id)] < 10000):
        await ctx.reply('You really want to risk losing your life to a poor person? (imagine robbing someone with < 10k net worth)')
        return
    elif (currency['wallet'][str(ctx.author.id)] < 5000):
        await ctx.reply('You have less than 10k in your wallet. Don\'t be greedy.')
        return
    if (chance <= 20):
        x:int = random.randint(10000, currency['wallet'][str(user.id)])
        currency['wallet'][str(ctx.author.id)] += x
        currency['bank'][str(user.id)] -= x
        await ctx.reply(f'You raided {user.display_name}\'s bank and ended up looting {x} coins from them! Now thats what I like to call *success*.')
    else:
        x:int = 10000
        currency['wallet'][str(ctx.author.id)] -= x
        await ctx.reply(f'Have you ever thought of this as the outcome? You failed AND ended up getting caught by the police. You just lost {x} coins, you absolute loser.')

@slash.slash(
    name='inventory', 
    description='Shows the items you (or someone else) own',
    options = [
        create_option(name='user', description='Whose inventory you want to view?', option_type=6, required=False)
    ]
)
async def inventory(ctx:SlashContext, user:discord.User = None):
    if plugins.economy == False: pass
    localembed = None
    if user == None:
        localembed = discord.Embed(title='Your Inventory')
        localembed.add_field(name='Utility', value=f'Hunting Rifle `ID: rifle`: {items[str(ctx.author.id)]["rifle"]}\nFishing Rod `ID: fishingpole`: {items[str(ctx.author.id)]["fishingpole"]}\nShovel `ID: shovel`: {items[str(ctx.author.id)]["shovel"]}', inline=False)
        localembed.add_field(name='Sellables', value=f'Rock `ID: rock`: {items[str(ctx.author.id)]["rock"]}\nAnt `ID: ant`: {items[str(ctx.author.id)]["ant"]}\nStickbug `ID: stickbug`: {items[str(ctx.author.id)]["stickbug"]}\nSkunk `ID: skunk`: {items[str(ctx.author.id)]["skunk"]}\nBoar `ID: boar`: {items[str(ctx.author.id)]["boar"]}\nDeer `ID: deer`: {items[str(ctx.author.id)]["deer"]}\nDragon `ID: dragon`: {items[str(ctx.author.id)]["dragon"]}\nGold `ID: gold`: {items[str(ctx.author.id)]["gold"]}', inline=False)
        localembed.add_field(name='Power-ups', value=f'Binoculars `ID: binoculars`: {items[str(ctx.author.id)]["binoculars"]}', inline=False)
    else:
        localembed = discord.Embed(title=f'{user.display_name}\'s Inventory')
        localembed.add_field(name='Utility', value=f'Hunting Rifle `ID: rifle`: {items[str(user.id)]["rifle"]}\nFishing Rod `ID: fishingpole`: {items[str(user.id)]["fishingpole"]}\nShovel `ID: shovel`: {items[str(user.id)]["shovel"]}', inline=False)
        localembed.add_field(name='Sellables', value=f'Rock `ID: rock`: {items[str(user.id)]["rock"]}\nAnt `ID: ant`: {items[str(user.id)]["ant"]}\nStickbug `ID: stickbug`: {items[str(user.id)]["stickbug"]}\nSkunk `ID: skunk`: {items[str(user.id)]["skunk"]}\nBoar `ID: boar`: {items[str(user.id)]["boar"]}\nDeer `ID: deer`: {items[str(user.id)]["deer"]}\nDragon `ID: dragon`: {items[str(user.id)]["dragon"]}\nGold `ID: gold`: {items[str(user.id)]["gold"]}', inline=False)
        localembed.add_field(name='Power-ups', value=f'Binoculars `ID: binoculars`: {items[str(user.id)]["binoculars"]}', inline=False)
    await ctx.send(embed=localembed)

@slash.slash(
    name='shop',
    description='Views and buys items from the shop',
    options=[
        create_option(name='item', description='Specify an item to view.', option_type=3, required=False)
    ]
)
async def shop(ctx:SlashContext, item:str=None):
    if plugins.economy == False: pass
    if item == None:
        localembed = discord.Embed(
            title='The Shop!', 
            description='**Tools**\n\n1) Hunting Rifle `ID: rifle`: A tool used for hunting animals. (10000 coins)\n2) Fishing Pole `ID: fishingpole`: A tool used for fishing. It lets you use /fish command. (6500 coins)\n3) Shovel `ID: shovel`: You can use this tool to dig stuff from the ground. (3000 coins)\n4) Binoculars `ID: binoculars`: Try scouting with these binoculars, maybe you can find more with it. (14850 coins)'
        )
        localembed.set_footer(text='Page 1 | Tools | This command is in development. More items will be added soon!')
        await ctx.send(embed=localembed)
    else:
        #localembed = discord.Embed(title='Item lookup', description='isn\'t ready just yet. Please check back a bit later!')
        try:
            localembed = discord.Embed(
                title=shopitem[item]['stylized name'],
                description=shopitem[item]['description']
            )
            localembed.add_field(name='Buying price', value=shopitem[item]['buy price'], inline=True)
            localembed.add_field(name='Selling price', value=shopitem[item]['sell price'], inline=True)
            localembed.add_field(name='In-store', value=shopitem[item]['available'], inline=True)
            localembed.add_field(name='ID', value=f'`{item}`', inline=True)
            await ctx.send(embed=localembed)
        except KeyError:
            await ctx.reply('That item isn\'t in the shop, do you are have stupid?')

@slash.slash(
    name='buy',
    description='Buys an item from the shop',
    options=[
        create_option(name='name', description='What do you want to buy?', option_type=3, required=True),
        create_option(name='quantity', description='How many do you want to buy?', option_type=4, required=False)
    ]
)
async def buy(ctx:SlashContext, name:str, quantity:int=1):
    if plugins.economy == False: pass
    try:
        amt = shopitem[name]['buy price'] * quantity
        if (currency['wallet'][str(ctx.author.id)] < amt):
            await ctx.reply('You don\'t have enough balance to buy this.')
            return
        if (shopitem[name]['available'] == False):
            await ctx.reply('You can\'t buy this item **dood**')
            return
        if (quantity <= 0):
            await ctx.reply('The specified quantity cannot be less than `1`!')
            return
        currency['wallet'][str(ctx.author.id)] -= int(amt)
        items[str(ctx.author.id)][str(name)] += quantity
        save()
        await ctx.reply(embed=discord.Embed(title=f'You just bought {quantity} {shopitem[name]["stylized name"]}!', description='Thank you for your purchase.', color=discord.Color.green()))
    except KeyError:
        await ctx.reply('That item doesn\'t exist.')

@slash.slash(
    name='sell',
    description='Sells an item from your inventory in exchange for cash',
    options=[
        create_option(name='name', description='What do you want to sell?', option_type=3, required=True),
        create_option(name='quantity', description='How many do you want to sell?', option_type=4, required=False)
    ]
)
async def sell(ctx:SlashContext, name:str, quantity:int=1):
    try:
        if shopitem[name]["sellable"] != True:
            await ctx.reply('Dumb, you can\'t sell this item.')
            return
        else:
            pass
        if quantity > items[str(ctx.author.id)][str(name)]:
            await ctx.reply('You can\'t sell more than you have.')
            return
        items[str(ctx.author.id)][str(name)] -= quantity
        ttl = shopitem[name]["sell price"] * quantity
        currency["wallet"][str(ctx.author.id)] += int(ttl)
        save()
        localembed = discord.Embed(title='Item sold', description=f'You successfully sold {quantity} {name} for {ttl} coins!', color=discord.Color.random())
        localembed.set_footer(text='Thank you for your business.')
        await ctx.reply(embed=localembed)
    except KeyError:
        await ctx.reply('what are you doing that item doesn\'t even exist')
    except Exception as e:
        await ctx.send(f'An error occured while processing this request. ```{e}```')

@slash.slash(
    name='hunt',
    description='Pull out your rifle and hunt down animals'
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def hunt(ctx:SlashContext):
    if plugins.economy == False: pass
    if (items[str(ctx.author.id)]['rifle'] == 0):
        await ctx.reply('I\'d hate to see you hunt with your bare hands. Please buy a hunting rifle from the shop. ||/buy rifle||')
        return
    loot = [
        'rock',
        'ant',
        'skunk',
        'boar',
        'deer',
        'dragon',
        'nothing',
        'died'
    ]
    choice = random.choice(loot)
    if (choice == "rock"):
        items[str(ctx.author.id)]['rock'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "ant"):
        items[str(ctx.author.id)]['ant'] += 1
        save()
        await ctx.reply(f'You found an {choice} while hunting!')
    elif (choice == "skunk"):
        items[str(ctx.author.id)]['skunk'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "boar"):
        items[str(ctx.author.id)]['boar'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "deer"):
        items[str(ctx.author.id)]['deer'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "dragon"):
        items[str(ctx.author.id)]['dragon'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting! Good job!')
    elif (choice == "nothing"):
        await ctx.reply('You found absolutely **nothing** while hunting.')
    elif (choice == "died"):
        currency[str(ctx.author.id)]['wallet'] += 1000
        save()
        await ctx.reply('Stupid, you died while hunting and lost 1000 coins...')

@slash.slash(
    name='fish',
    description='Prepare your fishing rod and catch some fish'
)
@commands.cooldown(1, 45, commands.BucketType.user)
async def fish(ctx:SlashContext):
    if plugins.economy == False: pass
    if (items[str(ctx.author.id)]['fishingpole'] == 0):
        await ctx.reply('I don\'t think you can fish with your bare hands. Please buy a fishing pole from the shop. ||/buy fishingpole||')
        return
    loot = [
        'shrimp',
        'fish',
        'rare fish',
        'exotic fish',
        'jellyfish',
        'shark',
        'nothing'
    ]
    choice = random.choice(loot)
    if (choice == "shrimp"):
        items[str(ctx.author.id)]['shrimp'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "fish"):
        items[str(ctx.author.id)]['fish'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "rare fish"):
        items[str(ctx.author.id)]['rarefish'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "exotic fish"):
        items[str(ctx.author.id)]['exoticfish'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting!')
    elif (choice == "jellyfish"):
        items[str(ctx.author.id)]['jellyfish'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting! Good job!')
    elif (choice == "shark"):
        items[str(ctx.author.id)]['shark'] += 1
        save()
        await ctx.reply(f'You found a {choice} while hunting! Great job!')
    elif (choice == "nothing"):
        await ctx.reply('Looks like the fish were weary of your rod. You caught nothing.')

@slash.slash(
    name='dig',
    description='Take your shovel and dig in the ground for some cool stuff!'
)
@commands.cooldown(1, 45, commands.BucketType.user)
async def dig(ctx:SlashContext):
    if plugins.economy == False: pass
    if (items[str(ctx.author.id)]['shovel'] == 0):
        await ctx.reply('You\'re too good to have to dig with your bare hands..... at least I hope so. Please buy a shovel from the shop. ||/buy shovel||')
        return
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
        currency['wallet'][str(ctx.author.id)] += random.choice('1000', '5000')
        save()
        await ctx.reply(f'You went digging and found a bunch of coins. Nice!')
    elif (choice == "shovel"):
        items[str(ctx.author.id)]['shovel'] += 1
        save()
        await ctx.reply(f'Looks like you found someone\'s lost {choice} while digging lmao')
    elif (choice == "ant"):
        items[str(ctx.author.id)]['ant'] += 1
        save()
        await ctx.reply(f'You found an {choice} while digging!')
    elif (choice == "stickbug"):
        items[str(ctx.author.id)]['stickbug'] += 1
        save()
        await ctx.reply(f'You found a {choice} while digging!')
    elif (choice == "rock"):
        items[str(ctx.author.id)]['rock'] += 1
        save()
        await ctx.reply(f'You found a {choice} while digging... Ok totally not sus')
    elif (choice == "gold"):
        items[str(ctx.author.id)]['gold'] += 1
        save()
        await ctx.reply(f'You found some {choice} while digging! Good job!')
    elif (choice == "coinbomb"):
        items[str(ctx.author.id)]['coinbomb'] += 1
        save()
        await ctx.reply(f'Looks like you found a pretty interesting {choice} while digging! Niceee')
    elif (choice == "rare lootbox"):
        items[str(ctx.author.id)]['rare lootbox'] += 1
        save()
        await ctx.reply(f'You found a {choice} while digging! Cool, right?')
    elif (choice == "nothing"):
        await ctx.reply('After some time of digging you eventually gave up. You got nothing.')
    elif (choice == "died"):
        currency['wallet'][str(ctx.author.id)] -= 2000
        save()
        await ctx.reply('YOU FELL INTO YOUR OWN TRAP AND DIED LMFAO\nYou lost 2000 coins in the process.')

@slash.slash(
  name='echo',
  description='Sends a bot message in the channel',
  options=[
    create_option(name='text', description='What do you want to send?', option_type=3, required=True)
  ]
)
async def echo(ctx:SlashContext, text:str):
    try:
        await ctx.reply("Message echoed!", hidden=True)
        await ctx.channel.send(text)
    except Exception as e:
        await ctx.send(f"An error occured while processing this request. {e}", hidden=True)

@slash.slash(
    name='whoami',
    description='Shows information on a user',
    options=[
        create_option(name='user', description='Who do you want to know about?', option_type=6, required=False)
    ]
)
async def whoami(ctx:SlashContext, user:discord.User=None):
    if user == None:
        user = ctx.author
    else:
        pass
    username = user
    displayname = user.display_name
    registered = user.joined_at.strftime("%b %d, %Y, %T")
    pfp = user.avatar_url
    localembed = discord.Embed(
        title=f'User Info on {username}', 
        description=f'`AKA` {displayname}'
    )
    localembed.set_thumbnail(url=pfp)
    localembed.add_field(name='Username', value=username, inline=False)
    localembed.add_field(name='Display Name', value=displayname, inline=False)
    localembed.add_field(name='Joined Discord on', value=registered, inline=False)
    localembed.add_field(name='Avatar URL', value=f"[here!]({pfp})", inline=False)
    role_render = ""
    for p in user.roles:
        if p == "everyone":
            pass
        else:
            role_render += f"<@&{p.id}> "
    localembed.add_field(name='Roles', value=role_render, inline=False)
    await ctx.send(embed=localembed)

# DevTools commands
@slash.slash(
    name='sync',
    description='Syncs all of the local databases with their latest version'
)
async def sync(ctx:SlashContext):
    if ctx.author.id != 738290097170153472:
        await ctx.reply('Sorry, this command is only for my developer\'s use.')
        return
    else:
        pass
    try:
        with open(f'{wdir}/database/currency.json', 'r') as f:
            global currency
            currency = json.load(f)
        with open(f'{wdir}/database/warnings.json', 'r') as f:
            global warnings
            warnings = json.load(f)
        with open(f'{wdir}/database/items.json', 'r') as f:
            global items
            items = json.load(f)
        with open(f'{wdir}/config/shop.json', 'r') as f:
            global shopitem
            shopitem = json.load(f)
        await ctx.send('Databases resynced.', hidden=True)
    except Exception as e:
        print(e)
        await ctx.reply('An error occured while resyncing. Check console.', hidden=True)

@slash.slash(
    name='stroketranslate',
    description='Gives you the ability to make full words and sentences from a cluster of letters',
    options=[create_option(name='strok', description='What do you want to translate?', option_type=3, required=True)]
)
async def stroketranslate(ctx:SlashContext, strok: str):
        try:
            if len(strok) > 300: return await ctx.reply("Please use no more than `300` character length", hidden=True)
            else:
                with open(f"{os.getcwd()}/config/words.json", "r") as f: words = json.load(f)
                var = str()
                s = strok.lower()
                for i, c in enumerate(s): var += random.choice(words[c])
                return await ctx.send(f"{var}")
        except Exception as e: return await ctx.send(f"{type(e).__name__}: {e}")
        var = ''.join(arr)
        await ctx.reply(f"{var}")

@slash.slash(
    name='prediction',
    description='Randomly predicts a yes/no question.',
    options=[create_option(name="question", description="What do you want to predict?", option_type=3, required=True)]
)
async def prediction(ctx:SlashContext, question:str): ## "question" argument is useless lol argument go BRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR XDDDDD
    predict = random.randint(1, 2)
    if predict == 1:
        await ctx.reply("My prediction is... **Yes!**")
    elif predict == 2:
        await ctx.reply("My prediction is... **No!**")

@slash.slash(
    name='memes',
    description='Finely hand-picks a high-quality meme from the depths of reddit.'
)
async def memes(ctx:SlashContext):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

@slash.slash(
    name='linuxmemes',
    description='Hands you a fabolous GNU/Linux meme from the r/linuxmemes subreddit.'
)
async def linuxmemes(ctx:SlashContext):
    memes_submissions = reddit.subreddit('linuxmemes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

@slash.slash(
    name='ihadastroke',
    description='I bet you\'ll have a stroke trying to see these. (JK ITS ABSOLUTELY SAFE FOR YOU DONT WORRY)'
)
async def ihadastroke(ctx:SlashContext):
    memes_submissions = reddit.subreddit('ihadastroke').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

@slash.slash(
    name='engrish',
    description='Features phuck ups in english of any kind!'
)
async def engrish(ctx:SlashContext):
    memes_submissions = reddit.subreddit('engrish').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

@slash.slash(
    name='nothecker',
    description='Features a post from the official r/nothecker subreddit!'
)
async def nothecker(ctx:SlashContext):
    memes_submissions = reddit.subreddit('nothecker').hot()
    post_to_pick = random.randint(1, 10)  #Value eased/reduced to 10 as there arent many posts there! 
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

@slash.slash(
    name='osugame',
    description='Features a post from the official osu! subreddit!'
)
async def osugame(ctx:SlashContext):
    memes_submissions = reddit.subreddit('osugame').hot()
    post_to_pick = random.randint(1, 100)  #Value eased/reduced to 10 as there arent many posts there! 
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    embed = discord.Embed(title=submission.title, color=color)
    embed.set_image(url=submission.url)
    embed.set_footer(text='Powered by PRAW')
    await ctx.send(embed = embed)

# Initialization
utils.ping.host()
client.run(api.auth.token)




# btw i use arch
