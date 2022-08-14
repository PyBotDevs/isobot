"""The library used for designing and outputting Discord embeds."""
import discord
from discord import Color


def embed(title: str, desc: str, *, image: str = None, thumbnail: str = None, color:int=None, footer_text: str = None, footer_img: str = None):
    """Designs a Discord embed.
    -----------------------------------------------------------
    The color argument is completely optional.
    - If a color is set, it will return the embed in that color only.
    - If the color is set as "rand", then it will return the embed with a random color.
    - If a color is not set, it will appear as Discord's blurple embed color.
    """
    if color == -1: color = Color.random()
    elif color == None: color = Color.blurple()
    local_embed = discord.Embed(
        title=title,
        description=desc,
        colour=color
    )
    if image is not None: local_embed.set_image(url=image)
    if thumbnail is not None: local_embed.set_thumbnail(url=thumbnail)
    if footer_text is not None and footer_img is not None: local_embed.set_footer(text=footer_text, icon_url=footer_img)
    elif footer_text is not None: local_embed.set_footer(text=footer_text)
    elif footer_img is not None: local_embed.set_footer(icon_url=footer_img)
    return local_embed
