#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import numpy as np
import pandas as pd
# from sklearn.metrics.pairwise import paired_distances
import re
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from scipy.spatial.distance import euclidean

# Idea: Have a database with for each feature how important it is for the user
# Feature is for example a specific artist
# To suggest a new song, find one with similar features

class MusicRecommender(object):
    """Item-based recommender for songs."""
    def __init__(self, songs_csv_path, preprocessed=True):
        super(MusicRecommender, self).__init__()
        self.songs_csv_path = songs_csv_path
        if preprocessed:
            self.df = pd.read_csv(self.songs_csv_path, index_col=0)
        else:
            self.df = self.preprocess(self.songs_csv_path)
        self.liked_songs = []

        self.used_features = [
            {'name': 'ArtistName', 'type': 'categorical'},
            {'name': 'Tempo', 'type': 'numerical'},
            {'name': 'KeySignature', 'type': 'categorical'},
            {'name': 'Danceability', 'type': 'numerical'},
            {'name': 'ArtistLocation', 'type': 'categorical'}
        ]

        self.vectors = {}
        for column_name in ['ArtistName', 'ArtistLocation', 'KeySignature']:
            counter = Counter(self.df['ArtistName'].values)
            vector = DictVectorizer(sparse=False)
            vector.fit([dict(counter)])
            self.vectors[column_name] = vector
        return

    def preprocess(self, songs_csv_path):
        df = pd.read_csv(songs_csv_path, index_col=0, na_values={'Year': [0], 'ArtistLocation': ["b''"]})
        regex1 = re.compile(r"b'(.*)'\"?")
        regex2 = re.compile(r"b(.*)\"\"")

        def clean_value(x):
            try:
                new_title, n_changes = regex1.subn(r"\1", x)
            except:
                return x
            if n_changes > 0:
                return new_title
            else:
                return regex2.sub(r"\1", x)

        df['Title'] = df['Title'].apply(clean_value)
        df['ArtistName'] = df['ArtistName'].apply(clean_value)
        df['ArtistLocation'] = df['ArtistLocation'].apply(clean_value)
        df['ArtistID'] = df['ArtistID'].apply(clean_value)
        df['SongID'] = df['SongID'].apply(clean_value)
        df['AlbumName'] = df['AlbumName'].apply(clean_value)
        return df

    def get_song_information(self, song_id):
        return self.df.loc[song_id]

    def song_vector(self, song_id, flattened=False):
        song = self.df.loc[song_id]
        song_vector = [song_id]
        for feature in self.used_features:
            name = feature['name']
            if feature['type'] == 'categorical':
                song_vector.append(self.vectors[name].transform([{song[name]: 1}])[0])
            else:
                song_vector.append(song[name])
        if flattened:
            return np.hstack(song_vector)
        else:
            return np.array(song_vector, dtype=np.object)
# song_vector = np.vectorize(song_vector, otypes=np.object)

    def recommend_song(self, sample_size=50):
        """Recommend a song (by giving it's id) based on the user's preferences"""
        # Compute for each song the similarity
        # Return the most similar song
        liked_songs_arr = np.array(self.liked_songs, dtype=np.object)
        liked_songs_ids = liked_songs_arr[:, 0]
        liked_songs_features = liked_songs_arr[:, 1:]
        # print("Making profile")
        profile = []
        for i, feature in enumerate(self.used_features):
            if feature['type'] == 'categorical':
                profile.extend(np.sum(liked_songs_features[:, i]))
            else:
                profile.append(np.mean(liked_songs_features[:, i]))
        profile = np.array(profile)
        # print("Making song vectors")
        songs_subset = np.random.choice(self.df.index, min(sample_size, len(self.df) - len(liked_songs_ids)), replace=False)
        song_vectors = np.array([self.song_vector(i, flattened=True) for i in songs_subset])

        def similarity(x):
            """Calculate the euclidean distance between the profile and the features of a song vector"""
            return euclidean(profile, x)
        # similarity = np.vectorize(similarity)
        # print("Computing similarities")
        # similarities = similarity(song_vectors)
        similarities = [similarity(x) for x in song_vectors[:, 1:]]
        return songs_subset[np.argmin(similarities)]

    def song_feedback(self, song_id, positive=True):
        """Change the preferences of the user based on the feedback given for the song"""
        self.liked_songs.append(self.song_vector(song_id))
        return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path to a CSV file with songs information.")
        sys.exit(1)
    recommender = MusicRecommender(sys.argv[1])
    recommender.song_feedback(5)
    recommender.song_feedback(343)
    recommender.song_feedback(234)
    recommended = recommender.recommend_song()
    song = recommender.get_song_information(recommended)
    print("Recommended: '{}' by '{}'".format(song['Title'], song['ArtistName']))
