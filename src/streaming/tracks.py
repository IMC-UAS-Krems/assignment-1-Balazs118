"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes implemented:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""



class Track:
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id


class Song(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist,):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist


class SingleRelease(Song):
    def __init__(self, track_id: str,title: str, duration_seconds: int, genre: str, artist, release_date=None, release_year: int = None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date
        self.release_year = release_year


class AlbumTrack(Song):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist, track_number: int = 1):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None


class Podcast(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str = "", description: str = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class InterviewEpisode(Podcast):
    def __init__( self, track_id: str, title: str, duration_seconds: int, genre: str, host: str = "", description: str = "",guest: str = ""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class NarrativeEpisode(Podcast):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str = "", description: str = "", season: int = 1, episode_number: int = 1):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number


class AudiobookTrack(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str = "", narrator: str = "", chapter_number: int = 1):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator
        self.chapter_number = chapter_number
