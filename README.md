![](images/logoslogan.png)

## Overview

- Music recommender app that based on the input of a song proposed by the User, it recommends either a hot nowdays mainstream song or a classic hit from the past. 
- The application is built with Python, using a K-Means Machine Learning model to cluster songs by similarities between audio features
- The audio features have been collected from Spotify using the Spotipy API.

## Contents

- Application: you can find it by clicking the following [link](https://song-recommender-hfontenla.herokuapp.com/)

- Notebooks
1. `main.ipynb` - It contains all the processes from the notebooks listed below condensed in a single file. Functions are called from a separate module.
2. `100hotsongs_scrapper.ipynb` - Web scrapper to obtain 100 nowadays mainstream songs DataFrame.
3. `nothotsongs.ipynb`- Creating the DataFrame containing classic hits.
4. `spotipy_api_webscrapper.ipynb`- Using the Spotipy API to get the audio features of all songs.
5. `clustering_songs_from_dataframes.ipynb`- Clustering the songs by similarities between audio features using the K-Means Machine Learning model. Several models are trained and you can choose which model to use based on the Silhouette or the Elbow method.

- Custom modules 
1. `deploy.py` - Main app file that runs all modules.
2. `music_recommender.py` - Separate module with the music_recommender core code.
3. `functions.py` - Separate module with all the functions I used.

- Other folders
1. data - Contains all the Datasets used in this project
2. data/dfmodels - Contains predefined DataFrames based on the top performance K-Means model I trained.
3. models - Contains all the fitted Models stored in pkl files.
4. scalers - Contains a fitted scaler stored in a pkl file.
5. audiofeats - Contains audio features collected using a function defined in the `spotipy_api_webscrapper.ipynb` Notebook. 

## Original Datasets:

-  `data/hot100.csv` - Obtained through webscrapping this [website](https://www.billboard.com/charts/hot-100)
-  `data/EvolutionPopUSA_MainData` - Obtained from [Kaggle](https://www.kaggle.com/).

## Acknowledgements:

- Thanks to Kaggle [this link](https://www.kaggle.com/) the DataFrame of Classic Hits. Sadly enough I could not find again the exact link where I got the data from.
- Thanks to Ignacio Soteras, my teacher from Ironhack for all the help during the process
- Thanks to Maria Soriano for all the help with Streamlit


## Installation and use:

1. Clone this repo
2. Install all the requirements from the requirements.txt file
3. Navigate through the Notebooks
