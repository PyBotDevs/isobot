# Imports
import discord
from math import sqrt
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
    async def squareroot(self, ctx: ApplicationContext, number: int):
        if number < 0: 
            localembed = discord.Embed(description="The square root of a negative number is an imaginary number.", color=color)
            localembed.set_footer(text=f"√({number}) = i√{number}")
            return await ctx.respond(embed=localembed)
        result = sqrt(number)
        localembed = discord.Embed(title=f"Square root of {number}", description=result, color=color)
        localembed.set_footer(text=f"√({number}) = {result}")
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="area_square",
        description="Finds the area of a square"
    )
    @option(name="length", description="What is the length of one side?", type=int)
    async def area_square(self, ctx: ApplicationContext, length: int):
        if length < 0: return await ctx.respond("Length cannot be lower than 0 units.")
        result = length * length
        localembed = discord.Embed(title=f"Area of square of side {length} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"A = s²\n{length} x {length} = {result} sq. units")
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="area_rectangle",
        description="Finds the area of a rectangle"
    )
    @option(name="length", description="What is the length?", type=int)
    @option(name="breadth", description="What is the breadth?", type=int)
    async def area_square(self, ctx: ApplicationContext, length: int, breadth: int):
        if length < 0: return await ctx.respond("Length cannot be lower than 0 units.")
        elif breadth < 0: return await ctx.respond("Breadth cannot be lower than 0 units.")
        result = length * breadth
        localembed = discord.Embed(title=f"Area of rectangle of length {length} units and breadth {breadth} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"A = l x b\n{length} x {breadth} = {result} sq. units")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="area_circle",
        description="Finds the area of a circle"
    )
    @option(name="radius", description="What is the radius of the circke?", type=int)
    async def area_circle(self, ctx: ApplicationContext, radius: int):
        if radius < 0: return await ctx.respond("Radius cannot be lower than 0 units.")
        result = ((22/7) * radius) ^ 2
        localembed = discord.Embed(title=f"Area of circle of radius {radius} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nA = πr²\nπ x {radius}² = {result} sq. units")
        await ctx.respond(embed=localembed)


# Cog Initialization
def setup(bot): 
    bot.add_cog(Maths(bot))
