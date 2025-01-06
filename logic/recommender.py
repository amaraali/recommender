import re
import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class Recommender:
    def __init__(self, spotify_model, spotify_client, cache):
        self.model = spotify_model
        self.spotify = spotify_client
        self.cache = cache
        self.data_cleaned = spotify_model.data_cleaned
        self.new_df = spotify_model.new_df
        self.nn_model = spotify_model.nn_model_content
        self.svd_model = spotify_model.svd
        self.data_content_scaled = spotify_model.data_content_scaled

    def extract_track_id_from_url(self, url):
        pattern = r"track/([a-zA-Z0-9]+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        raise ValueError("Invalid Spotify track URL.")

    def get_track_features(self, track_id):
        cached_data = self.cache.get(track_id)
        if cached_data:
            logger.info(f"Cache hit for track_id: {track_id}")
            return cached_data
            
        try:
            track_info = self.spotify.track(track_id)
            audio_features = self.spotify.audio_features([track_id])[0]
            
            track_data = {
                'track_id': track_info['id'],
                'track_name': track_info['name'],
                'artists': ', '.join([artist['name'] for artist in track_info['artists']]),
                'track_genre': 'Unknown',
                'popularity': track_info['popularity'],
                'danceability': audio_features.get('danceability', 0),
                'energy': audio_features.get('energy', 0),
                'acousticness': audio_features.get('acousticness', 0),
                'instrumentalness': audio_features.get('instrumentalness', 0),
                'liveness': audio_features.get('liveness', 0),
                'valence': audio_features.get('valence', 0),
                'tempo': audio_features.get('tempo', 0),
            }
            
            self.cache.set(track_id, track_data)
            return track_data
            
        except Exception as e:
            raise ValueError(f"Error fetching track data: {str(e)}")

    def get_content_based_recommendations(self, track_id, top_n=5):
        scaled_features = self.data_content_scaled
        track_index_map = {track: idx for idx, track in enumerate(self.data_cleaned['track_id'])}
        
        if track_id not in track_index_map:
            raise ValueError(f"Track ID '{track_id}' not found in dataset.")
            
        track_idx = track_index_map[track_id]
        query_vector = scaled_features[track_idx].reshape(1, -1)
        distances, indices = self.nn_model.kneighbors(query_vector, n_neighbors=top_n + 1)

        recommendations = []
        for i, idx in enumerate(indices[0]):
            if idx != track_idx:
                track_info = self.data_cleaned.iloc[idx]
                recommendations.append({
                    'track_id': track_info['track_id'],
                    'track_name': track_info.get('track_name', 'Unknown'),
                    'artists': track_info.get('artists', 'Unknown'),
                    'track_genre': track_info.get('track_genre', 'Unknown'),
                    'similarity_score': 1 - distances[0][i]
                })
            if len(recommendations) >= top_n:
                break

        return recommendations

    def get_collaborative_recommendations(self, user_id, top_n=10):
        all_track_ids = set(self.new_df['track_id'].unique())
        rated_track_ids = set(self.new_df[self.new_df['user_id'] == user_id]['track_id'].unique())
        unrated_track_ids = list(all_track_ids - rated_track_ids)

        predictions = [
            (track_id, self.svd_model.predict(user_id, track_id).est) 
            for track_id in unrated_track_ids
        ]

        return sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]

    def get_hybrid_recommendations(self, user_id, track_id, top_n=10):
        # Get content-based recommendations
        content_recommendations = self.get_content_based_recommendations(track_id, top_n)
        content_scores = {
            rec['track_id']: rec['similarity_score'] for rec in content_recommendations
        }

        # Get collaborative filtering recommendations
        collaborative_recommendations = self.get_collaborative_recommendations(user_id, top_n * 2)
        collaborative_scores = {
            rec[0]: rec[1] for rec in collaborative_recommendations
        }

        # Combine recommendations
        track_ids = set(content_scores.keys()).union(set(collaborative_scores.keys()))
        max_content = max(content_scores.values()) if content_scores else 1
        max_collaborative = max(collaborative_scores.values()) if collaborative_scores else 1

        combined_recommendations = []
        for track_id in track_ids:
            content_score = content_scores.get(track_id, 0) / max_content
            collaborative_score = collaborative_scores.get(track_id, 0) / max_collaborative
            
            final_score = 0.6 * content_score + 0.4 * collaborative_score
            
            track_info = self.data_cleaned[self.data_cleaned['track_id'] == track_id].iloc[0]
            combined_recommendations.append({
                'track_id': track_id,
                'track_name': track_info.get('track_name', 'Unknown'),
                'artists': track_info.get('artists', 'Unknown'),
                'track_genre': track_info.get('track_genre', 'Unknown'),
                'content_score': content_score,
                'collaborative_score': collaborative_score,
                'final_score': final_score
            })

        # Sort and remove duplicates
        combined_recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        unique_recommendations = {}
        for rec in combined_recommendations:
            if rec['track_id'] not in unique_recommendations:
                unique_recommendations[rec['track_id']] = rec
            if len(unique_recommendations) >= top_n:
                break

        return list(unique_recommendations.values())
