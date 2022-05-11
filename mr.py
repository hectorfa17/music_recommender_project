import streamlit as st
import pandas as pd
import numpy as np
import pickle
import config
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
from functions import *

hot100_m14k = pd.read_csv('data/dfmodels/hot100_m14k.csv')
nothot_m14k = pd.read_csv('data/dfmodels/nothot_m14k.csv')


def mr():

    song = st.text_input('Input a song you like so we can recommend you something cool: ')

    if (song):
        results = functions.get_audio_features_single(song)
        scaler = pickle.load(open("scalers/standardscaler.pickle","rb"))
        results_scaled = scaler.transform(results)
        results_scaled_df = pd.DataFrame(results_scaled, columns = results.columns)
        model = pickle.load(open("models/kmeans_14.pickle","rb"))
        prediction = model.predict(results_scaled_df)[0]

        if (song in hot100_m14k['songs'].values):
            recommendation = hot100_m14k[hot100_m14k['cluster'] == prediction].sample().index

            st.write('We recommend you: ', hot100_m14k['songs'][recommendation].values[0])
            st.write('From: ',hot100_m14k['artists'][recommendation].values[0])
            st.write('Spotify link: ', get_url(hot100_m14k['songs'][recommendation].values[0]))
            st.image(get_cover(hot100_m14k['songs'][recommendation].values[0]))

        else:
            recommendation = nothot_m14k[nothot_m14k['cluster'] == prediction].sample().index
            st.write('We recommend you: ', nothot_m14k['songs'][recommendation].values[0])
            st.write('From: ',nothot_m14k['artists'][recommendation].values[0])
            st.write('Spotify link: ', get_url(nothot_m14k['songs'][recommendation].values[0]))
            st.image(get_cover(nothot_m14k['songs'][recommendation].values[0]))

 
        