#!/usr/bin/python
# -*- coding: utf8 -*-

import numpy as np

from recommender import MusicRecommender
from text_to_speech import speak
# from speech_to_text import get_voice_feedback
from google_play_music import get_song, play_song
from multiprocessing import Process
from emotion_recognition import emotion_recognition
import cv2
import time
import sys
from getch import getch

recommender = MusicRecommender('songs.csv')
# speak("Making recommender.")

# Use voice feedback
# random_id = np.random.randint(recommender.available_songs())
# song = recommender.get_song_information(random_id)
# print("Title:", song['Title'])
# speak("Do you like '{}' by '{}'?".format(song['Title'], song['ArtistName']))
# likes = get_voice_feedback(["yes", "no"]) == "yes"
# if likes:
#     speak("I understood that you like this song.")
# else:
#     speak("I understood that you don't like this song.")
# speak("Taking it into account")
# recommender.song_feedback(random_id, score=(likes * 2 - 1))  # -1 or 1

recommender.song_feedback(343)
recommender.song_feedback(234)

def play(proc,imageQ):
 while not proc.empty():  # Keep playing songs
     found_song = False
     while not(found_song):
         recommend_song = recommender.recommend_song()
         song = recommender.get_song_information(recommend_song)
         speak("Now playing: " + song['Title'] + " by " + song['ArtistName'])
         try:
             song_gplay = get_song(song['Title'], song['ArtistName'])
             found_song = True
         except KeyboardInterrupt:
             sys.exit()
         except:
             continue
     play_process = play_song(song_gplay['nid'])
     time.sleep(5)
     if not imageQ.empty():
         gray = imageQ.get()
         print 'presa'
         while not imageQ.empty():
             trash=imageQ.get()
         score = emotion_recognition(gray)
         print("Feedback for song " + str(recommend_song) + ": " + str(score))
         recommender.song_feedback(recommend_song, score=score)
         key = None
     while(key != '\x1b'):
         key = getch()
         if key == 'q':
             sys.exit()
     play_process.terminate()
