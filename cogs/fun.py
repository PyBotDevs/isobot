# Imports
import discord
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
                with open(f"{os.getcwd()}/config/words.json", "r") as f: words = json.load(f)
                var = str()
                s = strok.lower()
                for i, c in enumerate(s): var += random.choice(words[c])
                return await ctx.respond(f"{var}")
        except Exception as e: return await ctx.respond(f"{type(e).__name__}: {e}")
        var = ''.join(arr)
        await ctx.respond(f"{var}")

# Initialization
def setup(bot): bot.add_cog(Fun(bot))
