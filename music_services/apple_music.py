import requests

from .base import MusicBase, Track

class AppleMusic(MusicBase):
    def __init__(self, token="", storefront="us"):
        service_name = "Apple Music"
        service_filter_links = (
            "music.apple.com",
        )
        super().__init__(service_name, service_filter_links)
        self.storefront = storefront
        self.token = token

    def get_apple_token(self):
        return self.token
    
    def object_to_track(self, track_object: any) -> Track:
        return None

    def get_track_from_message(self, message) -> Track:
        music_url = self.extract_url_from_text(message)

        # Url not found
        if not music_url:
            return False
        
        query_start = music_url.find('?')
        if not query_start != -1:
            return False
        query_string = music_url[query_start + 1:]
        
        params = query_string.split('&')

        for param in params:
            if param.startswith('i='):
                track_id = param.split('=')[1] 
                return self.get_track_by_id(track_id)

        return None

    def get_track_by_id(self, track_id) -> Track:
        print(f'[Apple]: Track id: {track_id}')

        response = requests.get(
            f'https://api.music.apple.com/v1/catalog/{self.storefront}/songs/{track_id}',
            headers={
                'Authorization': f'Bearer {self.get_apple_token()}'
            }
        )

        if response.status_code == 200:
            print(f'[Apple]: Track found')
            print(response.text)
            track_info = response.json()
            
            return self.object_to_track(track_info)
        
        else:
            print(f'[Apple]: Error - : {response.status_code}')
            return False
