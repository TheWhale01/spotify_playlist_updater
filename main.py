import json
import spotify
import secrets
import requests
		

def main():
	spotify.update(secrets.liked_playlist)

if (__name__ == "__main__"):
	main()