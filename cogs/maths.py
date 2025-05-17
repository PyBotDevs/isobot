"""The isobot cog file for maths commands."""

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

    math = SlashCommandGroup("math", "Use various math tools.")

    @math.command(
        name="squareroot",
        description="Finds the square root of any positive number."
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
    
    @math.command(
        name="solve_quadratic_roots",
        description="Find the (real) root(s) of a quadratic equation/function."
    )
    @option(name="coeff_a", description="Coefficient 'a' of the equation", type=int)
    @option(name="coeff_b", description="Coefficient 'b' of the equation", type=int)
    @option(name="coeff_c", description="Coefficient 'c' of the equation", type=int)
    async def math_solve_quadratic_roots(self, ctx: ApplicationContext, coeff_a: int, coeff_b: int, coeff_c: int):
        """Find the (real) root(s) of a quadratic equation/function."""
        # First finding discrim of Q.E
        a = coeff_a
        b = coeff_b
        c = coeff_c
        discrim = (b^2) - 4 * a * c
        if discrim >= 0:
            root_1 = (-b * sqrt((b^2) - 4 * a * c))/2*a
            root_2 = (-b * -sqrt((b^2) - 4 * a * c))/2*a
            result = f"The roots of the quadratic equation are:\n- **Root 1:** {root_1}``\n- **Root 2:** {root_2}``\n\n```Equation:\n\nf(x) = {a}x² + {b}x + {c} = 0```"
        else:
            result = "The roots of the quadratic equation are imaginary."
        localembed = discord.Embed(
            title=f"Roots of the Quadratic Equation **{a}x² + {b}x + {c} = 0**",
            description=result
        )
        await ctx.respond(embed=localembed)

    @math.command(
        name="area_square",
        description="Finds the area of a square."
    )
    @option(name="length", description="What is the length of one side?", type=int)
    async def area_square(self, ctx: ApplicationContext, length: int):
        if length < 0: return await ctx.respond("Length cannot be lower than 0 units.")
        result = length * length
        localembed = discord.Embed(title=f"Area of square of side {length} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"A = s²\n{length} x {length} = {result} sq. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="area_rectangle",
        description="Finds the area of a rectangle."
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

    @math.command(
        name="area_circle",
        description="Finds the area of a circle."
    )
    @option(name="radius", description="What is the radius of the circle?", type=int)
    @option(name="pi", description="Set a value for π (default is 22/7)", type=str, choices=["22/7", "3.14", "3"], default="22/7")
    async def area_circle(self, ctx: ApplicationContext, radius: int, pi: str = "22/7"):
        if radius < 0: return await ctx.respond("Radius cannot be lower than 0 units.")
        if pi == "22/7": result = (22/7) * (radius * radius)
        elif pi == "3.14": result = 3.14 * (radius * radius)
        elif pi == "3": result = 3 * (radius * radius)
        localembed = discord.Embed(title=f"Area of circle of radius {radius} units", description=f"{result} sq. units", color=color)
        if pi == "22/7": localembed.set_footer(text=f"Taking π as 22/7\nA = πr²\nπ x {radius}² = {result} sq. units")
        elif pi == "3.14": localembed.set_footer(text=f"Taking π as 3.14\nA = πr²\nπ x {radius}² = {result} sq. units")
        elif pi == "3":localembed.set_footer(text=f"Taking π as 3\nA = πr²\nπ x {radius}² = {result} sq. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="area_triangle",
        description="Finds the area of a triangle. (using Heron's formula)"
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

    # Volume Commands
    @math.command(
        name="volume_cuboid",
        description="Find the volume of a cuboid. (use only length for volume of cube)"
    )
    @option(name="length", description="The length of the cuboid", type=float)
    @option(name="breadth", description="The breadth of the cuboid", type=float, default=None)
    @option(name="height", description="The height/depth of the cuboid", type=float, default=None)
    async def volume_cuboid(self, ctx: ApplicationContext, length: float, breadth: float = None, height: float = None):
        if (breadth != None and height == None) or (height != None and breadth == None): return await ctx.respond("Both `breadth` and `height` arguments needs to be filled!")
        if breadth == None and height == None:
            breadth = length
            height = length
        result = length * breadth * height
        localembed = discord.Embed(title=f"Volume of cuboid (l: {length}, b: {breadth}, h: {height})", description=f"{result} cu. units", color=color)
        localembed.set_footer(text=f"v = (l x b x h)\n{length} x {breadth} x {height} = {result} cu. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="volume_sphere",
        description="Find the volume of a sphere."
    )
    @option(name="radius", description="The radius of the corresponding sphere", type=float)
    async def volume_sphere(self, ctx: ApplicationContext, radius: float):
        if radius < 0: return await ctx.respond("The radius of the sphere cannot be negative.")
        result = ((22/7) * (radius ** 3)) * 4/3
        localembed = discord.Embed(title=f"Volume of sphere of radius {radius} units", description=f"{result} cu. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nv = 4/3 x πr\u00B3\n4/3 x π x {radius}\u00B3 = {result} cu. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="volume_hemisphere",
        description="Find the volume of a hemisphere."
    )
    @option(name="radius", description="The radius of the corresponding hemisphere", type=float)
    async def volume_sphere(self, ctx: ApplicationContext, radius: float):
        if radius < 0: return await ctx.respond("The radius of the hemisphere cannot be negative.")
        result = ((22/7) * (radius ** 3)) * 2/3
        localembed = discord.Embed(title=f"Volume of hemisphere of radius {radius} units", description=f"{result} cu. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nv = 2/3 x πr\u00B3\n2/3 x π x {radius}\u00B3 = {result} cu. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="volume_cylinder",
        description="Find the volume of a cylinder."
    )
    @option(name="radius", description="The radius of the cylinder", type=float)
    @option(name="height", description="The height of the cylinder", type=float)
    async def volume_cylinder(self, ctx: ApplicationContext, radius: float, height: float):
        if radius < 0 or height < 0: return await ctx.respond("The `radius` and `height` arguments cannot be negative!")
        result = ((22/7) * (radius ** 2)) * height
        localembed = discord.Embed(title=f"Volume of cylinder (radius: {radius}, height: {height})", description=f"{result} cu. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nv = πr²h\nπ x {radius}² x {height} = {result} cu. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="volume_cone",
        description="Find the volume of a cone."
    )
    @option(name="radius", description="The radius of the base of the cone", type=float)
    @option(name="height", description="The height of the cone", type=float)
    async def volume_cylinder(self, ctx: ApplicationContext, radius: float, height: float):
        if radius < 0 or height < 0: return await ctx.respond("The `radius` and `height` arguments cannot be negative!")
        result = (1/3) * (((22/7) * (radius ** 2)) * height)
        localembed = discord.Embed(title=f"Volume of cone (base radius: {radius}, height: {height})", description=f"{result} cu. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\nv = 1/3 x πr²h\n1/3 x π x {radius}² x {height} = {result} cu. units")
        await ctx.respond(embed=localembed)

    # Surface Area Commands
    @math.command(
        name="surfacearea_cuboid",
        description="Find the surface area of a cuboid. (use only length for cube)"
    )
    @option(name="length", description="The length of the cuboid", type=float)
    @option(name="breadth", description="The breadth of the cuboid", type=float, default=None)
    @option(name="height", description="The height/depth of the cuboid", type=float, default=None)
    async def surfacearea_cuboid(self, ctx: ApplicationContext, length: float, breadth: float = None, height: float = None):
        if (breadth != None and height == None) or (height != None and breadth == None): return await ctx.respond("Both `breadth` and `height` arguments needs to be filled!")
        if breadth == None and height == None:
            breadth = length
            height = length
        result = 2 * ((length * breadth) + (breadth * height) + (height * length))
        localembed = discord.Embed(title=f"Surface Area of cuboid (l: {length}, b: {breadth}, h: {height})", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"a = 2(lb x bh x hl)\n2(({length} x {breadth}) + ({breadth} x {height}) + ({height} x {length})) = {result} sq. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="surfacearea_sphere",
        description="Find the surface area of a sphere."
    )
    @option(name="radius", description="The radius of the sphere", type=float)
    async def surfacearea_sphere(self, ctx: ApplicationContext, radius: float):
        if radius < 0: return await ctx.respond("The `radius` argument cannot be negative!")
        result = 4 * ((22/7) * (radius ** 2))
        localembed = discord.Embed(title=f"Surface Area of sphere of radius {radius} units", description=f"{result} sq. units", color=color)
        localembed.set_footer(text=f"Taking π as 22/7\na = 4 x πr²\n4 x π x {radius}² = {result} sq. units")
        await ctx.respond(embed=localembed)
    
    @math.command(
        name="surfacearea_hemisphere",
        description="Find the surface area of a hemisphere."
    )
    @option(name="mode", description="Do you want to calculate for CSA or TSA?", type=str, choices=["CSA", "TSA"])
    @option(name="radius", description="The radius of the hemisphere", type=float)
    async def surfacearea_hemisphere(self, ctx: ApplicationContext, mode: str, radius: float):
        if radius < 0: return await ctx.respond("The `radius` argument cannot be negative!")
        if mode == "CSA":
            result = 2 * ((22/7) * (radius ** 2))
            localembed = discord.Embed(title=f"Curved Surface Area of hemisphere of radius {radius} units", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\na = 2 x πr²\n4 x π x {radius}² = {result} sq. units")
        else:
            result = 3 * ((22/7) * (radius ** 2))
            localembed = discord.Embed(title=f"Total Surface Area of hemisphere of radius {radius} units", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\na = 3 x πr²\n4 x π x {radius}² = {result} sq. units")
        await ctx.respond(embed=localembed)
    
    @math.command(
        name="surfacearea_cylinder",
        description="Find the surface area of a cylinder."
    )
    @option(name="mode", description="Do you want to calculate for CSA or TSA?", type=str, choices=["CSA", "TSA"])
    @option(name="radius", description="The radius of the cylinder", type=float)
    @option(name="height", description="The height of the cylinder", type=float)
    async def surfacearea_cylinder(self, ctx: ApplicationContext, mode: str, radius: float, height: float):
        if radius < 0 or height < 0: return await ctx.respond("The `radius` and `height` arguments cannot be negative!")
        if mode == "CSA":
            result = 2 * (22/7) * radius * height
            localembed = discord.Embed(title=f"Curved Surface Area of cylinder (r: {radius}, h: {height})", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\na = 2πrh\n2 x π x {radius} x {height} = {result} sq. units")
        else:
            result = 2 * (22/7) * radius * (radius + height)
            localembed = discord.Embed(title=f"Total Surface Area of cylinder (r: {radius}, h: {height})", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\na = 2πr x (r + h)\n2 x π x {radius} x ({radius} + {height}) = {result} sq. units")
        await ctx.respond(embed=localembed)

    @math.command(
        name="surfacearea_cone",
        description="Find the surface area of a cone."
    )
    @option(name="mode", description="Do you want to calculate for CSA or TSA?", type=str, choices=["CSA", "TSA"])
    @option(name="radius", description="The radius of the cone", type=float)
    @option(name="height", description="The height of the cone", type=float)
    async def surfacearea_cone(self, ctx: ApplicationContext, mode: str, radius: float, height: float):
        if radius < 0 or height < 0: return await ctx.respond("The `radius` and `height` arguments cannot be negative!")
        slant_height = round(sqrt(radius + height), 3)
        if mode == "CSA":
            result = (22/7) * radius * slant_height
            localembed = discord.Embed(title=f"Curved Surface Area of cone (r: {radius}, h: {height})", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\nl = √(r + h)\na = πrl\nπ x {radius} x {slant_height} = {result} sq. units")
        else:
            result = (22/7) * radius * (slant_height + radius)
            localembed = discord.Embed(title=f"Total Surface Area of cone (r: {radius}, h: {height})", description=f"{result} sq. units", color=color)
            localembed.set_footer(text=f"Taking π as 22/7\nl = √(r + h)\na = πr x (l + r)\nπ x {radius} x ({slant_height} + {radius}) = {result} sq. units")
        await ctx.respond(embed=localembed)

# Initialization
def setup(bot):
    bot.add_cog(Maths(bot))
