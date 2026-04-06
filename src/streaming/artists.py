"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes implemented:
  - Artist
"""


class Artist:
    def __init__(self, artist_id: str, name: str, genre: str = ""):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self._tracks: list = []
    def add_track(self, track) -> None:
        if track not in self._tracks:
            self._tracks.append(track)

    def track_count(self) -> int:
        return len(self._tracks)

    @property
    def tracks(self) -> list:
        return list(self._tracks)
