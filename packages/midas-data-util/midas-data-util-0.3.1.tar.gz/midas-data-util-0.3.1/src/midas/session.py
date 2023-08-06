from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, TypedDict, Literal, Optional
from .playfab import get_playfab_str_from_datetime
from .event import Event

ScreenRatio = Literal["16:10","16:9","5:4","5:3","3:2","4:3","9:16","uncommon"]

class SessionDumpData(TypedDict):
	session_id: str
	user_id: str
	is_studio: bool
	timestamp: str
	version_text: str
	duration: float
	revenue: int
	index: int
	event_count: int
	account_age: Optional[int]
	roblox_language: Optional[str]
	system_language: Optional[str]
	accelerometer: Optional[bool]
	gamepad_enabled: Optional[bool]
	gyroscope_enabled: Optional[bool]
	keyboard_enabled: Optional[bool]
	mouse_enabled: Optional[bool]
	touch_enabled: Optional[bool]
	screen_size: Optional[int]
	screen_ratio: Optional[ScreenRatio]
	starting_group_memberships: Optional[dict[str, bool]]
	starting_gamepasses: Optional[dict[str, bool]]

class Session: 
	session_id: str
	user_id: str
	events: list[Event]
	timestamp: datetime
	version_text: str
	duration: float
	revenue: int
	index: int
	is_studio: bool
	account_age: Optional[int]
	roblox_language: Optional[str]
	system_language: Optional[str]
	accelerometer: Optional[bool]
	gamepad_enabled: Optional[bool]
	gyroscope_enabled: Optional[bool]
	keyboard_enabled: Optional[bool]
	mouse_enabled: Optional[bool]
	touch_enabled: Optional[bool]
	screen_size: Optional[int]
	screen_ratio: Optional[ScreenRatio]
	starting_group_memberships: Optional[dict[str, bool]]
	starting_gamepasses: Optional[dict[str, bool]]

	def __init__(
		self, 
		events: list[Event]
	):
		# sort list
		events = sorted(events, key=lambda event: event.timestamp)

		# get event bookends
		first_event = events[0]
		last_event = events[len(events)-1]
	
		self.session_id = first_event.session_id
		self.user_id = first_event.user_id
		self.events = events
		self.is_studio = first_event.is_studio
		self.timestamp = first_event.timestamp - timedelta(seconds=first_event.seconds_since_session_start)
	
		self.version_text = first_event.version_text

		# get duration
		self.duration = 0
		self.revenue = 0
		self.account_age: Optional[int] = None
		self.roblox_language: Optional[str] = None
		self.system_language: Optional[str] = None
		self.accelerometer: Optional[bool] = None
		self.gamepad_enabled: Optional[bool] = None
		self.gyroscope_enabled: Optional[bool] = None
		self.keyboard_enabled: Optional[bool] = None
		self.mouse_enabled: Optional[bool] = None
		self.touch_enabled: Optional[bool] = None
		self.screen_size: Optional[int] = None
		self.screen_ratio: Optional[ScreenRatio] = None
		self.starting_group_memberships: Optional[dict[str, bool]] = None
		self.starting_gamepasses: Optional[dict[str, bool]] = None



		def set_optional_state(state_data: Any):

			if "Demographics" in state_data:
				demo_data = state_data["Demographics"]

				def safe_index(key: str) -> Optional[Any]:
					if key in demo_data:
						return demo_data[key]
					else:
						return None

				if self.account_age == None:
					self.account_age = safe_index("AccountAge")

				if self.roblox_language == None:
					self.roblox_language = safe_index("RobloxLanguage")

				if self.system_language == None:
					self.system_language = safe_index("SystemLanguage")

				plat_data: Any = safe_index("Platform")
				if plat_data != None:
					if self.accelerometer == None:
						self.accelerometer = plat_data["Accelerometer"]
					if self.gamepad_enabled == None:
						self.gamepad_enabled = plat_data["Gamepad"]
					if self.gyroscope_enabled == None:
						self.gyroscope_enabled = plat_data["Gyroscope"]
					if self.keyboard_enabled == None:
						self.keyboard_enabled = plat_data["Keyboard"]
					if self.mouse_enabled == None:
						self.mouse_enabled = plat_data["Mouse"]
					if self.touch_enabled == None:
						self.touch_enabled = plat_data["Touch"]
					if self.screen_size == None:
						self.screen_size = plat_data["ScreenSize"]
					if self.screen_ratio == None:
						self.screen_ratio = plat_data["ScreenRatio"]

			if "Groups" in state_data:
				if self.starting_group_memberships == None:
					self.starting_group_memberships = deepcopy(state_data["Groups"])

			if "Market" in state_data:
				if "Gamepasses" in state_data["Market"]:
					if self.starting_gamepasses == None:
						self.starting_gamepasses = deepcopy(state_data["Market"]["Gamepasses"])
		for event in events:
			self.duration = max(self.duration, event.seconds_since_session_start)
			self.revenue += event.revenue
			set_optional_state(event.state_data)

		self.index = -1
	
	def __lt__(self, other):
		t1 = self.timestamp
		t2 = other.timestamp
		return t1 < t2

	def dump(self) -> SessionDumpData:
		out: SessionDumpData = {
			"session_id": self.session_id,
			"user_id": self.user_id,
			"is_studio": self.is_studio,
			"event_count": len(self.events),
			"timestamp": get_playfab_str_from_datetime(self.timestamp),
			"version_text": self.version_text,
			"duration": self.duration,
			"revenue": self.revenue,
			"index": self.index,
			"account_age": self.account_age,
			"roblox_language": self.roblox_language,
			"system_language": self.system_language,
			"accelerometer": self.accelerometer,
			"gamepad_enabled": self.gamepad_enabled,
			"gyroscope_enabled": self.gyroscope_enabled,
			"keyboard_enabled": self.keyboard_enabled,
			"mouse_enabled": self.mouse_enabled,
			"touch_enabled": self.touch_enabled,
			"screen_size": self.screen_size,
			"screen_ratio": self.screen_ratio,
			"starting_gamepasses": None,
			"starting_group_memberships": None,
		}
		
		if type(self.starting_group_memberships) == dict:
			out["starting_group_memberships"] = deepcopy(self.starting_group_memberships)

		if type(self.starting_gamepasses) == dict:	
			out["starting_gamepasses"] = deepcopy(self.starting_gamepasses)

		return out

def get_sessions_from_events(
	events: list[Event],
	sessions_must_include_exit_and_enter_events=False,
	exit_event_name="UserExitQuit", 
	enter_event_name="UserJoinEnter",
	) -> list[Session]:
	session_events: dict[str, list[Event]] = {}

	for event in events:
		if not event.session_id in session_events:
			session_events[event.session_id] = []
			
		session_events[event.session_id].append(event)
	
	max_session_count = len(list(session_events.keys()))
	print("session keys: ", max_session_count)

	# Sort session events by timestamp
	sessions: list[Session] = []
	sessions_missing_end_events = 0
	sessions_missing_start_events = 0
	sessions_with_bookends = 0

	valid_event_count = 0
	invalid_event_count = 0
	event_count = 0
	net_duration = 0.0
	
	for session_id in session_events:
		session_event_list = session_events[session_id]
		session_event_list = sorted(session_event_list, key=lambda session: session.timestamp)
		first_event = session_event_list[0]

		for i in range(1, len(events)):
			event = events[i]
			prev_event = events[i-1]
			if event.name != enter_event_name and event.name != exit_event_name:
				if event.index-1 == prev_event.index:
					valid_event_count += 1
				else:
					invalid_event_count += 1


		includes_bookend_events = False

		if first_event.name != enter_event_name:
			sessions_missing_start_events += 1
		
		if len(session_event_list) > 1:
			last_event = session_event_list[len(session_event_list)-1]
			if last_event.name != exit_event_name:
				sessions_missing_end_events += 1
				invalid_event_count += 1
			includes_bookend_events = first_event.name == enter_event_name and last_event.name == exit_event_name

		if includes_bookend_events:
			sessions_with_bookends += 1

		if len(session_event_list) > 0:
			if includes_bookend_events or sessions_must_include_exit_and_enter_events == False:
				session = Session(session_event_list)
				event_count += len(session.events)
				net_duration += float(session.duration)
				sessions.append(session)

	print("avg events per minute", round(10*((event_count/(net_duration/60))))/10)
	print("event validity rate:", round(1000*valid_event_count/(valid_event_count+invalid_event_count))/10, "%")
	print("start event success rate:", round(1000*sessions_missing_start_events/max_session_count)/10, "%")
	print("end event success rate:", round(1000*sessions_missing_end_events/max_session_count)/10, "%")	
	print("session bookend success rate:", round(1000*sessions_with_bookends/max_session_count)/10, "%")	

	return sessions