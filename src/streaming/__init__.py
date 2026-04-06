"""
streaming
---------
Music streaming platform domain model.

Exposes all public classes for convenient import:

    from streaming import StreamingPlatform, Artist, Album, ...
"""

from streaming.tracks import (Track, Song, SingleRelease, AlbumTrack, Podcast, InterviewEpisode, NarrativeEpisode, AudiobookTrack,)
from streaming.artists import Artist
from streaming.albums import Album
from streaming.users import User, FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist
from streaming.platform import StreamingPlatform

__all__ = ["Track", "Song", "SingleRelease", "AlbumTrack", "Podcast", "InterviewEpisode", "NarrativeEpisode","AudiobookTrack", "Artist", "Album", "User","FreeUser","PremiumUser", "FamilyAccountUser", "FamilyMember", "ListeningSession", "Playlist", "CollaborativePlaylist","StreamingPlatform",]
