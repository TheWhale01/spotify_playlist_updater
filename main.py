import json
import secrets
import requests

class SavedSongs:
	def __init__(self):
		self.token = secrets.token
		self.user_id = secrets.user_id
		self.refresh_token = secrets.refresh_token

	def find_songs(self, endpoint):
		tracks = []
		if (endpoint == "me"):
			query = f"https://api.spotify.com/v1/me/tracks?limit=50"
			print("Checking songs in \"Liked Songs\" playlist")
		else:
			query = f"https://api.spotify.com/v1/playlists/{endpoint}/tracks"
			print("Checking songs in custom playlist")
		response = requests.get(query, headers={
			"Content-type": "application/json",
			"Authorization": f"Bearer {self.token}"
		})
		response_json = response.json()
		if (endpoint == "me"):
			for item in response_json["items"]:
				tracks.append(item["track"]["uri"])
		else:
			item = response_json["items"][0]
			tracks.append(item["track"]["uri"])
		return (tracks)

	def refresh(self):
		response = requests.post("https://accounts.spotify.com/api/token",
		headers={
			"Authorization": f"Basic {secrets.client_id_base64}"
		}, data={
			"grant_type": "refresh_token",
			"refresh_token": self.refresh_token
		})
		self.token = response.json()["access_token"]

	def update(self, endpoint):
		i = 0
		self.refresh()
		tracks = self.find_songs("me")
		l_track = self.find_songs(endpoint)
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
			"Authorization": f"Bearer {self.token}",
		}, data=body)

def main():
	saved = SavedSongs()
	saved.update(secrets.liked_playlist)

if (__name__ == "__main__"):
	main()