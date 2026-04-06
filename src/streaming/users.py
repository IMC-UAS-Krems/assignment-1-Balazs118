"""
users.py
--------
Implement the class hierarchy for platform users.

Classes implemented:
  - User (base class)
    - FreeUser
    - PremiumUser
      - FamilyAccountUser
    - FamilyMember
"""

from datetime import date
class User:
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session) -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> float:
        total_seconds = 0
        for s in self.sessions:
            total_seconds += s.duration_listened_seconds
        return total_seconds

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        track_ids = set()
        for s in self.sessions:
            track_ids.add(s.track.track_id)
        return track_ids


class FreeUser(User):
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int,subscription_start = None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id: str, name: str, age: int, subscription_start = None):
        super().__init__(user_id, name, age, subscription_start)
        self._sub_users: list["FamilyMember"] = []

    def add_sub_user(self, member: "FamilyMember") -> None:
        if member not in self._sub_users:
            self._sub_users.append(member)
            member.parent = self

    @property
    def sub_users(self) -> list["FamilyMember"]:
        return list(self._sub_users)

    def all_members(self) -> list[User]:
        return [self] + self.sub_users


class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent = None):
        super().__init__(user_id, name, age)
        self.parent = parent
        if parent is not None:
            parent.add_sub_user(self)
