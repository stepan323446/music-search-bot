from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from music_services.base import Track

# Services
from music_services.deezer import Deezer
from music_services.spotify import Spotify

# Set envs
from pathlib import Path
import dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
dotenv_file = os.path.join(BASE_DIR, ".env")
print(BASE_DIR)
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Telegram bot token
BOT_TOKEN = os.environ['BOT_TOKEN']

# Other service credentials
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

# Set services where will search tracks
SERVICES_ENABLED = (
    Deezer(),
    Spotify(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
)



# Set answer template
async def reply_answer_from_bot(origin_track: Track,
                                service_tracks: list[Track], 
                                update: Update, 
                                context: ContextTypes.DEFAULT_TYPE):
    
    # Append other tracks from different services
    other_tracks_str = ''
    for track in service_tracks:
        if not track:
            continue

        other_tracks_str += f"{track.origin_service}: <a href=\"{track.url}\">{track.name} - {track.authors[0]}</a>\n"

    # Send message
    await update.message.reply_text(
        f"""
<b>Track: {origin_track.name}</b>
<i>Authors: {", ".join(origin_track.authors)}</i>
<i>Time: {origin_track.get_time()}</i>

<b>Other services:</b>
{other_tracks_str}
<i>Search query:</i> <code>{get_search_query(origin_track)}</code>
""", 
        ParseMode.HTML, disable_web_page_preview=True)

# Set search query for tracks in different services
def get_search_query(track: Track):
    return f'{track.name} {track.authors[0]}'