async function getRandomArtist() {
    const genre = document.getElementById('genreInput').value.trim();
    if (genre === '') {
        alert('Please enter a genre');
        return;
    }

    const clientId = '9c6d601fd446419dbd6e2860debd3bcd';
    const clientSecret = '256d9428794e4d899cf2a2bdcb0756e0';

    const tokenResponse = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret)
        },
        body: 'grant_type=client_credentials'
    });

    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;
    console.log(accessToken);

    const searchResponse = await fetch(`https://api.spotify.com/v1/search?q=genre:${genre}&type=artist&market=US&limit=50`, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
        
    });
    const data = null;

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
	if (this.readyState === this.DONE) {
		console.log(this.responseText);
	}
    });

    xhr.open('GET', 'https://spotify-artist-monthly-listeners.p.rapidapi.com/artists/spotify_artist_monthly_listeners?spotify_artist_id=66CXWjxzNUsdJxJ2JdwvnR');
    xhr.setRequestHeader('X-RapidAPI-Key', 'b1c0d2ab3bmsh3423ab435788a0ep1a728cjsneb122fb64986');
    xhr.setRequestHeader('X-RapidAPI-Host', 'spotify-artist-monthly-listeners.p.rapidapi.com');

    xhr.send(data);
}

