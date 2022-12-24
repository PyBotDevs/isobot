# Imports
import discord
import praw
from discord import ApplicationContext, option
from discord.ext import commands
from random import randint

# Variables
color = discord.Color.random()
reddit = praw.Reddit(client_id='_pazwWZHi9JldA', client_secret='1tq1HM7UMEGIro6LlwtlmQYJ1jB4vQ', user_agent='idk', check_for_async=False)

# Commands
class RedditMedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name='memes',
        description='Finely hand-picks a high-quality meme from the depths of reddit.'
    )
    async def memes(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name='linuxmemes',
        description='Hands you a fabolous GNU/Linux meme from the r/linuxmemes subreddit.'
    )
    async def linuxmemes(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('linuxmemes').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name='ihadastroke',
        description='I bet you\'ll have a stroke trying to see these. (JK ITS ABSOLUTELY SAFE FOR YOU DONT WORRY)'
    )
    async def ihadastroke(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('ihadastroke').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name='engrish',
        description='Features phuck ups in english of any kind!'
    )
    async def engrish(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('engrish').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name='softwaregore',
        description='Features glitchy, nasty, funny software bugs!'
    )
    async def softwaregore(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('softwaregore').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name='osugame',
        description='Features a post from the official osu! subreddit!'
    )
    async def osugame(self, ctx: ApplicationContext):
        memes_submissions = reddit.subreddit('osugame').hot()
        post_to_pick = randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title, color=color)
        embed.set_image(url=submission.url)
        embed.set_footer(text='Powered by PRAW')
        await ctx.respond(embed = embed)


# Cog Initialization
def setup(bot): bot.add_cog(RedditMedia(bot))
