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
        result_ids = set()
        for track in self._tracks:
            result_ids.add(track.track_id) 
        return result_ids

    def duration_seconds(self) -> int:
        total_duration = 0
        for track in self._tracks:
            total_duration += track.duration_seconds
        return total_duration

    @property
    def tracks(self) -> list:
        def get_track_number(track):
            return track.track_number
        try:
            return sorted(self._tracks, key=get_track_number)
        except AttributeError:
            return list(self._tracks)
