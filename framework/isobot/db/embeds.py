# Imports
import json
import discord
import datetime
import framework.types
from typing_extensions import Union
from framework.isobot.colors import Colors as colors

# Functions
class Embeds():
    """Initializes the Embed database system."""
    def __init__(self):
        print(f"[framework/db/Embeds] {colors.green}Embeds db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the embeds database."""
        with open("database/embeds.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open("database/embeds.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0
    
    def generate_server_key(self, server_id: Union[str, int]) -> int:
        """Creates a new data key for the specified server in the embeds database.\n\nReturns `0` if successful, returns `1` if the server already exists in the database."""
        embeds = self.load()
        if str(server_id) not in embeds.keys():
            embeds[str(server_id)] = {}
            self.save(embeds)
            return 0
        return 1
    
    def get_embeds_list(self, server_id: Union[str, int]) -> dict:
        """Fetches a `dict` of all the added embeds in the specified server.\n\nReturns an empty `dict` if none are set up."""
        embeds = self.load()
        return embeds[str(server_id)]

    def generate_embed(
            self,
            server_id: Union[str, int],
            embed_name: str,
            *,
            title: str = None,
            description: str = None,
            color: int = None,
            timestamp_enabled: bool = False,
            title_url: str = None,
            image_url: str = None,
            thumbnail: str = None

        ) -> int:
        """Generates an embed for the specified server using the given embed data.\n\nReturns `0` if successful, returns `1` if an embed with the same embed name already exists, returns `2` if the specified embed color is not a valid hex code."""
        embeds = self.load()
        
        self.generate_server_key(server_id)

        if embed_name not in embeds[str(server_id)].keys():
            # Check whether color code is a valid value or not
            if color not in [-1, 0] or not framework.types.is_hex_color_code(color):
                return 2
            
            embeds[str(server_id)][embed_name] = {
                "title": title,
                "description": description,
                "color": color,    # -1 = random color, None = no color, hex code = custom color
                "timestamp_enabled": timestamp_enabled,
                "title_url": title_url,
                "image_url": image_url,
                "thumbnail": thumbnail,
                "fields": [],
                "author": {},
                "footer": {}
            }
            self.save(embeds)
            return 0
        else: return 1

    def build_embed(self, server_id: Union[str, int], embed_name: str) -> discord.Embed:
        """Builds a Discord embed from the specified server's embed data, and returns it as `discord.Embed`.\n\nReturns `1` if the embeds does not exist."""
        embeds = self.load()
        if embed_name in embeds[str(server_id)].keys():
            embed_data = embeds[str(server_id)][embed_name]
            
            if embed_data["title"] == None: title = discord.Embed.Empty
            if embed_data["description"] == None: description = discord.Embed.Empty
            if embed_data["color"] == None: color = discord.Embed.Empty
            if embed_data["title_url"] == None: title_url = discord.Embed.Empty
            if embed_data["image_url"] == None: image_url = discord.Embed.Empty
            if embed_data["thumbnail"] == None: thumbnail = discord.Embed.Empty

            embed = discord.Embed(
                title=title,
                description=description,
                color = discord.Color.random() if embed_data["color"] == -1 else embed_data["color"],
                url=title_url,
                timestamp = datetime.datetime.utcnow() if embed_data["timestamp_enabled"] else discord.Embed.Empty
            )
            embed.set_image(url=image_url)
            embed.set_thumbnail(url=thumbnail)

            for field in embed_data["fields"]:
                embed.add_field(
                    name=embed_data["fields"][field]["name"],
                    value=embed_data["fields"][field]["value"],
                    inline=embed_data["fields"][field]["inline"]
                )

            if embed_data["author"] != {}:
                if embed_data["author"]["url"] == None: author_url = discord.Embed.Empty
                if embed_data["author"]["icon_url"] == None: author_icon_url = discord.Embed.Empty
                embed.set_author(name=embed_data["author"]["name"], url=author_url, icon_url=author_icon_url)

            if embed_data["footer"] != {}:
                if embed_data["footer"]["icon_url"] == None: footer_icon_url = discord.Embed.Empty
                embed.set_footer(text=embed_data["footer"]["text"], icon_url=footer_icon_url)

            return embed  # Returning the embed data as output
        else: return 1

    def delete_embed(self, server_id: Union[str, int], embed_name: str) -> int:
        """Deletes an existing embed from the specified server's embeds list.\n\nReturns `0` if successful, returns `1` if the embed does not exist."""
        embeds = self.load()
        if embed_name in embeds[str(server_id)].keys():
            del embeds[str(server_id)][embed_name]
            self.save(embeds)
            return 0
        else: return 1
    
    def add_embed_field(
        self,
        server_id: Union[str, int],
        embed_name: str,
        name: str,
        value: str,
        inline: bool = False
        ) -> int:
        """Adds a new field to an already existing embed.\n\nReturns `0` if successful, returns `1` if the embed does not exist."""
        embeds = self.load()
        if embed_name in embeds[str(server_id)].keys():
            list(embeds[str(server_id)][embed_name]["fields"]).append(
                {
                    "name": name,
                    "value": value,
                    "inline": inline
                }
            )
            self.save(embeds)
            return 0
        else: return 1
    
    def add_embed_footer(
        self,
        server_id: Union[str, int],
        embed_name: str,
        text: str,
        icon_url: str = None
        ) -> int:
        """Adds a footer to an already existing embed.\n\nReturns `0` if successful, returns `1` if the embed does not exist."""
        embeds = self.load()
        if embed_name in embeds[str(server_id)].keys():
            embeds[str(server_id)][embed_name]["footer"] = {
                "text": text,
                "icon_url": icon_url
            }
            self.save(embeds)
            return 0
        else: return 1

    def add_embed_author(
        self,
        server_id: Union[str, int],
        embed_name: str,
        name: str,
        url: str = None,
        icon_url: str = None
        ):
        """Adds the author field to an already existing embed.\n\nReturns `0` if successful, returns `1` if the embed does not exist."""
        embeds = self.load()
        if embed_name in embeds[str(server_id)].keys():
            embeds[str(server_id)][embed_name]["author"] = {
                "name": name,
                "url": url,
                "icon_url": icon_url
            }
            self.save(embeds)
            return 0
        else: return 1
