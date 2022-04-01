import json
import deezer
import spotify
import secrets
import requests

def main():
	spotify.refresh()
	spotify.update_liked(secrets.spotify_liked_playlist)
	for deezer_playlist_id in secrets.deezer_playlist_id:
		spotify_tracks = spotify.find_songs_name(secrets.spotify_shared_playlist)
		deezer_tracks = deezer.find_songs(deezer_playlist_id)
		spotify.update(deezer_tracks, secrets.spotify_shared_playlist)
		deezer.update(spotify_tracks, deezer_playlist_id)

if (__name__ == "__main__"):
	main()
