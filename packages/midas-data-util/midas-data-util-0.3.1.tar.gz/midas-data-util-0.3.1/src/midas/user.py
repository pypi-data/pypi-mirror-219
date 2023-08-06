import datetime as dt
import copy
from datetime import datetime
from typing import Any, TypedDict, Optional
from .session import Session
from .playfab import get_playfab_str_from_datetime

class UserDumpData(TypedDict):
	user_id: str
	timestamp: str
	index: int
	session_count: int
	net_revenue: int
	net_duration: float
	is_retained_on_d0: Optional[bool]
	is_retained_on_d1: Optional[bool]
	is_retained_on_d7: Optional[bool]
	is_retained_on_d14: Optional[bool]
	is_retained_on_d28: Optional[bool]

class User:
	user_id: str
	timestamp: datetime
	index: int
	session_count: int
	net_revenue: int
	net_duration: float
	is_retained_on_d0: Optional[bool]
	is_retained_on_d1: Optional[bool]
	is_retained_on_d7: Optional[bool]
	is_retained_on_d14: Optional[bool]
	is_retained_on_d28: Optional[bool]

	def __init__(self, sessions: list[Session]):
		sessions.sort()

		first_session = sessions[0]

		self.user_id = first_session.user_id
		self.sessions = sessions
		self.timestamp = first_session.timestamp

		last_session = sessions[len(sessions)-1]

		final_timestamp = last_session.timestamp
		
		self.net_revenue = 0
		self.net_duration = 0.0
	
		index = 0
		for session in sessions:
			index += 1
			session.index = index
			self.net_revenue += session.revenue
			self.net_duration += session.duration

		def get_sessions_count_between(start: datetime, finish: datetime):
			sessionsBetween = []

			for session in sessions:
				if session.timestamp >= start and session.timestamp <= finish:
					sessionsBetween.append(session)

			return sessionsBetween

		def get_retention_status(day: int, threshold: int) -> Optional[bool]:
			start: datetime = self.timestamp + dt.timedelta(days=day)
			finish: datetime = start + dt.timedelta(days=1)
			if finish <= datetime.now():
				return len(get_sessions_count_between(start, finish)) > threshold
			else:
				return None
			
		self.is_retained_on_d0 = get_retention_status(0, 1)
		self.is_retained_on_d1 = get_retention_status(1, 2)
		self.is_retained_on_d7 = get_retention_status(7, 8)
		self.is_retained_on_d14 = get_retention_status(14, 15)
		self.is_retained_on_d28 = get_retention_status(28, 29)

		self.index = -1

	def __lt__(self, other):
		t1 = self.timestamp
		t2 = other.timestamp
		return t1 < t2
		
	def dump(self) -> UserDumpData:
		data: Any = {
			"user_id": self.user_id,
			"timestamp": get_playfab_str_from_datetime(self.timestamp),
			"index": self.index,
			"session_count": len(self.sessions),
			"net_revenue": self.net_revenue,
			"net_duration": self.net_duration,
			"is_retained_on_d0": self.is_retained_on_d0,
			"is_retained_on_d1": self.is_retained_on_d1,
			"is_retained_on_d7": self.is_retained_on_d7,
			"is_retained_on_d14": self.is_retained_on_d14,
			"is_retained_on_d28": self.is_retained_on_d28,
		}
		return data

def get_users_from_session_list(sessions: list[Session]):
	
	user_session_lists: dict[str, list[Session]] = {}
	for session in sessions:
		user_id = session.user_id
		if not user_id in user_session_lists:
			user_session_lists[user_id] = []

		user_session_list = user_session_lists[user_id]
		user_session_list.append(session)

	print("Constructing user objects")
	users: list[User] = []
	for i, userId in enumerate(user_session_lists):
		user_data = user_session_lists[userId]
		user = User(user_data)
		users.append(user)
	
	print("sorting users")
	users = sorted(users, key=lambda user: user.timestamp)

	print("adding user indeces")
	user_index = 0
	for user in users:
		user_index += 1
		user.index = user_index

	print("returning users")
	return users