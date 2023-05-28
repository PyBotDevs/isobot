"""The isobot cog file for the economy system."""

# Imports
import discord
import os.path
import json
import random
import math
import utils.logger
import asyncio
from random import randint
from discord import option, ApplicationContext
from discord.ext import commands
from cogs.levelling import get_level

# Classes
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

# Variables
wdir = os.getcwd()
color = discord.Color.random()
shop_data = ShopData(f"{wdir}/config/shop.json")
all_item_ids = shop_data.get_item_ids()
jobs = [
    "Discord mod",
    "YouTuber",
    "Streamer",
    "Developer",
    "Scientist",
    "Engineer",
    "Doctor"
]

with open(f"{wdir}/database/currency.json", 'r') as f: currency = json.load(f)
with open(f"{wdir}/database/items.json", 'r') as f: items = json.load(f)
with open(f"{wdir}/config/shop.json", 'r') as f: shopitem = json.load(f)
with open(f"{wdir}/database/user_data.json", 'r') as f: userdat = json.load(f)

def save():
    with open(f"{wdir}/database/currency.json", 'w+') as f: json.dump(currency, f, indent=4)
    with open(f"{wdir}/database/items.json", 'w+') as f: json.dump(items, f, indent=4)
    with open(f"{wdir}/database/user_data.json", 'w+') as f: json.dump(userdat, f, indent=4)

# Functions
def get_user_networth(user_id:int):
    nw = currency["wallet"][str(user_id)] + currency["bank"][str(user_id)]
    #for e in items[str(user_id)]:
    #    if e != 0: nw += shopitem[e]["sell price"]
    return nw

def get_wallet(id: int) -> int:
    return currency['wallet'][str(id)]

def get_bank(id: int) -> int:
    return currency['bank'][str(id)]

def new_wallet(id: int):
    if str(id) not in currency['wallet']: 
        currency['wallet'][str(id)] = 5000
        return 0
    else: return 1
    
def new_bank(id: int):
    if str(id) not in currency['bank']: 
        currency['bank'][str(id)] = 0
        return 0
    else: return 1

def get_user_count():
    users = 0
    for x in currency["wallet"].keys():
        users += 1
    return users

def new_userdat(id: int):
    if str(id) not in userdat.keys(): 
        userdat[str(id)] = {"work_job": None}
        save()
        return 0
    else: return 1

# Commands
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name='openlootbox',
        description='Opens lootbox(es) in your inventory'
    )
    @option(name="lootbox", description="What lootbox do you want to open?", type=str, choices=["normal lootbox", "large lootbox", "special lootbox"])
    @option(name="amount", description="How many do you want to open?", type=int)
    async def openlootbox(self, ctx: ApplicationContext, lootbox:str, amount:int):
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
    
    @commands.slash_command(
        name='beg', 
        description='Begs for some quick cash'
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def beg(self, ctx: ApplicationContext):
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
            await ctx.respond(embed=discord.Embed(title=random.choice(names), description=f"Oh you poor beggar, here's {x} coin(s) for you. Hope it helps!"))
        else: await ctx.respond(embed=discord.Embed(title=random.choice(names), description=f'"{random.choice(fail_responses)}"'))

    @commands.slash_command(
        name='daily',
        description='Claims your daily (every 24 hours)'
    )
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def daily(self, ctx: ApplicationContext):
        currency['wallet'][str(ctx.author.id)] += 10000
        save()
        await ctx.respond(f'You claimed 10000 coins from the daily reward. Check back in 24 hours for your next one!')

    @commands.slash_command(
        name='weekly',
        description='Claims your weekly (every 7 days)'
    )
    @commands.cooldown(1, 302400, commands.BucketType.user)
    async def weekly(self, ctx: ApplicationContext):
        currency['wallet'][str(ctx.author.id)] += 45000
        save()
        await ctx.respond(f'You claimed 45000 coins from the weekly reward. Check back in 7 days for your next one!')

    @commands.slash_command(
        name='monthly',
        description='Claims your monthly (every 31 days)'
    )
    @commands.cooldown(1, 1339200, commands.BucketType.user)
    async def monthly(self, ctx: ApplicationContext):
        currency['wallet'][str(ctx.author.id)] += 1000000
        save()
        await ctx.respond(f'You claimed 1000000 coins from the monthly reward. Check back in 1 month for your next one!')
    
    @commands.slash_command(
        name='rob',
        description='Robs someone for their money'
    )
    @option(name="user", description="Who do you want to rob?", type=discord.User)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx: ApplicationContext, user:discord.User):
        if currency['wallet'][str(user.id)] < 5000: return await ctx.respond('They has less than 5000 coins on them. Don\'t waste your time...') 
        elif currency['wallet'][str(ctx.author.id)] < 5000: return await ctx.respond('You have less than 5k coins in your wallet. Play fair dude.')
        if randint(1, 100) <= 50:
            x = randint(5000, currency['wallet'][str(user.id)])
            currency['wallet'][str(ctx.author.id)] += x
            currency['wallet'][str(user.id)] -= x
            await ctx.respond(f"You just stole {x} coins from {user.display_name}! Feels good, doesn't it?")
        else:
            x = randint(5000, currency['wallet'][str(ctx.author.id)])
            currency['wallet'][str(ctx.author.id)] -= x
            currency['wallet'][str(user.id)] += x
            await ctx.respond(f"LOL YOU GOT CAUGHT! You paid {user.display_name} {x} coins as compensation for your action.")
        save()

    @commands.slash_command(
        name='bankrob',
        description="Raids someone's bank account"
    )
    @option(name="user", description="Whose bank account do you want to raid?", type=discord.User)
    @commands.cooldown(1, (60*5), commands.BucketType.user)
    async def bankrob(self, ctx: ApplicationContext, user:discord.User):
        if currency['wallet'][str(user.id)] < 10000: return await ctx.respond('You really want to risk losing your life to a poor person? (imagine robbing someone with < 10k net worth)')
        elif currency['wallet'][str(ctx.author.id)] < 10000: return await ctx.respond('You have less than 10k in your wallet. Don\'t be greedy.')
        if randint(1, 100) <= 20:
            x = randint(10000, currency['wallet'][str(user.id)])
            currency['wallet'][str(ctx.author.id)] += x
            currency['bank'][str(user.id)] -= x
            await ctx.respond(f"You raided {user.display_name}'s bank and ended up looting {x} coins from them! Now thats what I like to call *success*.")
        else:
            x = 10000
            currency['wallet'][str(ctx.author.id)] -= x
            await ctx.respond(f"Have you ever thought of this as the outcome? You failed AND ended up getting caught by the police. You just lost {x} coins, you absolute loser.")

    @commands.slash_command(
        name='hunt',
        description='Pull out your rifle and hunt down animals'
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hunt(self, ctx: ApplicationContext):
        if items[str(ctx.author.id)]['rifle'] == 0: return await ctx.respond("I'd hate to see you hunt with your bare hands. Please buy a hunting rifle from the shop. ||/buy rifle||")
        loot = ['rock', 'ant', 'skunk', 'boar', 'deer', 'dragon', 'nothing', 'died']
        choice = random.choice(loot)
        if choice != "nothing" and choice != "died":
            items[str(ctx.author.id)][choice] += 1
            await ctx.respond(f"You found a {choice} while hunting!")
            save()
        elif (choice == "nothing"): await ctx.respond('You found absolutely **nothing** while hunting.')
        elif (choice == "died"):
            currency['wallet'][str(ctx.author.id)] -= 1000
            save()
            await ctx.respond("Stupid, you died while hunting and lost 1000 coins...")

    @commands.slash_command(
        name='fish',
        description='Prepare your fishing rod and catch some fish'
    )
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def fish(self, ctx: ApplicationContext):
        if (items[str(ctx.author.id)]['fishingpole'] == 0): return await ctx.respond("I don't think you can fish with your bare hands... or you can just put yo hands in the water bro **giga chad moment**\nAnyway it's just better to buy a fishing pole from the shop. ||/buy fishingpole||")
        loot = ['shrimp', 'fish', 'rare fish', 'exotic fish', 'jellyfish', 'shark', 'nothing']
        choice = random.choice(loot)
        if choice != "nothing":
            items[str(ctx.author.id)][choice] += 1
            save()
            await ctx.respond(f'You found a {choice} while hunting!')
        else: await ctx.respond('Looks like the fish were weary of your rod. You caught nothing.')

    @commands.slash_command(
        name='dig',
        description='Take your shovel and dig in the ground for some cool stuff!'
    )
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def dig(self, ctx: ApplicationContext):
        if (items[str(ctx.author.id)]['shovel'] == 0): return await ctx.respond("You're too good to have to dig with your bare hands..... at least I hope so. Please buy a shovel from the shop. ||/buy shovel||")
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
    
    @commands.slash_command(
        name='shop',
        description='Views and buys items from the shop'
    )
    @option(name="item", description="Specify an item to view.", type=str, default=None, choices=all_item_ids)
    async def shop(self, ctx: ApplicationContext, item:str=None):
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

    @commands.slash_command(
        name='buy',
        description='Buys an item from the shop'
    )
    @option(name="name", description="What do you want to buy?", type=str, choices=all_item_ids)
    @option(name="quantity", description="How many do you want to buy?", type=int, default=1)
    async def buy(self, ctx: ApplicationContext, name: str, quantity: int=1):
        try:
            amt = shopitem[name]['buy price'] * quantity
            if (currency['wallet'][str(ctx.author.id)] < amt): return await ctx.respond('You don\'t have enough balance to buy this.')
            if (shopitem[name]['available'] == False): return await ctx.respond('You can\'t buy this item **dood**')
            if (quantity <= 0): return await ctx.respond('The specified quantity cannot be less than `1`!')
            tax = 3
            taxable_amount = (amt / 100) * tax
            rounded_taxable_amount = math.floor(taxable_amount)
            total_amount = amt + rounded_taxable_amount
            currency['wallet'][str(ctx.author.id)] -= int(total_amount)
            items[str(ctx.author.id)][str(name)] += quantity
            currency["treasury"] += rounded_taxable_amount
            save()
            localembed = discord.Embed(
                title=f'You just bought {quantity} {shopitem[name]["stylized name"]}!',
                description=f"**Your Purchase Invoice**\n\nItem: {quantity} {name.lower()}\n---------------\nBase Amount: {amt} coins\nTax: 3%\nTaxable Amount: {taxable_amount} coins\nTaxable Amount (rounded): {rounded_taxable_amount} coins\n**Charged Amount:** {total_amount} coins",
                color=discord.Color.green()
            )
            localembed.set_footer(text="Thank you for your purchase.")
            await ctx.respond(embed=localembed)
        except KeyError: await ctx.respond('That item doesn\'t exist.')

    @commands.slash_command(
        name='sell',
        description='Sells an item from your inventory in exchange for cash'
    )
    @option(name="name", description="What do you want to sell?", type=str, choices=all_item_ids)
    @option(name="quantity", description="How many do you want to sell?", type=int, default=1)
    async def sell(self, ctx: ApplicationContext, name: str, quantity: int=1):
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
    
    @commands.slash_command(
        name="gift",
        description="Gifts a (giftable) item to anyone you want"
    )
    @option(name="user", description="Who do you want to gift to?", type=discord.User)
    @option(name="item", description="What do you want to gift?", type=str, choices=all_item_ids)
    @option(name="amount", description="How many of these do you want to gift?", type=int, default=1)
    async def gift(self, ctx: ApplicationContext, user:discord.User, item:str, amount:int=1):
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
    
    @commands.slash_command(
        name='modify_balance',
        description="Modifies user balance (Normal Digit: Adds Balance; Negative Digit: Removes Balance)"
    )
    @option(name="user", description="Specify the user to change their balance", type=discord.User)
    @option(name="modifier", description="Specify the balance to modify", type=int)
    async def modify_balance(self, ctx: ApplicationContext, user:discord.User, modifier:int):
        if ctx.author.id != 738290097170153472: return ctx.respond("Sorry, but this command is only for my developer's use.", ephemeral=True)
        try:
            currency["wallet"][str(user.id)] += modifier
            save()
            await ctx.respond(f"{user.name}\'s balance has been modified by {modifier} coins.\n\n**New Balance:** {currency['wallet'][str(user.id)]} coins", ephemeral=True)
        except KeyError: await ctx.respond("That user doesn't exist in the database.", ephemeral=True)

    @commands.slash_command(
        name='give',
        description='Gives any amount of cash to someone else'
    )
    @option(name="user", description="Who do you want to give cash to?", type=discord.User)
    @option(name="amount", description="How much do you want to give?", type=int)
    async def give(self, ctx: ApplicationContext, user:discord.User, amount:int):
        if amount <= 0: return await ctx.respond('The amount you want to give must be greater than `0` coins!', ephemeral=True)
        if amount > int(currency['wallet'][str(ctx.author.id)]): return await ctx.respond('You don\'t have enough coins in your wallet to do this.', ephemeral=True)
        else:
            currency['wallet'][str(ctx.author.id)] -= amount
            currency['wallet'][str(user.id)] += amount
            save()
            await ctx.respond(f':gift: {ctx.author.mention} just gifted {amount} coin(s) to {user.display_name}!')
    
    @commands.slash_command(
        name='work',
        description='Work for a 30-minute shift and earn cash.'
    )
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def work(self, ctx: ApplicationContext):
        if userdat[str(ctx.author.id)]["work_job"] == None: return await ctx.respond("You don't currently have a job! Join one by using the `/work_select` command.", ephemeral=True)
        if userdat[str(ctx.author.id)]["work_job"] == "Discord mod": i = randint(5000, 10000)
        elif userdat[str(ctx.author.id)]["work_job"] == "YouTuber": i = randint(10000, 15000)
        elif userdat[str(ctx.author.id)]["work_job"] == "Streamer": i = randint(12000, 18000)
        elif userdat[str(ctx.author.id)]["work_job"] == "Developer": i = randint(20000, 40000)
        elif userdat[str(ctx.author.id)]["work_job"] == "Scientist": i = randint(50000, 100000)
        elif userdat[str(ctx.author.id)]["work_job"] == "Engineer": i = randint(100000, 175000)
        elif userdat[str(ctx.author.id)]["work_job"] == "Doctor": i = randint(200000, 300000)
        currency['wallet'][str(ctx.author.id)] += i
        save()
        await ctx.respond(f'{ctx.author.mention} worked for a 30-minute shift as a {userdat[str(ctx.author.id)]["work_job"]} and earned {i} coins.')

    @commands.slash_command(
        name="work_list",
        description="Shows a list of all the jobs currently available."
    )
    async def work_list(self, ctx: ApplicationContext):
        localembed = discord.Embed(
            title="List of jobs",
            # description="To join a job, make sure you meet the required level first.\n\n**Discord mod**: Moderate community servers\n  Salary: `5000 - 10000 coins` per shift\n  Level experience: None\n\n**YouTuber**: Make YouTube videos and get monetized\n  Salary: `10000-15000 coins` per shift\n  Level experience: Level 3\n\n**Streamer**: Stream on Twitch recieve viewer donations\n  Salary: `12000-18000 coins` per shift\n  Level experience: Level 5\n\n**Developer**: Write code and make money\n  Salary: `20000-40000 coins` per shift\n  Level experience: Level 10\n\n**Scientist**: Work as a scientist at a undisclosed lab\n  Salary: `50000-100000 coins` per shift\n  Level experience: Level 20\n\n**Engineer**: Do engineering stuff\n  Salary: `100000-175000 coins` per shift\n  Level experience: Level 25\n\n**Doctor**: Work as a surgeon\n  Salary: `200000-300000 coins` per shift\n  Level experience: Level 40"
            description="To join a job, make sure you meet the required level first.\n\n**Discord mod**\n  Salary: `5000 - 10000 coins` per shift\n  Level experience: None\n\n**YouTuber**\n  Salary: `10000-15000 coins` per shift\n  Level experience: Level 3\n\n**Streamer**\n  Salary: `12000-18000 coins` per shift\n  Level experience: Level 5\n\n**Developer**\n  Salary: `20000-40000 coins` per shift\n  Level experience: Level 10\n\n**Scientist**\n  Salary: `50000-100000 coins` per shift\n  Level experience: Level 20\n\n**Engineer**\n  Salary: `100000-175000 coins` per shift\n  Level experience: Level 25\n\n**Doctor**\n  Salary: `200000-300000 coins` per shift\n  Level experience: Level 40"
        )
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="work_select",
        description="Choose the job you want to work."
    )
    @option(name="job", description="What job do you want to work?", choices=jobs, type=str)
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def work_select(self, ctx: ApplicationContext, job: str):
        if job not in jobs: return await ctx.respond(f"This job does not exist. What kind of a job is even {job}??", ephemeral=True)
        if job == "YouTuber" and get_level(ctx.author.id) < 3: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        elif job == "Streamer" and get_level(ctx.author.id) < 5: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        elif job == "Developer" and get_level(ctx.author.id) < 10: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        elif job == "Scientist" and get_level(ctx.author.id) < 20: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        elif job == "Engineer" and get_level(ctx.author.id) < 25: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        elif job == "Doctor" and get_level(ctx.author.id) < 40: return await ctx.respond("You currently do not have the required level to perform this job!", ephemeral=True)
        userdat[str(ctx.author.id)]["work_job"] = job
        save()
        localembed = discord.Embed(title="New job!", description=f"You are now working as a {job}!")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="work_resign",
        description="Quit your job."
    )
    async def work_resign(self, ctx: ApplicationContext):
        if userdat[str(ctx.author.id)]["work_job"] is None: return await ctx.respond("You can't quit your job if you don't already have one!", ephemeral=True)
        userdat[str(ctx.author.id)]["work_job"] = None
        save()
        localembed = discord.Embed(title="Resignation", description="You have successfully resigned from your job.")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name='donate',
        description="Donate money to whoever you want"
    )
    @option(name="id", description="The ID of the user you are donating to", type=str)
    @option(name="amount", description="How much do you want to donate?", type=int)
    async def donate(self, ctx: ApplicationContext, id:str, amount):
        reciever_info = self.bot.get_user(int(id))
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
    
    @commands.slash_command(
        name='scout', 
        description='Scouts your area for coins'
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def scout(self, ctx: ApplicationContext):
        if (randint(1, 100) <= 90):
            x = randint(550, 2000)
            if items[str(ctx.author.id)]['binoculars'] >= 1:
                x *= 1.425
                x = math.floor(x)
            else: pass
            currency["wallet"][str(ctx.author.id)] += x
            save()
            await ctx.respond(embed=discord.Embed(title='What you found', description=f'You searched your area and found {x} coin(s)!'))
        else: await ctx.respond(embed=discord.Embed(title='What you found', description='Unfortunately no coins for you :('))

    @commands.slash_command(
        name="autogrind",
        description="Automatically grinds coins and items for you"
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def autogrind(self, ctx: ApplicationContext):
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

    @commands.slash_command(
        name='deposit',
        description='Deposits a specified amount of cash into the bank.'
    )
    @option(name="amount", description="Specify an amount to deposit (use 'max' for everything)", type=str)
    async def deposit(self, ctx: ApplicationContext, amount):
        if not amount.isdigit():
            if str(amount) == "max": amount = currency["wallet"][str(ctx.author.id)]
            else: return await ctx.respond("The amount must be a number, or `max`.", ephemeral=True)
        elif currency['bank'] == 0: return await ctx.respond('You don\'t have anything in your bank account.', ephemeral=True)
        elif int(amount) <= 0: return await ctx.respond('The amount to deposit must be more than `0` coins!', ephemeral=True)
        elif int(amount) > currency["wallet"][str(ctx.author.id)]: return await ctx.respond('The amount to deposit must not be more than what you have in your wallet!', ephemeral=True)
        currency["wallet"][str(ctx.author.id)] -= int(amount)
        currency["bank"][str(ctx.author.id)] += int(amount)
        localembed = discord.Embed(title="Deposit successful", description=f"You deposited `{amount}` coin(s) to your bank account.", color=color)
        localembed.add_field(name="You previously had", value=f"`{currency['bank'][str(ctx.author.id)] - amount} coins` in your bank account")
        localembed.add_field(name="Now you have", value=f"`{currency['bank'][str(ctx.author.id)]} coins` in your bank account")
        await ctx.respond(embed=localembed)
        save()

    @commands.slash_command(
        name='withdraw',
        description='Withdraws a specified amount of cash from the bank.'
    )
    @option(name="amount", description="Specify an amount to withdraw (use 'max' for everything)", type=str)
    async def withdraw(self, ctx: ApplicationContext, amount):
        if not amount.isdigit():
            if str(amount) == "max": amount = currency["bank"][str(ctx.author.id)]
            else: return await ctx.respond("The amount must be a number, or `max`.", ephemeral=True)
        elif currency['bank'][str(ctx.author.id)] == 0: return await ctx.respond('You don\'t have anything in your bank account.', ephemeral=True)
        elif int(amount) <= 0: return await ctx.respond('The amount to withdraw must be more than `0` coins!', ephemeral=True)
        elif int(amount) > currency["bank"][str(ctx.author.id)]: return await ctx.respond('The amount to withdraw must not be more than what you have in your bank account!', ephemeral=True)
        currency["wallet"][str(ctx.author.id)] += int(amount)
        currency["bank"][str(ctx.author.id)] -= int(amount)
        localembed = discord.Embed(title="Withdraw successful", description=f"You withdrew `{amount}` coin(s) from your bank account.", color=color)
        localembed.add_field(name="You previously had", value=f"`{currency['wallet'][str(ctx.author.id)] - amount} coins` in your wallet")
        localembed.add_field(name="Now you have", value=f"`{currency['wallet'][str(ctx.author.id)]} coins` in your wallet")
        await ctx.respond(embed=localembed)
        save()
    
    @commands.slash_command(
        name="networth",
        description="Get your networth, or another user's networth"
    )
    @option(name="user", description="Whose networth do you want to find?", type=discord.User, default=None)
    async def networth(self, ctx: ApplicationContext, user: discord.User=None):
        if user == None: user = ctx.author
        try:
            ntw = get_user_networth(user.id)
            localembed = discord.Embed(name=f"{user.display_name}'s networth", description=f"{ntw} coins", color=color)
            await ctx.respond(embed=localembed)
        except KeyError: return await ctx.respond("Looks like that user isn't cached yet. Please try again later.", ephemeral=True)
    
    @commands.slash_command(
        name='inventory', 
        description='Shows the items you (or someone else) own'
    )
    @option(name="user", description="Whose inventory you want to view?", type=discord.User, default=None)
    async def inventory(self, ctx: ApplicationContext, user:discord.User = None):
        if user == None: user = ctx.author
        localembed = discord.Embed(title=f"{user.display_name}'s Inventory")
        filtered_utility_items = list()
        filtered_sellables = list()
        filtered_powerups = list()
        filtered_lootboxes = list()
        parsed_utility_items = str()
        parsed_sellables = str()
        parsed_powerups = str()
        parsed_lootboxes = str()
        for x in shopitem:
            if shopitem[x]['collection'] == "utility": filtered_utility_items.append(x)
            elif shopitem[x]['collection'] == "sellable": filtered_sellables.append(x)
            elif shopitem[x]['collection'] == "power-up": filtered_powerups.append(x)
            elif shopitem[x]['collection'] == "lootbox": filtered_lootboxes.append(x)
        for g in filtered_utility_items:
            if items[str(user.id)][g] != 0:
                parsed_utility_items += f"{shopitem[g]['stylized name']} `ID: {g}`: {items[str(user.id)][g]}\n"
        for g in filtered_sellables:
            if items[str(user.id)][g] != 0:
                parsed_sellables += f"{shopitem[g]['stylized name']} `ID: {g}`: {items[str(user.id)][g]}\n"
        for g in filtered_powerups:
            if items[str(user.id)][g] != 0:
                parsed_powerups += f"{shopitem[g]['stylized name']} `ID: {g}`: {items[str(user.id)][g]}\n"
        for g in filtered_lootboxes:
            if items[str(user.id)][g] != 0:
                parsed_lootboxes += f"{shopitem[g]['stylized name']} `ID: {g}`: {items[str(user.id)][g]}\n"
        if parsed_utility_items != "": localembed.add_field(name='Utility', value=parsed_utility_items, inline=False)
        if parsed_sellables != "": localembed.add_field(name='Sellables', value=parsed_sellables, inline=False)
        if parsed_powerups != "": localembed.add_field(name='Power-ups', value=parsed_powerups, inline=False)
        if parsed_lootboxes != "": localembed.add_field(name='Power-ups', value=parsed_lootboxes, inline=False)
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name='balance', 
        description='Shows your own or another user\'s balance.'
    )
    @option(name="user", description="Which user do you want to view information on?", type=discord.User, default=None)
    async def balance(self, ctx: ApplicationContext, user=None):
        try:
            if user == None: user = ctx.author
            try:
                e = discord.Embed(title=f"{user.display_name}'s balance", color=color)
                e.add_field(name='Cash in wallet', value=f'{currency["wallet"][str(user.id)]} coin(s)', inline=True)
                e.add_field(name='Cash in bank account', value=f'{currency["bank"][str(user.id)]} coin(s)', inline=True)
                e.add_field(name="Networth", value=f"{get_user_networth(user.id)} coin(s)", inline=True)
                await ctx.respond(embed=e)
            except: await ctx.respond('Looks like that user is not indexed in our server. Try again later.', ephemeral=True)
        except Exception as e: await ctx.respond(f'An error occured: `{e}`. This has automatically been reported to the devs.')
    
    @commands.slash_command(
        name="treasury",
        description="See the amount of coins in the isobot treasury."
    )
    async def treasury(self, ctx: ApplicationContext):
        localembed = discord.Embed(description="There are currently {currency['treasury']} coins in the isobot treasury.")
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="leaderboard_nw", 
        description="View the global leaderboard for net worth."
    )
    async def leaderboard_nw(self, ctx: ApplicationContext):
        await ctx.respond("This command is currently disabled due to an internal issue. I apologize for the inconvenience.", ephemeral=True) 
        #await ctx.defer()
        #nw_dict = dict()
        #for person in currency["wallet"]:
        #    nw_dict[str(person)] = int(currency["wallet"][str(person)]) + int(currency["bank"][str(person)])
        #undicted_leaderboard = sorted(nw_dict.items(), key=lambda x:x[1], reverse=True)
        #dicted_leaderboard = dict(undicted_leaderboard)
        #parsed_output = str()
        #y = 1
        #for i in dicted_leaderboard:
        #    if y < 10:
        #        try:
        #            if nw_dict[i] != 0:
        #                user_context = await discord.ext.commands.Bot.fetch_user(self, int(i))
        #                if not user_context.bot:
        #                    print(i, nw_dict[i])
        #                    if y == 1: yf = ":first_place:"
        #                    elif y == 2: yf = ":second_place:"
        #                    elif y == 3: yf = ":third_place:"
        #                    else: yf = f"#{y}"
        #                    parsed_output += f"{yf} **{user_context.name}:** {nw_dict[i]} coins\n"
        #                    y += 1
        #        except discord.errors.NotFound: continue
        #        except Exception as e: print(e)
        #localembed = discord.Embed(title="Global net worth leaderboard", description=parsed_output, color=color)
        #await ctx.respond(embed=localembed)

# Initialization
def setup(bot):
    bot.add_cog(Economy(bot))
