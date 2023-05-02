from osrparse import GameMode as OsrparseGameMode

from ossapi.models import GameMode, User, Beatmap
from ossapi.mod import Mod
from ossapi.enums import UserLookupKey

game_mode_map = {
    OsrparseGameMode.STD:   GameMode.STD,
    OsrparseGameMode.TAIKO: GameMode.TAIKO,
    OsrparseGameMode.CTB:   GameMode.CTB,
    OsrparseGameMode.MANIA: GameMode.MANIA,
}

class Replay:
    """
    A replay played by a player.

    Notes
    -----
    This is a thin shim around an osrparse.Replay instance. It converts some
    attributes to more appropriate types and adds #user and #beatmap to retrieve
    api-related objects.
    """
    def __init__(self, replay, api):
        self._api = api
        self.mode = game_mode_map[replay.mode]
        self.game_version = replay.game_version
        self.beatmap_hash = replay.beatmap_hash
        self.username = replay.username
        self.replay_hash = replay.replay_hash
        self.count_300 = replay.count_300
        self.count_100 = replay.count_100
        self.count_50 = replay.count_50
        self.count_geki = replay.count_geki
        self.count_katu = replay.count_katu
        self.count_miss = replay.count_miss
        self.score = replay.score
        self.max_combo = replay.max_combo
        self.perfect = replay.perfect
        self.mods = Mod(replay.mods.value)
        self.life_bar_graph = replay.life_bar_graph
        self.timestamp = replay.timestamp
        self.replay_data = replay.replay_data
        self.replay_id = replay.replay_id
        self._beatmap = None
        self._user = None

    @property
    def beatmap(self) -> Beatmap:
        """
        The beatmap this replay was played on.

        Warnings
        --------
        Accessing this property for the first time will result in a web request
        to retrieve the beatmap from the api. We cache the return value, so
        further accesses are free.
        """
        if self._beatmap:
            return self._beatmap
        self._beatmap = self._api.beatmap(checksum=self.beatmap_hash)
        return self._beatmap

    @property
    def user(self) -> User:
        """
        The user that played this replay.

        Warnings
        --------
        Accessing this property for the first time will result in a web request
        to retrieve the user from the api. We cache the return value, so further
        accesses are free.
        """
        if self._user:
            return self._user
        self._user = self._api.user(self.username, key=UserLookupKey.USERNAME)
        return self._user
