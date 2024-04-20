"""The isobot cog file for the automod system."""

# Imports
import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from framework.isobot.db import automod

# Variables
color = discord.Color.random()
automod = automod.Automod()

# Commands
class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    automod_cmds = SlashCommandGroup(name="automod", description="Commands related to the server's automod setup and configuration.")

    @automod_cmds.command(
        name="config",
        description="Shows the current automod configuration for your server"
    )
    async def automod_config(self, ctx: ApplicationContext):
        loaded_config = automod.fetch_config(ctx.guild.id)
        localembed = discord.Embed(title=f"{ctx.guild.name}\'s automod configuration", description="Use the `/automod_set` command to change your server's automod configuration.", color=color)
        localembed.set_thumbnail(url=ctx.guild.icon)
        localembed.add_field(name="Swear-filter", value=loaded_config["swear_filter"]["enabled"])
        localembed.add_field(name="Swear-filter Keywords Count", value=f"{int(len(loaded_config['swear_filter']['keywords']['default'])) + int(len(loaded_config['swear_filter']['keywords']['custom']))} words")
        localembed.set_footer(text="More automod features will come soon!")
        await ctx.respond(embed=localembed)

    # Swear-filter Commands
    @automod_cmds.command(
        name="swearfilter",
        description="Turn on or off automod's swear-filter in your server"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_swearfilter(self, ctx: ApplicationContext, toggle: bool):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if automod.fetch_config(ctx.guild.id)["swear_filter"]["enabled"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        automod.swearfilter_enabled(ctx.guild.id, toggle)
        if toggle is True: await ctx.respond("Swear-filter successfully **enabled**.", ephemeral=True)
        elif toggle is False: await ctx.respond("Swear-filter successfully **disabled**.", ephemeral=True)

    @automod_cmds.command(
        name="use_default_keywords",
        description="Choose whether or not you want to use the default keywords for automod's swear-filter"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_use_default_keywords(self, ctx: ApplicationContext, toggle: bool):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if automod.fetch_config(ctx.guild.id)["swear_filter"]["keywords"]["use_default"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        automod.swearfilter_usedefaultkeywords(ctx.guild.id, toggle)
        if toggle is True: await ctx.respond("Using default swear-filter keywords successfully **enabled**.", ephemeral=True)
        elif toggle is False: await ctx.respond("Using default swear-filter keywords successfully **disabled**.", ephemeral=True)

    @automod_cmds.command(
        name="view_custom_keywords",
        description="Shows a list of the custom automod swear-filter keywords set for your server",
    )
    async def automod_view_custom_keywords(self, ctx: ApplicationContext):
        loaded_config = automod.fetch_config(ctx.guild.id)
        out = ""
        if loaded_config["swear_filter"]["keywords"]["custom"] != []:
            i = 0
            for x in loaded_config["swear_filter"]["keywords"]["custom"]:
                i += 1
                out += f"{i}. {x}\n"
        else: out = "*No custom keywords are set for your server.*"
        localembed = discord.Embed(title=f"Custom Swear-filter keywords for {ctx.guild.name}", description=out, color=color)
        localembed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.respond(embed=localembed)

    @automod_cmds.command(
        name="add_custom_keyword",
        description="Adds a custom keyword to your server's swear-filter"
    )
    @option(name="keyword", description="What keyword do you want to add?", type=str)
    async def automod_add_custom_keyword(self, ctx: ApplicationContext, keyword:str):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        loaded_config = automod.fetch_config(ctx.guild.id)
        if keyword not in loaded_config["swear_filter"]["keywords"]["custom"]:
            automod.swearfilter_addkeyword(ctx.guild.id, keyword)
            localembed = discord.Embed(description=f"New swear-filter keyword `{keyword}` successfully added to configuration.", color=discord.Color.green())
            await ctx.respond(embed=localembed, ephemeral=True)
        else: return await ctx.respond("That keyword is already added in your automod configuration.", ephemeral=True)

    @automod_cmds.command(
        name="remove_custom_keyword",
        description="Removes a custom keyword (matching its id) from your server's swear-filter"
    )
    @option(name="id", description="What's the id of the keyword to remove (can be found through /automod_view_custom_keywords", type=int)
    async def automod_remove_custom_keyword(self, ctx: ApplicationContext, id: int):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        try:
            automod.swearfilter_removekeyword(ctx.guild.id, id)
            return await ctx.respond(f"Keyword (id: `{id}`) successfully removed from swear-filter configuration.")
        except IndexError: await ctx.respond("That keyword id doesn't exist. Please specify a valid id and try again.", ephemeral=True)

    # Link Blocker Commands
    @automod_cmds.command(
        name="linkblocker",
        description="Turn on or off automod's link blocker in your server"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_linkblocker(self, ctx: ApplicationContext, toggle: bool):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if automod.fetch_config(ctx.guild.id)["link_blocker"]["enabled"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        automod.linkblocker_enabled(ctx.guild.id, toggle)
        if toggle is True: await ctx.respond("Link blocker successfully **enabled**.", ephemeral=True)
        elif toggle is False: await ctx.respond("Link blocker successfully **disabled**.", ephemeral=True)
    
    @automod_cmds.command(
        name="linkblocker_only_whitelisted",
        description="Only allows whitelisted links in the server and blocks all other links"
    )
    @option(name="toggle", description="Do you want to turn it on or off?", type=bool)
    async def automod_linkblocker_only_whitelisted_links(self, ctx: ApplicationContext, toggle: bool):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if automod.fetch_config(ctx.guild.id)["link_blocker"]["use_whitelist_only"] == toggle: return await ctx.respond(f"That automod option is already set to `{toggle}`.", ephemeral=True)
        automod.linkblocker_enabled(ctx.guild.id, toggle)
        if toggle is True: await ctx.respond("Link blocker successfully **enabled**.", ephemeral=True)
        elif toggle is False: await ctx.respond("Link blocker successfully **disabled**.", ephemeral=True)
    
    @automod_cmds.command(
        name="linkblocker_add_whitelist",
        description="Adds a link to your server link blocker's whitelist."
    )
    @option(name="link", description="The link that you want to add (must be in form of https://{url})", type=str)
    async def automod_linkblocker_add_whitelist(self, ctx: ApplicationContext, link: str):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if link in automod.fetch_config(ctx.guild.id)["link_blocker"]["whitelist"]: return await ctx.respond("This link is already in your server's link blocker whitelist.", ephemeral=True)
        if "https://" in link or "http://" in link:
            automod.linkblocker_add_whitelisted(link)
            await ctx.respond(f"Link `{link}` has successfully been added to whitelist.", ephemeral=True)
        else: return await ctx.respond(":warning: The link you entered is not formatted correctly. All added links must contain `https://`.")
    
    @automod_cmds.command(
        name="linkblocker_add_blacklist",
        description="Adds a link to your server link blocker's blacklist."
    )
    @option(name="link", description="The link that you want to add (must be in form of https://{url})", type=str)
    async def automod_linkblocker_add_blacklist(self, ctx: ApplicationContext, link: str):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        if link in automod.fetch_config(ctx.guild.id)["link_blocker"]["blacklist"]: return await ctx.respond("This link is already in your server's link blocker blacklist.", ephemeral=True)
        if "https://" in link or "http://" in link:
            automod.linkblocker_add_blacklisted(link)
            await ctx.respond(f"Link `{link}` has successfully been added to blacklist.", ephemeral=True)
        else: return await ctx.respond(":warning: The link you entered is not formatted correctly. All added links must contain `https://`.")
    
    @automod_cmds.command(
        name="linkblocker_view_whitelisted",
        description="Shows a list of the whitelisted links set for this server",
    )
    async def automod_view_custom_keywords(self, ctx: ApplicationContext):
        loaded_config = automod.fetch_config(ctx.guild.id)
        out = ""
        if loaded_config["link_blocker"]["whitelisted"] != []:
            i = 0
            for x in loaded_config["link_blocker"]["whitelisted"]:
                i += 1
                out += f"{i}. {x}\n"
        else: out = "*No whitelisted links are set for your server.*"
        localembed = discord.Embed(title=f"Whitelisted links for {ctx.guild.name}", description=out, color=color)
        localembed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.respond(embed=localembed)
    
    @automod_cmds.command(
        name="linkblocker_view_blacklisted",
        description="Shows a list of the blacklisted links set for this server",
    )
    async def automod_view_custom_keywords(self, ctx: ApplicationContext):
        loaded_config = automod.fetch_config(ctx.guild.id)
        out = ""
        if loaded_config["link_blocker"]["blacklisted"] != []:
            i = 0
            for x in loaded_config["link_blocker"]["blacklisted"]:
                i += 1
                out += f"{i}. {x}\n"
        else: out = "*No blacklisted links are set for your server.*"
        localembed = discord.Embed(title=f"Blacklisted links for {ctx.guild.name}", description=out, color=color)
        localembed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.respond(embed=localembed)
    
    @automod_cmds.command(
        name="linkblocker_remove_blacklist",
        description="Removes a blacklisted link (matching its id) from this server's link blocker"
    )
    @option(name="id", description="What's the id of the link to remove? (can be found through /automod_view_blacklisted_links", type=int)
    async def automod_linkblocker_remove_blacklist(self, ctx: ApplicationContext, id: int):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        try:
            automod.linkblocker_remove_blacklisted(ctx.guild.id, id)
            return await ctx.respond(f"Blacklisted link (id: `{id}`) successfully removed from link blocker.")
        except IndexError: await ctx.respond("That blacklisted link id doesn't exist. Please specify a valid id and try again.", ephemeral=True)
    
    @automod_cmds.command(
        name="linkblocker_remove_whitelist",
        description="Removes a whitelisted link (matching its id) from this server's link blocker"
    )
    @option(name="id", description="What's the id of the link to remove? (can be found through /automod_view_whitelisted_links", type=int)
    async def automod_linkblocker_remove_whitelist(self, ctx: ApplicationContext, id: int):
        if not ctx.author.guild_permissions.administrator: return await ctx.respond("You cannot use this command. If you think this is a mistake, please contact your server owner/administrator.", ephemeral=True)
        try:
            automod.linkblocker_remove_whitelisted(ctx.guild.id, id)
            return await ctx.respond(f"Whitelisted link (id: `{id}`) successfully removed from link blocker.")
        except IndexError: await ctx.respond("That whitelisted link id doesn't exist. Please specify a valid id and try again.", ephemeral=True)

def setup(bot):
    bot.add_cog(Automod(bot))
