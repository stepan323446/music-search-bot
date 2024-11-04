import re
from telegram.ext.filters import MessageFilter
from telegram import Update
from telegram.ext import ContextTypes
from telegram import Message


class Track:
    def __init__(self, 
                 track_name: str, 
                 track_authors: list[str],
                 track_url: str,
                 track_origin_service: str,
                 track_cover: str = None,
                 track_time_length: str = None):
        
        self.name = track_name
        self.authors = track_authors
        self.url = track_url
        self.origin_service = track_origin_service
        self.cover = track_cover
        self.time_length = track_time_length


class MusicFilter(MessageFilter):

    def __init__(self, service_links, name: str | None = None, data_filter: bool = False):
        super().__init__(name, data_filter)
        self.service_links = service_links


    def filter(self, message: Message):
        if not message.text:
            return False

        for service in self.service_links:
            if service in message.text:
                return True

        return False

class MusicBase:

    def __init__(self, service_name: str, service_filter_links: list[str]):
        self.service_name = service_name
        self.service_filter_links = service_filter_links

    def get_tg_filter(self) -> MusicFilter:
        return MusicFilter(self.service_filter_links)
    
    async def tg_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from config import reply_answer_from_bot

        user_message = update.message.text
        track = self.get_track_from_message(user_message)

        if track:
            other_tracks = self.search_track_other_services(track)

            await reply_answer_from_bot(track, other_tracks, update, context)
        else:
            await update.message.reply_text("Track not found")



    def check_contains_url(self, url: str):
        for service_link in self.service_filter_links:
            if url in service_link:
                return True
            
        return False
    
    def extract_url_from_text(self, text):
        # Search url
        url_pattern = r'(https?://[^\s]+)'
        match = re.search(url_pattern, text)

        if match:
            print(f"[MUSIC]: Music link found: {match.group(0)}")
            return match.group(0)
        else:
            return False

    def search_track_other_services(self, track) -> list[Track]:
        from config import SERVICES_ENABLED, get_search_query

        query_track = get_search_query(track)
        tracks = list()        
        for service in SERVICES_ENABLED:
            if service.service_name == self.service_name:
                continue

            track = service.search_track(query_track)
            if track:
                tracks.append(track)

        return tracks

    
    # Need to override this functions
    def search_track(self, query) -> Track:
        pass

    def object_to_track(self, track_object: any) -> Track:
        pass

    def get_track_from_message(self, message) -> Track:
        pass
    
