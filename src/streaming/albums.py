"""
albums.py
---------
Implement the Album class for ordered collections of AlbumTrack objects.

Classes implemented:
  - Album
"""


class Album:
    def __init__(self, album_id: str, title: str, artist=None, release_year: int = None,):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self._tracks: list = []

    def add_track(self, track) -> None:
        self._tracks.append(track)
        track.album = self

    def track_ids(self) -> set[str]:
        return {t.track_id for t in self._tracks}

    def duration_seconds(self) -> int:
        return sum(t.duration_seconds for t in self._tracks)

    @property
    def tracks(self) -> list:
        def get_track_number(t):
            return t.track_number
        try:
            return sorted(self._tracks, key=get_track_number)
        except AttributeError:
            return list(self._tracks)
