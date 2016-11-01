import sys
from subprocess import call
from gmusicapi import Mobileclient
from config import google_play_music_email, google_play_music_password
from text_to_speech import speak

api = Mobileclient()
if api.login(google_play_music_email, google_play_music_password, Mobileclient.FROM_MAC_ADDRESS):
    pass
else:
    print("Login unsuccessful, exiting")
    sys.exit(1)

def get_song(title, artist):
    """Get song information given the title and artist"""
    return api.search(title + " " + artist)['song_hits'][0]['track']

def play_song(song_id):
    """Play a song on Google Play Music using mpg123 given its song_id"""
    https_url = api.get_stream_url(song_id)
    url = 'http' + https_url[5:]
    call(["mpg123", "-q", url])

if __name__ == '__main__':
    song = get_song("Panda", "Designer")
    speak("Now playing '{}' by '{}'".format(song['title'], song['artist']))
    play_song(song['nid'])
