from recommender import MusicRecommender
from text_to_speech import speak
from google_play_music import get_song, play_song

speak("Making the recommender and filling it with information")
recommender = MusicRecommender('songs.csv')
recommender.song_feedback(5)
recommender.song_feedback(343)
recommender.song_feedback(234)
recommended = recommender.recommend_song()
song = recommender.get_song_information(recommended)

speak("Recommended song: '{}' by '{}'".format(song['Title'], song['ArtistName']))
try:
    song_gplay = get_song(song['Title'], song['ArtistName'])
    play_song(song_gplay['nid'])
except:
    speak("Sorry, I could not play the recommended song. Exiting.")
