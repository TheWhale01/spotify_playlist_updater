import json
import requests
import secrets

def find_songs(endpoint):
	tracks = []
	if (endpoint == "me"):
		query = f"https://api.spotify.com/v1/me/tracks?limit=50"
		print("Checking songs in \"Liked Songs\" playlist")
	else:
		query = f"https://api.spotify.com/v1/playlists/{endpoint}/tracks"
		print("Checking songs in custom playlist")
	response = requests.get(query, headers={
		"Content-type": "application/json",
		"Authorization": f"Bearer {secrets.token}"
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
		"Authorization": f"Basic {secrets.client_id_base64}"
	}, data={
		"grant_type": "refresh_token",
		"refresh_token": secrets.refresh_token
	})
	secrets.token = response.json()["access_token"]

def update(endpoint):
	i = 0
	refresh()
	tracks = find_songs("me")
	l_track = find_songs(endpoint)
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
		"Authorization": f"Bearer {secrets.token}",
	}, data=body)