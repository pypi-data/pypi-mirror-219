import pandas as pd
from pandas import DataFrame
from typing import Any
from .event import Event, get_events_from_df
from .session import Session, SessionDumpData,  get_sessions_from_events
from .user import User, UserDumpData, get_users_from_session_list

def dump(objects: list[Event] | list[Session] | list[User]):
	untyped_objects: Any = objects
	object_count = len(objects)
	if type(objects[0]) == Event:
		event_list: list[Event] = untyped_objects
		event_data_list: list[Any] = []
		for i, event in enumerate(event_list):
			event_data_list.append(event.dump())
		event_df: Any = DataFrame(event_data_list)
		return event_df
	if type(objects[0]) == Session:
		session_list: list[Session] = untyped_objects
		session_data_list: list[SessionDumpData] = []
		for i, session in enumerate(session_list):
			session_data_list.append(session.dump())
		session_df: Any = DataFrame(session_data_list)
		return session_df
	if type(objects[0]) == User:
		user_data_list: list[UserDumpData] = []
		user_list: list[User] = untyped_objects
		for i, user in enumerate(user_list):
			user_data_list.append(user.dump())
		user_df: Any = DataFrame(user_data_list)
		return user_df	
	

	
def load(
	decoded_df: DataFrame,
	# stitch_session_separation_limit_seconds=180, 
	exit_event_name="UserExitQuit", 
	enter_event_name="UserJoinEnter",
	# rejoin_event_name="UserRejoin",
	# teleport_event_name="UserTeleport",
	sessions_must_include_exit_and_enter_events=False,
	# fill_down_enabled=False, 
	# recursive_fill_down_enabled=False
) -> tuple[list[Event], list[Session], list[User]]:

	max_event_count = decoded_df.shape[0]
	print(f"assembling events from {max_event_count} event entries")
	events = get_events_from_df(decoded_df) #, stitch_session_separation_limit_seconds, exit_event_name, enter_event_name, rejoin_event_name, teleport_event_name, fill_down_enabled, recursive_fill_down_enabled)
	# print("failed to load ",round(1000*(1-(len(events)/max_event_count)))/10, "%","of events")

	print(f"assembling sessions from {len(events)} events")
	sessions = get_sessions_from_events(events, sessions_must_include_exit_and_enter_events, exit_event_name, enter_event_name)
	
	print(f"assembling users from {len(sessions)} sessions")
	users = get_users_from_session_list(sessions)
	
	# survival_rate = get_survival_rate(sessions)

	# print("event survival rate: "+str(round(survival_rate*100000)/1000)+"%")

	final_sessions: list[Session] = []
	for user in users:
		for session in user.sessions:
			final_sessions.append(session)

	final_events: list[Event] = []
	for session in final_sessions:
		for event in session.events:
			final_events.append(event)

	return final_events, final_sessions, users
