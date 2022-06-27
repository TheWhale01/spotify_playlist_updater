def erase_charset(charset, str):
	for c in charset:
		str = str.replace(c, "")
	return (str);

class Tokens():
	def __init__(self):
		self.spotify_token = ""
		self.spotify_redirect_uri = "https://github.com/TheWhale01"
		self.spotify_refresh_token = ""
		self.spotify_liked_playlist = ""
		self.spotify_client_id_base64 = ""
		self.spotify_shared_playlist = ""
		self.deezer_token = ""
		self.deezer_secret = ""
		self.deezer_playlist_id = []
		self.deezer_redirect_uri = self.spotify_redirect_uri
	
	def get_token(self, filename):
		with open(filename, "r") as file:
			lines = file.readlines()
			self.spotify_token = erase_charset("\n\"", lines[0])
			self.spotify_refresh_token =  erase_charset("\n\"", lines[1])
			self.spotify_liked_playlist = erase_charset("\n\"", lines[2])
			self.spotify_client_id_base64 = erase_charset("\n\"", lines[3])
			self.spotify_shared_playlist = erase_charset("\n\"", lines[4])
			self.deezer_token =  erase_charset("\n\"", lines[5])
			self.deezer_secret = erase_charset("\n\"", lines[6])
			self.deezer_playlist_id = erase_charset("\n[]\"", lines[7])
			self.deezer_playlist_id = self.deezer_playlist_id.split(", ")


	def show_tokens(self):
		print(f"spotify_token : {self.spotify_token}")
		print(f"spotify_refresh_token : {self.spotify_refresh_token}")
		print(f"spotify_liked_playlist : {self.spotify_liked_playlist}")
		print(f"spotify_client_id_base64 : {self.spotify_client_id_base64}")
		print(f"spotify_shared_playlist : {self.spotify_shared_playlist}")
		print(f"deezer_token : {self.deezer_token}")
		print(f"deezer_secret : {self.deezer_secret}")
		print(f"deezer_playlist_id : {self.deezer_playlist_id}")

tokens = Tokens()
tokens.get_token(".secrets.txt")
tokens.show_tokens()
