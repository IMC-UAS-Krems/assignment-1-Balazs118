"""
playlists.py
------------
Implement playlist classes for organising tracks.

Classes implemented:
  - Playlist                 – user-curated ordered collection of tracks
    - CollaborativePlaylist  – playlist with multiple contributors
"""


class Playlist:
    """An ordered, user-curated collection of tracks."""

    def __init__(self, playlist_id: str, name: str, owner=None):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self._tracks: list = []

    def add_track(self, track) -> None:
        if track not in self._tracks:
            self._tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        kept_tracks = []
        for track in self._tracks:
            if track.track_id != track_id:
                kept_tracks.append(track)
        self._tracks = kept_tracks

    def total_duration_seconds(self) -> int:
        total_seconds = 0
        for track in self._tracks:
            total_seconds += track.duration_seconds
        return total_seconds

    @property
    def tracks(self) -> list:
        return list(self._tracks)


class CollaborativePlaylist(Playlist):
    """A playlist that multiple users can contribute tracks to."""

    def __init__(self, playlist_id: str, name: str, owner=None):
        super().__init__(playlist_id, name, owner)
        self._contributors: list = []
        if owner:
            self.add_contributor(owner)

    def add_contributor(self, user) -> None:
        if user not in self._contributors:
            self._contributors.append(user)

    def remove_contributor(self, user) -> None:
        if user != self.owner:
            if user in self._contributors:
                self._contributors.remove(user)

    @property
    def contributors(self) -> list:
        return list(self._contributors)
