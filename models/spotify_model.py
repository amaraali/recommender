import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class SpotifyModel:
    def __init__(self):
        try:
            # Load pre-trained models with error handling
            model_path = 'nn_model.pkl'
            if os.path.exists(model_path):
                with open(model_path, 'rb') as file:
                    self.nn_model_content = pickle.load(file)
            else:
                logger.warning(f"Model file {model_path} not found")
                self.nn_model_content = None

            svd_path = 'svd_model.pkl'
            if os.path.exists(svd_path):
                with open(svd_path, 'rb') as file:
                    self.svd = pickle.load(file)
            else:
                logger.warning(f"Model file {svd_path} not found")
                self.svd = None

            # Load data
            self.data_cleaned = pd.read_csv('data/data_cleaned.csv')
            self.new_df = pd.read_csv('data/user_matrix.csv')

            # Prepare content features
            self.data_content_features = self.data_cleaned[['popularity', 'danceability', 'energy', 
                                                          'acousticness', 'instrumentalness', 
                                                          'liveness', 'valence', 'tempo']]
            self.scaler = StandardScaler()
            self.data_content_scaled = self.scaler.fit_transform(self.data_content_features)

        except Exception as e:
            logger.error(f"Error initializing SpotifyModel: {str(e)}")
            raise
