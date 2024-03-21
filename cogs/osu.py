"""The isobot cog file for osu! commands."""

# Imports
import discord
import os
from api import auth
from ossapi import *
from discord import option, ApplicationContext
from discord.ext import commands

# Commands
class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = OssapiV2(13110, os.environ['ossapi_CLIENT_SECRET'])
    
    @commands.slash_command(
        name="osu_user",
        description="View information on an osu! player."
    )
    @option(name="user", description="The name of the user", type=str)
    async def osu_user(self, ctx, *, user:str):
        try:
            compact_user = self.api.search(query=user).users.data[0]
            e = discord.Embed(title=f'osu! stats for {user}', color=0xff66aa)
            e.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Osu%21_Logo_2016.svg/2048px-Osu%21_Logo_2016.svg.png')
            e.add_field(name='Rank (Global)', value=f'#{compact_user.expand().statistics.global_rank}')
            e.add_field(name='Rank (Country)', value=f'#{compact_user.expand().statistics.country_rank}')
            e.add_field(name='Ranked Score', value=f'{compact_user.expand().statistics.ranked_score}')
            e.add_field(name='Level', value=f'Level {compact_user.expand().statistics.level.current} ({compact_user.expand().statistics.level.progress}% progress)')
            e.add_field(name='pp', value=round(compact_user.expand().statistics.pp))
            e.add_field(name='Max Combo', value=f'{compact_user.expand().statistics.maximum_combo}x')
            e.add_field(name='Total Hits', value=f'{compact_user.expand().statistics.total_hits}')
            e.add_field(name='Play Count', value=compact_user.expand().statistics.play_count)
            e.add_field(name='Accuracy', value=f'{round(compact_user.expand().statistics.hit_accuracy, 2)}%')
            e.add_field(name='Replays Watched by Others', value=f'{compact_user.expand().statistics.replays_watched_by_others}')
            await ctx.respond(embed=e)
        except: await ctx.respond(f':warning: {user} was not found in osu!.', ephemeral=True)

    @commands.slash_command(
        name="osu_beatmap",
        description="View information on an osu! beatmap."
    )
    @option(name="query", description="The beatmap's id", type=int)
    async def osu_beatmap(self, ctx, *, query:int):
        beatmap = self.api.beatmap(beatmap_id=query)
        e = discord.Embed(title=f'osu! beatmap info for {beatmap.expand()._beatmapset.title} ({beatmap.expand()._beatmapset.title_unicode})', color=0xff66aa)
        e.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Osu%21_Logo_2016.svg/2048px-Osu%21_Logo_2016.svg.png')
        #.beatmap.data[0]
        e.add_field(name='Artist', value=f'{beatmap.expand()._beatmapset.artist} ({beatmap.expand()._beatmapset.artist_unicode})')
        e.add_field(name='Mapper', value=beatmap.expand()._beatmapset.creator)
        e.add_field(name='Difficulty', value=f'{beatmap.expand().difficulty_rating} stars')
        e.add_field(name='BPM', value=beatmap.expand().bpm)
        e.add_field(name='Circles', value=beatmap.expand().count_circles)
        e.add_field(name='Sliders', value=beatmap.expand().count_sliders)
        e.add_field(name='HP Drain', value=beatmap.expand().drain)
        await ctx.respond(embed=e)

# Cog Initialization
def setup(bot): bot.add_cog(Osu(bot))
