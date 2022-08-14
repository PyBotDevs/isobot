"""The library used for designing and outputting Discord embeds."""
import discord
from discord import Color


def embed(title: str, desc: str, *, image: str = None, thumbnail: str = None, color:int=None, footer: dict = None):
    """Designs a Discord embed.
    -----------------------------------------------------------
    The color argument is completely optional.
    - If a color is set, it will return the embed in that color only.
    - If the color is set as "rand", then it will return the embed with a random color.
    - If a color is not set, it will appear as Discord's blurple embed color.

    Footer must be in a json format ONLY, otherwise it cannot be parsed.
    - Correct format: {"text": "something", "img" "an image url"}
    """
    if color == "rand":
        color = Color.random()
    elif color == None:
        color = Color.blurple()
    local_embed = discord.Embed(
        title=title,
        description=desc,
        colour=color
    )
    if image is not None:
        local_embed.set_image(url=image)
    if thumbnail is not None:
        local_embed.set_thumbnail(url=thumbnail)
    if footer is not None:
        try:
            local_embed.set_footer(text=footer["text"], icon_url=footer["img"])
        except KeyError:
            return "Unable to create embed: Failed to parse \"footer\" argument. Expected format: {\"text\": \"something\", \"img\" \"an image url\"}"
    return local_embed
