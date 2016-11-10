#!/usr/bin/python
# -*- coding: utf8 -*-

import numpy as np

from recommender import MusicRecommender
from text_to_speech import speak
from speech_to_text import get_voice_feedback
from google_play_music import get_song, play_song

recommender = MusicRecommender('songs.csv')
speak("Making recommender.")
random_id = np.random.randint(recommender.available_songs())
song = recommender.get_song_information(random_id)
print("Title:", song['Title'])
speak("Do you like '{}' by '{}'?".format(song['Title'], song['ArtistName']))
likes = get_voice_feedback(["yes", "no"]) == "yes"
if likes:
    speak("I understood that you like this song.")
else:
    speak("I understood that you don't like this song.")
speak("Taking it into account")
recommender.song_feedback(random_id, score=(likes * 2 - 1))  # -1 or 1
recommender.song_feedback(343)
recommender.song_feedback(234)
recommended = recommender.recommend_song()
song = recommender.get_song_information(recommended)
print("Title:", song['Title'])
speak("Recommended song: '{}' by '{}'".format(song['Title'], song['ArtistName']))
try:
    song_gplay = get_song(song['Title'], song['ArtistName'])
    play_song(song_gplay['nid'])
    print("Song executed")
except KeyboardInterrupt:
    pass
except:
    speak("Sorry, I could not play the recommended song. Exiting.")
