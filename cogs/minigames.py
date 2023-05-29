"""The isobot cog file for minigames."""

# Imports
import discord
import json
import os.path
import framework.isobot.currency
from random import randint
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
wdir = os.getcwd()
color = discord.Color.random()
currency = framework.isobot.currency.CurrencyAPI("database/currency.json", "logs/currency.log")

with open(f"{wdir}/database/currency.json", 'r', encoding="utf-8") as f: currency = json.load(f)

def save(): 
    with open(f"{wdir}/database/currency.json", 'w+', encoding="utf-8") as f: json.dump(currency, f)

# Commands
class Minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="guessthenumber",
        description="Guess a random number from 1 to 10 that the bot is thinking about"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guessthenumber(self, ctx: ApplicationContext):
        number = randint(1, 10)
        localembed = discord.Embed(name="Guess the number!", description="I am currently thinking of a number from 1 to 10. Can you guess what it is?", color=color)
        localembed.set_footer(text="If you guess what it is, you will win 500 to 1000 coins!")
        await ctx.respond(embed=localembed)
        def check(msg): return msg.author == ctx.author and msg.channel == ctx.channel and msg.content
        msg = await commands.wait_for("message", check=check)
        if int(msg.content) == number:
            randcoins = randint(500, 1000)
            currency.add(ctx.author.id, randcoins)
            await ctx.respond(f"Correct! You've just won **{randcoins} coins** by guessing the correct number.")
        else: return await ctx.respond("Too bad bozo, you guessed the number wrong and you won nothing.")

    @commands.slash_command(
        name="highlow",
        description="Guess whether the actual number is higher or lower than the hint number"
    )
    @commands.cooldown(1, 40, commands.BucketType.user)
    async def highlow(self, ctx: ApplicationContext):
        numb = randint(1, 100)
        numb2 = randint(1, 100)
        coins = randint(300, 1000)
        def check(msg): return msg.author == ctx.author and msg.channel == ctx.channel and (msg.content)
        localembed = discord.Embed(title=f"Your number is {numb}.", description="Choose if the other number is lower, higher or jackpot.", color=color)
        localembed.set_footer(text="Send your response in chat")
        await ctx.respond(embed=localembed)
        msg = await commands.wait_for("message", check=check)
        if msg.content == 'low':
            if numb > numb2:
                await ctx.respond(f'Congrats! Your number was {numb2} and you won **{coins} coins**.')
                currency.add(ctx.author.id, coins)
            elif numb < numb2: await ctx.respond(f"Wrong! The number was **{numb2}**.")
            elif numb == numb2: await ctx.respond("Rip bozo, you just missed your chance of winning 5 million coins because you didn't choose `jackpot` XD")
        if msg.content == 'jackpot':
            if numb == numb2:
                await ctx.respond(f'Congrats! Your luck did you good because your number was {numb2} and you earned **5 million coins**. GG!')
                currency.add(ctx.author.id, 5000000)
            else: await ctx.respond(f'Wrong! The number was {numb2}.')
        if msg.content == 'high':
            if numb < numb2:
                await ctx.respond(f'Congrats! Your number was {numb2} and you earned **{coins} coins**.')
                currency.add(ctx.author.id, coins)
            else: return await ctx.respond(f'Wrong! The number was {numb2}.')
        else: await ctx.respond(f'wtf is {msg.content}?')

def setup(bot):
    bot.add_cog(Minigames(bot))
