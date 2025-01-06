import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

logger = logging.getLogger(__name__)

def load_config():
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)

def initialize_spotify_client():
    try:
        config = load_config()
        client_credentials_manager = SpotifyClientCredentials(
            client_id=config['SPOTIFY_CLIENT_ID'],
            client_secret=config['SPOTIFY_CLIENT_SECRET']
        )
        return spotipy.Spotify(
            client_credentials_manager=client_credentials_manager,
            requests_timeout=10,
            retries=3
        )
    except Exception as e:
        logger.error(f"Failed to initialize Spotify client: {str(e)}")
        return None
