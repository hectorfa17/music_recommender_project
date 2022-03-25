#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import math
import pickle
import pandas as pd
import sys
from config import *
#sys.path.insert(1, '/Users/Hector_Martin/Documents/Labs/music_recommender_project/config.py')
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
import glob 
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret_id))


def hot100(link):

    
    music = requests.get(link)
    soup = BeautifulSoup(music.content, 'html.parser')
    
    songs = []
    for title in soup.select("li.o-chart-results-list__item > h3"):
        songs.append(title.get_text().strip())#strip removes adjacent characters to text 
    
    artists = []
    
    for artist in soup.select("li.o-chart-results-list__item > span.c-label"):
        artists.append(artist.get_text().strip())

    artists = [number for number in artists if not number.isdigit()]
    
    removal = ['-','NEW','RE-\nENTRY']

    for items in artists:
        for x in removal:
            if x in artists:
                artists.remove(x)

    hot100 = pd.DataFrame({"songs": songs, "artists": artists})
    
    hot100.to_csv("hot100.csv", index=False)
    
    return hot100

def get_audio_features_single(song):


    
    black = {'danceability': "Null", 
           'energy': "Null", 
           'key': "Null",
           'loudness': "Null", 
           'mode':"Null", 
           'speechiness': "Null", 
           'acousticness': "Null", 
           'instrumentalness': "Null", 
            'liveness': "Null", 
            'valence': "Null", 
            'tempo': "Null", 
            'type': "Null", 
            'id': "Null", 
            'uri': "Null", 
            'track_href': "Null", 
            'analysis_url': "Null", 
            'duration_ms': "Null", 
            'time_signature': "Null"}
    

    keys = list(black.keys())
    
    song_ids = []
    
    result = sp.search(q=song, limit=1)
    #print("Looking for song: ",song)
    song_ids.append(result['tracks']['items'][0]['id'])
    #print("Getting audio features")
    audio_feats = [sp.audio_features(song_id)[0] if ((song_id != None) and ( song_id != "")) else black for song_id in song_ids]
    name = "audio_feats_" + str(song) + ".pkl"
    with open(name, "wb") as handle:
        pickle.dump(audio_feats,handle)
    #print("Created file: ",name)
        
    #Grouping the files together in a list:
        
    pkls = glob.glob("*.pkl")
    pkls.sort()
    pkls
        
    df = pd.DataFrame()
        
    for i, pkl in enumerate(pkls):    
        try:
            #print(pkl)
            with open(pkl, "rb") as handle:
                audio_feats = pickle.load(handle)
                audio_feats_df = pd.DataFrame(audio_feats)
                df = pd.concat([df,audio_feats_df],axis = 0).reset_index(drop=True)
                os.remove(pkl)
                    
        except:
            #print("Corrupted",pkl)
            continue
                             
    df_clean = df.drop(['analysis_url', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature', 'type'],axis =1)
    
    for column in df_clean.columns:
        df_clean[column] = pd.to_numeric(df_clean[column], errors ='coerce')



    
    return df_clean

def get_audio_features_big(list_of_songs):

    
    song_ids = []

    black = {'danceability': "Null", 
           'energy': "Null", 
           'key': "Null",
           'loudness': "Null", 
           'mode':"Null", 
           'speechiness': "Null", 
           'acousticness': "Null", 
           'instrumentalness': "Null", 
            'liveness': "Null", 
            'valence': "Null", 
            'tempo': "Null", 
            'type': "Null", 
            'id': "Null", 
            'uri': "Null", 
            'track_href': "Null", 
            'analysis_url': "Null", 
            'duration_ms': "Null", 
            'time_signature': "Null"}
    
    keys = list(black.keys())
    
    df = pd.DataFrame()
    chunks = math.ceil(len(list_of_songs)/1000)
    for i in range(chunks): # chunks = 4 -> 0,1,2,3
        song_ids = []
        if ( i < chunks-1 ):
            j = i + 1
        else:
            j = len(list_of_songs)
        for index, song in enumerate(list_of_songs[1000*i:1000*j]): #[0:1000],[1000:2000],[2000:3000],[3000:]
            print("Looking for song: ",index)
            try:
                songs = sp.search(q=song, limit=1)
                song_ids.append(songs['tracks']['items'][0]['id'])
            except: # Si no esta no se para.
                print(song)
                song_ids.append("")
    
        print("Getting audio features")
        audio_feats = [sp.audio_features(song_id)[0] if ((song_id != None) and ( song_id != "")) else black for song_id in song_ids]
        name = "audio_feats_" + str(i) + ".pkl"
        with open(name, "wb") as handle:
            pickle.dump(audio_feats,handle)
        print("Created file: ",name)
        sleep(30)
        print('Sleeping for 30 seconds')
        
        #Grouping the files together in a list:
        
    pkls = glob.glob("*.pkl")
    pkls.sort()
    pkls
        
    df = pd.DataFrame()
        
    for i, pkl in enumerate(pkls):    
        try:
            print(pkl)
            with open(pkl, "rb") as handle:
                audio_feats = pickle.load(handle)
                audio_feats_df = pd.DataFrame(audio_feats)
                df = pd.concat([df,audio_feats_df],axis = 0).reset_index(drop=True)
                    
        except:
            print("Corrupted",pkl)
            continue
                             
    return df


def add_audio_features(df, audio_features_df, csvname):  
    if df.shape <=(100, df.columns):
        df_concat = pd.concat([df, audio_features_df], axis =1)
        df_concat = df_concat[df_concat['mode'] != 'Null']
        df_concat = df_concat.reset_index(drop=True)
        df_concat.to_csv(csvname+'.csv', index=False)
        return df_concat
    else:
        df = df.drop(df.index[1000:2000]).reset_index(drop=True)
        df_concat = pd.concat([df, audio_features_df], axis =1)
        df_concat = df_concat[df_concat['mode'] != 'Null']
        df_concat = df_concat.reset_index(drop=True)
        df_concat.to_csv(csvname+'.csv', index=False)
        return df_concat


def concatallsongs(dfhotconcat,dfnothotconcat,csvname):
    df_allsongsconcat = pd.concat([dfhotconcat, dfnothotconcat], axis =0).reset_index(drop=True)
    df_allsongsconcat = df_allsongsconcat[df_allsongsconcat['mode'] != 'Null']
    df_allsongsconcat = df_allsongsconcat.reset_index(drop=True)
    df_allsongsconcat.to_csv(csvname+'.csv', index=False)
    return df_allsongsconcat

def get_cover(song_title):
    result = sp.search(q=song_title, limit=1)
    cover = result['tracks']['items'][0]['album']['images'][0]['url']
    return cover

def get_url(song_title):
    result = sp.search(q=song_title, limit=1)
    url = result['tracks']['items'][0]['external_urls']['spotify']
    return url





