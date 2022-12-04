# Imports
import discord
from maths import sqrt
from discord.ext import commands
from discord import ApplicationContext, option

# Variables
color = discord.Color.random()


# Commands
class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
    name="squareroot",
    description="Finds the square root of any positive number"
    )
    @option(name="number", description="Which number do you want to find the root of?", type=int)
    async def squareroot(ctx: ApplicationContext, number: int):
        if number < 0: 
            localembed = discord.Embed(description="The square root of a negative number is an imaginary number.", color=color)
            localembed.set_footer(text=f"√({number}) = i√{number}")
            return await ctx.respond(embed=localembed)
        result = sqrt(number)
        localembed = discord.Embed(title=f"Square root of {number}", description=result, color=color)
        localembed.set_footer(text=f"√({number}) = {result}")
        await ctx.respond(embed=localembed)


# Cog Initialization
def setup(bot): bot.add_cog(Maths(bot))
