import json
import secrets
import requests

def find_songs(endpoint):
	tracks = []
	query = f"https://api.deezer.com/playlist/{endpoint}"
	response = requests.get(query, headers={"Content-Type": "application/json"})
	response_json = response.json()
	for track in response_json["tracks"]["data"]:
		tracks.append((track["title"].lower(), track["artist"]["name"].lower()))
	return (tracks)

def add_song(track: tuple(), endpoint: str()):
	query = f"https://api.deezer.com/search?q={track[0]}"
	response = requests.get(query, headers={"Content-Type": "application/json"})
	response_json = response.json()
	for item in response_json["data"]:
		if (track[1] == item["artist"]["name"].lower()):
			response = requests.post(f"https://api.deezer.com/playlist/{endpoint}/tracks?songs={item['id']}&access_token={secrets.tokens.deezer_token}")
			break 

def update(spotify_tracks, endpoint):
	print("Updating Deezer share playlist")
	deezer_tracks = find_songs(endpoint)
	for track in spotify_tracks:
		if (track not in deezer_tracks):
			add_song(track, endpoint)
