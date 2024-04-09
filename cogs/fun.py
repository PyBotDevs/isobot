"""The isobot cog file for fun commands."""

# Imports
import discord
import json
import os
import random
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
color = discord.Color.random()

# Functions
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='stroketranslate',
        description='Gives you the ability to make full words and sentences from a cluster of letters'
    )
    @option(name="strok", description="What do you want to translate?", type=str)
    async def stroketranslate(self, ctx: ApplicationContext, strok: str):
        if len(strok) > 300: return await ctx.respond("Please use no more than `300` character length", ephemeral=True)
        else:
            with open(f"{os.getcwd()}/config/words.json", "r", encoding="utf-8") as f: words = json.load(f)
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
        text += random.choice([" uwu", " owo", " UwU", " OwO", " XDDD", " :D", " ;-;", " <3", " ^-^", " >-<"])
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

# Initialization
def setup(bot): bot.add_cog(Fun(bot))
