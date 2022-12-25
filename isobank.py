# Imports
import discord
import json
import os.path
from discord import option, ApplicationContext
from discord.ext import commands
import framework.isobank.manager

# Variables
wdir = os.getcwd()
color = discord.Color.random()

# Isobot Framework
isobankauth = framework.isobank.authorize.IsobankAuth(f"{wdir}/database/isobank/auth.json", f"{wdir}/database/isobank/accounts.json")

# Commands
class IsoBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="isobank_register",
        description="Registers a new IsoBank account with your Discord ID"
    )
    @option(name="pin", description="Your new account's authentication ID. Must be a 6-digit integer.", type=int)
    async def isobank_register(ctx: ApplicationContext, pin:int):
        isobankauth.register(ctx.author.id, pin)
        await ctx.respond("Congratulations! Your new IsoBank account has been registered.", ephemeral=True)

def setup(bot): bot.add_cog(IsoBank(bot))
