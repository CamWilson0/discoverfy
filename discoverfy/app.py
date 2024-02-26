import requests
import base64
from flask import Flask, render_template, request
import json
import random

app = Flask(__name__, template_folder='templates')



client_id = '9c6d601fd446419dbd6e2860debd3bcd'
client_secret = '256d9428794e4d899cf2a2bdcb0756e0'

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        json_result = response.json()
        token = json_result.get("access_token")
        if token:
            return token
        else:
            print("Failed to retrieve access token.")
            return None
    except Exception as e:
        print("Exception occurred while getting token:", e)
        return None

token = get_token()


# Function to get a random artist from a given genre with popularity score < 20
def get_random_artist(genre, access_token):
    # Spotify API endpoint for searching artists
    url = 'https://api.spotify.com/v1/search'

    # Parameters for the API request
    params = {
        'q': f'genre:"{genre}"',
        'type': 'artist',
        'limit': 50,  # Limiting the number of results to 50 per page
        'offset': 0    # Start from the first page
    }

    # Authorization header with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # List to store artists with low popularity scores
    low_popularity_artists = []

    # Sending GET requests to Spotify API and paginating through the results
    while True:
        # Sending the GET request to Spotify API
        response = requests.get(url, params=params, headers=headers)

        # Parsing the JSON response
        data = response.json()

        # Extracting the list of artists from the current page
        artists = data['artists']['items']

        # Filtering artists with popularity score < 20
        for artist in artists:
            if genre in ('rap', 'hip-hop', 'edm', 'indie','pop', 'jazz', 'lo-fi'):
                if artist['popularity'] < 60:
                    low_popularity_artists.append(artist)
            else:
                if artist['popularity'] < 20:
                    low_popularity_artists.append(artist)

        # Checking if there are more pages to fetch
        if data['artists']['next']:
            # Update offset to fetch the next page
            params['offset'] += params['limit']
        else:
            break  # Break the loop if there are no more pages

        

        
    # Selecting a random artist from the list of artists with low popularity scores

    random_artist = random.choice(low_popularity_artists)


    return random_artist

@app.route('/')
def home():
    return render_template('index.html')

# Route for handling form submission
@app.route('/get_artist', methods=['POST'])
def get_artist():
    # Get the user input from the form
    genre = request.form['genre']
    access_token =  token

    # Get a random artist based on the genre
    random_artist = get_random_artist(genre, access_token)
    artist_spotify = random_artist['external_urls']['spotify']
    # Render the template with the random artist's name
    return render_template('result.html', artist=random_artist['name'], popularity=random_artist['popularity']), artist_spotify
    
if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0' )
