from copy import deepcopy
import json
from uuid import uuid4
from pandas import DataFrame
from datetime import datetime
from typing import Any
from .playfab import get_datetime_from_playfab_str, get_playfab_str_from_datetime
from .data_encoder import DecodedRowData as RowData
from .data_encoder import VersionData, EventData, BaseStateTree

SID_GEN_REFIX = "!generated"

# def get_if_session_id_generated(session_id: str) -> bool:
# 	pattern = session_id[0:len(SID_GEN_REFIX)]
# 	result = pattern == SID_GEN_REFIX
# 	# print(f"is_gen: {result} since {pattern} is start of {session_id}")
# 	return result

def version_to_version_text(version: VersionData, is_hotfix_included=True, is_tag_included=False, is_test_group_included=False, is_build_included=True):
	major = version["Major"]
	minor = version["Minor"]
	patch = version["Patch"]
	
	version_text = f"v{major}.{minor}.{patch}"

	if is_hotfix_included and "Hotfix" in version and version["Hotfix"] != None:
		hotfix = version["Hotfix"]
		version_text+=f".{hotfix}"

	if is_tag_included and "Tag" in version and version["Tag"] != None:
		tag = version["Tag"]
		version_text+=f"-{tag}"

	if is_test_group_included and "TestGroup" in version and version["TestGroup"] != None:
		test_group = version["Tag"]
		version_text+=f"-{test_group}"

	if is_build_included:
		build = version["Build"]
		version_text+=f"-{build}"

	return version_text

class EventDumpData:
	name: str
	event_id: str
	timestamp: str
	seconds_since_session_start: float
	version_text: str
	revenue: int
	session_id: str
	user_id: str
	place_id: str
	version: VersionData
	index: int
	is_studio: bool
	is_sequential: bool
	state_data: BaseStateTree

class Event: 
	name: str
	event_id: str
	timestamp: datetime
	seconds_since_session_start: float
	version_text: str
	revenue: int
	session_id: str
	user_id: str
	place_id: str
	version: VersionData
	index: int
	is_studio: bool
	is_sequential: bool
	state_data: BaseStateTree

	def __init__(
		self, 
		row_data: RowData
	):
		
		self.name = row_data["EventName"]
		self.event_id = row_data["EventId"]
		self.timestamp: datetime = get_datetime_from_playfab_str(row_data["Timestamp"])

		event_data: EventData = row_data["EventData"]
		state_data = event_data["State"]
	
		if not "Version" in state_data:
			print(self.event_id)

		self.version_text = version_to_version_text(state_data["Version"])
		self.session_id = SID_GEN_REFIX + str(uuid4())

		id_data = state_data["Id"]
		assert id_data != None
		self.place_id = id_data["Place"]
		self.user_id = id_data["User"]
		self.session_id = row_data["SessionId"]
		
		self.version = state_data["Version"]
		self.index = state_data["Index"]["Event"]
		self.is_studio = state_data["IsStudio"]
		self.state_data = state_data
		self.revenue = 0
		self.seconds_since_session_start = row_data["Time"]
		self.is_sequential = False

	def __lt__(self, other):
		t1 = self.index
		t2 = other.index
		return t1 < t2

	def dump(self) -> EventDumpData:
		event_dump_date: Any = {
			"name": self.name,
			"event_id": self.event_id,
			"timestamp": get_playfab_str_from_datetime(self.timestamp),
			"seconds_since_session_start": self.seconds_since_session_start,
			"version_text": self.version_text,
			"revenue": self.revenue,
			"session_id": self.session_id,
			"user_id": self.user_id,
			"place_id": self.place_id,
			"version": deepcopy(self.version),
			"index": self.index,
			"is_studio": self.is_studio,
			"is_sequential": self.is_sequential,
			"state_data": deepcopy(self.state_data),
		}
		return event_dump_date

# def fill_down(current_data: dict | None, prev_data: dict | None):
# 		if current_data == None:
# 			current_data = {}

# 		assert current_data

# 		if prev_data == None:
# 			return current_data

# 		assert prev_data

# 		for key in prev_data:
# 			val = prev_data[key]
# 			if not key in current_data:
# 				current_data[key] = deepcopy(prev_data[key])

# 				return current_data

# 			if type(val) == dict:
# 				fill_down(current_data[key], prev_data[key])
# 			else:
# 				current_data[key] = val

# 		return current_data

# def transfer_property(previous_data: dict, current_data: dict):
# 	for key in previous_data:
# 		val = previous_data[key]
# 		if not key in current_data:
# 			current_data[key] = {}

# 		if type(val) == dict:
# 			current_data[key] = fill_down(current_data[key], previous_data[key])
		

# # fill down event data when previous index is available
# def fill_down_event_from_previous(previous: Event, current: Event):
# 	if current.is_sequential:
# 		previous_data: Any = previous.state_data
# 		current_data: Any = current.state_data
# 		transfer_property(previous_data, current_data)

# def fill_down_events(session_events: list[Event], current: Event, targetIndex: int, depth: int):
# 	if current.is_sequential:
# 		depth += 1
# 		if depth > 100:
# 			return

# 		for previous in session_events:
# 			if previous.index == targetIndex:
# 				fill_down_event_from_previous(previous, current)
# 				break
# 		if targetIndex > 1:
# 			fill_down_events(session_events, current, targetIndex-1, depth)

def get_events_from_df(
	decoded_df: DataFrame
	# stitch_session_separation_limit_seconds=180, 
	# exit_event_name="UserExitQuit", 
	# enter_event_name="UserJoinEnter",
	# rejoin_event_name="UserRejoin",
	# teleport_event_name="UserTeleport",
	# fill_down_enabled=False, 
	# recursive_fill_down_enabled=False
) -> list[Event]:
	initial_events: list[Event] = []

	user_events: dict[str, list[Event]] = {}

	print("organizing events by user_id")
	for row_index, row_data in decoded_df.iterrows():

		if type(row_data["EventData"]) == str:
			row_data["EventData"] = json.loads(row_data["EventData"].replace("'", "\"").replace("False", "false").replace("True", "true"))

		event = Event(row_data)
		# if not event.user_id in user_events:
		# 	user_events[event.user_id] = []
		
		# user_events[event.user_id].append(event)
		initial_events.append(event)

	# final_events: list[Event] = []
	
	# print("organizing events into chronological series for session id")
	# for event_list in user_events.values():
	# 	sorted_event_list = sorted(event_list, key=lambda event: event.timestamp)
	# 	event_count = len(sorted_event_list)
	# 	final_index = event_count-1
	# 	session_id_order: list[str] = []
	# 	initial_session_registry: dict[str, list[Event]] = {}

	# 	def assemble_session(start_index=0) -> None:
	# 		session_id = str(uuid4())
			
	# 		session_events: list[Event] = []
	# 		next_index=start_index+1
	# 		if start_index == final_index:
	# 			session_events.append(sorted_event_list[start_index])
	# 		else:
	# 			# print("\nMULTI EVENT!")
	# 			for i in range(start_index, final_index):
					
	# 				event = sorted_event_list[i]
	# 				# print(f"index {i}: [{start_index}/{final_index}] at {event.timestamp}")
	# 				relative_index = i-start_index
	# 				next_index = i+1

	# 				if relative_index != 0 and event.name == enter_event_name:
	# 					# print("A")
	# 					break

	# 				is_session_id_generated = get_if_session_id_generated(event.session_id)
	# 				if relative_index > 0:
	# 					prev_event = session_events[relative_index-1]
	# 					is_prev_session_id_generated = get_if_session_id_generated(prev_event.session_id)
	# 					if is_session_id_generated and not is_prev_session_id_generated:
	# 						# print("B1")
	# 						break
	# 					elif not is_session_id_generated and not is_prev_session_id_generated and event.session_id != prev_event.session_id:
	# 						# print(f"B2: {event.session_id}, {prev_event.session_id}")
	# 						break
	# 					elif prev_event.name == exit_event_name:
	# 						# print("B3")
	# 						break
	# 					elif prev_event.is_studio != event.is_studio:
	# 						# print("B4")
	# 						break

	# 				session_events.append(event)

	# 		if len(session_events) > 0:
	# 			initial_session_registry[session_id] = session_events
	# 			session_id_order.append(session_id)

	# 		if next_index <= final_index:
	# 			assemble_session(next_index)

	# 		return None

	# 	assemble_session()
		
	# 	initial_final_index = len(session_id_order)-1
	# 	final_session_list: list[list[Event]] = []
	# 	def merge_sessions(start_index=0) -> None:
	# 		final_index = start_index+1
	# 		session_run: list[list[Event]] = []
	# 		if start_index == initial_final_index:
	# 			session_run.append(initial_session_registry[session_id_order[start_index]])
	# 		else:
	# 			for i in range(start_index, initial_final_index):
	# 				relative_index = i-start_index
	# 				session_event_list = initial_session_registry[session_id_order[i]]

	# 				final_index = i + 1
	# 				# print("ri", relative_index, "sr", len(session_run))
	# 				if relative_index > 0:
	# 					prev_session_event_list = session_run[relative_index-1]
	# 					prev_final_event = prev_session_event_list[len(prev_session_event_list)-1]
	# 					first_event = session_event_list[0]
	# 					sec_dif = (first_event.timestamp - prev_final_event.timestamp).total_seconds()
	# 					if sec_dif < stitch_session_separation_limit_seconds:
	# 						session_run.append(session_event_list)
	# 					else:
	# 						break
	# 				else:
	# 					session_run.append(session_event_list)
		
	# 		if len(session_run) > 1:
	# 			composite_event_list: list[Event] = []
	# 			for i, session_event_list in enumerate(session_run):
	# 				rename_first_event = i > 0
	# 				keep_final_event = i == len(session_run)-1

	# 				is_new_place = False
	# 				if i > 0:
	# 					prev_session_event_list = session_run[i-1]
	# 					is_new_place = prev_session_event_list[0].place_id == session_event_list[0].place_id

	# 				for j, event in enumerate(session_event_list):
	# 					if j == 0 and rename_first_event:
	# 						if is_new_place:
	# 							event.name == teleport_event_name
	# 						else:
	# 							event.name == rejoin_event_name
						
	# 					if j < len(session_event_list)-1 or keep_final_event:
	# 						composite_event_list.append(event)

	# 			final_session_list.append(composite_event_list)
	# 		else:
	# 			final_session_list.append(session_run[0])		

	# 		if final_index <= len(session_id_order)-1:
	# 			merge_sessions(final_index)

	# 		return None

	# 	merge_sessions()

	# 	for session_event_list in final_session_list:
	# 		session_id = str(uuid4())
	# 		if len(session_event_list) > 1:
	# 			first_event = session_event_list[0]
	# 			for i, event in enumerate(session_event_list):
	# 				event.session_id = session_id
	# 				final_events.append(event)
	# 				if i > 0:
	# 					prev_event = session_event_list[i-1]
	# 					event.seconds_since_session_start = (event.timestamp - first_event.timestamp).total_seconds()
							
	# 					# handle sequential stuff
	# 					if event.index == 2:
	# 						prev_event.is_sequential = True
	# 						event.is_sequential = True
	# 					elif prev_event.index == event.index - 1:
	# 						event.is_sequential = True

	# 					# handle fill down stuff
	# 					if fill_down_enabled:
	# 						if recursive_fill_down_enabled:
	# 							fill_down_event_from_previous(prev_event, event)
	# 						else:
	# 							fill_down_events(session_event_list, prev_event, event.index - 1, 0)
	# 		else:
	# 			event = session_event_list[0]
	# 			event.session_id = session_id
	# 			final_events.append(event)
		
	# 	# if len(event_list) > 1:
	# 	# 	break

	return initial_events

