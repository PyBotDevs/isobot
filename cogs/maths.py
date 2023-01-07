# Imports
import discord
from math import sqrt
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import ApplicationContext, option

# Variables
color = discord.Color.random()

# Commands
class Maths(commands.Cog):
    def __init__(self, bot): self.bot = bot
    
    area = SlashCommandGroup("area", "Find area of different figures.")

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
    
    @area.command(
        name="square",
        description="Finds the area of a square"
    )
    @option(name="length", description="What is the length of one side?", type=int)
    async def area_square(self, ctx: ApplicationContext, length: int):
        if length < 0: return await ctx.respond("Length cannot be lower than 0 units.")
        result = length * length
        localembed = discord.Embed(title=f"Area of square of side {length} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"A = s²\n{length} x {length} = {result} sq. units")
        await ctx.respond(embed=localembed)
    
    @area.command(
        name="rectangle",
        description="Finds the area of a rectangle"
    )
    @option(name="length", description="What is the length?", type=int)
    @option(name="breadth", description="What is the breadth?", type=int)
    async def area_rectangle(self, ctx: ApplicationContext, length: int, breadth: int):
        if length < 0: return await ctx.respond("Length cannot be lower than 0 units.")
        elif breadth < 0: return await ctx.respond("Breadth cannot be lower than 0 units.")
        result = length * breadth
        localembed = discord.Embed(title=f"Area of rectangle of length {length} units and breadth {breadth} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"A = l x b\n{length} x {breadth} = {result} sq. units")
        await ctx.respond(embed=localembed)

    @area.command(
        name="circle",
        description="Finds the area of a circle"
    )
    @option(name="radius", description="What is the radius of the circle?", type=int)
    async def area_circle(self, ctx: ApplicationContext, radius: int):
        if radius < 0: return await ctx.respond("Radius cannot be lower than 0 units.")
        result = (22/7) * (radius * radius)
        localembed = discord.Embed(title=f"Area of circle of radius {radius} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nA = πr²\nπ x {radius}² = {result} sq. units")
        await ctx.respond(embed=localembed)
    
    @area.command(
        name="triangle",
        description="Finds the area of a triangle (using Heron's formula)"
    )
    @option(name="side_length_a", description="What is the length of side A of the triangle?", type=int)
    @option(name="side_length_b", description="What is the length of side B of the triangle?", type=int)
    @option(name="side_length_c", description="What is the length of side C of the triangle?", type=int)
    async def area_triangle(self, ctx: ApplicationContext, side_length_a: int, side_length_b: int, side_length_c: int):
        if side_length_a < 0 or side_length_b < 0 or side_length_c < 0: return await ctx.respond("Any side of the triangle cannot be less than 0.")
        s = (side_length_a + side_length_b + side_length_c)/2
        eq1 = s - side_length_a
        eq2 = s - side_length_b
        eq3 = s - side_length_c
        result = sqrt(s * (eq1) * (eq2) * (eq3))
        localembed = discord.Embed(title=f"Area of triangle (a = {side_length_a}, b = {side_length_b}, c = {side_length_c})", description=f"{result} sq. units", color=color)
        localembed.set_footer(text="s = (a + b + c) / 2\nA = √(s x (s - a) x (s - b) x (s - c))")
        await ctx.respond(embed=localembed)

# Cog Initialization
def setup(bot): bot.add_cog(Maths(bot))
