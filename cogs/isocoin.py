"""The isobot cog file for the IsoCoin system."""

# Imports
import random
import json
import os
import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"
# if not os.path.isdir("database"):  # TEMPORARY: Allow cog to handle "database" directory generation (for now)
#     os.mkdir("database")
if not os.path.isfile(f"{client_data_dir}/database/isotokens.json"):  # Generate database file, if missing.
    with open(f"{client_data_dir}/database/isotokens.json", 'x', encoding="utf-8") as f:
        json.dump({}, f)
        f.close()

with open(f"{client_data_dir}/database/isotokens.json", 'r', encoding="utf-8") as f: isocoins = json.load(f)

def save():
    with open(f"{client_data_dir}/database/isotokens.json", 'w+', encoding="utf-8") as f: json.dump(isocoins, f)

# Functions
def create_isocoin_key(user_id: int) -> int:
    """Creates a new isocoin key and value for the specified user.\n\nReturns `0` if successful, returns `1` if user is already cached."""
    if str(user_id) not in isocoins: 
        isocoins[str(user_id)] = 0
        return 0
    else: return 1

# Commands
class IsoCoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    isocoin_system = SlashCommandGroup("isocoin", "Commands related to the IsoCoin rewards system.")

    @isocoin_system.command(
        name="balance",
        description="See your IsoCoin balances"
    )
    async def isocoin_balance(self, ctx: ApplicationContext):
        localembed = discord.Embed(description=f"You currently have **{isocoins[str(ctx.author.id)]}** IsoCoins.")
        await ctx.respond(embed=localembed)

    @isocoin_system.command(
        name="daily",
        description="Collect your daily reward of IsoCoins"
    )
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def isocoin_daily(self, ctx: ApplicationContext):
        isocoins_reward = random.randint(2500, 5000)
        isocoins[str(ctx.author.id)] += isocoins_reward
        save()
        await ctx.respond(f"You have earned {isocoins_reward} IsoCoins from this daily. Come back in 24 hours for the next one!")

    @isocoin_system.command(
        name="shop",
        description="See all the items that you can buy using your IsoCoins."
    )
    async def isocoin_shop(self, ctx: ApplicationContext):
        await ctx.respond("IsoCoin shop is coming soon! Check back later for new items.")

# Cog Initialization
def setup(bot): bot.add_cog(IsoCoin(bot))
