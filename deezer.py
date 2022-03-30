import json
import secrets
import requests
import urllib.parse

def find_songs(endpoint):
	tracks = []
	query = f"https://api.deezer.com/playlist/{endpoint}"
	response = requests.get(query, headers={"Content-Type": "application/json"})
	response_json = response.json()
	for track in response_json["tracks"]["data"]:
		tracks.append((track["title"].lower(), track["artist"]["name"].lower()))
	return (tracks)

def add_song(endpoint: tuple()):
	query = f"https://api.deezer.com/search?q={endpoint[0]}"
	response = requests.get(query, headers={"Content-Type": "application/json"})
	response_json = response.json()
	for item in response_json["data"]:
		print(item["artist"]["name"])
		if (endpoint[1] == item["artist"]["name"].lower()):
			response = requests.post(f"https://api.deezer.com/playlist/{secrets.deezer_playlist_id}/tracks?songs={item['id']}&access_token={secrets.deezer_token}")
			break 

def update(spotify_tracks, endpoint):
	print("Updating Deezer share playlist")
	deezer_tracks = find_songs(endpoint)
	for track in spotify_tracks:
		if (track not in deezer_tracks):
			print(track)
			add_song(track)