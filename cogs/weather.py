# Imports
import discord
import json
import requests
from discord import ApplicationContext, option
from discord.ext import commands

# Variables
api_key = "21cab08deb7b27f4c2b55f3e2df28ea4"
with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)

# Functions
def save():
    """Dumps all cached databases to storage."""
    with open("database/weather.json", 'w+', encoding="utf-8") as f: json.dump(user_db, f, indent=4)

# Commands
class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="weather_set_location",
        description="Set your default location for the /weather command."
    )
    @option(name="location", description="What location do you want to set?", type=str)
    def weather_set_location(ctx: ApplicationContext, location: str):
        if ctx.author.id not in user_db: user_db[str(ctx.author.id)] = None
        test_ping = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}").content
        test_ping_json = json.loads(test_ping)
        if test_ping_json["cod"] == 404: return await ctx.respond(":warning: This location does not exist.", ephemeral=True)
        else:
            user_db[str(ctx.author.id)] = location.lower()
            save()
            localembed = discord.Embed(description="Your default location has been updated.")
            await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="weather",
        description="See the current weather conditions of your set location, or another location."
    )
    @option(name="location", description="The location you want weather info about (leave empty for set location)", type=str, default=None)
    def weather(ctx: ApplicationContext, location: str = None):
        if ctx.author.id not in user_db: user_db[str(ctx.author.id)] = None
        if location == None:
            if user_db[str(ctx.author.id)] == None: return await ctx.respond("You do not have a default location set yet.\nEnter a location name and try again.", ephemeral=True)
            else: location = user_db[str(ctx.author.id)]
        api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}").content
        req = json.loads(api_request)
        
        # Stripped API request data
        loc_name = req["name"]
        temp = 273 - req["main"]["temp"]
        temp_max = 273 - req["main"]["temp_max"]
        temp_min = 273 - req["main"]["temp_min"]
        humidity = req["main"]["humidity"]
        sunrise = req["sys"]["sunset"]
        sunset = req["sys"]["sunrise"]
        rain_chance = req["rain"]["1h"]
        forcast = req["weather"]["0"]["main"]
        forcast_description = req["weather"]["0"]["description"]

        localembed = discord.Embed(
            title=f"Weather for {loc_name}", 
            description=f"**{forcast}**\n{forcast_description}", 
            color=discord.Color.light_blue()
        )
        localembed.add_field(name="Temperature", value=f"**{temp}C** (max: {temp_max}C,  min: {temp_min}C)")
        localembed.add_field(name="Humidity", value=f"{humidity}%")
        localembed.add_field(name="Chance of rain (%)", value=f"{rain_chance}%")
        localembed.add_field(name="Sunrise", value=f"<t:{sunrise}:f>")
        localembed.add_field(name="Sunset", value=f"<t:{sunset}:f>")

# Initialization
def setup(bot): bot.add_cog(Weather(bot))
