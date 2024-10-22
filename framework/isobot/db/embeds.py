# Imports
import json
import discord
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
        """Generates an embed for the specified server using the given embed data.\n\nReturns `0` if successful, returns `1` if an embed with the same embed name already exists."""
        embeds = self.load()

        if embed_name not in embeds[str(server_id)].keys():
            embeds[str(server_id)][embed_name] = {
                "title": title,
                "description": description,
                # "color":    # TODO: Fina a way to implement colors into the embeds
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
