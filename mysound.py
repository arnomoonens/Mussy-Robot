#!/usr/bin/python
# -*- coding: utf8 -*-

from recommender import MusicRecommender
from text_to_speech import speak
# from speech_to_text import get_voice_feedback
from google_play_music import get_song, play_song
from emotion_recognition import emotion_recognition
import time
import sys
from getch import getch

recommender = MusicRecommender('songs.csv')

#  Already fill the recommender with some feedback
recommender.song_feedback(343)
recommender.song_feedback(234)

def play(proc, imageQ):
    while not proc.empty():  # Keep playing songs
        found_song = False
        while not(found_song):
            recommend_song = recommender.recommend_song()
            song = recommender.get_song_information(recommend_song)
            speak("Now playing: " + song['Title'] + " by " + song['ArtistName'])
            try:
                song_gplay = get_song(song['Title'], song['ArtistName'])
                found_song = True
            except:
                continue
        play_process = play_song(song_gplay['nid'])
        time.sleep(5)
        if not imageQ.empty():  # If there are images to be used for emotion recognition
            gray = imageQ.get()
            print('presa')
            while not imageQ.empty():  # Remove all images from the queue
                imageQ.get()
            score = emotion_recognition(gray)
            print("Feedback for song " + str(recommend_song) + ": " + str(score))
            recommender.song_feedback(recommend_song, score=score)
        key = None
        while(key != '\x1b' and play_process.poll() != 0):  # While the song isn't done playing yet or no 'next' key is pressed
            key = getch()
            if key == 'q':
                print("Quitting...")
                play_process.terminate()
                sys.exit()
        print("Song is over or user wants the next song.")
        play_process.terminate()
