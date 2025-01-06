import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

class SpotifyModel:
    def __init__(self):
        # Load pre-trained models
        with open('nn_model.pkl', 'rb') as file:
            self.nn_model_content = pickle.load(file)

        with open('svd_model.pkl', 'rb') as file:
            self.svd = pickle.load(file)

        # Load data
        self.data_cleaned = pd.read_csv('data/data_cleaned.csv')
        self.new_df = pd.read_csv('data/user_matrix.csv')

        # Prepare content features
        self.data_content_features = self.data_cleaned[['popularity', 'danceability', 'energy', 
                                                      'acousticness', 'instrumentalness', 
                                                      'liveness', 'valence', 'tempo']]
        self.scaler = StandardScaler()
        self.data_content_scaled = self.scaler.fit_transform(self.data_content_features)
