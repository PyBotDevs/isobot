"""The isobot cog for managing and handling IsoCard."""

# Imports
import discord
import random
from framework.isobot.db.isocard import IsoCard
from discord import option, ApplicationContext, SlashCommandGroup
from discord.ext import commands

# Variables and Functions
isocard_db = IsoCard()

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
    @option(name="ssc", description="The Special Security Code for your new card. (aka. CVV)", type=int)
    async def register(self, ctx: ApplicationContext, ssc: int):
        new_card_id = generate_card_id()
        new_card_data = isocard_db.generate(new_card_id, ctx.author.id, ctx.author.name, ssc)
        localembed = discord.Embed(title=":tada: Congratulations!", description="Your new IsoCard has successfully been registered!", color=discord.Color.green())
        localembed.add_field(name="Cardholder name", value=ctx.author.name, inline=False)
        localembed.add_field(name="Card number", value=new_card_id, inline=False)
        localembed.add_field(name="SSC", value=f"`{ssc}`", inline=True)
        localembed.add_field(name="Card registration date", value=f"<t:{new_card_data['card_registration_timestamp']}:d>", inline=False)
        localembed.set_footer(text="Always remember, NEVER share your card info to anyone!")
        await ctx.respond(embed=localembed, ephemeral=True)

    @isocard.command(
        name="info",
        description="View information on your IsoCard."
    )
    @option(name="card_number", description="Enter your card number of the card you want to view.", type=int)
    async def info(self, ctx: ApplicationContext, card_number: int):
        try:
            try: card_data = isocard_db.fetch_card_data(card_number)
            except KeyError: return await ctx.respond("There was a problem with your card number. Please check it and try again.", ephemeral=True)
            if card_data["cardholder_user_id"] != ctx.author.id: return await ctx.respond("You do not have permission to access this IsoCard.\n If you think this is an error, please contact the devs.", ephemeral=True)
            localembed = discord.Embed(
                title=":credit_card: Your IsoCard information",
                description=f"**Card type:** {card_data['type']}",
                color=discord.Color.random()
            )
            localembed.add_field(name="Cardholder name", value=card_data['cardholder_name'], inline=True)
            localembed.add_field(name="Cardholder user id", value=card_data['cardholder_user_id'], inline=True)
            localembed.add_field(name="Card number", value=card_number, inline=False)
            if card_data["config"]["card_label"] != None: localembed.add_field(name="Card Label", value=f"'{card_data['config']['card_label']}'", inline=True)
            localembed.add_field(name="SSC", value=f"`{card_data['ssc']}`", inline=False)
            localembed.add_field(name="Card registration date", value=f"<t:{card_data['card_registration_timestamp']}:d>", inline=False)
            localembed.add_field(name="Daily spend limit", value=f"~~{card_data['config']['spend_limit']} coins~~ NA", inline=False)
            localembed.set_footer(text="Always remember, NEVER share your card info to anyone!")
            await ctx.respond(embed=localembed, ephemeral=True)
        except Exception as e: print(e)

    @isocard.command(
        name="my_cards",
        description="View a list of all your cards."
    )
    async def my_card(self, ctx: ApplicationContext):
        all_card_numbers = isocard_db.keys()
        your_cards = list()
        for card in all_card_numbers:
            if isocard_db[str(card)]["cardholder_user_id"] == ctx.author.id: your_cards.append(str(card))
        embed_desc = str()
        sr = 1
        for card in your_cards:
            if isocard_db[str(card)]["config"]["card_label"] != None:
                embed_desc += f"{sr}. **{card}**: {isocard_db[str(card)]['config']['card_label']}\n"
            else: embed_desc += f"{sr}. **{card}**\n"
            sr += 1
        embed_desc += "\n*Nothing more here*"
        localembed = discord.Embed(
            title=":credit_card: My cards",
            description=embed_desc,
            color=discord.Color.random()
        )
        localembed.set_footer(text="Always remember, NEVER share your card info to anyone!")
        await ctx.respond(embed=localembed, ephemeral=True)

    @isocard.command(
        name="options_label",
        description="Set your IsoCard's label"
    )
    @option(name="card_number", description="Enter your card number that you want to work with.", type=int)
    @option(name="new_label", description="What do you want your new card label to be?", type=str, default=None)
    async def options_label(self, ctx: ApplicationContext, card_number: int, new_label: str):
        try: card_data = isocard_db.fetch_card_data(card_number)
        except KeyError: return await ctx.respond("There was a problem with your card number. Please check it and try again.", ephemeral=True)
        if card_data["cardholder_user_id"] != ctx.author.id: return await ctx.respond("You do not have permission to access this IsoCard.\n If you think this is an error, please contact the devs.", ephemeral=True)
        isocard_db.set_card_label(card_number, new_label)
        if new_label == None: return await ctx.respond(embed=discord.Embed(description=":white_check_mark: Your card label has been reset.", color=discord.Color.green()), ephemeral=True)
        else: return await ctx.respond(embed=discord.Embed(description=":white_check_mark: Your card label has been edited.", color=discord.Color.green()), ephemeral=True)

    @isocard.command(
        name="verify_transaction",
        description="Verify an ongoing transaction."
    )
    @option(name="verification_code", description="The 6-digit verification code for your transaction", type=int)
    async def verify_transaction(ctx: ApplicationContext, verification_code: int):
        try:
            with open("database/isocard_transactions.json", 'r') as f: transactions_db = json.load(f)
            if transactions_db[str(verification_code)]["payer_id"] == ctx.author.id:
                transactions_db[str(verification_code)]["status"] = "complete"
                with open("database/isocard_transactions.json", 'w+') as f: json.dump(transactions_db, f, indent=4)
                localembed = discord.Embed(
                    title="Transaction successfully verified.",
                    description="Please wait patiently until the merchant has verified the transaction.",
                    color=discord.Color.green()
                )
                await ctx.respond(embed=localembed, ephemeral=True)
        except KeyError: return await ctx.respond("This transaction verification code is invalid.")

# Initialization
def setup(bot): bot.add_cog(IsoCard(bot))
