"""The isobot cog for managing and handling IsoCard."""

# Imports
import discord
import json
import os
import random
import time
from discord import option, ApplicationContext, SlashCommandGroup
from discord.ext import commands

# Variables
with open("database/isocard.json", 'r', encoding="utf-8") as f: isocard_db = json.load(f)

def save():
    with open("database/isocard.json", 'w+', encoding="utf-8") as f: json.dump(isocard_db, f, indent=4)

def generate_card_id() -> int:
    # Generate 16 random digits and append to a str variable
    new_card_id = str()
    i = 1
    while i != 16:
        new_card_id += str(random.randint(0, 9))
        i += 1
    print(new_card_id)
    return new_card_id

# Commands
class IsoCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    isocard = SlashCommandGroup("isocard", "Commands used for managing and handling IsoCard.")

    @isocard.command(
        name="register",
        description="Register a new IsoCard in your account."
    )
    @option(name="scc", description="The Special Security Code for your new card. (aka. CVV)", type=int)
    async def register(self, ctx: ApplicationContext, scc: int):
        try:
            new_card_id = generate_card_id()
            isocard_db[str(new_card_id)] = {
                "cardholder_user_id": ctx.author.id,
                "cardholder_name": ctx.author.name,
                "scc": scc,
                "card_registration_timestamp": round(time.time()),
                "type": "standard"
            }
            save()
            localembed = discord.Embed(title=":tada: Congratulations!", description="Your new IsoCard has successfully been registered!", color=discord.Color.green())
            localembed.add_field(name="Cardholder name", value=ctx.author.name, inline=False)
            localembed.add_field(name="Card number", value=new_card_id, inline=False)
            localembed.add_field(name="SCC", value=f"`{scc}`", inline=True)
            localembed.add_field(name="Card registration date", value=f"<t:{isocard_db[str(new_card_id)]['card_registration_timestamp']}:d>", inline=False)
            localembed.set_footer(text="Always remember, NEVER share your card info to anyone!")
            await ctx.respond(embed=localembed, ephemeral=True)
        except Exception as e: print(e)

# Initialization
def setup(bot): bot.add_cog(IsoCard(bot))
