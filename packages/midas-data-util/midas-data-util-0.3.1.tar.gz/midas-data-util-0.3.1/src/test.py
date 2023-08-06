import pandas as pd
import json
import midas
from pandas import DataFrame
from datetime import datetime
import midas.data_encoder as data_encoder
from midas.playfab import PlayFabClient

INPUT_JSON_PATH = "test/in/data.json"
MID_JSON_PATH = "test/in/mid-data.json"
RAW_INPUT_JSON_PATH = "test/in/raw-data.json"
CACHE = "midas.cache"
OUTPUT_DIR = "test/out"
EVENTS_JSON = OUTPUT_DIR+"/events.json"
SESSIONS_JSON = OUTPUT_DIR+"/sessions.json"
USERS_JSON = OUTPUT_DIR+"/users.json"

def download():

	pf = PlayFabClient(
		client_id="f0cea4a6-6f42-4cb4-aab3-9f95cab2a23c",
		client_secret="xWX8Q~B_nKuRzt60MNABJAaInJPnax1lCMNt3bxz",
		tenant_id="23bc396d-18ee-4fcd-b259-78655a83767e",
		title_id="FA114"
	)

	print("downloading raw-df")
	download_df = DataFrame(pf.download_all_event_data(
		user_join_floor=datetime(year=2023, month=7, day=10),
		join_window_in_days=10,
		user_limit=10000000,
		max_event_list_length=10000,
		update_increment=2500,
	))
	print("converting to json")
	download_df.to_json(RAW_INPUT_JSON_PATH, indent=4, orient="records")

def decode_data_with_patch():

	with open(CACHE, "r") as midas_cache_file:
		cache_text = midas_cache_file.read()
		midas_cache = json.loads(cache_text)

	# decode json
	with open(RAW_INPUT_JSON_PATH, "r") as raw_json_reader:
		raw_json_txt = raw_json_reader.read()

		raw_json_data = json.loads(raw_json_txt)
		for event_data in raw_json_data:
			if "~%" in event_data:
				demographic_data = event_data["~%"]
				event_data["~$("] = demographic_data
				event_data.pop("~%")

		final_raw_json_data = []
		for event_data in raw_json_data:
			if not "+0" in event_data["EventData"]["Version"]:
				final_raw_json_data.append(event_data)

		mid_json_txt = json.dumps(final_raw_json_data, indent=5)

		with open(MID_JSON_PATH, "w") as mid_json_writer:
			mid_json_writer.write(mid_json_txt)

	raw_df = pd.read_json(MID_JSON_PATH)
	df = data_encoder.decode_raw_df(raw_df, midas_cache)
	df.to_json(INPUT_JSON_PATH, indent=4, orient="records")

def oop_the_data():
	# export data into json
	df = pd.read_json(INPUT_JSON_PATH)
	events, sessions, users = midas.load(df)
	print("constructing event table")
	event_df = DataFrame(midas.dump(events))
	event_df.to_json(EVENTS_JSON, indent=4, orient="records")

	print("constructing session table")
	session_df = DataFrame(midas.dump(sessions))
	session_df.to_json(SESSIONS_JSON, indent=4, orient="records")

	print("constructing user table")
	session_df = DataFrame(midas.dump(users))
	session_df.to_json(USERS_JSON, indent=4, orient="records")

# decode_data_with_patch()
oop_the_data()