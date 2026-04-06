"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain
entities and exposes analytical query methods (Q1-Q10).

Classes implemented:
  - StreamingPlatform
"""

from collections import defaultdict
from datetime import datetime, timedelta

class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._tracks: dict = {}
        self._users: dict = {}
        self._artists: dict = {}
        self._albums: dict = {}
        self._playlists: list = []
        self._sessions: list = []       

# Registration methods
    def add_track(self, track) -> None:
        self._tracks[track.track_id] = track

    def add_user(self, user) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist) -> None:
        self._playlists.append(playlist)

    def record_session(self, session: "ListeningSession") -> None:
        self._sessions.append(session)
        session.user.add_session(session)

# Accessors
    def get_track(self, track_id: str):
        return self._tracks.get(track_id)

    def get_user(self, user_id: str):
        return self._users.get(user_id)

    def get_artist(self, artist_id: str):
        return self._artists.get(artist_id)

    def get_album(self, album_id: str):
        return self._albums.get(album_id)

    def all_users(self) -> list:
        return list(self._users.values())

    def all_tracks(self) -> list:
        return list(self._tracks.values())

# Q1 
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0
        for s in self._sessions:
            if start <= s.timestamp <= end:
                total_seconds += s.duration_listened_seconds
        return float(total_seconds / 60.0)

# Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        from streaming.users import PremiumUser

        cutoff = datetime.now() - timedelta(days=days)
        premium_users = []
        for u in self._users.values():
            if isinstance(u, PremiumUser):
                premium_users.append(u)
        if not premium_users:
            return 0.0

        total_unique = 0
        for user in premium_users:
            unique_tracks: set[str] = set()
            for s in self._sessions:
                if s.user.user_id == user.user_id and s.timestamp >= cutoff:
                    unique_tracks.add(s.track.track_id)
            total_unique += len(unique_tracks)

        return float(total_unique / len(premium_users))

# Q3 
    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None

        listener_map: dict[str, set[str]] = defaultdict(set)
        for s in self._sessions:
            listener_map[s.track.track_id].add(s.user.user_id)
        
        def get_listener_count(tid):
            return len(listener_map[tid])
            
        best_track_id = max(listener_map, key=get_listener_count)
        return self._tracks.get(best_track_id)

# Q4 
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        type_durations: dict[str, list[float]] = defaultdict(list)
        for s in self._sessions:
            type_name = type(s.user).__name__
            type_durations[type_name].append(s.duration_listened_seconds)

        result = []
        for type_name, durations in type_durations.items():
            average_duration = float(sum(durations) / len(durations))
            result.append((type_name, average_duration))
        
        def get_avg_duration(item):
            return item[1]
            
        return sorted(result, key=get_avg_duration, reverse=True)

# Q5 
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        from streaming.users import FamilyMember

        total_seconds = 0
        for s in self._sessions:
            if isinstance(s.user, FamilyMember) and s.user.age < age_threshold:
                total_seconds += s.duration_listened_seconds
        return float(total_seconds / 60.0)

# Q6 
    def top_artists_by_listening_time(self, n: int = 5) -> list:
        from streaming.tracks import Song

        artist_seconds: dict[str, float] = defaultdict(float)
        for s in self._sessions:
            if isinstance(s.track, Song):
                artist_seconds[s.track.artist.artist_id] += s.duration_listened_seconds

        result = []
        for artist_id, total_secs in artist_seconds.items():
            artist = self._artists.get(artist_id)
            if artist is not None:
                result.append((artist, float(total_secs / 60.0)))

        def get_listening_time(item):
            return item[1]
        result.sort(key=get_listening_time, reverse=True)
        return result[:n]

# Q7 
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        if user_id not in self._users:
            return None

        genre_seconds: dict[str, float] = defaultdict(float)
        for s in self._sessions:
            if s.user.user_id == user_id:
                genre_seconds[s.track.genre] += s.duration_listened_seconds
        if not genre_seconds:
            return None
        total = sum(genre_seconds.values())
        
        def get_seconds(g):
            return genre_seconds[g]
            
        top_genre = max(genre_seconds, key=get_seconds)
        percentage = (genre_seconds[top_genre] / total) * 100.0
        return (top_genre, float(percentage))

