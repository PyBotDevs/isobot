#Imports
import discord
from discord.ext import commands
from discord.ext.commands import *
from discord.ext import tasks
import os
import os.path
import json
import time
import asyncio
import random
import datetime
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import api.auth
import utils.logger

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
client = commands.Bot(command_prefix='s!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
color = discord.Color.random()
with open('./Desktop/Stock/database/currency.json', 'r') as f:
    global currency
    currency = json.load(f)
with open('./Desktop/Stock/database/warnings.json', 'r') as f:
    global warnings
    warnings = json.load(f)

#Pre-Initialization Commands
def timenow(): 
    datetime.datetime.now().strftime("%H:%M:%S")
def save():
    with open('./Desktop/Stock/database/currency.json', 'w+') as f:
        json.dump(currency, f, indent=4)
    with open(f'./Desktop/Stock/database/warnings.json', 'w+') as f:
        json.dump(warnings, f, indent=4)

#Classes
class colors:
    cyan = '\033[96m'
    red = '\033[91m'
    green = '\033[92m'
    end = '\033[0m'

#Events
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + '.')
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
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f':stopwatch: Not now! Please try after **{str(datetime.timedelta(seconds=int(round(error.retry_after))))}**')
        if os.name == 'nt':
            print(f'[{current_time}] Ignoring exception at {colors.cyan}CommandOnCooldown{colors.end}. Details: This command is currently on cooldown.')
        else:
            pass
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(':warning: Missing required argument(s)', delete_after=8)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at MissingRequiredArgument. Details: The command can\'t be executed because required arguments are missing.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}MissingRequiredArgument{colors.end}. Details: The command can\'t be executed because required arguments are missing.')
        else:
            pass
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have permission to do this!', hidden=True)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at MissingPermissions. Details: The user doesn\'t have the required permissions.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}MissingPermissions{colors.end}. Details: The user doesn\'t have the required permissions.')
        else:
            pass
    if isinstance(error, BadArgument):
        await ctx.send(':x: Invalid argument.', delete_after=8)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BadArgument.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BadArgument{colors.end}.')
        else:
            pass
    if isinstance(error, BotMissingPermissions):
        await ctx.send(':x: I don\'t have the required permissions to use this.')
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BotMissingPermissions.\n Details: The bot doesn\'t have the required permissions.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BotMissingPremissions{colors.end}. Details: The bot doesn\'t have the required permissions.')
        else:
            pass
    if isinstance(error, BadBoolArgument):
        await ctx.send(':x: Invalid true/false argument.', delete_after=8)
        if os.name == 'nt':
            with open(errorHandler_path, 'a') as f:
                f.write(f'[{current_time}] Ignoring exception at BadBoolArgument.\n')
                f.close()
            print(f'[{current_time}] Ignoring exception at {colors.cyan}BadBoolArgument{colors.end}.')
        else:
            pass

#Commands
@slash.slash(name='balance', description='Shows your balance, or another user\'s balance.', options=[create_option(name='user', description='The user\'s balance you want to see.', option_type=6, required=False)])
async def balance(ctx:SlashContext, user=None):
    try:
        if user == None:
            e = discord.Embed(title=f'{ctx.author.display_name}\'s balance', color=color)
            e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(ctx.author.id)]} coins', inline=True)
            e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(ctx.author.id)]} coins', inline=True)
            await ctx.send(embed=e)
        else:
            try:
                e = discord.Embed(title=f'{user.display_name}\'s balance', color=color)
                e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(user.id)]} coins', inline=True)
                e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(user.id)]} coins', inline=True)
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
        create_option(name='user', description='The user you will kick', option_type=6, required=True), 
        create_option(name='reason', description='Why you want to kick the user', option_type=3, required=False)
    ]
)
async def kick(ctx:SlashContext, user, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        raise(MissingPermissions)
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
        create_option(name='user', description='The user you will ban', option_type=6, required=True), 
        create_option(name='reason', description='Why you want to ban the user', option_type=3, required=False)
    ]
)
async def ban(ctx:SlashContext, user, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        raise(MissingPermissions)
    else:
        try:
            if reason == None: await user.ban()
            else: await user.ban(reason=reason)
            await ctx.send(embed=discord.Embed(title=f'{user} has been banned.', description=f'Reason: {str(reason)}'))
        except:
            await ctx.send(embed=discord.Embed(title='Well, something happened...', description='Either I don\'t have permission to do this, or my role isn\'t high enough.', color=discord.Colour.red()))

@slash.slash(
    name='warn',
    description='Warn someone in your server.',
    options=[
        create_option(name='user', description='The person you want to warn', option_type=6, required=True),
        create_option(name='reason', description='Why you are warning the user', option_type=3, required=True)
    ]
)
async def warn(ctx:SlashContext, user, reason):
    if not ctx.author.guild_permissions.manage_messages:
        raise(MissingPermissions)
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
    description='Clear someone\'s warnings.',
    options=[
        create_option(name='user', description='The person you want to remove warns from', option_type=6, required=True)
    ]
)
async def warn(ctx:SlashContext, user):
    if not ctx.author.guild_permissions.manage_messages:
        raise(MissingPermissions)
    warnings[str(ctx.guild.id)][str(user.id)] = []
    save()
    await ctx.send(embed=discord.Embed(description=f'All warnings have been cleared for {user}.'))

@slash.slash(
    name='deposit',
    description='Deposits a specified amount of cash into the bank.',
    options=[
        create_option(name='amount', description='Specify an amount to deposit (leave blank for max)', option_type=4, required=False)
    ]
)
async def deposit(ctx:SlashContext, amount=None):
    if amount == None:
        amount = currency["wallet"][str(user.id)]
    elif amount <= 0:
        await ctx.reply('The amount you want to deposit must be more than `0` coins!', hidden=True)
        return
    elif amount > currency["wallet"][str(user.id)]:
        await ctx.reply('The amount you want to deposit must not be more than what you have in your wallet!', hidden=True)
        return
    else:
        pass
    currency["wallet"][str(user.id)] -= int(amount)
    currency["bank"][str(user.id)] += int(amount)
    await ctx.send(f'You deposited `{amount}` coins to your bank account.')

@slash.slash(
    name='withdraw',
    description='Withdraws a specified amount of cash from the bank.',
    options=[
        create_option(name='amount', description='Specify an amount to withdraw (leave blank for max)', option_type=4, required=False)
    ]
)
async def withdraw(ctx:SlashContext, amount=None):
    if amount == None:
        amount = currency["bank"][str(user.id)]
    elif amount <= 0:
        await ctx.reply('The amount you want to withdraw must be more than `0` coins!', hidden=True)
        return
    elif amount > currency["bank"][str(user.id)]:
        await ctx.reply('The amount you want to withdraw must not be more than what you have in your bank account!', hidden=True)
        return
    else:
        pass
    currency["wallet"][str(user.id)] += int(amount)
    currency["bank"][str(user.id)] -= int(amount)
    await ctx.send(f'You withdrew `{amount}` coins from your bank account.')

@slash.slash(
    name='work',
    description='Work for a 30-minute shift and earn cash.'
)
@commands.cooldown(1, (30*60), commands.BucketType.user)
async def work(ctx:SlashContext):
    i = random.randint(10000, 20000)
    currency['wallet'][str(ctx.author.id)] += i
    save()
    await ctx.send(f'{ctx.author.mention} worked for a 30-minute shift and earned {i} coins.')

@slash.slash(
    name='daily',
    description='Claim your daily (every 24 hours)'
)
@commands.cooldown(1, 24*(60*60), commands.BucketType.user)
async def daily(ctx:SlashContext):
    currency['wallet'][str(ctx.author.id)] += 10000
    save()
    await ctx.reply(f'You claimed 10000 coins from this daily. Check back in 24 hours for your next one!')

@slash.slash(
    name='weekly',
    description='Claim your weekly (every 7 days)'
)
@commands.cooldown(1, 7*(24*(60*60)), commands.BucketType.user)
async def weekly(ctx:SlashContext):
    currency['wallet'][str(ctx.author.id)] += 45000
    save()
    await ctx.reply(f'You claimed 45000 coins from this weekly. Check back in 7 days for your next one!')

@slash.slash(
    name='monthly',
    description='Claim your monthly (every 31 days)'
)
@commands.cooldown(1, 31*(24*(60*60)), commands.BucketType.user)
async def monthly(ctx:SlashContext):
    currency['wallet'][str(ctx.author.id)] += 1000000
    save()
    await ctx.reply(f'You claimed 1000000 coins from this weekly. Check back in 1 month for your next one!')

@slash.slash(
    name='beg', 
    description='Beg for some quick cash'
)
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx:SlashContext):
    chance:int = random.randint(1, 100)
    if (chance >= 50):
        x:int = random.randint(10, 100)
        currency[wallet][str(ctx.author.id)] += x
        save()
        await ctx.send(embed=discord.Embed(title='A random person', description=f'"Oh you poor beggar, here\'s {x} for you"'))
    else:
        await ctx.send(embed=discord.Embed(title='A random person', description='"lol no get a life"'))

# Initialization
client.run(api.auth.token)
