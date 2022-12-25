# Imports
import discord
import json
import os
from discord import option, ApplicationContext
from discord.ext import commands

# Variables
wdir = os.getcwd()
color = discord.Color.random()

with open(f'{wdir}/database/automod.json', 'r') as f: automod_config = json.load(f)

def save():
    with open(f'{wdir}/database/automod.json', 'w+') as f: json.dump(automod_config, f, indent=4)

# Commands
class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="automod",
        description="Shows the current automod configuration for your server"
    )
    async def automod(ctx: ApplicationContext):
        loaded_config = automod_config[str(ctx.guild.id)]
        localembed = discord.Embed(title=f"{ctx.guild.name}\'s automod configuration", descripton="Use the `/automod_set` command to change your server's automod configuration.", color=color)
        localembed.set_thumbnail(url=ctx.guild.icon_url)
        localembed.add_field(name="Swear-filter", value=loaded_config["swear_filter"]["enabled"])
        localembed.add_field(name="Swear-filter Keywords Count", value=f"{int(len(loaded_config['swear_filter']['keywords']['default'])) + int(len(loaded_config['swear_filter']['keywords']['custom']))} words")
        localembed.set_footer(text="More automod features will come soon!")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="automod_swearfilter",
        description="Turn on or off automod's swear-filter in your server"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_swearfilter(ctx: ApplicationContext, toggle:bool):
        loaded_config = automod_config[str(ctx.guild.id)]
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if loaded_config["swear_filter"]["enabled"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        loaded_config["swear_filter"]["enabled"] = toggle
        if toggle == True: await ctx.respond("Swear-filter successfully **enabled**.", ephemeral=True)
        elif toggle == False: await ctx.respond("Swear-filter successfully **disabled**.", ephemeral=True)
        save()

    @commands.slash_command(
        name="automod_use_default_keywords",
        description="Choose whether or not you want to use the default keywords for automod's swear-filter"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_use_default_keywords(ctx: ApplicationContext, toggle:bool):
        loaded_config = automod_config[str(ctx.guild.id)]
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if loaded_config["swear_filter"]["keywords"]["use_default"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        loaded_config["swear_filter"]["keywords"]["use_default"] = toggle
        if toggle == True: await ctx.respond("Using default swear-filter keywords successfully **enabled**.", ephemeral=True)
        elif toggle == False: await ctx.respond("Using default swear-filter keywords successfully **disabled**.", ephemeral=True)
        save()

    @commands.slash_command(
        name="automod_view_custom_keywords",
        description="Shows a list of the custom automod swear-filter keywords set for your server",
    )
    async def automod_view_custom_keywords(ctx: ApplicationContext):
        loaded_config = automod_config[str(ctx.guild.id)]
        out = ""
        if loaded_config["swear_filter"]["keywords"]["custom"] != []:
            i = 0
            for x in loaded_config["swear_filter"]["keywords"]["custom"]:
                i += 1
                out += f"**{i})** {x}\n"
        else: out = "*No custom keywords are set for your server.*"
        localembed = discord.Embed(title=f"Custom Swear-filter keywords for {ctx.guild.name}", description=out, color=color)
        localembed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.respond(embed=localembed)

    @commands.slash_command(
        name="automod_add_custom_keyword",
        description="Adds a custom keyword to your server's swear-filter"
    )
    @option(name="keyword", description="What keyword do you want to add?", type=str)
    async def automod_add_custom_keyword(ctx: ApplicationContext, keyword:str):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        loaded_config = automod_config[str(ctx.guild.id)]
        if keyword not in loaded_config["swear_filter"]["keywords"]["custom"]:
            loaded_config["swear_filter"]["keywords"]["custom"].append(keyword)
            save()
            localembed = discord.Embed(description=f"New swear-filter keyword `{keyword}` successfully added to configuration.", color=discord.Color.green())
            await ctx.respond(embed=localembed, ephemeral=True)
        else: return await ctx.respond("That keyword is already added in your automod configuration.", ephemeral=True)

    @commands.slash_command(
        name="automod_remove_custom_keyword",
        description="Removes a custom keyword (matching its id) from your server's swear-filter"
    )
    @option(name="id", description="What's the id of the keyword to remove (can be found in bold through /automod_view_custom_keywords", type=int)
    async def automod_remove_custom_keyword(ctx: ApplicationContext, id:int):
        loaded_config = automod_config[str(ctx.guild.id)]
        try:
            data = loaded_config["swear_filter"]["keywords"]["custom"]
            data.pop(id-1)
            save()
            return await ctx.respond(f"Keyword (id: `{id}`) successfully removed from swear-filter configuration.")
        except IndexError: await ctx.respond("That keyword id doesn't exist. Please specify a valid id and try again.", ephemeral=True)

def setup(bot):
    bot.add_cog(Automod(bot))
