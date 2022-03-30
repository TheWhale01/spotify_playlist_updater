import json
import secrets
import requests
import urllib.parse

def find_songs_name(endpoint):
	tracks = []
	query = f"https://api.spotify.com/v1/playlists/{endpoint}/tracks"
	response = requests.get(query, headers={
		"Content-type": "application/json",
		"Authorization": f"Bearer {secrets.spotify_token}"
	})
	response_json = response.json()
	for item in response_json["items"]:
		tracks.append((item["track"]["name"].lower(), item["track"]["artists"][0]["name"].lower()))
	return (tracks)

def find_songs_uri(endpoint):
	tracks = []
	if (endpoint == "me"):
		query = f"https://api.spotify.com/v1/me/tracks?limit=50"
		print("Checking songs in \"Liked Songs\" playlist")
	else:
		query = f"https://api.spotify.com/v1/playlists/{endpoint}/tracks"
		print("Checking songs in custom playlist")
	response = requests.get(query, headers={
		"Content-type": "application/json",
		"Authorization": f"Bearer {secrets.spotify_token}"
	})
	response_json = response.json()
	if (endpoint == "me"):
		for item in response_json["items"]:
			tracks.append(item["track"]["uri"])
	else:
		item = response_json["items"][0]
		tracks.append(item["track"]["uri"])
	return (tracks)

def refresh():
	response = requests.post("https://accounts.spotify.com/api/token",
	headers={
		"Authorization": f"Basic {secrets.spotify_client_id_base64}"
	}, data={
		"grant_type": "refresh_token",
		"refresh_token": secrets.spotify_refresh_token
	})
	secrets.spotify_token = response.json()["access_token"]

def update_liked(endpoint):
	i = 0
	tracks = find_songs_uri("me")
	l_track = find_songs_uri(endpoint)
	print("Updating")
	if (tracks[0] == l_track[0]):
		return
	while (i < len(tracks) and tracks[i] != l_track[0]):
		i+=1
	while (i < len(tracks) and tracks[i]):
		del tracks[i]
	body = json.dumps({
		"uris": tracks,
		"position" : 0
	})
	query = f"https://api.spotify.com/v1/playlists/{endpoint}/tracks/"
	response = requests.post(query, headers={
		"Content-type": "application/json",
		"Authorization": f"Bearer {secrets.spotify_token}",
	}, data=body)

def add_songs(track):
	response = requests.get(f"https://api.spotify.com/v1/search?q={track[0]}&type=track", headers={
		"Content-Type": "application/json",
		"Authorization": f"Bearer {secrets.spotify_token}"
	})
	response_json = response.json()
	for item in response_json["tracks"]["items"]:
		if (track[1] == item["artists"][0]["name"].lower()):
			body = json.dumps({"uris": [item["uri"]]})
			query = f"https://api.spotify.com/v1/playlists/{secrets.spotify_shared_playlist}/tracks/"
			response = requests.post(query, data=body, headers={
				"Content-type": "application/json",
				"Authorization": f"Bearer {secrets.spotify_token}",
			})
			break

def update(deezer_tracks, endpoint):
	print("Updating Spotify share playlist")
	spotify_tracks = find_songs_name(endpoint)
	for track in deezer_tracks:
		if (track not in spotify_tracks):
			add_songs(track)