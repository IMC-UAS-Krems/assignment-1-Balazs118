"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    platform.add_artist(pixels)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)


    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice   = FreeUser("u1", "Alice",   age=30)
    bob     = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    charlie = FamilyAccountUser("u3", "Charlie", age=40)
    dave    = FamilyMember("u4", "Dave", age=15, parent=charlie)

    for user in (alice, bob, charlie, dave):
        platform.add_user(user)

    #playlists
    p1 = Playlist("pl1", "Alice's Mix", alice)
    p1.add_track(t1)
    platform.add_playlist(p1)

    cp1 = CollaborativePlaylist("cp1", "Bob & Dave's Jams", bob)
    cp1.add_track(t1)
    cp1.add_track(t2)
    cp1.add_track(t3)
    platform.add_playlist(cp1)

    #sessions
    s1 = ListeningSession("s1", alice, t1, RECENT, 120)
    platform.record_session(s1)

    #Bob (PremiumUser) listens to t1 for 180s (3m) RECENTLY
    s2 = ListeningSession("s2", bob, t1, RECENT + timedelta(minutes=5), 180)
    platform.record_session(s2)

    #Bob (PremiumUser) listens to t2 for 240s (4m) OLD
    s3 = ListeningSession("s3", bob, t2, OLD, 240)
    platform.record_session(s3)

    #Dave (FamilyMember, age 15) listens to t1 for 60s (1m) RECENTLY
    s4 = ListeningSession("s4", dave, t1, RECENT, 60)
    platform.record_session(s4)

    #Alice listens to t2 and t3 to complete "Digital Dreams"
    s5 = ListeningSession("s5", alice, t2, RECENT, 210)
    s6 = ListeningSession("s6", alice, t3, RECENT, 195)
    platform.record_session(s5)
    platform.record_session(s6)

    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
