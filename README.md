# Spotify Music Recommender

## Introduction
The Spotify Music Recommender is a hybrid recommendation system built using Streamlit, designed to provide personalized music suggestions. This system combines content-based filtering and collaborative filtering approaches to generate diverse and accurate recommendations based on user behavior and track features.

---

## Features
- **Content-Based Filtering**: Recommends songs similar to a given track using musical features such as danceability, energy, and tempo.
- **Collaborative Filtering**: Suggests songs based on user-item interaction data and preferences.
- **Hybrid Recommendations**: Combines content-based and collaborative scores with adjustable weights to generate the final recommendations.
- **Spotify Integration**: Fetches track details and audio features directly from Spotify using their API.
- **Interactive Interface**: User-friendly web interface built with Streamlit, allowing users to input parameters and view results instantly.

---

## Installation

### Prerequisites
1. **Python 3.8 or later**
2. **Spotify API Credentials**: Register an app on [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and get your `Client ID` and `Client Secret`.

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/amaraali/recommender.git
    cd recommender
    ```
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a `config.yaml` file in the root directory with the following format:
    ```yaml
    SPOTIFY_CLIENT_ID: "your_client_id_here"
    SPOTIFY_CLIENT_SECRET: "your_client_secret_here"
    ```
4. Run the application:
    ```bash
    streamlit run app.py
    ```

---

## Usage
1. Open the application in your browser (usually at `http://localhost:8501`).
2. Enter your **User ID** and a **Spotify Track ID** or **Spotify URL** in the input fields.
3. Adjust the number of recommendations you want.
4. Click on **Get Recommendations** to view results.

---

## File Structure
- `app.py`: Main Streamlit application.
- `config.yaml`: Contains Spotify API credentials.
- `nn_model.pkl`: Pre-trained content-based model.
- `svd_model.pkl`: Pre-trained collaborative filtering model.
- `data_cleaned.csv`: Cleaned dataset with track information.
- `user_matrix.csv`: User-item interaction matrix.

---

## Technologies Used
- **Streamlit**: For building the web interface.
- **Spotipy**: For interacting with the Spotify API.
- **Scikit-learn**: For preprocessing and implementing content-based filtering.
- **Surprise**: For collaborative filtering using the SVD algorithm.

---

## Known Issues
- Spotify API rate limits may cause delays in fetching track details. Implement caching to minimize API calls.
- Some tracks may not have complete audio features, resulting in limited content-based recommendations.

---

## Future Enhancements
- Add user authentication for personalized recommendations.
- Integrate additional data sources for more robust recommendations.
- Improve the interface with more visualization options.

---