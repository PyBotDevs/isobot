# Imports
import discord
import random
import json
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from framework.isobot.db import serverconfig

# Variables
serverconf = serverconfig.ServerConfig()

# Functions
class ServerConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Load Verification Database
        with open("database/serververification.json", 'r', encoding="utf-8") as f:
            self.verification_db: dict = json.load(f)
    
    serverconfig_cmds = SlashCommandGroup(name="serverconfig", description="Commands related to server customization and configuration.")

    @serverconfig_cmds.command(
        name="autorole",
        description="Set a role to provide to all newly-joined members of the server."
    )
    @commands.guild_only()
    @option(name="role", description="The role that you want to automatically give to all new members.", type=discord.Role, default=None)
    async def autorole(self, ctx: ApplicationContext, role: discord.Role = None):
        """Set a role to provide to all newly-joined members of the server."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        if role != None:
            serverconf.set_autorole(ctx.guild.id, role.id)
            localembed = discord.Embed(
                title=f":white_check_mark: Autorole successfully set for **{ctx.guild.name}**!",
                description=f"From now onwards, all new members will receive the {role.mention} role.",
                color=discord.Color.green()
            )
        else:
            serverconf.set_autorole(ctx.guild.id, None)
            localembed = discord.Embed(
                title=f":white_check_mark: Autorole successfully disabled for **{ctx.guild.name}**",
                description="New members will not automatically receive any roles anymore.",
                color=discord.Color.green()
            )
        await ctx.respond(embed=localembed)
    
    @serverconfig_cmds.command(
        name="levelup_override_channel",
        description="Set a server channel to send level-up messages to, instead of DMs."
    )
    @commands.guild_only()
    @option(name="channel", description="The channel in which you want level-up messages to be sent.", type=discord.TextChannel, default=None)
    async def autorole(self, ctx: ApplicationContext, channel: discord.TextChannel = None):
        """Set a role to provide to all newly-joined members of the server."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        if channel != None:
            serverconf.set_levelup_override_channel(ctx.guild.id, channel.id)
            localembed = discord.Embed(
                title=f":white_check_mark: Level-up Override Channel successfully set for **{ctx.guild.name}**!",
                description=f"From now onwards, all new level-up messages for members in this server will be sent to {channel.mention}, instead of user DMs.",
                color=discord.Color.green()
            )
        else:
            serverconf.set_levelup_override_channel(ctx.guild.id, None)
            localembed = discord.Embed(
                title=f":white_check_mark: Level-up Override Channel successfully disabled for **{ctx.guild.name}**",
                description="All new level-up messages will be sent to user DMs.",
                color=discord.Color.green()
            )
        await ctx.respond(embed=localembed)

    @serverconfig_cmds.command(
        name="enable_welcome_message",
        description="Automatically send a welcome message to a specified channel in the server, when a member joins."
    )
    @option(name="channel", description="The channel in which you want to send the welcome message.", type=discord.TextChannel)
    @option(name="message", description="Formatting: [user.nickname], [user.username], [user.mention], [server.name], [server.membercount]", type=str)
    async def enable_welcome_message(self, ctx: ApplicationContext, channel: discord.TextChannel, message: str):
        """Automatically send a welcome message to a specified channel in the server, when a member joins."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        serverconf.set_welcome_message(ctx.guild.id, channel.id, message)

        # Test Welcome Message
        welcome_message = serverconf.fetch_welcome_message(ctx.guild.id)
        if welcome_message["message"] is not None:
            welcome_message_autoresponder_channel = discord.Guild.get_channel(ctx.guild, welcome_message["channel"])

            # Perform attribute formatting for welcome message
            welcome_message_formatted = welcome_message["message"]
            welcome_message_formatted = welcome_message_formatted.replace("[user.nickname]", str(ctx.author.display_name))
            welcome_message_formatted = welcome_message_formatted.replace("[user.username]", str(ctx.author.name))
            welcome_message_formatted = welcome_message_formatted.replace("[user.mention]", str(ctx.author.mention))
            welcome_message_formatted = welcome_message_formatted.replace("[server.name]", str(ctx.guild.name))
            welcome_message_formatted = welcome_message_formatted.replace("[server.membercount]", str(ctx.guild.member_count))
            await welcome_message_autoresponder_channel.send(welcome_message_formatted)
        
        localembed = discord.Embed(
            title=f":white_check_mark: Server Welcome Message Autoresponder has been successfully set for **{ctx.guild.name}**!",
            description=f"From now onwards, all new members who join this server will be sent a welcome message in {channel.mention}\n\nA test message has been sent to the channel for reference.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)
    
    @serverconfig_cmds.command(
        name="disable_welcome_message",
        description="Disables welcome message autoresponder for this server."
    )
    async def disable_welcome_message(self, ctx: ApplicationContext):
        """Disables welcome message autoresponder for this server."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        serverconf.set_welcome_message(ctx.guild.id, None, None)
        localembed = discord.Embed(
            title=f":white_check_mark: Server Welcome Message Autoresponder successfully disabled for **{ctx.guild.name}**.",
            description="From now onwards, no new welcome messages will be sent in the server for newly-joined members.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)

    @serverconfig_cmds.command(
        name="enable_goodbye_message",
        description="Automatically send a goodbye message to a specified channel in the server, when a member leaves."
    )
    @option(name="channel", description="The channel in which you want to send the goodbye message.", type=discord.TextChannel)
    @option(name="message", description="Formatting: [user.nickname], [user.username], [user.mention], [server.name], [server.membercount]", type=str)
    async def enable_goodbye_message(self, ctx: ApplicationContext, channel: discord.TextChannel, message: str):
        """Automatically send a goodbye message to a specified channel in the server, when a member leaves."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        serverconf.set_goodbye_message(ctx.guild.id, channel.id, message)

        # Test Goodbye Message
        goodbye_message = serverconf.fetch_goodbye_message(ctx.guild.id)
        if goodbye_message["message"] is not None:
            goodbye_message_autoresponder_channel = discord.Guild.get_channel(ctx.guild, goodbye_message["channel"])

            # Perform attribute formatting for goodbye message
            goodbye_message_formatted = goodbye_message["message"]
            goodbye_message_formatted = goodbye_message_formatted.replace("[user.nickname]", str(ctx.author.display_name))
            goodbye_message_formatted = goodbye_message_formatted.replace("[user.username]", str(ctx.author.name))
            goodbye_message_formatted = goodbye_message_formatted.replace("[user.mention]", str(ctx.author.mention))
            goodbye_message_formatted = goodbye_message_formatted.replace("[server.name]", str(ctx.guild.name))
            goodbye_message_formatted = goodbye_message_formatted.replace("[server.membercount]", str(ctx.guild.member_count))
            await goodbye_message_autoresponder_channel.send(goodbye_message_formatted)
        
        localembed = discord.Embed(
            title=f":white_check_mark: Server Goodbye Message Autoresponder has been successfully set for **{ctx.guild.name}**!",
            description=f"From now onwards, a goodbye message will be sent in {channel.mention} for all members who leave this server.\n\nA test message has been sent to the channel for reference.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)
    
    @serverconfig_cmds.command(
        name="disable_goodbye_message",
        description="Disables goodbye message autoresponder for this server."
    )
    async def disable_goodbye_message(self, ctx: ApplicationContext):
        """Disables goodbye message autoresponder for this server."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.respond("You can't use this command! You need the `Manage Server` permission to run this.", ephemeral=True)
        serverconf.set_goodbye_message(ctx.guild.id, None, None)
        localembed = discord.Embed(
            title=f":white_check_mark: Server Goodbye Message Autoresponder successfully disabled for **{ctx.guild.name}**.",
            description="From now onwards, no new goodbye messages will be sent in the server for members who leave.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)

    # Server Member Verification System
    @serverconfig_cmds.command(
        name="enable_verification",
        description="Enable new member verification for this server."
    )
    @commands.guild_only()
    @option(name="verified_role", description="The role to provide to all verified members.", type=discord.Role)
    async def enable_verification(self, ctx: ApplicationContext, verified_role: discord.Role):
        """Enable new user verification for this server."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("You can't use this command! You need the `Administrator` permission to run this.", ephemeral=True)
        serverconf.set_verification_role(ctx.guild.id, verified_role.id)
        localembed = discord.Embed(
            title=f":white_check_mark: Server Member Verification successfully enabled for **{ctx.guild.name}**!",
            description=f"From now onwards, all new members will have to verify with `/verify` command, and will receive the {verified_role.mention} once verified.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)
    
    @serverconfig_cmds.command(
        name="disable_verification",
        description="Disable new member verification for this server."
    )
    @commands.guild_only()
    async def disable_verification(self, ctx: ApplicationContext):
        """Disable new member verification for this server."""
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("You can't use this command! You need the `Administrator` permission to run this.", ephemeral=True)
        serverconf.set_verification_role(ctx.guild.id, None)
        localembed = discord.Embed(
            title=f":white_check_mark: Server Member Verification successfully disabled for **{ctx.guild.name}**",
            description=f"New members now won't have to verify in the server.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=localembed)
    
    @commands.slash_command(
        name="start_verification",
        description="Start your verification process in this server."
    )
    @commands.guild_only()
    async def start_verification(self, ctx: ApplicationContext):
        """Start your verification process in this server."""
        verification_role = serverconf.fetch_verification_role(ctx.guild.id)
        if verification_role is None:
            return await ctx.respond(":warning: Verification system is disabled for this server!", ephemeral=True)
        if ctx.author.get_role(verification_role) is not None:
            return await ctx.respond(":warning: You are already verified in this server!", ephemeral=True)

        # Construct verification data
        verify_code = random.randint(100000, 999999)
        if str(ctx.author.id) not in self.verification_db:
            self.verification_db[str(ctx.author.id)] = {}

        for code in self.verification_db[str(ctx.author.id)]:
            if self.verification_db[str(ctx.author.id)][str(code)]["guild_id"] == ctx.guild.id:
                return await ctx.respond("Your verification process is already ongoing in this server!", ephemeral=True)

        self.verification_db[str(ctx.author.id)][str(verify_code)] = {"guild_id": ctx.guild.id}
        with open("database/serververification.json", 'w+', encoding="utf-8") as f:
            json.dump(self.verification_db, f, indent=4)

        localembed = discord.Embed(
            title=f"Verification for {ctx.author.name} in {ctx.guild.name} has started",
            description=f"Your one-time verification code is `{verify_code}`. **DO NOT share this code with anyone!**\n\nGo to isobot's DMs, and run the `/verify` command entering your verification code.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=localembed, ephemeral=True)
    
    @commands.slash_command(
        name="verify",
        description="Enter your one-time verification code to verify membership in a server. (DM-ONLY)"
    )
    @commands.dm_only()
    @option(name="verification_code", description="Your one-time verification code. (6-digit number)", type=int)
    async def verify(self, ctx: ApplicationContext, verification_code: int):
        """Enter your one-time verification code to verify membership in a server."""
        if str(ctx.author.id) not in self.verification_db.keys():
            return await ctx.respond("You are not pending verification in any servers.", ephemeral=True)
        if str(verification_code) not in self.verification_db[str(ctx.author.id)].keys():
            return await ctx.respond(":x: This verification code is invalid. Please double-check and try a different code!", ephemeral=True)

        verification_role_id = serverconf.fetch_verification_role(self.verification_db[str(ctx.author.id)][str(verification_code)]["guild_id"])
        vcode_guild: discord.Guild = self.bot.get_guild(self.verification_db[str(ctx.author.id)][str(verification_code)]["guild_id"])
        verification_role = discord.Guild.get_role(vcode_guild, verification_role_id)
        server_context_user: discord.Member = vcode_guild.get_member(ctx.author.id)
        await server_context_user.add_roles(verification_role, reason="Member has been successfully verified in server.")

        del self.verification_db[str(ctx.author.id)][str(verification_code)]
        with open("database/serververification.json", 'w+', encoding="utf-8") as f:
            json.dump(self.verification_db, f, indent=4)

        return await ctx.respond(f"You have been successfully verified in **{vcode_guild.name}**!")
    
    # Autoresponder Configuration Commands
    #autoresponder_commands = SlashCommandGroup(name="autoresponder", description="Commands related to the management of server text-based autoresponders.")

    commands.slash_command(
        name="autoresponder_add",
        description="Add a new text-based autoresponder to your server."
    )
    @option(name="autoresponder_name", description="The name (id) of the autoresponder.", type=str)
    @option(name="text_trigger", description="The text on which the autoresponder is triggered.", type=str)
    @option(name="text_response", description="The response you want the bot to send, when triggered.", type=str)
    @option(name="trigger_condition", description="MATCH_MESSAGE: The message content must be the same as the trigger; WITHIN_MESSAGE: When trigger is found anywhere within the message", type=str, choices=["MATCH_MESSAGE", "WITHIN_MESSAGE"])
    @option(name="active_channel", description="In which channel do you want the autoresponder to be active?", type=discord.TextChannel, default=None)
    @option(name="match_case", description="Do you want the trigger to be case-sensitive?", type=bool, default=False)
    async def autoresponder_add(self, ctx: ApplicationContext, autoresponder_name: str, text_trigger: str, text_response: str, trigger_condition: str, active_channel: discord.TextChannel, match_case: bool):
        """Add a new text-based autoresponder to your server."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond("You can't use this command! You need the `Manage Messages` permission to run this.", ephemeral=True)
        serverconf.add_autoresponder(
            ctx.guild.id,
            autoresponder_name=autoresponder_name,
            autoresponder_trigger=text_trigger,
            autoresponder_text=text_response,
            autoresponder_trigger_condition=trigger_condition,
            channels=active_channel,
            match_case=match_case
        )
        localembed = discord.Embed(
            title=":white_check_mark: Autoresponder Successfully Created",
            description=f"Autoresponder Name: `{autoresponder_name}`\n\nYou may use the autoresponder name to reference this autoresponder, for editing or deleting.",
            color=discord.Color.green()
        )
        localembed.add_field(name="Text Trigger", value=text_trigger)
        localembed.add_field(name="Bot Response", value=text_response)
        localembed.add_field(name="Autoresponder Trigger Condition", value=trigger_condition)
        if active_channel == None:
            localembed.add_field(name="Active Channel", value="all channels")
        else:
            localembed.add_field(name="Active Channel", value=f"<#{active_channel.id}>")
        localembed.add_field(name="Match Case?", value=match_case)
        await ctx.respond(embed=localembed)

def setup(bot):
    bot.add_cog(ServerConfig(bot))
    