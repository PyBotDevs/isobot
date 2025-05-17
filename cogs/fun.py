"""The isobot cog file for fun commands."""

# Imports
import discord
import json
import os
import random
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"
color = discord.Color.random()

# Functions
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='stroketranslate',
        description='Gives you the ability to make full words and sentences from a cluster of letters!'
    )
    @option(name="strok", description="What do you want to translate?", type=str)
    async def stroketranslate(self, ctx: ApplicationContext, strok: str):
        """Gives you the ability to make full words and sentences from a cluster of letters!"""
        if len(strok) > 300: return await ctx.respond("Please use no more than `300` character length", ephemeral=True)
        else:
            with open(f"{client_data_dir}/config/words.json", "r", encoding="utf-8") as f: words = json.load(f)
            var = str()
            s = strok.lower()
            for i, c in enumerate(s): var += random.choice(words[c])
            return await ctx.respond(f"{var}")
        var = ''.join(arr)
        await ctx.respond(f"{var}")

    @commands.slash_command(
        name='prediction',
        description='Randomly predicts a yes/no question.'
    )
    @option(name="question", description="What do you want to predict?", type=str)
    async def prediction(self, ctx: ApplicationContext, question: str):
        await ctx.respond(f"My prediction is... **{random.choice(['Yes', 'No'])}!**")

    @commands.slash_command(
        name="owoify",
        description="Owoify any text you want!"
    )
    @option(name="text", description="The text you want to owoify", type=str)
    async def owoify(self, ctx: ApplicationContext, text: str):
        """Owoify any text you want!"""
        text = text.replace("r", "w")
        text = text.replace("l", "w")
        text = text.replace("the", "da")
        text = text.replace("you", "u")
        text = text.replace("your", "ur")
        text += random.choice((" uwu", " owo", " UwU", " OwO", " XDDD", " :D", " ;-;", " <3", " ^-^", " >-<"))
        await ctx.respond(text)

    @commands.slash_command(
        name="hackertext",
        description="Turn any text into m4st3r h4xx0r text."
    )
    @option(name="text", description="The text that you want to convert", type=str)
    async def hackertext(self, ctx: ApplicationContext, text: str):
        """Turn any text into m4st3r h4xx0r text."""
        text = text.lower()
        text = text.replace("a", "4")
        text = text.replace("l", "1")
        text = text.replace("e", "3")
        text = text.replace("o", "0")
        text = text.replace("c", "x")
        text = text.replace("u", "x")
        text = text.replace("t", "7")
        await ctx.respond(text)
    
    @commands.slash_command(
        name="randomnumber",
        description="Choose a random number from x to y."
    )
    @option(name="x", description="The minimum limit of the random number.", type=int)
    @option(name="y", description="The maximum limit of the random number.", type=int)
    async def randomnumber(self, ctx: ApplicationContext, x: int, y: int):
        """Choose a random number from x to y."""
        if x > y:
            return await ctx.respond(":x: Your minimum limit needs to be lower than the maximum limit!", ephemeral=True)
        await ctx.respond(f"Your random number is `{random.randint(x, y)}`\n\nMinimum limit: `{x}`\nMaximum limit: `{y}`")

    @commands.slash_command(
        name="howgay",
        description="See the gay percentage of a person!"
    )
    @option(name="user", description="The person who you want to gayrate", type=discord.User, default=None)
    async def howgay(self, ctx: ApplicationContext, user: discord.User = None):
        """See the gay percentage of a person!"""
        if user == None:
            user = ctx.author
        rating = random.randint(0, 100)
        response = str()
        if rating == 0:
            response = "You are straighter than your bedroom walls!"
        elif rating <= 30:
            response = "You are the average person in society"
        elif rating <= 60:
            response = "You're pretty gay tbh"
        elif rating <= 90:
            response = "You're really gay!"
        elif rating <= 99:
            response = "You are **extremely gay**!! No cap"
        elif rating == 100:
            response = "You are ***SUPER*** gay!!! You're so gay you make gay people look straight"
        localembed = discord.Embed(
            title=f":rainbow_flag: {user.display_name}'s gay rating",
            description=f"{user.display_name} is **{rating}%** gay! {response}",
            color=discord.Color.random()
        )
        await ctx.respond(embed=localembed)

# Initialization
def setup(bot): bot.add_cog(Fun(bot))
