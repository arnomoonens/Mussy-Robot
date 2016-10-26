#!/usr/bin/python
# -*- coding: utf8 -*-

# import sys
import numpy as np
import pandas as pd
# from sklearn.metrics.pairwise import paired_distances
# import re
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from scipy.spatial.distance import euclidean

# Idea: Have a database with for each feature how important it is for the user
# Feature is for example a specific artist
# To suggest a new song, find one with similar features


# Dataframe with all song information
# df = pd.read_csv('SongCSV.csv', index_col=0, na_values={'Year': [0], 'ArtistLocation': ["b''"]})
# Preprocessing
# regex1 = re.compile(r"b'(.*)'\"?")
# regex2 = re.compile(r"b(.*)\"\"")
# def clean_value(x):
#     try:
#         new_title, n_changes = regex1.subn(r"\1", x)
#     except:
#         return x
#     if n_changes > 0:
#         return new_title
#     else:
#         return regex2.sub(r"\1", x)

# df['Title'] = df['Title'].apply(clean_value)
# df['ArtistName'] = df['ArtistName'].apply(clean_value)
# df['ArtistLocation'] = df['ArtistLocation'].apply(clean_value)
# df['ArtistID'] = df['ArtistID'].apply(clean_value)
# df['SongID'] = df['SongID'].apply(clean_value)
# df['AlbumName'] = df['AlbumName'].apply(clean_value)

liked_songs = []

used_features = [
    {'name': 'ArtistName', 'type': 'categorical'},
    {'name': 'Tempo', 'type': 'numerical'},
    {'name': 'KeySignature', 'type': 'categorical'},
    {'name': 'Danceability', 'type': 'numerical'},
    {'name': 'ArtistLocation', 'type': 'categorical'}
]


df = pd.read_csv('songs.csv', index_col=0)

vectors = {}
for column_name in ['ArtistName', 'ArtistLocation', 'KeySignature']:
    counter = Counter(df['ArtistName'].values)
    vector = DictVectorizer(sparse=False)
    vector.fit([dict(counter)])
    vectors[column_name] = vector

def song_vector(song_id, flattened=False):
    song = df.loc[song_id]
    song_vector = []
    for feature in used_features:
        name = feature['name']
        if feature['type'] == 'categorical':
            song_vector.append(vectors[name].transform([{song[name]: 1}])[0])
        else:
            song_vector.append(song[name])
    if flattened:
        return np.hstack(song_vector)
    else:
        return np.array(song_vector)
# song_vector = np.vectorize(song_vector, otypes=np.object)

def recommend_song(sample_size=50):
    """Recommend a song (by giving it's id) based on the user's preferences"""
    # Compute for each song the similarity
    # Return the most similar song
    liked_songs_arr = np.array(liked_songs)
    # print("Making profile")
    profile = []
    for i, feature in enumerate(used_features):
        if feature['type'] == 'categorical':
            profile.extend(np.sum(liked_songs_arr[:, i]))
        else:
            profile.append(np.mean(liked_songs_arr[:, i]))
    profile = np.array(profile)
    # print("Making song vectors")
    songs_subset = np.random.choice(df.index, sample_size, replace=False)
    song_vectors = np.array([song_vector(i, flattened=True) for i in songs_subset])

    def similarity(x):
        return euclidean(profile, x)
    # similarity = np.vectorize(similarity)
    # print("Computing similarities")
    # similarities = similarity(song_vectors)
    similarities = [similarity(x) for x in song_vectors]
    return songs_subset[np.argmin(similarities)]

def song_feedback(song_id, positive):
    """Change the preferences of the user based on the feedback given for the song"""
    liked_songs.append(song_vector(song_id))
    return

if __name__ == '__main__':
    song_feedback(5, True)
    song_feedback(343, True)
    song_feedback(234, True)
    print("Recommended:", recommend_song())
