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
        try:
            if len(strok) > 300: return await ctx.respond("Please use no more than `300` character length", ephemeral=True)
            else:
                with open(f"{os.getcwd()}/config/words.json", "r", encoding="utf-8") as f: words = json.load(f)
                var = str()
                s = strok.lower()
                for i, c in enumerate(s): var += random.choice(words[c])
                return await ctx.respond(f"{var}")
        except Exception as e: return await ctx.respond(f"{type(e).__name__}: {e}")
        var = ''.join(arr)
        await ctx.respond(f"{var}")

    @commands.slash_command(
        name='prediction',
        description='Randomly predicts a yes/no question.'
    )
    @option(name="question", description="What do you want to predict?", type=str)
    async def prediction(self, ctx: ApplicationContext, question: str):
        await ctx.respond(f"My prediction is... **{random.choice(['Yes', 'No'])}!**")


# Initialization
def setup(bot): bot.add_cog(Fun(bot))
