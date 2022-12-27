# Imports
import discord
import os.path
import json
import random
from random import randint
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
wdir = os.getcwd()
color = discord.Color.random()

with open(f"{wdir}/database/currency.json", 'r') as f: currency = json.load(f)
with open(f"{wdir}/database/items.json", 'r') as f: items = json.load(f)
with open(f"{wdir}/config/shop.json", 'r') as f: shopitem = json.load(f)

def recache():
    "Replaces the cached databases with new data fetched directly from the database files. Useful if using a multi-cog setup."
    with open(f"{wdir}/database/currency.json", 'r') as f: currency = json.load(f)
    with open(f"{wdir}/database/items.json", 'r') as f: items = json.load(f)

def save():
    with open(f"{wdir}/database/currency.json", 'w+') as f: json.dump(currency, f, indent=4)
    with open(f"{wdir}/database/items.json", 'w+') as f: json.dump(items, f, indent=4)

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
        recache()
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
        recache()
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

    @commands.slash_command(
        name='daily',
        description='Claims your daily (every 24 hours)'
    )
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def daily(self, ctx: ApplicationContext):
        recache()
        currency['wallet'][str(ctx.author.id)] += 10000
        save()
        await ctx.respond(f'You claimed 10000 coins from the daily reward. Check back in 24 hours for your next one!')

    @commands.slash_command(
        name='weekly',
        description='Claims your weekly (every 7 days)'
    )
    @commands.cooldown(1, 302400, commands.BucketType.user)
    async def weekly(self, ctx: ApplicationContext):
        recache()
        currency['wallet'][str(ctx.author.id)] += 45000
        save()
        await ctx.respond(f'You claimed 45000 coins from the weekly reward. Check back in 7 days for your next one!')

    @commands.slash_command(
        name='monthly',
        description='Claims your monthly (every 31 days)'
    )
    @commands.cooldown(1, 1339200, commands.BucketType.user)
    async def monthly(self, ctx: ApplicationContext):
        recache()
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
        recache()
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

    @commands.slash_command(
        name='bankrob',
        description='Raids someone\'s bank account'
    )
    @option(name="user", description="Whose bank account do you want to raid?", type=discord.User)
    @commands.cooldown(1, (60*5), commands.BucketType.user)
    async def bankrob(self, ctx: ApplicationContext, user:discord.User):
        recache()
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

    @commands.slash_command(
        name='hunt',
        description='Pull out your rifle and hunt down animals'
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hunt(self, ctx: ApplicationContext):
        recache()
        if items[str(ctx.author.id)]['rifle'] == 0: return await ctx.respond('I\'d hate to see you hunt with your bare hands. Please buy a hunting rifle from the shop. ||/buy rifle||')
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
            await ctx.respond('Stupid, you died while hunting and lost 1000 coins...')

    @commands.slash_command(
        name='fish',
        description='Prepare your fishing rod and catch some fish'
    )
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def fish(self, ctx: ApplicationContext):
        recache()
        if (items[str(ctx.author.id)]['fishingpole'] == 0): return await ctx.respond('I don\'t think you can fish with your bare hands... or you can just put yo hands in the water bro **giga chad moment**\nAnyway it\'s just better to buy a fishing pole from the shop. ||/buy fishingpole||')
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
        recache()
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


# Initialization
def setup(bot):
    bot.add_cog(Economy(bot))
