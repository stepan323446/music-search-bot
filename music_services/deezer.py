import requests
from .base import MusicBase, Track

class Deezer(MusicBase):
    def __init__(self):
        service_name = "Deezer"
        service_filter_links = (
            "https://deezer",
            "https://www.deezer",
        )
        super().__init__(service_name, service_filter_links)

    def object_to_track(self, track_object: any) -> Track:
        artist_name = track_object['artist']['name']
        track_title = track_object['title']
        track_link = track_object['link']

        return Track(track_title, 
                    (artist_name, ), 
                    track_link,
                    self.service_name)
    
    def get_track_from_message(self, message) -> Track:
        music_url = self.extract_url_from_text(message)

        # Url not found
        if not music_url:
            return False
        
        track_id = music_url.split('/')[-1]

        # like https://deezer.page.link/ry6x3Tf64HEhHnbT8. Where we don't have id
        if not track_id.isnumeric():
            print(f'[Deezer]: Track hasn\'t id: {track_id}')
            response = requests.get(music_url, allow_redirects=True)

            if not response.status_code == 200:
                print(f'[Deezer]: Redirect not working.')
                return False
            
            final_url = response.url
            track_id = final_url.split('/track/')[-1]

        return self.get_track_by_id(track_id)


    def get_track_by_id(self, track_id) -> Track:
        print(f'[MUSIC][Deezer]: Track id: {track_id}')
        response = requests.get(f'https://api.deezer.com/track/{track_id}')

        if response.status_code == 200:
            print(f'[Deezer]: Track found')
            track_info = response.json()
            
            return self.object_to_track(track_info)
        
        else:
            print(f'[Deezer]: Error - : {response.status_code}')
            return False

    

    def search_track(self, query) -> Track:
        search_url = f'https://api.deezer.com/search/track?q={query}'

        print(f'[Deezer]: Searching "{query}"...')
        response = requests.get(search_url)
        if response.status_code == 200:
            print(f'[Deezer]: Response found')
            search_results = response.json()
        
            # Check we have data from response or not
            if search_results['data']:
                print(f'[Deezer]: Track found')
                first_track = search_results['data'][0]

                return self.object_to_track(first_track)
            else:
                print(f'[Deezer]: Track not found')
                return list()
        
        print(f'[Deezer]: Error. Status code: ' + response.status_code)
        print(response.json())
        return False


