# Imports
import discord
import json
import requests
import os
from framework.isobot.db import weather
from discord import ApplicationContext, option
from discord.ext import commands

# Variables
#api_key = os.environ['openweathermap_API_KEY']
api_key = auth.ext_token('openweathermap')
weather = weather.Weather()

# Commands
class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="weather_set_location",
        description="Set your default location for the /weather command."
    )
    @option(name="location", description="What location do you want to set?", type=str)
    async def weather_set_location(self, ctx: ApplicationContext, location: str):
        weather.new(ctx.author.id)
        test_ping = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}").content
        test_ping_json = json.loads(test_ping)
        if test_ping_json["cod"] == '404': return await ctx.respond(":warning: This location does not exist.", ephemeral=True)
        else:
            weather.set_default_location(ctx.author.id, location.lower())
            localembed = discord.Embed(description="Your default location has been updated.", color=discord.Color.green())
            await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="weather_set_scale",
        description="Set your preferred unit scale for temperature for the /weather command."
    )
    @option(name="scale", description="Which scale do you want to use?", type=str, choices=["Celsius", "Fahrenheit", "Kelvin"])
    async def weather_set_scale(self, ctx: ApplicationContext, scale: str):
        weather.new(ctx.author.id)
        if scale not in ["Celsius", "Fahrenheit", "Kelvin"]: return 1
        weather.set_scale(ctx.author.id, scale)
        localembed = discord.Embed(description="Your preferred unit scale has been updated.", color=discord.Color.green())
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="weather",
        description="See the current weather conditions of your set location, or another location."
    )
    @option(name="location", description="The location you want weather info about (leave empty for set location)", type=str, default=None)
    async def weather(self, ctx: ApplicationContext, location: str = None):
        weather.new(ctx.author.id)
        if location == None:
            if weather.get_default_location(ctx.author.id) == None: return await ctx.respond("You do not have a default location set yet.\nEnter a location name and try again.", ephemeral=True)
            else: location = weather.get_default_location(ctx.author.id)
        location = location.replace(" ", "%20")
        api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}").content
        req: dict = json.loads(api_request)
        print(req)
        if req["cod"] == '404': return await ctx.respond(":x: This location was not found. Check your spelling or try another location instead.", ephemeral=True)
        elif req["cod"] != 200:
            print(f"Unable to fetch API request successfully in /weather: Status code {req['cod']}")
            return await ctx.respond("A slight problem occured when trying to get information. This error has been automatically reported to the devs.", ephemeral=True)
        else: pass

        # Stripped API request data
        loc_name = req["name"]
        if weather.get_scale(ctx.author.id) == "Celsius":
            temp = round(req["main"]["temp"] - 273)
            temp_max = round(req["main"]["temp_max"] - 273)
            temp_min = round(req["main"]["temp_min"] - 273)
        elif weather.get_scale(ctx.author.id) == "Fahrenheit":
            temp = round(((req["main"]["temp"] - 273) * 9/5) + 32)
            temp_max = round(((req["main"]["temp_max"] - 273) * 9/5) + 32)
            temp_min = round(((req["main"]["temp_min"] - 273) * 9/5) + 32)
        else:
            temp = round(req["main"]["temp"])
            temp_max = round(req["main"]["temp_max"])
            temp_min = round(req["main"]["temp_min"])
        humidity = req["main"]["humidity"]
        sunset = req["sys"]["sunset"]
        sunrise = req["sys"]["sunrise"]
        forcast = req["weather"][0]["main"]
        forcast_description = req["weather"][0]["description"]

        localembed = discord.Embed(
            title=f"Weather for {loc_name} :flag_{req['sys']['country'].lower()}:",
            description=f"**{forcast}**\n{forcast_description}",
            color=discord.Color.blue()
        )
        if weather.get_scale(ctx.author.id) == "Celsius": localembed.add_field(name="Temperature", value=f"**{temp}C** (max: {temp_max}C,  min: {temp_min}C)")
        elif weather.get_scale(ctx.author.id) == "Fahrenheit": localembed.add_field(name="Temperature", value=f"**{temp}F** (max: {temp_max}F,  min: {temp_min}F)")
        else: localembed.add_field(name="Temperature", value=f"**{temp}K** (max: {temp_max}K,  min: {temp_min}K)")
        localembed.add_field(name="Humidity", value=f"{humidity}%")
        localembed.add_field(name="Sunrise", value=f"<t:{sunrise}:f>", inline=False)
        localembed.add_field(name="Sunset", value=f"<t:{sunset}:f>", inline=True)
        await ctx.respond(embed=localembed)

# Initialization
def setup(bot): bot.add_cog(Weather(bot))
