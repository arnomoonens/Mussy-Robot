#!/usr/bin/python
# -*- coding: utf8 -*-

from recommender import MusicRecommender
# from text_to_speech import speak
# from speech_to_text import get_voice_feedback
from google_play_music import get_song, play_song
from emotion_recognition import emotion_recognition
import time

recommender = MusicRecommender('songs.csv')

#  Already fill the recommender with some feedback
recommender.song_feedback(343)
recommender.song_feedback(234)

def play(proc, imageQ, mylock):
    while not proc.empty():  # Keep playing songs
        print("Proc not empty, can play")
        found_song = False
        while not(found_song):
            recommend_song = recommender.recommend_song()
            song = recommender.get_song_information(recommend_song)
            try:
                song_gplay = get_song(song['Title'], song['ArtistName'])
                found_song = True
            except:
                continue
        play_process = play_song(song_gplay['nid'])
        time.sleep(5)
        score = 0
        while(score >= 0 and not(proc.empty()) and play_process.poll() != 0):  # While the song isn't done playing yet or no 'next' key is pressed
            if not imageQ.empty():  # If there are images to be used for emotion recognition
                mylock.acquire()
                gray = imageQ.get()
                print('I get it')
                while not imageQ.empty():  # Remove all images from the queue
                    imageQ.get()
                    print('empy')
                mylock.release()
                print('empty? ' + str(imageQ.empty()))
                #score = emotion_recognition(gray)
		score = 0
                print("Feedback for song " + str(recommend_song) + ": " + str(score))
                recommender.song_feedback(recommend_song, score=score)
        print("Song is over or user wants the next song.")
        play_process.terminate()
    play_process.terminate()
