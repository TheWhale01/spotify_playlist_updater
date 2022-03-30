import json
import deezer
import spotify
import secrets
import requests

def main():
	spotify.refresh()
	spotify.update_liked(secrets.spotify_liked_playlist)
	spotify_tracks = spotify.find_songs_name(secrets.spotify_shared_playlist)
	deezer_tracks = deezer.find_songs(secrets.deezer_playlist_id)
	deezer.update(spotify_tracks, secrets.deezer_playlist_id)

if (__name__ == "__main__"):
	main()