import requests
import base64

from .base import MusicBase, Track

class Spotify(MusicBase):
    def __init__(self, spotify_client_id, spotify_client_secret):
        service_name = "Spotify"
        service_filter_links = (
            "https://open.spotify.com",
            "https://www.open.spotify.com"
        )
        super().__init__(service_name, service_filter_links)
        
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        

    def get_spotify_token(self):
        credentials = f"{self.spotify_client_id}:{self.spotify_client_secret}"
        credentials_b64 = base64.b64encode(credentials.encode()).decode()

        # Request token for spotify
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': f'Basic {credentials_b64}',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'grant_type': 'client_credentials'
            }
        )

        # Get token from response
        token = response.json()['access_token']
        print(f'[Spotify]: Got token: {token}')
        return token

    def object_to_track(self, track_object: any) -> Track:
        track_id = track_object['id']

        artists = list()
        for artist_obj in track_object['artists']:
            artists.append(artist_obj['name'])

        track_title = track_object['name']
        track_cover = track_object['album']['images'][0]['url']
        track_link = track_object['external_urls']['spotify']

        
        track_duration = track_object['duration_ms'] // 1000
        track_date = track_object['album']['release_date']

        return Track(
                    id              =   track_id,
                    name            =   track_title, 
                    authors         =   artists,
                    url             =   track_link,
                    origin_service  =   self.service_name,
                    cover           =   track_cover,
                    time_length     =   track_duration,
                    realese_date    =   track_date)

    def get_track_from_message(self, message) -> Track:
        music_url = self.extract_url_from_text(message)

        # Url not found
        if not music_url:
            return False
        
        track_id = music_url.split('/')[-1].split('?')[0]

        return self.get_track_by_id(track_id)
    
    def get_track_by_id(self, track_id) -> Track:
        print(f'[MUSIC][Spotify]: Track id: {track_id}')

        response = requests.get(
            f'https://api.spotify.com/v1/tracks/{track_id}',
            headers={
                'Authorization': f'Bearer {self.get_spotify_token()}'
            }
        )

        if response.status_code == 200:
            print(f'[MUSIC][Spotify]: Track found')
            track_info = response.json()
            
            return self.object_to_track(track_info)
        
        else:
            print(f'[Spotify]: Error - : {response.status_code}')
            return False
        
    def search_track(self, query):
        access_token = self.get_spotify_token()
        if not access_token:
            print(f'[Spotify]: Token not found')
            return None

        print(f'[Spotify]: Searching track "{query}"...')
        
        search_url = f'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        params = {
            'q': query,
            'type': 'track',
            'limit': 1
        }
        
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            print(f'[Spotify]: Response found')
            search_results = response.json()
            
            # Проверяем, есть ли найденные треки
            if search_results['tracks']['items']:
                print(f'[Spotify]: Track found')
                first_track = search_results['tracks']['items'][0]

                return self.object_to_track(first_track)
            else:
                print(f'[Spotify]: Track not found')
                return None
        else:
            print(f'[Spotify]: Error - : {response.status_code}')
            return None